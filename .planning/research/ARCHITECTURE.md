# Architecture Research: Excel Batch Import and Parallel Execution

**Domain:** AI-Driven UI Testing Platform -- Batch Import & Execution
**Researched:** 2026-04-08
**Confidence:** HIGH (based on comprehensive codebase analysis of existing Task/Run/Agent pipeline)

## System Overview

The batch import and parallel execution feature extends the existing Task -> Run -> Agent pipeline. The core data flow is:

```
Excel File Upload
       |
       v
[Parse + Validate] --> [Preview Response]
       |
       v (user confirms)
[Batch Task Creation] (single transaction, N tasks)
       |
       v (user selects tasks + clicks "batch execute")
[Batch Execution Manager]
  |
  +---> [Semaphore (max 2 concurrent)]
  |       |
  |       +---> Run Agent Task 1 (reuse run_agent_background)
  |       +---> Run Agent Task 2 (reuse run_agent_background)
  |       |
  |       +---> (wait for slot) --> Run Agent Task 3 ...
  |
  +---> [Batch Progress SSE / Polling]
          |
          +---> per-task status updates
          +---> batch-level aggregate status
```

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                             │
├──────────────┬──────────────┬───────────────────────────────────────┤
│ TaskList     │ ImportModal  │ BatchExecutionDashboard                │
│ (checkboxes) │ (upload+prev)│ (per-task status + progress)           │
└──────┬───────┴──────┬───────┴──────────────┬────────────────────────┘
       │              │                      │
┌──────┴──────────────┴──────────────────────┴────────────────────────┐
│                     FastAPI REST + SSE                               │
├──────────────┬──────────────┬───────────────────────────────────────┤
│ /api/tasks   │ /api/import  │ /api/batches                           │
│ (existing)   │ (new)        │ (new)                                  │
└──────┬───────┴──────┬───────┴──────────────┬────────────────────────┘
       │              │                      │
┌──────┴──────────────┴──────────────────────┴────────────────────────┐
│                     Service Layer                                    │
├──────────────┬──────────────┬───────────────────────────────────────┤
│ TaskRepo     │ ImportService│ BatchExecutionManager                  │
│ (existing)   │ (new)        │ (new: semaphore + progress tracking)  │
│              │              │                                        │
│              │ ExcelParser  │ reuses: run_agent_background()        │
│              │ (new)        │                                        │
└──────┬───────┴──────┬───────┴──────────────┬────────────────────────┘
       │              │                      │
┌──────┴──────────────┴──────────────────────┴────────────────────────┐
│                     Data Layer (SQLite WAL)                          │
├──────────────┬──────────────┬───────────────────────────────────────┤
│ tasks        │ batches      │ batch_task_entries                     │
│ (existing)   │ (new)        │ (new: batch_id -> task_id mapping)    │
│ runs         │              │                                       │
│ (existing)   │              │                                       │
└──────────────┴──────────────┴───────────────────────────────────────┘
```

## Recommended Project Structure

### New Backend Files

```
backend/
├── api/
│   └── routes/
│       └── batches.py           # NEW: batch import + execution endpoints
├── core/
│   ├── import_service.py        # NEW: Excel parsing + validation + preview
│   └── batch_manager.py         # NEW: semaphore-based parallel execution + progress
├── db/
│   ├── models.py                # MODIFY: add Batch, BatchTaskEntry models
│   ├── repository.py            # MODIFY: add BatchRepository
│   └── schemas.py               # MODIFY: add batch-related schemas
```

### New Frontend Files

```
frontend/src/
├── api/
│   └── batches.ts               # NEW: batch API client
├── components/
│   ├── ImportModal/
│   │   ├── UploadStep.tsx       # NEW: file upload + drag-drop
│   │   ├── PreviewStep.tsx      # NEW: parsed data preview table
│   │   └── ImportResult.tsx     # NEW: import success/failure summary
│   └── BatchExecution/
│       ├── BatchDashboard.tsx   # NEW: batch progress overview
│       └── TaskStatusCard.tsx   # NEW: individual task status in batch
├── hooks/
│   ├── useBatchImport.ts        # NEW: import state management
│   └── useBatchExecution.ts     # NEW: batch execution + polling
├── pages/
│   └── BatchMonitor.tsx         # NEW: batch execution monitoring page
└── types/
    └── index.ts                 # MODIFY: add Batch-related types
