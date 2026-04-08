# Phase 71: 批量导入工作流 - Research

**Researched:** 2026-04-08
**Domain:** FastAPI file upload + two-phase import (preview/confirm) + React Modal UI + atomic batch create
**Confidence:** HIGH

## Summary

Phase 71 implements the complete Excel batch import workflow: QA uploads a filled .xlsx file, sees a preview of parsed rows (valid rows green, invalid rows red with error details), and confirms import to batch-create Tasks in a single database transaction. The phase builds directly on Phase 70's ExcelParser and TEMPLATE_COLUMNS, requiring no new Python or npm dependencies. All required packages (python-multipart 0.0.22, openpyxl 3.1.5, FastAPI 0.135.1) are already installed and verified.

The backend adds two endpoints to the existing `tasks.py` router: `POST /tasks/import/preview` and `POST /tasks/import/confirm`. Both accept `UploadFile`, and the confirm endpoint re-parses the file (no server-side caching). The frontend creates a new `ImportModal` component following the established `TaskFormModal` pattern (fixed overlay, z-50, X close button), with a three-step internal state machine (upload -> preview -> result). The critical integration point is using raw `fetch` with `FormData` to bypass the existing `apiClient` which sets `Content-Type: application/json`.

**Primary recommendation:** Build two lean endpoints reusing ExcelParser directly, create ImportModal as a sibling of TaskModal with three-phase state, and wrap batch creates in a single `async with session.begin()` block for atomicity.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Upload entry via TaskListHeader "Import" button, Modal popup, no page navigation
- **D-02:** Modal has drag zone + click-to-select dual mode, highlight on drag-over
- **D-03:** Accept .xlsx only, 5MB max, front-end instant rejection for wrong format/size
- **D-04:** Preview shows full table with all columns matching Excel template headers (Chinese)
- **D-05:** Table top shows summary stats ("valid X rows, invalid Y rows"), error rows light-red background + error info
- **D-06:** Preview table scrolls within Modal, sticky header on overflow
- **D-07:** "Confirm Import" button disabled when invalid rows exist
- **D-08:** Two-phase re-upload pattern -- POST /tasks/import/preview returns preview JSON; POST /tasks/import/confirm re-uploads same file for batch creation. Confirm re-parses, no server state cache
- **D-09:** Both endpoints added to existing tasks.py router, consistent with /tasks/template
- **D-10:** Confirm endpoint wraps all creates in a DB transaction, any failure rolls back all
- **D-11:** Imported Task status is draft (consistent with manual creation)
- **D-12:** Backend also validates file format/size (defensive, not trusting front-end)
- **D-13:** Create standalone ImportModal component (components/ImportModal/), sibling to TaskFormModal
- **D-14:** Modal three-step state: upload -> preview -> confirm/result, each with independent loading state
- **D-15:** On success: close Modal + toast success + auto-refresh task list
- **D-16:** On failure: toast error, Modal stays open for retry
- **D-17:** Upload API uses raw fetch + API_BASE config, bypasses apiClient's Content-Type: application/json

### Claude's Discretion
- Modal specific UI styling and layout (Tailwind CSS)
- Preview table column width distribution
- Error message display format (column vs tooltip vs row-expand)
- Modal size (suggest large/wide to fit preview table)
- Backend response specific JSON structure
- ImportModal internal sub-component splitting

