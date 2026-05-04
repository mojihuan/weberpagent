# Architecture

**Analysis Date:** 2026-05-02

## Pattern Overview

**Overall:** Monolithic full-stack application with backend/frontend separation and AI-driven browser automation pipeline

**Key Characteristics:**
- Backend: FastAPI async REST API serving a React SPA
- AI-driven browser automation via browser-use library (Playwright under the hood)
- Server-Sent Events (SSE) for real-time execution streaming to frontend
- SQLite with async SQLAlchemy for persistence
- External project integration via dynamic module loading (webseleniumerp)
- Code generation pipeline: AI actions -> Playwright test code translation
- Multi-stage execution: preconditions -> agent run -> assertions -> code generation -> report

## Layers

### Frontend Layer (React SPA)
- Purpose: Single-page application for task management, execution monitoring, and report viewing
- Location: `frontend/src/`
- Contains: Pages, components, hooks, API client modules, TypeScript types
- Depends on: Backend REST API (`/api/*`), SSE stream for real-time updates
- Used by: End users (QA testers)
- Key files: `frontend/src/App.tsx` (routing), `frontend/src/hooks/useRunStream.ts` (SSE), `frontend/src/api/client.ts` (HTTP)

### API Layer (FastAPI)
- Purpose: HTTP endpoints, request validation, response formatting, SSE streaming
- Location: `backend/api/`
- Contains: Route handlers (`routes/`), shared helpers, response format module, Pydantic schemas
- Depends on: Core services, database repositories, event manager
- Used by: Frontend via REST calls and SSE connections
- Key files: `backend/api/main.py` (app + middleware), `backend/api/routes/runs_routes.py` (run endpoints), `backend/api/routes/run_pipeline.py` (execution orchestration)

### Core Services Layer
- Purpose: Business logic orchestration for test execution, code generation, assertions, preconditions
- Location: `backend/core/`
- Contains: Service classes for agent execution, code generation, preconditions, assertions, reporting, batch execution
- Depends on: Database repositories, LLM factory, agent module, external modules
- Used by: API route handlers and pipeline functions
- Key files: `backend/core/agent_service.py`, `backend/core/code_generator.py`, `backend/core/action_translator.py`, `backend/core/step_code_buffer.py`

### Agent Layer (AI Automation)
- Purpose: Browser automation agent with monitoring, stall detection, submit guarding, and progress tracking
- Location: `backend/agent/`
- Contains: MonitoredAgent subclass, DOM patching, stall detector, pre-submit guard, task progress tracker, prompts
- Depends on: browser-use library, LLM (via langchain)
- Used by: `backend/core/agent_service.py`
- Key files: `backend/agent/monitored_agent.py`, `backend/agent/dom_patch.py`, `backend/agent/stall_detector.py`

### Data Access Layer
- Purpose: ORM models, database operations, data schemas
- Location: `backend/db/`
- Contains: SQLAlchemy models, Pydantic schemas, repository classes with async session management
- Depends on: SQLAlchemy, aiosqlite
- Used by: Core services, API routes
- Key files: `backend/db/models.py`, `backend/db/repository.py`, `backend/db/schemas.py`

### LLM Abstraction Layer
- Purpose: LLM provider abstraction, instance management, and retry logic
- Location: `backend/llm/`
- Contains: Base LLM interface, factory with caching, YAML config loader, OpenAI/DashScope adapter
- Depends on: langchain-openai, browser-use ChatOpenAI, tenacity
- Used by: Agent service, code generation services
- Key files: `backend/llm/factory.py`, `backend/llm/base.py`, `backend/llm/config.py`

### External Integration Layer
- Purpose: Dynamic loading and execution of external webseleniumerp project modules
- Location: Split across three files in `backend/core/`
  - `backend/core/external_module_loader.py` -- lazy module loading and path configuration
  - `backend/core/external_method_discovery.py` -- docstring parsing for method discovery
  - `backend/core/external_execution_engine.py` -- execution of assertions, data methods, operations
- Depends on: External project at configurable path (`WEBSERP_PATH`)
- Used by: Precondition service, assertion routes, data method routes
- Backward-compatible facade: `backend/core/external_precondition_bridge.py` re-exports from all three

### Configuration Layer
- Purpose: Centralized settings management
- Location: `backend/config/`
- Contains: Pydantic BaseSettings singleton, YAML test targets, path validators
- Depends on: pydantic-settings, python-dotenv
- Used by: All backend modules
- Key files: `backend/config/settings.py`

### Utility Layer
- Purpose: Cross-cutting utilities for logging, screenshots, Excel I/O
- Location: `backend/utils/`
- Contains: Structured logger, run logger, screenshot manager, Excel parser, Excel template generator
- Key files: `backend/utils/run_logger.py`, `backend/utils/excel_parser.py`, `backend/utils/excel_template.py`

