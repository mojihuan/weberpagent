# Feature Research: Excel Batch Import & Parallel Execution (v0.9.0)

**Domain:** AI-driven UI test automation -- Excel template design, batch import, batch execution
**Researched:** 2026-04-08
**Confidence:** MEDIUM (web search limit exhausted; findings based on thorough codebase analysis + established patterns from test management tools and browser automation ecosystem)

## Executive Summary

This document covers three feature areas for v0.9.0: (1) Excel template design for test case configuration, (2) batch import with parse/validate/preview workflow, and (3) batch execution with parallel browser automation. The existing system has a well-structured Task model with 7 fields (name, description, target_url, max_steps, preconditions, assertions, status) and a complete single-task execution pipeline. The challenge is representing complex fields -- preconditions as Python code blocks and assertions as structured JSON configs -- within the flat row/column constraints of a spreadsheet.

The recommended approach: a flat Excel template where each row represents one Task, with preconditions as semicolon-delimited code snippets and assertions as a JSON array string in a single cell. This avoids the complexity of multi-row parsing while keeping the template usable for QA testers.

## Feature Landscape

### Table Stakes (Users Expect These)

Features QA testers assume exist in an "Excel import" workflow. Missing any of these = the import feature feels broken or unusable.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Excel template download** | QA needs a reference format before filling. Every test management tool (TestRail, Zephyr, qTest) provides downloadable templates. | LOW | Generate a pre-filled `.xlsx` with header row + 2 example rows. Use `openpyxl` (Python) to create the file. No new dependency needed (add `openpyxl` to pyproject.toml). |
| **Excel file upload** | Core interaction: click "import" button, select file, submit. Standard file upload UX. | LOW | FastAPI `UploadFile` + multipart form. Frontend: `<input type="file" accept=".xlsx" />` or drag-and-drop zone. Max 10 MB file size. |
| **Header/column validation** | If headers don't match template, parsing fails silently or creates garbage data. QA expects immediate feedback on format errors. | LOW | Compare uploaded sheet headers against expected column names. Return row/col-level error messages. Fail-fast on header mismatch, per-cell validation on data. |
| **Row-level data validation** | Each row must produce a valid TaskCreate payload. Missing required fields (name, description) or invalid values (negative max_steps) must be caught before database writes. | MEDIUM | Validate each row against TaskCreate schema. Required: `name` (non-empty, max 200 chars), `description` (non-empty). Optional: `target_url` (valid URL format if provided), `max_steps` (integer 1-100, default 10), `preconditions` (parseable code string), `assertions` (valid JSON array if provided). |
| **Preview before import** | QA wants to see what tasks will be created before committing. Especially important for batch operations -- one wrong row should not force a redo. | MEDIUM | Parse Excel, validate all rows, return array of `ParsedTask` objects (valid rows) + `RowError` objects (invalid rows). Frontend shows a table preview with green/red row indicators. User clicks "confirm import" to proceed. |
| **Batch task creation** | After preview confirmation, create all validated tasks in the database atomically. | LOW | Call `TaskRepository.create()` in a loop within a single DB transaction. If any insert fails, roll back all. Reuse existing `TaskCreate` schema and `TaskRepository` without modification. |
| **Task list integration** | Imported tasks appear in the existing task list with status "draft". No special treatment. | LOW | Zero code change needed. Existing `TaskRepository.list()` returns all tasks. New tasks with `status="draft"` appear naturally. |
| **Batch task selection** | QA needs to select multiple tasks for execution. Existing TaskTable already has checkbox selection. | LOW | `TaskTable.tsx` already has `selectedIds`, `onSelectAll`, `onToggleSelect` props. `BatchActions.tsx` already has batch action UI (currently "set ready" and "batch delete"). Add "batch execute" button here. |
| **Batch execution launch** | Click "execute" on selected tasks, create a Run for each, start all. | MEDIUM | New endpoint `POST /runs/batch` accepting `{task_ids: string[]}`. Creates N Run records, launches N `run_agent_background` tasks. Returns array of Run IDs. |