```

### Structure Rationale

- **import_service.py** separated from batch_manager.py because import and execution are independent operations with different lifecycles. Import is synchronous (parse + validate + create tasks); execution is long-running async.
- **BatchRepository** is NOT created as a separate file. Instead, add methods to the existing repository.py following the existing pattern (TaskRepository, RunRepository in same file).
- **Frontend components** split by feature (ImportModal vs BatchExecution) rather than type, matching existing pattern (TaskList/, RunMonitor/, Report/).

## Component Responsibilities

| Component | Responsibility | Integration with Existing |
|-----------|---------------|--------------------------|
| ImportService | Parse Excel, validate rows, generate preview, create tasks | Uses TaskRepository.create() |
| ExcelParser | Low-level openpyxl row parsing + field extraction | None (pure utility) |
| BatchExecutionManager | Semaphore-controlled parallel agent execution + progress tracking | Reuses run_agent_background() |
| Batch (model) | Batch metadata (name, status, created_at, total/progress counts) | References existing Task |
| BatchTaskEntry (model) | Mapping: batch_id -> task_id with per-task status | References Batch + Task |
| batches.py (route) | REST endpoints for import preview, confirm, batch execute | Uses ImportService, BatchManager |
| ImportModal (frontend) | Upload Excel, show preview, confirm import | Uses batches API client |
| BatchDashboard (frontend) | Task selection, start batch, per-task progress | Uses useBatchExecution hook |

## Architectural Patterns

### Pattern 1: Two-Phase Import (Preview then Confirm)

**What:** The Excel upload is split into two API calls: (1) POST /api/import/preview returns parsed data without creating tasks, (2) POST /api/import/confirm creates tasks after user reviews.

**When to use:** Any data import where user validation is important.

**Trade-offs:** Extra API round-trip, but prevents accidental bad imports. Memory cost of holding parsed data temporarily.

**Why this pattern:** QA users need to verify the parsed data before committing. The preview shows exactly which tasks will be created and flags validation errors per-row.

```
POST /api/import/preview   --> { rows: [...], errors: [...], valid_count, error_count }
POST /api/import/confirm   --> { tasks: [...], batch_id }
```

Implementation detail: The preview endpoint stores parsed data in a temporary location (either server-side session cache keyed by a preview_id, or re-parses on confirm). **Recommendation: re-parse on confirm** -- avoids server-side state management and is simpler. Excel files are small (typically <100 rows for test cases), so re-parsing cost is negligible.

### Pattern 2: Semaphore-Based Concurrency Control

**What:** A module-level `asyncio.Semaphore` limits the number of concurrent browser-use agent executions to prevent resource exhaustion.

**When to use:** Any batch operation that launches resource-heavy async tasks.

**Trade-offs:** Tasks wait in queue when semaphore is full, but prevents OOM and SQLite write contention.

**Implementation:**

```python
# backend/core/batch_manager.py

import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

