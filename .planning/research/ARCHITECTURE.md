# Architecture Research

**Domain:** Playwright code verification and task management UI integration
**Researched:** 2026-04-23
**Confidence:** HIGH (based on direct codebase analysis of existing patterns)

## Recommended Architecture

### System Overview -- Current + New Components

```
                            FRONTEND (React)
┌─────────────────────────────────────────────────────────────────┐
│  Tasks Page                                                      │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │  TaskTable                                                 │   │
│  │  ┌─────────┬────────┬──────────┬───────┬──────┬────────┐  │   │
│  │  │ check   │ name   │ url      │status │ code │ actions│  │   │
│  │  │ box     │        │          │       │ NEW  │        │  │   │
│  │  └─────────┴────────┴──────────┴───────┴──────┴────────┘  │   │
│  │  TaskRow  ──── "has code" indicator ──── view/run btns     │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                   │
│  CodeViewerModal (NEW)        RunCodeDialog (NEW)                │
│  ┌───────────────────────┐    ┌──────────────────────────┐      │
│  │ react-syntax-highlighter│    │ Execution status display │      │
│  │ Read-only Python code  │    │ stdout/stderr output     │      │
│  │ Line numbers + themes  │    │ Pass/Fail result         │      │
│  └───────────────────────┘    └──────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
         | REST (GET code, POST execute)
         v
┌─────────────────────────────────────────────────────────────────┐
│  BACKEND (FastAPI)                                                │
│                                                                   │
│  routes/runs.py (MODIFY)                                          │
│  ┌──────────────────────────┐  ┌────────────────────────────┐    │
│  │ GET /runs/{id}/code      │  │ POST /runs/{id}/run-code   │    │
│  │ Read file -> return text │  │ subprocess pytest + status │    │
│  └──────────────────────────┘  └────────────────────────────┘    │
│                                                                   │
│  routes/tasks.py (MODIFY)                                         │
│  ┌──────────────────────────┐                                     │
│  │ TaskResponse + has_code  │  Task status: + "success"          │
│  │ from latest run          │                                     │
│  └──────────────────────────┘                                     │
│                                                                   │
│  SelfHealingRunner (EXISTING -- reuse)                            │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ Already handles: pytest subprocess + storage_state        │    │
│  │ + timeout + LLM retry. Reuse for "run code" button.      │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
         |
         v
┌─────────────────────────────────────────────────────────────────┐
│  STORAGE (SQLite + Filesystem)                                    │
│  ┌─────────────┐  ┌──────────────────────────────────────┐      │
│  │ tasks table  │  │ outputs/{run_id}/generated/          │      │
│  │ status +     │  │   test_{run_id}.py                   │      │
│  │ "success"    │  │ outputs/{run_id}/.storage_state.json │      │
│  └─────────────┘  │ outputs/{run_id}/conftest.py          │      │
│                    └──────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### Component Boundaries

| Component | Responsibility | New/Modified | Communicates With |
|-----------|---------------|-------------|-------------------|
| TaskTable | Add "code" column header | MODIFIED | TaskRow |
| TaskRow | Show code indicator + view/run buttons | MODIFIED | CodeViewerModal, RunCodeDialog, API |
| CodeViewerModal | Read-only Python code display | NEW | runs API |
| RunCodeDialog | Trigger code execution, show result | NEW | runs API |
| GET /runs/{id}/code | Serve generated code file content | NEW (endpoint) | Filesystem |
| POST /runs/{id}/run-code | Execute Playwright code via pytest | NEW (endpoint) | SelfHealingRunner |
| TaskResponse schema | Add `has_code` computed field | MODIFIED | runs query |
| Task.status field | Extend to include "success" | MODIFIED | DB, schemas |
| StatusBadge | Add "success" status display | MODIFIED (already exists) | TaskRow |
| SelfHealingRunner | Reuse for single-run code execution | UNCHANGED (reuse) | subprocess |

### Data Flow

#### Flow 1: "Has Code" Indicator in Task List

```
Tasks page loads
    |
    v
GET /tasks (existing)
    |
    v
TaskResponse includes computed has_code: boolean
    |
    v
For each task, check: does latest run have generated_code_path that exists?
    |
    v
TaskRow renders code indicator (icon/badge) based on has_code
```

**Key decision:** `has_code` is computed on the backend from the task's latest run's `generated_code_path` field. This avoids N+1 file existence checks on the frontend.

#### Flow 2: View Code (read-only)

```
User clicks "view code" button on TaskRow
    |
    v
