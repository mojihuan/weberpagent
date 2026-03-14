# Architecture Research

**Domain:** AI-Driven UI Testing Platform
**Researched:** 2026-03-14
**Confidence:** HIGH (based on comprehensive codebase analysis and established patterns)

## Executive Summary

The aiDriveUITest platform follows a clean layered architecture with event-driven real-time updates. The current implementation has a solid foundation but requires targeted restructuring to achieve v0.1 stability. Key issues include: database schema lacking assertions support, frontend-backend type mismatches, and inconsistent API response formats.

**Recommended approach:** Incremental refactoring preserving the core architecture while fixing data flow issues and adding missing components.

## Current Architecture Assessment

### System Overview (Current)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER (React)                        │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Dashboard │  │  Tasks   │  │   Runs   │  │ Reports  │  │ Monitor  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │             │             │             │             │         │
│  ┌────┴─────────────┴─────────────┴─────────────┴─────────────┴────┐   │
│  │                    API Client + SSE Hook                         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────────┤
│                          API LAYER (FastAPI)                             │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │  /tasks  │  │  /runs   │  │/reports  │  │/dashboard│                 │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘                 │
│       │             │             │             │                        │
├───────┴─────────────┴─────────────┴─────────────┴────────────────────────┤
│                         SERVICE LAYER                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌────────────────┐  ┌─────────────────┐             │
│  │ AgentService  │  │  EventManager  │  │AssertionService │             │
│  │ (browser-use) │  │  (SSE pub-sub) │  │   (archived)    │             │
│  └───────┬───────┘  └───────┬────────┘  └─────────────────┘             │
│          │                  │                                           │
├──────────┴──────────────────┴───────────────────────────────────────────┤
│                           DATA LAYER                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐         │
│  │TaskRepository│ │RunRepository│ │StepRepository│ │ReportRepository│   │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘         │
│         └────────────────┴────────────────┴────────────────┘             │
│                              │                                           │
│                    ┌─────────┴─────────┐                                 │
│                    │   SQLite + ORM    │                                 │
│                    └───────────────────┘                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                      EXTERNAL INTEGRATION                                │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐             │
│  │ Browser-Use    │  │  LLM Provider  │  │   Playwright   │             │
│  │ (Agent Engine) │  │ (Qwen/OpenAI)  │  │   (Browser)    │             │
│  └────────────────┘  └────────────────┘  └────────────────┘             │
└─────────────────────────────────────────────────────────────────────────┘
```

### Current Component Responsibilities

| Component | Responsibility | Status |
|-----------|----------------|--------|
| **Frontend Pages** | UI rendering, user interaction | Works but has type mismatches |
| **API Client** | HTTP communication, error handling | Functional, needs response transform |
| **useRunStream Hook** | SSE connection management | Works correctly |
| **FastAPI Routes** | Request handling, validation | Functional, inconsistent responses |
| **AgentService** | Browser-Use orchestration | Works correctly |
| **EventManager** | SSE pub-sub distribution | Works correctly |
| **Repositories** | Data access abstraction | Missing some methods |
| **LLM Factory** | LLM instance creation | Works, uses archived code |

## Identified Architecture Issues

### Issue 1: Database Schema Gaps

**Problem:** Current schema lacks:
- Assertion configuration (types: URL check, text exists, no errors)
- Assertion results per run/step
- Task configuration storage (target_url underutilized)

**Impact:** Assertions mentioned in requirements but no database support

**Fix:**
```sql
-- Add to schema
CREATE TABLE assertions (
    id TEXT PRIMARY KEY,
    task_id TEXT REFERENCES tasks(id),
    type TEXT NOT NULL,  -- url_check, text_exists, no_errors
    config JSON NOT NULL,
    enabled BOOLEAN DEFAULT true
);

