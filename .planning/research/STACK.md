# Technology Stack -- v0.9.0 Excel Batch Import and Parallel Execution

**Project:** aiDriveUITest -- Excel Template, Batch Import, Batch Execution
**Researched:** 2026-04-08
**Scope:** New dependencies and patterns for TMPL-01, IMPT-01, BATCH-01 only
**Confidence:** HIGH (verified against installed packages and existing codebase)

## Executive Summary

The three v0.9.0 features (Excel template generation, batch import, parallel execution) require exactly **one new dependency** (`python-multipart` for FastAPI file upload), plus leveraging two packages already installed: `openpyxl` (3.1.5) for Excel read/write and `asyncio.Semaphore` from stdlib for concurrency control. The frontend file upload uses native HTML `<input type="file">` with Tailwind CSS styling -- no new npm packages needed.

This is a low-dependency milestone. The stack is intentionally minimal: openpyxl handles both template generation and import parsing, FastAPI's built-in `UploadFile` covers file upload, and Python's stdlib `asyncio` provides parallel execution primitives. The critical constraint is browser resource consumption during parallel execution -- each Playwright Chromium instance uses ~150-300MB RAM, so the concurrency limit must be configurable and default conservative (2 concurrent browsers on the server).

## Required Stack Changes

### Backend: New Dependencies

| Package | Version | Purpose | Why |
|---------|---------|---------|-----|
| **python-multipart** | 0.0.22 (installed) | FastAPI `UploadFile` support | Required by Starlette/FastAPI for `multipart/form-data` parsing. Already installed as a transitive dependency of FastAPI 0.135.1. No action needed -- just start using `UploadFile` in route handlers. |

**No new packages to add to `pyproject.toml`.**

### Backend: Already Installed (Leverage Existing)

| Package | Version | Purpose | Why This Choice |
|---------|---------|---------|-----------------|
| **openpyxl** | 3.1.5 (installed) | Excel template generation + import parsing | Already in the venv (used by `webseleniumerp/use_case/export.py`). Supports both reading and writing `.xlsx` files, cell styling (headers, validation hints), data validation rules, and streaming row iteration. Handles the full lifecycle: generate template with styled headers -> parse uploaded file -> validate row data -> create tasks. |
| **asyncio.Semaphore** | stdlib (Python 3.11) | Concurrency limiter for parallel browser task execution | Stdlib primitive. No external dependency. Controls how many browser-use Agent instances run simultaneously to prevent RAM exhaustion. |
| **asyncio.TaskGroup** | stdlib (Python 3.11) | Structured concurrent task execution | Python 3.11 feature. Cleaner than `asyncio.gather` for structured concurrency with proper exception propagation. Ensures all parallel runs complete (or fail) as a group. |

### Frontend: New Dependencies

**None.** The file upload UI is built with existing stack:

| What | Approach | Why |
|------|----------|-----|
| **File upload input** | Native `<input type="file" accept=".xlsx">` + Tailwind CSS | No drag-and-drop library needed for QA users uploading one file at a time. Native file input is accessible, tested, and zero-dependency. |
| **Upload progress** | XMLHttpRequest progress event or fetch with readable stream | FastAPI `UploadFile` streams to disk; for files under 10MB (Excel templates), progress indication is optional. Start with a simple loading spinner. |
| **File validation** | Client-side check of `.xlsx` extension + size limit | Reject non-Excel files before upload. Check `file.size < 5MB` client-side. |

## Detailed Technology Decisions

### 1. Excel Handling: openpyxl (not xlsxwriter, not pandas)

**Decision:** Use openpyxl 3.1.5 for both template generation and import parsing.

**Why openpyxl:**
- Already installed in the project venv
- Read AND write support (xlsxwriter is write-only -- cannot parse uploaded files)
- Cell-level styling for template headers (bold, colored backgrounds, borders)
- Data validation rules (dropdown lists for status fields, input length limits)
- Row iteration API is straightforward for parsing: `worksheet.iter_rows(min_row=2, values_only=True)`
- No dependency on pandas (avoid pulling in numpy for a simple read/write use case)

**Why not xlsxwriter:**
- Cannot read existing files -- would need a separate library for parsing uploads
- No advantage for template generation since openpyxl already handles styling

**Why not pandas:**
- Overkill for this use case -- we need cell-level control for styled templates, not DataFrame operations
- `pd.read_excel()` would require openpyxl as the engine anyway (circular dependency argument)
- Cannot write styled headers, merged cells, or data validation rules

**Template generation pattern:**
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border

