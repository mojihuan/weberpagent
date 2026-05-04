# Technology Stack

**Analysis Date:** 2026-05-02

## Languages

**Primary:**
- Python 3.11+ (requires `>=3.11`, tested with 3.14.3) - Backend API, AI agent orchestration, browser automation, test code generation
- TypeScript ~5.9.3 - Frontend SPA, E2E test configuration

**Secondary:**
- YAML - LLM model configuration (`backend/config/llm_config.yaml`), test target configuration (`backend/config/test_targets.yaml`)
- Jinja2 templates - Variable substitution in test flow descriptions (`backend/core/test_flow_service.py`)
- HTML/CSS (Tailwind CSS v4) - Frontend styling

## Runtime

**Environment:**
- Python 3.14.3 (development machine)
- Node.js v22.22.0 (development machine)
- Python `>=3.11` required (project constraint in `pyproject.toml`)

**Package Manager:**
- uv 0.9.24 - Python dependency management (lockfile: `uv.lock`)
- npm 10.9.4 - Node.js dependency management (lockfiles: `package-lock.json` in root and `frontend/`)

## Frameworks

**Core - Backend:**
- FastAPI >=0.135.1 - REST API framework (`backend/api/main.py`)
- Uvicorn >=0.34.0 - ASGI server with standard extras
- SQLAlchemy >=2.0.0 - Async ORM for database operations
- aiosqlite >=0.20.0 - Async SQLite driver
- Pydantic >=2.4.0 + pydantic-settings >=2.0.0 - Data validation and settings management

**Core - Frontend:**
- React 19.2.0 - UI framework
- React Router DOM 7.13.1 - Client-side routing
- TanStack React Query 5.90.21 - Server state management
- Vite 7.3.1 - Build tool and dev server

**Core - AI/Browser:**
- browser-use >=0.12.2 - Browser automation framework (wraps Playwright)
- Playwright >=1.40.0 - Browser automation (Python)
- langchain-openai >=0.3.0 + langchain-core >=0.3.0 - LLM integration via OpenAI-compatible API
- dashscope >=1.20.0 - Alibaba Cloud DashScope SDK (Qwen models)

**Testing:**
- pytest >=8.0.0 + pytest-asyncio >=0.24.0 - Python unit/integration testing
- pytest-playwright >=0.7.0 - Python Playwright test fixtures
- @playwright/test 1.51.1 - E2E testing framework (Node.js, configured in `e2e/playwright.config.ts`)
- pytest-timeout >=2.4.0 - Test timeout enforcement
- pytest-html >=4.0.0 - HTML test reports

**Build/Dev:**
- Vite 7.3.1 - Frontend build with `@vitejs/plugin-react` and `@tailwindcss/vite` plugins
- Tailwind CSS 4.2.1 via `@tailwindcss/vite` plugin - Utility-first CSS (imported as `@import "tailwindcss"` in `frontend/src/index.css`)
- ruff >=0.4.0 - Python linter (configured in `pyproject.toml`: line-length=100, target=py311)
- ESLint 9.39.1 + typescript-eslint 8.48.0 - Frontend linting (`frontend/eslint.config.js`)
- TypeScript ~5.9.3 - Strict mode enabled (`strict: true` in `frontend/tsconfig.app.json`)

## Key Dependencies

**Critical:**
- `browser-use>=0.12.2` - Core browser automation engine; provides `Agent`, `BrowserSession`, `BrowserProfile` classes used in `backend/core/agent_service.py`
- `langchain-openai>=0.3.0` - LLM abstraction layer; `ChatOpenAI` used in `backend/llm/openai.py` for model communication
- `fastapi>=0.135.1` - API framework; all routes defined under `backend/api/routes/`
- `sqlalchemy>=2.0.0` - Async ORM; models in `backend/db/models.py`, database config in `backend/db/database.py`
- `pydantic>=2.4.0` - Schema validation; settings in `backend/config/settings.py`, API schemas in `backend/api/schemas/`

**Infrastructure:**
- `httpx>=0.28.1` - Async HTTP client used for ERP authentication (`backend/core/auth_service.py`) and API calls
- `tenacity>=8.0.0` - Retry logic for LLM calls with exponential backoff (`backend/llm/factory.py`)
- `jinja2>=3.1.6` - Template-based variable substitution in test flow descriptions (`backend/core/test_flow_service.py`)
- `openpyxl>=3.1.5` - Excel file parsing for test case import (`backend/utils/excel_parser.py`)
- `nest_asyncio>=1.5.0` - Event loop compatibility for sync/async interop (`backend/core/precondition_service.py`)
- `pyyaml>=6.0` - YAML config parsing for LLM configuration (`backend/llm/config.py`)
- `python-dotenv>=1.0.0` - `.env` file loading in settings

**Frontend Libraries:**
- `sonner@2.0.7` - Toast notification library for React
- `recharts@3.8.0` - Chart library for dashboard visualizations
- `lucide-react@0.577.0` - Icon library
- `react-syntax-highlighter@16.1.1` - Code display in report/test views

## Configuration

**Environment:**
- Pydantic BaseSettings (`backend/config/settings.py`) loads from `.env` file at project root
- Environment variable names are case-insensitive
- `.env.example` documents all required/optional variables
- Frontend uses Vite env vars (`VITE_API_BASE`, `VITE_API_PROXY_TARGET`)

**Key Configuration Files:**
- `.env` - Secrets and environment config (gitignored, `.env.example` is committed)
- `pyproject.toml` - Python project metadata, dependencies, ruff config, mypy config
- `frontend/package.json` - Frontend dependencies and scripts
- `frontend/vite.config.ts` - Vite build config with dev proxy to backend (`/api` -> `http://localhost:11002`)
- `frontend/tsconfig.app.json` - TypeScript strict mode config (ES2022 target, `verbatimModuleSyntax`)
- `backend/config/test_targets.yaml` - Test target URLs and login credentials
- `backend/config/settings.py` - Centralized settings with Pydantic BaseSettings
- `backend/config/validators.py` - Configuration validation (WEBSERP_PATH checks)
- `backend/llm/config.py` - LLM model configuration loader with env var substitution

**Build:**
- Frontend: `tsc -b && vite build` (TypeScript check then Vite build)
- Dev proxy: Vite proxies `/api` requests to `http://localhost:11002` (configurable via `VITE_API_PROXY_TARGET`)
- Backend: `uv run uvicorn backend.api.main:app --port 11002`
- Backend (Windows): `uv run python backend/run_server.py` (handles ProactorEventLoop)

## Platform Requirements

**Development:**
- Python >=3.11 (tested with 3.14.3)
- Node.js v22+ (tested with v22.22.0)
- uv package manager
- npm package manager
- Playwright browsers (`playwright install`)
- Windows support: `backend/run_server.py` handles Windows ProactorEventLoop for browser-use subprocess compatibility

**Production:**
- Linux server (deployed to 121.40.191.49)
- Nginx serves frontend static build from `/var/www/aidriveuitest/`
- Backend runs as uvicorn process on port 8080 behind Nginx reverse proxy
- Deployment managed via `deploy.sh` script at project root (supports `--backend-only`, `--frontend-only`, `--skip-build`, `--stop`)
- SQLite database at `backend/data/database.db` (with WAL-compatible busy_timeout=30s)
- Headless Chrome with `--no-sandbox`, `--disable-setuid-sandbox`, `--disable-dev-shm-usage`, `--disable-gpu`, `--disable-software-rasterizer` flags
- Viewport: 1920x1080

---

*Stack analysis: 2026-05-02*
