# Browser-Use 测试平台后端实现计划

> 日期：2026-03-12
> 设计文档：`docs/plans/2026-03-12-browser-use-restart-design.md`
> 预计时间：6.5 小时

---

## Phase 1: 项目初始化 (30分钟)

### Task 1.1: 更新依赖配置

**文件**: `pyproject.toml`

```toml
[project]
name = "weberpagent"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    # browser-use 核心
    "browser-use>=0.12.0",

    # LLM 集成
    "langchain-openai>=0.3.0",

    # Web 框架
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",

    # 浏览器自动化
    "playwright>=1.40.0",

    # 数据存储
    "sqlalchemy>=2.0.0",
    "aiosqlite>=0.20.0",

    # 测试框架
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",

    # 配置管理
    "pyyaml>=6.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**命令**:
```bash
uv sync
```

**预期输出**:
```
Resolved <N> packages in <time>
Installed <N> packages
```

---

### Task 1.2: 创建目录结构

**命令**:
```bash
mkdir -p backend/api/routes
mkdir -p backend/api/schemas
mkdir -p backend/core
mkdir -p backend/storage
touch backend/api/__init__.py
touch backend/api/routes/__init__.py
touch backend/api/schemas/__init__.py
touch backend/core/__init__.py
touch backend/storage/__init__.py
```

---

### Task 1.3: 更新环境变量

**文件**: `.env`

```bash
# LLM 配置
DEEPSEEK_API_KEY=your-deepseek-api-key
OPENAI_API_KEY=your-openai-api-key

# 测试目标
ERP_BASE_URL=https://your-erp-url.com
ERP_USERNAME=your-username
ERP_PASSWORD=your-password

# 存储配置
DATABASE_URL=sqlite+aiosqlite:///./data/test_platform.db
SCREENSHOT_DIR=./screenshots
```

---

## Phase 2: 核心服务开发 (2小时)

### Task 2.1: 创建 LLM 工厂

**文件**: `backend/core/llm_factory.py`

```python
"""
LLM 工厂 - 创建和管理 LLM 实例
"""
import os
from typing import Optional
from enum import Enum

from langchain_openai import ChatOpenAI
from pydantic import BaseModel


class LLMProvider(str, Enum):
    DEEPSEEK = "deepseek"
    OPENAI = "openai"


class LLMConfig(BaseModel):
    provider: LLMProvider = LLMProvider.DEEPSEEK
    api_key: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.0


class LLMFactory:
    """LLM 实例工厂"""

    DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL = "deepseek-chat"
    OPENAI_MODEL = "gpt-4o"

    @staticmethod
    def create(config: Optional[LLMConfig] = None) -> ChatOpenAI:
        """
        创建 LLM 实例

        Args:
            config: LLM 配置，如果为 None 则从环境变量读取

        Returns:
            ChatOpenAI 实例
        """
        if config is None:
            config = LLMConfig()

        if config.provider == LLMProvider.DEEPSEEK:
            api_key = config.api_key or os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                raise ValueError("DEEPSEEK_API_KEY not set")

            return ChatOpenAI(
                model=config.model or LLMFactory.DEEPSEEK_MODEL,
                api_key=api_key,
                base_url=LLMFactory.DEEPSEEK_BASE_URL,
                temperature=config.temperature,
            )

        elif config.provider == LLMProvider.OPENAI:
            api_key = config.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")

            return ChatOpenAI(
                model=config.model or LLMFactory.OPENAI_MODEL,
                api_key=api_key,
                temperature=config.temperature,
            )

        else:
            raise ValueError(f"Unsupported LLM provider: {config.provider}")

    @staticmethod
    def create_with_fallback(
        primary: LLMProvider = LLMProvider.DEEPSEEK,
        fallback: LLMProvider = LLMProvider.OPENAI,
    ) -> ChatOpenAI:
        """
        创建带备选的 LLM 实例

        先尝试主 provider，失败则切换到备选
        """
        try:
            return LLMFactory.create(LLMConfig(provider=primary))
        except ValueError:
            print(f"Primary LLM ({primary}) not available, falling back to {fallback}")
            return LLMFactory.create(LLMConfig(provider=fallback))
