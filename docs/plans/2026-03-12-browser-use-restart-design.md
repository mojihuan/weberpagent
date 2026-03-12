# Browser-Use 测试平台后端设计文档

> 日期：2026-03-12
> 状态：设计完成，待实施
> 版本：v2.0（架构重设计）

## 1. 背景

### 1.1 项目定位

将 browser-use 作为 **AI + Playwright UI 自动化测试平台** 的核心框架，构建完整的后端服务。

### 1.2 核心需求

| 需求 | 说明 |
|------|------|
| LLM 选择 | DeepSeek 优先，GPT-4o/Gemini 备选 |
| 前后端分离 | FastAPI 后端 + React 前端（已完成） |
| 实时推送 | SSE 推送执行进度、截图、AI 推理 |
| 断言方式 | AI 断言 + 代码断言双重验证 |
| 优先场景 | 登录/认证流程 |

### 1.3 关键发现

browser-use 支持以下能力，可用于实现 SSE 实时推送：

1. **EventBus 事件系统** - 基于 `bubus` 库，可监听浏览器事件
2. **History API** - 执行后获取 `model_actions()`、`model_thoughts()`、`errors()`
3. **Sandbox 回调** - `@sandbox(on_log=..., on_result=..., on_error=...)`

---

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│              前端 (已完成)                                   │
│   React + Vite + Tailwind + SSE EventSource                │
│   Dashboard / Tasks / RunMonitor / Reports                 │
└─────────────────────┬───────────────────────────────────────┘
                      │ REST + SSE
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI 后端 (待开发)                           │
│                                                             │
│   路由层                                                    │
│   ├── /api/tasks      任务 CRUD                            │
│   ├── /api/runs       执行管理 + SSE 推送                   │
│   ├── /api/reports    报告查看                              │
│   └── /api/config     配置管理                              │
│                                                             │
│   核心层 (browser-use)                                      │
│   ├── Agent           AI 决策 + 执行                        │
│   ├── ChatDeepSeek    LLM 适配                              │
│   └── Browser         浏览器控制                            │
│                                                             │
│   数据层                                                    │
│   ├── SQLite/JSON     任务/报告存储                         │
│   └── screenshots/    截图存储                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 核心原则

1. **browser-use 为核心**：直接使用原生 API，最小化封装
2. **DeepSeek 优先**：`ChatDeepSeek` 官方原生支持
3. **SSE 实时推送**：通过 `asyncio.Queue` 实现步骤流式返回
4. **双重断言**：AI 判断 + 代码验证

---

## 3. 后端项目结构

```
backend/
├── api/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 入口
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tasks.py            # 任务管理
│   │   ├── runs.py             # 执行管理 + SSE
│   │   ├── reports.py          # 报告查看
│   │   └── config.py           # 配置管理
│   └── schemas/
│       └── index.py            # Pydantic 模型
│
├── core/
│   ├── __init__.py
│   ├── agent_service.py        # browser-use Agent 封装
│   ├── llm_factory.py          # LLM 工厂 (DeepSeek/GPT 备选)
│   └── assertion_service.py    # 断言服务
│
├── storage/
│   ├── __init__.py
│   ├── task_store.py           # 任务存储
│   ├── run_store.py            # 执行记录存储
│   └── screenshot_store.py     # 截图存储
│
├── _archived/                  # 归档代码（保留参考）
│   ├── agent_simple/
│   ├── proxy/
│   └── llm/
│
└── tests/
    ├── conftest.py
    └── test_login.py           # 登录场景测试
```

---

## 4. API 设计

### 4.1 路由设计

```python
# backend/api/main.py

# ===== 任务管理 =====
GET    /api/tasks              # 获取任务列表
POST   /api/tasks              # 创建新任务
GET    /api/tasks/{id}         # 获取任务详情
PUT    /api/tasks/{id}         # 更新任务
DELETE /api/tasks/{id}         # 删除任务

# ===== 执行管理 =====
POST   /api/runs               # 启动执行（传入任务ID）
GET    /api/runs               # 获取执行历史列表
GET    /api/runs/{id}          # 获取单次执行详情
POST   /api/runs/{id}/stop     # 停止执行
GET    /api/runs/{id}/stream   # SSE 实时推送执行进度

# ===== 报告查看 =====
GET    /api/reports            # 获取报告列表
GET    /api/reports/{id}       # 获取报告详情
GET    /api/screenshots/{path} # 获取截图文件

# ===== 配置管理 =====
GET    /api/config/targets     # 获取测试目标配置
PUT    /api/config/targets     # 更新测试目标配置
GET    /api/config/models      # 获取可用模型列表
```

