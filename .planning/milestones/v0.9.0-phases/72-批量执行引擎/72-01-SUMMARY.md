---
phase: 72-批量执行引擎
plan: 01
subsystem: api, database
tags: [asyncio, semaphore, fastapi, sqlalchemy, batch-execution, sqlite]

# Dependency graph
requires:
  - phase: 71-批量导入工作流
    provides: Task model with imported tasks for batch execution
provides:
  - Batch ORM model with id, concurrency, status, created_at, finished_at
  - Run.batch_id foreign key linking runs to batches
  - BatchRepository with CRUD and run listing
  - BatchExecutionService with Semaphore-gated concurrency control
  - POST /batches, GET /batches/{id}, GET /batches/{id}/runs API routes
  - SQLite busy_timeout (30s) for concurrent write lock handling
affects: [73-批量进度UI]

# Tech tracking
tech-stack:
  added: []
  patterns: [asyncio.Semaphore concurrency gating, module-level _active_batches GC prevention, fire-and-forget asyncio.create_task for background batch execution]

key-files:
  created:
    - backend/core/batch_execution.py
    - backend/api/routes/batches.py
    - backend/tests/unit/test_batch_api.py
    - backend/tests/unit/test_batch_execution.py
  modified:
    - backend/db/models.py
    - backend/db/schemas.py
    - backend/db/repository.py
    - backend/db/database.py
    - backend/api/main.py

key-decisions:
  - "BatchExecutionService uses asyncio.Semaphore with min(concurrency, MAX_CONCURRENCY=4) hard cap"
  - "_active_batches module-level dict prevents GC of active services during batch execution"
  - "asyncio.create_task for fire-and-forget batch execution (not FastAPI BackgroundTasks) for immediate status tracking"
  - "SQLite busy_timeout set to 30 seconds via connect_args={'timeout': 30}"
  - "Batch status transitions: pending -> running -> completed, finalized in try/finally with registry cleanup"

patterns-established:
  - "Semaphore-gated parallel execution: BatchExecutionService._execute_run acquires semaphore per run"
  - "Error isolation: gather(return_exceptions=True) + per-run try/except ensures single failures do not propagate"
  - "Independent DB sessions per concurrent run via async_session() context manager"

requirements-completed: [BATCH-01, BATCH-02]

# Metrics
duration: 72min
completed: 2026-04-08
---

# Phase 72: Batch Execution Engine Summary

**Batch ORM model, BatchExecutionService with Semaphore concurrency (default 2, cap 4), and POST/GET /batches API routes for parallel task execution**

## Performance

- **Duration:** 72 min
- **Started:** 2026-04-08T17:20:00Z
- **Completed:** 2026-04-08T18:32:51Z
- **Tasks:** 3
- **Files modified:** 9

## Accomplishments
- Batch ORM model with concurrency tracking and Run relationship for batch execution lifecycle
- BatchExecutionService with asyncio.Semaphore concurrency control, error isolation, and GC prevention via _active_batches registry
- Three batch API endpoints: POST /batches (create + start), GET /batches/{id} (status + run summaries), GET /batches/{id}/runs (run list for progress UI)
- SQLite busy_timeout (30s) configured for concurrent write lock contention during parallel browser execution

## Task Commits

Each task was committed atomically:

1. **Task 0: Wave 0 test stubs** - `7bb5c28` (test)
2. **Task 1: Batch model, schemas, repository, DB config** - `b17103a` (feat)
3. **Task 2: BatchExecutionService and batches API routes** - `074f366` (feat)

## Files Created/Modified
- `backend/core/batch_execution.py` - BatchExecutionService with Semaphore-gated parallel execution, error isolation, batch finalization
- `backend/api/routes/batches.py` - POST /batches, GET /batches/{id}, GET /batches/{id}/runs endpoints
- `backend/tests/unit/test_batch_api.py` - 3 Wave 0 test stubs for batch API integration tests
- `backend/tests/unit/test_batch_execution.py` - 4 Wave 0 test stubs for BatchExecutionService unit tests
- `backend/db/models.py` - Batch ORM model added before Run; Run gains batch_id FK and batch relationship
- `backend/db/schemas.py` - BatchCreateRequest, BatchRunSummary, BatchResponse Pydantic schemas
- `backend/db/repository.py` - BatchRepository with create, get, get_with_runs, update_status, list_runs_by_batch
- `backend/db/database.py` - connect_args={"timeout": 30} for SQLite busy_timeout + batch_id migration
- `backend/api/main.py` - batches router registered at /api prefix

## Decisions Made
- Used asyncio.create_task instead of FastAPI BackgroundTasks for immediate status tracking from batch creation moment
- _active_batches module-level dict chosen over app.state for GC prevention (simpler, sufficient for single-server deployment)
- Batch status set to "completed" after all runs finish, regardless of individual run outcomes (success/failed/stopped all count as terminal)
- Concurrency cap enforced at BatchExecutionService.__init__ via min(concurrency, MAX_CONCURRENCY)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Batch backend complete and ready for Phase 73 (batch progress UI) which will consume GET /batches/{id} for polling
- Phase 72-02 will add frontend batch execute button + confirmation dialog to the Tasks page
- Wave 0 test stubs ready for implementation in Phase 72-02 or during integration testing

## Self-Check: PASSED

- All 4 created files verified: backend/core/batch_execution.py, backend/api/routes/batches.py, backend/tests/unit/test_batch_api.py, backend/tests/unit/test_batch_execution.py
- All 3 task commits verified: 7bb5c28, b17103a, 074f366
- All Python imports succeed without errors
- All 7 test stubs collected by pytest

---
*Phase: 72-批量执行引擎*
*Completed: 2026-04-08*
