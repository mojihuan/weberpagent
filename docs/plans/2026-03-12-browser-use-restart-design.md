# Browser-Use Restart 设计文档

> 最后更新：2026-03-12
> 状态：✅ 已批准

---

## 1. 项目目标

构建 **AI + Playwright UI 自动化测试平台**，使用 Browser-Use + DeepSeek 实现 ERP 系统自动化测试。

### 核心价值

| 价值点 | 说明 |
|--------|------|
| 🤖 AI 驱动 | 自然语言描述测试任务，AI 自动决策执行 |
| 🔄 实时反馈 | SSE 推送执行进度、截图、AI 推理过程 |
| ✅ 双重断言 | AI 判断 + 代码断言双重验证 |
| 🎯 优先场景 | 登录/认证流程优先 |

---

## 2. 技术架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    前端 (React + Vite)                       │
│   Dashboard / Tasks / RunMonitor / Reports                  │
│   ────────────────────────────────────────────────          │
│   EventSource ← SSE 实时推送                                │
└─────────────────────┬───────────────────────────────────────┘
                      │ REST + SSE
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI 后端                              │
├─────────────────────────────────────────────────────────────┤
│  路由层 (backend/api/)                                       │
│  ├── routes/tasks.py    任务 CRUD                           │
│  ├── routes/runs.py     执行管理 + SSE                       │
│  └── schemas/           Pydantic 模型                       │
├─────────────────────────────────────────────────────────────┤
│  核心层 (复用现有代码)                                        │
│  ├── backend/llm/factory.py    LLM 工厂 ✅ 已存在            │
│  ├── backend/agent/            Agent 封装 ✅ 已存在          │
│  └── backend/core/             新增服务                      │
├─────────────────────────────────────────────────────────────┤
│  数据层 (backend/storage/)                                   │
│  ├── task_store.py      任务存储 (JSON)                      │
│  └── run_store.py       执行记录 (JSON)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              browser-use Agent (原生)                        │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│   │  感知    │───▶│  决策    │───▶│  执行    │             │
│   │ Browser  │    │ DeepSeek │    │Playwright│             │
│   └──────────┘    └──────────┘    └──────────┘             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 目录结构

```
backend/
├── api/                      # FastAPI 路由层 (新增)
│   ├── __init__.py
│   ├── main.py               # FastAPI 入口
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tasks.py          # 任务 CRUD
│   │   └── runs.py           # 执行管理 + SSE
│   └── schemas/
│       ├── __init__.py
│       └── index.py          # Pydantic 模型
├── core/                     # 核心服务 (新增)
│   ├── __init__.py
│   ├── agent_service.py      # browser-use 服务封装
│   └── assertion_service.py  # 断言服务
├── storage/                  # 存储层 (新增)
│   ├── __init__.py
│   ├── task_store.py         # 任务存储
│   └── run_store.py          # 执行记录存储
├── llm/                      # LLM 层 ✅ 已存在
│   ├── factory.py            # LLM 工厂
│   ├── openai.py             # OpenAI/DeepSeek 封装
│   └── config.py             # LLM 配置
├── agent/                    # Agent 层 ✅ 已存在
│   ├── browser_agent.py      # browser-use Agent 封装
│   └── prompts.py            # 提示词
├── utils/                    # 工具层 ✅ 已存在
│   ├── logger.py
│   └── screenshot.py
├── _archived/                # 归档代码 ✅ 已存在
└── tests/                    # 测试 ✅ 已存在
```

---

## 3. 数据模型

### 3.1 任务模型 (Task)

```python
class Task(BaseModel):
    id: str                    # UUID
    name: str                  # 任务名称
    description: str           # 自然语言任务描述
    assertions: list[Assertion]  # 断言列表
    created_at: datetime
    updated_at: datetime

class Assertion(BaseModel):
    name: str                  # 断言名称
    type: Literal["url_contains", "text_exists", "no_errors"]
    expected: str | bool       # 期望值
```

### 3.2 执行记录模型 (Run)

