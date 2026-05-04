# Codebase Structure

**Analysis Date:** 2026-05-02

## Directory Layout

```
weberpagent/                         # Project root
├── backend/                         # Python FastAPI backend
│   ├── api/                         # HTTP API layer
│   │   ├── main.py                  # FastAPI app entry, middleware, exception handlers
│   │   ├── helpers.py               # Shared route helpers (_build_task_dict, raise_not_found)
│   │   ├── response.py              # Standard API response format (ApiResponse, error_response)
│   │   ├── schemas/                 # API-level Pydantic schemas (currently __init__.py only)
│   │   └── routes/                  # Route handlers per domain
│   │       ├── tasks.py             # Task CRUD + Excel import/preview/confirm
│   │       ├── runs.py              # Re-exports from runs_routes + run_pipeline
│   │       ├── runs_routes.py       # Run HTTP endpoints (start, stream, stop, code)
│   │       ├── run_pipeline.py      # Run execution orchestration (background pipeline)
│   │       ├── reports.py           # Report listing + detail + timeline
│   │       ├── dashboard.py         # Dashboard statistics
│   │       ├── batches.py           # Batch execution CRUD + start
│   │       ├── external_operations.py   # External precondition operations discovery
│   │       ├── external_data_methods.py # External data method discovery + execution
│   │       └── external_assertions.py   # External assertion method discovery + execution
│   ├── agent/                       # AI browser automation layer
│   │   ├── __init__.py              # Re-exports MonitoredAgent, detectors, prompts
│   │   ├── monitored_agent.py       # Agent subclass with stall/submit/progress hooks
│   │   ├── stall_detector.py        # Detects agent stall (consecutive failures, stagnant DOM)
│   │   ├── pre_submit_guard.py      # Blocks premature submit clicks
│   │   ├── task_progress_tracker.py # Warns when step budget is tight
│   │   ├── action_utils.py          # Action extraction from browser-use responses
│   │   ├── dom_patch.py             # Monkey-patches browser-use DOM for ax_name enrichment
│   │   └── prompts.py               # System prompts (ENHANCED_SYSTEM_MESSAGE, LOGIN_TASK_PROMPT)
│   ├── core/                        # Business logic services
│   │   ├── agent_service.py         # Agent execution: browser session, step callback, screenshots
│   │   ├── code_generator.py        # Assembles Playwright test file from translated actions
│   │   ├── action_translator.py     # Translates browser-use actions to Playwright code
│   │   ├── step_code_buffer.py      # Accumulates translated steps during execution
│   │   ├── locator_chain_builder.py # Generates multi-strategy Playwright locators from DOM
│   │   ├── precondition_service.py  # Precondition execution with Jinja2 variable substitution
│   │   ├── assertion_service.py     # UI assertion evaluation (url_contains, text_exists, no_errors)
│   │   ├── report_service.py        # Report generation with timeline (steps + preconditions + assertions)
│   │   ├── test_flow_service.py     # Login prefix injection + two-phase variable substitution
│   │   ├── batch_execution.py       # Semaphore-gated parallel batch execution
│   │   ├── event_manager.py         # SSE pub/sub singleton with heartbeat
│   │   ├── account_service.py       # Role name -> ERP credential resolution
│   │   ├── auth_service.py          # HTTP-based ERP token acquisition
│   │   ├── cache_service.py         # Run-scoped in-memory cache with deep-copy immutability
│   │   ├── error_utils.py           # non_blocking_execute, silent_execute helpers
│   │   ├── random_generators.py     # Test data generators (IMEI, phone, waybill, serial)
│   │   ├── time_utils.py            # Time formatting utilities
│   │   ├── external_module_loader.py        # Lazy loading of external webseleniumerp modules
│   │   ├── external_method_discovery.py     # Docstring-based method discovery from external project
│   │   ├── external_execution_engine.py     # Execute external assertions, data methods, operations
│   │   └── external_precondition_bridge.py   # Backward-compatible facade re-exporting above three
│   ├── llm/                         # LLM integration layer
│   │   ├── base.py                  # BaseLLM abstract class, ActionResult, LLMResponse
│   │   ├── factory.py               # LLMFactory + create_llm() with retry
│   │   ├── config.py                # YAML-based LLM model configuration
│   │   ├── openai.py                # OpenAI-compatible implementation (DashScope)
│   │   └── utils.py                 # LLM utility functions
│   ├── db/                          # Database layer
│   │   ├── __init__.py              # Re-exports models, schemas, repositories
│   │   ├── database.py              # Async engine, session factory, init_db() with migrations
│   │   ├── models.py                # SQLAlchemy ORM models (Task, Run, Step, Batch, Assertion, etc.)
│   │   ├── repository.py            # Repository classes for each model
│   │   └── schemas.py               # Pydantic request/response schemas
│   ├── config/                      # Configuration
│   │   ├── __init__.py              # Re-exports Settings, get_settings
│   │   ├── settings.py              # Pydantic BaseSettings from .env
│   │   ├── validators.py            # Path and config validators
│   │   └── test_targets.yaml        # Test target URL configuration
│   ├── utils/                       # Utilities
│   │   ├── logger.py                # StructuredLogger (JSONL output)
│   │   ├── run_logger.py            # Per-run execution logger
│   │   ├── screenshot.py            # Screenshot capture utilities
│   │   ├── excel_parser.py          # Parse test case Excel files
│   │   └── excel_template.py        # Generate test case Excel template
│   ├── data/                        # Runtime data (database, screenshots, test files)
│   │   ├── database.db              # SQLite database
│   │   ├── screenshots/             # Step screenshots
│   │   └── test-files/              # Uploadable test attachments
│   └── run_server.py                # Server startup script (uvicorn on port 11002)
├── frontend/                        # React + Vite + TypeScript frontend
│   ├── src/
│   │   ├── main.tsx                 # React root with QueryClientProvider + Toaster
│   │   ├── App.tsx                  # Router definition (8 routes)
│   │   ├── index.css                # Tailwind CSS entry
│   │   ├── assets/                  # Static assets
│   │   ├── pages/                   # Page-level components
│   │   │   ├── Dashboard.tsx        # / - Statistics overview
│   │   │   ├── Tasks.tsx            # /tasks - Task list with CRUD
│   │   │   ├── TaskDetail.tsx       # /tasks/:id - Task detail + edit
│   │   │   ├── RunList.tsx          # /runs - Execution history
│   │   │   ├── RunMonitor.tsx       # /runs/:id - Live execution monitoring
│   │   │   ├── BatchProgress.tsx    # /batches/:id - Batch execution progress
│   │   │   ├── Reports.tsx          # /reports - Report list
│   │   │   └── ReportDetail.tsx     # /reports/:id - Report detail with timeline
│   │   ├── components/              # Reusable UI components
│   │   │   ├── Layout.tsx           # Page layout wrapper
│   │   │   ├── Sidebar.tsx          # Navigation sidebar
│   │   │   ├── NavItem.tsx          # Navigation item
│   │   │   ├── Button.tsx           # Button component
│   │   │   ├── BatchProgress/       # Batch execution progress components
│   │   │   ├── Dashboard/           # Dashboard stat components
│   │   │   ├── ImportModal/         # Excel import modal
│   │   │   ├── Report/              # Report rendering components
│   │   │   ├── RunMonitor/          # Run monitoring components
│   │   │   ├── TaskDetail/          # Task detail form components
│   │   │   ├── TaskList/            # Task list item components
│   │   │   ├── TaskModal/           # Task create/edit modal components
│   │   │   └── shared/              # Shared UI components (StatusBadge, etc.)
│   │   ├── api/                     # Backend API client modules
│   │   │   ├── client.ts            # HTTP client with retry + error toast
│   │   │   ├── tasks.ts             # Task API calls
│   │   │   ├── runs.ts              # Run API calls
│   │   │   ├── reports.ts           # Report API calls
│   │   │   ├── batches.ts           # Batch API calls
│   │   │   ├── dashboard.ts         # Dashboard API calls
│   │   │   ├── externalOperations.ts       # External operations API
│   │   │   ├── externalDataMethods.ts      # External data methods API
│   │   │   └── externalAssertions.ts       # External assertions API
│   │   ├── hooks/                   # Custom React hooks
│   │   │   ├── useRunStream.ts      # SSE real-time run monitoring
│   │   │   ├── useTasks.ts          # Task CRUD hooks
│   │   │   ├── useReports.ts        # Report hooks
│   │   │   ├── useDashboard.ts      # Dashboard stats hooks
│   │   │   └── useBatchProgress.ts  # Batch progress hooks
│   │   ├── types/
│   │   │   └── index.ts             # All TypeScript interfaces and types (457 lines)
│   │   ├── constants/
│   │   │   └── roleLabels.ts        # Role display name mapping
│   │   └── utils/
│   │       ├── reasoningParser.ts   # Parse reasoning text from AI
│   │       └── retry.ts             # Retry utilities with exponential backoff
│   ├── index.html                   # HTML entry
│   ├── vite.config.ts               # Vite config (port 11001, API proxy)
│   ├── eslint.config.js             # ESLint configuration
│   ├── tsconfig.json                # TypeScript config
│   ├── tsconfig.app.json            # TypeScript app config
│   ├── tsconfig.node.json           # TypeScript node config
│   └── package.json                 # Node dependencies
├── e2e/                             # Playwright E2E tests
│   ├── playwright.config.ts         # Playwright config
│   └── tests/                       # E2E test specs
│       ├── smoke.spec.ts            # Basic smoke test
│       ├── task-flow.spec.ts        # Task CRUD flow
│       ├── full-flow.spec.ts        # Complete end-to-end flow
│       ├── assertion-flow.spec.ts   # Assertion execution flow
│       ├── data-method-execution.spec.ts    # Data method execution
│       ├── data-method-selector.spec.ts     # Data method selector UI
│       └── variable-substitution.spec.ts    # Variable substitution
├── outputs/                         # Per-run execution artifacts (gitignored)
│   └── {run_id}/
│       ├── test_{task_id}.py        # Generated Playwright test file
│       ├── logs/run.jsonl           # Structured execution logs
│       ├── dom/step_N.txt           # DOM snapshots per step
│       └── screenshots/step_N.png   # Screenshots per step
├── data/                            # Shared runtime data
│   ├── screenshots/                 # Legacy screenshot storage
│   └── test-files/                  # Files available for test upload
├── docs/                            # Documentation
│   ├── plans/                       # Implementation plans
│   ├── test-steps/                  # Test step documentation
│   └── troubleshooting/             # Troubleshooting guides
├── _backup/                         # Archived code and runtime data
├── _documents/                      # Project documents
├── .planning/                       # GSD planning documents
│   └── codebase/                    # Codebase analysis documents (this dir)
├── pyproject.toml                   # Python project config (dependencies, ruff, mypy)
├── deploy.sh                        # Deployment script to remote server
├── .env.example                     # Environment variable template
├── CLAUDE.md                        # AI coding guidelines
└── README.md                        # Project documentation
```