## Data Flow

### Test Execution Flow (Primary)

```
Frontend: User clicks "Run"
       |
       v
POST /api/runs  (runs_routes.py)
       |
       v
run_agent_background()  (run_pipeline.py)
       |
       +--> Run preconditions  (precondition_service.py)
       |         |
       |         +--> Execute Python code snippets
       |         +--> Call external data methods (optional)
       |         +--> Store variables in ContextWrapper
       |         |
       +--> Inject login steps  (test_flow_service.py)
       |         |
       +--> Create browser session  (agent_service.py)
       |         |
       +--> Run MonitoredAgent  (agent_service.py)
       |         |
       |         +--> Per step: StallDetector + PreSubmitGuard + TaskProgressTracker
       |         +--> Per step: Translate action -> Playwright code  (step_code_buffer.py)
       |         +--> Per step: Publish SSE event  (event_manager.py)
       |         |
       +--> Evaluate UI assertions  (assertion_service.py)
       |         |
       +--> Execute external assertions  (external_execution_engine.py)
       |         |
       +--> Generate report  (report_service.py)
       |         |
       +--> Assemble & save Playwright test file  (code_generator.py)
       |         |
       v
Frontend: SSE events received via useRunStream hook
```

### Code Generation Pipeline

```
browser-use agent step
       |
       v
DOMInteractedElement captured
       |
       v
LocatorChainBuilder.extract()  (locator_chain_builder.py)
  - Multi-strategy locators: get_by_role > get_by_text > CSS[placeholder] > CSS class > XPath
  - Max 3 locators per action
       |
       v
ActionTranslator.translate()  (action_translator.py)
  - 10 core types: click, input, navigate, scroll, send_keys, go_back,
    wait, evaluate, select_dropdown, upload_file
  - Generates Playwright API call strings with try-except fallback chains
       |
       v
StepCodeBuffer.append_step()  (step_code_buffer.py)
  - Accumulates StepRecord per step during execution
       |
       v
PlaywrightCodeGenerator.generate()  (code_generator.py)
  - Assembles: metadata header + imports + login code + test function body + assertions
  - Outputs complete pytest Playwright test file
       |
       v
Saved to outputs/{run_id}/test_{task_id}.py
```

### Batch Execution Flow

```
POST /api/batches  (batches.py)
       |
       v
BatchExecutionService.start()  (batch_execution.py)
       |
       +--> asyncio.Semaphore(concurrency) gates parallel execution
       +--> Each task -> run_agent_background() as asyncio.Task
       +--> Single failure does not affect other runs (D-10)
       +--> Max concurrency: 4 (hard cap per D-09)
       |
       v
Frontend: BatchProgress page polls status
```

### State Management

**Backend State:** SQLite database with async sessions (`backend/db/database.py`). Each request gets its own `AsyncSession` via `get_db()` FastAPI dependency. Repository pattern wraps all CRUD operations. Schema migrations handled via `ALTER TABLE ADD COLUMN` in `init_db()`.

**Frontend State:** React Query (`@tanstack/react-query`) for server state caching. Local state via React `useState`/`useRef`. SSE-driven real-time updates in `useRunStream` hook using `EventSource` API.

**Cache State:** `backend/core/cache_service.py` provides run-scoped in-memory cache with deep-copy immutability guarantees (both on store and retrieve).

**Event State:** `backend/core/event_manager.py` global singleton holds event history and subscriber queues per `run_id`. Supports history replay for late subscribers.

## Key Abstractions

### Repository Pattern
- Purpose: Encapsulate all database CRUD operations behind typed async interfaces
- Examples: `backend/db/repository.py`
- Pattern: `BaseRepository(session)` with `_persist()` helper. Specialized subclasses: `TaskRepository`, `RunRepository`, `StepRepository`, `BatchRepository`, `AssertionResultRepository`, `PreconditionResultRepository`, `ReportRepository`
- Usage: Instantiated in route handlers via `Depends(get_task_repo)` pattern

### Service Pattern
- Purpose: Business logic orchestration separate from HTTP handling and data access
- Examples: `backend/core/agent_service.py`, `backend/core/report_service.py`, `backend/core/assertion_service.py`, `backend/core/precondition_service.py`
- Pattern: Services compose repositories and other services; routes never access the database directly

### Event Manager (Pub/Sub)
- Purpose: Decouple agent execution from SSE streaming to frontend
- Location: `backend/core/event_manager.py`
- Pattern: Global singleton with `publish(run_id, event)` / `subscribe(run_id)` async generator. Supports history replay and heartbeat (20s interval).