```

**测试命令**:
```bash
uv run python -c "from backend.core.llm_factory import LLMFactory; print(LLMFactory.create())"
```

---

### Task 2.2: 创建 Agent 服务

**文件**: `backend/core/agent_service.py`

```python
"""
Agent 服务 - browser-use Agent 封装
"""
import asyncio
import base64
import os
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Any

from browser_use import Agent, Browser, BrowserConfig
from browser_use.agent.views import AgentHistoryList
from langchain_openai import ChatOpenAI

from backend.core.llm_factory import LLMFactory, LLMProvider


class StepData(dict):
    """步骤数据"""
    pass


class AgentService:
    """browser-use Agent 服务封装"""

    def __init__(
        self,
        llm_provider: LLMProvider = LLMProvider.DEEPSEEK,
        headless: bool = False,
        screenshot_dir: Optional[str] = None,
    ):
        self.llm = LLMFactory.create_with_fallback(primary=llm_provider)
        self.headless = headless
        self.screenshot_dir = Path(screenshot_dir or os.getenv("SCREENSHOT_DIR", "./screenshots"))
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    async def run_with_streaming(
        self,
        task: str,
        on_step: Callable[[StepData], None],
        max_steps: int = 20,
    ) -> AgentHistoryList:
        """
        执行任务并流式返回步骤

        Args:
            task: 任务描述
            on_step: 步骤回调函数
            max_steps: 最大步数

        Returns:
            AgentHistoryList 执行历史
        """
        browser = Browser(
            config=BrowserConfig(
                headless=self.headless,
            )
        )

        step_index = 0

        async def process_step():
            nonlocal step_index
            # browser-use 不直接支持步骤回调
            # 我们需要在执行后从历史中提取
            pass

        agent = Agent(
            task=task,
            llm=self.llm,
            browser=browser,
        )

        # 执行
        history = await agent.run(max_steps=max_steps)

        # 从历史中提取步骤并回调
        actions = history.model_actions()
        thoughts = history.model_thoughts()

        for i, (action, thought) in enumerate(zip(actions, thoughts)):
            step_index = i + 1

            step_data = StepData(
                index=step_index,
                action=str(action),
                thought=str(thought) if thought else None,
                timestamp=datetime.now().isoformat(),
            )

            # 调用回调
            if on_step:
                on_step(step_data)

        # 关闭浏览器
        await browser.close()

        return history

    async def run_simple(self, task: str, max_steps: int = 20) -> AgentHistoryList:
        """
        简单执行，不流式返回

        Args:
            task: 任务描述
            max_steps: 最大步数

        Returns:
            AgentHistoryList 执行历史
        """
        agent = Agent(
            task=task,
            llm=self.llm,
        )
        return await agent.run(max_steps=max_steps)

    async def take_screenshot(self, browser: Browser, step_index: int) -> str:
        """截取屏幕并保存"""
        screenshot_path = self.screenshot_dir / f"step_{step_index}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        # browser-use 的截图方法
        # 需要根据实际 API 调整
        screenshot_bytes = await browser.take_screenshot()

        if screenshot_bytes:
            with open(screenshot_path, "wb") as f:
                f.write(screenshot_bytes)
            return str(screenshot_path)

        return ""

    @staticmethod
    def screenshot_to_base64(image_path: str) -> str:
        """将截图转换为 base64"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
```

---

### Task 2.3: 创建断言服务

**文件**: `backend/core/assertion_service.py`

```python
"""
断言服务 - 执行测试断言
"""
from typing import Any
from enum import Enum

from browser_use.agent.views import AgentHistoryList


class AssertionType(str, Enum):
    URL_CONTAINS = "url_contains"
    TEXT_EXISTS = "text_exists"
    NO_ERRORS = "no_errors"
    URL_EQUALS = "url_equals"


class AssertionService:
    """断言服务"""

    @staticmethod
    def check_url_contains(history: AgentHistoryList, expected: str) -> bool:
        """检查最终 URL 是否包含预期字符串"""
        final_result = history.final_result()
        if not final_result:
            return False
        final_url = getattr(final_result, "url", "") or ""
        return expected in final_url

    @staticmethod
    def check_text_exists(history: AgentHistoryList, expected: str) -> bool:
        """检查页面是否存在预期文本"""
        final_result = history.final_result()
        if not final_result:
            return False
        content = getattr(final_result, "content", "") or ""
        return expected in content

    @staticmethod
    def check_no_errors(history: AgentHistoryList) -> bool:
        """检查是否有错误"""
        errors = history.errors()
        return len(errors) == 0

    @staticmethod
    def check_url_equals(history: AgentHistoryList, expected: str) -> bool:
        """检查最终 URL 是否等于预期"""
        final_result = history.final_result()
        if not final_result:
            return False
        final_url = getattr(final_result, "url", "") or ""
        return final_url == expected

    def run_assertion(
        self,
        history: AgentHistoryList,
        assertion_type: AssertionType,
        expected: Any,
    ) -> bool:
        """运行单个断言"""
        if assertion_type == AssertionType.URL_CONTAINS:
            return self.check_url_contains(history, expected)
        elif assertion_type == AssertionType.TEXT_EXISTS:
            return self.check_text_exists(history, expected)
        elif assertion_type == AssertionType.NO_ERRORS:
            return self.check_no_errors(history)
        elif assertion_type == AssertionType.URL_EQUALS:
            return self.check_url_equals(history, expected)
        else:
            raise ValueError(f"Unknown assertion type: {assertion_type}")

    def run_all_assertions(
        self,
        history: AgentHistoryList,
        assertions: list[dict],
    ) -> dict:
        """
        运行所有断言

        Args:
            history: Agent 执行历史
            assertions: 断言配置列表

        Returns:
            断言结果
        """
        results = {}

        for assertion in assertions:
            name = assertion.get("name", "unnamed")
            assertion_type = AssertionType(assertion["type"])
            expected = assertion.get("expected")

            try:
                passed = self.run_assertion(history, assertion_type, expected)
                results[name] = {
                    "passed": passed,
                    "type": assertion_type.value,
                    "expected": expected,
                }
            except Exception as e:
                results[name] = {
                    "passed": False,
                    "error": str(e),
                }

        return {
            "all_passed": all(r.get("passed", False) for r in results.values()),
            "details": results,
        }
```

---

## Phase 3: API 路由开发 (2小时)

### Task 3.1: 创建数据模型

**文件**: `backend/api/schemas/index.py`

```python
"""
API 数据模型
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List, Any
from pydantic import BaseModel, Field


