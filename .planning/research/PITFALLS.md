# Domain Pitfalls: Excel Batch Import and Parallel Execution

**Domain:** Adding Excel template design, batch import, and parallel browser execution to an existing AI-driven UI test automation platform (v0.9.0)
**Researched:** 2026-04-08
**Context:** v0.9.0 milestone -- TMPL-01, IMPT-01, BATCH-01
**Confidence:** HIGH (based on direct code analysis, SQLite documentation, browser-use library knowledge, and established web security practices)

## Critical Pitfalls

Mistakes that cause rewrites or major issues.

### Pitfall 1: Parallel Browser Instances Exhausting Server RAM

**What goes wrong:**
Launching multiple browser-use Agent instances in parallel causes the server to run out of memory. Each Chromium instance with a 1920x1080 viewport consumes 200-500MB RAM. The deployment server (121.40.191.49) is a 2-core machine with limited RAM. Running 3-4 agents simultaneously can consume 1-2GB+ and trigger OOM kills, crashing the entire service.

**Why it happens:**
The current `agent_service.py` creates a fresh `BrowserSession` per call to `run_with_streaming()` (line 164: `browser_session = create_browser_session()`). There is no concurrency control or resource semaphore. When batch execution launches N tasks in parallel via `asyncio.gather()`, each one spawns a full Chromium process independently.

The Gunicorn deployment uses 2 workers (deployment-v0.5.0.md), meaning each worker could independently spawn browsers. The total browser count could be 2x the intended parallelism.

**Consequences:**
- Server becomes unresponsive, all in-progress runs fail
- OOM killer terminates the FastAPI worker process
- Gunicorn restarts the worker but all running tasks lose their state
- Database writes for in-progress runs never complete, leaving runs stuck in "running" status

**How to avoid:**
1. Implement a global `asyncio.Semaphore` that limits concurrent browser instances. Default to `max(1, (total_ram_mb - 1024) // 400)`. On the 2-core server, this should be 2 at most.
2. Place the semaphore in a shared module (not per-request) so it is respected across all concurrent batch executions.
3. Queue excess tasks rather than launching them immediately. Show queued status in the UI.
4. Consider using Playwright's `browser.new_context()` from a shared browser instance instead of launching separate browsers per agent. However, browser-use's `BrowserSession` may not support this pattern -- verify before relying on it.
5. Add a health check that refuses new batch executions if memory usage exceeds a threshold (e.g., 80%).

**Warning signs:**
- Server response time degrades during batch execution
- `dmesg` shows OOM killer messages
- Runs stuck in "running" status permanently
- Gunicorn worker restart count increases in `journalctl`

**Phase to address:**
BATCH-01 (batch execution phase) -- must be designed into the execution scheduler from the start, not bolted on later.

**Confidence:** HIGH -- direct code analysis of `agent_service.py` line 164, server specs from deployment-v0.5.0.md, well-documented Chromium memory behavior.

---

### Pitfall 2: SQLite Concurrent Write Locks Under Parallel Runs

**What goes wrong:**
When multiple browser agents execute in parallel, each one writes step data, status updates, and precondition results to SQLite. SQLite's WAL mode allows concurrent reads but still serializes writes. Under parallel load, writes from different agents queue up and eventually hit `SQLITE_BUSY` errors despite `busy_timeout=5000`.

**Why it happens:**
The current codebase creates a new database session per background task (runs.py line 76: `async with async_session() as session`). When 3 agents run in parallel, each holds its own session. Their writes (step inserts, status updates) contend for the single SQLite write lock. Each write operation in `add_step()` (repository.py line 158-174) does `session.add()` + `session.commit()`, which acquires and releases the write lock per step. With 3 agents each writing a step every 2-5 seconds, that is 3-6 write lock acquisitions per 5 seconds. Under normal load this works, but under sustained parallel execution with precondition results, assertion results, and step data all writing simultaneously, contention spikes.

The deployment has Gunicorn with 2 workers. Each worker has its own async engine (`create_async_engine` with `pool_size=5`). This means there are 2 independent connection pools, each with 5 connections. SQLite's WAL mode allows one writer at a time across ALL connections to the same file.