CREATE TABLE assertion_results (
    id TEXT PRIMARY KEY,
    run_id TEXT REFERENCES runs(id),
    assertion_id TEXT REFERENCES assertions(id),
    passed BOOLEAN NOT NULL,
    actual_value TEXT,
    error_message TEXT
);
```

### Issue 2: Frontend-Backend Type Mismatch

**Problem:**
- Backend uses `step_index`, frontend expects `index`
- Backend uses `screenshot_path`, frontend expects `screenshot` URL
- Date formats inconsistent (ISO string vs datetime objects)

**Current Transform (frontend/src/api/reports.ts):**
```typescript
function transformStep(step: StepApiResponse): Step {
  return {
    index: step.step_index,        // Rename
    screenshot: step.screenshot_url || '',  // Transform
    // ...
  }
}
```

**Fix Options:**
1. **Backend-first (recommended):** Standardize backend response to match frontend expectations
2. **Frontend transform layer:** Keep current approach but document mapping explicitly

### Issue 3: Inconsistent API Response Format

**Problem:**
- Some endpoints return direct objects (`/tasks/{id}`)
- Others return wrapped objects (`/reports` returns `{reports: [], total: number}`)
- No consistent error response structure

**Recommended Standard:**
```typescript
// All list endpoints
interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
}

// All single item endpoints
interface ItemResponse<T> {
  data: T;
}

// All errors
interface ErrorResponse {
  error: string;
  detail?: string;
  code?: string;
}
```

### Issue 4: Missing Run-Steps Relationship in Repository

**Problem:** `RunRepository` has `get_steps()` called but not defined

**Location:** `backend/api/routes/runs.py:141`
```python
steps = await run_repo.get_steps(run_id)  # Method doesn't exist
```

**Fix:** Add to RunRepository or use StepRepository

### Issue 5: Hardcoded API Base URL

**Problem:** `API_BASE = 'http://localhost:8080/api'` hardcoded in multiple frontend files

**Files affected:**
- `frontend/src/api/client.ts:1`
- `frontend/src/api/runs.ts:5`
- `frontend/src/hooks/useRunStream.ts:5`

**Fix:** Use environment variable
```typescript
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080/api'
```

## Recommended Architecture (v0.1 Target)

### Target System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER (React)                        │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                         Pages                                     │   │
│  │  Dashboard │ Tasks │ TaskDetail │ RunMonitor │ Reports │ Report  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                         Hooks                                     │   │
│  │  useTasks │ useDashboard │ useRunStream │ useReports              │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                       API Layer                                   │   │
│  │  client.ts │ tasks.ts │ runs.ts │ reports.ts │ dashboard.ts       │   │
│  └──────────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────────┤
│                          API LAYER (FastAPI)                             │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                       Routes (backend/api/routes/)                │   │
│  │  tasks.py │ runs.py │ reports.py │ dashboard.py                   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                       Schemas (backend/db/schemas.py)             │   │
│  │  Request/Response validation with Pydantic                        │   │
│  └──────────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────────┤
│                         SERVICE LAYER                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │AgentService │  │EventManager │  │AssertionSrvc│  │ReportService│    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
├─────────────────────────────────────────────────────────────────────────┤
│                           DATA LAYER                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │              Repositories (backend/db/repository.py)              │   │
│  │  TaskRepo │ RunRepo │ StepRepo │ ReportRepo │ AssertionRepo       │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                  Models (backend/db/models.py)                    │   │
│  │  Task │ Run │ Step │ Report │ Assertion │ AssertionResult         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│                    ┌─────────┴─────────┐                                 │
│                    │   SQLite + ORM    │                                 │
│                    └───────────────────┘                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                      EXTERNAL INTEGRATION                                │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐             │
│  │ Browser-Use    │  │  LLM Provider  │  │   Playwright   │             │
│  │ Agent Engine   │  │ Qwen/OpenAI    │  │   Browser      │             │
│  └────────────────┘  └────────────────┘  └────────────────┘             │
└─────────────────────────────────────────────────────────────────────────┘
```

## Recommended Project Structure

### Backend Structure (Recommended)