## Directory Purposes

### `backend/api/`
- Purpose: HTTP API layer -- route handlers, request/response processing, SSE streaming
- Contains: FastAPI routers organized by domain entity, shared helpers, standard response format
- Key files: `main.py` (app init + middleware), `routes/run_pipeline.py` (execution orchestration), `routes/runs_routes.py` (run endpoints)

### `backend/agent/`
- Purpose: AI browser automation layer -- extends browser-use Agent with monitoring capabilities
- Contains: MonitoredAgent subclass, three detectors (stall, submit guard, progress), DOM patches, system prompts
- Key files: `monitored_agent.py`, `dom_patch.py`, `stall_detector.py`

### `backend/core/`
- Purpose: Business logic services -- orchestrates execution pipeline, code generation, assertions
- Contains: 23 service files covering agent execution, code generation, preconditions, assertions, reporting, external integration
- Key files: `agent_service.py`, `code_generator.py`, `action_translator.py`, `step_code_buffer.py`, `external_precondition_bridge.py`

### `backend/llm/`
- Purpose: LLM provider abstraction -- unified interface for AI model access
- Contains: Abstract base class, factory with caching, configuration loader, OpenAI implementation
- Key files: `factory.py` (create_llm with retry), `base.py` (BaseLLM interface)

### `backend/db/`
- Purpose: Data persistence layer -- ORM models, repositories, schemas
- Contains: SQLAlchemy models (7 tables), Pydantic schemas (request/response DTOs), repository classes with async operations
- Key files: `models.py`, `repository.py`, `schemas.py`, `database.py`