### Differentiators (Competitive Advantage)

Features that go beyond basic import/execute. Not expected by QA, but significantly improve usability.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Per-task progress in batch execution** | When running 10 tasks in parallel, QA needs to see which are running/succeeded/failed at a glance, not just a global spinner. | HIGH | Requires a new "batch run" concept with a batch dashboard UI. Each task shows its own status badge. SSE aggregation from multiple run streams. This is the single highest-complexity feature in the milestone. |
| **Import error report download** | When 8 out of 50 rows have errors, QA wants to download an error-highlighted Excel file to fix offline and re-upload. | MEDIUM | Parse results include error annotations per cell. Generate a new `.xlsx` with an "errors" column appended. Re-use openpyxl writer. |
| **Template with dropdown validation** | Excel data validation dropdowns for fields like `max_steps` (1-100), `status` (draft/ready). Prevents data entry errors at the source. | LOW | openpyxl supports `DataValidation` type "list" for cell ranges. Add during template generation. Minimal code, high QA value. |
| **Conditional assertions format** | Allow assertions in a simplified "methodName|headers|data|params" pipe-delimited format that is easier to type in Excel than JSON. Auto-convert to AssertionConfig on import. | MEDIUM | Custom parser: `"attachment_inventory_list_assert|main|main|i=1,j=2"` converts to `{className: "PcAssert", methodName: "...", headers: "main", data: "main", params: {i:1, j:2}}`. Requires knowing the className mapping (hardcode "PcAssert" as default, or add className column). |
| **Concurrent execution limit control** | Let QA set max parallel tasks (e.g., "run 3 at a time" on a 4-core server). Prevents server OOM from launching 10 browser instances simultaneously. | MEDIUM | `asyncio.Semaphore(max_concurrent)` in the batch execution endpoint. Frontend provides a slider/input (default: 2). Server-side hard cap at 4 to protect single-server deployment. |
| **Batch execution summary report** | After batch completes, show aggregate stats: X passed, Y failed, Z errors. One-click to view individual reports. | MEDIUM | New `BatchRun` model with aggregated status. Query all Runs in batch, compute summary. Link to individual Report pages. |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create significant complexity or maintenance burden for this milestone.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| **Multi-row assertions (one task = multiple assertion rows)** | "Assertions should be one per row for readability" -- seems cleaner in Excel. | Requires row-grouping logic: which assertion rows belong to which task? Merged cells? Indentation? This is the #1 source of Excel parsing bugs in test management tools. QA testers frequently break the grouping by sorting/filtering. | Single cell per assertion. Use pipe-delimited format (`method|headers|data|params`) or JSON array for multiple assertions. Less "Excel-native" but parseable and unambiguous. |
| **Excel formula support (e.g., dynamic target_url)** | "Let me use `=CONCATENATE(A1, "/login")` to generate URLs dynamically." | openpyxl in `data_only=True` mode returns formula results only if the file was last saved by Excel (not LibreOffice, not programmatically). Formulas create fragile dependencies between cells. | Keep template flat with literal values. If QA needs URL generation, provide a "base URL" field on the import form and auto-prepend it to relative paths in each row. |
| **CSV import in addition to XLSX** | "CSV is simpler, works everywhere." | CSV has no standard for encoding, line breaks within cells, or type information. Chinese characters in CSV require BOM handling. Edge cases dwarf the "simplicity" benefit. | Support only `.xlsx`. It handles Unicode natively, supports data validation, and is the standard format for every major test management tool's import. |
| **Real-time SSE for batch execution progress** | "I want to watch all 10 tasks execute simultaneously." | Aggregating 10 SSE streams into one frontend connection requires a multiplexer. The current `event_manager` is per-run_id. Scaling to per-batch-id requires a pub/sub architecture change. | Polling-based progress: frontend polls `GET /runs/batch/{batch_id}/status` every 2 seconds. Simpler, works with existing infrastructure. Add SSE per-task later as a v2 enhancement. |
| **Excel export of existing tasks** | "I should be able to export tasks to Excel, edit, and re-import." | Round-trip (export-edit-import) creates an expectation of ID preservation and merge semantics. "Did my edit create a new task or update the existing one?" is a UX trap. | Import-only for v0.9.0. Export can be added as a separate feature in a later milestone. |
| **Parallel browser instance reuse** | "Keep browser instances warm between tasks to speed up batch execution." | Browser-use Agent manages its own browser lifecycle. Reusing browser contexts across different ERP tasks risks session contamination (cookies, localStorage, auth state). The existing `run_with_cleanup` pattern creates fresh sessions per run for good reason. | Create a new browser session per task (current pattern). The overhead is ~2-3 seconds per session launch, acceptable for a tool that runs tasks taking 30-120 seconds each. |
| **Assertion auto-completion in Excel** | "When I type a method name, show me the available options." | This would require an Excel add-in or VBA macro, which is a completely different development surface from the web platform. Massive scope expansion. | Provide a "reference sheet" tab in the template with all available assertion methods and their parameters. QA copies from reference to data sheet. |

