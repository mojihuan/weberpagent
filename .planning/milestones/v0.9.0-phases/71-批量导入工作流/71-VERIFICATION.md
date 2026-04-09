---
phase: 71-批量导入工作流
verified: 2026-04-08T08:15:00Z
status: human_needed
score: 13/13 must-haves verified
human_verification:
  - test: "Drag-and-drop upload interaction"
    expected: "User can drag a .xlsx file onto the drop zone; zone highlights blue on drag-over; file uploads on drop"
    why_human: "Drag-and-drop is a browser DOM event interaction that cannot be verified without a running browser"
  - test: "Preview table visual rendering"
    expected: "Valid rows have white background with green CheckCircle; invalid rows have red background with AlertCircle and error text"
    why_human: "CSS class application and visual rendering requires browser inspection"
  - test: "Confirm button disabled state appearance"
    expected: "When has_errors=true, the confirm button is visually gray with opacity-50 and not clickable"
    why_human: "Disabled button visual state requires browser rendering verification"
  - test: "Auto-close timer after successful import"
    expected: "Result step displays for 1.5 seconds with success icon, then modal closes and task list shows new draft tasks"
    why_human: "Timer behavior and post-close state refresh requires runtime observation"
  - test: "Toast notification display"
    expected: "Success toast shows '成功导入 N 个任务' after confirm; error toast shows server error message on failure"
    why_human: "Toast notification rendering and positioning requires running application"
---

# Phase 71: 批量导入工作流 Verification Report

**Phase Goal:** QA 上传填写好的 Excel 后，可以在确认前预览解析结果（有效行绿色、无效行红色+错误信息），确认后系统批量创建所有 Task
**Verified:** 2026-04-08T08:15:00Z
**Status:** human_needed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | POST /tasks/import/preview accepts .xlsx file and returns parsed rows with valid/error status per row | VERIFIED | Endpoint at tasks.py:50-69, calls parse_excel(BytesIO(content)), returns rows with row_number/data/errors/valid fields. Test test_preview_valid_file passes. |
| 2 | POST /tasks/import/confirm accepts .xlsx file with no errors and creates all Tasks atomically in a single transaction | VERIFIED | Endpoint at tasks.py:72-101, uses async with db.begin() for atomic batch, maps assertions->external_assertions. Test test_confirm_creates_tasks passes (verifies 2 tasks in DB). |
| 3 | Both endpoints reject non-.xlsx files and files >5MB with Chinese error messages | VERIFIED | Shared _validate_upload_file helper at tasks.py:23-32 checks .xlsx extension, empty file, 5MB limit. Tests test_preview_rejects_non_xlsx, test_preview_rejects_oversized, test_preview_rejects_empty, test_confirm_rejects_non_xlsx all pass. |
| 4 | Confirm endpoint rejects files with any parse errors (has_errors=true) | VERIFIED | tasks.py:81-82 raises HTTPException(400) when result.has_errors. Test test_confirm_rejects_invalid passes (verifies no tasks created). |
| 5 | Any failure during batch create rolls back ALL inserts (no partial data) | VERIFIED | tasks.py:85 wraps all db.add() in async with db.begin(). Test test_confirm_rollback_on_error patches Task.__init__ to fail on 2nd row, verifies task count unchanged. |
| 6 | User clicks 'Import' button in TaskListHeader and ImportModal opens | VERIFIED | TaskListHeader.tsx:17 renders Button with onImportClick and Upload icon. Tasks.tsx:99 passes onImportClick={() => setImportModalOpen(true)}. Tasks.tsx:165-169 renders ImportModal with open={importModalOpen}. |
| 7 | User drags or clicks to select a .xlsx file, file is uploaded and preview table renders with all 6 data columns | VERIFIED | UploadStep.tsx implements drag-and-drop (onDragOver/onDrop) and click-to-upload (hidden input ref). Calls importPreview(file) on valid file, passes result to parent. PreviewStep.tsx:14-21 defines 6 PREVIEW_COLUMNS matching Excel template. |
| 8 | Valid rows show white background with green CheckCircle icon; invalid rows show red background with error messages | VERIFIED | PreviewStep.tsx:63 applies bg-white for valid rows, bg-red-50 for invalid. Lines 71-72 render CheckCircle (green) for valid, AlertCircle (red) + joined errors for invalid. |
| 9 | Summary bar shows valid X rows, invalid Y rows in Chinese | VERIFIED | PreviewStep.tsx:34-38 renders text with total_rows, valid_count in text-green-600, error_count in text-red-600. |
| 10 | Confirm Import button is disabled (gray, opacity-50) when has_errors=true | VERIFIED | PreviewStep.tsx:95 sets disabled={data.has_errors \|\| confirming}. Button component applies disabled styles (opacity-50, cursor-not-allowed). |
| 11 | On confirm success: Modal closes, success toast appears, task list refreshes with new draft tasks | VERIFIED | ImportModal.tsx:67-74 calls importConfirm(file), shows toast.success, sets step='result', starts 1.5s autoCloseTimer calling handleClose + onImportComplete (which is fetchTasks from Tasks.tsx:168). |
| 12 | On confirm failure: Error toast appears, Modal stays open for retry | VERIFIED | ImportModal.tsx:75-77 catches error, calls toast.error(message), does NOT change step -- stays on preview. |
| 13 | File input rejects non-.xlsx and >5MB files with Chinese error messages | VERIFIED | UploadStep.tsx:18-26 validateFile checks .xlsx extension (Chinese error) and 5MB limit (Chinese error). |

