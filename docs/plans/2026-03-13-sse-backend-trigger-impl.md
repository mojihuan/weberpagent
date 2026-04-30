# SSE 后端触发模式实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将执行触发从前端移到后端，前端只负责订阅 SSE 流展示进度

**Architecture:** 创建 run 时立即启动后台执行任务，EventManager 管理事件发布/订阅，前端通过 GET 请求订阅 SSE 流

**Tech Stack:** Python 3.11, FastAPI, asyncio, React 18, EventSource API

---

## Task 1: 创建 EventManager 单元测试

**Files:**
- Create: `backend/tests/test_event_manager.py`

**Step 1: 编写 EventManager 测试**

```python
# backend/tests/test_event_manager.py
import pytest
import asyncio
from backend.core.event_manager import EventManager


@pytest.fixture
def event_manager():
    return EventManager()


class TestEventManager:
    """EventManager 单元测试"""

    @pytest.mark.asyncio
    async def test_publish_and_subscribe(self, event_manager):
        """测试发布和订阅事件"""
        run_id = "test-run-1"

        # 发布事件
        await event_manager.publish(run_id, "event: test\ndata: hello\n\n")

        # 订阅并获取事件
        events = []
        async for event in event_manager.subscribe(run_id):
            events.append(event)
            break  # 只获取一个事件

        assert len(events) == 1
        assert events[0] == "event: test\ndata: hello\n\n"

    @pytest.mark.asyncio
    async def test_multiple_events(self, event_manager):
        """测试多个事件"""
        run_id = "test-run-2"

        # 发布多个事件
        await event_manager.publish(run_id, "event: started\ndata: 1\n\n")
        await event_manager.publish(run_id, "event: step\ndata: 2\n\n")
        await event_manager.publish(run_id, None)  # 结束信号

        # 订阅获取所有事件
        events = []
        async for event in event_manager.subscribe(run_id):
            if event is None:
                break
            events.append(event)

        assert len(events) == 2

    @pytest.mark.asyncio
    async def test_is_finished(self, event_manager):
        """测试执行状态检查"""
        run_id = "test-run-3"

        assert event_manager.is_finished(run_id) is False

        event_manager.set_status(run_id, "success")
        assert event_manager.is_finished(run_id) is True

        event_manager.set_status(run_id, "failed")
        assert event_manager.is_finished(run_id) is True

        event_manager.set_status(run_id, "running")
        assert event_manager.is_finished(run_id) is False

    @pytest.mark.asyncio
    async def test_reconnect_gets_history(self, event_manager):
        """测试重新连接获取历史事件"""
        run_id = "test-run-4"

        # 发布事件
        await event_manager.publish(run_id, "event: started\ndata: 1\n\n")
        await event_manager.publish(run_id, "event: step\ndata: 2\n\n")

        # 标记完成
        event_manager.set_status(run_id, "success")

        # 订阅应该获取历史事件
        events = []
        async for event in event_manager.subscribe(run_id):
            if event is None:
                break
            events.append(event)

        assert len(events) == 2

    @pytest.mark.asyncio
    async def test_cleanup(self, event_manager):
        """测试清理资源"""
        run_id = "test-run-5"

        await event_manager.publish(run_id, "event: test\ndata: 1\n\n")
        event_manager.cleanup(run_id)

        # 清理后历史应该为空
        events = event_manager._events.get(run_id, [])
        assert len(events) == 0
```

**Step 2: 运行测试验证失败**

```bash
cd /Users/huhu/project/weberpagent && source .venv/bin/activate && python -m pytest backend/tests/test_event_manager.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'backend.core.event_manager'"

---

## Task 2: 实现 EventManager

**Files:**
- Create: `backend/core/event_manager.py`

**Step 1: 编写 EventManager 实现**

```python
# backend/core/event_manager.py
"""SSE 事件管理器 - 管理执行事件的发布和订阅"""

import asyncio
from collections import defaultdict
from typing import AsyncGenerator