## Feature Dependencies

```
TMPL-01: Excel Template Design
    └──generates──> Expected column format (contract for IMPT-01)
                       │
                       v
IMPT-01: Excel Batch Import
    ├──requires──> TMPL-01 (template defines column contract)
    ├──requires──> TaskCreate schema (existing, no change needed)
    ├──requires──> TaskRepository.create() (existing, no change needed)
    └──produces──> N Task records in database
                       │
                       v
BATCH-01: Batch Execution
    ├──requires──> IMPT-01 (tasks must exist before execution)
    ├──requires──> run_agent_background() (existing, no change needed)
    ├──requires──> Concurrent execution limiter (new: asyncio.Semaphore)
    └──produces──> N Run records + N Reports
                       │
                       v
BATCH-UI: Batch Progress Dashboard
    ├──requires──> BATCH-01 (need batch concept to display progress)
    ├──requires──> Run status polling endpoint (new)
    └──produces──> Per-task status grid in frontend
```

### Dependency Notes

- **IMPT-01 requires TMPL-01**: The template defines the column names and order. The parser must match exactly. Design the template first, then build the parser against it. Changing the template later means changing the parser -- keep them versioned together.
- **BATCH-01 requires IMPT-01 (but not strictly)**: Batch execution operates on task IDs, regardless of how tasks were created (manual form OR Excel import). However, the primary use case for batch execution is "import 20 tasks from Excel, then execute all 20." The milestone couples them.
- **BATCH-UI requires BATCH-01**: The progress dashboard needs a "batch run" concept (a group of Runs started together). Without this grouping, the frontend cannot show "batch 1: 5/10 complete."
- **TaskCreate schema is shared**: The Excel parser must produce data that validates against the existing `TaskCreate` Pydantic model. No schema changes needed -- the parser is a pure adapter layer.

## MVP Definition

### Launch With (v0.9.0)

Minimum features to deliver the milestone goal: "QA imports test cases from Excel and batch-executes them."

- [ ] **TMPL-01: Template generation endpoint** (`GET /templates/tasks.xlsx`) -- returns pre-formatted Excel with headers + example rows + data validation dropdowns
- [ ] **TMPL-02: Template download button** in frontend TaskList page
- [ ] **IMPT-01: Upload endpoint** (`POST /tasks/import`) -- accepts `.xlsx`, parses rows, validates, returns preview
- [ ] **IMPT-02: Preview UI** -- modal/table showing parsed tasks with valid/invalid indicators per row
- [ ] **IMPT-03: Confirm import** (`POST /tasks/import/confirm`) -- creates validated tasks in DB
- [ ] **BATCH-01: Batch execute endpoint** (`POST /runs/batch`) -- accepts `{task_ids, max_concurrent}`, creates Runs, launches agents with semaphore
- [ ] **BATCH-02: Batch execute button** in BatchActions component (alongside existing "set ready" and "batch delete")
- [ ] **BATCH-03: Batch progress page** -- shows list of running Runs with per-task status (polling-based)

