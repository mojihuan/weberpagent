# CLAUDE.md

## Project Overview

AI + Playwright UI 自动化测试 POC 项目。验证"AI 决策 + Playwright 执行"混合架构的可行性，解决传统 UI 自动化对页面结构依赖强、维护成本高的问题。

## Tech Stack

**Backend**: Python, Playwright, 自研 Agent, 通义千问/GLM/DeepSeek, FastAPI, pytest

**Frontend**: React 18, TypeScript, Vite 5, Tailwind CSS 3, React Router 6, SSE

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      SimpleAgent                             │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ 感知模块  │───▶│ 决策模块  │───▶│ 执行模块  │              │
│  │Perception│    │ Decision │    │ Executor │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       │              │               │                      │
│       ▼              ▼               ▼                      │
│  ┌─────────────────────────────────────────────┐           │
│  │              循环控制 + 反思机制               │           │
│  └─────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### 模块职责

| 模块 | 文件 | 职责 |
|------|------|------|
| Perception | `perception.py` | 截图、DOM 提取、元素识别 |
| Decision | `decision.py`, `prompts.py` | LLM 决策、Prompt 构建、输出解析 |
| Executor | `executor.py` | Playwright 动作执行 |
| Agent | `agent.py` | 循环控制、反思机制 |

### 反思策略

| 策略 | 触发条件 |
|------|----------|
| `retry` | 网络超时、页面未加载 |
| `alternative` | 元素定位失败 |
| `skip` | 非关键步骤失败 |

## Key Commands

**Backend**
```bash
source .venv/bin/activate && pip install -r requirements.txt
playwright install chromium
pytest                                    # 运行测试
python -m backend.tests.test_agent        # 运行 Agent
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