class BatchExecutionManager:
    """Manages parallel execution of batch tasks with resource control."""

    def __init__(self, max_concurrent: int = 2):
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._active_batches: dict[str, dict[str, Any]] = {}  # batch_id -> progress

    async def execute_batch(self, batch_id: str, task_ids: list[str]) -> None:
        """Execute multiple tasks in parallel with semaphore control."""
        self._active_batches[batch_id] = {
            "total": len(task_ids),
            "completed": 0,
            "success": 0,
            "failed": 0,
            "task_status": {tid: "pending" for tid in task_ids},
        }

        async def run_single(task_id: str) -> None:
            async with self._semaphore:
                self._active_batches[batch_id]["task_status"][task_id] = "running"
                try:
                    # Reuse existing run_agent_background with fresh DB session
                    await self._run_task(task_id)
                    self._active_batches[batch_id]["task_status"][task_id] = "success"
                    self._active_batches[batch_id]["success"] += 1
                except Exception as e:
                    logger.error(f"Batch task {task_id} failed: {e}")
                    self._active_batches[batch_id]["task_status"][task_id] = "failed"
                    self._active_batches[batch_id]["failed"] += 1
                finally:
                    self._active_batches[batch_id]["completed"] += 1

        await asyncio.gather(*[run_single(tid) for tid in task_ids])
        # Cleanup after completion
        del self._active_batches[batch_id]
```

**Key design decision: max_concurrent = 2.** Rationale:
- Each browser-use agent consumes 200-500MB RAM (Chromium instance).
- Server has ~2GB available RAM.
- Two concurrent browsers = ~1GB max, leaving headroom for FastAPI, SQLite, OS.
- Can be made configurable via environment variable for future scaling.

### Pattern 3: Polling-Based Batch Progress (NOT SSE)

**What:** Batch progress is fetched via periodic GET polling rather than SSE streaming.

**When to use:** When you have multiple concurrent data streams and need aggregate status.

**Trade-offs:** Higher latency than SSE per-update, but dramatically simpler implementation. No need to multiplex N SSE streams.

**Why NOT SSE for batch progress:**
- SSE is currently per-run (one stream per run_id via EventManager).
- Batch execution runs N agents, each with its own SSE stream.
- Adding a batch-level SSE would require multiplexing N run streams into one batch stream, adding significant complexity.
- For batch progress, polling every 2-3 seconds is sufficient (QA users watch the dashboard, not individual steps).

**Implementation:** `GET /api/batches/{batch_id}/progress` returns:

```json
{
  "batch_id": "abc123",
  "status": "running",
  "total": 10,
  "completed": 3,
  "success": 2,
  "failed": 1,
  "tasks": [
    {"task_id": "t1", "task_name": "Login test", "status": "success", "run_id": "r1"},
    {"task_id": "t2", "task_name": "Create order", "status": "running", "run_id": "r2"},
    {"task_id": "t3", "task_name": "Delete order", "status": "pending"},
    ...
  ]
}
```

**Note:** Individual run monitoring still uses existing SSE streaming. Click on a running task in the batch dashboard -> navigate to RunMonitor page with SSE connection, exactly as it works today.

### Pattern 4: In-Memory Progress with DB Persistence

**What:** Batch progress is tracked in memory (BatchExecutionManager._active_batches) during execution, then persisted to the Batch model when complete.

**When to use:** For high-frequency status updates where DB writes per-update are too expensive.

**Trade-offs:** In-memory state is lost on server restart during batch execution. Acceptable because batch execution is a user-initiated operation -- if server restarts mid-batch, user restarts the batch.

**Why this is acceptable:** The worst case is a batch appears "stuck" after restart. The user can check individual task statuses and re-run failed ones. No data corruption risk because each task creates its own Run independently.

## Data Flow

### Import Flow

```
[User uploads .xlsx]
    |
    v
POST /api/import/preview
    |
    +--> ImportService.parse_excel(file_bytes)
    |       |
    |       +--> validate each row (name required, description required, max_steps range)
    |       +--> return { preview_id, rows: [...parsed], errors: [...per-row] }
    |
    v
[Frontend shows preview table + errors]
    |
    v
POST /api/import/confirm   (body: { preview data / re-upload file, batch_name })
    |
    +--> ImportService.parse_excel(file_bytes)  # re-parse (no server state)
    +--> DB transaction:
    |       create Batch row
    |       for each valid row:
    |           create Task row
    |           create BatchTaskEntry row (batch_id -> task_id)
    |       commit
    |
    v
Response: { batch_id, task_ids, created_count, skipped_count }
```

### Batch Execution Flow

```
[User selects tasks on TaskList page, clicks "Batch Execute"]
    |
    v