### Add After Validation (v0.9.x)

Features to add once core import/execute flow works end-to-end.

- [ ] **Error report download** -- generate annotated Excel for failed import rows
- [ ] **Pipe-delimited assertion format** -- simplified assertion syntax in Excel cells
- [ ] **Batch execution summary** -- aggregate stats after all tasks complete
- [ ] **Template versioning** -- track template version in header row, warn on mismatch

### Future Consideration (v1.0+)

Features to defer until batch import/execute is validated with real QA usage.

- [ ] **Real-time SSE for batch progress** -- replace polling with multiplexed SSE stream
- [ ] **Task export to Excel** -- reverse of import
- [ ] **Scheduled batch execution** -- cron-like scheduling for nightly test runs
- [ ] **Batch retry failed tasks** -- one-click re-run only the failed tasks from a batch

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Template download | HIGH | LOW (30 lines backend + 10 lines frontend) | P1 |
| Excel upload + parse | HIGH | MEDIUM (~150 lines parser + validation) | P1 |
| Preview before import | HIGH | MEDIUM (~100 lines new frontend component) | P1 |
| Confirm + batch create | HIGH | LOW (30 lines endpoint, reuse TaskRepository) | P1 |
| Batch execute endpoint | HIGH | MEDIUM (~80 lines, asyncio.Semaphore pattern) | P1 |
| Batch execute button | HIGH | LOW (10 lines in BatchActions.tsx) | P1 |
| Batch progress page | HIGH | HIGH (~200 lines new page + polling logic) | P1 |
| Import error report download | MEDIUM | MEDIUM (~80 lines openpyxl writer) | P2 |
| Pipe-delimited assertions | MEDIUM | MEDIUM (~60 lines parser + documentation) | P2 |
| Dropdown validation in template | LOW | LOW (20 lines in template generator) | P2 |
| Concurrent limit slider | MEDIUM | LOW (10 lines endpoint param + 20 lines frontend) | P2 |
| Batch execution summary | MEDIUM | MEDIUM (~60 lines aggregation query) | P3 |
| Real-time SSE batch progress | LOW | HIGH (event_manager refactor) | P3 |
| Excel export | LOW | MEDIUM (~100 lines writer) | P3 |

## Excel Template Column Design

This section specifies the recommended template columns, derived from the existing `TaskCreate` schema and `TaskForm` fields.

### Recommended Columns

| Column | Header | Type | Required | Default | Notes |
|--------|--------|------|----------|---------|-------|
| A | `任务名称` | text | YES | - | Max 200 chars. Maps to `TaskCreate.name`. |
| B | `任务描述` | text | YES | - | Natural language steps. Maps to `TaskCreate.description`. This is what the AI Agent reads and executes. |
| C | `目标URL` | text | NO | "" | Valid URL. Maps to `TaskCreate.target_url`. Leave blank if preconditions handle navigation. |
| D | `最大步数` | integer | NO | 20 | Range 1-100. Maps to `TaskCreate.max_steps`. Default 20 (not 10 -- batch-imported tasks tend to be more complex). |
| E | `前置条件` | text | NO | - | Semicolon-delimited Python code snippets. Each snippet is one precondition. Example: `context['token'] = login(); context['order_id'] = create_order(token)`. Maps to `TaskCreate.preconditions` as `List[str]`. |
| F | `断言` | text | NO | - | JSON array of AssertionConfig objects. Example: `[{"className":"PcAssert","methodName":"check_total","headers":"main","data":"main","params":{"i":1}}]`. Maps to `TaskCreate.assertions`. |

### Column Rationale