**Score:** 13/13 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| backend/api/routes/tasks.py | Import preview and confirm endpoints | VERIFIED | 153 lines, contains import_preview (line 50), import_confirm (line 72), _validate_upload_file (line 23), db.begin() atomic transaction, external_assertions mapping |
| backend/tests/unit/test_import_endpoints.py | 9 unit tests for both endpoints | VERIFIED | 267 lines, 9 tests in 2 classes (TestImportPreview, TestImportConfirm), all passing |
| frontend/src/api/tasks.ts | importPreview and importConfirm using raw fetch | VERIFIED | 113 lines, defines ImportPreviewResponse/ImportConfirmResponse types, uses new FormData + raw fetch (not apiClient) |
| frontend/src/components/ImportModal/ImportModal.tsx | 3-step state machine orchestrator | VERIFIED | 117 lines, ImportStep type, STEP_TITLES, handles upload/preview/result transitions with state management |
| frontend/src/components/ImportModal/UploadStep.tsx | Drag-and-drop upload zone | VERIFIED | 132 lines, implements onDragOver/onDrop/click upload, client-side .xlsx/5MB validation, calls importPreview |
| frontend/src/components/ImportModal/PreviewStep.tsx | Preview table with valid/error styling | VERIFIED | 109 lines, 6 PREVIEW_COLUMNS, bg-red-50 for errors, CheckCircle/AlertCircle icons, disabled confirm on has_errors |
| frontend/src/components/ImportModal/ResultStep.tsx | Success display with auto-close | VERIFIED | 30 lines, CheckCircle icon, "导入完成" title, 1.5s setTimeout auto-close with cleanup |
| frontend/src/components/ImportModal/index.ts | Re-export | VERIFIED | 1 line, exports ImportModal |
| frontend/src/components/TaskList/TaskListHeader.tsx | Import button with onImportClick | VERIFIED | 28 lines, Upload icon, Button variant="secondary", onImportClick prop |
| frontend/src/pages/Tasks.tsx | ImportModal integration | VERIFIED | 172 lines, importModalOpen state, ImportModal render at line 165, passes fetchTasks as onImportComplete |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| backend/api/routes/tasks.py | backend/utils/excel_parser.py | from backend.utils.excel_parser import parse_excel | WIRED | Line 15: import present. Lines 54, 79: parse_excel(BytesIO(content)) called in both endpoints |
| backend/api/routes/tasks.py | backend/db/models.py | from backend.db.models import Task | WIRED | Line 11: import present. Line 96: Task(**task_data, status="draft") used in confirm endpoint |
| frontend/src/api/tasks.ts | /api/tasks/import/preview | raw fetch with FormData | WIRED | Lines 30-31: new FormData(), formData.append('file', file). Line 32: fetch to /tasks/import/preview |
| frontend/src/api/tasks.ts | /api/tasks/import/confirm | raw fetch with FormData | WIRED | Lines 45-47: new FormData(), fetch to /tasks/import/confirm |
| ImportModal.tsx | api/tasks.ts (importConfirm) | import { importConfirm } | WIRED | Line 4: import. Line 67: await importConfirm(file) |
| UploadStep.tsx | api/tasks.ts (importPreview) | import { importPreview } | WIRED | Line 3: import. Line 38: await importPreview(file) |
| Tasks.tsx | ImportModal component | ImportModal render in JSX | WIRED | Line 10: import. Line 165: <ImportModal open={importModalOpen}...> |
| TaskListHeader.tsx | Tasks.tsx (onImportClick) | Button onClick={onImportClick} | WIRED | Line 17: onClick handler. Tasks.tsx:99 passes onImportClick={() => setImportModalOpen(true)} |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|--------------|--------|--------------------|--------|
| import_preview endpoint | result (ParseResult) | parse_excel(BytesIO(content)) from uploaded file | Yes -- parse_excel reads workbook, iterates rows, validates fields, returns ParsedRow list | FLOWING |
| import_confirm endpoint | result.rows | parse_excel(BytesIO(content)) re-parsed + db.begin() | Yes -- iterates result.rows, creates Task objects, db.add() in transaction | FLOWING |
| PreviewStep | data.rows | importPreview API call response | Yes -- UploadStep calls importPreview which hits backend preview endpoint, returns real parsed data | FLOWING |
| ImportModal (confirm) | result.created_count | importConfirm API call response | Yes -- hits backend confirm endpoint which creates Tasks and returns actual count | FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Import endpoint tests pass | uv run pytest backend/tests/unit/test_import_endpoints.py -x -v | 9 passed in 0.51s | PASS |
| All backend tests pass (no regressions) | uv run pytest backend/tests/unit/ -v | 42 passed in 0.61s | PASS |
| TypeScript compilation succeeds | npx tsc --noEmit -p tsconfig.app.json | (no output = success) | PASS |
| Production build succeeds | npm run build | Built in 1.54s, 3 output files | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| IMPT-01 | 71-01, 71-02 | User can upload .xlsx, system parses rows and validates all fields | SATISFIED | Backend preview endpoint parses and validates; frontend UploadStep + importPreview API wired |
| IMPT-02 | 71-02 | User can preview results before confirming; valid rows green, invalid rows red with errors | SATISFIED | PreviewStep renders table with bg-white/bg-red-50, CheckCircle/AlertCircle icons, summary bar with counts; confirm button disabled when has_errors |
| IMPT-03 | 71-01, 71-02 | Confirm creates Tasks atomically (all-or-nothing), status=draft | SATISFIED | confirm endpoint uses async with db.begin(), rollback test passes; frontend calls importConfirm and shows success toast + task list refresh |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| ImportModal.tsx | 83 | `return null` when !open | Info | Standard conditional rendering guard -- not a stub |
| UploadStep.tsx | 25 | `return null` from validateFile on success | Info | Validation success path (null = no error) -- not a stub |

