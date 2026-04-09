# Phase 72: 批量执行引擎 - Research

**Researched:** 2026-04-08
**Domain:** Async batch execution with concurrency control (asyncio.Semaphore + SQLite + FastAPI)
**Confidence:** HIGH

## Summary

Phase 72 adds a batch execution engine that lets QA select multiple tasks and run them in parallel with controlled concurrency. The architecture reuses the existing `run_agent_background()` function for each individual task, wrapping it in a new `BatchExecutionService` that coordinates scheduling via `asyncio.Semaphore` (default 2, max 4 concurrent browser instances). A new `Batch` ORM model tracks the overall batch progress, with individual `Run` records linked via a new `batch_id` foreign key. The frontend adds a "batch execute" button to the existing `BatchActions` component with a confirmation dialog containing a concurrency slider.

The backend follows established patterns: new `BatchRepository`, new `batches.py` route module, and Pydantic schemas. SQLite concurrent write contention is the primary risk -- each concurrent run writes steps/assertion results, and the current `pool_size=5` with no `busy_timeout` configuration may cause lock timeouts. The plan must ensure each concurrent run gets its own `async_session` and that SQLite busy timeout is configured.

**Primary recommendation:** Create `BatchExecutionService` as a standalone class that spawns `asyncio.create_task` for each run (not FastAPI BackgroundTasks), wraps each in a Semaphore-gated coroutine with isolated error handling, and aggregates run statuses to update batch status on completion.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Click "batch execute" opens confirmation dialog with task count + concurrency slider (1-4, default 2) + confirm/cancel buttons
- **D-02:** "Batch execute" button added to existing BatchActions component, alongside "set ready" and "batch delete"
- **D-03:** Confirmation dialog is simple summary form (task count + concurrency), not a full task list
- **D-04:** New Batch database table with id, concurrency, status, created_at, finished_at
- **D-05:** Batch-Run one-to-many relationship, each Run associates with a Batch via batch_id
- **D-06:** Two-level status flow -- Batch: pending/running/completed; Run: pending/running/success/failed/stopped
- **D-07:** Batch status aggregated from child Run statuses: all Runs in terminal state -> Batch becomes completed
- **D-08:** Create standalone BatchExecutionService class for Semaphore, task scheduling, error isolation, progress updates
- **D-09:** BatchExecutionService uses asyncio.Semaphore, default 2, hard limit 4
- **D-10:** Single task failure does not affect other tasks, errors recorded in corresponding Run
- **D-11:** Reuse existing `run_agent_background()` for individual task execution, BatchExecutionService handles coordination
- **D-12:** Create independent batches route module (backend/api/routes/batches.py)
- **D-13:** POST /batches -- create batch (receives task_ids + concurrency), creates Batch record + Run per task, starts parallel execution
- **D-14:** GET /batches/{id} -- query batch progress (returns batch status + run status summary)
- **D-15:** GET /batches/{id}/runs -- query runs within a batch (for Phase 73 batch progress UI)

### Claude's Discretion
- Batch model specific field types and default values
- Confirmation dialog component specific UI style and layout
- Concurrency slider step size and default display
- BatchExecutionService internal implementation details (semaphore allocation, error handling flow)
- API response specific JSON structure

### Deferred Ideas (OUT OF SCOPE)
- Batch cancel operation (BATCH-05) -- v2 requirement
- Batch retry failed tasks (BATCH-06) -- v2 requirement
- Batch execution summary report (BATCH-04) -- v2 requirement
- Batch progress UI page -- Phase 73 scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| BATCH-01 | User can select multiple Tasks in TaskTable and click "batch execute" to start parallel execution | Frontend BatchActions extension (D-02), TaskTable already has selectedIds mechanism, confirmation dialog (D-01/D-03) |
| BATCH-02 | Batch execution uses asyncio.Semaphore to control concurrency, default 2, user-configurable (max 4), preventing server OOM | BatchExecutionService (D-08/D-09), Semaphore pattern, per-Run error isolation (D-10) |
</phase_requirements>

## Standard Stack

### Core (already installed, zero new dependencies)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| asyncio | stdlib | Semaphore concurrency control, task spawning | Built-in, no dependency needed |
| FastAPI | >=0.135.1 | Batch API routes | Existing framework |
| SQLAlchemy | >=2.0.0 | Batch ORM model, relationships | Existing ORM layer |
| aiosqlite | >=0.20.0 | Async SQLite driver | Existing async DB driver |
| Pydantic | >=2.4.0 | Batch request/response schemas | Existing validation layer |

