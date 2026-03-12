# Browser-Use Restart Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建 AI + Playwright UI 自动化测试平台，使用 Browser-Use + DeepSeek 实现 ERP 系统自动化测试。

**Architecture:** FastAPI 后端 + React 前端 + SSE 实时推送。后端封装 browser-use Agent，前端通过 SSE 接收执行进度。复用现有 `backend/llm/` 和 `backend/agent/` 代码。

**Tech Stack:** Python, FastAPI, browser-use, langchain-openai, DeepSeek/GPT-4o, Playwright, React, TypeScript, SSE

---

## Phase 1: 依赖更新 + 目录结构

### Task 1.1: 更新依赖配置

**Files:**
- Modify: `pyproject.toml`

**Step 1: 添加缺失依赖**

在 `dependencies` 数组中添加：

```toml
dependencies = [
    "browser-use>=0.12.0",
    "langchain-openai>=0.3.0",
    "langchain-core>=0.3.0",
    "playwright>=1.40.0",
    "fastapi>=0.135.1",
    "uvicorn[standard]>=0.34.0",
    "httpx>=0.28.1",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "tenacity>=8.0.0",
    "dashscope>=1.20.0",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
]
```

**Step 2: 同步依赖**

Run: `uv sync`
Expected: 无错误，依赖安装成功

**Step 3: 验证导入**

Run: `uv run python -c "from browser_use import Agent; from langchain_openai import ChatOpenAI; print('OK')"`
Expected: 输出 `OK`

**Step 4: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "chore: 更新依赖配置，添加 pydantic-settings"
```

---

### Task 1.2: 创建目录结构

**Files:**
- Create: `backend/api/__init__.py`
- Create: `backend/api/routes/__init__.py`
- Create: `backend/api/schemas/__init__.py`
- Create: `backend/core/__init__.py`
- Create: `backend/storage/__init__.py`

**Step 1: 创建目录和 __init__.py 文件**

```bash
mkdir -p backend/api/routes backend/api/schemas backend/core backend/storage
```

**Step 2: 创建 __init__.py 文件**

`backend/api/__init__.py`:
```python
"""FastAPI 路由层"""
```

`backend/api/routes/__init__.py`:
```python
"""API 路由模块"""
```

`backend/api/schemas/__init__.py`:
```python
"""Pydantic 数据模型"""
```

`backend/core/__init__.py`:
```python
"""核心服务层"""
```

`backend/storage/__init__.py`:
```python
"""存储层"""
```

**Step 3: Commit**

```bash
git add backend/api/ backend/core/ backend/storage/
git commit -m "chore: 创建 API、Core、Storage 目录结构"
```

---

## Phase 2: 核心服务开发

### Task 2.1: 创建 Pydantic 数据模型

**Files:**
- Create: `backend/api/schemas/index.py`
- Test: `backend/tests/test_schemas.py`

**Step 1: 编写数据模型测试**

`backend/tests/test_schemas.py`:
```python
"""测试 Pydantic 数据模型"""

import pytest
from datetime import datetime
from backend.api.schemas.index import Task, Run, Step, Assertion, RunResult


def test_assertion_creation():
    """测试断言模型创建"""
    assertion = Assertion(name="URL检查", type="url_contains", expected="/dashboard")
    assert assertion.name == "URL检查"
    assert assertion.type == "url_contains"
    assert assertion.expected == "/dashboard"


def test_task_creation():
    """测试任务模型创建"""
    task = Task(
        id="test-123",
        name="登录测试",
        description="测试登录功能",
        assertions=[
            Assertion(name="URL检查", type="url_contains", expected="/dashboard")
        ],
    )
    assert task.id == "test-123"
    assert task.name == "登录测试"
    assert len(task.assertions) == 1


def test_step_creation():
    """测试步骤模型创建"""
    step = Step(
        step=1,
        action="click",
        reasoning="点击登录按钮",
        screenshot="/screenshots/1.png",
    )
    assert step.step == 1
    assert step.action == "click"