No TODO/FIXME/HACK/PLACEHOLDER comments found in any files. No console.log statements. No hardcoded empty data flows. No stub implementations detected.

### Human Verification Required

### 1. Drag-and-drop upload interaction

**Test:** Open Tasks page, click "Import" button, drag a .xlsx file from desktop onto the drop zone
**Expected:** Drop zone highlights blue (border-blue-500 bg-blue-50) while dragging; on drop, file uploads and preview table appears
**Why human:** Drag-and-drop is a browser DOM event interaction that cannot be verified programmatically

### 2. Preview table visual rendering

**Test:** Upload a .xlsx file with 2 valid rows and 1 invalid row (e.g., missing task name)
**Expected:** Valid rows have white background with green CheckCircle; invalid row has red background with AlertCircle icon and specific error messages (e.g., "必填字段 '任务名称' 不能为空")
**Why human:** CSS class application and visual rendering requires browser inspection

### 3. Confirm button disabled state

**Test:** Upload a .xlsx file with at least one invalid row
**Expected:** The "确认导入" button appears grayed out (opacity-50) and is not clickable; only becomes enabled when all rows are valid
**Why human:** Disabled button visual state and click behavior requires runtime verification

### 4. End-to-end import flow

**Test:** Upload a valid .xlsx with 3 test tasks, click "确认导入"
**Expected:** Success toast "成功导入 3 个任务" appears, result step shows CheckCircle + "导入完成", modal auto-closes after 1.5s, task list refreshes showing 3 new draft tasks
**Why human:** Full end-to-end flow involving toast notifications, timer behavior, and state refresh requires running application

### 5. Error handling on confirm failure

**Test:** Upload a file that passes preview validation but confirm fails (e.g., server error)
**Expected:** Error toast appears with error message, modal stays on preview step for retry
**Why human:** Runtime error handling and toast display requires live application

### Gaps Summary

No code-level gaps found. All 13 observable truths verified through source code analysis, test execution, and wiring verification. All 3 requirement IDs (IMPT-01, IMPT-02, IMPT-03) are satisfied by implementation evidence across both plans.

The phase goal is achieved from a code perspective: the backend provides two endpoints (preview + confirm) with full validation and atomic batch creation, and the frontend provides a complete ImportModal with 3-step state machine (upload -> preview -> result) integrated into the Tasks page. The 5 items flagged for human verification are all visual/interactive behaviors that require a running browser to confirm but have solid code evidence supporting correct implementation.

---

_Verified: 2026-04-08T08:15:00Z_
_Verifier: Claude (gsd-verifier)_