### Supporting (already installed)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest-asyncio | >=0.24.0 | Async test runner | Unit/integration tests for BatchExecutionService |
| lucide-react | >=0.577.0 | Play icon for batch execute button | Frontend button icon |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| asyncio.create_task | FastAPI BackgroundTasks | BackgroundTasks runs after response, harder to track; create_task gives immediate control and status tracking |
| asyncio.Semaphore | Celery/task queue | Overkill for single-server; Semaphore is lightweight and sufficient |
| In-memory batch tracking | Database-only tracking | In-memory + DB hybrid gives instant status reads; DB-only requires queries per status check |

**Installation:**
```bash
# Zero new dependencies required
```

**Version verification:** All dependencies already installed per pyproject.toml and frontend/package.json.

## Architecture Patterns

### Recommended Project Structure
```
backend/
├── api/routes/batches.py        # NEW: batch API routes
├── core/batch_execution.py      # NEW: BatchExecutionService
├── db/models.py                 # MODIFY: add Batch model, add batch_id to Run
├── db/schemas.py                # MODIFY: add Batch schemas
├── db/repository.py             # MODIFY: add BatchRepository
├── db/database.py               # MODIFY: add busy_timeout for concurrent writes
├── api/main.py                  # MODIFY: include batches router

frontend/src/
├── api/batches.ts               # NEW: batch API client
├── components/TaskList/BatchActions.tsx  # MODIFY: add batch execute button + dialog
├── pages/Tasks.tsx              # MODIFY: add batch execute handler
├── types/index.ts               # MODIFY: add Batch types
```

### Pattern 1: Semaphore-Gated Task Execution
**What:** BatchExecutionService creates an asyncio.Semaphore with user-specified concurrency, then spawns one asyncio.Task per run. Each task acquires the semaphore before starting browser execution.
**When to use:** All batch execution scenarios.
**Example:**
```python
# Source: established asyncio pattern
class BatchExecutionService:
    def __init__(self, concurrency: int = 2):
        self._semaphore = asyncio.Semaphore(min(concurrency, 4))  # hard cap
        self._tasks: list[asyncio.Task] = []

    async def execute_batch(self, batch_id: str, run_configs: list[dict]):
        """Execute all runs with semaphore-gated concurrency."""
        self._tasks = [
            asyncio.create_task(self._execute_run(batch_id, config))
            for config in run_configs
        ]
        await asyncio.gather(*self._tasks, return_exceptions=True)
        await self._finalize_batch(batch_id)

    async def _execute_run(self, batch_id: str, config: dict):
        async with self._semaphore:
            try:
                await run_agent_background(**config)
            except Exception as e:
                logger.error(f"Run {config['run_id']} failed: {e}")
                # Error recorded in run by run_agent_background, no propagation needed
```

### Pattern 2: Batch Status Aggregation
**What:** After all runs complete, query all run statuses and set batch status accordingly.
**When to use:** In BatchExecutionService._finalize_batch after all tasks complete.
**Example:**
```python
async def _finalize_batch(self, batch_id: str):
    async with async_session() as session:
        batch_repo = BatchRepository(session)
        run_repo = RunRepository(session)
        runs = await run_repo.list_by_batch(batch_id)
        terminal_states = {"success", "failed", "stopped"}
        all_terminal = all(r.status in terminal_states for r in runs)
        if all_terminal:
            await batch_repo.update_status(batch_id, "completed")
```

### Pattern 3: Independent Database Sessions per Run
**What:** Each concurrent run creates its own `async_session()` context, matching the existing `run_agent_background` pattern (line 76 of runs.py: `async with async_session() as session`).
**When to use:** All batch execution -- critical for SQLite concurrency since each run needs its own connection.

### Anti-Patterns to Avoid
- **Shared DB session across runs:** SQLite only allows one writer at a time; sharing a session across concurrent runs will cause lock contention and data corruption. Each run MUST have its own session.
- **Using BackgroundTasks for batch runs:** `FastAPI.BackgroundTasks.add_task()` runs after the response is sent and is designed for fire-and-forget. For batch execution, we need immediate task creation with `asyncio.create_task` so status is trackable from the moment the batch starts.
- **Blocking the event loop:** `run_agent_background` is already fully async (aiosqlite, browser-use agent). No risk here as long as we don't introduce sync I/O in the coordination layer.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Concurrency control | Custom thread pool or process pool | asyncio.Semaphore | All browser-use code is async; threads add complexity for no benefit |
| Task status tracking | Custom in-memory state machine | Database models (Batch/Run status fields) | Persistence across server restarts, queryable by API |
| Error isolation | try/except at top level per run | run_agent_background already handles errors internally (lines 381-394) | Existing error handling records failures to Run and publishes SSE events |
| Batch-run relationship | Custom mapping table | SQLAlchemy ForeignKey + relationship | ORM handles joins, cascades, and queries |

