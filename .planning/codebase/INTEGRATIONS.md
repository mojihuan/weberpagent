# External Integrations

**Analysis Date:** 2026-04-03

## APIs & External Services

**LLM Providers:**
- **DashScope (Alibaba Cloud)** - Primary LLM provider
  - SDK: `dashscope>=1.20.0`
  - Models: qwen-vl-max, qwen3.5-plus
  - Base URL: `https://dashscope.aliyuncs.com/compatible-mode/v1`
  - Auth: `DASHSCOPE_API_KEY` environment variable

- **OpenAI Compatible APIs** - Via browser-use ChatOpenAI adapter
  - SDK: `browser-use` built-in ChatOpenAI
  - Base URL: Configurable via `LLM_BASE_URL`
  - Auth: `OPENAI_API_KEY` environment variable

**Browser Automation:**
- **browser-use Framework**
  - Core: CDP-based browser control
  - Models: Inherits from langchain Runnable interfaces
  - Configuration: `backend/agent/monitored_agent.py`

- **Chrome/Chromium**
  - Headless mode for server environments
  - Args: `--no-sandbox`, `--disable-setuid-sandbox`, `--disable-dev-shm-usage`

## Data Storage

**Databases:**
- **SQLite** (development default)
  - Connection: `aiosqlite` async driver
  - ORM: SQLAlchemy 2.0 with async support
  - Location: `data/database.db`
  - Schema: WAL mode for concurrent access

**File Storage:**
- **Local filesystem**
  - Screenshots: `outputs/{run_id}/screenshots/step_N.png`
  - DOM snapshots: `outputs/{run_id}/dom/step_N.txt`
  - Logs: `outputs/{run_id}/logs/run.jsonl`

**Caching:**
- **In-memory** - EventManager for SSE subscriptions
- **React Query** - Frontend data caching

## Authentication & Identity

**ERP System:**
- Basic HTTP authentication
- Env vars: `ERP_USERNAME`, `ERP_PASSWORD`
- Target URL: `ERP_BASE_URL`

**LLM APIs:**
- API key authentication
- Env vars: `DASHSCOPE_API_KEY`, `OPENAI_API_KEY`

## Monitoring & Observability

**Error Tracking:**
- Python `logging` module with structured output
- DEBUG level for browser-use traces
- JSONL per-run logs for post-mortem analysis

**Logs:**
```
outputs/{run_id}/logs/run.jsonl
  - timestamp, level, category, message, run_id
  - Categories: step, browser, agent, system, monitor
```

**SSE Events:**
- `event: started` - Run started
- `event: step` - Per-step updates
- `event: precondition` - Precondition execution
- `event: assertion` - Assertion results
- `event: finished` - Run completed
- `event: error` - Error occurred
- `:heartbeat` - Keep-alive comments (20s interval)

## CI/CD & Deployment

**Hosting:**
- Server: Linux (production at 121.40.191.49)
- Backend: FastAPI + uvicorn + gunicorn (2 workers)
- Frontend: Static build served via Nginx

**CI Pipeline:**
- pytest: Backend unit tests
- Ruff: Python linting
- Playwright: E2E tests

## Environment Configuration

**Required env vars:**
| Variable | Description | Default |
|----------|-------------|---------|
| `DASHSCOPE_API_KEY` | Alibaba Cloud AI API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `LLM_MODEL` | Model name | qwen3.5-plus |
| `LLM_BASE_URL` | API base URL | dashscope endpoint |
| `LLM_TEMPERATURE` | Model temperature | 0.0 |
| `ERP_BASE_URL` | Target ERP URL | - |
| `ERP_USERNAME` | ERP username | - |
| `ERP_PASSWORD` | ERP password | - |
| `WEBSERP_PATH` | webseleniumerp project path | - |

**Secrets location:**
- `.env` file (local development)
- Environment variables (production)
- Never committed to git

## Webhooks & Callbacks

**Incoming:**
- `GET /api/runs/{run_id}/stream` - SSE subscription
- REST endpoints for CRUD operations

**Outgoing:**
- LLM API calls (DashScope/OpenAI)
- ERP system interactions (via browser automation)

---

*Integration audit: 2026-04-03*