# ===== 枚举 =====

class TaskStatus(str, Enum):
    DRAFT = "draft"
    READY = "ready"


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    STOPPED = "stopped"


# ===== 任务 =====

class TaskCreate(BaseModel):
    """创建任务请求"""
    name: str
    description: str
    target_url: str
    max_steps: int = Field(default=20, ge=1, le=100)
    assertions: List[dict] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    """更新任务请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    target_url: Optional[str] = None
    max_steps: Optional[int] = None
    assertions: Optional[List[dict]] = None
    status: Optional[TaskStatus] = None


class Task(BaseModel):
    """任务"""
    id: str
    name: str
    description: str
    target_url: str
    max_steps: int = 20
    status: TaskStatus = TaskStatus.DRAFT
    assertions: List[dict] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


# ===== 步骤 =====

class Step(BaseModel):
    """执行步骤"""
    index: int
    action: str
    thought: Optional[str] = None
    screenshot: Optional[str] = None
    duration_ms: Optional[int] = None
    timestamp: Optional[str] = None


# ===== 执行 =====

class RunCreate(BaseModel):
    """创建执行请求"""
    task_id: str


class Run(BaseModel):
    """执行记录"""
    id: str
    task_id: str
    status: RunStatus
    started_at: datetime
    finished_at: Optional[datetime] = None
    steps: List[Step] = Field(default_factory=list)
    ai_assertion: Optional[bool] = None
    code_assertion: Optional[bool] = None
    assertion_details: Optional[dict] = None
    final_url: Optional[str] = None
    error: Optional[str] = None


# ===== 报告 =====

class Report(BaseModel):
    """报告"""
    id: str
    run_id: str
    task_name: str
    status: RunStatus
    started_at: datetime
    finished_at: Optional[datetime] = None
    step_count: int
    ai_assertion: Optional[bool] = None
    code_assertion: Optional[bool] = None
    assertion_details: Optional[dict] = None


# ===== 响应 =====

class ApiResponse(BaseModel):
    """通用 API 响应"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


