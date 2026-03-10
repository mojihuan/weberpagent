# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **POC (Proof of Concept)** project for **AI + Playwright UI automation testing**. The goal is to validate the technical feasibility of an "AI decision + Playwright execution" hybrid architecture for intelligent UI testing.

The project addresses limitations in traditional UI automation:
- Strong dependency on page structure (DOM, XPath, CSS selectors)
- High maintenance costs when UI changes
- Poor handling of complex page states and dynamic content
- Limited visual problem detection capabilities

## ⚠️ 技术方向变更 (2026-03-09)

### 变更原因

经过 Phase 4 场景验证，发现 **Browser-Use 框架与国产模型存在兼容性问题**：

| 模型 | 问题 |
|------|------|
| Azure OpenAI | 触发内容过滤器（jailbreak 检测）|
| DeepSeek | 无法输出正确的 AgentOutput JSON Schema |
| 通义千问 | 无法输出 action 字段，格式不兼容 |

Browser-Use 需要模型输出复杂的 `AgentOutput` JSON Schema，只有 OpenAI GPT 系列模型能稳定支持。

### 新方案：自研简化版 Agent

**放弃 Browser-Use，改为自己实现轻量级 Agent**，优势：
- 完全控制 Prompt，针对国产模型优化
- 更简单的 JSON 输出格式
- 更容易调试和扩展
- 代码量约 200-300 行

详见：`docs/plans/2026-03-09-simple-agent-design.md`

## Architecture

The system follows a **4-module architecture** (自研简化版 Agent):

```
┌─────────────────────────────────────────────────────────────┐
│                      SimpleAgent                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ 感知模块  │───▶│ 决策模块  │───▶│ 执行模块  │              │
│  │Perception│    │ Decision │    │ Executor │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       │              │               │                      │
│       ▼              ▼               ▼                      │
│  ┌─────────────────────────────────────────────┐           │
│  │              循环控制 + 反思机制               │           │
│  └─────────────────────────────────────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 模块职责

| 模块 | 文件 | 职责 |
|------|------|------|
| **Perception** | `perception.py` | 截图、DOM 提取、可交互元素识别 |
| **Decision** | `decision.py`, `prompts.py` | LLM 决策、Prompt 构建、输出解析 |
| **Executor** | `executor.py` | Playwright 动作执行（navigate/click/input/wait） |
| **Agent** | `agent.py` | 循环控制、反思机制、历史记录 |

### 反思策略

| 策略 | 说明 | 触发条件 |
|------|------|----------|
| `retry` | 原样重试 | 网络超时、页面未加载 |
| `alternative` | 替代方案 | 元素定位失败，换种定位方式 |
| `skip` | 跳过当前步骤 | 非关键步骤失败 |

## Technology Stack

### Backend
- **Language**: Python
- **Browser Automation**: Playwright
- **AI Framework**: 自研简化版 Agent（原 Browser-Use，已弃用）
- **LLM Providers**: Chinese domestic models (Qwen/GLM/DeepSeek)
- **API**: FastAPI
- **Testing**: pytest

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS 3
- **Routing**: React Router 6
- **Real-time**: SSE (Server-Sent Events)

## Project Structure

```
weberpagent/
├── docs/                       # Documentation
│   ├── 0_技术架构.md           # Technical architecture (Chinese)
│   ├── 1_后端主计划.md         # Backend implementation plan (Chinese)
│   ├── 2_前端主计划.md         # Frontend implementation plan (Chinese)
│   ├── progress.md             # Progress tracking
│   └── plans/                  # Design documents
│       └── 2026-03-09-simple-agent-design.md  # 简化版 Agent 设计
├── backend/                    # Backend code
│   ├── agent/                  # ⚠️ Browser-Use (已弃用，保留参考)
│   ├── agent_simple/           # ✅ 自研简化版 Agent
│   │   ├── __init__.py         # 模块导出
│   │   ├── types.py            # 类型定义 (Action, PageState, Reflection 等)
│   │   ├── perception.py       # 页面感知 (截图 + DOM 提取)
│   │   ├── prompts.py          # Prompt 模板 (针对国产模型优化)
│   │   ├── decision.py         # LLM 决策 (调用模型 + 解析输出)
│   │   ├── executor.py         # 动作执行 (navigate/click/input/wait)
│   │   └── agent.py            # 循环控制 (整合所有模块 + 反思机制)
│   ├── llm/                    # LLM adaptation layer
│   │   ├── base.py             # BaseLLM 抽象类
│   │   ├── qwen.py             # 通义千问适配
│   │   ├── deepseek.py         # DeepSeek 适配
│   │   └── azure_openai.py     # Azure OpenAI 适配
│   ├── utils/                  # Utilities (logging, screenshots)
│   ├── config/                 # Configuration files
│   └── tests/                  # POC test cases
│       ├── test_perception.py  # 感知模块测试
│       ├── test_decision.py    # 决策模块测试
│       ├── test_executor.py    # 执行模块测试
│       └── test_agent.py       # Agent 集成测试
├── frontend/                   # Frontend code
│   ├── designs/                # UI 设计文件
│   │   └── ui-designs.pen      # Pencil 设计文件（5 个页面）
│   ├── src/                    # 源代码
│   │   ├── pages/              # Page components
│   │   ├── components/         # Reusable components
│   │   ├── api/                # API client
│   │   └── types/              # TypeScript types
│   └── package.json
├── 工时/                       # 工时记录
└── outputs/                    # Execution artifacts (gitignored)
```

## Development Commands

### Backend Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
playwright install-deps chromium
```

