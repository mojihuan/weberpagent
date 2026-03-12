# CLAUDE.md

## Project Overview

AI + Playwright UI 自动化测试平台。使用 Browser-Use + OpenAI 构建"AI 决策 + Playwright 执行"混合架构。

**当前阶段**: Phase 10 - Browser-Use 重构（2026-03-12）

## Tech Stack

**Backend**: Python, Playwright, Browser-Use, OpenAI GPT-4o, FastAPI, pytest

**Frontend**: React 18, TypeScript, Vite 5, Tailwind CSS 3, React Router 6, SSE

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser-Use Agent                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  感知    │───▶│  决策    │───▶│  执行    │              │
│  │ Browser  │    │ OpenAI   │    │Playwright│              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       │              │               │                      │
│       ▼              ▼               ▼                      │
│  ┌─────────────────────────────────────────────┐           │
│  │              DOM Tree + Screenshot           │           │
│  └─────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## 模块职责

| 模块 | 文件 | 职责 |
|------|------|------|
| Browser Agent | `backend/agent/browser_agent.py` | Browser-Use Agent 封装 |
| LLM Wrapper | `backend/llm/openai.py` | OpenAI API 封装 |
| Test Runner | `backend/tests/test_agent.py` | 测试脚本 |

### 归档代码

自研 SimpleAgent 已归档到 `backend/agent_simple_archived/`，保留参考。

## Key Commands

**Backend**
```bash
source .venv/bin/activate && pip install -r requirements.txt
playwright install chromium
python -m backend.tests.test_agent        # 运行 Agent 测试
```

**Frontend**
```bash
cd frontend && npm install && npm run dev # 启动开发服务器
```

**API Server**
```bash
uvicorn backend.api.main:app --reload    # 启动 FastAPI
```

## Documentation

**当前阶段计划** (`docs/plans/`)：
- `2026-03-12-browser-use-restart-design.md` - 架构重设计
- `2026-03-12-browser-use-restart-impl.md` - 实施计划
- `2026-03-12-browser-use-backend-impl.md` - 后端开发详情
- `2026-03-12-multi-llm-config.md` - 多 LLM 配置

**归档文档** (`docs/_archived/phase-1-9/`)：
- Phase 1-9 的技术架构、实施计划、调优记录等历史文档