```
backend/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry, middleware setup
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tasks.py         # Task CRUD endpoints
│   │   ├── runs.py          # Run execution endpoints
│   │   ├── reports.py       # Report endpoints
│   │   └── dashboard.py     # Dashboard stats endpoints
│   └── deps.py              # Dependency injection helpers (NEW)
├── core/
│   ├── __init__.py
│   ├── agent_service.py     # Browser-Use orchestration
│   ├── event_manager.py     # SSE event management
│   ├── assertion_service.py # Assertion evaluation (restore)
│   └── report_service.py    # Report generation (NEW)
├── db/
│   ├── __init__.py
│   ├── database.py          # SQLAlchemy async setup
│   ├── models.py            # ORM models
│   ├── schemas.py           # Pydantic schemas
│   └── repository.py        # Data access layer
├── llm/
│   ├── __init__.py
│   ├── base.py              # LLM interface
│   ├── factory.py           # LLM creation
│   ├── config.py            # LLM configuration
│   └── openai.py            # OpenAI-compatible implementation
├── config/
│   ├── __init__.py
│   └── settings.py          # Environment config (NEW)
├── tests/
│   └── ...                  # Test files
└── data/
    ├── database.db          # SQLite database
    └── screenshots/         # Screenshot storage
```

### Frontend Structure (Recommended)

```
frontend/src/
├── api/
│   ├── client.ts            # Base fetch wrapper, error handling
│   ├── tasks.ts             # Task API calls
│   ├── runs.ts              # Run API calls
│   ├── reports.ts           # Report API calls
│   ├── dashboard.ts         # Dashboard API calls
│   └── types.ts             # API response types (NEW)
├── components/
│   ├── shared/              # Reusable components
│   ├── Dashboard/           # Dashboard-specific
│   ├── TaskList/            # Task list components
│   ├── TaskDetail/          # Task detail components
│   ├── TaskModal/           # Task form modal
│   ├── RunMonitor/          # Run monitoring components
│   └── Report/              # Report components
├── hooks/
│   ├── useTasks.ts          # Task queries (TanStack Query)
│   ├── useRunStream.ts      # SSE streaming hook
│   ├── useReports.ts        # Report queries
│   └── useDashboard.ts      # Dashboard data
├── pages/
│   ├── Dashboard.tsx
│   ├── Tasks.tsx
│   ├── TaskDetail.tsx
│   ├── RunList.tsx
│   ├── RunMonitor.tsx
│   ├── Reports.tsx
│   └── ReportDetail.tsx
├── types/
│   └── index.ts             # Domain types
├── utils/
│   └── transforms.ts        # API response transforms (NEW)
├── config/
│   └── env.ts               # Environment config (NEW)
├── App.tsx
└── main.tsx
```

### Structure Rationale