```python
class Run(BaseModel):
    id: str                    # UUID
    task_id: str               # 关联任务 ID
    status: Literal["pending", "running", "completed", "failed"]
    steps: list[Step]          # 执行步骤
    result: RunResult | None   # 执行结果
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None

class Step(BaseModel):
    step: int                  # 步骤编号
    action: str                # 动作类型
    reasoning: str             # AI 推理
    screenshot: str | None     # 截图路径
    timestamp: datetime

class RunResult(BaseModel):
    success: bool              # 是否成功
    ai_assertion: dict         # AI 断言结果
    code_assertion: dict       # 代码断言结果
    duration_seconds: float    # 执行时长
    total_steps: int           # 总步数
```

---

## 4. API 设计

### 4.1 REST API

```
任务管理
  GET    /api/tasks           # 列表
  POST   /api/tasks           # 创建
  GET    /api/tasks/{id}      # 详情
  PUT    /api/tasks/{id}      # 更新
  DELETE /api/tasks/{id}      # 删除

执行管理
  POST   /api/runs            # 创建执行记录
  GET    /api/runs            # 执行列表
  GET    /api/runs/{id}       # 执行详情
  POST   /api/runs/{id}/execute  # 执行并返回 SSE 流
  POST   /api/runs/{id}/stop  # 停止执行
```

### 4.2 SSE 事件格式

```
event: step
data: {"step": 1, "action": "click", "reasoning": "点击登录按钮", "screenshot": "/screenshots/1.png"}

event: complete
data: {"success": true, "duration_seconds": 12.5, "total_steps": 5}

event: error
data: {"error": "LLM API 超时"}
```

---

## 5. 实施计划

### Phase 1: 依赖更新 + 代码结构整理 (0.5h)

**任务：**
1. 更新 `pyproject.toml` 添加缺失依赖
2. 创建 `backend/api/`, `backend/core/`, `backend/storage/` 目录结构
3. 运行 `uv sync` 安装依赖

**验收：**
- 依赖安装无错误
- 目录结构创建完成

### Phase 2: 核心服务开发 (1.5h)

**任务：**
1. 创建 `backend/core/agent_service.py` - 封装 browser-use Agent
2. 创建 `backend/core/assertion_service.py` - 断言服务
3. 创建 `backend/storage/task_store.py` - 任务存储
4. 创建 `backend/storage/run_store.py` - 执行记录存储

**验收：**
- 单元测试通过
- 覆盖率 ≥ 80%

### Phase 3: FastAPI 路由开发 (2h)

**任务：**
1. 创建 Pydantic 模型 `backend/api/schemas/`
2. 创建任务路由 `backend/api/routes/tasks.py`
3. 创建执行路由 + SSE `backend/api/routes/runs.py`
4. 创建 FastAPI 入口 `backend/api/main.py`

**验收：**
- `uvicorn backend.api.main:app` 启动成功
- `/docs` Swagger UI 可访问
- SSE 推送正常

### Phase 4: 前后端联调 (1h)

**任务：**
1. 配置 CORS
2. 前端对接真实 API
3. 移除 Mock 数据

**验收：**
- 前端任务列表显示真实数据
- 执行任务时 SSE 实时推送

### Phase 5: ERP 登录验证 (1h)

**任务：**
1. 创建登录测试任务
2. 执行端到端测试
3. 验证双重断言

**验收：**
- 登录测试通过
- 截图保存正确

### Phase 6: 文档收尾 (0.5h)

**任务：**
1. 更新 CLAUDE.md
2. 更新主计划状态
3. 创建 Git Tag

**验收：**
- 文档反映最新架构
- Git Tag 创建成功

---

## 6. 风险与缓解

| 风险 | 等级 | 缓解措施 |
|------|:----:|----------|
| DeepSeek API 不稳定 | 🔴 高 | 自动切换到 GPT-4o 备选 |
| SSE 连接中断 | 🟡 中 | 前端实现重连机制 |
| browser-use 版本变化 | 🟡 中 | 锁定版本号 |

---

## 7. 技术决策

| # | 决策点 | 决策 | 理由 |
|---|--------|------|------|
| D1 | LLM 选择 | DeepSeek 优先 | 成本低，中文能力强 |
| D2 | 架构模式 | browser-use 原生 API | 减少维护负担 |
| D3 | 实时推送 | SSE | 简单、单向、足够 |
| D4 | 存储方案 | JSON 文件 | 轻量、无需数据库 |
| D5 | 复用现有代码 | 保留 llm/, agent/, utils/ | 已验证可用 |