### Deferred Ideas (OUT OF SCOPE)
- Error-annotated Excel download (IMPT-04) -- v2 requirement
- Simplified assertion format (IMPT-05) -- v2 requirement
- CSV import -- Out of Scope
- Task export to Excel -- Out of Scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| IMPT-01 | User uploads .xlsx, system parses row-by-row to TaskCreate format with field validation | ExcelParser.parse_excel() from Phase 70 returns ParsedRow with row_number, data dict, and errors list. The data dict keys match TaskCreate fields directly. Preview endpoint feeds UploadFile bytes through ExcelParser and returns structured JSON. |
| IMPT-02 | Preview parsed results before confirm: valid rows green, invalid rows red + error details (row number + field + reason) | Frontend ImportModal renders ParseResult.rows in a table. Each row checks `errors.length > 0` to determine red/green styling. ExcelParser already returns row_number + specific error strings with field names. |
| IMPT-03 | Confirm import batch-creates Tasks (all valid required), any failure rolls back all, imported status is draft | Confirm endpoint re-parses file, validates has_errors is False, then iterates rows calling TaskRepository logic within a single `async with session.begin()` transaction block. Session-level begin ensures one DB transaction covering all inserts. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| FastAPI | 0.135.1 | UploadFile endpoint, APIRouter | Already installed, project framework |
| python-multipart | 0.0.22 | multipart/form-data parsing for UploadFile | Already installed as FastAPI transitive dep |
| openpyxl | 3.1.5 | Excel parsing (via ExcelParser) | Phase 70 dependency, already installed |
| SQLAlchemy (async) | 2.x | AsyncSession transaction for batch create | Already installed, project ORM |
| aiosqlite | 0.20+ | SQLite async driver | Already installed |
| React | 19.2.0 | ImportModal component | Project frontend framework |
| Tailwind CSS | 4.2.1 | Modal and table styling | Project CSS framework |
| sonner | 2.0.7 | Toast notifications on success/failure | Already used in apiClient and Tasks page |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| lucide-react | 0.577.0 | Icons (Upload, X, CheckCircle, AlertCircle) | ImportModal UI icons |
| Pydantic | 2.x | TaskCreate validation on confirm | Validate each row's data against schema before create |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Raw fetch for upload | Modify apiClient to support FormData | Modifying apiClient risks breaking existing JSON calls; raw fetch is simpler and isolated |
| Full-table preview | Paginated preview | For 5MB max files (likely <500 rows), full table is fine; pagination adds unnecessary complexity |
| Server-side preview caching | Re-parse on confirm (chosen) | Caching requires session state management; re-parse is stateless and simpler |

**Installation:**
```bash
# No new packages needed. All dependencies verified installed.
uv run python -c "import multipart; print(multipart.__version__)"   # 0.0.22
uv run python -c "import openpyxl; print(openpyxl.__version__)"     # 3.1.5
```

## Architecture Patterns

### Recommended Project Structure
```
backend/api/routes/tasks.py         # Add import_preview + import_confirm endpoints
backend/utils/excel_parser.py       # Phase 70 asset (reuse, no changes)
backend/utils/excel_template.py     # Phase 70 asset (reuse, no changes)
backend/db/repository.py            # May add batch_create or inline in endpoint
backend/db/schemas.py               # May add ImportPreviewResponse schema

frontend/src/components/ImportModal/
  index.ts                          # Re-export
  ImportModal.tsx                   # Main modal component (3-step state machine)
  UploadStep.tsx                    # Step 1: drag-and-drop + file picker
  PreviewStep.tsx                   # Step 2: parsed data table with validation
  ResultStep.tsx                    # Step 3: success/error result display
frontend/src/api/tasks.ts           # Add importPreview() + importConfirm() using raw fetch
frontend/src/components/TaskList/TaskListHeader.tsx  # Add "Import" button
frontend/src/pages/Tasks.tsx        # Add importModalOpen state + handler
```