### 4.2 数据结构

```python
# backend/api/schemas/index.py
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime

class TaskStatus(str, Enum):
    DRAFT = "draft"
    READY = "ready"

class RunStatus(str, Enum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    STOPPED = "stopped"

class Task(BaseModel):
    id: str
    name: str
    description: str              # 自然语言任务描述
    target_url: str
    max_steps: int = 20
    status: TaskStatus = TaskStatus.DRAFT
    created_at: datetime
    updated_at: datetime

class Step(BaseModel):
    index: int
    action: str                   # AI 输出的动作
    thought: Optional[str]        # AI 的推理过程
    screenshot: str               # 截图路径 (base64 或 URL)
    duration_ms: Optional[int]

class Run(BaseModel):
    id: str
    task_id: str
    status: RunStatus
    started_at: datetime
    finished_at: Optional[datetime]
    steps: List[Step]
    ai_assertion: Optional[bool]  # AI 判断结果
    code_assertion: Optional[bool] # 代码断言结果
    final_url: Optional[str]
    error: Optional[str]
```

---

## 5. 核心服务设计

### 5.1 AgentService - browser-use 封装

```python
# backend/core/agent_service.py
import asyncio
from typing import Callable, Optional
from browser_use import Agent, Browser
from browser_use.llm import ChatDeepSeek, ChatOpenAI
from browser_use.agent.views import AgentHistoryList

class AgentService:
    def __init__(
        self,
        llm_provider: str = "deepseek",
        api_key: Optional[str] = None,
    ):
        self.llm = self._create_llm(llm_provider, api_key)

    def _create_llm(self, provider: str, api_key: Optional[str]):
        """创建 LLM 实例"""
        if provider == "deepseek":
            return ChatDeepSeek(
                model="deepseek-chat",
                api_key=api_key,
            )
        elif provider == "openai":
            return ChatOpenAI(
                model="gpt-4o",
                api_key=api_key,
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    async def run_with_streaming(
        self,
        task: str,
        on_step: Callable[[dict], None],
        max_steps: int = 20,
    ) -> AgentHistoryList:
        """执行任务并流式返回步骤"""

        browser = Browser(headless=False)
        step_queue = asyncio.Queue()
        step_index = 0

        async def step_callback(step_data: dict):
            nonlocal step_index
            step_index += 1
            step_data["index"] = step_index

            # 截图
            step_data["screenshot"] = await browser.take_screenshot()

            # 推送到队列
            await step_queue.put(step_data)

            # 调用外部回调
            if on_step:
                on_step(step_data)

        agent = Agent(
            task=task,
            llm=self.llm,
            browser=browser,
        )

        # 执行
        history = await agent.run(max_steps=max_steps)

        # 等待队列清空
        await step_queue.put(None)  # 结束信号

        return history

    async def run_simple(self, task: str, max_steps: int = 20) -> AgentHistoryList:
        """简单执行，不流式返回"""
        agent = Agent(
            task=task,
            llm=self.llm,
        )
        return await agent.run(max_steps=max_steps)
```

### 5.2 AssertionService - 断言服务

