# Codebase Structure

**Analysis Date:** 2026-04-03

## Directory Layout

```
aiDriveUITest/
├── backend/
│   ├── api/
│   │   ├── main.py                 # FastAPI app entry point
│   │   └── routes/
│   │       ├── tasks.py            # Task CRUD endpoints
│   │       ├── runs.py             # Run execution + SSE streaming
│   │       ├── reports.py         # Report endpoints
│   │       ├── dashboard.py        # Dashboard stats
│   │       ├── external_operations.py
│   │       ├── external_data_methods.py
│   │       └── external_assertions.py
│   ├── agent/                      # Browser automation layer
│   │   ├── browser_agent.py        # UIBrowserAgent wrapper (legacy)
│   │   ├── proxy_agent.py          # ProxyBrowserAgent wrapper (legacy)
│   │   ├── monitored_agent.py      # MonitoredAgent (current implementation)
│   │   ├── stall_detector.py       # Stall detection
│   │   ├── pre_submit_guard.py     # Form validation guard
│   │   ├── task_progress_tracker.py # Step progress tracking
│   │   ├── dom_patch.py            # browser-use DOM monkey-patch
│   │   └── prompts.py              # System prompts (ENHANCED_SYSTEM_MESSAGE)
│   ├── core/                       # Business logic services
│   │   ├── agent_service.py        # Agent execution service (main entry)
│   │   ├── precondition_service.py # Precondition execution
│   │   ├── assertion_service.py    # UI assertion validation
│   │   ├── report_service.py        # Report generation
│   │   ├── event_manager.py        # SSE pub/sub
│   │   ├── external_precondition_bridge.py # External assertion execution
│   │   ├── precondition_service.py # Variable substitution (Jinja2)
│   │   └── random_generators.py    # Test data generators
│   ├── llm/                        # LLM integration
│   │   ├── factory.py              # LLM factory with caching
│   │   ├── base.py                 # BaseLLM abstract class
│   │   ├── config.py               # YAML config loader
│   │   ├── browser_use_adapter.py  # browser-use adapter
│   │   └── openai.py               # OpenAI implementation
│   ├── db/                         # Database layer
│   │   ├── database.py             # SQLAlchemy async setup
│   │   ├── models.py               # ORM models (Task, Run, Step, Report, Assertion)
│   │   ├── repository.py          # Data access objects
│   │   └── schemas.py             # Pydantic schemas
│   ├── config/                     # Configuration
│   │   ├── settings.py             # Pydantic settings from env
│   │   └── validators.py           # Config validators
│   ├── utils/                      # Utilities
│   │   ├── logger.py               # Structured logging
│   │   ├── run_logger.py           # Per-run JSONL logger
│   │   └── screenshot.py           # Screenshot utilities
│   ├── run_server.py               # Server entry point
│   └── _archived/                  # Archived code (legacy implementations)
├── frontend/                       # React + Vite frontend
│   └── src/
│       ├── components/             # React components
│       ├── pages/                  # Page components
│       ├── hooks/                  # Custom React hooks
│       ├── api/                    # API client
│       └── types/index.ts          # TypeScript interfaces
├── webseleniumerp/                # External Selenium project
│   ├── api/                       # API modules
│   ├── common/                    # Common utilities
│   ├── pages/                     # Page objects
│   ├── testcase/                  # Test cases
│   ├── use_case/                  # Use cases
│   ├── base_prerequisites.py     # Precondition operations
│   ├── base_assertions.py        # Business assertions
│   └── run_testcase.py            # Test runner
├── data/
│   ├── database.db               # SQLite database
│   ├── screenshots/              # Screenshot storage
│   └── test-files/               # Uploadable test files
├── outputs/                       # Execution outputs (per run)
│   └── {run_id}/
│       ├── logs/run.jsonl        # Structured logs
│       ├── dom/step_N.txt        # DOM snapshots
│       └── screenshots/step_N.png # Screenshots
├── e2e/                          # Playwright E2E tests
├── pyproject.toml                # Python dependencies
└── .env                         # Environment config
```

## Directory Purposes

**backend/api/:**
- Purpose: HTTP API endpoints
- Contains: FastAPI routers, request/response handlers
- Key files: `main.py`, `routes/runs.py`

**backend/agent/:**
- Purpose: Browser automation with LLM
- Contains: Agent wrappers, detectors, DOM patches, prompts
- Key files: `monitored_agent.py`, `stall_detector.py`, `dom_patch.py`