### Pattern 1: Two-Phase Upload with Re-Parse (Backend)
**What:** Both preview and confirm endpoints accept the same file. Confirm re-parses instead of caching preview state.
**When to use:** Stateless import workflows where the file is small enough to parse twice.
**Example:**
```python
# backend/api/routes/tasks.py
from fastapi import UploadFile, File
from io import BytesIO
from backend.utils.excel_parser import parse_excel

@router.post("/import/preview")
async def import_preview(file: UploadFile = File(...)):
    # 1. Validate file format and size
    if not file.filename or not file.filename.endswith(".xlsx"):
        raise HTTPException(400, detail="仅支持 .xlsx 格式文件")
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(400, detail="文件大小不能超过 5MB")

    # 2. Parse
    result = parse_excel(BytesIO(content))

    # 3. Return structured preview
    return {
        "rows": [
            {
                "row_number": row.row_number,
                "data": row.data,
                "errors": row.errors,
                "valid": len(row.errors) == 0,
            }
            for row in result.rows
        ],
        "total_rows": result.total_rows,
        "valid_count": sum(1 for r in result.rows if not r.errors),
        "error_count": sum(1 for r in result.rows if r.errors),
        "has_errors": result.has_errors,
    }

@router.post("/import/confirm")
async def import_confirm(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    # 1. Validate file (same checks as preview)
    # 2. Re-parse
    result = parse_excel(BytesIO(content))
    if result.has_errors:
        raise HTTPException(400, detail="文件包含无效行，请返回预览检查")

    # 3. Atomic batch create in single transaction
    tasks_created = []
    async with db.begin():
        repo = TaskRepository(db)
        for row in result.rows:
            task_data = TaskCreate(**row.data)
            task = Task(**task_data.model_dump())
            # Serialize preconditions and assertions as repo.create does
            # ... (or call repo.create but without its internal commit)
            db.add(task)
            tasks_created.append(task)
    # Transaction committed on block exit; any exception rolls back
```

### Pattern 2: Raw Fetch for FormData Upload (Frontend)
**What:** Bypass apiClient's Content-Type: application/json by using raw fetch with FormData.
**When to use:** File upload endpoints where multipart/form-data is required.
**Example:**
```typescript
// frontend/src/api/tasks.ts
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080/api'

export async function importPreview(file: File): Promise<ImportPreviewResponse> {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`${API_BASE}/tasks/import/preview`, {
    method: 'POST',
    body: formData,
    // Do NOT set Content-Type header -- browser sets multipart boundary automatically
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Upload failed' }))
    throw new Error(error.detail || `Upload failed: ${response.status}`)
  }
  return response.json()
}
```

### Pattern 3: Three-Step Modal State Machine (Frontend)
**What:** ImportModal manages internal step state with independent loading states per step.
**When to use:** Multi-step wizard patterns in modals.
**Example:**
```typescript
type ImportStep = 'upload' | 'preview' | 'result'
const [step, setStep] = useState<ImportStep>('upload')
const [file, setFile] = useState<File | null>(null)
const [previewData, setPreviewData] = useState<ImportPreviewResponse | null>(null)
const [uploading, setUploading] = useState(false)
const [confirming, setConfirming] = useState(false)
const [result, setResult] = useState<{ success: boolean; count?: number; error?: string } | null>(null)
```

### Pattern 4: Atomic Batch Create with Session Transaction
**What:** Use `async with session.begin()` to wrap all task creates in a single DB transaction.
**When to use:** When all-or-nothing semantics are required (IMPT-03).
**Key insight:** The existing `TaskRepository.create()` calls `session.commit()` internally, which commits per-row. For batch import, we need to either: (a) create a `batch_create()` method that defers commit, or (b) add tasks directly via `session.add()` and let the `begin()` block commit on exit.

**Recommended approach (b):** Direct `session.add()` in the endpoint within `async with db.begin()`, replicating the serialization logic from `TaskRepository.create()` without calling commit. This avoids modifying the existing repository pattern.

### Anti-Patterns to Avoid
- **Server-side preview caching:** Do NOT store parsed results in memory/session/Redis between preview and confirm. Re-parse on confirm (per D-08 decision).
- **Per-row commit in confirm:** Do NOT call `TaskRepository.create()` which commits per row. Use `session.add()` + `session.begin()` for atomic batch.
- **Using apiClient for FormData:** Do NOT use the existing apiClient which sets `Content-Type: application/json`. Use raw `fetch` with `FormData`.
- **Trusting front-end validation only:** Backend MUST independently validate file format and size (per D-12 decision).
- **Mutating ExcelParser output:** ParsedRow is a frozen dataclass. Create new objects if transformation is needed.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Excel parsing | Custom CSV/Excel reader | ExcelParser.parse_excel() from Phase 70 | Handles type coercion, JSON parsing, merged cells, empty rows, header validation |
| File validation | Custom extension check | FastAPI UploadFile + filename check + size check | Standard pattern, python-multipart handles parsing |
| FormData serialization | Manual multipart construction | Browser FormData API | Browser handles boundaries, encoding, content-transfer |
| DB transaction | Manual BEGIN/COMMIT/ROLLBACK | SQLAlchemy `async with session.begin()` | Handles rollback on exception automatically |
| Toast notifications | Custom notification system | sonner (already installed) | Used throughout the app, consistent UX |
| Modal overlay | Custom modal component | Copy TaskFormModal pattern | Same z-50 fixed overlay, backdrop, close button pattern |