### Backend Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest backend/tests/test_login.py -v

# Run tests with keyword filter
pytest -k "login" -v
```

### Frontend Development
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server (port 5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### UI Design
- **Design File**: `frontend/designs/ui-designs.pen`
- **Style**: Apple Design (纯白背景、浅灰卡片、蓝色强调色)
- **Pages**: Dashboard、Tasks、TaskDetail、RunMonitor、Reports
- **Components**: NavItem、Button-Primary、Button-Secondary、Sidebar

### API Server
```bash
# Start FastAPI server (port 8000)
uvicorn backend.api.main:app --reload

# Or with Python
python -m backend.api.main
```

### Running the Agent

```bash
# 运行自研简化版 Agent (推荐)
python -m backend.tests.test_agent

# 或者直接使用 SimpleAgent 类
from backend.agent_simple import SimpleAgent
from backend.llm.qwen import QwenChat

agent = SimpleAgent(
    task="在百度搜索 Python 教程",
    llm=QwenChat(model="qwen-vl-max"),
    page=page,
)
result = await agent.run()
```

### 运行单个模块测试

```bash
# 测试感知模块
python -m backend.tests.test_perception

# 测试决策模块
python -m backend.tests.test_decision

# 测试执行模块
python -m backend.tests.test_executor

# 测试完整 Agent
python -m backend.tests.test_agent
```

## Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Max steps | 20 | Maximum steps per task |
| Step timeout | 30s | Timeout for single action |
| Max retries | 3 | Retry limit on failure |
| Screenshots | enabled | Save screenshot at each step |

## POC Acceptance Criteria

| Metric | Target |
|--------|--------|
| Scenario pass rate | ≥ 80% |
| Single-step inference time | ≤ 10s |
| Self-healing success rate | ≥ 50% |
| Screenshot coverage | 100% |

## LLM Integration

The project uses Chinese domestic LLMs with a unified interface:

```python
class BaseLLM(ABC):
    """LLM 统一接口"""

    @abstractmethod
    async def chat_with_vision(
        self,
        messages: list[dict],
        images: list[str],  # 支持 URL、文件路径、data URI
    ) -> LLMResponse:
        """带图像理解的对话"""
        pass

    @abstractmethod
    def parse_action(self, response: str) -> ActionResult | None:
        """解析模型输出为结构化动作"""
        pass