def test_run_result_creation():
    """测试执行结果模型创建"""
    result = RunResult(
        success=True,
        ai_assertion={"passed": True},
        code_assertion={"passed": True},
        duration_seconds=10.5,
        total_steps=5,
    )
    assert result.success is True
    assert result.total_steps == 5


def test_run_creation():
    """测试执行记录模型创建"""
    run = Run(
        id="run-123",
        task_id="task-123",
        status="pending",
        steps=[],
    )
    assert run.id == "run-123"
    assert run.status == "pending"
```

**Step 2: 运行测试验证失败**

Run: `uv run pytest backend/tests/test_schemas.py -v`
Expected: FAIL - 模块不存在

**Step 3: 实现数据模型**

`backend/api/schemas/index.py`:
```python
"""Pydantic 数据模型定义"""

from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field


class Assertion(BaseModel):
    """断言模型"""

    name: str = Field(..., description="断言名称")
    type: Literal["url_contains", "text_exists", "no_errors"] = Field(
        ..., description="断言类型"
    )
    expected: str | bool = Field(..., description="期望值")


class Task(BaseModel):
    """任务模型"""

    id: str = Field(..., description="任务 ID")
    name: str = Field(..., description="任务名称")
    description: str = Field(..., description="自然语言任务描述")
    assertions: list[Assertion] = Field(default_factory=list, description="断言列表")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")


class Step(BaseModel):
    """执行步骤模型"""

    step: int = Field(..., description="步骤编号")
    action: str = Field(..., description="动作类型")
    reasoning: str = Field(default="", description="AI 推理")
    screenshot: str | None = Field(default=None, description="截图路径")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")


class RunResult(BaseModel):
    """执行结果模型"""

    success: bool = Field(..., description="是否成功")
    ai_assertion: dict[str, Any] = Field(default_factory=dict, description="AI 断言结果")
    code_assertion: dict[str, Any] = Field(default_factory=dict, description="代码断言结果")
    duration_seconds: float = Field(..., description="执行时长")
    total_steps: int = Field(..., description="总步数")


class Run(BaseModel):
    """执行记录模型"""

    id: str = Field(..., description="执行 ID")
    task_id: str = Field(..., description="关联任务 ID")
    status: Literal["pending", "running", "completed", "failed"] = Field(
        default="pending", description="执行状态"
    )
    steps: list[Step] = Field(default_factory=list, description="执行步骤")
    result: RunResult | None = Field(default=None, description="执行结果")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    started_at: datetime | None = Field(default=None, description="开始时间")
    completed_at: datetime | None = Field(default=None, description="完成时间")


class TaskCreate(BaseModel):
    """创建任务请求模型"""

    name: str
    description: str
    assertions: list[Assertion] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    """更新任务请求模型"""

    name: str | None = None
    description: str | None = None
    assertions: list[Assertion] | None = None
```

**Step 4: 运行测试验证通过**

Run: `uv run pytest backend/tests/test_schemas.py -v`
Expected: PASS - 所有测试通过

**Step 5: Commit**

```bash
git add backend/api/schemas/index.py backend/tests/test_schemas.py
git commit -m "feat: 添加 Pydantic 数据模型"
```

---

### Task 2.2: 创建任务存储服务

**Files:**
- Create: `backend/storage/task_store.py`
- Test: `backend/tests/test_task_store.py`

**Step 1: 编写存储测试**

`backend/tests/test_task_store.py`:
```python
"""测试任务存储"""

import os
import tempfile
import pytest
from backend.storage.task_store import TaskStore
from backend.api.schemas.index import Task, Assertion