**Consequences:**
- `sqlite3.OperationalError: database is locked` errors in logs
- Steps fail to save, causing incomplete execution records
- Runs may get stuck in "running" status if the final status update fails
- Error recovery is complicated because the original write context is lost

**How to avoid:**
1. Increase `busy_timeout` to 10000ms or higher for batch execution scenarios. The current 5000ms may not be enough under parallel load.
2. Batch step writes: accumulate steps in memory and flush them in a single transaction rather than committing per step. The current `add_step()` commits individually (repository.py line 172: `await self.session.commit()`).
3. Implement a write serializer: route all database writes through a single asyncio task with an internal queue. This eliminates write contention entirely.
4. Consider separating the step write path from the status update path. Steps can be batched (acceptable to lose the last few if the server crashes), but status updates must be reliable.
5. Add retry logic with exponential backoff for `OperationalError` exceptions on write operations during batch execution.

**Warning signs:**
- `database is locked` errors in server logs
- Steps missing from execution records (step_index gaps)
- Runs completing but status remaining "running" in the database
- `busy_timeout` exceeded warnings in SQLite logs

**Phase to address:**
BATCH-01 (batch execution phase) -- the write serialization pattern must be designed before implementing parallel execution. IMPT-01 should use simple sequential writes for batch import (less risk).

**Confidence:** HIGH -- direct code analysis of database.py (pool_size=5, busy_timeout=5000), repository.py (per-step commit pattern), and well-documented SQLite WAL single-writer constraint.

---

### Pitfall 3: Excel Parsing Returns Wrong Data Types Due to Cell Formatting

**What goes wrong:**
openpyxl returns different Python types depending on how the cell was formatted in Excel. A cell that looks like "10" might be the integer `10`, the float `10.0`, or the string `"10"` depending on whether Excel stored it as a number, a formula result, or text. Date cells may return `datetime` objects or serial numbers. This causes silent data corruption when importing to Task fields.

**Why it happens:**
The Task model has strict field types: `name` is `String(200)`, `description` is `Text`, `max_steps` is `Integer`, `target_url` is `String(500)`. When openpyxl reads a cell:
- A number like `10` in the `max_steps` column comes through as `int(10)` -- correct
- But if the user formatted the cell as text, it comes as `str("10")` -- needs casting
- If the user typed `=10` (formula), openpyxl without `data_only=True` returns the string `"=10"`, not the value
- Dates in `preconditions` or `description` columns may become `datetime(2024, 1, 15)` objects that `json.dumps()` serializes differently than expected
- Merged cells return `None` for all but the top-left cell, silently dropping data
- Leading/trailing whitespace is invisible in Excel but causes validation failures (e.g., `" test name "` fails `min_length=1` after trimming but passes before)

**Consequences:**
- Batch import silently creates tasks with wrong `max_steps` values
- Task names with trailing spaces cause matching issues later
- Formula cells cause cryptic import errors ("=10 is not a valid integer")
- Merged cells in header rows cause entire columns to be skipped
- Date objects cause JSON serialization failures when storing preconditions

**How to avoid:**
1. Always load with `data_only=True` to get cached values instead of formula strings.
2. Implement explicit type coercion per column: cast `max_steps` to `int()`, `target_url` to `str()`, etc. Do NOT rely on openpyxl's type inference.
3. Strip whitespace from all string fields before validation.
4. Check for `None` values from merged cells and provide clear error messages like "Row 5, column B: merged cell detected, please unmerge or fill value".
5. Add a `preprocess_row()` function that normalizes types before passing to Pydantic validation.
6. Reject or warn on formula cells by checking `cell.data_type == 'f'`.

**Warning signs:**
- Import succeeds but tasks have `max_steps=0` or `max_steps=None`
- Task names contain leading/trailing spaces
- Import errors reference formula strings like `"=VLOOKUP(...)"` in error messages
- `json.dumps()` fails on cell values that are `datetime` objects

**Phase to address:**
IMPT-01 (Excel import phase) -- type coercion must be built into the parsing layer from the start.