**backend/core/:**
- Purpose: Business logic orchestration
- Contains: Service classes, event management
- Key files: `agent_service.py`, `precondition_service.py`

**backend/llm/:**
- Purpose: AI model integration
- Contains: LLM factory, adapters, config
- Key files: `factory.py`, `base.py`

**backend/db/:**
- Purpose: Data persistence
- Contains: Models, repositories, schemas
- Key files: `models.py`, `repository.py`

**webseleniumerp/:**
- Purpose: External Selenium automation project (reused for preconditions/assertions)
- Contains: Page objects, API wrappers, precondition operations, business assertions
- Key files: `base_prerequisites.py`, `base_assertions.py`

## Key File Locations

**Entry Points:**
- `backend/api/main.py`: FastAPI app initialization
- `backend/run_server.py`: Server startup script
- `backend/api/routes/runs.py`: Background execution entry

**Configuration:**
- `backend/config/settings.py`: Pydantic settings from env
- `backend/llm/config.py`: YAML-based LLM config
- `.env`: Environment variables

**Core Logic:**
- `backend/core/agent_service.py`: Agent execution orchestration (main entry)
- `backend/agent/monitored_agent.py`: Monitored browser-use Agent
- `backend/api/routes/runs.py:run_agent_background()`: Full pipeline

**Testing:**
- `backend/tests/`: Unit tests
- `e2e/`: Playwright E2E tests

## Naming Conventions

**Files:**
- Python: snake_case (`agent_service.py`, `run_logger.py`)
- TypeScript: camelCase (`index.ts`, `RunMonitor.tsx`)
- Directories: snake_case

**Functions/Classes:**
- Classes: PascalCase (`MonitoredAgent`, `AgentService`)
- Functions: snake_case (`create_llm`, `run_agent_background`)

**Variables:**
- snake_case (`run_id`, `step_index`)
- Constants: SCREAMING_SNAKE_CASE (`SERVER_BROWSER_ARGS`)

## Where to Add New Code

**New Feature (API endpoint):**
- Primary code: `backend/api/routes/{feature}.py`
- Register in: `backend/api/main.py`
- Add schema: `backend/db/schemas.py`

**New Agent Detector:**
- Implementation: `backend/agent/{detector_name}.py`
- Integration: `backend/agent/monitored_agent.py` (inject in `__init__`)

**New Core Service:**
- Implementation: `backend/core/{service_name}_service.py`
- Used by: `backend/api/routes/runs.py`

**New Database Model:**
- Model: `backend/db/models.py`
- Repository: `backend/db/repository.py`
- Schema: `backend/db/schemas.py`

**Utilities:**
- Shared helpers: `backend/utils/{utility_name}.py`

## Special Directories

**outputs/:**
- Purpose: Per-run execution artifacts
- Contains: JSONL logs, DOM snapshots, screenshots
- Generated: Yes (during execution)
- Committed: No (gitignored)

**data/:**
- Purpose: Persistent runtime data
- Contains: SQLite database, test files
- Generated: Yes (automatic)
- Committed: `database.db` may be committed for dev

**webseleniumerp/:**
- Purpose: External Selenium automation project
- Contains: Page objects, test cases, API wrappers
- Used by: PreconditionService for external operations

## Database Models

**Task:**
- Purpose: Test case definition
- Fields: id, name, description, target_url, max_steps, preconditions, external_assertions

**Run:**
- Purpose: Single test execution instance
- Fields: id, task_id, status, started_at, finished_at, external_assertion_results
- Relations: task, steps, assertion_results, precondition_results

**Step:**
- Purpose: Individual execution step
- Fields: id, run_id, step_index, action, reasoning, screenshot_path, status, error, step_stats, sequence_number

**Assertion:**
- Purpose: UI assertion definition
- Fields: id, task_id, name, type, expected

**AssertionResult:**
- Purpose: Assertion execution result
- Fields: id, run_id, assertion_id, status, message, actual_value, sequence_number

**PreconditionResult:**
- Purpose: Precondition execution result
- Fields: id, run_id, sequence_number, index, code, status, error, duration_ms, variables

**Report:**
- Purpose: Test execution summary
- Fields: id, run_id, task_id, task_name, status, total_steps, success_steps, failed_steps, duration_ms

---

*Structure analysis: 2026-04-03*