def generate_template() -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Cases"

    headers = [
        "用例名称", "任务描述", "目标URL",
        "前置条件", "断言配置", "最大步数"
    ]
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font

    # Example row with placeholder data
    ws.append(["示例用例", "点击销售出库菜单", "https://erp.example.com",
               '["login_first()"]', '[{"name":"验证标题","type":"text_exists","expected":"销售出库"}]',
               "15"])

    buffer = io.BytesIO()
    wb.save(buffer)
    return buffer.getvalue()
```

**Import parsing pattern:**
```python
from openpyxl import load_workbook

async def parse_excel(file: UploadFile) -> list[dict]:
    contents = await file.read()
    wb = load_workbook(io.BytesIO(contents), read_only=True)
    ws = wb.active

    tasks = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or not row[0]:  # skip empty rows
            continue
        tasks.append({
            "name": str(row[0]),
            "description": str(row[1]),
            "target_url": str(row[2] or ""),
            "preconditions": json.loads(str(row[3] or "[]")),
            "assertions": json.loads(str(row[4] or "[]")),
            "max_steps": int(row[5] or 10),
        })
    return tasks
```

### 2. File Upload: FastAPI UploadFile

**Decision:** Use FastAPI's built-in `UploadFile` with `python-multipart` (already installed).

**Pattern:**
```python
from fastapi import UploadFile, File, HTTPException

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@router.post("/import")
async def import_tasks(
    file: UploadFile = File(..., description="Excel file (.xlsx)"),
    repo: TaskRepository = Depends(get_task_repo),
):
    # Validate file type
    if not file.filename or not file.filename.endswith(".xlsx"):
        raise HTTPException(400, detail="Only .xlsx files are supported")

    # Validate file size (read with limit)
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(413, detail="File too large (max 5MB)")

    # Parse and validate
    tasks = parse_excel_bytes(contents)

    # Batch create
    created = []
    for task_data in tasks:
        task = await repo.create(TaskCreate(**task_data))
        created.append(task)

    return {"imported": len(created), "tasks": created}
```

**Why UploadFile over `bytes` parameter:**
- Spooled to disk for large files (memory-safe)
- Provides `filename` and `content_type` metadata for validation
- Standard FastAPI pattern with auto-generated OpenAPI docs

**Why not streaming chunks:**
- Excel files for QA test cases are small (under 5MB even with 500 rows)
- Reading entire file into memory for openpyxl parsing is simpler and safe at this scale

### 3. Parallel Execution: asyncio.Semaphore + TaskGroup

**Decision:** Use `asyncio.Semaphore` for concurrency limiting with `asyncio.TaskGroup` for structured execution.

**Critical constraint:** Each browser-use Agent creates a Playwright Chromium browser instance consuming 150-300MB RAM. The server (121.40.191.49) has limited resources. Default concurrency: 2. Maximum configurable: 4.

**Pattern:**
```python
import asyncio

class BatchExecutionService:
    def __init__(self, max_concurrent: int = 2):
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._agent_service = AgentService()

    async def execute_batch(
        self,
        task_ids: list[str],
        on_task_complete: Callable[[str, str], Awaitable[None]],
    ) -> list[BatchRunResult]:
        results: list[BatchRunResult] = []

        async def run_one(task_id: str) -> BatchRunResult:
            async with self._semaphore:
                try:
                    result = await self._agent_service.run_with_cleanup(...)
                    batch_result = BatchRunResult(
                        task_id=task_id, status="success", ...
                    )
                except Exception as e:
                    batch_result = BatchRunResult(
                        task_id=task_id, status="failed", error=str(e)
                    )
                await on_task_complete(task_id, batch_result.status)
                return batch_result

        async with asyncio.TaskGroup() as tg:
            task_futures = [
                tg.create_task(run_one(tid)) for tid in task_ids
            ]

        return [f.result() for f in task_futures]
