# External Integrations

**Analysis Date:** 2026-05-02

## APIs & External Services

**LLM Providers:**
- **DashScope (Alibaba Cloud)** - Primary LLM provider for Qwen models
  - SDK: `dashscope>=1.20.0` and `langchain-openai>=0.3.0`
  - Default model: qwen3.5-plus
  - Base URL: `https://dashscope.aliyuncs.com/compatible-mode/v1`
  - Auth: `DASHSCOPE_API_KEY` environment variable
  - Integration: `backend/llm/openai.py` wraps ChatOpenAI with DashScope-compatible base URL
  - Config loader: `backend/llm/config.py` loads per-module model assignments from YAML

- **OpenAI Compatible APIs** - Via langchain ChatOpenAI and browser-use built-in ChatOpenAI
  - SDK: `langchain-openai` in `backend/llm/openai.py`, `browser-use` built-in in `backend/llm/factory.py`
  - Base URL: Configurable via `LLM_BASE_URL` or `code_gen_base_url`
  - Auth: `OPENAI_API_KEY` environment variable
  - Supports separate model config for code generation: `code_gen_model`, `code_gen_api_key`, `code_gen_base_url` in `backend/config/settings.py`

**ERP System Under Test:**
- **Target ERP** - The web application being tested by the AI agent
  - URL: `ERP_BASE_URL` env var (example: `https://erptest.epbox.cn`)
  - Authentication: HTTP POST to `/auth/login` endpoint
  - Auth service: `backend/core/auth_service.py` fetches tokens via httpx
  - Account service: `backend/core/account_service.py` maps role names (main, special, vice, camera, platform, super, idle) to credentials
  - Login roles: Defined in `backend/config/test_targets.yaml`

**Browser Automation:**
- **browser-use Framework** - AI-powered browser control
  - Core classes: `Agent`, `BrowserSession`, `BrowserProfile` in `backend/core/agent_service.py`
  - MonitoredAgent subclass: `backend/agent/monitored_agent.py` adds stall detection, submit guarding, progress tracking
  - DOM patching: `backend/agent/dom_patch.py`
  - Pre-submit validation: `backend/agent/pre_submit_guard.py`
  - Stall detection: `backend/agent/stall_detector.py`
  - Custom prompts: `backend/agent/prompts.py`

- **Chrome/Chromium** - Headless browser for test execution
  - Configuration: `SERVER_BROWSER_ARGS` in `backend/core/agent_service.py`
  - Headless mode: `headless=True`, viewport 1920x1080
  - Args: `--no-sandbox`, `--disable-setuid-sandbox`, `--disable-dev-shm-usage`, `--disable-gpu`

## Data Storage

**Databases:**
- **SQLite** with async driver
  - Connection string: `sqlite+aiosqlite:///./data/database.db`
  - ORM: SQLAlchemy 2.0 async (`create_async_engine`, `async_sessionmaker`)
  - Configuration: `backend/db/database.py`
  - Pool: size=5, max_overflow=0, pool_pre_ping=True, pool_recycle=3600s
  - Busy timeout: 30s for lock contention during batch execution
  - Schema migration: Inline ALTER TABLE in `init_db()` function (no Alembic)
  - Models: `backend/db/models.py` (Task, Batch, Run, Step, Assertion, AssertionResult, PreconditionResult, Report)
  - Repository layer: `backend/db/repository.py` (CRUD operations with async sessions)
  - Schemas: `backend/db/schemas.py` and `backend/api/schemas/index.py`

**File Storage:**
- **Local filesystem**
  - Database: `backend/data/database.db`
  - Screenshots: `outputs/{run_id}/screenshots/step_N.png`
  - DOM snapshots: `outputs/{run_id}/dom/step_N.txt`
  - Logs: `outputs/{run_id}/logs/run.jsonl`
  - Generated test code: stored in `runs.generated_code_path`
  - Test upload files: `data/test-files/`
  - Screenshot utility: `backend/utils/screenshot.py`

