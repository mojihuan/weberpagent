# SSE 流实现计划

基于设计文档: [2026-03-12-sse-stream-design.md](./2026-03-12-sse-stream-design.md)

## 前置条件

- [x] browser-use 0.12.0+ 已安装
- [x] FastAPI + Pydantic 已安装
- [ ] 需要添加 SQLAlchemy + aiosqlite 依赖

## 任务分解

### Phase 1: 数据库层 (SQLite + SQLAlchemy)

#### Task 1.1: 添加数据库依赖

**文件**: `pyproject.toml`

**改动**:
```toml
dependencies = [
    # ... existing
    "sqlalchemy>=2.0.0",
    "aiosqlite>=0.20.0",  # 异步 SQLite
]
```

**测试命令**:
```bash
pip install sqlalchemy aiosqlite
```

---

#### Task 1.2: 创建数据库配置

**文件**: `backend/db/__init__.py` (新建)

**代码**:
```python
"""数据库模块"""

from backend.db.database import get_db, init_db
from backend.db.models import Task, Run, Step
from backend.db.schemas import (
    TaskCreate,
    TaskUpdate,
    RunCreate,
    StepCreate,
)

__all__ = [
    "get_db",
    "init_db",
    "Task",
    "Run",
    "Step",
    "TaskCreate",
    "TaskUpdate",
    "RunCreate",
    "StepCreate",
]
```

---

#### Task 1.3: 创建数据库连接

**文件**: `backend/db/database.py` (新建)

**代码**:
```python
"""SQLAlchemy 数据库配置"""

from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# 数据库文件路径
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DATABASE_URL = f"sqlite+aiosqlite:///{DATA_DIR}/database.db"


class Base(DeclarativeBase):
    """SQLAlchemy 基类"""
    pass


# 异步引擎
engine = create_async_engine(DATABASE_URL, echo=False)

# 异步会话工厂
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """获取数据库会话"""
    async with async_session() as session:
        yield session


async def init_db():
    """初始化数据库（创建表）"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

**测试命令**:
```bash
python -c "from backend.db import init_db; import asyncio; asyncio.run(init_db())"
```

---

#### Task 1.4: 创建 ORM 模型

**文件**: `backend/db/models.py` (新建)

**代码**:
```python
"""SQLAlchemy ORM 模型"""

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.database import Base


def generate_id() -> str:
    return str(uuid.uuid4())[:8]


class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    target_url: Mapped[str] = mapped_column(String(500), default="")
    max_steps: Mapped[int] = mapped_column(Integer, default=10)
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, ready
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    runs: Mapped[list["Run"]] = relationship("Run", back_populates="task")