CodeViewerModal opens with run_id from latest run with code
    |
    v
GET /runs/{run_id}/code
    |
    v
Backend reads generated_code_path file from disk
    |
    v
Returns { code: string, language: "python", task_name: string }
    |
    v
CodeViewerModal renders with react-syntax-highlighter
```

#### Flow 3: Run Code (execute)

```
User clicks "run code" button on TaskRow
    |
    v
RunCodeDialog opens, shows confirmation
    |
    v
POST /runs/{run_id}/run-code
    |
    v
Backend reuses SelfHealingRunner.run() with max_iterations=1 (no LLM retry)
    |
    v
Returns { status: "passed"|"failed", stdout: string, stderr: string }
    |
    v
RunCodeDialog shows execution result
    |
    v
If passed -> update task status to "success"
```

#### Flow 4: Task Status State Machine

```
Current:
  draft --> ready    (user sets ready)
  ready --> draft    (user sets draft back)

New (STATUS-01):
  draft --> ready --> success
                    ^         |
                    |         v
                    +- (re-run fails) <-- ready

Rules:
  - "success" set automatically when Playwright code execution passes
  - "success" reverted to "ready" if user re-runs and it fails
  - User cannot manually set "success" -- only system sets it
```

## Integration Points -- Detailed

### Backend Changes

#### 1. New Endpoint: GET /runs/{run_id}/code

Add to `backend/api/routes/runs.py`:

```
Purpose: Return generated Playwright code content for a run
Input: run_id (path param)
Output: { code: str, task_name: str, generated_at: str } or 404
Logic:
  1. Fetch run from DB, get generated_code_path
  2. If no path or file doesn't exist -> 404
  3. Read file content
  4. Return JSON response
```

This follows the existing pattern of `GET /runs/{run_id}/screenshots/{step_index}` which serves file-based content from disk.

#### 2. New Endpoint: POST /runs/{run_id}/run-code

Add to `backend/api/routes/runs.py`:

```
Purpose: Execute the generated Playwright code for a run
Input: run_id (path param)
Output: { status: "passed"|"failed", stdout: str, stderr: str, attempts: int }
Logic:
  1. Fetch run, get generated_code_path + task.login_role
  2. Instantiate SelfHealingRunner (existing class)
  3. Call runner.run() with max_iterations=1 (single attempt, no LLM retry)
  4. Return HealingResult as JSON
  5. If passed -> update task status to "success"
```

**Why reuse SelfHealingRunner instead of writing new subprocess code:**
- SelfHealingRunner already handles: storage_state injection, conftest generation, subprocess timeout, pytest invocation, error capture, cleanup
- Setting max_iterations=1 effectively disables LLM retry while keeping all other infrastructure
- Single responsibility: no code duplication

**Implementation approach for disabling LLM retry:**
Add a `max_iterations` parameter to `SelfHealingRunner.run()` with default 3. When called from the "run code" endpoint, pass `max_iterations=1`. This is a minimal change to the existing class.

#### 3. Modified: TaskResponse Schema

Add computed field `has_code` to `TaskResponse` in `backend/db/schemas.py`:

```python
has_code: bool = False
```

Populate in the list endpoint by checking if the task's latest run has a non-null `generated_code_path`. This requires modifying the `list_tasks` route to join with runs and compute this field.

**Efficient approach:** Add a subquery or hybrid property that checks `exists(select 1 from runs where task_id = :id and generated_code_path is not null)`. Alternatively, load the latest run per task and check in the response serializer. Given the small dataset (typically < 100 tasks), the simpler approach of loading latest runs is acceptable.

#### 4. Modified: Task.status Field

Extend `Task.status` column comment from `# draft, ready` to `# draft, ready, success`. No schema migration needed -- the column is `String(20)` which already supports "success".

Update `TaskUpdate.status` regex pattern from `^(draft|ready)$` to `^(draft|ready|success)$`.

Update frontend `Task` type:
```typescript
status: 'draft' | 'ready' | 'success'
```

#### 5. Modified: Task Status Update After Code Execution

In the `POST /runs/{run_id}/run-code` endpoint, after `SelfHealingRunner` returns with `final_status="passed"`:
- Update `Task.status` to `"success"` via `TaskRepository.update_status()`
- If `final_status="failed"`, revert `Task.status` from `"success"` back to `"ready"` (only if currently "success")