**Why semicolons for preconditions, not separate rows?**
The existing precondition system stores preconditions as a `List[str]` of Python code blocks. Each code block can be multi-line. Using separate rows for preconditions would require a grouping mechanism (e.g., a "task_id" column or merged cells), which is fragile. Instead, semicolons delimit separate precondition code snippets within a single cell. This is a deliberate tradeoff: slightly less readable in Excel, but unambiguous parsing.

**Why JSON for assertions instead of separate columns?**
AssertionConfig has 6 fields (`className`, `methodName`, `headers`, `data`, `params`, `field_params`). Spreading these across 6+ columns would make the template very wide and complex for the common case (most tasks have 0-2 assertions). A single JSON cell keeps the template compact. The v0.9.x pipe-delimited format (`method|headers|data|params`) is a future simplification for QA testers who struggle with JSON syntax.

**Why no "status" column?**
All imported tasks are created as `status="draft"`. The QA workflow is: import -> preview -> confirm -> tasks appear as "draft" -> QA selects and batch-executes. Adding a status column would create confusion about whether "ready" tasks should auto-execute on import.

## Existing Infrastructure Dependencies

| Existing Component | How Batch Features Use It | File | Risk |
|--------------------|--------------------------|------|------|
| `TaskCreate` schema | Parser output must validate against this. No changes needed. | `backend/db/schemas.py:21-23` | LOW -- well-tested Pydantic model |
| `TaskRepository.create()` | Called N times in import confirm endpoint. Transaction wrapping needed. | `backend/db/repository.py:32-47` | LOW -- existing method, add transaction wrapper |
| `run_agent_background()` | Called N times in batch execute. Each call is independent. | `backend/api/routes/runs.py:55-394` | MEDIUM -- each call creates its own browser session, DB session, and SSE event stream. Resource usage scales linearly with N. |
| `event_manager` | Each run gets its own SSE channel via `run_id`. No conflicts. | `backend/core/event_manager.py` | LOW -- existing per-run isolation |
| `AgentService.run_with_cleanup()` | Each batch task uses this independently. No shared state. | `backend/core/agent_service.py:426-474` | LOW -- fresh AgentService per invocation |
| `create_browser_session()` | Called per task. Each creates a headless Chromium instance (~300-500 MB RAM). | `backend/core/agent_service.py:45-54` | HIGH -- memory is the primary constraint for parallel execution |
| `ReportService.generate_report()` | Called per task after completion. Independent. | `backend/core/report_service.py` | LOW -- no shared state |
| `BatchActions.tsx` | Add "batch execute" button alongside existing "set ready" and "batch delete". | `frontend/src/components/TaskList/BatchActions.tsx` | LOW -- additive change |
| `TaskTable.tsx` | Already has checkbox selection. No changes needed. | `frontend/src/components/TaskList/TaskTable.tsx` | LOW -- existing selection mechanism |
| `useTasks.ts` | May need a new `importTasks` function. | `frontend/src/hooks/useTasks.ts` | LOW -- additive hook |

## Browser Resource Constraints for Parallel Execution

The server (121.40.191.49) runs on a single machine. Each headless Chromium instance consumes approximately 300-500 MB RAM. The existing `create_browser_session()` launches a fresh browser per task with no reuse.

| Concurrent Tasks | Estimated RAM (browser only) | Risk Level | Recommendation |
|------------------|------------------------------|------------|----------------|
| 1 | 300-500 MB | LOW | Current behavior, safe |
| 2 | 600-1000 MB | LOW | Recommended default for batch execution |
| 3 | 900-1500 MB | MEDIUM | Acceptable if server has 4+ GB available |
| 4 | 1200-2000 MB | HIGH | Only if server has 8+ GB RAM |
| 5+ | 1500+ MB | CRITICAL | Risk of OOM kill on single-server deployment |

**Recommended hard cap: 2 concurrent tasks by default, 4 maximum.**

The `asyncio.Semaphore` pattern for limiting concurrency:

