# CLAUDE.md

## Project Overview

AI + Playwright UI 自动化测试 POC 项目。验证"AI 决策 + Playwright 执行"混合架构的可行性，解决传统 UI 自动化对页面结构依赖强、维护成本高的问题。

**当前架构**: Browser-Use + OpenAI（2026-03-12 重新集成）

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

### 模块职责

| 模块 | 文件 | 职责 |
|------|------|------|
| Browser Agent | `backend/agent/browser_agent.py` | Browser-Use Agent 封装 |
| LLM Wrapper | `backend/llm/openai.py` | OpenAI API 封装 |
| Test Runner | `backend/tests/test_agent.py` | 测试脚本 |

### 归档代码

自研 SimpleAgent 已归档到 `backend/agent_simple_archived/`，保留参考：
- `perception.py` - 页面感知
- `decision.py` - LLM 决策
- `executor.py` - 动作执行
- `agent.py` - 循环控制

详见：`docs/plans/2026-03-12-browser-use-restart-design.md`

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

## Reference

- `docs/0_技术架构.md` - 完整技术架构
- `docs/1_后端主计划.md` - 后端实施计划
- `docs/2_前端主计划.md` - 前端实施计划
- `docs/3_agent调优.md` - Agent 调优记录
- `docs/4_Agent开发.md` - 多 Agent 协作模式
- `docs/workflow.md` - 阶段完成规则、工时记录
- `docs/llm-integration.md` - LLM 集成详情
- `docs/progress.md` - 进度跟踪
- `docs/plans/2026-03-12-browser-use-restart-design.md` - Browser-Use 重新集成设计