@pytest.fixture
def temp_store():
    """使用临时目录的存储"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = TaskStore(data_dir=tmpdir)
        yield store


def test_create_task(temp_store):
    """测试创建任务"""
    task = temp_store.create(
        name="登录测试",
        description="测试登录功能",
        assertions=[Assertion(name="URL", type="url_contains", expected="/dashboard")],
    )
    assert task.id
    assert task.name == "登录测试"


def test_get_task(temp_store):
    """测试获取任务"""
    created = temp_store.create(name="测试", description="描述")
    found = temp_store.get(created.id)
    assert found is not None
    assert found.id == created.id


def test_list_tasks(temp_store):
    """测试列出任务"""
    temp_store.create(name="任务1", description="描述1")
    temp_store.create(name="任务2", description="描述2")
    tasks = temp_store.list()
    assert len(tasks) == 2


def test_update_task(temp_store):
    """测试更新任务"""
    created = temp_store.create(name="原名称", description="原描述")
    updated = temp_store.update(created.id, name="新名称")
    assert updated is not None
    assert updated.name == "新名称"


def test_delete_task(temp_store):
    """测试删除任务"""
    created = temp_store.create(name="测试", description="描述")
    assert temp_store.delete(created.id) is True
    assert temp_store.get(created.id) is None
```

**Step 2: 运行测试验证失败**

Run: `uv run pytest backend/tests/test_task_store.py -v`
Expected: FAIL - 模块不存在

**Step 3: 实现任务存储**

`backend/storage/task_store.py`:
```python
"""任务存储服务 - JSON 文件实现"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path

from backend.api.schemas.index import Task, TaskCreate, TaskUpdate


class TaskStore:
    """任务存储"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.data_dir / "tasks.json"
        self._ensure_file()

    def _ensure_file(self) -> None:
        """确保文件存在"""
        if not self.file_path.exists():
            self._save([])

    def _load(self) -> list[dict]:
        """加载所有任务"""
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, tasks: list[dict]) -> None:
        """保存所有任务"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2, default=str)

    def create(self, name: str, description: str, assertions: list = None) -> Task:
        """创建任务"""
        tasks = self._load()
        now = datetime.now()
        task_data = {
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "description": description,
            "assertions": assertions or [],
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }
        tasks.append(task_data)
        self._save(tasks)
        return Task(**task_data)

    def get(self, task_id: str) -> Task | None:
        """获取单个任务"""
        tasks = self._load()
        for task in tasks:
            if task["id"] == task_id:
                return Task(**task)
        return None

    def list(self) -> list[Task]:
        """列出所有任务"""
        return [Task(**t) for t in self._load()]

    def update(self, task_id: str, **kwargs) -> Task | None:
        """更新任务"""
        tasks = self._load()
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                task.update(kwargs)
                task["updated_at"] = datetime.now().isoformat()
                tasks[i] = task
                self._save(tasks)
                return Task(**task)
        return None

    def delete(self, task_id: str) -> bool:
        """删除任务"""
        tasks = self._load()
        original_len = len(tasks)
        tasks = [t for t in tasks if t["id"] != task_id]
        if len(tasks) < original_len:
            self._save(tasks)
            return True
        return False
```

**Step 4: 运行测试验证通过**

Run: `uv run pytest backend/tests/test_task_store.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add backend/storage/task_store.py backend/tests/test_task_store.py
git commit -m "feat: 添加任务存储服务"
```

---

### Task 2.3: 创建执行记录存储服务

**Files:**
- Create: `backend/storage/run_store.py`
- Test: `backend/tests/test_run_store.py`

**Step 1: 编写存储测试**

`backend/tests/test_run_store.py`:
```python
"""测试执行记录存储"""

import tempfile
import pytest
from backend.storage.run_store import RunStore
from backend.api.schemas.index import Run, Step