```

**Why Semaphore, not ThreadPoolExecutor or ProcessPoolExecutor:**
- browser-use Agent is fully async (uses `async_playwright`)
- No CPU-bound work that benefits from threads/processes
- Semaphore is the idiomatic asyncio primitive for this exact pattern
- No extra process overhead or inter-process communication complexity

**Why TaskGroup, not asyncio.gather:**
- Python 3.11+ feature (project uses 3.11.14)
- Structured concurrency: if one task raises an unhandled exception, all others are cancelled cleanly
- No "fire and forget" risk -- all tasks complete or fail as a group
- Better error messages showing which specific task failed

**Why NOT multiple pages in one browser:**
- Each task runs an independent ERP workflow with login state
- Browser contexts share cookies by default in browser-use's `BrowserSession`
- Separate browser instances provide full isolation (login state, navigation, cookies)
- Trade-off: higher RAM usage (2x 200MB = 400MB for 2 concurrent) vs correct isolation

**Configurable concurrency approach:**
- Store `max_concurrent` in a config or environment variable (default: 2)
- Frontend exposes a "concurrency" dropdown when starting batch execution
- Server validates: clamp between 1 and 4 to prevent resource exhaustion

### 4. Frontend File Upload: Native Input + Tailwind

**Decision:** Custom React component using native `<input type="file">` styled with Tailwind CSS.

**Pattern:**
```tsx
// FileUpload.tsx
function FileUpload({ onUpload, isUploading }: FileUploadProps) {
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    // Client-side validation
    if (!file.name.endsWith('.xlsx')) {
      toast.error('Please select an .xlsx file')
      return
    }
    if (file.size > 5 * 1024 * 1024) {
      toast.error('File size must be under 5MB')
      return
    }

    const formData = new FormData()
    formData.append('file', file)
    await onUpload(formData)
  }

  return (
    <label className="cursor-pointer inline-flex items-center gap-2 px-4 h-9
                       rounded-lg bg-blue-500 text-white text-sm font-medium
                       hover:bg-blue-600 transition-colors">
      <Upload className="w-4 h-4" />
      {isUploading ? 'Uploading...' : 'Import Excel'}
      <input type="file" accept=".xlsx" onChange={handleFileChange}
             className="hidden" disabled={isUploading} />
    </label>
  )
}
```

**API client for FormData upload:**
```typescript
// In tasks.ts -- note: must NOT set Content-Type header (browser sets it with boundary)
async importExcel(file: File): Promise<ImportResult> {
  const formData = new FormData()
  formData.append('file', file)

  const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080/api'
  const response = await fetch(`${API_BASE}/tasks/import`, {
    method: 'POST',
    body: formData,
    // DO NOT set Content-Type -- browser handles multipart boundary
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Import failed')
  }

  return response.json()
}
```

**Why native input, not a library (react-dropzone, uppy):**
- Single file upload for QA users -- no drag-and-drop complexity needed
- Zero new npm dependencies
- Native `<input>` is fully accessible (keyboard navigation, screen readers)
- Tailwind styling matches existing Button component pattern
- react-dropzone adds ~15KB for a feature we don't need (multi-file drag)

**Why not antd or shadcn upload component:**
- Project uses custom Tailwind components (see `Button.tsx`), not a UI framework
- Adding a component library for one file upload input is over-engineering

### 5. Template Download: BytesIO Response

**Decision:** Generate template in-memory with openpyxl, return as FastAPI `Response` with `Content-Disposition` header.

**Pattern:**
```python
from fastapi.responses import Response

@router.get("/template")
async def download_template():
    buffer = generate_template()  # Returns BytesIO bytes
    return Response(
        content=buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=test_case_template.xlsx"
        },
    )
```

**Why in-memory, not filesystem:**
- Template is generated fresh each time (always latest format)
- No file cleanup needed
- Small file (under 50KB) -- no memory concern
- Consistent with the project's SQLite-based architecture (no external file storage)

## What NOT to Add

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **pandas** | Overkill for reading 50-200 rows of Excel data. Adds numpy as transitive dependency (~50MB). Cannot write styled templates. | openpyxl direct row iteration |
| **xlsxwriter** | Cannot read files (write-only). Would need openpyxl anyway for import parsing. | openpyxl for both read and write |
| **celery / dramatiq / task queue** | Parallel execution is async IO-bound (browser automation), not CPU-bound. Runs on single server. asyncio.Semaphore is sufficient. | asyncio.Semaphore + TaskGroup |
| **Redis** | No need for distributed task coordination. Single-server deployment. Task status tracked in SQLite. | SQLite status updates |
| **react-dropzone** | Single file upload. Adds ~15KB bundle for features we don't use (drag-and-drop, multi-file). | Native `<input type="file">` with Tailwind |
| **File upload library (uppy, filepond)** | Heavyweight UI components for a simple one-file upload. | Custom component with native input |
| **multer / formidable (Node.js)** | This is a Python backend. FastAPI handles multipart natively. | FastAPI UploadFile |
| **Temporary file storage** | No need to persist uploaded files after parsing. Parse in-memory, create tasks, discard. | BytesIO + openpyxl load_workbook |
| **WebSocket for batch progress** | Project already uses SSE for streaming. SSE is simpler for server-to-client progress updates. | SSE events for batch progress |

## Integration Points with Existing Stack

### Database: SQLite + SQLAlchemy

**Batch task creation pattern:**
```python
# Batch insert within a single transaction
async with db.begin():
    for task_data in parsed_tasks:
        task = Task(
            name=task_data["name"],
            description=task_data["description"],
            target_url=task_data["target_url"],
            max_steps=task_data["max_steps"],
            preconditions=json.dumps(task_data["preconditions"]),
            external_assertions=json.dumps(task_data["assertions"]),
            status="draft",
        )
        db.add(task)