**Caching:**
- **In-memory CacheService** - Run-scoped key-value cache with deep-copy immutability
  - Implementation: `backend/core/cache_service.py`
  - Lifecycle: Tied to a single Run execution
  - Replaces JSON file-based caching from webseleniumerp
- **React Query** - Frontend data caching (TanStack React Query 5.90.21)
  - Configuration: `refetchOnWindowFocus: false`
- **LLM instance cache** - `LLMFactory._instances` dict caches LLM instances by model name
  - Implementation: `backend/llm/factory.py`

## Authentication & Identity

**ERP System Authentication:**
- HTTP-based token acquisition (no browser needed)
  - Implementation: `backend/core/auth_service.py`
  - Method: POST to ERP `/auth/login` with account/password, extracts `access_token`
  - Error class: `TokenFetchError` with role name and human-readable reason
  - Multiple roles supported: main, special, vice, camera, platform, super, idle
  - Account resolution: `backend/core/account_service.py` maps role names to credentials from external `user_info.py`

**LLM API Authentication:**
- API key authentication
  - `DASHSCOPE_API_KEY` - DashScope (Alibaba Cloud)
  - `OPENAI_API_KEY` - OpenAI-compatible endpoints
  - `code_gen_api_key` - Separate key for code generation LLM (optional, falls back to default)

**No end-user authentication:**
- The platform itself has no user login system
- CORS configured with `allow_origins=["*"]` (open access)

## Monitoring & Observability

**Error Tracking:**
- Python `logging` module with structured output
- Global exception handlers in `backend/api/main.py` with request IDs
- JSONL per-run logs: `backend/utils/run_logger.py`
- Categories: step, browser, agent, system, monitor

**Logging Infrastructure:**
- Run logger: `backend/utils/run_logger.py` - Per-run JSONL log files
- Step code buffer: `backend/core/step_code_buffer.py`
- Error utilities: `backend/core/error_utils.py`
- General logger: `backend/utils/logger.py`

**Real-time Communication:**
- SSE (Server-Sent Events) for live run monitoring
  - Event manager: `backend/core/event_manager.py` (publish/subscribe with heartbeat)
  - Frontend hook: `frontend/src/hooks/useRunStream.ts` (EventSource connection)
  - Heartbeat interval: 20 seconds
  - Endpoint: `GET /api/runs/{run_id}/stream`

**SSE Event Types:**
- `event: started` - Run started
- `event: step` - Per-step progress updates
- `event: precondition` - Precondition execution results
- `event: assertion` - Assertion evaluation results
- `event: finished` - Run completed
- `event: error` - Error occurred
- `:heartbeat` - Keep-alive comments (20s interval)

## CI/CD & Deployment

**Hosting:**
- Server: Linux at 121.40.191.49
- Backend: FastAPI + uvicorn on port 8080
- Frontend: Static build served via Nginx from `/var/www/aidriveuitest/`
- Deployment script: `deploy.sh` at project root

**Deployment Commands:**
```bash
./deploy.sh                  # Full deploy (pull, install, build, restart)
./deploy.sh --backend-only   # Backend only
./deploy.sh --frontend-only  # Frontend only
./deploy.sh --skip-build     # Pull and restart without rebuild
./deploy.sh --stop           # Stop backend service
```

**CI Pipeline:**
- pytest: Backend unit/integration tests
- ruff: Python linting
- @playwright/test: E2E tests (configured in `e2e/playwright.config.ts`)
- E2E config: Sequential execution, 2min timeout, Chromium only

## Environment Configuration

**Required env vars:**
| Variable | Description | Default |
|----------|-------------|---------|
| `DASHSCOPE_API_KEY` | Alibaba Cloud AI API key | `""` (empty) |
| `OPENAI_API_KEY` | OpenAI API key | `""` (empty) |
| `LLM_MODEL` | Model name | `qwen3.5-plus` |
| `LLM_BASE_URL` | API base URL | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `LLM_TEMPERATURE` | Model temperature | `0.0` |
| `ERP_BASE_URL` | Target ERP URL | `""` (empty) |
| `ERP_USERNAME` | ERP username | `""` (empty) |
| `ERP_PASSWORD` | ERP password | `""` (empty) |
| `WEBSERP_PATH` | External webseleniumerp project path | `None` |
| `DATABASE_URL` | SQLite connection string | `sqlite+aiosqlite:///./data/database.db` |
| `LOG_LEVEL` | Logging level | `INFO` |