**Key insight:** Phase 70 already solved the hardest part (Excel parsing with type coercion, error collection, and edge cases). Phase 71 is wiring: upload -> parse -> display -> confirm -> create.

## Common Pitfalls

### Pitfall 1: apiClient Content-Type Override
**What goes wrong:** Using apiClient for file upload sends `Content-Type: application/json`, causing FastAPI to fail parsing the multipart body.
**Why it happens:** apiClient hardcodes `'Content-Type': 'application/json'` in its headers.
**How to avoid:** Use raw `fetch` with `FormData` for upload endpoints. Do NOT set Content-Type header -- browser auto-sets `multipart/form-data` with proper boundary.
**Warning signs:** 422 Unprocessable Entity from FastAPI; request body seen as empty.

### Pitfall 2: Per-Row Commit in Batch Create
**What goes wrong:** Calling `TaskRepository.create()` in a loop commits after each row, meaning a failure at row 50 leaves 49 orphaned tasks.
**Why it happens:** `TaskRepository.create()` calls `await self.session.commit()` internally.
**How to avoid:** Use `session.add(task)` directly in endpoint within `async with db.begin()` block. Replicate preconditions/assertions serialization logic inline. Do NOT call repo.commit().
**Warning signs:** Partial tasks created after error; non-atomic import.

### Pitfall 3: FormData Field Name Mismatch
**What goes wrong:** Frontend sends `formData.append('file', file)` but backend expects a different parameter name, causing 422.
**Why it happens:** FastAPI's `File(...)` parameter name must match the FormData key.
**How to avoid:** Use consistent naming: `file: UploadFile = File(...)` on backend, `formData.append('file', file)` on frontend.
**Warning signs:** 422 validation error: "field required" for the file parameter.

### Pitfall 4: Preview Confirm File Mismatch
**What goes wrong:** User previews file A, changes file on disk, selects file B for confirm, gets different results.
**Why it happens:** Browser File object is held in React state, user could theoretically change it.
**How to avoid:** Hold the File object in state throughout the Modal lifecycle. Do not allow file re-selection while in preview step (or allow only with reset to step 1).
**Warning signs:** Confirm creates different tasks than preview showed.

### Pitfall 5: SQLite Write Lock During Batch
**What goes wrong:** Large batch (100+ tasks) holds write lock for extended period, blocking other operations.
**Why it happens:** SQLite WAL mode still serializes writes; long transactions block other writers.
**How to avoid:** Keep transaction short -- only INSERT operations, no reads. Batch size naturally limited by 5MB file size (realistically <500 rows, more likely <100).
**Warning signs:** Other API calls timeout during import.

### Pitfall 6: File Object Lost on Re-Render
**What goes wrong:** User clicks "Confirm Import" but `file` state is null because component re-rendered or Modal was closed.
**Why it happens:** React state resets on unmount; File objects are not serializable.
**How to avoid:** Keep Modal mounted with `open` prop control (same pattern as TaskFormModal). File state persists while Modal is open.
**Warning signs:** Confirm button triggers "No file selected" error.