```

SQLite handles batch inserts well within a single transaction. The `aiosqlite` driver's async session wraps this correctly.

**New model fields needed:** None. The existing `Task` model has all required fields: `name`, `description`, `target_url`, `max_steps`, `preconditions` (JSON string), `external_assertions` (JSON string), `status`.

### API: FastAPI Routes

New routes to add to `backend/api/routes/tasks.py`:

| Route | Method | Purpose |
|-------|--------|---------|
| `/tasks/template` | GET | Download Excel template |
| `/tasks/import` | POST | Upload and parse Excel, batch create tasks |
| `/tasks/batch-execute` | POST | Start parallel execution of selected tasks |

### Frontend: API Client

New methods to add to `frontend/src/api/tasks.ts`:

| Method | Purpose |
|--------|---------|
| `downloadTemplate()` | GET template file, trigger browser download |
| `importExcel(file: File)` | POST multipart upload, return import results |
| `batchExecute(ids: string[], concurrency: number)` | POST start parallel execution |

**Important:** The `importExcel` method must NOT use the existing `apiClient` helper (which sets `Content-Type: application/json`). FormData uploads must let the browser set the Content-Type header with the multipart boundary.

### SSE: Batch Execution Progress

Reuse the existing SSE streaming pattern for individual runs. For batch execution, add a batch-level SSE channel:

```
GET /runs/batch/{batch_id}/stream  -> SSE events per task completion
```

Each event: `{ "task_id": "abc", "status": "running" | "success" | "failed" }`

## Version Compatibility

| Package | Version | Compatibility Note |
|---------|---------|-------------------|
| **openpyxl** | 3.1.5 | Current stable. Supports read_only mode, cell styling, data validation. No breaking changes expected. |
| **python-multipart** | 0.0.22 | Already installed. Required by FastAPI for UploadFile. |
| **FastAPI** | 0.135.1 | UploadFile API is stable since 0.65+. No changes needed. |
| **SQLAlchemy** | 2.0.48 | Async session for batch inserts is stable in 2.0+. |
| **Python** | 3.11.14 | `asyncio.TaskGroup` requires 3.11+. Confirmed available. |

## Performance Considerations

| Concern | Impact | Mitigation |
|---------|--------|------------|
| Excel parsing (100 rows) | Negligible (~50ms) | openpyxl `read_only=True` for large files |
| Browser RAM per parallel task | 150-300MB each | Semaphore limits concurrency; default 2 (400-600MB total) |
| SQLite concurrent writes from parallel tasks | Low -- aiosqlite serializes writes | WAL mode (already configured) handles read/write concurrency |
| File upload size | Small (Excel <5MB) | Validate size server-side, reject >5MB |
| SSE events for batch progress | Low frequency (1 per task completion) | No throttling needed |

## Installation

**No new packages to install.** All required dependencies are already in the project:

```bash
# Verify existing dependencies
python3 -c "import openpyxl; print(f'openpyxl {openpyxl.__version__}')"   # 3.1.5
python3 -c "import multipart; print(f'python-multipart {multipart.__version__}')"  # 0.0.22
python3 -c "import fastapi; print(f'fastapi {fastapi.__version__}')"  # 0.135.1
```

## Sources

### Verified Against Installed Code (HIGH confidence)
- `pyproject.toml` -- project dependencies, Python version requirement (3.11+)
- `.venv/bin/python3` -- verified openpyxl 3.1.5, python-multipart 0.0.22, FastAPI 0.135.1 installed
- `backend/db/models.py` -- Task model has all fields needed for batch import
- `backend/api/routes/tasks.py` -- existing route patterns to follow
- `backend/api/schemas/index.py` -- existing Pydantic schemas to extend
- `backend/core/agent_service.py` -- run_with_cleanup pattern for parallel execution
- `frontend/src/api/client.ts` -- existing API client (note: sets Content-Type:json, cannot use for FormData)
- `frontend/src/api/tasks.ts` -- existing task API methods to extend
- `frontend/src/components/Button.tsx` -- styling pattern to follow for upload button
- `webseleniumerp/use_case/export.py` -- existing openpyxl usage in project (load_workbook pattern)

### API Documentation (HIGH confidence)
- FastAPI UploadFile: built-in since FastAPI 0.65+, stable API in 0.135.1
- openpyxl 3.1: stable release, Workbook/load_workbook/iter_rows API well-documented
- asyncio.Semaphore + TaskGroup: Python 3.11 stdlib, no version concerns

---
*Stack research for: aiDriveUITest v0.9.0 Excel Batch Import and Parallel Execution*
*Researched: 2026-04-08*