**Optional env vars:**
| Variable | Description | Default |
|----------|-------------|---------|
| `code_gen_model` | Code generation LLM model | Falls back to `LLM_MODEL` |
| `code_gen_api_key` | Code generation API key | Falls back to primary |
| `code_gen_base_url` | Code generation API URL | Falls back to `LLM_BASE_URL` |
| `erp_api_module_path` | External API module path | `None` |
| `VITE_API_BASE` | Frontend API base URL | `http://localhost:11002/api` |
| `VITE_API_PROXY_TARGET` | Vite dev proxy target | `http://localhost:11002` |

**Secrets location:**
- `.env` file at project root (local development, gitignored)
- `.env.example` committed as template (documents all variables)
- Environment variables on production server
- Never committed to git

## External Module Integration

**webseleniumerp Project:**
- Optional integration via `WEBSERP_PATH` env var
  - Validation: `backend/config/validators.py` checks directory structure and imports
  - Module loader: `backend/core/external_module_loader.py` - Lazy loading with caching
  - Method discovery: `backend/core/external_method_discovery.py` - Discovers operations, data methods, assertion classes
  - Execution engine: `backend/core/external_execution_engine.py` - Runs assertion/data methods
  - Precondition bridge: `backend/core/external_precondition_bridge.py` - Connects external ops to run pipeline
  - Required files in external project: `common/base_prerequisites.py`, `config/settings.py`

**Excel Test Case Import:**
- Format: `.xlsx` files parsed via openpyxl
  - Parser: `backend/utils/excel_parser.py`
  - Template definition: `backend/utils/excel_template.py`
  - Import via API: Excel upload endpoint in task routes

## Webhooks & Callbacks

**Incoming:**
- `GET /api/runs/{run_id}/stream` - SSE subscription for real-time run monitoring
- REST endpoints under `/api/` for CRUD operations on tasks, runs, batches, reports
- `POST /api/tasks/import` - Excel file upload for bulk test case import
- Static file serving for screenshots and generated code

**Outgoing:**
- LLM API calls to DashScope/OpenAI-compatible endpoints
- ERP system HTTP authentication (`/auth/login`)
- ERP system browser automation (navigating forms, clicking buttons)

## API Contracts

**REST API Response Format:**
All API responses follow a standard envelope defined in `backend/api/response.py`:
```python
{
    "success": boolean,
    "data": T | null,       # Present on success
    "error": {              # Present on failure
        "code": string,
        "message": string,
        "request_id": string
    },
    "meta": dict | null     # Pagination, totals, etc.
}
```

**API Route Prefixes:**
- `/api/tasks` - Task CRUD and import (`backend/api/routes/tasks.py`)
- `/api/runs` - Run execution and monitoring (`backend/api/routes/runs.py`, `runs_routes.py`, `run_pipeline.py`)
- `/api/reports` - Report generation and retrieval (`backend/api/routes/reports.py`)
- `/api/batches` - Batch execution management (`backend/api/routes/batches.py`)
- `/api/dashboard` - Dashboard aggregation (`backend/api/routes/dashboard.py`)
- `/api/external-operations` - External module operations (`backend/api/routes/external_operations.py`)
- `/api/external-data-methods` - External data methods (`backend/api/routes/external_data_methods.py`)
- `/api/external-assertions` - External assertions (`backend/api/routes/external_assertions.py`)

**Frontend API Client:**
- HTTP client: `frontend/src/api/client.ts` - Fetch-based with retry (3 attempts, exponential backoff)
- Domain clients: `frontend/src/api/tasks.ts`, `runs.ts`, `reports.ts`, `dashboard.ts`, `batches.ts`, etc.
- Error handling: `ApiError` class with toast notifications via sonner

---

*Integration audit: 2026-05-02*