POST /api/batches  (body: { task_ids: [...], batch_name: "..." })
    |
    +--> Create Batch row (status: "pending")
    +--> Create BatchTaskEntry rows
    +--> Start background task: BatchExecutionManager.execute_batch()
    |
    v
Response: { batch_id }

[Frontend polls every 2s]
    |
    v
GET /api/batches/{batch_id}/progress
    |
    +--> Read from BatchExecutionManager._active_batches (in-memory)
    |       OR read from DB if batch is complete
    |
    v
[Dashboard updates: progress bar, per-task status cards]

[User clicks on a running task]
    |
    v
Navigate to /runs/{run_id}  (existing RunMonitor with SSE)
```

### State Management (Frontend)

```
useBatchImport (hook)
    state: { step: 'upload'|'preview'|'result', file, preview, errors, importing }

useBatchExecution (hook)
    state: { batchId, progress, pollTimer }
    effect: setInterval(pollProgress, 2000)
    cleanup: clearInterval on unmount or batch complete
```

## Database Schema Changes

### New Tables

```sql
-- Batch: groups multiple tasks for batch operations
CREATE TABLE batches (
    id VARCHAR(8) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    type VARCHAR(20) NOT NULL DEFAULT 'execution',  -- 'import' or 'execution'
    status VARCHAR(20) NOT NULL DEFAULT 'pending',   -- pending, running, completed, failed
    total INTEGER NOT NULL DEFAULT 0,
    completed INTEGER NOT NULL DEFAULT 0,
    success INTEGER NOT NULL DEFAULT 0,
    failed INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at DATETIME
);

