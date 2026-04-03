# Architecture

**Analysis Date:** 2026-04-03

## Pattern Overview

**Overall:** Event-Driven Async Pipeline with LLM-Orchestrated Browser Automation

**Key Characteristics:**
- Asynchronous execution pipeline (FastAPI + asyncio)
- LLM-driven browser automation using browser-use framework
- SSE (Server-Sent Events) for real-time progress streaming
- Multi-stage execution: preconditions -> agent run -> assertions -> report
- Plugin-style detectors for runtime monitoring

## Layers

**API Layer (FastAPI):**
- Purpose: HTTP API endpoints for task/run management
- Location: `backend/api/`
- Contains: Route handlers, SSE event streaming
- Depends on: Core services
- Used by: Frontend React application

**Core Services Layer:**
- Purpose: Business logic orchestration
- Location: `backend/core/`
- Contains: `AgentService`, `PreconditionService`, `AssertionService`, `ReportService`, `EventManager`
- Depends on: Database repositories, LLM factory
- Used by: API routes

**Agent Layer (browser-use):**
- Purpose: LLM-powered browser automation execution
- Location: `backend/agent/`
- Contains: `MonitoredAgent`, `StallDetector`, `PreSubmitGuard`, `TaskProgressTracker`, `Prompts`
- Depends on: browser-use library, LLM adapters
- Used by: AgentService

**LLM Integration Layer:**
- Purpose: Unified interface for AI model providers
- Location: `backend/llm/`
- Contains: `Factory`, `BaseLLM`, `Config`, `BrowserUseAdapter`
- Depends on: External AI APIs (DashScope, OpenAI compatible)
- Used by: Agent layer, PreconditionService

**Data Access Layer (SQLAlchemy):**
- Purpose: Database persistence
- Location: `backend/db/`
- Contains: Models, Repository classes, Schemas
- Used by: Core services

**Utility Layer:**
- Purpose: Logging, screenshots, file operations
- Location: `backend/utils/`
- Contains: `RunLogger`, `StructuredLogger`, `ScreenshotManager`

## Data Flow

**Task Execution Pipeline:**

```
Frontend Request
       |
       v
POST /api/runs (runs.py:create_run)
       |
       v
Background Task: run_agent_background()
       |
       +--> PreconditionService.execute_single()  [Optional]
       |         |
       |         v
       |    ContextWrapper (variable storage)
       |         |
       +--> AgentService.run_with_cleanup()
       |         |
       |         v
       |    MonitoredAgent (browser-use)
       |         |
       |         +--> StallDetector.check()
       |         +--> PreSubmitGuard.check()
       |         +--> TaskProgressTracker.check_progress()
       |         |
       |         v
       |    Per-step callbacks -> EventManager.publish()
       |         |
       +--> AssertionService.evaluate_all()  [Optional]
       |         |
       |         v
       +--> execute_all_assertions() (external)  [Optional]
       |
       v
ReportService.generate_report()
       |
       v
Database (SQLite)
```

**State Management:**
- **Run State**: Stored in SQLite database (`Run` model with status: pending/running/success/failed/stopped)
- **Step State**: Appended to `Step` table per execution step
- **Variable State**: `ContextWrapper` dict for preconditions, passed via Jinja2 substitution
- **Event State**: `EventManager` in-memory store with SSE subscription

## Key Abstractions

**MonitoredAgent:**
- Purpose: Wraps browser-use Agent with runtime detectors
- Location: `backend/agent/monitored_agent.py`
- Pattern: Inherit from browser-use `Agent`, override `_prepare_context()` and `_execute_actions()`
- Key methods:
  - `_prepare_context()`: Injects intervention messages into LLM context
  - `_execute_actions()`: Blocks submit clicks when PreSubmitGuard detects mismatches
  - `create_step_callback()`: Returns async callback for detector integration

**StallDetector:**
- Purpose: Detects agent stall via consecutive failures and stagnant DOM
- Location: `backend/agent/stall_detector.py`
- Detection: Monitors action_name, target_index, evaluation, dom_hash
- Triggers: Consecutive 2+ failures on same element OR 3+ steps with identical DOM

**PreSubmitGuard:**
- Purpose: Validates form fields before submit clicks
- Location: `backend/agent/pre_submit_guard.py`
- Pattern: Extracts expected values via regex from task description
- Blocks submit when extracted expectations don't match actual values

**TaskProgressTracker:**
- Purpose: Tracks step progress and warns when budget is tight
- Location: `backend/agent/task_progress_tracker.py`
- Pattern: Parses task description into structured step lists
- Warns when remaining_steps < remaining_tasks * 1.5

**EventManager:**
- Purpose: Pub/sub for SSE events per run
- Location: `backend/core/event_manager.py`
- Pattern: Singleton, async queue-based subscription with heartbeat

**LLM Factory:**
- Purpose: Create and cache LLM instances per model
- Location: `backend/llm/factory.py`
- Pattern: Class method factory with caching
- Uses: `tenacity` for retry with exponential backoff

**ContextWrapper:**
- Purpose: Dict-like interface for precondition execution context
- Location: `backend/core/precondition_service.py`
- Supports: Variable storage (`context['var'] = value`), data method calls (`context.get_data()`)

## Entry Points

**HTTP API:**
- Location: `backend/api/main.py`
- Triggers: Frontend HTTP requests
- Responsibilities: Route registration, exception handling, CORS

**Background Task Runner:**
- Location: `backend/api/routes/runs.py:run_agent_background()`
- Triggers: POST /api/runs with BackgroundTasks
- Responsibilities: Full execution pipeline orchestration

**CLI/Server:**
- Location: `backend/run_server.py`
- Triggers: `uv run python backend/run_server.py`
- Responsibilities: FastAPI app startup

## Error Handling

**Strategy:** Layered error handling with graceful degradation

**Patterns:**
- Preconditions: Fail-fast (stop execution on first failure)
- Agent execution: Fault-tolerant detectors (non-blocking errors)
- Assertions: Non-fail-fast (results collected, status determined by aggregate)
- API: Global exception handlers with structured JSON responses

## Cross-Cutting Concerns

**Logging:**
- Structured JSONL per-run logs (`RunLogger` in `outputs/{run_id}/logs/run.jsonl`)
- DOM snapshots saved per step (`outputs/{run_id}/dom/step_N.txt`)
- Screenshots captured per step (`outputs/{run_id}/screenshots/step_N.png`)

**Validation:**
- Pydantic BaseSettings for config (`backend/config/settings.py`)
- Pydantic schemas for API request/response (`backend/db/schemas.py`)

**Authentication:**
- API keys via environment variables (DASHSCOPE_API_KEY, OPENAI_API_KEY)
- ERP credentials via environment variables

---

*Architecture analysis: 2026-04-03*