### Frontend Changes

#### 1. New Component: CodeViewerModal

Location: `frontend/src/components/CodeViewer/CodeViewerModal.tsx`

```
Props:
  - open: boolean
  - onClose: () => void
  - runId: string | null

Behavior:
  - When opened with runId, fetches GET /runs/{runId}/code
  - Displays Python code with react-syntax-highlighter (v3 light build)
  - Read-only -- no editing capability
  - Shows task name in header
  - Copy-to-clipboard button

Dependencies: react-syntax-highlighter + @types/react-syntax-highlighter
```

**Why react-syntax-highlighter over prism-react-renderer:**
- The project needs a simple, drop-in code viewer -- not a highly customized rendering pipeline
- react-syntax-highlighter provides built-in line numbers, themes, and language detection out of the box
- The bundle size difference is negligible for this project (single-page app, no SSR concerns)
- Fewer API surface decisions = faster implementation

#### 2. New Component: RunCodeDialog

Location: `frontend/src/components/CodeViewer/RunCodeDialog.tsx`

```
Props:
  - open: boolean
  - onClose: () => void
  - runId: string | null
  - onSuccess: () => void  // callback to refresh task list

Behavior:
  - Shows confirmation dialog before execution
  - On confirm, calls POST /runs/{runId}/run-code
  - Shows loading spinner during execution (pytest can take 30-120s)
  - On complete, shows pass/fail result with stdout/stderr
  - If passed, calls onSuccess to refresh task status

Pattern: Same as existing ConfirmModal + loading state pattern used in BatchExecuteDialog
```

#### 3. Modified: TaskTable

Add "code" column header between "status" and "steps" columns.

#### 4. Modified: TaskRow

Add code indicator cell and view/run buttons:

```
New column cell:
  - If task.has_code: show green code icon
  - If !task.has_code: show gray dash

New buttons (in existing actions column):
  - "View Code" button (eye icon) -- only visible when has_code
  - "Run Code" button (play-code icon) -- only visible when has_code
```

#### 5. Modified: StatusBadge

Already has `success` mapping (line 14): `{ label: '已完成', className: 'bg-green-100 text-green-700' }`. May want to change label to `'成功'` for the new Task.status = "success" semantic, but the visual styling is already correct.

#### 6. New API Functions

Add to `frontend/src/api/runs.ts`:

```typescript
getCode(runId: string): Promise<{ code: string; task_name: string }>
runCode(runId: string): Promise<{ status: string; stdout: string; stderr: string }>
```

#### 7. Modified: Task Type

Update in `frontend/src/types/index.ts`:

```typescript
export interface Task {
  ...
  status: 'draft' | 'ready' | 'success'  // add 'success'
  has_code?: boolean  // NEW computed field
}
```

## Architectural Patterns

### Pattern 1: File-Based Code Storage (Existing)

**What:** Generated Playwright code is stored as `.py` files on disk at `outputs/{run_id}/generated/test_{run_id}.py`. The Run model stores the path in `generated_code_path`.

**Why this works:** Files can be directly executed by pytest subprocess without any serialization/deserialization. The `SelfHealingRunner` writes a `conftest.py` and `.storage_state.json` alongside the test file, which pytest auto-discovers.

**Implication for new features:** The "view code" endpoint reads the file from disk. The "run code" endpoint passes the same file path to `SelfHealingRunner`. No new storage mechanism needed.

### Pattern 2: Subprocess Execution with Timeout (Existing)

**What:** `SelfHealingRunner.run()` executes `uv run pytest {test_file} --headed=false --timeout=60 -v` via `subprocess.run` wrapped in `asyncio.to_thread`, with a 120-second overall timeout.

**Why this works for code execution button:** The same subprocess mechanism serves both the automatic self-healing pipeline and the manual "run code" trigger. The only difference is max_iterations (3 vs 1).

### Pattern 3: Request-Response for Bounded Operations (New)

**What:** The "run code" endpoint uses a standard REST request-response cycle, not BackgroundTasks or SSE.

**Why:** Unlike agent execution (which takes minutes and uses SSE for streaming), code execution is bounded (120s max timeout) and the user expects an immediate result. `SelfHealingRunner.run()` already wraps subprocess in `asyncio.to_thread` so it won't block the event loop. The HTTP request stays open during execution (up to 120s), which is acceptable for this use case.