class Run(Base):
    """执行记录模型"""
    __tablename__ = "runs"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    task_id: Mapped[str] = mapped_column(String(8), ForeignKey("tasks.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, running, success, failed, stopped
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # 关系
    task: Mapped["Task"] = relationship("Task", back_populates="run")
    steps: Mapped[list["Step"]] = relationship("Step", back_populates="run", order_by="Step.step_index")


class Step(Base):
    """执行步骤模型"""
    __tablename__ = "steps"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    run_id: Mapped[str] = mapped_column(String(8), ForeignKey("runs.id"), nullable=False)
    step_index: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    reasoning: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    screenshot_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # success, failed
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # 关系
    run: Mapped["Run"] = relationship("Run", back_populates="step")
```

---

#### Task 1.5: 创建 Pydantic Schema

**文件**: `backend/db/schemas.py` (新建)

**代码**:
```python
"""Pydantic 请求/响应模型"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# === Task Schemas ===

class TaskBase(BaseModel):
    """任务基础模型"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    target_url: str = Field(default="", max_length=500)
    max_steps: int = Field(default=10, ge=1, le=100)


class TaskCreate(TaskBase):
    """创建任务请求"""
    pass


class TaskUpdate(BaseModel):
    """更新任务请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    target_url: Optional[str] = Field(None, max_length=500)
    max_steps: Optional[int] = Field(None, ge=1, le=100)
    status: Optional[str] = Field(None, pattern="^(draft|ready)$")


class TaskResponse(TaskBase):
    """任务响应"""
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# === Run Schemas ===

class RunCreate(BaseModel):
    """创建执行请求"""
    task_id: str


class RunResponse(BaseModel):
    """执行响应"""
    id: str
    task_id: str
    status: str
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# === Step Schemas ===

class StepResponse(BaseModel):
    """步骤响应"""
    id: str
    run_id: str
    step_index: int
    action: str
    reasoning: Optional[str] = None
    screenshot_url: Optional[str] = None  # 前端访问 URL
    status: str
    error: Optional[str] = None
    duration_ms: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# === SSE Event Schemas ===

class SSEStartedEvent(BaseModel):
    """SSE started 事件"""
    run_id: str
    task_name: str


class SSEStepEvent(BaseModel):
    """SSE step 事件"""
    index: int
    action: str
    reasoning: Optional[str] = None
    screenshot_url: Optional[str] = None
    status: str
    duration_ms: Optional[int] = None


class SSEFinishedEvent(BaseModel):
    """SSE finished 事件"""
    status: str  # success, failed, stopped
    total_steps: int
    duration_ms: int


class SSEErrorEvent(BaseModel):
    """SSE error 事件"""
    error: str
```

---

#### Task 1.6: 创建 Repository

**文件**: `backend/db/repository.py` (新建)

**代码**:
```python
"""数据库操作封装"""

from datetime import datetime
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models import Task, Run, Step
from backend.db.schemas import TaskCreate, TaskUpdate, RunCreate


class TaskRepository:
    """任务仓库"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: TaskCreate) -> Task:
        task = Task(**data.model_dump())
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get(self, task_id: str) -> Optional[Task]:
        return await self.session.get(Task, task_id)

    async def list(self, status: Optional[str] = None) -> list[Task]:
        stmt = select(Task)
        if status:
            stmt = stmt.where(Task.status == status)
        stmt = stmt.order_by(Task.created_at.desc)
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def update(self, task_id: str, data: TaskUpdate) -> Optional[Task]:
        task = await self.get(task_id)
        if not task:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        task.updated_at = datetime.now()
        await self.session.commit()
        return task

    async def delete(self, task_id: str) -> bool:
        task = await self.get(task_id)
        if not task:
            return False
        await self.session.delete(task)
        await self.session.commit()
        return True


class RunRepository:
    """执行记录仓库"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task_id: str) -> Run:
        run = Run(task_id=task_id, status="pending")
        self.session.add(run)
        await self.session.commit()
        await self.session.refresh(run)
        return run

    async def get(self, run_id: str) -> Optional[Run]:
        return await self.session.get(Run, run_id)

    async def list(self, task_id: Optional[str] = None) -> list[Run]:
        stmt = select(Run)
        if task_id:
            stmt = stmt.where(Run.task_id == task_id)
        stmt = stmt.order_by(Run.created_at.desc)
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def update_status(self, run_id: str, status: str) -> Optional[Run]:
        run = await self.get(run_id)
        if not run:
            return None
        run.status = status
        if status == "running":
            run.started_at = datetime.now()
        elif status in ("success", "failed", "stopped"):
            run.finished_at = datetime.now()
        await self.session.commit()
        return run

    async def add_step(self, run_id: str, step_data: dict) -> Step:
        step = Step(run_id=run_id, **step_data)
        self.session.add(step)
        await self.session.commit()
        await self.session.refresh(step)
        return step


class StepRepository:
    """步骤仓库"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, step_id: str) -> Optional[Step]:
        return await self.session.get(Step, step_id)

    async def list_by_run(self, run_id: str) -> list[Step]:
        stmt = select(Step).where(Step.run_id == run_id).order_by(Step.step_index)
        result = await self.session.execute(stmt)
        return list(result.scalars())
```

---

### Phase 2: 后端 Agent Service 回调

#### Task 2.1: 增强 Agent Service 截图支持

**文件**: `backend/core/agent_service.py`

**改动**:
1. 添加 `save_screenshot()` 方法
2. 修改 `run_with_streaming()` 支持截图保存

3. 添加 `run_id` 参数用于截图命名

**关键代码**:
```python
from pathlib import Path
from datetime import datetime
import base64

class AgentService:
    def __init__(self, output_dir: str = "outputs", screenshots_dir: str = "data/screenshots"):
        self.output_dir = Path(output_dir)
        self.screenshots_dir = Path(screenshots_dir)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

    async def save_screenshot(self, screenshot_bytes: bytes, run_id: str, step_index: int) -> str:
        """保存截图到本地文件

        Args:
            screenshot_bytes: 截图的二进制数据
            run_id: 执行 ID
            step_index: 步骤索引

        Returns:
            截图文件路径
        """
        filename = f"{run_id}_{step_index}.png"
        filepath = self.screenshots_dir / filename
        filepath.write_bytes(screenshot_bytes)
        return str(filepath)

    async def run_with_streaming(
        self,
        task: str,
        run_id: str,
        on_step: Callable[[int, str, str, str | None], None],
        max_steps: int = 10,
        llm_config: dict | None = None,
    ) -> Any:
        """带流式回调的执行"""
        llm = create_llm(llm_config)
        step_times = {}

        async def step_callback(browser_state, agent_output, step: int):
            start_time = datetime.now()
            step_times[step] = start_time

            # 提取动作和推理
            action = ""
            reasoning = ""
            if agent_output and hasattr(agent_output, "action"):
                actions = agent_output.action
                if actions and len(actions) > 0:
                    first_action = actions[0]
                    action = getattr(first_action, "action", "")
                    reasoning = getattr(first_action, "reasoning", "")

            # 提取截图
            screenshot_path = None
            if browser_state and hasattr(browser_state, "screenshot"):
                screenshot_bytes = browser_state.screenshot
                if screenshot_bytes:
                    screenshot_path = await self.save_screenshot(
                        screenshot_bytes, run_id, step
                    )

            # 计算耗时
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            on_step(step, action, reasoning, screenshot_path)

        agent = Agent(
            task=task,
            llm=llm,
            max_actions_per_step=5,
            register_new_step_callback=step_callback,
        )

        result = await agent.run(max_steps=max_steps)
        return result
```

**测试命令**:
```bash
python -m pytest backend/tests/test_agent_service.py -v
```

---

### Phase 3: 后端 SSE 路由

#### Task 3.1: 重构 runs 路由使用 SQLite

**文件**: `backend/api/routes/runs.py`

**改动**:
1. 使用 `RunRepository` 替代 `RunStore`
2. 实现 SSE 流式响应
3. 添加截图 API 端点

**关键代码**:
```python
from fastapi import Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db, Run
from backend.db.repository import RunRepository, StepRepository
from backend.db.schemas import SSEStartedEvent, SSEStepEvent, SSEFinishedEvent, SSEErrorEvent
from backend.core.agent_service import AgentService


async def get_run_repo(db: AsyncSession = Depends(get_db)) -> RunRepository:
    return RunRepository(db)


async def get_step_repo(db: AsyncSession = Depends(get_db)) -> StepRepository:
    return StepRepository(db)


@router.post("/{run_id}/execute")
async def execute_run(
    run_id: str,
    run_repo: RunRepository = Depends(get_run_repo),
    step_repo: StepRepository = Depends(get_step_repo),
):
    """SSE 流式执行任务"""
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(404, "Run not found")

    task = run.task

    async def event_generator():
        start_time = datetime.now()
        await run_repo.update_status(run_id, "running")

        # 发送 started 事件
        yield f"event: started\ndata: {SSEStartedEvent(run_id=run_id, task_name=task.name).model_dump_json()}\n\n"

        try:
            step_count = 0

            def on_step(index: int, action: str, reasoning: str, screenshot_path: str | None):
                nonlocal step_count
                step_count = index

                # 保存步骤到数据库
                step = await step_repo.add_step(run_id, {
                    "step_index": index,
                    "action": action,
                    "reasoning": reasoning,
                    "screenshot_path": screenshot_path,
                    "status": "success",
                    "duration_ms": 0,  # 由 agent_service 计算
                })

                # 发送 step 事件
                screenshot_url = f"/api/runs/{run_id}/screenshots/{index}" if screenshot_path else None
                event = SSEStepEvent(
                    index=index,
                    action=action,
                    reasoning=reasoning,
                    screenshot_url=screenshot_url,
                    status="success",
                    duration_ms=step.duration_ms,
                )
                yield f"event: step\ndata: {event.model_dump_json()}\n\n"

            agent_service = AgentService()
            result = await agent_service.run_with_streaming(
                task=task.description,
                run_id=run_id,
                on_step=on_step,
                max_steps=task.max_steps,
            )

            # 计算总耗时
            total_duration = int((datetime.now() - start_time).total_seconds() * 1000)

            # 发送 finished 事件
            final_status = "success" if result.is_successful() else "failed"
            await run_repo.update_status(run_id, final_status)

            finished = SSEFinishedEvent(
                status=final_status,
                total_steps=step_count,
                duration_ms=total_duration,
            )
            yield f"event: finished\ndata: {finished.model_dump_json()}\n\n"

        except Exception as e:
            await run_repo.update_status(run_id, "failed")
            error = SSEErrorEvent(error=str(e))
            yield f"event: error\ndata: {error.model_dump_json()}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.get("/{run_id}/screenshots/{step_index}")
async def get_screenshot(
    run_id: str,
    step_index: int,
    step_repo: StepRepository = Depends(get_step_repo),
):
    """获取截图"""
    steps = await step_repo.list_by_run(run_id)
    step = next((s for s in steps if s.step_index == step_index), None)

    if not step or not step.screenshot_path:
        raise HTTPException(404, "Screenshot not found")

    from fastapi.responses import FileResponse
    return FileResponse(
        step.screenshot_path,
        media_type="image/png",
    )
```

---

#### Task 3.2: 重构 tasks 路由使用 SQLite

**文件**: `backend/api/routes/tasks.py`

**改动**:
- 使用 `TaskRepository` 替代 `TaskStore`
- 保持 API 接口不变

---

#### Task 3.3: 更新 main.py 初始化

**文件**: `backend/api/main.py`

**改动**:
```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import init_db
from backend.api.routes import tasks, runs


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Browser-Use API Server...")
    await init_db()  # 初始化数据库
    yield
    print("Shutting down Browser-Use API Server...")


# ... rest unchanged
```

---

### Phase 4: 前端 SSE 连接

#### Task 4.1: 实现真实 SSE 连接

**文件**: `frontend/src/hooks/useRunStream.ts`

**改动**:
1. 添加 `useMock=false` 的真实 SSE 实现
2. 解析 SSE 事件并更新状态

**关键代码**:
```typescript
// 添加真实 SSE 连接
} else {
  // 真实 SSE 连接
  const eventSource = new EventSource(`${API_BASE}/runs/${runId}/execute`, {
    withCredentials: true,
  })

  eventSource.addEventListener('started', (e) => {
    const data = JSON.parse(e.data)
    setRun({
      id: runId,
      task_id: data.run_id,
      status: 'running',
      started_at: new Date().toISOString(),
      steps: [],
    })
    setIsConnected(true)
    isConnectedRef.current = true
  })

  eventSource.addEventListener('step', (e) => {
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

  eventSource.addEventListener('finished', (e) => {
    const data = JSON.parse(e.data)
    setRun(prev => {
      if (!prev) return prev
      return {
        ...prev,
        status: data.status,
        finished_at: new Date().toISOString(),
      }
    })
    setIsConnected(false)
    isConnectedRef.current = false
    eventSource.close()
  })

  eventSource.addEventListener('error', (e) => {
    const data = JSON.parse(e.data)
    setError(new Error(data.error))
    setIsConnected(false)
    isConnectedRef.current = false
    eventSource.close()
  })

  eventSource.onerror = (e) => {
    setError(new Error('SSE connection error'))
    setIsConnected(false)
    isConnectedRef.current = false
    eventSource.close()
  }

  streamRef.current = {
    stop: () => {
      eventSource.close()
      setIsConnected(false)
      isConnectedRef.current = false
    },
  } as any
}
```

---

#### Task 4.2: 更新 API 调用

**文件**: `frontend/src/api/runs.ts`

**改动**:
```typescript
import { apiClient } from './client'

const API_BASE = 'http://localhost:8080/api'

// 创建执行记录
export async function createRun(taskId: string): Promise<{ runId: string }> {
  return apiClient<{ runId: string }>(`/runs?task_id=${taskId}`, {
    method: 'POST',
  })
}

// 获取执行详情
export async function getRun(runId: string): Promise<Run> {
  return apiClient<Run>(`/runs/${runId}`)
}

// 停止执行
export async function stopRun(runId: string): Promise<{ status: string }> {
  return apiClient<{ status: string }>(`/runs/${runId}/stop`, {
    method: 'POST',
  })
}
```

---

### Phase 5: 集成测试

#### Task 5.1: 后端单元测试

**文件**: `backend/tests/test_db_repository.py` (新建)

**测试内容**:
- TaskRepository CRUD 操作
- RunRepository 状态更新
- StepRepository 步骤存储

---

#### Task 5.2: 后端 SSE 测试

**文件**: `backend/tests/test_sse_endpoint.py` (新建)

**测试内容**:
- SSE 事件格式验证
- 截图保存和访问

---

#### Task 5.3: 前端 SSE 集成测试

**文件**: `frontend/src/hooks/__tests__/useRunStream.test.ts` (新建)

**测试内容**:
- Mock 模式验证
- 真实 SSE 连接验证

---

## 验证清单

### Phase 1 完成标准
- [ ] `pip install sqlalchemy aiosqlite` 成功
- [ ] `python -c "from backend.db import init_db; import asyncio; asyncio.run(init_db())"` 无报错
- [ ] `data/database.db` 文件已创建

### Phase 2 完成标准
- [ ] `python -m pytest backend/tests/test_agent_service.py -v` 通过

### Phase 3 完成标准
- [ ] `uvicorn backend.api.main:app --reload --port 8080` 启动成功
- [ ] `curl http://localhost:8080/api/tasks` 返回空数组
- [ ] `curl -X POST http://localhost:8080/api/tasks -d '{"name":"test","description":"test"}'` 返回任务

### Phase 4 完成标准
- [ ] `cd frontend && npm run dev` 启动成功
- [ ] 访问 http://localhost:5173/tasks 无报错
- [ ] 点击执行按钮能建立 SSE 连接

### Phase 5 完成标准
- [ ] 所有后端测试通过
- [ ] 前端 SSE 连接成功
- [ ] 截图能正确显示

---

## 风险和注意事项

1. **Browser-Use 回调兼容性**: `register_new_step_callback` 的签名可能变化，需要测试验证
2. **SSE 超时**: 长时间执行可能导致 SSE 连接超时，需要设置合理的超时时间
3. **截图存储**: 确保截图目录有写入权限
4. **前端 EventSource**: 需要 POST 请求启动执行，但 EventSource 只支持 GET，需要调整 API 设计

---

## 预计时间

| Phase | 任务数 | 预计时间 |
|-------|--------|----------|
| Phase 1 | 6 | 1-2 小时 |
| Phase 2 | 1 | 0.5 小时 |
| Phase 3 | 3 | 1-2 小时 |
| Phase 4 | 2 | 0.5-1 小时 |
| Phase 5 | 3 | 1 小时 |
| **总计** | **15** | **4-6.5 小时** |
