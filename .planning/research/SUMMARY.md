# Project Research Summary

**Project:** aiDriveUITest v0.9.0 -- Excel Batch Import and Parallel Execution
**Domain:** AI-driven UI test automation -- batch test case management and execution
**Researched:** 2026-04-08
**Confidence:** HIGH

## Executive Summary

aiDriveUITest is an existing AI-driven UI test automation platform where QA testers write test cases in natural language, an AI agent executes them in a browser, and reports are generated automatically. The v0.9.0 milestone adds three capabilities: Excel template design for test case configuration, batch import with a parse/validate/preview workflow, and batch parallel execution of selected tasks with concurrency control. This is a feature-rich extension of a working single-task pipeline, not a greenfield build.

The recommended approach is deliberately minimal on new dependencies. Only openpyxl (already installed at 3.1.5) is needed for Excel read/write, FastAPI's built-in UploadFile handles file uploads, and Python stdlib asyncio.Semaphore plus TaskGroup provide concurrency control. The architecture introduces two new database tables (batches, batch_task_entries) and splits the work into three tightly-scoped phases: template and import first, then batch execution, then polish. A two-phase import pattern (preview then confirm) prevents bad data from entering the system, and polling-based batch progress avoids the complexity of SSE multiplexing.

The dominant risk is server resource exhaustion. Each headless Chromium instance consumes 200-500MB RAM, and the deployment server (121.40.191.49) is resource-constrained. The semaphore must default to 2 concurrent browsers with a hard cap at 4. SQLite write lock contention under parallel agent execution is the second critical risk, mitigated by in-memory progress tracking during execution and retry logic with exponential backoff. Excel parsing type coercion (numbers-as-strings, formula cells, merged cells) is the third major pitfall and must be handled with explicit per-column type normalization from day one.

## Key Findings

### Recommended Stack

Zero new packages need to be installed. All required dependencies already exist in the project venv. The stack is intentionally lean -- openpyxl for Excel, stdlib asyncio for concurrency, and FastAPI UploadFile for file handling.

**Core technologies:**
- **openpyxl 3.1.5** (installed): Excel template generation and import parsing -- supports both read and write, cell styling, and data validation rules. Already used in the codebase (`webseleniumerp/use_case/export.py`).
- **asyncio.Semaphore + TaskGroup** (stdlib): Concurrency control for parallel browser execution -- no external dependency, Python 3.11 provides structured concurrency via TaskGroup.
- **FastAPI UploadFile** (installed): File upload handling -- `python-multipart 0.0.22` already installed as a transitive dependency of FastAPI 0.135.1.
- **Native HTML file input + Tailwind CSS**: Frontend file upload -- zero npm dependencies, matches existing component patterns.

### Expected Features

**Must have (table stakes):**
- Excel template download with styled headers, example rows, and data validation dropdowns
- Excel file upload with `.xlsx` validation and 5MB size limit
- Row-level data validation against existing TaskCreate schema (name required, description required, max_steps 1-100)
- Preview before import showing valid/invalid rows with per-row error messages
- Atomic batch task creation in a single transaction
- Batch task selection using existing TaskTable checkbox mechanism
- Batch execution endpoint with semaphore-controlled parallelism (default 2 concurrent)
- Per-task status tracking during batch execution (pending/running/success/failed)

**Should have (competitive):**
- Import error report download (annotated Excel for offline fixing)
- Pipe-delimited assertion format as simpler alternative to JSON
- Configurable concurrency limit with frontend slider
- Batch execution summary with aggregate stats

**Defer (v2+):**
- Real-time SSE multiplexing for batch progress (use polling for now)
- Excel export of existing tasks (import-only for v0.9.0)
- Scheduled batch execution (cron-like nightly runs)
- Browser instance reuse between tasks (session contamination risk)

### Architecture Approach

The architecture extends the existing Task -> Run -> Agent pipeline with two new service classes (ImportService, BatchExecutionManager) and two new database tables (batches, batch_task_entries). The design follows four key patterns: two-phase import (preview then confirm with re-parse on confirm), semaphore-based concurrency control, polling-based batch progress (not SSE), and in-memory progress tracking persisted to DB only on completion.