```python
async def execute_batch(task_ids: list[str], max_concurrent: int = 2):
    semaphore = asyncio.Semaphore(min(max_concurrent, 4))  # hard cap at 4

    async def run_one(task_id: str):
        async with semaphore:
            return await run_agent_background(...)

    results = await asyncio.gather(
        *[run_one(tid) for tid in task_ids],
        return_exceptions=True,
    )
```

## Complexity Assessment

| Feature | Backend LOC (est.) | Frontend LOC (est.) | Files Modified/Created | Testing Difficulty |
|---------|---------------------|----------------------|------------------------|--------------------|
| Template download endpoint | 40-60 | 10 | 1 new route file, 1 new service file | LOW -- unit test generates file, checks headers |
| Excel parser + validator | 120-180 | 0 | 1 new service file | MEDIUM -- need test fixtures with valid/invalid .xlsx files |
| Upload + preview endpoint | 40-60 | 0 | 1 new route file | LOW -- FastAPI TestClient with file upload |
| Preview confirm endpoint | 30-40 | 0 | same route file | LOW -- mock TaskRepository |
| Import UI (upload + preview modal) | 0 | 150-200 | 2-3 new components | MEDIUM -- file upload + table preview interaction |
| Batch execute endpoint | 60-80 | 0 | 1 new route (extend runs.py) | MEDIUM -- need to mock AgentService for parallel test |
| Batch execute button | 0 | 20 | BatchActions.tsx | LOW -- button + API call |
| Batch progress page | 0 | 200-300 | 2-3 new components + new page | HIGH -- polling logic, status aggregation, per-task display |
| New dependency: openpyxl | 1 line | 0 | pyproject.toml | LOW -- well-established library |

**Total estimated:** 290-420 lines backend, 380-530 lines frontend, 8-10 new files.

## Competitor Feature Analysis

| Feature | TestRail | Zephyr (Jira) | Our Approach |
|---------|----------|---------------|--------------|
| Template download | Pre-built XLSX with all fields | CSV template with Jira field mapping | Generated XLSX with Chinese headers matching our schema |
| Complex field handling | Multi-row sections with "step" and "expected" columns | Flat CSV, no complex fields | Single-row-per-task with JSON cells for complex fields |
| Validation feedback | "Errors found: row 3 missing title" | Generic Jira import errors | Row-level validation with cell-specific error messages |
| Preview before import | Yes, shows parsed test cases | No (direct import) | Yes, mandatory preview step with valid/invalid indicators |
| Batch execution | Test runs with multi-case selection | Zephyr Squad execution | Async parallel with configurable concurrency limit |
| Progress tracking | Real-time per-case status in run | Basic pass/fail | Polling-based per-task status grid |

## Sources

- Existing Task model and schemas: `backend/db/models.py`, `backend/db/schemas.py`
- Existing TaskRepository: `backend/db/repository.py`
- Existing run execution pipeline: `backend/api/routes/runs.py`
- Existing AgentService with browser session creation: `backend/core/agent_service.py`
- Existing frontend TaskList with batch selection: `frontend/src/components/TaskList/TaskTable.tsx`, `BatchActions.tsx`
- Existing TaskForm showing all editable fields: `frontend/src/components/TaskModal/TaskForm.tsx`
- Existing TypeScript types: `frontend/src/types/index.ts`
- Project context: `.planning/PROJECT.md`
- Test management tool patterns (TestRail, Zephyr, qTest): industry standard column structures for test case import (training data, MEDIUM confidence)
- openpyxl FastAPI upload pattern: established Python ecosystem pattern (training data, HIGH confidence)
- Browser resource consumption estimates: ~300-500 MB per headless Chromium instance (established benchmark, HIGH confidence)
- asyncio.Semaphore for concurrency control: standard Python async pattern (training data, HIGH confidence)

---
*Feature research for: Excel batch import and parallel execution (v0.9.0)*
*Researched: 2026-04-08*