**Confidence:** HIGH -- well-documented openpyxl behavior, directly applicable to the Task model field types in models.py.

---

### Pitfall 4: Malicious Excel File Upload (ZIP Bomb / Macro Attack)

**What goes wrong:**
A maliciously crafted `.xlsx` file (which is actually a ZIP archive) can contain: (a) a ZIP bomb that expands to gigabytes when opened, exhausting disk and RAM; (b) embedded VBA macros in a renamed `.xlsm` file; (c) formula injection payloads (`=CMD|...`) that execute when the data is later exported; (d) XML entity expansion attacks (billion laughs) that exhaust memory during parsing.

**Why it happens:**
The current system has no file upload endpoints at all. When IMPT-01 adds the upload endpoint, it is tempting to accept any file with an `.xlsx` extension and pass it directly to openpyxl. FastAPI's `UploadFile` does not validate file content -- it trusts the `Content-Type` header and filename extension, both of which are client-controlled.

The system runs as `root` on the server (deployment-v0.5.0.md), meaning any file write or code execution vulnerability has maximum privilege.

**Consequences:**
- ZIP bomb crashes the Python worker (OOM or disk full)
- XML entity expansion crashes openpyxl during parse
- Path traversal in filename writes files outside intended directory
- Macro code execution (if file is opened in Excel later for review)
- Formula injection if imported data is ever exported to CSV/Excel

**How to avoid:**
1. **File size limit**: Enforce a hard limit (e.g., 5MB) at the FastAPI endpoint level BEFORE reading the file into memory. Use `file.size` or stream-read with a cap.
2. **Magic bytes validation**: Check the file header. Valid `.xlsx` files start with `PK\x03\x04` (ZIP signature). Reject anything else.
3. **Block macro extensions**: Reject `.xlsm`, `.xlsb`, `.xltm` files explicitly.
4. **Load in read-only mode**: Use `openpyxl.load_workbook(..., read_only=True, data_only=True)`. This prevents formula evaluation and macro execution.
5. **Sandbox parsing**: Parse in a subprocess or with resource limits (`resource.setrlimit`) so a crash does not take down the main worker.
6. **Sanitize filename**: Use `os.path.basename()` and strip special characters. Never use the user-supplied filename directly.
7. **Row/column limits**: Enforce a maximum number of rows (e.g., 500) and columns (e.g., 20) to prevent resource exhaustion from oversized files.

**Warning signs:**
- Upload endpoint takes longer than 5 seconds to respond (parsing huge file)
- Worker process memory spikes after upload
- `openpyxl` throws `ZipBadZipFile` or `xml.parsers.expat.ExpatError`
- Uploaded file extension differs from actual content type

**Phase to address:**
IMPT-01 (Excel import phase) -- security validations must be in the first version of the upload endpoint. Do not defer security.

**Confidence:** HIGH -- standard web security practices, directly applicable to FastAPI + openpyxl stack.

---

### Pitfall 5: Batch Import Partial Failure Leaving Orphaned Tasks

**What goes wrong:**
When importing 50 tasks from an Excel file, if task #37 fails validation (e.g., description too long), the system either: (a) creates tasks 1-36 and stops, leaving the user confused about which tasks were imported; or (b) creates all valid tasks and silently skips invalid ones, making it impossible for the user to know which rows failed.

**Why it happens:**
There is no transaction boundary for batch creation in the current TaskRepository. Each `create()` call commits independently (repository.py line 45: `await self.session.commit()`). If row 37 fails, rows 1-36 are already committed. There is no rollback mechanism and no tracking of which rows succeeded vs failed.

The user expects either all-or-nothing (rollback on first error) or best-effort-with-report (import valid rows, report invalid rows). Neither is the default behavior -- the default is the worst of both worlds: partial import with no clear feedback.

**Consequences:**
- User cannot tell which tasks were imported without manually comparing
- Re-importing the same file creates duplicate tasks for the rows that succeeded
- User has to manually clean up partial imports before retrying
- No way to fix just the failed rows and re-import only those