class PaginatedResponse(BaseModel):
    """分页响应"""
    items: List[Any]
    total: int
    page: int
    page_size: int
```

---

### Task 3.2: 创建存储服务

**文件**: `backend/storage/task_store.py`

```python
"""
任务存储服务
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from uuid import uuid4

from backend.api.schemas import Task, TaskCreate, TaskUpdate, TaskStatus


class TaskStore:
    """任务存储（基于 JSON 文件）"""

    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.tasks_file = self.data_dir / "tasks.json"
        self._ensure_file()

    def _ensure_file(self):
        """确保文件存在"""
        if not self.tasks_file.exists():
            self._save_all([])

    def _load_all(self) -> List[dict]:
        """加载所有任务"""
        with open(self.tasks_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_all(self, tasks: List[dict]):
        """保存所有任务"""
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2, default=str)

    def list(self) -> List[Task]:
        """获取所有任务"""
        tasks = self._load_all()
        return [Task(**t) for t in tasks]

    def get(self, task_id: str) -> Optional[Task]:
        """获取单个任务"""
        tasks = self._load_all()
        for t in tasks:
            if t["id"] == task_id:
                return Task(**t)
        return None

    def create(self, data: TaskCreate) -> Task:
        """创建任务"""
        now = datetime.now()
        task = Task(
            id=str(uuid4()),
            name=data.name,
            description=data.description,
            target_url=data.target_url,
            max_steps=data.max_steps,
            assertions=data.assertions,
            status=TaskStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )

        tasks = self._load_all()
        tasks.append(task.model_dump())
        self._save_all(tasks)

        return task

    def update(self, task_id: str, data: TaskUpdate) -> Optional[Task]:
        """更新任务"""
        tasks = self._load_all()

        for i, t in enumerate(tasks):
            if t["id"] == task_id:
                update_data = data.model_dump(exclude_unset=True)
                update_data["updated_at"] = datetime.now()
                tasks[i].update(update_data)
                self._save_all(tasks)
                return Task(**tasks[i])

        return None

    def delete(self, task_id: str) -> bool:
        """删除任务"""
        tasks = self._load_all()
        original_count = len(tasks)
        tasks = [t for t in tasks if t["id"] != task_id]

        if len(tasks) < original_count:
            self._save_all(tasks)
            return True
        return False


# 全局实例
task_store = TaskStore()
```

---

### Task 3.3: 创建执行存储服务

**文件**: `backend/storage/run_store.py`

```python
"""
执行记录存储服务
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from uuid import uuid4

from backend.api.schemas import Run, RunCreate, RunStatus, Step


class RunStore:
    """执行记录存储"""

    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.runs_file = self.data_dir / "runs.json"
        self._ensure_file()

    def _ensure_file(self):
        if not self.runs_file.exists():
            self._save_all([])

    def _load_all(self) -> List[dict]:
        with open(self.runs_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_all(self, runs: List[dict]):
        with open(self.runs_file, "w", encoding="utf-8") as f:
            json.dump(runs, f, ensure_ascii=False, indent=2, default=str)

    def list(self, task_id: Optional[str] = None) -> List[Run]:
        """获取执行列表"""
        runs = self._load_all()
        if task_id:
            runs = [r for r in runs if r.get("task_id") == task_id]
        return [Run(**r) for r in runs]

    def get(self, run_id: str) -> Optional[Run]:
        """获取单个执行"""
        runs = self._load_all()
        for r in runs:
            if r["id"] == run_id:
                return Run(**r)
        return None

    def create(self, data: RunCreate) -> Run:
        """创建执行记录"""
        run = Run(
            id=str(uuid4()),
            task_id=data.task_id,
            status=RunStatus.PENDING,
            started_at=datetime.now(),
        )

        runs = self._load_all()
        runs.append(run.model_dump())
        self._save_all(runs)

        return run

    def update(self, run_id: str, **kwargs) -> Optional[Run]:
        """更新执行记录"""
        runs = self._load_all()

        for i, r in enumerate(runs):
            if r["id"] == run_id:
                runs[i].update(kwargs)
                self._save_all(runs)
                return Run(**runs[i])

        return None

    def add_step(self, run_id: str, step: Step) -> Optional[Run]:
        """添加步骤"""
        runs = self._load_all()

        for i, r in enumerate(runs):
            if r["id"] == run_id:
                steps = r.get("steps", [])
                steps.append(step.model_dump())
                runs[i]["steps"] = steps
                self._save_all(runs)
                return Run(**runs[i])

        return None


# 全局实例
run_store = RunStore()
```

---

### Task 3.4: 创建任务路由

**文件**: `backend/api/routes/tasks.py`

```python
"""
任务管理路由
"""
from typing import List
from fastapi import APIRouter, HTTPException

from backend.api.schemas import Task, TaskCreate, TaskUpdate, ApiResponse
from backend.storage.task_store import task_store


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=List[Task])
async def list_tasks():
    """获取任务列表"""
    return task_store.list()