### `backend/config/`
- Purpose: Centralized configuration management
- Contains: Pydantic BaseSettings singleton, YAML config, validators
- Key files: `settings.py`

### `backend/utils/`
- Purpose: Cross-cutting utilities for logging, screenshots, Excel I/O
- Contains: Structured logger, run logger, screenshot manager, Excel parser, template generator
- Key files: `excel_parser.py`, `run_logger.py`

### `backend/data/`
- Purpose: Runtime data storage (database, screenshots, test files)
- Contains: SQLite database file, step screenshots, uploadable test files
- Generated: Yes (automatic)

### `frontend/src/pages/`
- Purpose: Top-level page components mapped to routes
- Contains: 8 page components for dashboard, tasks, runs, batches, reports
- Key files: `Tasks.tsx`, `RunMonitor.tsx`, `ReportDetail.tsx`

### `frontend/src/components/`
- Purpose: Reusable UI components organized by feature
- Contains: Layout, sidebar, navigation, plus feature-specific component subdirectories
- Subdirectories: `BatchProgress/`, `Dashboard/`, `ImportModal/`, `Report/`, `RunMonitor/`, `TaskDetail/`, `TaskList/`, `TaskModal/`, `shared/`

### `frontend/src/api/`
- Purpose: Backend API client modules
- Contains: HTTP client wrapper with retry logic, one file per API domain
- Key files: `client.ts` (fetch wrapper + error handling), `tasks.ts`, `runs.ts`

