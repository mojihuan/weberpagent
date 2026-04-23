# Domain Pitfalls

**Domain:** Adding Playwright code verification, execution, and task management UI integration to existing aiDriveUITest platform (v0.10.4)
**Researched:** 2026-04-23
**Context:** v0.10.4 milestone -- Playwright code execution from web UI, code viewer component, task status state machine extension, task list "code" column
**Confidence:** HIGH (based on direct code analysis of `self_healing_runner.py`, `code_generator.py`, `runs.py`, `database.py` migration patterns, frontend TaskRow/StatusBadge components, and verified external sources on subprocess cleanup and path traversal)

## Critical Pitfalls

Mistakes that cause rewrites or major issues.

---

### Pitfall 1: Orphaned Playwright/Chrome Processes from Subprocess pytest

**What goes wrong:** When a user clicks "Run Code" from the web UI, the backend spawns a subprocess to run `pytest` on the generated Playwright test file. If the subprocess times out, the test hangs, or the user navigates away, the Playwright-launched Chrome browser process (and its renderer/GPU child processes) become zombie processes that consume memory indefinitely.

**Why it happens:** The existing `SelfHealingRunner` uses `asyncio.to_thread(subprocess.run, ...)` with a `timeout=PYTEST_TIMEOUT_SECONDS` (120s). When the timeout fires, `subprocess.run` raises `TimeoutExpired`, but it does NOT kill the child process tree. Playwright spawns Chrome as a separate child process. When only the parent pytest process is terminated, Chrome processes become orphaned. This is a [known issue with pytest-timeout](https://github.com/pytest-dev/pytest-timeout/issues/159) and has been [observed in production Playwright deployments](https://github.com/windmill-labs/windmill/issues/6048).

The existing `SelfHealingRunner._cleanup()` only deletes `.storage_state.json` and `conftest.py` files -- it does NOT clean up browser processes.

**Consequences:**
- Server memory exhaustion after multiple "Run Code" clicks (2GB deployment server)
- Port conflicts when new Playwright instances try to launch on occupied debug ports
- Zombie Chrome processes accumulate until server becomes unresponsive
- 3-4 orphaned Chrome instances (each ~200-400MB) can exhaust the deployment server's RAM
- [Playwright Python zombie threads](https://github.com/microsoft/playwright-python/issues/2397) are a known issue in containerized/server environments

**Prevention:**
- Use `subprocess.Popen` with `start_new_session=True` instead of `subprocess.run`, enabling process group tracking
- Kill the entire process group on timeout: `os.killpg(os.getpgid(proc.pid), signal.SIGKILL)`
- Add a global `_active_code_runs` dict (same pattern as `_active_batches` in `batch_execution.py`) to track running subprocesses and enable cleanup on shutdown
- Limit concurrent code runs with a dedicated `asyncio.Semaphore(1)` for single-server deployment
- Register FastAPI shutdown event handler to kill any remaining subprocesses
- Consider reusing the existing `SelfHealingRunner` infrastructure rather than building a parallel execution path

**Detection:**
- Log subprocess PID at start, verify process termination in `finally` block
- Monitor Chrome process count: `pgrep -c chrome` or `pgrep -c chromium` before/after runs
- Add a health-check endpoint that warns when zombie count exceeds threshold

---

### Pitfall 2: Path Traversal in Code File Serving Endpoint

**What goes wrong:** The new "View Code" endpoint serves generated `.py` files from the `outputs/` directory. If the endpoint accepts a file path or run ID without proper validation, an attacker (or buggy client) could request `../../../etc/passwd` or `../../backend/config/settings.py` and read sensitive configuration including API keys.

**Why it happens:** FastAPI's `FileResponse` does not prevent path traversal by itself. The existing screenshot endpoint (`/runs/{run_id}/screenshots/{step_index}`) is safe because `step_index` is an integer, but a code file endpoint will accept string-based identifiers.

The existing `run.generated_code_path` stores an absolute file path (e.g., `/root/project/weberpagent/outputs/abc12345/generated/test_abc12345.py`). If the endpoint uses this path directly from the database without validation, and the database value was somehow tampered with (or if the endpoint accepts a raw path parameter), files outside the intended directory can be served.

**Consequences:**
- Exposure of `DASHSCOPE_API_KEY` and other secrets in `.env` or settings files
- Exposure of `database.db` containing all test data and user information
- Full source code access including authentication logic and API keys
- [CVE-2025-55526](https://www.sentinelone.com/vulnerability-database/cve-2025-55526/) demonstrates this exact vulnerability pattern in a FastAPI application

**Prevention:**
- Never accept raw file paths as API parameters. Accept only `run_id` and resolve the path server-side from the database (`run.generated_code_path`)
- Validate the resolved path is within the allowed directory: `Path(code_path).resolve().is_relative_to(OUTPUTS_DIR.resolve())`
- Use the same pattern as the existing screenshot endpoint: look up the run, get the stored path, verify it exists, then serve
- Reject any path containing `..` components after normalization
- Only serve files with `.py` extension as an additional safeguard
- Return `Content-Type: text/plain; charset=utf-8` to prevent browser execution

**Detection:**
- Unit test with path traversal payloads: `../../../etc/passwd`, `..%2F..%2F`, null byte injection (`%00`)
- Integration test: verify the endpoint returns 404 for paths outside `outputs/`
- Security test: request the endpoint with a run_id that has a path pointing to `/etc/passwd` (requires database tampering)

---

### Pitfall 3: Task Status State Machine Extension Breaking Existing Data

**What goes wrong:** The milestone requires adding a "success" status to tasks (STATUS-01). Currently, `Task.status` only allows `"draft"` and `"ready"`. The validation is enforced in multiple places with strict matching. Changing the status enum without updating all consumers breaks existing functionality.

**Why it happens:** The status field is validated at multiple layers:
- `backend/db/schemas.py` line 33: `TaskUpdate.status` has regex `^(draft|ready)$`
- `frontend/src/types/index.ts` line 11: `status: 'draft' | 'ready'`
- `TaskRow.tsx` passes status to `StatusBadge` which may not handle unknown values
- SQLite has no ENUM constraint; validation is purely application-level
- The existing `init_db()` migration pattern in `database.py` (lines 44-89) uses `ALTER TABLE ADD COLUMN` with defaults

More critically, "success" conflates two different concepts:
- **Task editorial state**: draft (incomplete definition) / ready (ready to execute)
- **Task execution outcome**: success / failed (result of running the task)

Adding "success" to Task.status means a task that was executed successfully is no longer "ready" for re-execution. This creates UX confusion: if a user edits a "successful" task, does it revert to "draft"? What if they just want to re-run it?

**Consequences:**
- Existing tasks cannot be updated if the new status is not in the regex allowlist (`TaskUpdate` rejects with 400)
- Frontend TypeScript compilation errors or runtime crashes when `StatusBadge` receives an unknown status string
- Existing task filtering by status breaks (queries expecting only draft/ready get unexpected results)
- Semantic confusion: task is "successful" but cannot be re-run without changing status back to "ready"

**Prevention:**
- Consider whether "success" belongs on `Task` at all. Better options:
  - **Option A (recommended):** Derive task success from its latest `Run.status`. Add a computed `latest_run_status` field on the task list response (subquery: `SELECT status FROM runs WHERE task_id = ? ORDER BY created_at DESC LIMIT 1`). The Task model stays unchanged (draft/ready only).
  - **Option B:** Add a separate `latest_outcome` field on Task, updated on run completion. Keeps editorial state and execution outcome separate.
  - **Option C:** If "success" must go on Task.status, update ALL validation points: regex, TypeScript type, StatusBadge component, and add the column migration to `init_db()`.
- If Option C is chosen:
  - Update `TaskUpdate` regex to `^(draft|ready|success)$`
  - Update TypeScript `Task` interface to include `'success'`
  - Ensure `StatusBadge` handles the new value with appropriate styling
  - The "success" status should be set ONLY by the system after code verification, not by user input
  - Add clear transition rules: editing a "success" task reverts it to "draft"; re-running reverts to "ready"

**Detection:**
- Test that existing task CRUD operations still work after schema changes
- Test that the frontend renders all status values without TypeScript errors or crashes
- Test that draft/ready filtering in the task list still works correctly
- Test that a "successful" task can be re-edited and re-run

---

### Pitfall 4: Concurrent Code Execution Resource Exhaustion

**What goes wrong:** Multiple users (or the same user in multiple tabs) can click "Run Code" simultaneously. Each click spawns a subprocess pytest process which launches a Playwright browser. On the 2GB deployment server, 2+ concurrent Playwright runs can exhaust memory and crash the server or cause all runs to fail with OOM.

**Why it happens:** The existing `SelfHealingRunner` already runs subprocess pytest during the post-execution pipeline, but it runs in the background after an agent execution completes. The new "Run Code" button is user-initiated and can be triggered multiple times rapidly. The existing `_active_batches` Semaphore pattern (max 2 concurrency) exists for batch runs but does not cover this new code execution path.

The [`asyncio.Semaphore` may not properly gate subprocess creation](https://stackoverflow.com/questions/72198249/asyncio-semaphore2-does-not-limit-amount-of-subprocesses-to-2) because subprocess spawning is not inherently async -- a thread pool is used (`asyncio.to_thread`), and the semaphore is released before the subprocess completes.

**Consequences:**
- Server crash due to OOM (2GB RAM, each Chrome ~300MB, 2 concurrent = 600MB just for browsers)
- All in-progress runs fail when the server becomes unresponsive
- SQLite corruption risk if write is interrupted during OOM kill
- Chrome processes become zombies on crash, preventing recovery

**Prevention:**
- Create a dedicated `_active_code_runs` module-level dict similar to `batch_execution._active_batches`
- Use an `asyncio.Semaphore(1)` to limit concurrent code executions to 1 on the deployment server
- Hold the semaphore for the ENTIRE subprocess lifetime (acquire before spawn, release in finally after process group killed)
- Return HTTP 409 Conflict if a code run is already in progress
- Debounce the "Run Code" button on the frontend: disable during execution, show spinner
- Show execution status in the UI so users know when a run is in progress

**Detection:**
- Integration test: fire 3 simultaneous "Run Code" requests, verify only 1 succeeds and others get 409
- Monitor memory usage during code runs on the deployment server
- Test that killing a run cleans up all Chrome subprocesses

---

### Pitfall 5: XSS via Code Content in Code Viewer

**What goes wrong:** Generated Playwright code is displayed in a read-only code viewer. The generated code may contain string literals from the ERP system's DOM (page titles, error messages, form values). If any of these contain `<script>` tags and the viewer uses `dangerouslySetInnerHTML` or similar unsafe rendering, the browser executes injected scripts.

**Why it happens:** The `PlaywrightCodeGenerator` produces code that includes string values from the agent's interaction with the ERP system. For example, `page.expect_inner_text()` assertions may contain arbitrary HTML from the page. If the frontend renders this code as HTML rather than text, XSS occurs.

**Consequences:**
- Session hijacking if XSS steals browser tokens
- Unauthorized API calls on behalf of the user
- Phishing attacks via injected UI elements in the code panel
- Single-user local tool mitigates severity, but the deployment server is internet-accessible (121.40.191.49)

**Prevention:**
- Use `react-syntax-highlighter` with the Prism backend for code display -- it [renders text nodes, not raw HTML](https://github.com/react-syntax-highlighter/react-syntax-highlighter)
- NEVER use `dangerouslySetInnerHTML` for code content
- If building a custom viewer, always use `textContent` or `React.createElement` not `innerHTML`
- Return code content as `Content-Type: text/plain; charset=utf-8` from the API, not as HTML
- Alternatively, wrap code in a JSON response field (the existing pattern in the codebase uses JSON responses)

**Detection:**
- Test with code content containing `<script>alert('xss')</script>` in string literals
- Test with DOM assertion content that includes HTML tags like `<img onerror=alert(1)>`
- Verify the browser console shows no script execution

---

## Moderate Pitfalls

### Pitfall 6: Large Generated Files Freezing the Code Viewer

**What goes wrong:** Generated Playwright test files for complex tasks with 30+ steps can be several hundred lines. `react-syntax-highlighter` [renders all lines as individual React elements upfront](https://github.com/react-syntax-highlighter/react-syntax-highlighter/issues/545), causing DOM bloat and UI freezes for files over ~500 lines.

**Why it happens:** The library does not virtualize by default. Each line becomes a separate DOM node with nested spans for syntax highlighting. For a 300-line file, this creates 300+ React element trees.

**Prevention:**
- Use `react-syntax-highlighter` with the `LightAsync` build for reduced bundle size and lazy language loading
- Cap displayed code at a reasonable length (e.g., 500 lines) with a "truncated, download full file" indicator
- For v0.10.4 scope, generated test files are typically 50-150 lines (based on analysis of `code_generator.py` output patterns), so plain `react-syntax-highlighter` with Prism should be sufficient
- If files regularly exceed 200 lines, consider the [virtualized renderer](https://github.com/conorhastings/react-syntax-highlighter-virtualized-renderer) or a simple `<pre>` with line numbers
- Add a loading state while code content is being fetched and parsed

**Detection:**
- Test with a 500-line generated file and measure render time in browser DevTools
- Check Performance tab for layout thrashing or long tasks

---

### Pitfall 7: File Not Found After Disk Cleanup or Healing Runner Cleanup

**What goes wrong:** The "View Code" button reads from `generated_code_path` stored in the Run database record. If the file has been deleted (disk cleanup, manual deletion, or the `SelfHealingRunner._cleanup()` method), the endpoint returns 500 instead of a user-friendly error.

**Why it happens:** The `generated_code_path` column is set during code generation (Phase 82, line 490 in `runs.py`), but there is no guarantee the file still exists when the user clicks "View Code" minutes or hours later. The `SelfHealingRunner._cleanup()` method deletes `.storage_state.json` and `conftest.py` (NOT the test file), but other cleanup processes or manual operations could delete the generated code.

**Prevention:**
- Always check `Path(code_path).exists()` before attempting to serve
- Return 404 with a clear message: "Generated code file not found. The code may have been cleaned up."
- Add a `has_code` boolean to the Task/Run response so the frontend can hide or disable the "View Code" button when code is unavailable
- Derive `has_code` from: `generated_code_path IS NOT NULL AND healing_status NOT IN ('pending', 'healing')`
- Do NOT delete the generated `.py` file in `_cleanup()` -- only delete `.storage_state.json` and `conftest.py`

**Detection:**
- Test by deleting the generated file manually and then requesting the view endpoint
- Verify the frontend handles 404 gracefully with a user-facing message
- Verify the "View Code" button is hidden/disabled when `has_code` is false

---

### Pitfall 8: Race Condition Between Code Generation and Code Viewing

**What goes wrong:** A user creates a run, and while the agent is still executing (code not yet generated), they see the task in the list and click "View Code". The endpoint finds no generated code and returns an error, confusing the user.

**Why it happens:** Code generation happens at the end of the run pipeline (after agent execution, after assertions, after report generation -- lines 479-493 in `runs.py`). The UI may show the task with a "code" indicator before code is actually generated. The `healing_status` field transitions from "pending" to "healing" to "passed"/"failed"/"skipped", providing a signal for code availability.

**Prevention:**
- The "has code" indicator should only show when `healing_status` is in a terminal state: `passed`, `failed`, or `skipped` (not `pending` or `healing`)
- Disable the "View Code" button in the UI until code is confirmed available
- Add a tooltip explaining why the button is disabled: "Code generation in progress" or "No code generated for this task"
- The task list endpoint should expose `healing_status` so the frontend can make this determination

**Detection:**
- Create a run and immediately try to view code before generation completes
- Verify the UI does not show the code button until healing_status reaches a terminal state

---

### Pitfall 9: SQLite Write Contention During Concurrent Code Execution

**What goes wrong:** When code execution is triggered from the web UI, it needs to update run status in SQLite. If this happens concurrently with the existing agent execution pipeline (which also writes to SQLite), the database may lock or timeout.

**Why it happens:** SQLite uses file-level locking. The `busy_timeout` is set to 30 seconds (line 26 in `database.py`), but concurrent writes from multiple asyncio tasks can still cause `OperationalError: database is locked`. The existing batch execution uses `Semaphore(2)` to limit concurrent runs, but the new code execution path is independent.

**Prevention:**
- Reuse the existing database session pattern: create a new session per operation, commit promptly
- Avoid long-running transactions that hold write locks during the subprocess run
- The code execution endpoint should update status quickly (single UPDATE statement) and not hold a session open during the subprocess
- Use the same `async_session` factory to ensure proper connection pool behavior
- Update status BEFORE spawning the subprocess (pending -> running) and AFTER it completes (running -> success/failed)

**Detection:**
- Run agent execution and code execution simultaneously and monitor for `OperationalError: database is locked`
- Check SQLite WAL file size during concurrent operations

---

### Pitfall 10: Subprocess stdout/stderr Buffer Overflow

**What goes wrong:** When running pytest via subprocess, if the test produces excessive output (verbose mode with many steps, large assertion errors), `subprocess.run` with `capture_output=True` buffers everything in memory. On the 2GB server, a runaway test producing megabytes of output can cause OOM.

**Why it happens:** The existing `SelfHealingRunner` uses `capture_output=True` and `text=True` (line 188-199), which reads all stdout/stderr into Python strings. A Playwright test in verbose mode (`-v` flag is used) against a complex ERP page can produce substantial output.

**Prevention:**
- Limit captured output to a reasonable size (e.g., 100KB)
- Truncate output if it exceeds the limit, keeping the tail (most recent traceback)
- The existing `_truncate_error()` method (line 361) handles this for display, but the raw subprocess capture can still grow unbounded before truncation
- Consider using `-q` flag for user-triggered code runs instead of `-v` to reduce output volume
- Use `subprocess.Popen` with `PIPE` and read incrementally to enforce size limits

**Detection:**
- Run a test that produces 1MB+ of output and monitor memory usage
- Verify truncated output still contains the relevant error information (traceback tail)

---

## Minor Pitfalls

### Pitfall 11: Frontend "Code" Column Performance in Task List (N+1 Queries)

**What goes wrong:** Adding a "has code" column to the task list requires knowing whether each task has generated code. Naively querying runs for each task to check `generated_code_path` causes N+1 queries.

**Why it happens:** The task list endpoint (`GET /tasks`) currently does not join with runs. Adding code availability information requires either a join or a subquery.

**Prevention:**
- Add a subquery in the task list repository method: `EXISTS (SELECT 1 FROM runs WHERE task_id = tasks.id AND generated_code_path IS NOT NULL AND healing_status NOT IN ('pending', 'healing'))`
- Or add a `latest_run_healing_status` field to the task list response, derived from a join
- Frontend should not make additional per-task requests to determine code availability

**Detection:**
- Load task list with 50+ tasks and measure API response time
- Enable SQLAlchemy echo logging and check for N+1 query patterns

---

### Pitfall 12: Unicode/Encoding Issues in Generated Code Content

**What goes wrong:** Task names contain Chinese characters. The `_sanitize_function_name()` method preserves Unicode identifiers. File paths and code content contain mixed Chinese/ASCII. If encoding is not handled consistently, the code viewer shows garbled text.

**Why it happens:** The generated files are written with `encoding="utf-8"` (line 121 in `code_generator.py`), but the HTTP response may not specify the correct charset.

**Prevention:**
- Ensure the code content API response sets `Content-Type: text/plain; charset=utf-8`
- If wrapping in JSON, use `ensure_ascii=False` (the existing codebase pattern)
- Test with task names containing Chinese characters

**Detection:**
- View code for a task with a Chinese name and verify characters render correctly in the browser

---

### Pitfall 13: Browser State Leakage Between Code Runs

**What goes wrong:** When running Playwright code from the web UI, the test may reuse `storage_state` from a previous run. If the login token has expired, the test fails with authentication errors. If a different user's state is used, the test operates with wrong permissions.

**Why it happens:** The existing `SelfHealingRunner` generates a fresh `storage_state` for each run using `_get_storage_state_for_role()`. The new code execution endpoint must do the same. If it accidentally reuses a state file from a previous run, the behavior is unpredictable.

**Prevention:**
- Always generate fresh `storage_state` for code execution using the same `_get_storage_state_for_role()` function
- Verify the token is valid before starting the subprocess
- Clean up `storage_state` file after execution completes
- Use unique temporary directories for each code run to prevent file collisions

**Detection:**
- Run code with an expired token and verify a clear error message is returned
- Run code for role "main" then immediately for "special" and verify no state leakage

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Backend: Code serving endpoint | Path traversal (Pitfall 2) | Resolve path from DB, validate within `outputs/`, use `is_relative_to()` |
| Backend: Code execution endpoint | Orphaned processes (Pitfall 1) | Process group kill via `os.killpg`, Semaphore(1), `_active_code_runs` tracking |
| Backend: Task status extension | State machine breakage (Pitfall 3) | Consider deriving from Run.status; update ALL validation layers if adding to Task |
| Frontend: Code viewer component | XSS (Pitfall 5), large files (Pitfall 6) | Use react-syntax-highlighter (safe by default), cap file size |
| Frontend: "Run Code" button | Concurrent execution (Pitfall 4) | Debounce, disable during run, Semaphore(1), HTTP 409 |
| Frontend: Task list "code" column | N+1 queries (Pitfall 11) | Subquery or join, no per-task API calls |
| Database: Schema migration | NULL/wrong defaults (Pitfall 3) | Follow existing `init_db()` pattern in `database.py` |
| Integration: Code generation timing | Race condition (Pitfall 8) | Use `healing_status` as availability gate |
| Integration: Error handling | File not found (Pitfall 7) | Check file exists before serving, return 404 |
| Deployment: Memory limits | Subprocess OOM (Pitfall 4, 10) | Semaphore(1), output truncation, process group kill |

---

## Architectural Decision Flag: Task "success" Status

The most impactful decision is whether "success" should be a `Task.status` value or derived from `Run.status`. The current system has a clean separation:

- **Task** = test definition (status: draft/ready = editorial state)
- **Run** = execution instance (status: pending/running/success/failed/stopped = execution outcome)

Adding "success" to `Task.status` conflates editorial state with execution outcome. Consider:
- **Option A (recommended):** Derive task success from latest Run.status. Add a computed field on the task list response. Task model stays draft/ready only.
- **Option B:** Add a separate `latest_outcome` field on Task, updated on run completion. Clean separation, but requires migration and update logic.
- **Option C:** Add "success" to Task.status. Simplest query, but creates semantic confusion (what happens when re-running a "successful" task?).

If Option C is chosen, define clear transition rules: editing a "success" task reverts to "draft"; re-running reverts to "ready".

---

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Orphaned Chrome processes | LOW | `pkill -f chromium` or `pkill -f chrome`; add process group kill to finally block |
| Path traversal serving wrong file | LOW | Fix path validation, deploy fix, audit access logs for exploitation |
| Task status state machine break | MEDIUM | Add missing validation, update TypeScript types, redeploy. Existing data with "success" status may need manual cleanup if Option C is chosen. |
| OOM from concurrent runs | LOW | Add Semaphore(1), deploy fix. Recovery: kill orphaned processes, restart server. |
| XSS in code viewer | LOW | Switch to react-syntax-highlighter or ensure text-only rendering. No data migration needed. |
| File not found on View Code | LOW | Add file existence check, return 404. No data migration. |
| Race condition (code not ready) | LOW | Use healing_status gate, disable button. No data migration. |

---

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Process cleanup:** Often missing the process group kill -- verify that Chrome subprocesses are killed on timeout, not just the pytest parent process
- [ ] **Path validation:** Often missing the `is_relative_to()` check -- verify that path traversal payloads return 404, not 200
- [ ] **Status validation consistency:** Often missing the TypeScript type update -- verify frontend compiles without errors after adding "success" status
- [ ] **Concurrency limit:** Often missing the Semaphore -- verify that concurrent "Run Code" clicks return 409 instead of spawning multiple processes
- [ ] **Code availability check:** Often missing the `healing_status` gate -- verify the "View Code" button is disabled while code is being generated
- [ ] **N+1 query prevention:** Often missing the subquery/join -- verify task list API does not make per-task queries for code availability
- [ ] **Browser state freshness:** Often missing the fresh storage_state generation -- verify each code run gets a new token, not a cached one
- [ ] **Output truncation:** Often missing the stdout/stderr size limit -- verify that a verbose test does not cause memory issues

---

## Sources

- [pytest-timeout subprocess leak issue](https://github.com/pytest-dev/pytest-timeout/issues/159) -- HIGH confidence, official GitHub issue
- [Playwright zombie processes in production](https://github.com/windmill-labs/windmill/issues/6048) -- HIGH confidence, verified production issue
- [Playwright Python zombie thread issue](https://github.com/microsoft/playwright-python/issues/2397) -- HIGH confidence, official repo
- [asyncio.Semaphore does not limit subprocesses](https://stackoverflow.com/questions/72198249/asyncio-semaphore2-does-not-limit-amount-of-subprocesses-to-2) -- MEDIUM confidence, SO verified
- [CPython ResourceWarning: subprocess is still running](https://github.com/python/cpython/issues/109490) -- HIGH confidence, official CPython issue
- [FastAPI path traversal CVE-2025-55526](https://www.sentinelone.com/vulnerability-database/cve-2025-55526/) -- HIGH confidence, CVE entry
- [Path traversal prevention guide](https://directorytraversalattack.hashnode.dev/directory-traversal-attack) -- MEDIUM confidence, community guide
- [react-syntax-highlighter large file issue](https://github.com/react-syntax-highlighter/react-syntax-highlighter/issues/545) -- HIGH confidence, official GitHub issue
- [react-syntax-highlighter virtualized renderer](https://github.com/conorhastings/react-syntax-highlighter-virtualized-renderer) -- HIGH confidence, verified solution
- [SQLite ALTER TABLE limitations](https://stackoverflow.com/questions/9935593/sqlite3-change-column-default-value) -- HIGH confidence, official SQLite docs
- [Playwright in production memory issues](https://medium.com/@onurmaciit/8gb-was-a-lie-playwright-in-production-c2bdbe4429d6) -- MEDIUM confidence, production experience report
- Direct code analysis: `backend/core/self_healing_runner.py` (subprocess execution, cleanup), `backend/core/code_generator.py` (code generation), `backend/api/routes/runs.py` (execution pipeline), `backend/db/database.py` (migration pattern), `backend/db/models.py` (schema), `backend/db/schemas.py` (validation), `frontend/src/types/index.ts` (TypeScript types), `frontend/src/components/TaskList/TaskRow.tsx` (UI component)

---
*Pitfalls research for: v0.10.4 Playwright code verification and task management UI integration*
*Researched: 2026-04-23*