**Key insight:** The existing `run_agent_background` function (runs.py lines 55-394) is already a self-contained execution unit with its own DB session, error handling, and SSE event publishing. BatchExecutionService only needs to coordinate WHEN each run starts (via Semaphore) and aggregate final statuses. This dramatically reduces implementation risk.

## Common Pitfalls

### Pitfall 1: SQLite Concurrent Write Lock Contention
**What goes wrong:** Multiple runs writing steps/assertion results simultaneously cause "database is locked" errors.
**Why it happens:** SQLite only allows one writer at a time. The current engine config has `pool_size=5` but no `busy_timeout` -- a waiting writer will fail immediately instead of waiting.
**How to avoid:** Add `connect_args={"timeout": 30}` to `create_async_engine` in database.py. This sets SQLite's busy_timeout to 30 seconds, allowing concurrent writers to wait for locks rather than failing. Additionally, ensure each run creates its own `async_session()` context (already the pattern in run_agent_background).
**Warning signs:** "OperationalError: database is locked" in logs during batch execution.

### Pitfall 2: Batch Status Not Finalized on Partial Failure
**What goes wrong:** One run fails with an uncaught exception, asyncio.gather(return_exceptions=True) swallows it, and _finalize_batch never runs.
**Why it happens:** If _finalize_batch is called after gather but the batch status update itself fails.
**How to avoid:** Wrap _finalize_batch in its own try/finally, and consider updating batch status in each individual run's finally block as a belt-and-suspenders approach.
**Warning signs:** Batch stuck in "running" status indefinitely after all runs have completed.

### Pitfall 3: Server OOM from Too Many Browser Instances
**What goes wrong:** User sets concurrency to 4, each Chromium instance uses 200-500MB, total 0.8-2GB exceeds available server memory.
**Why it happens:** Server (121.40.191.49) has limited RAM; concurrent browser instances compound memory usage.
**How to avoid:** Hard cap Semaphore at 4 (D-09). The slider UI must enforce max=4. Default 2 is conservative and safe for the deployment server.
**Warning signs:** Server becomes unresponsive, Chromium crashes with OOM, runs fail with browser disconnection errors.

### Pitfall 4: Frontend Race Condition on Batch Creation
**What goes wrong:** User clicks "batch execute" twice quickly, creating two batches for the same tasks.
**Why it happens:** No debounce or loading state guard on the button.
**How to avoid:** Disable the button while the batch creation request is in flight (standard loading state pattern). The confirmation dialog should also close immediately on confirm.
**Warning signs:** Duplicate runs for the same tasks in the same batch.

### Pitfall 5: BatchExecutionService Lifecycle
**What goes wrong:** BatchExecutionService instance is garbage collected while runs are still in progress.
**Why it happens:** If the service is created as a local variable in the route handler, it may be GC'd after the response is sent.
**How to avoid:** Store active batch services in a module-level dict or attach to app state. For the current scale (single server, low batch volume), a simple `dict[str, BatchExecutionService]` at module level is sufficient.
**Warning signs:** Runs start but batch status never updates; "Task was destroyed but it is pending" warnings in logs.

## Code Examples

### Batch ORM Model (models.py addition)
```python
# Source: following existing model patterns (Task, Run, etc.)
class Batch(Base):
    """批量执行批次模型"""
    __tablename__ = "batches"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    concurrency: Mapped[int] = mapped_column(Integer, default=2)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, running, completed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    runs: Mapped[List["Run"]] = relationship("Run", back_populates="batch")
```

### Run Model Modification (add batch_id)
```python
# Source: extending existing Run model
# Add to Run class:
batch_id: Mapped[Optional[str]] = mapped_column(
    String(8), ForeignKey("batches.id"), nullable=True
)
batch: Mapped[Optional["Batch"]] = relationship("Batch", back_populates="runs")
```

### Batch Schema (schemas.py addition)
```python
# Source: following existing Pydantic patterns
class BatchCreateRequest(BaseModel):
    task_ids: List[str] = Field(..., min_length=1, max_length=50)
    concurrency: int = Field(default=2, ge=1, le=4)

class BatchRunSummary(BaseModel):
    id: str
    task_id: str
    task_name: Optional[str] = None
    status: str

class BatchResponse(BaseModel):
    id: str
    concurrency: int
    status: str
    created_at: datetime
    finished_at: Optional[datetime] = None
    runs: Optional[List[BatchRunSummary]] = None

    class Config:
        from_attributes = True
```