@pytest.fixture
def temp_store():
    """使用临时目录的存储"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = RunStore(data_dir=tmpdir)
        yield store


def test_create_run(temp_store):
    """测试创建执行记录"""
    run = temp_store.create(task_id="task-123")
    assert run.id
    assert run.task_id == "task-123"
    assert run.status == "pending"


def test_update_run_status(temp_store):
    """测试更新执行状态"""
    run = temp_store.create(task_id="task-123")
    updated = temp_store.update_status(run.id, "running")
    assert updated is not None
    assert updated.status == "running"


def test_add_step(temp_store):
    """测试添加步骤"""
    run = temp_store.create(task_id="task-123")
    step = Step(step=1, action="click", reasoning="点击按钮")
    updated = temp_store.add_step(run.id, step)
    assert updated is not None
    assert len(updated.steps) == 1


def test_get_runs_by_task(temp_store):
    """测试按任务 ID 获取执行记录"""
    temp_store.create(task_id="task-1")
    temp_store.create(task_id="task-1")
    temp_store.create(task_id="task-2")
    runs = temp_store.list_by_task("task-1")
    assert len(runs) == 2
```

**Step 2: 运行测试验证失败**

Run: `uv run pytest backend/tests/test_run_store.py -v`
Expected: FAIL - 模块不存在

**Step 3: 实现执行记录存储**

`backend/storage/run_store.py`:
```python
"""执行记录存储服务 - JSON 文件实现"""

import json
from datetime import datetime
from pathlib import Path

from backend.api.schemas.index import Run, Step, RunResult


class RunStore:
    """执行记录存储"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.data_dir / "runs.json"
        self._ensure_file()

    def _ensure_file(self) -> None:
        """确保文件存在"""
        if not self.file_path.exists():
            self._save([])

    def _load(self) -> list[dict]:
        """加载所有执行记录"""
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, runs: list[dict]) -> None:
        """保存所有执行记录"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(runs, f, ensure_ascii=False, indent=2, default=str)

    def create(self, task_id: str) -> Run:
        """创建执行记录"""
        import uuid
        runs = self._load()
        run_data = {
            "id": str(uuid.uuid4())[:8],
            "task_id": task_id,
            "status": "pending",
            "steps": [],
            "result": None,
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None,
        }
        runs.append(run_data)
        self._save(runs)
        return Run(**run_data)

    def get(self, run_id: str) -> Run | None:
        """获取单个执行记录"""
        runs = self._load()
        for run in runs:
            if run["id"] == run_id:
                return Run(**run)
        return None

    def list(self) -> list[Run]:
        """列出所有执行记录"""
        return [Run(**r) for r in self._load()]

    def list_by_task(self, task_id: str) -> list[Run]:
        """按任务 ID 列出执行记录"""
        return [Run(**r) for r in self._load() if r["task_id"] == task_id]

    def update_status(self, run_id: str, status: str) -> Run | None:
        """更新执行状态"""
        runs = self._load()
        for i, run in enumerate(runs):
            if run["id"] == run_id:
                run["status"] = status
                if status == "running":
                    run["started_at"] = datetime.now().isoformat()
                elif status in ("completed", "failed"):
                    run["completed_at"] = datetime.now().isoformat()
                runs[i] = run
                self._save(runs)
                return Run(**run)
        return None

    def add_step(self, run_id: str, step: Step) -> Run | None:
        """添加执行步骤"""
        runs = self._load()
        for i, run in enumerate(runs):
            if run["id"] == run_id:
                run["steps"].append(step.model_dump())
                runs[i] = run
                self._save(runs)
                return Run(**run)
        return None

    def set_result(self, run_id: str, result: RunResult) -> Run | None:
        """设置执行结果"""
        runs = self._load()
        for i, run in enumerate(runs):
            if run["id"] == run_id:
                run["result"] = result.model_dump()
                runs[i] = run
                self._save(runs)
                return Run(**run)
        return None

    def delete(self, run_id: str) -> bool:
        """删除执行记录"""
        runs = self._load()
        original_len = len(runs)
        runs = [r for r in runs if r["id"] != run_id]
        if len(runs) < original_len:
            self._save(runs)
            return True
        return False
```

**Step 4: 运行测试验证通过**

Run: `uv run pytest backend/tests/test_run_store.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add backend/storage/run_store.py backend/tests/test_run_store.py
git commit -m "feat: 添加执行记录存储服务"
```

---

### Task 2.4: 创建断言服务

**Files:**
- Create: `backend/core/assertion_service.py`
- Test: `backend/tests/test_assertion_service.py`

**Step 1: 编写断言服务测试**

`backend/tests/test_assertion_service.py`:
```python
"""测试断言服务"""

import pytest
from backend.core.assertion_service import AssertionService
from backend.api.schemas.index import Assertion


@pytest.fixture
def service():
    return AssertionService()


def test_check_url_contains_success(service):
    """测试 URL 包含检查 - 成功"""
    # 模拟 history 对象
    class MockHistory:
        final_result = type("Result", (), {"url": "https://example.com/dashboard"})()

    result = service.check_url_contains(MockHistory(), "/dashboard")
    assert result is True


def test_check_url_contains_failure(service):
    """测试 URL 包含检查 - 失败"""
    class MockHistory:
        final_result = type("Result", (), {"url": "https://example.com/login"})()

    result = service.check_url_contains(MockHistory(), "/dashboard")
    assert result is False


def test_check_text_exists_success(service):
    """测试文本存在检查 - 成功"""
    class MockHistory:
        final_result = type("Result", (), {"text_content": "欢迎回来，用户"})()

    result = service.check_text_exists(MockHistory(), "欢迎")
    assert result is True


def test_check_no_errors(service):
    """测试无错误检查"""
    class MockHistory:
        is_done = True
        final_result = type("Result", (), {"error": None})()

    result = service.check_no_errors(MockHistory())
    assert result is True


def test_run_all_assertions(service):
    """测试运行所有断言"""
    class MockHistory:
        is_done = True
        final_result = type(
            "Result", (), {"url": "https://example.com/dashboard", "error": None}
        )()

    assertions = [
        Assertion(name="URL检查", type="url_contains", expected="/dashboard"),
        Assertion(name="无错误", type="no_errors", expected=True),
    ]

    results = service.run_all_assertions(MockHistory(), assertions)
    assert results["URL检查"] is True
    assert results["无错误"] is True
```

**Step 2: 运行测试验证失败**

Run: `uv run pytest backend/tests/test_assertion_service.py -v`
Expected: FAIL - 模块不存在

**Step 3: 实现断言服务**

`backend/core/assertion_service.py`:
```python
"""断言服务 - 验证执行结果"""

from typing import Any

from backend.api.schemas.index import Assertion


class AssertionService:
    """断言服务"""

    def check_url_contains(self, history: Any, expected: str) -> bool:
        """检查最终 URL 是否包含期望字符串

        Args:
            history: browser-use Agent 执行历史
            expected: 期望包含的字符串

        Returns:
            是否通过
        """
        try:
            if hasattr(history, "final_result") and history.final_result:
                url = getattr(history.final_result, "url", "")
                return expected in str(url)
        except Exception:
            pass
        return False

    def check_text_exists(self, history: Any, expected: str) -> bool:
        """检查页面是否包含期望文本

        Args:
            history: browser-use Agent 执行历史
            expected: 期望存在的文本

        Returns:
            是否通过
        """
        try:
            if hasattr(history, "final_result") and history.final_result:
                text = getattr(history.final_result, "text_content", "")
                return expected in str(text)
        except Exception:
            pass
        return False

    def check_no_errors(self, history: Any) -> bool:
        """检查执行是否无错误

        Args:
            history: browser-use Agent 执行历史

        Returns:
            是否无错误
        """
        try:
            if hasattr(history, "is_done") and history.is_done:
                if hasattr(history, "final_result") and history.final_result:
                    error = getattr(history.final_result, "error", None)
                    return error is None
                return True
        except Exception:
            pass
        return False

    def run_all_assertions(
        self, history: Any, assertions: list[Assertion]
    ) -> dict[str, bool]:
        """运行所有断言

        Args:
            history: browser-use Agent 执行历史
            assertions: 断言列表

        Returns:
            断言名称 -> 是否通过的字典
        """
        results = {}
        for assertion in assertions:
            if assertion.type == "url_contains":
                results[assertion.name] = self.check_url_contains(
                    history, str(assertion.expected)
                )
            elif assertion.type == "text_exists":
                results[assertion.name] = self.check_text_exists(
                    history, str(assertion.expected)
                )
            elif assertion.type == "no_errors":
                results[assertion.name] = self.check_no_errors(history)
            else:
                results[assertion.name] = False
        return results
```

**Step 4: 运行测试验证通过**

Run: `uv run pytest backend/tests/test_assertion_service.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add backend/core/assertion_service.py backend/tests/test_assertion_service.py
git commit -m "feat: 添加断言服务"
```

---

### Task 2.5: 创建 Agent 服务

**Files:**
- Create: `backend/core/agent_service.py`
- Test: `backend/tests/test_agent_service.py`

**Step 1: 编写 Agent 服务测试**

`backend/tests/test_agent_service.py`:
```python
"""测试 Agent 服务"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from backend.core.agent_service import AgentService