### `frontend/src/hooks/`
- Purpose: Custom React hooks for data fetching and SSE
- Contains: React Query hooks and SSE streaming hook
- Key files: `useRunStream.ts` (SSE connection with EventSource)

### `frontend/src/types/`
- Purpose: Shared TypeScript type definitions
- Contains: All interfaces for API data types, SSE events, UI models
- Key files: `index.ts` (single barrel file with all types)

### `outputs/`
- Purpose: Per-run execution artifacts
- Contains: Generated Playwright test files, JSONL logs, DOM snapshots, screenshots
- Generated: Yes (during test execution)
- Committed: No (gitignored)

### `e2e/`
- Purpose: End-to-end Playwright tests for the platform UI itself
- Contains: 7 test spec files covering smoke, task flow, full flow, assertions, data methods, variables

### `docs/`
- Purpose: Project documentation and implementation plans
- Contains: Plans, test step docs, troubleshooting guides, Excel templates

## Key File Locations

### Entry Points
- `backend/run_server.py`: Server startup script (uvicorn on port 11002)
- `backend/api/main.py`: FastAPI app definition, middleware, route registration
- `frontend/src/main.tsx`: React root with providers
- `frontend/src/App.tsx`: Route definitions

### Configuration
- `backend/config/settings.py`: Pydantic BaseSettings (LLM, ERP, database URLs)
- `backend/config/test_targets.yaml`: Test target URL configuration
- `.env.example`: Required environment variables template
- `frontend/vite.config.ts`: Vite dev server + API proxy config
- `pyproject.toml`: Python dependencies, ruff, mypy config

### Core Logic (Execution Pipeline)
- `backend/api/routes/run_pipeline.py`: Full execution orchestration (preconditions -> agent -> assertions -> report -> code)
- `backend/core/agent_service.py`: Browser session creation, MonitoredAgent setup, step callback wiring
- `backend/core/step_code_buffer.py`: Step-by-step code translation during execution

### Core Logic (Code Generation)
- `backend/core/code_generator.py`: Playwright test file assembly
- `backend/core/action_translator.py`: Action-to-Playwright translation (10 core types)
- `backend/core/locator_chain_builder.py`: Multi-strategy locator generation

### Core Logic (External Integration)
- `backend/core/external_module_loader.py`: Lazy loading of external project
- `backend/core/external_method_discovery.py`: Docstring-based method discovery
- `backend/core/external_execution_engine.py`: External assertion/data method execution

### Data Models
- `backend/db/models.py`: ORM models (Task, Run, Step, Batch, Assertion, AssertionResult, PreconditionResult, Report)
- `backend/db/repository.py`: Repository classes for all models
- `backend/db/schemas.py`: Pydantic request/response DTOs
- `backend/db/database.py`: Engine, session factory, init_db() with schema migrations

### Frontend Data Layer
- `frontend/src/types/index.ts`: All TypeScript interfaces (Task, Run, Step, SSE events, assertions, batches)
- `frontend/src/api/client.ts`: HTTP client with retry and error toast
- `frontend/src/hooks/useRunStream.ts`: SSE connection with real-time state updates

## Naming Conventions

### Python Files
- Pattern: `snake_case.py`
- Examples: `agent_service.py`, `run_pipeline.py`, `external_precondition_bridge.py`
- Service files: `{domain}_service.py` (e.g., `assertion_service.py`, `report_service.py`)
- Utility files: descriptive noun (e.g., `excel_parser.py`, `logger.py`, `screenshot.py`)