### Database Busy Timeout (database.py modification)
```python
# Source: SQLAlchemy async engine with SQLite busy_timeout
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"timeout": 30},  # SQLite busy_timeout: wait up to 30s for locks
)
```

### Batch Execution Service Core (batch_execution.py)
```python
# Source: asyncio pattern for semaphore-gated parallel execution
import asyncio
import logging
from datetime import datetime
from typing import Any

from backend.db.database import async_session
from backend.db.repository import BatchRepository, RunRepository, TaskRepository
from backend.api.routes.runs import run_agent_background

logger = logging.getLogger(__name__)

MAX_CONCURRENCY = 4

# Module-level registry to prevent GC of active services
_active_batches: dict[str, "BatchExecutionService"] = {}


class BatchExecutionService:
    def __init__(self, batch_id: str, concurrency: int = 2):
        self.batch_id = batch_id
        self._semaphore = asyncio.Semaphore(min(concurrency, MAX_CONCURRENCY))
        self._tasks: list[asyncio.Task] = []

    async def start(self, run_configs: list[dict[str, Any]]):
        """Start all runs with semaphore-gated concurrency."""
        _active_batches[self.batch_id] = self

        # Update batch status to running
        async with async_session() as session:
            repo = BatchRepository(session)
            await repo.update_status(self.batch_id, "running")

        # Create tasks
        self._tasks = [
            asyncio.create_task(self._execute_run(config))
            for config in run_configs
        ]

        # Run all and finalize
        await asyncio.gather(*self._tasks, return_exceptions=True)
        await self._finalize_batch()

    async def _execute_run(self, config: dict[str, Any]):
        """Execute a single run under semaphore control."""
        async with self._semaphore:
            try:
                await run_agent_background(**config)
            except Exception as e:
                logger.error(f"[Batch {self.batch_id}] Run {config.get('run_id')} error: {e}")

    async def _finalize_batch(self):
        """Aggregate run statuses and update batch status."""
        try:
            async with async_session() as session:
                batch_repo = BatchRepository(session)
                await batch_repo.update_status(
                    self.batch_id, "completed",
                    finished_at=datetime.now(),
                )
        finally:
            _active_batches.pop(self.batch_id, None)
```

### Frontend Batch Execute Button (BatchActions.tsx modification)
```typescript
// Source: extending existing BatchActions pattern
import { Trash2, CheckCircle, Play } from 'lucide-react'

interface BatchActionsProps {
  selectedCount: number
  onBatchDelete: () => void
  onBatchSetReady: () => void
  onBatchExecute: () => void  // NEW prop
}

export function BatchActions({
  selectedCount,
  onBatchDelete,
  onBatchSetReady,
  onBatchExecute,  // NEW
}: BatchActionsProps) {
  if (selectedCount === 0) return null

  return (
    <div className="flex items-center gap-4 px-4 py-2 bg-blue-50 border-y border-blue-100">
      <span className="text-sm text-blue-700">已选中 {selectedCount} 项</span>
      <div className="flex items-center gap-2">
        <button onClick={onBatchExecute} className="...">
          <Play className="w-4 h-4" />
          批量执行
        </button>
        {/* existing buttons */}
      </div>
    </div>
  )
}
```