### Pitfall 7: JSON Serialization of ParsedRow Data
**What goes wrong:** ParsedRow.data contains Python types (int, None, list) that FastAPI must serialize to JSON. Assertions field may be a string (when JSON parse failed) instead of list.
**Why it happens:** ExcelParser stores raw string in data[key] when JSON parsing fails, so Phase 71 UI can display original input.
**How to avoid:** In the preview endpoint, serialize errors clearly. In confirm, only proceed if has_errors is False (which means all JSON fields parsed successfully). Do NOT try to create TaskCreate from a row with string-valued assertions.
**Warning signs:** 500 error on confirm because Pydantic receives string where list expected.

## Code Examples

### Backend: Preview Endpoint
```python
# backend/api/routes/tasks.py
from fastapi import UploadFile, File
from io import BytesIO
from backend.utils.excel_parser import parse_excel

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

async def _validate_and_parse(file: UploadFile) -> tuple[bytes, str]:
    """Validate upload file, return (content, filename). Shared by preview and confirm."""
    if not file.filename or not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="仅支持 .xlsx 格式文件")
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小不能超过 5MB")
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="文件为空")
    return content, file.filename

@router.post("/import/preview")
async def import_preview(file: UploadFile = File(...)):
    content, _ = await _validate_and_parse(file)
    result = parse_excel(BytesIO(content))
    return {
        "rows": [
            {
                "row_number": row.row_number,
                "data": row.data,
                "errors": row.errors,
                "valid": len(row.errors) == 0,
            }
            for row in result.rows
        ],
        "total_rows": result.total_rows,
        "valid_count": sum(1 for r in result.rows if not r.errors),
        "error_count": sum(1 for r in result.rows if r.errors),
        "has_errors": result.has_errors,
    }
```

### Backend: Confirm Endpoint with Atomic Transaction
```python
import json
from backend.db.models import Task

@router.post("/import/confirm")
async def import_confirm(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    content, _ = await _validate_and_parse(file)
    result = parse_excel(BytesIO(content))

    if result.has_errors:
        raise HTTPException(status_code=400, detail="文件包含无效行，无法导入")

    created_count = 0
    async with db.begin():
        for row in result.rows:
            task_data = row.data
            # Serialize preconditions (same as TaskRepository.create)
            preconditions = task_data.get("preconditions")
            if preconditions is not None:
                task_data["preconditions"] = json.dumps(preconditions, ensure_ascii=False)
            # Serialize assertions to external_assertions (same as TaskRepository.create)
            assertions = task_data.pop("assertions", None)
            if assertions is not None:
                task_data["external_assertions"] = json.dumps(assertions, ensure_ascii=False)

            task = Task(**task_data, status="draft")
            db.add(task)
            created_count += 1
    # Transaction commits here on successful block exit

    return {"status": "success", "created_count": created_count}
```

### Frontend: Raw Fetch Upload
```typescript
// frontend/src/api/tasks.ts
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080/api'

export interface ImportPreviewRow {
  row_number: number
  data: Record<string, unknown>
  errors: string[]
  valid: boolean
}

export interface ImportPreviewResponse {
  rows: ImportPreviewRow[]
  total_rows: number
  valid_count: number
  error_count: number
  has_errors: boolean
}

export async function importPreview(file: File): Promise<ImportPreviewResponse> {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`${API_BASE}/tasks/import/preview`, {
    method: 'POST',
    body: formData,
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Upload failed' }))
    throw new Error(error.detail || `Upload failed: ${response.status}`)
  }
  return response.json()
}

export async function importConfirm(file: File): Promise<{ status: string; created_count: number }> {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`${API_BASE}/tasks/import/confirm`, {
    method: 'POST',
    body: formData,
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Import failed' }))
    throw new Error(error.detail || `Import failed: ${response.status}`)
  }
  return response.json()
}
```

### Frontend: ImportModal Structure
```typescript
// frontend/src/components/ImportModal/ImportModal.tsx
// Pattern follows TaskFormModal: fixed inset-0, z-50, bg-black/50 backdrop

// Key state:
type ImportStep = 'upload' | 'preview' | 'result'
const [step, setStep] = useState<ImportStep>('upload')
const [file, setFile] = useState<File | null>(null)
const [previewData, setPreviewData] = useState<ImportPreviewResponse | null>(null)
const [uploading, setUploading] = useState(false)
const [confirming, setConfirming] = useState(false)

// Step transitions:
// upload -> preview: on file selected, call importPreview(file), set previewData, setStep('preview')
// preview -> result: on confirm click, call importConfirm(file), set result, setStep('result')
// result -> (auto-close): on success, onClose + toast + refresh task list

// Modal sizing: max-w-4xl or wider to accommodate 6-column preview table
```