**Major components:**
1. **ImportService** (new) -- Parses Excel via openpyxl, validates rows against TaskCreate schema, returns preview with per-row valid/error status. Re-parses on confirm to avoid server-side state.
2. **BatchExecutionManager** (new) -- Manages parallel agent execution with asyncio.Semaphore, tracks in-memory progress per batch, wraps existing run_agent_background() per task.
3. **Batch + BatchTaskEntry** (new DB models) -- Many-to-many relationship between batches and tasks. Batch holds aggregate status/counts. BatchTaskEntry holds per-task status within a batch.
4. **ImportModal** (new frontend) -- Three-step wizard: upload file, preview parsed data with validation indicators, confirm import.
5. **BatchDashboard** (new frontend) -- Per-task status grid with polling every 2 seconds, click-through to individual RunMonitor for real-time SSE.

### Critical Pitfalls

1. **Parallel browser instances exhausting server RAM** -- Each Chromium instance uses 200-500MB. Semaphore must default to 2, hard-cap at 4. Must be designed into BatchExecutionManager from the start.
2. **SQLite concurrent write locks under parallel runs** -- WAL mode serializes writes. Increase busy_timeout, batch step writes, add retry with exponential backoff on SQLITE_BUSY errors.
3. **Excel parsing type coercion errors** -- openpyxl returns varying Python types depending on cell formatting. Must use `data_only=True`, explicit per-column type coercion, whitespace stripping, and merged cell detection.
4. **Malicious Excel file upload** -- ZIP bombs, macro attacks, formula injection. Must validate magic bytes (PK header), enforce size limit, use `read_only=True`, sanitize filenames.
5. **Batch import partial failure leaving orphaned tasks** -- Validate ALL rows before any database writes. Return structured errors with row numbers. Do not create tasks one-by-one with per-row commits.

## Implications for Roadmap

Based on research, the suggested phase structure follows the dependency chain: template defines the column contract, import depends on that contract, execution depends on imported tasks.

### Phase 1: Template Design + Excel Parser

**Rationale:** The template defines the column names, types, and order that both the parser and the import service depend on. Building this first establishes the contract that downstream phases consume.
**Delivers:** Template download endpoint, ExcelParser utility with type coercion, unit-tested against edge cases.
**Addresses:** TMPL-01, IMPT-01 (parsing foundation)
**Avoids:** Pitfall 3 (type coercion errors) -- type normalization built into parser from day one. Pitfall 4 (malicious upload) -- file validation in upload handler.

### Phase 2: Import Workflow (Preview + Confirm)

**Rationale:** With the parser validated, build the two-phase import flow. Requires database schema changes (Batch, BatchTaskEntry tables) and new API endpoints.
**Delivers:** Upload endpoint, preview endpoint returning per-row validation, confirm endpoint with atomic task creation, frontend ImportModal with upload/preview/result steps.
**Addresses:** IMPT-01, IMPT-02, IMPT-03
**Uses:** ExcelParser from Phase 1, existing TaskRepository.create(), openpyxl, FastAPI UploadFile
**Avoids:** Pitfall 5 (partial import) -- validate-all-then-create pattern. Anti-pattern 2 (server-side preview state) -- re-parse on confirm.

### Phase 3: Batch Execution Engine

**Rationale:** With tasks importable, build the parallel execution engine. This is the highest-risk phase due to browser resource consumption and SQLite write contention.
**Delivers:** BatchExecutionManager with semaphore control, batch execution API endpoints, batch progress polling endpoint, frontend BatchDashboard with per-task status.
**Addresses:** BATCH-01, BATCH-02, BATCH-03
**Uses:** asyncio.Semaphore, asyncio.TaskGroup, existing run_agent_background(), existing EventManager for individual runs
**Avoids:** Pitfall 1 (RAM exhaustion) -- semaphore limits concurrency. Pitfall 2 (SQLite lock contention) -- in-memory progress, retry logic. Pitfall 6 (zombie processes) -- explicit browser cleanup in finally blocks.

### Phase 4: Polish and Edge Cases

**Rationale:** With core import and execution working end-to-end, address remaining UX, error handling, and operational concerns.
**Delivers:** Cancel batch execution, template data validation dropdowns, error report download, concurrency limit configuration, E2E tests for full flow.
**Addresses:** Remaining P2 features, operational safety
**Uses:** All components from previous phases

### Phase Ordering Rationale