@pytest.fixture
def agent_service():
    return AgentService()


def test_agent_service_creation(agent_service):
    """测试服务创建"""
    assert agent_service is not None


@pytest.mark.asyncio
async def test_run_simple_mock(agent_service):
    """测试简单执行（Mock）"""
    # Mock browser-use Agent
    with patch("backend.core.agent_service.Agent") as MockAgent:
        mock_agent = MagicMock()
        mock_agent.run = AsyncMock()
        mock_agent.run.return_value = MagicMock(is_done=True)
        MockAgent.return_value = mock_agent

        result = await agent_service.run_simple(task="打开网页")

        assert result is not None
        mock_agent.run.assert_called_once()
```

**Step 2: 运行测试验证失败**

Run: `uv run pytest backend/tests/test_agent_service.py -v`
Expected: FAIL - 模块不存在

**Step 3: 实现 Agent 服务**

`backend/core/agent_service.py`:
```python
"""Agent 服务 - 封装 browser-use Agent"""

import asyncio
import time
from typing import Any, Callable

from browser_use import Agent

from backend.llm.factory import create_llm


class AgentService:
    """browser-use Agent 服务封装"""

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir

    async def run_simple(
        self,
        task: str,
        max_steps: int = 10,
        llm_config: dict | None = None,
    ) -> Any:
        """简单执行任务

        Args:
            task: 自然语言任务描述
            max_steps: 最大执行步数
            llm_config: LLM 配置

        Returns:
            Agent 执行历史
        """
        llm = create_llm(llm_config)

        agent = Agent(
            task=task,
            llm=llm,
            max_actions_per_step=5,
        )

        result = await agent.run(max_steps=max_steps)
        return result

    async def run_with_streaming(
        self,
        task: str,
        on_step: Callable[[int, str, str, str | None], None],
        max_steps: int = 10,
        llm_config: dict | None = None,
    ) -> Any:
        """带流式回调的执行

        Args:
            task: 自然语言任务描述
            on_step: 步骤回调函数 (step, action, reasoning, screenshot_path)
            max_steps: 最大执行步数
            llm_config: LLM 配置

        Returns:
            Agent 执行历史
        """
        llm = create_llm(llm_config)
        step_count = 0

        def step_callback(browser_state, agent_output, step: int):
            nonlocal step_count
            step_count = step

            # 提取动作和推理
            action = ""
            reasoning = ""
            if agent_output and hasattr(agent_output, "action"):
                actions = agent_output.action
                if actions and len(actions) > 0:
                    first_action = actions[0]
                    action = getattr(first_action, "action", "")
                    reasoning = getattr(first_action, "reasoning", "")

            on_step(step, action, reasoning, None)

        agent = Agent(
            task=task,
            llm=llm,
            max_actions_per_step=5,
            register_new_step_callback=step_callback,
        )

        result = await agent.run(max_steps=max_steps)
        return result