class EventManager:
    """
    管理执行事件的发布和订阅

    - 存储事件历史，支持重新连接
    - 支持多个并发订阅者
    - 自动清理完成的执行
    """

    def __init__(self):
        # run_id -> 事件列表
        self._events: dict[str, list[str | None]] = defaultdict(list)
        # run_id -> 订阅者队列列表
        self._subscribers: dict[str, list[asyncio.Queue]] = defaultdict(list)
        # run_id -> 执行状态
        self._status: dict[str, str] = {}

    async def publish(self, run_id: str, event: str | None) -> None:
        """
        发布事件到指定 run

        Args:
            run_id: 执行 ID
            event: SSE 事件字符串，None 表示执行结束
        """
        # 存储事件历史
        if event is not None:
            self._events[run_id].append(event)

        # 通知所有订阅者
        for queue in self._subscribers.get(run_id, []):
            await queue.put(event)

    async def subscribe(self, run_id: str) -> AsyncGenerator[str | None, None]:
        """
        订阅 run 的事件流

        Args:
            run_id: 执行 ID

        Yields:
            SSE 事件字符串，None 表示流结束
        """
        queue: asyncio.Queue[str | None] = asyncio.Queue()
        self._subscribers[run_id].append(queue)

        try:
            # 先发送历史事件
            for event in self._events.get(run_id, []):
                yield event

            # 如果已经完成，直接结束
            if self.is_finished(run_id):
                return

            # 等待新事件
            while True:
                event = await queue.get()
                yield event
                if event is None:  # 结束信号
                    break
        finally:
            # 移除订阅者
            if queue in self._subscribers[run_id]:
                self._subscribers[run_id].remove(queue)

    def set_status(self, run_id: str, status: str) -> None:
        """
        设置执行状态

        Args:
            run_id: 执行 ID
            status: 状态 (running, success, failed, stopped)
        """
        self._status[run_id] = status

    def is_finished(self, run_id: str) -> bool:
        """
        检查执行是否已结束

        Args:
            run_id: 执行 ID

        Returns:
            True 如果执行已成功或失败
        """
        return self._status.get(run_id) in ("success", "failed", "stopped")

    def cleanup(self, run_id: str) -> None:
        """
        清理执行资源

        Args:
            run_id: 执行 ID
        """
        if run_id in self._events:
            del self._events[run_id]
        if run_id in self._subscribers:
            del self._subscribers[run_id]
        if run_id in self._status:
            del self._status[run_id]


# 全局单例
event_manager = EventManager()
```

**Step 2: 运行测试验证通过**

```bash
cd /Users/huhu/project/weberpagent && source .venv/bin/activate && python -m pytest backend/tests/test_event_manager.py -v
```

Expected: PASS (6 tests)

**Step 3: 提交**

```bash
git add backend/core/event_manager.py backend/tests/test_event_manager.py
git commit -m "feat: 添加 EventManager 管理 SSE 事件发布/订阅"
```

---

## Task 3: 修改 runs.py - 添加 stream endpoint

**Files:**
- Modify: `backend/api/routes/runs.py`

**Step 1: 添加导入和 stream endpoint**

在文件顶部添加导入：

```python
# 在现有导入后添加
from backend.core.event_manager import event_manager
```

在 `get_run` endpoint 后添加新的 stream endpoint：

```python
@router.get("/{run_id}/stream")
async def stream_run(
    run_id: str,
    run_repo: RunRepository = Depends(get_run_repo),
):
    """SSE 订阅执行流"""
    # 验证 run 存在
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    async def event_generator():
        async for event in event_manager.subscribe(run_id):
            if event is None:
                break
            yield event

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
```

**Step 2: 验证语法正确**

```bash
cd /Users/huhu/project/weberpagent && source .venv/bin/activate && python -c "from backend.api.routes.runs import router; print('OK')"
```

Expected: OK

**Step 3: 提交**

```bash
git add backend/api/routes/runs.py
git commit -m "feat: 添加 GET /runs/{id}/stream SSE 订阅 endpoint"
```

---

## Task 4: 修改 create_run 启动后台执行

**Files:**
- Modify: `backend/api/routes/runs.py`

**Step 1: 添加后台执行函数**

在 `router` 定义之前添加：

```python
async def run_agent_background(run_id: str, task_name: str, task_description: str, max_steps: int):
    """后台执行 agent 任务"""
    from backend.db.database import async_session
    from backend.db.repository import RunRepository, StepRepository
    from backend.core.agent_service import AgentService
    from backend.db.schemas import SSEStartedEvent, SSEStepEvent, SSEFinishedEvent, SSEErrorEvent

    async with async_session() as session:
        run_repo = RunRepository(session)
        step_repo = StepRepository(session)
        agent_service = AgentService()

        await run_repo.update_status(run_id, "running")

        # 发送 started 事件
        started = SSEStartedEvent(run_id=run_id, task_name=task_name)
        await event_manager.publish(run_id, f"event: started\ndata: {started.model_dump_json()}\n\n")

        step_count = 0

        async def on_step(step: int, action: str, reasoning: str, screenshot_path: str | None):
            nonlocal step_count
            step_count = step

            # 保存步骤到数据库
            step_data = {
                "step_index": step,
                "action": action,
                "reasoning": reasoning,
                "screenshot_path": screenshot_path,
                "status": "success",
                "duration_ms": 0,
            }
            await step_repo.add_step(run_id, step_data)

            # 构造截图 URL
            screenshot_url = f"/api/runs/{run_id}/screenshots/{step}" if screenshot_path else None

            # 发送 step 事件
            event = SSEStepEvent(
                index=step,
                action=action,
                reasoning=reasoning,
                screenshot_url=screenshot_url,
                status="success",
                duration_ms=0,
            )
            await event_manager.publish(run_id, f"event: step\ndata: {event.model_dump_json()}\n\n")

        try:
            result = await agent_service.run_with_streaming(
                task=task_description,
                run_id=run_id,
                on_step=on_step,
                max_steps=max_steps,
            )

            # 发送 finished 事件
            final_status = "success" if result.is_successful() else "failed"
            await run_repo.update_status(run_id, final_status)
            event_manager.set_status(run_id, final_status)

            finished = SSEFinishedEvent(
                status=final_status,
                total_steps=step_count,
                duration_ms=0,
            )
            await event_manager.publish(run_id, f"event: finished\ndata: {finished.model_dump_json()}\n\n")

        except Exception as e:
            await run_repo.update_status(run_id, "failed")
            event_manager.set_status(run_id, "failed")

            error = SSEErrorEvent(error=str(e))
            await event_manager.publish(run_id, f"event: error\ndata: {error.model_dump_json()}\n\n")

        finally:
            await event_manager.publish(run_id, None)  # 结束信号