**Contrast with existing patterns:** The existing `create_run` uses `BackgroundTasks` + SSE because agent execution is unbounded and produces incremental step events. Code execution produces a single binary result (passed/failed), making SSE overkill.

### Pattern 4: Computed Fields on List Endpoints (New)

**What:** The `has_code` field on `TaskResponse` is computed from associated Run data, not stored on the Task model itself.

**Why:** Avoids data duplication and keeps the Task model simple. The relationship is Task -> Runs (1:many), and `has_code` depends on whether any Run has a valid `generated_code_path`. Computed on read rather than stored on write.

**Implementation:** In `list_tasks`, after fetching tasks, batch-fetch the latest run per task and check `generated_code_path`. Use a single query with a window function or subquery to avoid N+1:

```sql
SELECT r.task_id, r.generated_code_path
FROM runs r
WHERE r.id = (
    SELECT r2.id FROM runs r2
    WHERE r2.task_id = r.task_id
    ORDER BY r2.created_at DESC
    LIMIT 1
)
AND r.generated_code_path IS NOT NULL
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Storing Code Content in the Database

**What people do:** Read the generated .py file and store its content as a TEXT column in the Run table.

**Why it's wrong:** Duplication with filesystem, larger DB, SQLite bloat, and the code already exists on disk where pytest can directly execute it.

**Do this instead:** Keep code on disk. Use `generated_code_path` as the reference. The "view code" endpoint reads the file at request time. File size is small (typically 2-20 KB) so disk I/O is negligible.

### Anti-Pattern 2: Creating a New Subprocess Execution Mechanism

**What people do:** Write a new function that calls `subprocess.run(["pytest", ...])` specifically for the "run code" button.

**Why it's wrong:** Duplicates all the infrastructure SelfHealingRunner already handles: storage_state injection, conftest generation, timeout protection, error capture, cleanup.

**Do this instead:** Reuse `SelfHealingRunner` with `max_iterations=1`. Add the parameter to the existing `run()` method.

### Anti-Pattern 3: SSE for Code Execution Results

**What people do:** Use the existing SSE event stream to push code execution results.

**Why it's wrong:** The SSE infrastructure is designed for long-running agent executions with real-time step updates. Code execution is a single request-response cycle (run pytest, return result). SSE adds unnecessary complexity and requires the frontend to subscribe/unsubscribe to a stream.

**Do this instead:** Use a standard REST request-response. POST /runs/{id}/run-code awaits the result and returns it directly.

### Anti-Pattern 4: Adding "success" Status from Agent Execution

**What people do:** Set Task.status = "success" whenever the agent-based run completes successfully.

**Why it's wrong:** The requirement (STATUS-01) is specifically about *Playwright code* execution success, not agent execution success. Agent execution and code execution are different things -- the agent uses browser-use LLM, while code execution runs the generated pytest file. Conflating them creates ambiguity.

**Do this instead:** Only set Task.status = "success" when the generated Playwright pytest code successfully executes via the "run code" mechanism (SelfHealingRunner with max_iterations=1 returns "passed").

### Anti-Pattern 5: has_code Flag Stored on Task Model

**What people do:** Add a `has_code` boolean column to the tasks table, updated whenever code is generated.

**Why it's wrong:** Denormalized data that can drift out of sync. If a run is deleted or the file is manually removed, the flag becomes stale. Adds write-path complexity (must update Task on every code generation).

**Do this instead:** Compute `has_code` on read from the runs relationship. The query cost is negligible for the current dataset size.

## Build Order (Dependency-Aware)

The following build order ensures each phase has its dependencies met:

### Phase 1: Backend Data Layer (no frontend deps)

1. Extend Task.status to support "success" (model comment + schema regex)
2. Add `max_iterations` parameter to `SelfHealingRunner.run()`
3. Add GET /runs/{run_id}/code endpoint
4. Add POST /runs/{run_id}/run-code endpoint
5. Add `has_code` computed field to TaskResponse + list_tasks route

**Tests:** Unit tests for both new endpoints, test that max_iterations=1 skips LLM retry.

### Phase 2: Frontend Infrastructure (depends on Phase 1 APIs)

1. Install react-syntax-highlighter
2. Add API functions: `getCode()`, `runCode()`
3. Update Task type (status union + has_code field)
4. Update StatusBadge if needed

### Phase 3: Frontend UI Components (depends on Phase 2)

1. Build CodeViewerModal
2. Build RunCodeDialog
3. Modify TaskTable (add column header)
4. Modify TaskRow (code indicator + buttons)
5. Wire up Tasks page to host new modals

**Tests:** Component rendering tests for each new component.

### Phase 4: Integration Testing

1. E2E test: task with generated code -> view code -> verify display
2. E2E test: task with generated code -> run code -> verify status update
3. E2E test: task status state machine (draft -> ready -> success -> re-run -> ready)

## Project Structure Changes

### New Files

```
frontend/src/
├── components/
│   └── CodeViewer/
│       ├── CodeViewerModal.tsx    # NEW: read-only Python code display
│       └── RunCodeDialog.tsx      # NEW: execute code confirmation + result
```

### Modified Files

```
backend/
├── api/routes/
│   ├── runs.py                    # MODIFY: add GET /code + POST /run-code endpoints
│   └── tasks.py                   # MODIFY: add has_code to list response
├── core/
│   └── self_healing_runner.py     # MODIFY: add max_iterations param to run()
├── db/
│   ├── models.py                  # MODIFY: Task.status comment -> add "success"
│   ├── schemas.py                 # MODIFY: TaskUpdate regex + TaskResponse has_code
│   └── repository.py              # MODIFY: add task status update method

