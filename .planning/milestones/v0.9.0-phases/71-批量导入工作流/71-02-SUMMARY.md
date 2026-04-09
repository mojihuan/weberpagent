---
phase: 71-批量导入工作流
plan: 02
subsystem: ui
tags: [react, typescript, tailwind, import-modal, form-data, drag-and-drop]

# Dependency graph
requires:
  - phase: 71-01
    provides: Import preview and confirm API endpoints (POST /tasks/import/preview, POST /tasks/import/confirm)
provides:
  - ImportModal component with 3-step upload/preview/result workflow
  - importPreview/importConfirm API functions using raw fetch with FormData
  - Import button in TaskListHeader
  - UploadStep with drag-and-drop and client-side validation
  - PreviewStep with valid/error row styling and summary bar
  - ResultStep with success display and auto-close
affects: [72-batch-execution, tasks-page]

# Tech tracking
tech-stack:
  added: []
  patterns: [raw-fetch-formdata, step-state-machine, drag-and-drop-upload]

key-files:
  created:
    - frontend/src/components/ImportModal/ImportModal.tsx
    - frontend/src/components/ImportModal/UploadStep.tsx
    - frontend/src/components/ImportModal/PreviewStep.tsx
    - frontend/src/components/ImportModal/ResultStep.tsx
    - frontend/src/components/ImportModal/index.ts
  modified:
    - frontend/src/api/tasks.ts
    - frontend/src/components/TaskList/TaskListHeader.tsx
    - frontend/src/pages/Tasks.tsx

key-decisions:
  - "Raw fetch used for FormData upload instead of apiClient (which sets Content-Type: application/json)"
  - "UploadStep calls importPreview internally, passing both file and response to parent via onFileSelected callback"
  - "PreviewStep uses bg-red-50 for error rows with AlertCircle icon + joined error messages"
  - "Confirm button disabled via data.has_errors check, preventing import when any row is invalid"

patterns-established:
  - "Raw fetch pattern for file uploads: bypass apiClient Content-Type header"
  - "Step-based modal state machine: useState<ImportStep> with upload/preview/result transitions"
  - "Client-side file validation: .xlsx extension and 5MB size limit with Chinese error messages"

requirements-completed: [IMPT-02]

# Metrics
duration: 8min
completed: 2026-04-08
---

# Phase 71 Plan 02: Frontend Import Workflow Summary

**ImportModal with 3-step state machine (upload/preview/result), raw fetch FormData upload, drag-and-drop with .xlsx validation**

## Performance

- **Duration:** 8 min
- **Started:** 2026-04-08T07:18:37Z
- **Completed:** 2026-04-08T07:27:02Z
- **Tasks:** 2
- **Files modified:** 8

## Accomplishments
- Complete ImportModal component with upload/preview/result step flow
- UploadStep with drag-and-drop and click-to-upload, client-side .xlsx and 5MB validation
- PreviewStep with 6-column table, valid/error row styling, summary counts, disabled confirm on errors
- Import button integrated into TaskListHeader, ImportModal wired into Tasks page with state management

## Task Commits

Each task was committed atomically:

1. **Task 1: Add import API functions, ImportModal shell, and wire into Tasks page** - `755bbd4` (feat)
2. **Task 2: Create UploadStep, PreviewStep, and ResultStep sub-components** - `1ce1e1c` (feat)

## Files Created/Modified
- `frontend/src/api/tasks.ts` - Added importPreview/importConfirm functions with raw fetch + FormData, ImportPreviewResponse/ImportConfirmResponse types
- `frontend/src/components/ImportModal/ImportModal.tsx` - Orchestrator with 3-step state machine, transitions, auto-close timer
- `frontend/src/components/ImportModal/UploadStep.tsx` - Drag-and-drop + click upload zone with .xlsx/5MB validation
- `frontend/src/components/ImportModal/PreviewStep.tsx` - Preview table with valid/error rows, summary bar, confirm/back buttons
- `frontend/src/components/ImportModal/ResultStep.tsx` - Success display with CheckCircle icon and 1.5s auto-close
- `frontend/src/components/ImportModal/index.ts` - Re-export ImportModal
- `frontend/src/components/TaskList/TaskListHeader.tsx` - Added onImportClick prop and Import button with Upload icon
- `frontend/src/pages/Tasks.tsx` - Added importModalOpen state, ImportModal render with fetchTasks callback

## Decisions Made
- Raw fetch used for FormData upload instead of apiClient which forces Content-Type: application/json header
- UploadStep internally calls importPreview and passes both file and response to parent via onFileSelected callback, keeping the API call responsibility in the upload component
- PreviewStep renders all 6 template columns in a scrollable table with max-h-[50vh]
- Auto-close timer in ResultStep uses useRef for cleanup, preventing stale timeouts on unmount

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Removed unused importPreview import from ImportModal.tsx**
- **Found during:** Task 1 (verifying TypeScript compilation)
- **Issue:** ImportModal.tsx imported importPreview but only uses importConfirm directly; importPreview is called from UploadStep, not ImportModal
- **Fix:** Changed import to only import importConfirm
- **Files modified:** frontend/src/components/ImportModal/ImportModal.tsx
- **Verification:** TypeScript compiles without TS6133 errors
- **Committed in:** 755bbd4 (Task 1 commit)

**2. [Rule 2 - Missing Critical] Added ImportModal render to Tasks.tsx**
- **Found during:** Task 1 (verifying all plan requirements)
- **Issue:** Tasks.tsx had importModalOpen state and onImportClick handler but was missing the actual `<ImportModal>` component render in JSX
- **Fix:** Added `<ImportModal open={importModalOpen} onClose={...} onImportComplete={fetchTasks} />` after the last ConfirmModal
- **Files modified:** frontend/src/pages/Tasks.tsx
- **Verification:** TypeScript compiles, ImportModal renders in component tree
- **Committed in:** 755bbd4 (Task 1 commit)

---

**Total deviations:** 2 auto-fixed (1 bug, 1 missing critical)
**Impact on plan:** Both auto-fixes necessary for correctness. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- ImportModal fully functional with upload/preview/confirm flow
- IMPT-02 requirement (preview with valid/error row styling) implemented
- Phase 71 complete, ready for Phase 72 (batch execution)
- Manual UI verification recommended for drag-and-drop interaction and visual rendering

## Self-Check: PASSED

- All 8 created/modified files verified on disk
- Both task commits (755bbd4, 1ce1e1c) verified in git log
- TypeScript compilation (tsc --noEmit -p tsconfig.app.json) passes
- Production build (npm run build) passes
- All 8 verification grep patterns confirmed present

---
*Phase: 71-批量导入工作流*
*Completed: 2026-04-08*