**How to avoid:**
1. **Validate all rows first**: Parse the entire Excel file, validate every row against Pydantic schemas, collect ALL errors, and only proceed to create tasks if all rows are valid. Show a preview with validation results before creating anything.
2. **Dry-run / preview mode**: Add an import preview endpoint that returns parsed data and validation errors without creating tasks. The frontend shows the preview; user confirms or fixes errors; then the actual import runs.
3. **If partial import is desired**: Track row numbers. Return a detailed response: `{ "created": [task_ids...], "failed": [{"row": 37, "error": "description exceeds max length"}] }`.
4. **Idempotency key**: Allow the user to re-import without duplicates by tracking the import batch (e.g., a `batch_id` field on tasks, or checking for name+description duplicates).
5. **Rollback on threshold**: If more than X% of rows fail, rollback everything. Only commit if the failure rate is below a threshold.

**Warning signs:**
- User reports "I imported 50 tasks but only 36 appeared"
- Same task name appears multiple times (duplicate imports)
- No error messages shown in the UI for failed rows
- Import endpoint returns 200 but fewer tasks created than rows in the file

**Phase to address:**
IMPT-01 (Excel import phase) -- the import flow must be designed as validate-all-then-create, not create-one-by-one.

**Confidence:** HIGH -- directly follows from the current TaskRepository design (per-row commit), Pydantic validation patterns, and standard batch import UX requirements.

---

### Pitfall 6: Browser Agent Cleanup Failure in Parallel Execution

**What goes wrong:**
When running multiple browser agents in parallel, if one agent crashes or times out, its browser process may not be cleaned up properly. Over time, zombie Chromium processes accumulate, consuming memory and file descriptors until the server becomes unusable.

**Why it happens:**
The current `run_with_cleanup()` in agent_service.py (line 426-474) wraps `run_with_streaming()` with try/finally for logging, but the actual browser cleanup is handled by browser-use's `Agent` class internally. If the agent crashes during initialization (before browser launch) or during an unrecoverable Playwright error, the browser process may be orphaned.

In parallel execution, a single `asyncio.gather()` call manages multiple agents. If one agent raises an exception, `gather()` with default behavior cancels remaining tasks. If `gather(return_exceptions=True)` is used instead, the failed agent's browser may not be cleaned up because its finally block runs in an uncertain state.

On the server (running as root), orphaned Chromium processes can accumulate indefinitely because no one is monitoring process counts.

**Consequences:**
- Server memory gradually increases as zombie Chrome processes accumulate
- After several batch executions, no new browser instances can launch (file descriptor limit)
- Eventually requires manual `pkill chromium` or server restart
- Screenshot directories fill with orphaned files from incomplete runs

**How to avoid:**
1. Implement explicit browser process tracking: maintain a registry of launched browser PIDs. On cleanup, verify the process is actually dead.
2. Add a startup health check that kills any orphaned Chromium processes before accepting new batch execution requests.
3. Use `asyncio.timeout()` or `asyncio.wait_for()` with a hard limit per agent run (e.g., 5 minutes for a 10-step task).
4. In the batch execution scheduler, always use `try/finally` per agent, not per batch. Each agent's browser must be cleaned up independently regardless of other agents' status.
5. Add a periodic cleanup task (e.g., every 10 minutes) that scans for and kills orphaned Chromium processes older than a threshold.

**Warning signs:**
- `ps aux | grep chromium` shows processes from completed runs
- Server memory usage does not decrease after batch execution completes
- New agent launches fail with "Failed to launch browser" (too many open files)
- Screenshot directories contain files for runs that show "failed" status

**Phase to address:**
BATCH-01 (batch execution phase) -- browser lifecycle management must be explicit, not delegated to browser-use's implicit cleanup.