### Frontend Batch API Client (batches.ts)
```typescript
// Source: following existing apiClient pattern from tasks.ts
import { apiClient } from './client'

export interface BatchCreateResponse {
  id: string
  concurrency: number
  status: string
  created_at: string
}

export const batchesApi = {
  async create(taskIds: string[], concurrency: number = 2): Promise<BatchCreateResponse> {
    return apiClient<BatchCreateResponse>('/batches', {
      method: 'POST',
      body: JSON.stringify({ task_ids: taskIds, concurrency }),
    })
  },

  async getStatus(batchId: string) {
    return apiClient<any>(`/batches/${batchId}`)
  },

  async getRuns(batchId: string) {
    return apiClient<any[]>(`/batches/${batchId}/runs`)
  },
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Sequential task execution | Semaphore-gated parallel execution | This phase | Dramatically faster for multi-task QA workflows |
| No batch tracking | Batch model + aggregated status | This phase | Enables Phase 73 progress UI |

**Deprecated/outdated:**
- None -- this is a greenfield feature within the batch execution domain.

## Open Questions

1. **SQLite busy_timeout value**
   - What we know: Current engine config has no busy_timeout; default is 0 (fail immediately).
   - What's unclear: Whether 30 seconds is sufficient for worst case (4 concurrent runs writing steps simultaneously).
   - Recommendation: Set to 30 seconds initially, which is generous for SQLite. Monitor for lock errors in Phase 72 testing. STATE.md mentions "busy_timeout 5000ms may not be enough" but 30s gives ample margin.

2. **BatchExecutionService lifecycle management**
   - What we know: Must prevent GC while runs are in progress.
   - What's unclear: Whether a simple module-level dict is sufficient or if we need app-state integration.
   - Recommendation: Use module-level `_active_batches` dict. For the current single-server, low-volume deployment this is simpler and sufficient. If scale increases later, migrate to app.state.

3. **Frontend confirmation dialog -- custom vs. reuse ConfirmModal**
   - What we know: Existing ConfirmModal is text-only (title + message). Batch confirmation needs a slider control.
   - What's unclear: Whether to extend ConfirmModal or create a new BatchExecuteDialog component.
   - Recommendation: Create a new BatchExecuteDialog component. ConfirmModal's API doesn't support interactive controls like sliders. A dedicated dialog is cleaner and keeps ConfirmModal unchanged for its existing uses.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.11+ | Backend runtime | Available | 3.14.3 | -- |
| uv | Package management | Available | 0.9.24 | -- |
| Node.js 18+ | Frontend build | Available | 22.22.0 | -- |
| npm | Frontend packages | Available | 10.9.4 | -- |
| pytest-asyncio | Backend tests | Available (installed) | >=0.24.0 | -- |
| SQLite | Database | Available (aiosqlite) | bundled | -- |

**Missing dependencies with no fallback:**
- None -- all required dependencies are already installed.

**Missing dependencies with fallback:**
- None.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest + pytest-asyncio |
| Config file | None (defaults) |
| Quick run command | `uv run pytest backend/tests/unit/test_batch*.py -v -x` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| BATCH-01 | POST /batches creates batch record with runs, returns batch_id | integration | `uv run pytest backend/tests/unit/test_batch_api.py::test_create_batch -x` | Wave 0 |
| BATCH-01 | GET /batches/{id} returns batch status with run summaries | integration | `uv run pytest backend/tests/unit/test_batch_api.py::test_get_batch_status -x` | Wave 0 |
| BATCH-01 | GET /batches/{id}/runs returns runs for a batch | integration | `uv run pytest backend/tests/unit/test_batch_api.py::test_get_batch_runs -x` | Wave 0 |
| BATCH-02 | BatchExecutionService respects concurrency limit | unit | `uv run pytest backend/tests/unit/test_batch_execution.py::test_semaphore_limits_concurrency -x` | Wave 0 |
| BATCH-02 | Single run failure does not block other runs | unit | `uv run pytest backend/tests/unit/test_batch_execution.py::test_error_isolation -x` | Wave 0 |
| BATCH-02 | Batch status transitions pending->running->completed | unit | `uv run pytest backend/tests/unit/test_batch_execution.py::test_batch_status_transitions -x` | Wave 0 |
| BATCH-02 | Concurrency capped at MAX_CONCURRENCY=4 | unit | `uv run pytest backend/tests/unit/test_batch_execution.py::test_concurrency_cap -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_batch*.py -v -x`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_batch_api.py` -- covers BATCH-01 API endpoint tests
- [ ] `backend/tests/unit/test_batch_execution.py` -- covers BATCH-02 service tests (Semaphore, error isolation)
- [ ] BatchRepository unit tests can share existing `db_session` fixture from conftest.py

## Sources

### Primary (HIGH confidence)
- Existing codebase analysis -- models.py, repository.py, schemas.py, runs.py, agent_service.py, event_manager.py, database.py, BatchActions.tsx, TaskTable.tsx, Tasks.tsx, useTasks.ts
- STATE.md -- locked decisions on Semaphore defaults, polling strategy, SQLite concerns
- CONTEXT.md -- all architectural decisions (D-01 through D-15)
- Existing test patterns -- conftest.py, test_database_concurrent.py

### Secondary (MEDIUM confidence)
- asyncio.Semaphore documentation (Python stdlib) -- well-established API
- SQLAlchemy async session patterns -- already used in codebase
- FastAPI BackgroundTasks vs asyncio.create_task -- established best practices

### Tertiary (LOW confidence)
- None -- all findings verified against actual codebase.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- zero new dependencies; all patterns established in existing codebase
- Architecture: HIGH -- reuse of run_agent_background eliminates most execution risk; BatchExecutionService is a thin coordination layer
- Pitfalls: HIGH -- SQLite concurrent write contention is a known, well-documented issue with clear mitigation (busy_timeout)
- Frontend: HIGH -- BatchActions extension follows established component patterns

**Research date:** 2026-04-08
**Valid until:** 2026-05-08 (stable -- no fast-moving dependencies)