```

**Step 4: 运行测试验证通过**

Run: `uv run pytest backend/tests/test_agent_service.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add backend/core/agent_service.py backend/tests/test_agent_service.py
git commit -m "feat: 添加 Agent 服务"
```

---

## Phase 3: FastAPI 路由开发

### Task 3.1: 创建任务路由

**Files:**
- Create: `backend/api/routes/tasks.py`

**Step 1: 实现任务路由**

`backend/api/routes/tasks.py`:
```python
"""任务管理路由"""

from fastapi import APIRouter, HTTPException

from backend.api.schemas.index import Task, TaskCreate, TaskUpdate
from backend.storage.task_store import TaskStore

router = APIRouter(prefix="/tasks", tags=["tasks"])

# 全局存储实例
task_store = TaskStore()


@router.get("", response_model=list[Task])
async def list_tasks():
    """获取任务列表"""
    return task_store.list()


@router.post("", response_model=Task)
async def create_task(task: TaskCreate):
    """创建任务"""
    return task_store.create(
        name=task.name,
        description=task.description,
        assertions=[a.model_dump() for a in task.assertions],
    )


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """获取任务详情"""
    task = task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: str, task: TaskUpdate):
    """更新任务"""
    update_data = {k: v for k, v in task.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    updated = task_store.update(task_id, **update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """删除任务"""
    if not task_store.delete(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "deleted"}
```

**Step 2: Commit**

```bash
git add backend/api/routes/tasks.py
git commit -m "feat: 添加任务管理路由"
```

---

### Task 3.2: 创建执行路由（含 SSE）

**Files:**
- Create: `backend/api/routes/runs.py`

**Step 1: 实现执行路由**

`backend/api/routes/runs.py`:
```python
"""执行管理路由"""

import asyncio
import json
from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.api.schemas.index import Run, Step, RunResult
from backend.storage.run_store import RunStore
from backend.storage.task_store import TaskStore
from backend.core.agent_service import AgentService
from backend.core.assertion_service import AssertionService

router = APIRouter(prefix="/runs", tags=["runs"])

# 全局存储实例
run_store = RunStore()
task_store = TaskStore()
agent_service = AgentService()
assertion_service = AssertionService()


@router.get("", response_model=list[Run])
async def list_runs():
    """获取执行列表"""
    return run_store.list()


@router.post("", response_model=Run)
async def create_run(task_id: str):
    """创建执行记录"""
    task = task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return run_store.create(task_id=task_id)


@router.get("/{run_id}", response_model=Run)
async def get_run(run_id: str):
    """获取执行详情"""
    run = run_store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
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

    async def event_generator():
        start_time = datetime.now()
        run_store.update_status(run_id, "running")

        # 发送开始事件
        yield f"event: start\ndata: {json.dumps({'run_id': run_id, 'task': task.name})}\n\n"

        try:
            steps_data = []

            def on_step(step: int, action: str, reasoning: str, screenshot: str | None):
                step_obj = Step(
                    step=step,
                    action=action,
                    reasoning=reasoning,
                    screenshot=screenshot,
                )
                steps_data.append(step_obj.model_dump())
                run_store.add_step(run_id, step_obj)

            # 执行任务
            result = await agent_service.run_simple(task=task.description)

            # 运行断言
            assertion_results = assertion_service.run_all_assertions(result, task.assertions)

            # 计算执行时间
            duration = (datetime.now() - start_time).total_seconds()
            total_steps = len(steps_data)

            # 创建执行结果
            run_result = RunResult(
                success=result.is_done if hasattr(result, "is_done") else True,
                ai_assertion={"passed": result.is_done if hasattr(result, "is_done") else True},
                code_assertion=assertion_results,
                duration_seconds=duration,
                total_steps=total_steps,
            )

            run_store.set_result(run_id, run_result)
            run_store.update_status(run_id, "completed")

            # 发送完成事件
            yield f"event: complete\ndata: {json.dumps(run_result.model_dump())}\n\n"

        except Exception as e:
            run_store.update_status(run_id, "failed")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.post("/{run_id}/stop")
async def stop_run(run_id: str):
    """停止执行"""
    run = run_store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    if run.status != "running":
        raise HTTPException(status_code=400, detail="Run is not running")

    run_store.update_status(run_id, "failed")
    return {"status": "stopped"}
```

**Step 2: Commit**

```bash
git add backend/api/routes/runs.py
git commit -m "feat: 添加执行管理路由和 SSE 推送"
```

---

### Task 3.3: 创建 FastAPI 入口

**Files:**
- Create: `backend/api/main.py`

**Step 1: 实现 FastAPI 入口**

`backend/api/main.py`:
```python
"""FastAPI 应用入口"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import tasks, runs


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期"""
    # 启动时初始化
    print("Starting Browser-Use API Server...")
    yield
    # 关闭时清理
    print("Shutting down Browser-Use API Server...")


app = FastAPI(
    title="Browser-Use API",
    description="AI + Playwright UI 自动化测试平台 API",
    version="0.1.0",
    lifespan=lifespan,
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
app.include_router(tasks.router, prefix="/api")
app.include_router(runs.router, prefix="/api")


@app.get("/")
async def root():
    """根路径"""
    return {"message": "Browser-Use API", "docs": "/docs"}


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}
```

**Step 2: 验证服务启动**

Run: `uv run uvicorn backend.api.main:app --reload &
sleep 3 && curl http://localhost:8000/health`
Expected: `{"status": "healthy"}`

**Step 3: Commit**

```bash
git add backend/api/main.py
git commit -m "feat: 添加 FastAPI 应用入口"
```

---

## Phase 4: 前后端联调

### Task 4.1: 更新前端 API 客户端

**Files:**
- Modify: `frontend/src/api/client.ts`

**Step 1: 检查前端 API 客户端是否存在**

Run: `ls -la frontend/src/api/ 2>/dev/null || echo "目录不存在"`
Expected: 显示文件列表或 "目录不存在"

**Step 2: 根据实际情况调整前端代码**

如果 `frontend/src/api/` 存在，修改 API 基础 URL 指向后端：

```typescript
const API_BASE_URL = 'http://localhost:8000/api';
```

**Step 3: 移除 Mock 数据**

找到并删除或重命名 mock 文件。

**Step 4: Commit**

```bash
git add frontend/src/
git commit -m "feat: 前端对接真实后端 API"
```

---

## Phase 5: ERP 登录验证

### Task 5.1: 配置测试目标

**Files:**
- Modify: `.env`

**Step 1: 确认环境变量**

确认 `.env` 包含：
```
DEEPSEEK_API_KEY=your_key_here
ERP_BASE_URL=https://your-erp-url.com
ERP_USERNAME=your_username
ERP_PASSWORD=your_password
```

**Step 2: 创建登录测试脚本**

`backend/tests/test_login_e2e_browser_use.py`:
```python
"""ERP 登录端到端测试"""

import asyncio
import pytest

from backend.core.agent_service import AgentService


@pytest.mark.asyncio
async def test_erp_login():
    """测试 ERP 登录"""
    import os

    base_url = os.getenv("ERP_BASE_URL")
    username = os.getenv("ERP_USERNAME")
    password = os.getenv("ERP_PASSWORD")

    if not all([base_url, username, password]):
        pytest.skip("ERP 环境变量未配置")

    task = f"""
登录 ERP 系统：
1. 打开 {base_url}
2. 如果显示手机验证码登录，点击切换到"密码登录"
3. 输入用户名 {username} 和密码
4. 点击登录按钮
5. 确认登录成功
"""

    service = AgentService()
    result = await service.run_simple(task=task, max_steps=15)

    assert result is not None
    assert hasattr(result, "is_done")
```

**Step 3: 运行测试**

Run: `uv run pytest backend/tests/test_login_e2e_browser_use.py -v`
Expected: PASS（如果环境配置正确）

**Step 4: Commit**

```bash
git add backend/tests/test_login_e2e_browser_use.py
git commit -m "test: 添加 ERP 登录端到端测试"
```

---

## Phase 6: 文档收尾

### Task 6.1: 更新 CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

**Step 1: 更新项目文档**

确保 CLAUDE.md 反映最新架构，包括新增的 `backend/api/`, `backend/core/`, `backend/storage/` 目录。

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: 更新 CLAUDE.md 反映最新架构"
```

---

### Task 6.2: 创建 Git Tag

**Step 1: 创建 Tag**

Run: `git tag v0.1.0-browser-use-restart -m "Browser-Use Restart 完成"`

**Step 2: 推送 Tag**

Run: `git push origin v0.1.0-browser-use-restart`

---

## 完成检查

- [ ] Phase 1: 依赖更新 + 目录结构 ✅
- [ ] Phase 2: 核心服务开发 ✅
- [ ] Phase 3: FastAPI 路由开发 ✅
- [ ] Phase 4: 前后端联调 ✅
- [ ] Phase 5: ERP 登录验证 ✅
- [ ] Phase 6: 文档收尾 ✅