-- BatchTaskEntry: many-to-many mapping between batches and tasks
CREATE TABLE batch_task_entries (
    id VARCHAR(8) PRIMARY KEY,
    batch_id VARCHAR(8) NOT NULL REFERENCES batches(id),
    task_id VARCHAR(8) NOT NULL REFERENCES tasks(id),
    run_id VARCHAR(8) REFERENCES runs(id),   -- set when execution starts
    status VARCHAR(20) NOT NULL DEFAULT 'pending',  -- pending, running, success, failed
    error TEXT,                               -- error message if failed
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Why Two Tables Instead of Adding Fields to Task

- A task can belong to multiple batches (import batch A, execution batch B).
- Batch-level metadata (total, completed, progress) should not live on individual tasks.
- Clean separation: Batch owns orchestration, Task owns test definition.
- Matches existing patterns: Run references Task but Task has no run-specific fields.

### Why status and progress fields on Batch model (duplicated from in-memory)

- Batch status and counts are persisted to DB on completion (or interruption).
- This allows querying batch history without the in-memory manager.
- During execution, reads come from in-memory (fast). After execution, reads come from DB (durable).

## Integration Points with Existing Code

### 1. Task Creation (ImportService -> TaskRepository)

ImportService calls `TaskRepository.create()` for each valid row. This is identical to the existing single-task creation flow. No changes to TaskRepository needed.

The import endpoint validates all rows first, then creates tasks in a single transaction:

```python
async def create_batch_tasks(self, rows: list[TaskCreate]) -> list[Task]:
    """Create multiple tasks in a single transaction."""
    tasks = []
    for row_data in rows:
        task = Task(**row_data.model_dump())
        self.session.add(task)
        tasks.append(task)
    await self.session.commit()
    for task in tasks:
        await self.session.refresh(task)
    return tasks
```

**SQLite concurrency concern:** All task creation happens in one transaction. With WAL mode, this blocks other writers briefly but is fast for <100 inserts. Acceptable for a single-user QA tool.

### 2. Task Execution (BatchManager -> run_agent_background)

BatchExecutionManager calls the existing `run_agent_background()` function directly. This function already:
- Creates its own DB session via `async_session()`
- Creates its own AgentService instance
- Handles SSE events via EventManager
- Generates reports via ReportService

**No changes needed to run_agent_background().** The BatchManager wraps each call in a semaphore slot.

**Critical detail:** Each call to run_agent_background creates a separate browser session (line 45-54 of agent_service.py: `browser_session = create_browser_session()`). This is correct for parallel execution -- each task gets its own browser.

### 3. SSE Streaming (Existing EventManager, Unchanged)

Individual run monitoring continues to use the existing EventManager + SSE pattern. The batch dashboard does NOT use SSE -- it polls the batch progress endpoint.

Users can still click into individual runs from the batch dashboard and get the full SSE streaming experience.

### 4. API Router Registration

```python
# In backend/api/main.py, add:
from backend.api.routes import batches
app.include_router(batches.router, prefix="/api")
```

## Scaling Considerations

| Concern | Current (single QA user) | 5 concurrent users | Notes |
|---------|--------------------------|--------------------|-------|
| Browser RAM | 2 instances = 1GB | 2 instances = 1GB | Semaphore is global, shared across all users |
| SQLite writes | WAL mode handles it | May see occasional lock timeouts | Add retry logic on SQLITE_BUSY |
| Import file size | <100 rows typical | <100 rows per user | File size limit: 5MB enforced |
| Batch size | 10-20 tasks | 10-20 tasks per user | No limit needed -- semaphore throttles execution |
| In-memory progress | 1-2 active batches | 5-10 active batches | Trivial memory cost |

### Scaling Priorities

1. **First bottleneck: Browser RAM.** Semaphore with max_concurrent=2 handles this. If server is upgraded, increase via env var.
2. **Second bottleneck: SQLite write contention under parallel execution.** Each parallel agent writes steps to DB. With 2 concurrent agents, this is fine. With more, add retry with backoff on SQLITE_BUSY errors.

## Anti-Patterns

### Anti-Pattern 1: SSE Multiplexing for Batch Progress

**What people do:** Create a single SSE stream that combines events from N concurrent runs into one stream.
**Why it is wrong:** Requires substantial changes to EventManager, complex event routing, and harder-to-debug frontend code. Each run already has its own SSE stream.
**Do this instead:** Use polling for batch-level progress. Users click into individual runs for real-time SSE monitoring.

### Anti-Pattern 2: Server-Side Preview State

**What people do:** Store parsed Excel data in server memory or a temp DB table between preview and confirm.
**Why it is wrong:** Requires state cleanup, session management, and TTL logic. Server restart loses preview state.
**Do this instead:** Re-parse the Excel file on confirm. The file is small (<100 rows) and parsing is fast (<100ms). Send the file again from the frontend (it is already in browser memory).

### Anti-Pattern 3: Per-Step Batch Progress Updates

**What people do:** Update batch progress on every agent step event.
**Why it is wrong:** With 2 concurrent agents each producing steps every few seconds, this creates excessive DB writes on the batch table.
**Do this instead:** Update batch progress only on task completion (success/fail), not per-step. Per-step updates are already handled by the existing SSE + Step persistence.

### Anti-Pattern 4: Creating Tasks Without Validation

**What people do:** Import all rows, mark invalid ones as "draft" with errors.
**Why it is wrong:** Pollutes task list with invalid tasks that can never be executed.
**Do this instead:** Two-phase import -- preview shows all validation errors, confirm only creates valid rows. Invalid rows are reported back with row numbers and error messages so users can fix their Excel.

### Anti-Pattern 5: Long-Running Excel Parsing on Event Loop

**What people do:** Call openpyxl directly in async FastAPI route.
**Why it is wrong:** openpyxl is synchronous and blocks the event loop, preventing SSE heartbeats and other requests.
**Do this instead:** Run openpyxl parsing in a thread executor via `asyncio.to_thread()` or `loop.run_in_executor()`.

## Excel Template Design

### Recommended Template Structure

| Column | Required | Type | Example | Maps To |
|--------|----------|------|---------|---------|
| A: 用例名称 | Yes | text | "销售出库-标准流程" | Task.name |
| B: 步骤描述 | Yes | text | "1. 点击销售管理..." | Task.description |
| C: 目标URL | No | text | "/sales/out" | Task.target_url |
| D: 最大步数 | No | number | 15 | Task.max_steps (default 10) |
| E: 前置条件 | No | text (semicolon-separated) | "login(); get_warehouse()" | Task.preconditions |
| F: 断言配置 | No | text (JSON) | '{"className":"PcAssert",...}' | Task.external_assertions |

**Why this structure:**
- Column A and B are the only required fields (matches existing TaskCreate schema).
- Precondition codes are semicolon-separated to fit in a single cell (frontend TaskFormModal already has a precondition editor -- the import simply splits by semicolon).
- Assertion config as JSON string is consistent with how external_assertions is already stored.
- Optional columns have sensible defaults matching existing Task model defaults.

### Template File

Ship a `data/templates/task_import_template.xlsx` file with:
- Header row with column names
- 2-3 example rows
- Data validation (dropdown for max_steps, input validation hints)
- A "readme" sheet explaining each column

## API Endpoints Design

### Import Endpoints

```
POST /api/import/preview
  Content-Type: multipart/form-data
  Body: file (xlsx)
  Response: {
    rows: [{ row_number, name, description, target_url, max_steps, preconditions, assertions, valid, errors }],
    total_rows: number,
    valid_rows: number,
    error_rows: number
  }

POST /api/import/confirm
  Content-Type: multipart/form-data
  Body: file (xlsx), batch_name (string)
  Response: {
    batch_id: string,
    created_count: number,
    skipped_count: number,
    task_ids: string[]
  }

GET /api/import/template
  Response: xlsx file download
```

### Batch Execution Endpoints

```
POST /api/batches
  Body: { task_ids: string[], batch_name?: string }
  Response: { batch_id: string, status: "pending" }

GET /api/batches
  Response: [{ batch_id, name, status, total, completed, success, failed, created_at }]

GET /api/batches/{batch_id}
  Response: { batch details + task entries }

GET /api/batches/{batch_id}/progress
  Response: { batch status, per-task status, counts }
  (This is the polling endpoint, returns from in-memory if running, DB if complete)

POST /api/batches/{batch_id}/cancel
  Response: { status: "cancelled" }
  (Sets cancelled flag, semaphore-released tasks check flag before starting)
```

## Frontend State Management

### useBatchImport Hook

```typescript
interface BatchImportState {
  step: 'upload' | 'preview' | 'importing' | 'result'
  file: File | null
  preview: PreviewResponse | null
  importing: boolean
  result: ImportConfirmResponse | null
  error: string | null
}

// Hook returns:
{
  state: BatchImportState,
  uploadAndPreview: (file: File) => Promise<void>,
  confirmImport: () => Promise<void>,
  reset: () => void,
}
```

### useBatchExecution Hook

```typescript
interface BatchExecutionState {
  batchId: string | null
  progress: BatchProgress | null
  loading: boolean
  error: string | null
}

// Hook returns:
{
  state: BatchExecutionState,
  startBatch: (taskIds: string[], batchName?: string) => Promise<void>,
  // polling starts automatically when batchId is set, stops on completion/unmount
}
```

### Integration with Existing TaskList

The existing TaskList page already has checkbox selection (`selectedIds`). The batch execution trigger integrates as:

1. Add a "Batch Execute" button to the existing `BatchActions` component (alongside "Batch Delete" and "Batch Set Ready").
2. Clicking "Batch Execute" calls `POST /api/batches` with `selectedIds`.
3. On success, navigate to `/batches/{batch_id}` (new BatchMonitor page).
4. BatchMonitor page uses `useBatchExecution` hook for polling.

## SQLite Concurrency Strategy

### Write Concurrency

| Operation | Concurrency Pattern | Rationale |
|-----------|---------------------|-----------|
| Import (batch task creation) | Single transaction | Fast (<100 inserts), brief lock |
| Batch execution step writes | WAL mode handles concurrent reads, writes are serialized | 2 concurrent agents = 2 writers, WAL handles this |
| Batch progress updates | In-memory, no DB writes during execution | Avoids write contention |
| Batch completion | Single write on batch complete | One-time, fast |

### Read Concurrency

| Operation | Pattern | Rationale |
|-----------|---------|-----------|
| Progress polling | In-memory first, DB fallback | Fastest path for active batches |
| Batch list | Standard DB read | WAL allows concurrent reads |
| Individual run SSE | Existing EventManager | Unchanged |

### Error Recovery for SQLITE_BUSY

Add retry logic to the repository layer for batch operations:

```python
import asyncio
from sqlalchemy.exc import OperationalError

async def with_retry(func, max_retries=3, base_delay=0.1):
    """Retry on SQLITE_BUSY errors with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return await func()
        except OperationalError as e:
            if "locked" in str(e) and attempt < max_retries - 1:
                await asyncio.sleep(base_delay * (2 ** attempt))
            else:
                raise
```

## Build Order (Dependencies)

The implementation must follow this order due to dependencies:

```
Phase 1: Excel Template + Parse (no DB changes)
  1.1 Create Excel template file (data/templates/task_import_template.xlsx)
  1.2 Create ExcelParser utility (openpyxl wrapper)
  1.3 Create ImportService (parse + validate)
  1.4 Add /api/import/preview endpoint
  1.5 Frontend: ImportModal (upload + preview)
  Tests: Unit tests for ExcelParser, ImportService

Phase 2: Batch Task Creation (DB changes needed)
  2.1 Add Batch + BatchTaskEntry models to models.py
  2.2 Add migration in database.py init_db() (ALTER TABLE if not exists)
  2.3 Add batch schemas to schemas.py
  2.4 Add /api/import/confirm endpoint (creates tasks + batch)
  2.5 Frontend: ImportResult component + confirm flow
  Tests: Integration tests for confirm endpoint, DB schema tests

Phase 3: Batch Execution (depends on Phase 2 DB)
  3.1 Create BatchExecutionManager (semaphore + progress tracking)
  3.2 Add batch execution endpoints (POST /api/batches, GET progress)
  3.3 Frontend: BatchExecution dashboard + useBatchExecution hook
  3.4 Integration with TaskList "Batch Execute" button
  3.5 Route / App.tsx: add /batches routes
  Tests: Integration test for batch execution with mocked agent

Phase 4: Polish + Edge Cases
  4.1 Cancel batch execution support
  4.2 Retry failed tasks within a batch
  4.3 Error handling for server restart during batch
  4.4 Template download endpoint
  4.5 E2E test for full import -> batch execute flow
```

## Key Design Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Batch progress: SSE vs polling | Polling (2s interval) | Simpler, no EventManager changes, sufficient for batch-level |
| Individual run monitoring | Existing SSE (unchanged) | Already works, click-through from batch dashboard |
| Preview state | Re-parse on confirm | No server-side state to manage |
| Concurrency control | asyncio.Semaphore (max 2) | Browser RAM constraint, configurable |
| Import validation | Per-row validation in preview | Users see exactly what will import |
| Batch-Task relationship | Many-to-many via BatchTaskEntry | Tasks can be in multiple batches |
| New dependency | openpyxl (add to pyproject.toml) | Standard Python Excel library, sync (use with run_in_executor) |
| Frontend file upload | Standard fetch FormData | No need for special upload library |

## Sources

- Codebase analysis: existing Task/Run/Agent pipeline in backend/
- Existing patterns: EventManager, Repository pattern, useRunStream hook
- SQLite WAL mode documentation: https://www.sqlite.org/wal.html
- FastAPI file upload: https://fastapi.tiangolo.com/tutorial/request-files/
- asyncio.Semaphore: Python standard library documentation
- openpyxl: https://openpyxl.readthedocs.io/ (sync library, use with run_in_executor)

---
*Architecture research for: Excel batch import and parallel execution*
*Researched: 2026-04-08*