**Confidence:** HIGH -- based on direct code analysis of `run_with_cleanup()` (agent_service.py), browser-use Agent lifecycle patterns, and well-known Chromium zombie process issues.

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Sequential batch import (create one by one, no transaction) | Simple implementation, matches current `TaskRepository.create()` pattern | Partial failures leave inconsistent state, hard to retry | Never for IMPT-01 -- must use validate-all-then-create |
| No row limit on Excel import | Users can import as many tasks as they want | Large files crash the server, timeout the request | Never -- hard limit at 200-500 rows |
| Reuse existing `create_task` endpoint for batch | No new backend code, frontend loops through rows | N+1 API calls, no transactional guarantees, slow for large batches | Never -- dedicated batch endpoint required |
| Skip file type validation on upload | Faster to implement | Security vulnerability, server crashes on malformed files | Never -- must validate magic bytes |
| Use `asyncio.gather()` without semaphore for parallel execution | Simple parallelism, no queue management code | Server crashes under load, no backpressure | Never -- must use semaphore or task queue |
| Store import errors in frontend state only | No backend changes needed | Errors lost on page refresh, no audit trail | Only for preview phase; actual import must persist errors |
| Use `data_only=False` in openpyxl | Sees formulas in error messages (helpful for debugging) | Returns formula strings instead of values, breaks data import | Never for production import; only for debug tooling |

## Integration Gotchas

Common mistakes when connecting to external services/libraries.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| openpyxl + Excel dates | Assuming `cell.value` returns string for date-formatted cells | Check `isinstance(cell.value, datetime)` and format explicitly with `.strftime()` |
| openpyxl + merged cells | Reading merged cell range returns `None` for non-anchor cells | Check `ws.merged_cells.ranges`, resolve anchor cell, reject merged cells in data rows |
| openpyxl + number formats | Trusting `cell.value` type matches the visual appearance | Use explicit type coercion per column, check `cell.number_format` for ambiguous cases |
| browser-use + parallel agents | Creating N independent `BrowserSession` instances in `asyncio.gather()` | Use semaphore to limit concurrency, share browser instance across agents if possible |
| aiosqlite + parallel writes | Each parallel task creates its own session and commits independently | Serialize writes through a single queue or use batch commits |
| FastAPI `UploadFile` | Trusting `file.content_type` or `file.filename` for validation | Validate magic bytes, sanitize filename, enforce size limits independently |
| Pydantic validation on imported data | Passing raw openpyxl cell values directly to Pydantic models | Preprocess: strip whitespace, coerce types, handle `None` from empty cells before validation |

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Per-step SQLite commits during parallel execution | Step saves take 50-500ms, "database is locked" errors | Batch step writes or use write serializer | 2+ parallel agents with frequent step callbacks |
| Loading entire Excel file into memory | Server memory spikes, OOM on large files | Use `read_only=True` in openpyxl, stream rows | Files over 5MB or 1000+ rows |
| Creating browser instances per task in batch | RAM exhaustion, long startup time per task | Reuse browser contexts, limit concurrency with semaphore | 3+ parallel tasks on 2-core server |
| No timeout on batch execution | Some runs hang forever, blocking the queue | Per-run timeout, overall batch timeout | Any scale -- single hanging run blocks the queue |
| Returning all import errors as a single string | Frontend cannot display structured error feedback, user confused | Return structured error list with row numbers and field names | First time user encounters an error |
| No pagination on import preview | 200-row preview payload is large, slow to render | Paginate preview results, show first 20 rows with "show more" | 100+ rows in a single import |

## Security Mistakes

Domain-specific security issues beyond general web security.

| Mistake | Risk | Prevention |
|---------|------|------------|
| Accepting file upload without magic byte check | Attacker uploads executable renamed to `.xlsx`, server processes it | Check first 4 bytes are `PK\x03\x04` (ZIP signature for xlsx) |
| No file size limit on upload endpoint | ZIP bomb or huge file crashes worker process | Enforce 5MB limit at endpoint level, check size before parsing |
| Using user-supplied filename for disk storage | Path traversal attack writes files outside intended directory | Generate server-side filename (UUID-based), never use user input for path |
| Loading Excel with `data_only=False` | Formula strings could contain injection payloads | Always use `data_only=True` to get cached values only |
| Allowing any cell content without sanitization | Formula injection (`=CMD|...`) in cell values could execute later | Strip or prefix dangerous characters (`=`, `+`, `-`, `@`) in cell values |
| No rate limiting on import endpoint | Repeated imports flood server with file processing | Rate limit to 5 imports per minute per client |
| Running as root on server with file upload | Any vulnerability gives attacker full system access | Create dedicated user for the service, restrict file write permissions |