- **api/**: Separate API layer for clear data fetching boundaries
- **components/**: Feature-based organization with shared components
- **hooks/**: TanStack Query hooks abstract data fetching from UI
- **types/**: Central type definitions matching backend schemas
- **utils/transforms.ts**: Single location for API-to-domain mapping

## Data Flow Patterns

### Test Execution Flow

```
User Clicks "Run"
    │
    ▼
┌─────────────────┐
│  Frontend       │  POST /api/runs?task_id=xxx
│  createRun()    │────────────────────────────────┐
└─────────────────┘                                │
                                                   ▼
                            ┌──────────────────────────────────┐
                            │  FastAPI /runs                   │
                            │  1. Create Run (status: pending) │
                            │  2. Queue background task        │
                            │  3. Return RunResponse           │
                            └──────────────┬───────────────────┘
                                           │
    ┌──────────────────────────────────────┴────────────────────────┐
    │                    Background Task                              │
    │  ┌──────────────────────────────────────────────────────────┐ │
    │  │  1. Update Run status → "running"                         │ │
    │  │  2. Publish SSE "started" event                           │ │
    │  │  3. Create Browser-Use Agent with LLM                     │ │
    │  │  4. For each step:                                        │ │
    │  │     a. Agent executes action                              │ │
    │  │     b. Callback captures action/reasoning/screenshot      │ │
    │  │     c. Save Step to database                              │ │
    │  │     d. Publish SSE "step" event                           │ │
    │  │  5. Update Run status → "success"/"failed"               │ │
    │  │  6. Create Report                                         │ │
    │  │  7. Publish SSE "finished" event                          │ │
    │  └──────────────────────────────────────────────────────────┘ │
    └───────────────────────────────────────────────────────────────┘
                                           │
                                           ▼
                            ┌──────────────────────────────────┐
                            │  Frontend SSE                    │
                            │  useRunStream subscribes         │
                            │  Real-time UI updates            │
                            └──────────────────────────────────┘
```

### State Management Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                    React Query Cache                             │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │  tasks    │  │   runs    │  │  reports  │  │ dashboard │   │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘   │
└────────┼──────────────┼──────────────┼──────────────┼──────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Hooks Layer                                 │
│  useTasks()   useRunStream()  useReports()  useDashboard()      │
└─────────────────────────────────────────────────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Components                                  │
│  Pages consume hooks, react to state changes automatically      │
└─────────────────────────────────────────────────────────────────┘
```

## Key Architectural Patterns

### Pattern 1: Repository Pattern for Data Access

**What:** Abstract database operations behind repository interfaces

**When to use:** Always - isolates business logic from data access

**Implementation:**
```python
# backend/db/repository.py
class RunRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task_id: str) -> Run:
        run = Run(task_id=task_id, status="pending")
        self.session.add(run)
        await self.session.commit()
        await self.session.refresh(run)
        return run

    async def get_with_steps(self, run_id: str) -> Optional[Run]:
        """NEW: Get run with all steps loaded"""
        stmt = select(Run).where(Run.id == run_id).options(
            selectinload(Run.steps)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
```

### Pattern 2: SSE Event Manager (Pub-Sub)

**What:** In-memory event distribution for real-time updates

**When to use:** Real-time status updates from background tasks

**Current Implementation (works well):**
```python
# backend/core/event_manager.py
class EventManager:
    def __init__(self):
        self._events: dict[str, list[str]] = defaultdict(list)
        self._subscribers: dict[str, list[asyncio.Queue]] = defaultdict(list)

    async def publish(self, run_id: str, event: str | None):
        if event:
            self._events[run_id].append(event)
        for queue in self._subscribers.get(run_id, []):
            await queue.put(event)

    async def subscribe(self, run_id: str) -> AsyncGenerator[str, None]:
        queue = asyncio.Queue()
        self._subscribers[run_id].append(queue)
        # Replay history first
        for event in self._events.get(run_id, []):
            yield event
        # Then stream new events
        while True:
            event = await queue.get()
            yield event
            if event is None:
                break
```

**Trade-offs:**
- (+) Simple, no external dependencies
- (+) History replay for reconnection
- (-) Memory grows with concurrent runs
- (-) Lost on server restart (acceptable for v0.1)

### Pattern 3: Background Tasks with FastAPI

**What:** Use FastAPI BackgroundTasks for async execution

**When to use:** Long-running operations (AI agent execution)

**Implementation:**
```python
# backend/api/routes/runs.py
@router.post("", response_model=RunResponse)
async def create_run(
    task_id: str,
    background_tasks: BackgroundTasks,
    task_repo: TaskRepository = Depends(get_task_repo),
    run_repo: RunRepository = Depends(get_run_repo),
):
    task = await task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    run = await run_repo.create(task_id=task_id)

    # Queue background execution
    background_tasks.add_task(
        run_agent_background,
        run.id,
        task.name,
        task.description,
        task.max_steps,
    )

    return run  # Return immediately, execution continues in background
```

### Pattern 4: Type Transformation Layer

**What:** Transform API responses to frontend domain types

**When to use:** Backend naming conventions differ from frontend expectations

**Implementation:**
```typescript
// frontend/src/utils/transforms.ts
export function transformStep(api: StepApiResponse): Step {
  return {
    index: api.step_index,
    action: api.action,
    reasoning: api.reasoning,
    screenshot: api.screenshot_url
      ? `${API_BASE}${api.screenshot_url}`
      : '',
    status: api.status as 'success' | 'failed',
    error: api.error || undefined,
    duration_ms: api.duration_ms,
  }
}
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Direct Database Access in Routes

**What people do:**
```python
@router.get("/runs/{run_id}")
async def get_run(run_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Run).where(Run.id == run_id))
    return result.scalar_one_or_none()
```

**Why it's wrong:**
- Business logic leaks into route handlers
- Hard to test, hard to reuse
- No single source of truth for queries

**Do this instead:**
```python
@router.get("/runs/{run_id}")
async def get_run(
    run_id: str,
    run_repo: RunRepository = Depends(get_run_repo),
):
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run
```

### Anti-Pattern 2: Hardcoded URLs and Configuration

**What people do:**
```typescript
const response = await fetch('http://localhost:8080/api/tasks')
```

**Why it's wrong:**
- Breaks in production
- No environment-specific configuration
- Scattered magic values

**Do this instead:**
```typescript
// frontend/src/config/env.ts
export const config = {
  apiBase: import.meta.env.VITE_API_BASE || 'http://localhost:8080/api',
}

// frontend/src/api/client.ts
import { config } from '../config/env'

export async function apiClient<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${config.apiBase}${endpoint}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  })
  // ...
}
```

### Anti-Pattern 3: Inconsistent Error Handling

**What people do:**
```python
# Sometimes HTTPException
raise HTTPException(status_code=404, detail="Not found")

# Sometimes return error dict
return {"error": "Not found"}

# Sometimes let exception propagate
```

**Why it's wrong:**
- Frontend can't handle errors consistently
- Mixed response formats

**Do this instead:**
```python
# Always use HTTPException with consistent format
from fastapi import HTTPException

@router.get("/runs/{run_id}")
async def get_run(run_id: str, run_repo: RunRepository = Depends(get_run_repo)):
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(
            status_code=404,
            detail={"error": "RUN_NOT_FOUND", "message": f"Run {run_id} not found"}
        )
    return run
```

### Anti-Pattern 4: Missing Database Migrations

**What people do:** Modify models.py and manually alter SQLite

**Why it's wrong:**
- No version control for schema changes
- Can't rollback
- Team members have inconsistent schemas

**Do this instead:**
```bash
# Add Alembic for v0.2+
alembic init migrations
alembic revision --autogenerate -m "Add assertions tables"
alembic upgrade head
```

**Note:** For v0.1, since SQLite allows schema flexibility, we can add tables without migrations. Plan for Alembic in v0.2.

## Database Schema Recommendations

### Current Schema (Keep)

```python
# backend/db/models.py - EXISTING
class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[str]  # 8-char UUID
    name: Mapped[str]
    description: Mapped[str]
    target_url: Mapped[str]  # Currently underutilized
    max_steps: Mapped[int]
    status: Mapped[str]  # draft, ready
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    runs: Mapped[List["Run"]]

class Run(Base):
    __tablename__ = "runs"
    id: Mapped[str]
    task_id: Mapped[str]
    status: Mapped[str]  # pending, running, success, failed, stopped
    started_at: Mapped[datetime | None]
    finished_at: Mapped[datetime | None]
    created_at: Mapped[datetime]
    steps: Mapped[List["Step"]]

class Step(Base):
    __tablename__ = "steps"
    id: Mapped[str]
    run_id: Mapped[str]
    step_index: Mapped[int]
    action: Mapped[str]
    reasoning: Mapped[str | None]
    screenshot_path: Mapped[str | None]
    status: Mapped[str]
    error: Mapped[str | None]
    duration_ms: Mapped[int | None]

class Report(Base):
    __tablename__ = "reports"
    id: Mapped[str]
    run_id: Mapped[str]
    task_id: Mapped[str]
    task_name: Mapped[str]
    status: Mapped[str]
    total_steps: Mapped[int]
    success_steps: Mapped[int]
    failed_steps: Mapped[int]
    duration_ms: Mapped[int]
```

### Recommended Additions (v0.1)

```python
# NEW: Assertion configuration per task
class Assertion(Base):
    __tablename__ = "assertions"
    id: Mapped[str]
    task_id: Mapped[str]  # FK to tasks
    type: Mapped[str]  # url_check, text_exists, no_errors, custom
    config: Mapped[str]  # JSON string with type-specific config
    enabled: Mapped[bool] = True
    created_at: Mapped[datetime]

    # Relationships
    task: Mapped["Task"] = relationship(back_populates="assertions")

# NEW: Assertion results per run
class AssertionResult(Base):
    __tablename__ = "assertion_results"
    id: Mapped[str]
    run_id: Mapped[str]  # FK to runs
    assertion_id: Mapped[str]  # FK to assertions
    passed: Mapped[bool]
    actual_value: Mapped[str | None]
    error_message: Mapped[str | None]
    created_at: Mapped[datetime]

    # Relationships
    run: Mapped["Run"] = relationship(back_populates="assertion_results")
    assertion: Mapped["Assertion"] = relationship()
```

### Repository Methods to Add

```python
# Add to RunRepository
async def get_steps(self, run_id: str) -> List[Step]:
    """Get all steps for a run"""
    stmt = select(Step).where(Step.run_id == run_id).order_by(Step.step_index)
    result = await self.session.execute(stmt)
    return list(result.scalars())

async def get_with_steps(self, run_id: str) -> Optional[Run]:
    """Get run with steps loaded"""
    stmt = select(Run).where(Run.id == run_id).options(selectinload(Run.steps))
    result = await self.session.execute(stmt)
    return result.scalar_one_or_none()

# Add TaskRepository for assertions
async def get_assertions(self, task_id: str) -> List[Assertion]:
    """Get all assertions for a task"""
    stmt = select(Assertion).where(Assertion.task_id == task_id, Assertion.enabled == True)
    result = await self.session.execute(stmt)
    return list(result.scalars())
```

## Build Order for Restructuring

Based on dependency analysis, recommended implementation order:

### Phase 1: Foundation Fixes (Day 1-2)
1. **Add environment configuration** - Backend `config/settings.py`, Frontend `config/env.ts`
2. **Standardize API responses** - Update all routes to use consistent format
3. **Fix repository methods** - Add missing `get_steps()` method
4. **Add response transformation** - Frontend `utils/transforms.ts`

### Phase 2: Database Enhancement (Day 2-3)
5. **Add Assertion models** - New tables in `models.py`
6. **Add AssertionRepository** - Data access for assertions
7. **Update Task model** - Add assertions relationship

### Phase 3: Service Layer (Day 3-4)
8. **Restore AssertionService** - From archived code, update for new schema
9. **Add ReportService** - Centralize report generation logic
10. **Wire assertions into run flow** - Evaluate after agent execution

### Phase 4: Frontend Alignment (Day 4-5)
11. **Update API types** - Match backend response format
12. **Fix all API clients** - Use transforms consistently
13. **Test end-to-end flow** - Full integration testing

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| **0-10 concurrent users** | Current architecture is sufficient. SQLite handles this load. |
| **10-100 concurrent users** | Add connection pooling, consider PostgreSQL migration. |
| **100+ concurrent users** | Move SSE to Redis pub/sub, add load balancer, separate services. |

### Scaling Priorities

1. **First bottleneck:** SQLite write concurrency
   - **Fix:** Migrate to PostgreSQL with connection pool

2. **Second bottleneck:** EventManager memory
   - **Fix:** Move to Redis pub/sub for event distribution

3. **Third bottleneck:** Screenshot storage
   - **Fix:** Move to S3/MinIO object storage

**Note:** v0.1 targets single-user local development. Scaling considerations are for v0.2+.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| **Browser-Use** | Python library import | Core agent engine, well-isolated |
| **Qwen/OpenAI LLM** | HTTP via OpenAI SDK | Compatible API, configure via env |
| **Playwright** | Browser-Use dependency | Automatic browser management |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Frontend ↔ API | REST + SSE | Keep REST synchronous, SSE for streaming |
| API ↔ Services | Direct function calls | Services are stateless, injected |
| Services ↔ Repositories | Async method calls | All DB access through repositories |
| Services ↔ External | Async HTTP | LLM calls are the main external dependency |

## Sources

- [FastAPI Best Practices (GitHub)](https://github.com/zhanymkanov/fastapi-best-practices) - HIGH confidence
- [Async APIs with FastAPI: Patterns, Pitfalls & Best Practices](https://shiladityamajumder.medium.com/async-apis-with-fastapi-patterns-pitfalls-best-practices-2d72b2b66f25) - HIGH confidence
- [Real-Time Streaming with FastAPI](https://medium.com/@bhagyarana80/real-time-streaming-with-fastapi-simply-90287fe2228b) - HIGH confidence
- [FastAPI Patterns for Real-Time APIs](https://medium.com/@hadiyolworld007/fastapi-patterns-for-real-time-apis-a169aac97b44) - MEDIUM confidence
- Browser-Use Documentation - HIGH confidence (from codebase analysis)
- SQLAlchemy 2.0 Async Documentation - HIGH confidence

---

*Architecture research for: AI-Driven UI Testing Platform*
*Researched: 2026-03-14*
