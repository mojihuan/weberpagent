# CLAUDE.md

## Project Overview

AI + Playwright UI 自动化测试平台。使用 Browser-Use + 阿里云 Qwen 3.5 Plus 构建"AI 决策 + Playwright 执行"混合架构。

**当前阶段**: Phase 10 - Browser-Use 集成完成（2026-03-12）

## Tech Stack

**Backend**: Python 3.11, Playwright, Browser-Use 0.12.1, 阿里云 Qwen 3.5 Plus, FastAPI, pytest

**Frontend**: React 18, TypeScript, Vite 5, Tailwind CSS 3, React Router 6, SSE

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser-Use Agent                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  感知    │───▶│  决策    │───▶│  执行    │              │
│  │ Browser  │    │ Qwen 3.5 │    │Playwright│              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       │              │               │                      │
│       ▼              ▼               ▼                      │
│  ┌─────────────────────────────────────────────┐           │
│  │              DOM Tree + Screenshot           │           │
│  └─────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## LLM 配置

**推荐**: 阿里云 DashScope + Qwen 3.5 Plus

```python
from browser_use import Agent, ChatOpenAI

llm = ChatOpenAI(
    model="qwen3.5-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

agent = Agent(task="...", llm=llm, use_vision=True)
result = await agent.run()
```

**环境变量 (.env)**:
```bash
DASHSCOPE_API_KEY=sk-xxx
ERP_BASE_URL=https://erptest.epbox.cn
ERP_USERNAME=xxx
ERP_PASSWORD=xxx
```

**备选 API**:
| API | 模型 | 状态 |
|-----|------|------|
| 阿里云 DashScope | qwen3.5-plus | ✅ 推荐 |
| Univibe 中转站 | gpt-5, claude-sonnet-4-6 | ⚠️ 兼容性问题 |
| DeepSeek | deepseek-chat | ❌ 不支持 JSON 格式 |

## 模块职责

| 模块 | 文件 | 职责 |
|------|------|------|
| Browser Agent | `backend/tests/test_login_browser_use.py` | Browser-Use 登录测试 |
| Task Store | `backend/storage/task_store.py` | 任务存储 (JSON) |
| Run Store | `backend/storage/run_store.py` | 执行记录存储 (JSON) |
| Assertion Service | `backend/core/assertion_service.py` | 断言验证服务 |
| API Routes | `backend/api/routes/` | FastAPI 路由 |

### 归档代码

自研 SimpleAgent 已归档到 `backend/agent_simple_archived/`，保留参考。

## Key Commands

**Backend**
```bash
source .venv/bin/activate && pip install -r requirements.txt
playwright install chromium
python -m pytest backend/tests/test_login_browser_use.py -v  # 运行登录测试
```

**Frontend**
```bash
cd frontend && npm install && npm run dev # 启动开发服务器
```

**API Server**
```bash
uvicorn backend.api.main:app --reload --port 8080  # 启动 FastAPI
```

## Documentation

**当前阶段计划** (`docs/plans/`):
- `browser-use-restart-design.md` - 架构重设计
- `browser-use-restart-impl.md` - 实施计划

**归档文档** (`docs/_archived/phase-1-9/`)：
- Phase 1-9 的技术架构、实施计划、调优记录等历史文档

## Test Results

**Phase 5 ERP 登录验证** (2026-03-12):
- ✅ `test_browser_navigation` - PASSED
- ✅ `test_erp_login` - PASSED (364.39s)