## UX Pitfalls

Common user experience mistakes in this domain.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Template with no sample data row | QA users guess at format, get validation errors on first import | Include 2-3 example rows with realistic data (Chinese test case names, real ERP URLs) |
| Template column headers in English/abbreviated | QA users (non-technical) do not understand "tc_name", "max_steps", "assertions" | Use Chinese headers with descriptions: "用例名称 (必填)", "最大步数 (默认10)" |
| No data validation in the Excel template | Users enter invalid data, only discover on import | Use Excel data validation dropdowns for constrained fields (e.g., assertion type) |
| Error messages reference row/column indices | "Row 5, Col 3 error" requires counting cells manually | Show the actual cell content in error: "Row 5, '最大步数' column: value 'abc' is not a valid number" |
| All-or-nothing import with no error preview | User imports 50 tasks, one fails, all are lost | Preview mode: parse all rows, show errors, let user fix and retry |
| No "download template" button | Users create their own Excel from scratch, format mismatch | Provide a pre-formatted `.xlsx` template with locked header row, data validation, and instructions sheet |
| Template uses multiple sheets for different data | QA users get confused about which sheet to fill | Single sheet, flat table format. Put instructions in a separate "说明" tab, not mixed with data |
| No progress indicator during import | User clicks import, nothing happens for 5 seconds, clicks again (duplicate) | Show upload progress bar, parsing progress, then results. Disable button during processing |
| Batch execution shows no individual status | All tasks show "running" or "completed" as a group | Per-task status indicators: queued, running, success, failed, with individual error messages |

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Excel import**: Often missing merged cell handling -- verify by importing a file with merged header cells
- [ ] **Excel import**: Often missing empty row handling -- verify by importing a file with blank rows between data rows
- [ ] **Excel import**: Often missing Unicode handling -- verify by importing a file with Chinese characters, emoji, and special punctuation in all fields
- [ ] **Excel import**: Often missing whitespace trimming -- verify by importing a file with leading/trailing spaces in task names
- [ ] **Template download**: Often missing data validation rules -- verify by opening template in Excel and checking dropdowns and input restrictions
- [ ] **Batch execution**: Often missing cleanup on server restart -- verify by killing the server mid-batch and checking for zombie processes on restart
- [ ] **Batch execution**: Often missing per-task error isolation -- verify by running a batch where one task has invalid preconditions; confirm other tasks still execute
- [ ] **Batch execution UI**: Often missing "stop all" functionality -- verify that stopping a batch execution cancels all queued/running tasks, not just the current one
- [ ] **Import preview**: Often missing display of precondition code -- verify that multi-line Python code in a cell renders correctly in the preview
- [ ] **Import error reporting**: Often missing the distinction between "row-level error" (bad data) and "system error" (server issue) -- verify error messages clearly differentiate

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Server OOM from parallel browsers | HIGH | 1. `pkill -f chromium` to free RAM. 2. Check `database.db` for runs stuck in "running" status. 3. Update stuck runs to "failed". 4. Reduce parallelism limit before restarting. |
| SQLite database locked errors | MEDIUM | 1. Check if WAL file exists alongside database.db. 2. Stop all workers. 3. Run `sqlite3 database.db "PRAGMA wal_checkpoint(TRUNCATE)"`. 4. Restart with higher busy_timeout. |
| Partial import with orphaned tasks | MEDIUM | 1. Query tasks by creation timestamp matching the import time. 2. Show user the list of imported tasks. 3. Provide "delete batch" option using the import batch_id. 4. User fixes Excel and re-imports. |
| Zombie Chromium processes | LOW | 1. `ps aux | grep chromium` to identify PIDs. 2. `pkill -f chromium` or kill individual PIDs. 3. Add periodic cleanup cron job. |
| Excel parsing returns wrong types | LOW | 1. Delete incorrectly imported tasks by batch_id. 2. Fix type coercion in parser. 3. Re-import the file. |
| Import file contains formula injection | LOW | 1. Import with sanitization enabled. 2. Verify cell values in imported tasks do not start with `=`, `+`, `-`, `@`. 3. If already imported with raw values, sanitize through a database update. |

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Parallel browser RAM exhaustion | BATCH-01 design phase | Load test: launch max parallel agents, monitor `free -m` during execution, verify no OOM |
| SQLite write lock contention | BATCH-01 design phase | Integration test: run 3 agents in parallel, verify no "database is locked" errors in logs |
| Excel type coercion errors | IMPT-01 implementation | Unit test: import Excel file with mixed types (number as text, formula, date, merged cells) and verify correct coercion |
| Malicious file upload | IMPT-01 implementation | Security test: upload `.xlsm`, oversized file, renamed `.zip`, verify rejection with clear error |
| Batch partial failure | IMPT-01 design phase | Integration test: import file with 1 invalid row, verify all-or-nothing or clear partial results |
| Browser zombie processes | BATCH-01 implementation | Stress test: kill agent mid-execution, verify browser process is cleaned up within 30 seconds |
| Template usability | TMPL-01 design phase | User test: give template to a QA person, observe if they can fill it without instructions |
| Import preview UX | IMPT-01 implementation | Manual test: import file with errors at rows 3, 7, 15, verify all errors are shown with row numbers |
| Batch execution status UI | BATCH-01 implementation | E2E test: launch batch of 5 tasks, verify each shows independent status in UI |

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| TMPL-01: Template column design | Over-complex template confuses QA users | Start with minimal columns (name + description + steps), add optional columns iteratively |
| TMPL-01: Template format | Using `.xls` instead of `.xlsx` or mixing formats | Enforce `.xlsx` only, document this clearly in the template download UI |
| IMPT-01: File upload endpoint | No size limit, server crashes on large file | Set 5MB limit, validate before parsing |
| IMPT-01: Excel parsing | Merged cells, formulas, empty rows cause silent data loss | Preprocess: detect and reject merged cells, use `data_only=True`, skip empty rows |
| IMPT-01: Batch validation | Validating one row at a time instead of all rows first | Parse all rows, validate all, report all errors before any database writes |
| IMPT-01: Import response | Returning only "success" without details of what was created | Return full list of created task IDs and names, plus any validation errors |
| BATCH-01: Execution scheduler | No concurrency limit, server crashes | Implement semaphore, default to 2 concurrent agents |
| BATCH-01: Browser lifecycle | Agents crash but browsers stay alive | Track browser PIDs, clean up in finally block, periodic cleanup cron |
| BATCH-01: Status tracking | UI shows batch as "running" even when individual tasks are done | Per-task SSE events, batch-level summary event |
| BATCH-01: Error isolation | One task failure crashes the entire batch | Per-task try/except, failed task marks itself as "failed", others continue |

## Sources

- Direct code analysis: `backend/db/models.py`, `backend/db/repository.py`, `backend/db/database.py`, `backend/core/agent_service.py`, `backend/api/routes/runs.py`, `backend/api/routes/tasks.py`
- Deployment configuration: `.planning/PROJECT.md`, `memory/deployment-v0.5.0.md` (2-core server, 2 Gunicorn workers, SQLite WAL with busy_timeout=5000)
- openpyxl documentation: cell data types, `data_only` parameter, `read_only` mode, merged cell behavior
- SQLite documentation: WAL mode single-writer constraint, `busy_timeout`, `SQLITE_BUSY` error handling
- FastAPI documentation: `UploadFile` security considerations, file size limits
- Chromium/Playwright: memory usage patterns (~200-500MB per instance with headless mode)
- browser-use library: `BrowserSession` lifecycle, `Agent` cleanup patterns
- Playwright: `browser.new_context()` for context reuse, resource management patterns

---
*Pitfalls research for: v0.9.0 Excel batch import and parallel execution features*
*Researched: 2026-04-08*