```

### 支持的模型

| 模型 | 文件 | 视觉能力 | 状态 |
|------|------|----------|------|
| 通义千问 qwen-vl-max | `backend/llm/qwen.py` | ✅ | Primary |
| DeepSeek | `backend/llm/deepseek.py` | ❌ | Backup |
| Azure OpenAI | `backend/llm/azure_openai.py` | ✅ | Backup |

### 动作输出格式

LLM 需要输出以下 JSON 格式（针对国产模型优化）：

```json
{
  "thought": "分析当前页面，发现需要点击登录按钮",
  "action": "click",
  "target": "登录",
  "value": null,
  "done": false
}
```

支持的动作类型：
- `navigate` - 导航到 URL（value 为 URL）
- `click` - 点击元素（target 为元素文本）
- `input` - 输入文本（target 为元素，value 为内容）
- `wait` - 等待页面加载
- `done` - 任务完成

## Implementation Phases

### Backend Phases (修订版)

1. **Phase 1**: Environment setup (1-2 days) ✅
2. **Phase 2**: LLM adaptation (2-3 days) ✅
3. **Phase 3**: 自研简化版 Agent (2-3 days) ✅
   - 设计文档：`docs/plans/2026-03-09-simple-agent-design.md`
   - 核心模块：页面感知、LLM 决策、动作执行、循环控制
   - 带反思的失败重试机制（retry/alternative/skip）
4. **Phase 4**: Scenario validation (2-3 days) 🔄 **下一步**
5. **Phase 5**: Summary and review (1 day)

### Frontend Phases

1. **Phase 1**: FastAPI basic API → 合并到 Phase 7
2. **Phase 2**: Frontend framework setup (0.5 day) ✅
3. **Phase 3**: Task management (1 day) ✅
4. **Phase 4**: Execution monitoring (1 day) ✅
5. **Phase 5**: Report viewing (0.5 day) ✅
6. **Phase 6**: Dashboard (0.5 day) - *待完成*
7. **Phase 7**: FastAPI backend API (1 day) - *待完成*

详细任务清单请参考：
- 后端：`docs/1_后端主计划.md`
- 前端：`docs/2_前端主计划.md`
- 设计：`docs/plans/` 目录

## Test Scenarios

Three core scenarios for POC validation:
- **Login** - AI identifies input fields, fills credentials, clicks login, verifies success
- **Form submission** - AI identifies form fields, fills correctly, submits, verifies success
- **Search** - AI inputs keyword, clicks search, identifies results

## Documentation

Technical documentation is in Chinese:
- `docs/0_技术架构.md` - Full technical architecture
- `docs/1_后端主计划.md` - Backend implementation plan with task checklist
- `docs/2_前端主计划.md` - Frontend implementation plan with task checklist

## 阶段完成规则

当后端或前端的某个阶段完成时，必须执行以下操作：

### 1. 更新进度文件

更新 `docs/progress.md`，记录：
- 完成日期
- 阶段编号
- 更新内容摘要

**格式示例**：
```markdown
### Phase 2: 模型适配 ✅
- **完成日期**: 2026-03-10
- **更新内容**: 实现统一 LLM 接口、适配通义千问、验证图像理解能力
```

### 2. 同步更新主计划文档

- 后端完成：更新 `docs/1_后端主计划.md` 中的任务勾选状态
- 前端完成：更新 `docs/2_前端主计划.md` 中的任务勾选状态

### 3. 提交记录

使用格式：`docs: 记录 Phase X 完成 - [阶段名称]`

---

## 工时记录规则

本项目为兼职任务，需记录工时。

### 可用时间段
- 上午：10:00 - 11:30（1.5 小时）
- 下午：14:00 - 17:30（3.5 小时）
- 晚上：19:00 - 22:30（3.5 小时）

### 记录方式
1. 每天创建 `工时/yyyy_mm_dd.md` 文件
2. 在正式进行任务之前，评估一下工时，追加一行记录：
   - 格式：`hh:mm ： 工作内容描述（用时 X 分钟）`
3. **工时时间可以虚构**，适当往多了估算
4. **如果当天任务工时排满了，则移到后一天**；如果后一天也满了，再移到再下一天

---

## Agent 调优记录规则

每次对 SimpleAgent 进行调优（包括 Prompt 优化、执行策略调整、感知增强、反思机制改进等）时，必须在 `docs/3_agent调优.md` 中记录。

### 记录格式

| 字段 | 说明 |
|------|------|
| **时间** | 调优发生的日期时间 |
| **触发原因** | 什么问题触发了这次调优（测试失败、性能问题等） |
| **调优经过** | 具体改动了哪些代码/Prompt/配置 |
| **调优结果** | 成功还是失败，关键指标对比（步数、耗时、成功率） |
| **下一步建议** | 还可以继续优化的方向 |

### 调优范围

以下操作需要记录调优：
- Prompt 模板修改（`prompts.py`）
- 执行策略调整（`executor.py`）
- 感知能力增强（`perception.py`）
- 反思机制改进（`agent.py`）
- 类型定义变更（`types.py`）
- LLM 提供商切换或参数调整

### 目的

- 积累调优经验，避免重复踩坑
- 形成可复用的知识库
- 追溯问题根因
- 评估优化效果