- Phase 1 must come first because the template column contract governs everything downstream -- changing column names later requires updating parser, preview, and frontend simultaneously.
- Phase 2 depends on Phase 1 but is independent of Phase 3. Import and execution are separate operations with different lifecycles.
- Phase 3 depends on Phase 2 for database schema (batches table) and the import pipeline that creates tasks to execute.
- Phase 4 is additive polish that does not change core architecture.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3 (Batch Execution):** Complex integration with browser-use Agent lifecycle under parallel load. Need to verify browser-use's cleanup behavior when agents crash concurrently. The current `run_with_cleanup()` pattern may need modification for per-agent isolation in a TaskGroup.
- **Phase 3 (Batch Execution):** SQLite write contention under parallel agent step writes needs load testing. The retry-with-backoff pattern needs empirical tuning for the deployment server.

Phases with standard patterns (skip research-phase):
- **Phase 1 (Template + Parser):** openpyxl read/write patterns are well-documented and already used in the codebase.
- **Phase 2 (Import Workflow):** FastAPI file upload + Pydantic validation is standard territory.
- **Phase 4 (Polish):** Additive features with established implementation patterns.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Verified against installed packages and existing codebase. Zero new dependencies needed. All required packages confirmed in venv. |
| Features | MEDIUM | Feature definitions are clear and grounded in codebase analysis, but competitor analysis relied on training data rather than live web research. QA user assumptions need validation during implementation. |
| Architecture | HIGH | Based on comprehensive codebase analysis of existing Task/Run/Agent pipeline. Patterns (two-phase import, semaphore concurrency, polling progress) are well-established and fit the existing architecture cleanly. |
| Pitfalls | HIGH | All 6 critical pitfalls derived from direct code analysis (agent_service.py, repository.py, database.py, runs.py). Resource constraints confirmed by deployment documentation. |

**Overall confidence:** HIGH

### Gaps to Address

- **browser-use parallel cleanup behavior:** Need to verify that browser-use Agent properly cleans up Chromium processes when exceptions propagate through asyncio.TaskGroup. May require explicit PID tracking as a safety net.
- **SQLite busy_timeout tuning:** The current 5000ms may be insufficient under 2 concurrent agents writing steps. Needs empirical testing during Phase 3 implementation.
- **Excel template QA usability:** The recommended column structure (semicolon-delimited preconditions, JSON assertions) is pragmatic but may confuse non-technical QA testers. Needs user validation before finalizing. Consider the pipe-delimited assertion format as a fallback.
- **FormData upload with existing API client:** The existing `apiClient` sets `Content-Type: application/json` which breaks multipart uploads. The import API call must bypass this client and use raw fetch. This is noted but needs careful implementation to avoid confusion.

## Sources

### Primary (HIGH confidence)
- `pyproject.toml` -- project dependencies, Python 3.11+ requirement
- `backend/db/models.py` -- Task model fields for import mapping
- `backend/db/repository.py` -- per-row commit pattern (source of partial import pitfall)
- `backend/db/database.py` -- pool_size=5, busy_timeout=5000, WAL mode
- `backend/core/agent_service.py` -- run_with_cleanup(), create_browser_session(), browser lifecycle
- `backend/api/routes/runs.py` -- run_agent_background() pattern for reuse
- `backend/api/schemas/index.py` -- TaskCreate schema for validation
- `frontend/src/api/client.ts` -- API client (Content-Type: json issue for FormData)
- `frontend/src/components/TaskList/BatchActions.tsx` -- existing batch action UI
- `webseleniumerp/use_case/export.py` -- existing openpyxl usage pattern
- FastAPI UploadFile documentation -- stable since 0.65+
- openpyxl 3.1 documentation -- Workbook, load_workbook, iter_rows API
- asyncio.Semaphore + TaskGroup -- Python 3.11 stdlib

### Secondary (MEDIUM confidence)
- Test management tool patterns (TestRail, Zephyr, qTest) -- industry standard import workflows
- Browser resource consumption estimates -- ~300-500MB per headless Chromium instance (established benchmark)
- SQLite WAL single-writer constraint -- well-documented behavior

### Tertiary (LOW confidence)
- browser-use Agent cleanup behavior under concurrent TaskGroup exceptions -- needs empirical verification
- QA user preference for Excel template column format -- needs user testing

---
*Research completed: 2026-04-08*
*Ready for roadmap: yes*