```python
# backend/core/assertion_service.py
from browser_use.agent.views import AgentHistoryList

class AssertionService:
    @staticmethod
    def check_url_contains(history: AgentHistoryList, expected: str) -> bool:
        """检查最终 URL 是否包含预期字符串"""
        final_url = history.final_result().get("url", "")
        return expected in final_url

    @staticmethod
    def check_text_exists(history: AgentHistoryList, expected: str) -> bool:
        """检查页面是否存在预期文本"""
        final_result = history.final_result()
        page_content = final_result.get("content", "")
        return expected in page_content

    @staticmethod
    def check_no_errors(history: AgentHistoryList) -> bool:
        """检查是否有错误"""
        errors = history.errors()
        return len(errors) == 0

    def run_all_assertions(
        self,
        history: AgentHistoryList,
        assertions: list[dict],
    ) -> dict:
        """运行所有断言"""
        results = {}

        for assertion in assertions:
            assertion_type = assertion["type"]
            expected = assertion["expected"]

            if assertion_type == "url_contains":
                results[assertion["name"]] = self.check_url_contains(history, expected)
            elif assertion_type == "text_exists":
                results[assertion["name"]] = self.check_text_exists(history, expected)
            elif assertion_type == "no_errors":
                results[assertion["name"]] = self.check_no_errors(history)

        return {
            "all_passed": all(results.values()),
            "details": results,
        }
```

---

## 6. SSE 实时推送设计

### 6.1 执行路由

```python
# backend/api/routes/runs.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from core.agent_service import AgentService
from core.assertion_service import AssertionService
import asyncio
import json

router = APIRouter()

@router.post("/api/runs")
async def start_run(task_id: str):
    """启动执行并返回 SSE 流"""

    task = get_task(task_id)  # 从存储获取任务

    async def event_stream():
        agent = AgentService(llm_provider="deepseek")
        assertion = AssertionService()

        step_queue = asyncio.Queue()

        def on_step(step_data):
            # 将步骤推送到队列
            asyncio.create_task(step_queue.put(step_data))

        # 启动执行任务（后台）
        async def run_task():
            history = await agent.run_with_streaming(
                task=task.description,
                on_step=on_step,
                max_steps=task.max_steps,
            )

            # 执行完成，运行断言
            assertion_results = assertion.run_all_assertions(
                history,
                task.assertions,
            )

            # 推送完成事件
            await step_queue.put({
                "type": "done",
                "ai_assertion": history.final_result().get("success", False),
                "code_assertion": assertion_results["all_passed"],
                "assertion_details": assertion_results["details"],
            })

        # 启动后台任务
        asyncio.create_task(run_task())

        # SSE 流式返回
        while True:
            event = await step_queue.get()

            if event is None:
                break

            if event.get("type") == "done":
                yield f"data: {json.dumps(event)}\n\n"
                break
            else:
                yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )

@router.get("/api/runs/{run_id}/stream")
async def stream_run(run_id: str):
    """获取正在执行的 SSE 流"""
    # 实现类似，从现有执行中获取队列
    pass
```

### 6.2 前端接收（已实现）

```typescript
// 前端 RunMonitor.tsx
const eventSource = new EventSource(`/api/runs/${runId}/stream`);

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.type === 'done') {
        setStatus('completed');
        setAiAssertion(data.ai_assertion);
        setCodeAssertion(data.code_assertion);
        eventSource.close();
    } else {
        // 新步骤
        setSteps(prev => [...prev, data]);
        setScreenshot(data.screenshot);
    }
};
```

---

## 7. 登录测试示例

### 7.1 任务配置

```python
# 创建登录任务
task = Task(
    id="login-001",
    name="ERP 登录测试",
    description="""
    登录 ERP 系统：
    1. 打开 https://erp.example.com/login
    2. 如果看到手机登录，点击切换到"账号密码登录"
    3. 输入账号: admin，密码: password123
    4. 点击登录按钮
    5. 确认登录成功（看到"商品采购"或用户名"admin"）
    """,
    target_url="https://erp.example.com/login",
    max_steps=10,
)
```

### 7.2 断言配置

```python
# 任务关联的断言
assertions = [
    {
        "name": "URL 跳转正确",
        "type": "url_contains",
        "expected": "/dashboard",
    },
    {
        "name": "显示欢迎信息",
        "type": "text_exists",
        "expected": "商品采购",
    },
    {
        "name": "无执行错误",
        "type": "no_errors",
        "expected": True,
    },
]
```

### 7.3 执行流程

```
1. 前端发送 POST /api/runs { task_id: "login-001" }
2. 后端创建 Agent，开始执行
3. 每步执行后，SSE 推送:
   - step index
   - action (AI 决策的动作)
   - thought (AI 推理过程)
   - screenshot (当前页面截图)
4. 执行完成，推送:
   - ai_assertion (AI 判断是否成功)
   - code_assertion (代码断言结果)
5. 前端显示最终结果
```