```

**Step 2: 修改 create_run endpoint**

替换现有的 `create_run` 函数：

```python
@router.post("", response_model=RunResponse)
async def create_run(
    task_id: str,
    background_tasks: BackgroundTasks,
    task_repo: TaskRepository = Depends(get_task_repo),
    run_repo: RunRepository = Depends(get_run_repo),
):
    """创建执行记录并启动后台执行"""
    from fastapi import BackgroundTasks

    task = await task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    run = await run_repo.create(task_id=task_id)

    # 启动后台执行
    background_tasks.add_task(
        run_agent_background,
        run.id,
        task.name,
        task.description,
        task.max_steps,
    )

    return run
```

**Step 3: 添加 BackgroundTasks 导入**

在文件顶部的导入中添加：

```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
```

**Step 4: 验证语法正确**

```bash
cd /Users/huhu/project/weberpagent && source .venv/bin/activate && python -c "from backend.api.routes.runs import router; print('OK')"
```

Expected: OK

**Step 5: 提交**

```bash
git add backend/api/routes/runs.py
git commit -m "feat: create_run 启动后台执行任务"
```

---

## Task 5: 删除旧的 execute endpoint

**Files:**
- Modify: `backend/api/routes/runs.py`

**Step 1: 删除 execute_run endpoint**

删除 `@router.post("/{run_id}/execute")` 及其整个函数（约 110 行代码）。

**Step 2: 验证语法正确**

```bash
cd /Users/huhu/project/weberpagent && source .venv/bin/activate && python -c "from backend.api.routes.runs import router; print('OK')"
```

Expected: OK

**Step 3: 提交**

```bash
git add backend/api/routes/runs.py
git commit -m "refactor: 删除旧的 POST /runs/{id}/execute endpoint"
```

---

## Task 6: 修改前端 useRunStream 使用 GET

**Files:**
- Modify: `frontend/src/hooks/useRunStream.ts`

**Step 1: 重写 connect 函数使用 EventSource**

替换 `connect` 函数（从第 77 行开始）：

```typescript
const connect = useCallback(() => {
  // 使用 ref 检查，避免循环依赖
  if (isConnectedRef.current) return

  setError(null)
  setIsConnected(true)
  isConnectedRef.current = true

  if (useMock) {
    // Mock 模式
    streamRef.current = createMockRunStream({
      runId,
      onEvent: handleMockEvent,
    })
    streamRef.current.start()
  } else {
    // 真实 SSE 连接 - 使用 EventSource (GET 请求)
    const eventSource = new EventSource(`${API_BASE}/runs/${runId}/stream`)
    streamRef.current = eventSource as unknown as EventSource

    eventSource.addEventListener('started', (e: MessageEvent) => {
      const data = JSON.parse(e.data)
      setRun({
        id: runId,
        task_id: data.run_id || '',
        status: 'running',
        started_at: new Date().toISOString(),
        steps: [],
      })
      setIsConnected(true)
      isConnectedRef.current = true
    })

    eventSource.addEventListener('step', (e: MessageEvent) => {
      const stepData = JSON.parse(e.data)
      setRun(prev => {
        if (!prev) return prev
        const newStep: Step = {
          index: stepData.index,
          action: stepData.action,
          reasoning: stepData.reasoning,
          screenshot: stepData.screenshot_url || '',
          status: stepData.status,
          duration_ms: stepData.duration_ms || 0,
        }
        return {
          ...prev,
          steps: [...prev.steps, newStep],
        }
      })
    })

    eventSource.addEventListener('finished', (e: MessageEvent) => {
      const parsed = JSON.parse(e.data)
      setRun(prev => {
        if (!prev) return prev
        return {
          ...prev,
          status: parsed.status,
          finished_at: new Date().toISOString(),
        }
      })
      setIsConnected(false)
      isConnectedRef.current = false
      eventSource.close()
    })

    eventSource.addEventListener('error', (e: MessageEvent) => {
      if (e.data) {
        const parsed = JSON.parse(e.data)
        setError(new Error(parsed.error || 'Unknown error'))
      }
      setIsConnected(false)
      isConnectedRef.current = false
      eventSource.close()
    })

    eventSource.onerror = () => {
      // 连接错误，可能是网络问题或执行已结束
      if (eventSource.readyState === EventSource.CLOSED) {
        setIsConnected(false)
        isConnectedRef.current = false
      }
    }
  }
}, [runId, useMock, handleMockEvent])
```

**Step 2: 修改 disconnect 函数**

替换 `disconnect` 函数：

```typescript
const disconnect = useCallback(() => {
  if (streamRef.current) {
    if ('stop' in streamRef.current) {
      // Mock stream
      (streamRef.current as ReturnType<typeof createMockRunStream>).stop()
    } else {
      // EventSource
      (streamRef.current as EventSource).close()
    }
    streamRef.current = null
  }
  setIsConnected(false)
  isConnectedRef.current = false
}, [])
```

**Step 3: 验证 TypeScript 编译**

```bash
cd /Users/huhu/project/weberpagent/frontend && npm run build
```

Expected: Build successful

**Step 4: 提交**

```bash
git add frontend/src/hooks/useRunStream.ts
git commit -m "refactor: useRunStream 使用 EventSource GET 请求订阅 SSE"
```

---

## Task 7: 集成测试

**Step 1: 启动后端服务**

```bash
cd /Users/huhu/project/weberpagent && source .venv/bin/activate && uvicorn backend.api.main:app --reload --port 11002
```

**Step 2: 启动前端服务（新终端）**

```bash
cd /Users/huhu/project/weberpagent/frontend && npm run dev
```

**Step 3: 手动测试**

1. 打开浏览器访问 http://localhost:11001
2. 选择一个任务，点击执行
3. 验证：
   - 只有一次 POST /runs 请求（创建 run）
   - GET /runs/{id}/stream 请求成功
   - 执行监控页面正常显示进度
   - 刷新页面后能重新连接并显示历史事件

**Step 4: 检查日志**

后端日志应该显示：
- POST /api/runs - 200 OK (创建 run)
- GET /api/runs/{id}/stream - 200 (SSE 订阅)

不应该出现：
- 重复的 POST /runs/{id}/execute
- GET /runs/{id}/execute 405 错误

---

## Task 8: 最终提交

**Step 1: 确认所有改动**

```bash
git status
```

**Step 2: 更新设计文档状态**

在 `docs/plans/2026-03-13-sse-backend-trigger-design.md` 末尾添加：

```markdown
## 实施状态

- [x] Task 1: 创建 EventManager 单元测试
- [x] Task 2: 实现 EventManager
- [x] Task 3: 添加 stream endpoint
- [x] Task 4: 修改 create_run 启动后台执行
- [x] Task 5: 删除旧的 execute endpoint
- [x] Task 6: 修改前端 useRunStream
- [x] Task 7: 集成测试

实施日期: 2026-03-13
```

**Step 3: 提交设计文档**

```bash
git add docs/plans/2026-03-13-sse-backend-trigger-design.md docs/plans/2026-03-13-sse-backend-trigger-impl.md
git commit -m "docs: SSE 后端触发模式设计和实施计划"
```