frontend/src/
├── api/
│   └── runs.ts                    # MODIFY: add getCode(), runCode()
├── components/
│   ├── TaskList/
│   │   ├── TaskTable.tsx          # MODIFY: add "code" column header
│   │   └── TaskRow.tsx            # MODIFY: add code indicator + view/run buttons
│   └── shared/
│       └── StatusBadge.tsx        # MODIFY: update "success" label if needed
├── pages/
│   └── Tasks.tsx                  # MODIFY: add state for CodeViewerModal + RunCodeDialog
└── types/
    └── index.ts                   # MODIFY: add has_code + "success" to Task type
```

### Structure Rationale

- **CodeViewer/ folder** (new): Groups CodeViewerModal and RunCodeDialog together as they share a domain concern (code viewing/execution). Follows the existing pattern of feature-based folders (TaskList/, RunMonitor/, ImportModal/).
- **No new backend services:** SelfHealingRunner is reused, not duplicated. The new endpoints are thin wrappers.
- **Minimal model changes:** Task.status String(20) already fits "success". No migration needed.

## Scalability Considerations

| Concern | Current (single server) | If scaling needed |
|---------|------------------------|-------------------|
| Code file reads | Direct disk I/O, <1ms per file | Already fine for 100s of tasks |
| Concurrent code executions | Single pytest at a time (subprocess) | Add Semaphore like batch execution (existing pattern) |
| Task list has_code computation | SQL subquery per list request | Add cached column on Task if list becomes slow |

**No scaling concerns for current use case.** This is a single-user QA tool with < 1000 tasks.

## Key Design Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Code viewer library | react-syntax-highlighter | Drop-in simple, built-in themes/line numbers, adequate for read-only use |
| Code execution mechanism | Reuse SelfHealingRunner | Already handles all subprocess infrastructure, max_iterations=1 disables retry |
| Run-code API style | REST request-response (not SSE) | Bounded operation (120s max), single result, no streaming needed |
| has_code field | Computed on read from runs | Avoids denormalization, no stale data risk |
| Task "success" status | System-set only (not user) | Matches semantic: success = Playwright code passed |
| New frontend dependency | react-syntax-highlighter | One new npm package, widely used, well-maintained |
| Storage of code content | Filesystem only (not DB) | Files already exist on disk for pytest, no duplication |

## Sources

- Direct codebase analysis: `backend/db/models.py`, `backend/api/routes/runs.py`, `backend/api/routes/tasks.py`, `backend/core/self_healing_runner.py`, `backend/core/code_generator.py`, `backend/db/repository.py`, `backend/db/schemas.py`
- Frontend analysis: `frontend/src/types/index.ts`, `frontend/src/components/TaskList/TaskTable.tsx`, `frontend/src/components/TaskList/TaskRow.tsx`, `frontend/src/components/shared/StatusBadge.tsx`, `frontend/src/api/runs.ts`, `frontend/package.json`
- [FastAPI Custom Response Docs](https://fastapi.tiangolo.com/advanced/custom-response/) -- for serving file content patterns

---
*Architecture research for: Playwright code verification and task management UI integration*
*Researched: 2026-04-23*