### Frontend: Preview Table Row Styling
```typescript
// Row rendering in PreviewStep.tsx
{previewData.rows.map(row => (
  <tr
    key={row.row_number}
    className={row.valid ? 'bg-white' : 'bg-red-50'}
  >
    <td className="...">{row.row_number}</td>
    <td className="...">{row.data.name}</td>
    {/* ... other columns ... */}
    <td className="...">
      {row.errors.length > 0 ? (
        <span className="text-red-600 text-sm">{row.errors.join('; ')}</span>
      ) : (
        <CheckCircle className="w-4 h-4 text-green-500" />
      )}
    </td>
  </tr>
))}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| apiClient for all requests | Raw fetch for multipart | Project constraint | FormData upload must bypass apiClient |
| Per-row commit (repo.create) | Batch session.begin() | Phase 71 design | Atomicity requires new transaction pattern |
| In-memory preview cache | Re-parse on confirm | v0.9.0 decision | Stateless, simpler, slightly more CPU |

**Deprecated/outdated:**
- FastAPI's deprecated `UploadFile.read()` sync pattern -- use `await file.read()` async version (current code uses this correctly)

## Open Questions

1. **Should batch_create be a method on TaskRepository or inline in the endpoint?**
   - What we know: Current repo.create() commits per-row, incompatible with atomic batch.
   - What's unclear: Whether adding a batch_create() method is cleaner than inlining.
   - Recommendation: Inline in the endpoint. A batch_create() method would require passing the session differently or modifying the commit pattern. Keep it simple and visible in the endpoint where the transaction boundary is clear.

2. **Should the preview response include the full data dict for each row, or just display-ready values?**
   - What we know: ExcelParser returns data as dict with Python types. Some fields (assertions, preconditions) may be lists or raw strings.
   - What's unclear: Whether the frontend needs the raw data or just formatted strings.
   - Recommendation: Return the full data dict in the preview response. The frontend can display it as-is (JSON arrays as strings, etc.) and does not need to parse it. For the confirm endpoint, re-parsing ensures correct types.

3. **What happens if the user uploads a very large valid file (hundreds of rows)?**
   - What we know: 5MB limit caps realistic rows at ~500 (typical test case row is ~500 bytes). SQLite can handle this in a single transaction.
   - What's unclear: Whether the UI should paginate the preview.
   - Recommendation: No pagination for v0.9.0. Full table display in scrollable Modal is fine for <500 rows. If needed later, add pagination as a v2 enhancement.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| python-multipart | FastAPI UploadFile | Yes | 0.0.22 | -- |
| openpyxl | ExcelParser | Yes | 3.1.5 | -- |
| FastAPI | API endpoints | Yes | 0.135.1 | -- |
| SQLAlchemy async | Batch transaction | Yes | 2.x | -- |
| aiosqlite | SQLite async driver | Yes | 0.20+ | -- |
| React | Frontend components | Yes | 19.2.0 | -- |
| sonner | Toast notifications | Yes | 2.0.7 | -- |
| lucide-react | UI icons | Yes | 0.577.0 | -- |
| Tailwind CSS | Styling | Yes | 4.2.1 | -- |
| pytest | Test framework | Yes | 8.x | -- |
| pytest-asyncio | Async test support | Yes | 0.24+ | -- |

**Missing dependencies with no fallback:** None

**Missing dependencies with fallback:** None

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.x + pytest-asyncio 0.24+ |
| Config file | pyproject.toml [tool.pytest.ini_options] |
| Quick run command | `uv run pytest backend/tests/unit/test_import_endpoints.py -x -v` |
| Full suite command | `uv run pytest backend/tests/unit/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| IMPT-01 | File upload -> parse -> return preview with row data | unit | `uv run pytest backend/tests/unit/test_import_endpoints.py::test_preview_valid_file -x` | Wave 0 |
| IMPT-01 | File format validation (non-xlsx rejected) | unit | `uv run pytest backend/tests/unit/test_import_endpoints.py::test_preview_rejects_non_xlsx -x` | Wave 0 |
| IMPT-01 | File size validation (>5MB rejected) | unit | `uv run pytest backend/tests/unit/test_import_endpoints.py::test_preview_rejects_oversized -x` | Wave 0 |
| IMPT-02 | Preview returns errors for invalid rows | unit | `uv run pytest backend/tests/unit/test_import_endpoints.py::test_preview_shows_errors -x` | Wave 0 |
| IMPT-03 | Confirm creates tasks atomically | unit | `uv run pytest backend/tests/unit/test_import_endpoints.py::test_confirm_creates_tasks -x` | Wave 0 |
| IMPT-03 | Confirm rolls back on error | unit | `uv run pytest backend/tests/unit/test_import_endpoints.py::test_confirm_rollback_on_error -x` | Wave 0 |
| IMPT-03 | Confirm rejects file with errors | unit | `uv run pytest backend/tests/unit/test_import_endpoints.py::test_confirm_rejects_invalid -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_import_endpoints.py -x -v`
- **Per wave merge:** `uv run pytest backend/tests/unit/ -v`
- **Phase gate:** Full unit suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_import_endpoints.py` -- covers IMPT-01, IMPT-02, IMPT-03 (FastAPI TestClient with async)
- [ ] Consider: shared test fixture for creating valid .xlsx BytesIO buffers (can reuse `_make_workbook` from test_excel_parser.py)

## Sources

### Primary (HIGH confidence)
- `backend/utils/excel_parser.py` -- ParsedRow, ParseResult, parse_excel() API and return types (verified 2026-04-08)
- `backend/utils/excel_template.py` -- TEMPLATE_COLUMNS column contract (verified 2026-04-08)
- `backend/db/schemas.py` -- TaskCreate Pydantic model with field validation (verified 2026-04-08)
- `backend/db/models.py` -- Task ORM model, fields, status default "draft" (verified 2026-04-08)
- `backend/db/repository.py` -- TaskRepository.create() serialization pattern for preconditions/assertions (verified 2026-04-08)
- `backend/db/database.py` -- async_session factory, get_db() dependency (verified 2026-04-08)
- `backend/api/routes/tasks.py` -- Existing router structure and dependency injection pattern (verified 2026-04-08)
- `frontend/src/api/client.ts` -- apiClient Content-Type: application/json hardcoded (verified 2026-04-08)
- `frontend/src/components/TaskModal/TaskFormModal.tsx` -- Modal overlay pattern reference (verified 2026-04-08)
- `frontend/src/components/shared/ConfirmModal.tsx` -- Shared modal pattern reference (verified 2026-04-08)
- `pyproject.toml` -- All project dependencies verified installed (verified 2026-04-08)

### Secondary (MEDIUM confidence)
- SQLAlchemy AsyncSession.begin() documentation -- nested transaction semantics for atomic batch create
- FastAPI UploadFile documentation -- File(...) parameter binding, python-multipart requirement

### Tertiary (LOW confidence)
- None -- all findings verified against installed code and packages

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all packages verified installed, versions confirmed via `uv run python -c` commands
- Architecture: HIGH -- patterns derived from existing code (TaskFormModal, apiClient, repository), ExcelParser API fully analyzed
- Pitfalls: HIGH -- apiClient Content-Type issue confirmed in code (client.ts line 25), repository per-row commit confirmed in repository.py line 46
- Transaction pattern: HIGH -- SQLAlchemy AsyncSession.begin() is well-documented, aiosqlite supports it

**Research date:** 2026-04-08
**Valid until:** 2026-05-08 (stable -- all dependencies are established packages)