### LLM Factory
- Purpose: Abstract LLM provider selection and instance caching
- Location: `backend/llm/factory.py`
- Pattern: Class-level factory with `create(module_path)` and model-based caching. `create_llm()` at module level returns browser-use-compatible `ChatOpenAI` with tenacity retry (3 attempts, exponential backoff).

### MonitoredAgent (Decorator Pattern)
- Purpose: Extend browser-use Agent with stall detection, submit guarding, and progress tracking
- Location: `backend/agent/monitored_agent.py`
- Pattern: Subclass of `browser_use.Agent`. Overrides `_prepare_context()` to inject intervention messages and `_execute_actions()` to block premature submit clicks. Detector calls wrapped in try/except for fault tolerance.

### Code Generation Pipeline (Translator Pattern)
- Purpose: Convert browser-use actions into standalone Playwright test code
- Components:
  - `backend/core/locator_chain_builder.py` -- DOM element to Playwright locator strings
  - `backend/core/action_translator.py` -- action dicts to Playwright API calls
  - `backend/core/step_code_buffer.py` -- step-by-step accumulation during execution
  - `backend/core/code_generator.py` -- final test file assembly with imports, login, assertions
- Pattern: Immutable data classes (`TranslatedAction`, `StepRecord`) flow through pipeline stages

### External Integration (Facade Pattern)
- Purpose: Bridge to external webseleniumerp project for preconditions, data methods, and assertions
- Location: `backend/core/external_precondition_bridge.py` (facade), `external_module_loader.py` (loading), `external_method_discovery.py` (discovery), `external_execution_engine.py` (execution)
- Pattern: Lazy loading with module-level caching. Method discovery via docstring parsing. Backward-compatible re-exports from facade module.

## Entry Points

### Backend Server
- Location: `backend/run_server.py` (startup script) -> `backend/api/main.py:app` (ASGI app)
- Triggers: `uv run python backend/run_server.py` or `uvicorn backend.api.main:app`
- Responsibilities: Starts uvicorn on port 11002, initializes database tables, validates config, registers all routes

### Frontend Dev Server
- Location: `frontend/vite.config.ts`
- Triggers: `npm run dev` in `frontend/` directory
- Responsibilities: Vite dev server on port 11001, proxies `/api` to backend at `localhost:11002`

### Production Deployment
- Location: `deploy.sh` at project root
- Responsibilities: Deploys to remote server at `121.40.191.49:/root/project/weberpagent/`

## Error Handling

**Strategy:** Layered error handling with consistent API response format and graceful degradation

**Patterns:**
- **Global exception handlers** in `backend/api/main.py`: Catches `HTTPException`, `RequestValidationError`, and generic `Exception`. All return `{"success": false, "error": {"code", "message", "request_id"}}` format.
- **Response helpers** in `backend/api/response.py`: `success_response()` and `error_response()` with `ErrorCodes` constants.
- **Non-blocking execution** in `backend/core/error_utils.py`: `non_blocking_execute()` for optional operations (never raises), `scan_with_fallback()` for graceful degradation, `silent_execute()` for cleanup.
- **LLM retry** in `backend/llm/factory.py`: tenacity retry with exponential backoff (1s, 2s, 4s). Distinguishes retryable (timeout, 429, 503) from non-retryable (401, 403, quota) errors.
- **Agent fault tolerance** in `backend/agent/monitored_agent.py`: All detector calls wrapped in try/except (D-07/D-08). Detector failures never crash agent execution.

## Cross-Cutting Concerns

**Logging:** Python `logging` module throughout backend. `backend/utils/logger.py` provides JSONL structured logger. `backend/utils/run_logger.py` for per-run execution logs. DEBUG level enabled for browser-use and cdp_use loggers during server startup.

**Validation:** Pydantic v2 models for all request/response schemas (`backend/db/schemas.py`). Excel import validation in `backend/utils/excel_parser.py`. Configuration validation in `backend/config/validators.py` (validates `WEBSERP_PATH`). Request validation via FastAPI's `RequestValidationError` handler.

**Authentication:** No user-facing auth on the platform itself. ERP authentication handled by `backend/core/auth_service.py` (HTTP POST token fetch to `/auth/login`) and `backend/core/account_service.py` (role name to credential resolution via external `user_info.py`). Platform API is open (CORS allows `*`).

**Real-time Communication:** SSE via `EventManager` singleton. Frontend `EventSource` connects to `GET /api/runs/{run_id}/stream`. Events: `started`, `step`, `precondition`, `assertion`, `external_assertions`, `finished`, `error`. Heartbeat every 20 seconds to keep connections alive.

**Concurrency Control:** `asyncio.Semaphore` for batch execution concurrency (default 2, hard max 4) in `backend/core/batch_execution.py`. Module-level semaphore for code execution in `runs_routes.py`. `active_batches` dict prevents GC of running services.

---

*Architecture analysis: 2026-05-02*