### TypeScript/React Files
- Pattern: `PascalCase.tsx` for components, `camelCase.ts` for utilities
- Page components: `PascalCase.tsx` matching route name (e.g., `Dashboard.tsx`, `RunMonitor.tsx`)
- Hook files: `use{Feature}.ts` (e.g., `useRunStream.ts`, `useTasks.ts`)
- API files: `{domain}.ts` (e.g., `tasks.ts`, `runs.ts`)
- Type files: `index.ts` barrel file in `types/`

### Directories
- Pattern: `PascalCase` for frontend component groups, `snake_case` for backend packages
- Frontend component groups: `TaskDetail/`, `RunMonitor/`, `ImportModal/`
- Backend packages: `api/`, `core/`, `agent/`, `llm/`, `db/`, `config/`, `utils/`

### Functions and Classes
- Python classes: `PascalCase` (e.g., `MonitoredAgent`, `AgentService`, `CacheService`)
- Python functions: `snake_case` (e.g., `create_llm()`, `run_agent_background()`, `non_blocking_execute()`)
- Python constants: `SCREAMING_SNAKE_CASE` (e.g., `SERVER_BROWSER_ARGS`, `MAX_CONCURRENCY`)
- React components: `PascalCase` function components (e.g., `Dashboard`, `RunMonitor`)

## Where to Add New Code

### New API Endpoint
1. Create route file: `backend/api/routes/{domain}.py`
2. Register in `backend/api/main.py` (add `app.include_router({domain}.router, prefix="/api")`)
3. Add request/response schemas: `backend/db/schemas.py`
4. Add repository methods (if needed): `backend/db/repository.py`
5. Add service logic: `backend/core/{domain}_service.py`

### New Agent Detector
1. Create detector: `backend/agent/{detector_name}.py`
2. Wire into `backend/agent/monitored_agent.py` (`__init__` parameter + `_prepare_context` / `_execute_actions` hooks)
3. Re-export from `backend/agent/__init__.py`

### New Database Model
1. Add model class: `backend/db/models.py`
2. Add migration in `backend/db/database.py` `init_db()` function (`ALTER TABLE ADD COLUMN`)
3. Add Pydantic schemas: `backend/db/schemas.py`
4. Add repository class: `backend/db/repository.py`
5. Re-export from `backend/db/__init__.py`

### New Frontend Page
1. Create page component: `frontend/src/pages/{PageName}.tsx`
2. Add route in `frontend/src/App.tsx`
3. Add navigation item in `frontend/src/components/Sidebar.tsx`
4. Add API client: `frontend/src/api/{domain}.ts`
5. Add React Query hook: `frontend/src/hooks/use{Feature}.ts`
6. Add TypeScript types: `frontend/src/types/index.ts`

### New Frontend Component
1. Create in feature directory: `frontend/src/components/{Feature}/{ComponentName}.tsx`
2. If shared across features: `frontend/src/components/shared/{ComponentName}.tsx`

### New Core Service
1. Create service: `backend/core/{service_name}_service.py`
2. Import and use from route handler or `run_pipeline.py`
3. If service needs external module access, use `external_precondition_bridge.py` facade

### New Code Translation Action Type
1. Add action type to `_CORE_TYPES` set in `backend/core/action_translator.py`
2. Add translation method in `ActionTranslator` class
3. Update `PlaywrightCodeGenerator` if new action needs special handling

## Special Directories

### `outputs/`
- Purpose: Per-run execution artifacts (generated code, logs, DOM snapshots, screenshots)
- Structure: `outputs/{run_id}/` with subdirectories `logs/`, `dom/`, `screenshots/`
- Generated: Yes (created during test execution)
- Committed: No (gitignored)
- Key output: `outputs/{run_id}/test_{task_id}.py` (generated Playwright test)

### `backend/data/`
- Purpose: Persistent runtime data
- Contains: SQLite database (`database.db`), step screenshots, uploadable test files
- Generated: Yes (automatic)
- Committed: `database.db` is committed for development continuity

### `_backup/`
- Purpose: Archived code and runtime data from previous iterations
- Contains: Archived backend implementations, old test cases, old runtime data
- Committed: Yes (historical reference)

### `docs/plans/`
- Purpose: Implementation phase plans (numbered phases)
- Contains: Planning documents for each development phase
- Committed: Yes

### `docs/test-steps/`
- Purpose: Test step documentation for manual testing
- Contains: Step-by-step test case documentation
- Committed: Yes

### `.planning/`
- Purpose: GSD (Get Stuff Done) planning framework documents
- Contains: Codebase analysis documents generated by `/gsd:map-codebase`
- Committed: Yes (part of project knowledge base)

---

*Structure analysis: 2026-05-02*