---

## 8. 环境配置

### 8.1 环境变量

```bash
# .env
# LLM 配置
DEEPSEEK_API_KEY=sk-xxx           # DeepSeek API Key（优先）
OPENAI_API_KEY=sk-xxx             # OpenAI API Key（备选）

# 测试目标
ERP_BASE_URL=https://erp.example.com
ERP_USERNAME=admin
ERP_PASSWORD=xxx

# 存储配置
DATABASE_URL=sqlite:///data/test_platform.db
SCREENSHOT_DIR=./screenshots
```

### 8.2 依赖清单

```toml
# pyproject.toml
[project]
dependencies = [
    # browser-use 核心
    "browser-use>=0.12.0",

    # LLM 集成
    "langchain-openai>=0.3.0",

    # Web 框架
    "fastapi>=0.115.0",
    "uvicorn>=0.30.0",

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
]
```

---

## 9. 实施步骤

### 9.1 阶段划分

| 阶段 | 内容 | 预计时间 |
|------|------|----------|
| **Phase 1** | 核心服务开发 | 2 小时 |
| **Phase 2** | API 路由开发 | 2 小时 |
| **Phase 3** | 前后端联调 | 1 小时 |
| **Phase 4** | 登录场景验证 | 1 小时 |
| **Phase 5** | 文档更新 | 0.5 小时 |

**总计：约 6.5 小时**

### 9.2 详细步骤

#### Phase 1: 核心服务开发（2小时）

- [ ] 1.1 创建 `core/agent_service.py` - browser-use 封装
- [ ] 1.2 创建 `core/llm_factory.py` - LLM 工厂
- [ ] 1.3 创建 `core/assertion_service.py` - 断言服务
- [ ] 1.4 编写单元测试验证

#### Phase 2: API 路由开发（2小时）

- [ ] 2.1 创建 `api/main.py` - FastAPI 入口
- [ ] 2.2 创建 `api/routes/tasks.py` - 任务 CRUD
- [ ] 2.3 创建 `api/routes/runs.py` - 执行管理 + SSE
- [ ] 2.4 创建 `api/routes/reports.py` - 报告查看
- [ ] 2.5 创建 `api/schemas/index.py` - 数据模型

#### Phase 3: 前后端联调（1小时）

- [ ] 3.1 配置 CORS
- [ ] 3.2 前端移除 Mock，对接真实 API
- [ ] 3.3 验证 SSE 实时推送

#### Phase 4: 登录场景验证（1小时）

- [ ] 4.1 配置测试目标环境
- [ ] 4.2 创建登录任务
- [ ] 4.3 执行并验证 SSE 推送
- [ ] 4.4 验证断言结果

#### Phase 5: 文档更新（0.5小时）

- [ ] 5.1 更新 `CLAUDE.md`
- [ ] 5.2 更新 `docs/1_后端主计划.md`
- [ ] 5.3 创建实施计划文档

---

## 10. 验收标准

| 标准 | 验证方式 |
|------|----------|
| 登录测试通过 | 任务执行成功，断言全部通过 |
| SSE 推送正常 | 前端实时显示步骤、截图 |
| 截图保存 | 每步截图保存并可访问 |
| 断言结果准确 | AI 断言 + 代码断言结果一致 |
| API 响应正常 | 所有 REST API 返回正确格式 |

---

## 11. 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| DeepSeek API 不稳定 | 自动切换到 GPT-4o 备选 |
| SSE 连接中断 | 前端实现重连机制 |
| 截图存储空间 | 定期清理旧截图，限制保留天数 |
| 浏览器资源占用 | 执行完成后及时关闭浏览器 |

---

## 12. 后续扩展

完成登录场景后，可逐步扩展：

1. **采购单表单**：侧边栏导航 + 表单填写
2. **发货单表单**：类似采购单
3. **批量测试**：多场景并行执行
4. **定时任务**：支持定时自动执行
5. **报告导出**：PDF/Excel 报告导出
6. **API 断言**：支持调用后端 API 验证