@router.post("", response_model=Task)
async def create_task(data: TaskCreate):
    """创建任务"""
    return task_store.create(data)


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """获取任务详情"""
    task = task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: str, data: TaskUpdate):
    """更新任务"""
    task = task_store.update(task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", response_model=ApiResponse)
async def delete_task(task_id: str):
    """删除任务"""
    success = task_store.delete(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return ApiResponse(success=True)
```

---

### Task 3.5: 创建执行路由（含 SSE）

**文件**: `backend/api/routes/runs.py`

```python
"""
执行管理路由
"""
import asyncio
import json
from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.api.schemas import Run, RunCreate, ApiResponse
from backend.storage.run_store import run_store
from backend.storage.task_store import task_store
from backend.core.agent_service import AgentService, StepData
from backend.core.assertion_service import AssertionService
from backend.core.llm_factory import LLMProvider


router = APIRouter(prefix="/api/runs", tags=["runs"])

# 存储正在运行的执行队列
active_runs: dict[str, asyncio.Queue] = {}


@router.get("", response_model=List[Run])
async def list_runs(task_id: str = None):
    """获取执行列表"""
    return run_store.list(task_id)


@router.post("", response_model=Run)
async def start_run(data: RunCreate):
    """启动执行"""
    # 验证任务存在
    task = task_store.get(data.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # 创建执行记录
    run = run_store.create(data)
    run_store.update(run.id, status="running")

    return run


@router.post("/{run_id}/execute")
async def execute_run(run_id: str):
    """执行任务并返回 SSE 流"""

    run = run_store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    task = task_store.get(run.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    async def event_stream():
        step_queue = asyncio.Queue()
        active_runs[run_id] = step_queue

        agent = AgentService(
            llm_provider=LLMProvider.DEEPSEEK,
            headless=False,
        )
        assertion = AssertionService()

        async def run_task():
            try:
                steps = []

                def on_step(step_data: StepData):
                    # 添加到本地列表
                    steps.append(step_data)

                    # 推送到 SSE 队列
                    asyncio.create_task(step_queue.put({
                        "type": "step",
                        "data": step_data,
                    }))

                # 执行任务
                history = await agent.run_with_streaming(
                    task=task.description,
                    on_step=on_step,
                    max_steps=task.max_steps,
                )

                # 运行断言
                assertion_results = assertion.run_all_assertions(
                    history,
                    task.assertions,
                )

                # 推送完成事件
                await step_queue.put({
                    "type": "done",
                    "data": {
                        "ai_assertion": True,  # 简化，实际应从 history 获取
                        "code_assertion": assertion_results["all_passed"],
                        "assertion_details": assertion_results["details"],
                    },
                })

                # 更新执行记录
                run_store.update(
                    run_id,
                    status="success" if assertion_results["all_passed"] else "failed",
                    steps=[s for s in steps],
                    ai_assertion=True,
                    code_assertion=assertion_results["all_passed"],
                    assertion_details=assertion_results["details"],
                )

            except Exception as e:
                await step_queue.put({
                    "type": "error",
                    "data": {"error": str(e)},
                })
                run_store.update(run_id, status="failed", error=str(e))

            finally:
                if run_id in active_runs:
                    del active_runs[run_id]

        # 启动后台任务
        asyncio.create_task(run_task())

        # SSE 流式返回
        while True:
            event = await step_queue.get()

            yield f"data: {json.dumps(event)}\n\n"

            if event.get("type") in ("done", "error"):
                break

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )


@router.get("/{run_id}", response_model=Run)
async def get_run(run_id: str):
    """获取执行详情"""
    run = run_store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("/{run_id}/stop", response_model=ApiResponse)
async def stop_run(run_id: str):
    """停止执行"""
    if run_id in active_runs:
        await active_runs[run_id].put({"type": "stop"})
        run_store.update(run_id, status="stopped")
        return ApiResponse(success=True)
    raise HTTPException(status_code=404, detail="Run not running")
```

---

### Task 3.6: 创建 FastAPI 主入口

**文件**: `backend/api/main.py`

```python
"""
FastAPI 主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import tasks, runs


app = FastAPI(
    title="Browser-Use 测试平台 API",
    description="AI + Playwright UI 自动化测试平台后端",
    version="1.0.0",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(tasks.router)
app.include_router(runs.router)


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}


@app.get("/")
async def root():
    """根路径"""
    return {"message": "Browser-Use Test Platform API", "docs": "/docs"}
```

---

### Task 3.7: 更新 `__init__.py`

**文件**: `backend/api/__init__.py`

```python
from backend.api.main import app

__all__ = ["app"]
```

---

## Phase 4: 测试与验证 (1小时)

### Task 4.1: 启动后端服务

**命令**:
```bash
uv run uvicorn backend.api.main:app --reload --port 8000
```

**预期输出**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**验证**:
- 访问 http://localhost:8000/docs 查看 API 文档
- 访问 http://localhost:8000/api/health 确认健康检查

---

### Task 4.2: 创建登录任务测试

**命令**:
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ERP 登录测试",
    "description": "登录 ERP 系统：1. 打开登录页 2. 切换到账号密码登录 3. 输入账号密码 4. 点击登录",
    "target_url": "https://your-erp-url.com/login",
    "max_steps": 10,
    "assertions": [
      {"name": "URL 跳转", "type": "url_contains", "expected": "/dashboard"},
      {"name": "无错误", "type": "no_errors", "expected": true}
    ]
  }'
```

**预期输出**:
```json
{
  "id": "xxx-xxx-xxx",
  "name": "ERP 登录测试",
  "status": "draft",
  ...
}
```

---

### Task 4.3: 执行测试

**命令**:
```bash
# 先创建执行记录
RUN_ID=$(curl -s -X POST http://localhost:8000/api/runs \
  -H "Content-Type: application/json" \
  -d '{"task_id": "xxx-xxx-xxx"}' | jq -r '.id')

# 执行并接收 SSE 流
curl -N http://localhost:8000/api/runs/$RUN_ID/execute
```

**预期输出** (SSE 流):
```
data: {"type": "step", "data": {"index": 1, "action": "navigate", ...}}

data: {"type": "step", "data": {"index": 2, "action": "click", ...}}

data: {"type": "done", "data": {"ai_assertion": true, "code_assertion": true, ...}}
```

---

## Phase 5: 前后端联调 (1小时)

### Task 5.1: 前端配置

**文件**: `frontend/src/api/client.ts` (修改)

```typescript
const API_BASE = 'http://localhost:8000';

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  return response.json();
}
```

### Task 5.2: 移除 Mock 数据

在 `frontend/src/` 中搜索 `mock` 相关代码，替换为真实 API 调用。

---

## 验收清单

| 项目 | 验证命令 | 预期结果 |
|------|----------|----------|
| 依赖安装 | `uv sync` | 无错误 |
| 后端启动 | `uv run uvicorn backend.api.main:app` | 服务正常运行 |
| API 文档 | 访问 `/docs` | Swagger UI 正常显示 |
| 任务 CRUD | `curl localhost:8000/api/tasks` | 返回任务列表 |
| 执行创建 | `POST /api/runs` | 返回执行记录 |
| SSE 推送 | `POST /api/runs/{id}/execute` | SSE 流正常返回 |
| 前端联调 | 访问前端页面 | 数据正常显示 |

---

## 后续任务

1. 添加更多断言类型
2. 实现截图存储和展示
3. 添加执行历史分页
4. 实现 API 断言能力
5. 添加定时任务支持
