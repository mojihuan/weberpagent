# SSE 后端触发模式设计

## 背景

当前实现中，前端进入 RunMonitor 页面时通过 POST 请求触发执行，存在以下问题：
1. React StrictMode 导致 useEffect 运行两次，产生重复请求
2. POST 请求不适合页面刷新后重新连接
3. 前端控制执行流程不够可靠

## 设计目标

将执行触发从前端移到后端：
- 创建 run 时立即启动后台执行
- 前端只负责订阅 SSE 流展示进度
- 支持页面刷新后重新连接

## 架构变更

### 当前流程
```
前端点击执行 → POST /runs (创建 run)
            → 导航到 /runs/{id}
            → POST /runs/{id}/execute (开始执行 + SSE)
```

### 新流程
```
前端点击执行 → POST /runs (创建 run + 启动后台执行)
            → 导航到 /runs/{id}
            → GET /runs/{id}/stream (只读 SSE 订阅)
```

## 实现方案

### 1. 后端改动

#### 1.1 新增 GET /runs/{run_id}/stream endpoint

```python
@router.get("/{run_id}/stream")
async def stream_run(run_id: str, ...):
    """SSE 订阅执行流"""
    # 验证 run 存在
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    return StreamingResponse(
        event_generator(run_id),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
```

#### 1.2 创建全局事件管理器

使用内存存储事件历史，支持重新连接：

```python
# backend/core/event_manager.py
class EventManager:
    def __init__(self):
        self._events: dict[str, list[str]] = {}  # run_id -> events
        self._subscribers: dict[str, list[Queue]] = {}
        self._status: dict[str, str] = {}  # run_id -> status

    async def publish(self, run_id: str, event: str):
        """发布事件"""
        if run_id not in self._events:
            self._events[run_id] = []
        self._events[run_id].append(event)

        # 通知所有订阅者
        for queue in self._subscribers.get(run_id, []):
            await queue.put(event)

    async def subscribe(self, run_id: str) -> AsyncGenerator[str, None]:
        """订阅事件流"""
        queue = asyncio.Queue()
        if run_id not in self._subscribers:
            self._subscribers[run_id] = []
        self._subscribers[run_id].append(queue)

        try:
            # 先发送历史事件
            for event in self._events.get(run_id, []):
                yield event

            # 然后等待新事件
            while True:
                event = await queue.get()
                if event is None:  # 结束信号
                    break
                yield event
        finally:
            self._subscribers[run_id].remove(queue)

    def is_finished(self, run_id: str) -> bool:
        """检查执行是否已结束"""
        return self._status.get(run_id) in ("success", "failed", "stopped")

# 全局实例
event_manager = EventManager()
```

#### 1.3 修改 create_run 启动后台执行

```python
@router.post("", response_model=RunResponse)
async def create_run(
    task_id: str,
    task_repo: TaskRepository = Depends(get_task_repo),
    run_repo: RunRepository = Depends(get_run_repo),
):
    """创建执行记录并启动后台执行"""
    task = await task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    run = await run_repo.create(task_id=task_id)

    # 启动后台执行
    asyncio.create_task(run_agent_background(run.id, task))

    return run
```

#### 1.4 后台执行函数

```python
async def run_agent_background(run_id: str, task):
    """后台执行 agent 任务"""
    async with async_session() as session:
        run_repo = RunRepository(session)
        step_repo = StepRepository(session)
        agent_service = AgentService()

        await run_repo.update_status(run_id, "running")
        await event_manager.publish(run_id, f"event: started\ndata: {{...}}\n\n")

        try:
            result = await agent_service.run_with_streaming(
                task=task.description,
                run_id=run_id,
                on_step=lambda step, action, reasoning, screenshot: (
                    event_manager.publish(run_id, f"event: step\ndata: {{...}}\n\n")
                ),
                max_steps=task.max_steps,
            )

            status = "success" if result.is_successful() else "failed"
            await run_repo.update_status(run_id, status)
            await event_manager.publish(run_id, f"event: finished\ndata: {{...}}\n\n")

        except Exception as e:
            await run_repo.update_status(run_id, "failed")
            await event_manager.publish(run_id, f"event: error\ndata: {{...}}\n\n")

        finally:
            event_manager.set_status(run_id, "finished")
            await event_manager.publish(run_id, None)  # 结束信号
```

### 2. 前端改动

#### 2.1 修改 useRunStream 使用 GET 请求

```typescript
const connect = useCallback(() => {
  if (isConnectedRef.current) return

  setError(null)
  setIsConnected(true)
  isConnectedRef.current = true

  // 使用 EventSource 进行 GET 请求
  const eventSource = new EventSource(`${API_BASE}/runs/${runId}/stream`)
  streamRef.current = eventSource

  eventSource.addEventListener('started', (e) => {
    const data = JSON.parse(e.data)
    setRun({ id: runId, task_id: data.run_id, status: 'running', ... })
  })

  eventSource.addEventListener('step', (e) => {
    const stepData = JSON.parse(e.data)
    setRun(prev => ({ ...prev, steps: [...prev.steps, stepData] }))
  })

  eventSource.addEventListener('finished', (e) => {
    const data = JSON.parse(e.data)
    setRun(prev => ({ ...prev, status: data.status }))
    disconnect()
  })

  eventSource.addEventListener('error', (e) => {
    if (e.data) {
      const data = JSON.parse(e.data)
      setError(new Error(data.error))
    }
    disconnect()
  })

  eventSource.onerror = () => {
    // 连接错误，可能是网络问题或执行已结束
    if (eventSource.readyState === EventSource.CLOSED) {
      disconnect()
    }
  }
}, [runId])
```

### 3. 删除旧代码

- 删除 `POST /runs/{run_id}/execute` endpoint
- 删除 `useRunStream` 中的 fetch POST 逻辑

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 内存泄漏（事件历史无限增长） | 限制历史事件数量，执行完成后延迟清理 |
| 服务器重启丢失状态 | 使用 Redis 或数据库存储事件（未来优化） |
| 并发订阅者 | EventManager 使用列表支持多个订阅者 |

## 测试计划

1. 单元测试 EventManager 发布/订阅
2. 集成测试创建 run 后自动执行
3. E2E 测试页面刷新后重新连接
4. 测试 StrictMode 下无重复执行

## 文件改动清单

```
backend/
├── core/
│   └── event_manager.py      # 新增
├── api/routes/
│   └── runs.py               # 修改：拆分 endpoint
frontend/
└── src/hooks/
    └── useRunStream.ts       # 修改：使用 EventSource
```
