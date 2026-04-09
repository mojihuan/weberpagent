---
phase: 71-批量导入工作流
plan: 01
subsystem: api
tags: [fastapi, openpyxl, sqlalchemy, async, file-upload, batch-import]

# Dependency graph
requires:
  - phase: 70-excel
    provides: "parse_excel() function, ParsedRow/ParseResult dataclasses, TEMPLATE_COLUMNS contract"
provides:
  - "POST /tasks/import/preview endpoint with row-level validation"
  - "POST /tasks/import/confirm endpoint with atomic batch Task creation"
  - "Shared _validate_upload_file() helper for .xlsx format and 5MB size check"
affects: [71-02, frontend-import-ui]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Two-phase import: preview (stateless parse) -> confirm (re-parse + atomic insert)"
    - "async with db.begin() for batch transactional integrity"
    - "assertions -> external_assertions column mapping in import confirm"

key-files:
  created:
    - backend/tests/unit/test_import_endpoints.py
  modified:
    - backend/api/routes/tasks.py

key-decisions:
  - "confirm endpoint re-parses file rather than caching server state (per D-08 decision)"
  - "async with db.begin() wraps all inserts for atomic rollback on any failure"
  - "assertions key popped and renamed to external_assertions matching Task model"
  - "Test isolation: _ensure_tables + _clean_tasks fixture handles DB state across test runs"

patterns-established:
  - "File upload validation: _validate_upload_file() shared between preview and confirm"
  - "json_module alias avoids collision with fastapi/starlette imports"

requirements-completed: [IMPT-01, IMPT-03]

# Metrics
duration: 12min
completed: 2026-04-08
---

# Phase 71 Plan 01: Import Preview and Confirm Endpoints Summary

**Two-phase Excel import: POST /import/preview returns row-level validation, POST /import/confirm atomically creates Tasks in a single db.begin() transaction**

## Performance

- **Duration:** 12 min
- **Started:** 2026-04-08T06:47:20Z
- **Completed:** 2026-04-08T06:59:30Z
- **Tasks:** 1 (TDD: RED + GREEN)
- **Files modified:** 2

## Accomplishments
- POST /tasks/import/preview parses .xlsx and returns per-row validation (valid/error status, row_number, data, errors)
- POST /tasks/import/confirm batch-creates Tasks atomically using async with db.begin()
- Both endpoints validate file format (.xlsx), size (5MB limit), and non-empty content
- 9 unit tests covering all acceptance criteria including rollback verification

## Task Commits

Each task was committed atomically:

1. **Task 1 RED: Failing tests for import endpoints** - `cfd0d11` (test)
2. **Task 1 GREEN: Import preview and confirm implementation** - `08f9e0c` (feat)

_Note: TDD task with separate RED and GREEN commits_

## Files Created/Modified
- `backend/api/routes/tasks.py` - Added import_preview, import_confirm endpoints and _validate_upload_file helper
- `backend/tests/unit/test_import_endpoints.py` - 9 unit tests for both endpoints (created)

## Decisions Made
- confirm re-parses file on each call (stateless) rather than caching server state, per D-08 decision
- Used `json as json_module` alias to prevent naming collision with FastAPI/Starlette imports
- assertions key is popped from parsed data and renamed to external_assertions for correct column mapping
- Test fixture uses asyncio.new_event_loop() for DB setup/cleanup since TestClient is synchronous

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Adapted rollback test for SQLite leniency**
- **Found during:** Task 1 (test_confirm_rollback_on_error)
- **Issue:** Plan suggested using a 201-char name to trigger DB constraint, but SQLite does not enforce String(200) length at INSERT time
- **Fix:** Used Task.__init__ mock to simulate DB error on second row, with raise_server_exceptions=False on TestClient
- **Files modified:** backend/tests/unit/test_import_endpoints.py
- **Verification:** All 9 tests pass, rollback verified by checking task count unchanged

**2. [Rule 3 - Blocking] Added DB isolation fixture for test independence**
- **Found during:** Task 1 (test_confirm_creates_tasks)
- **Issue:** Tests failed with "no such table: tasks" when run after other test files that drop tables in conftest.py db_session fixture
- **Fix:** Added autouse _setup_db fixture that creates tables and cleans Task rows before/after each test
- **Files modified:** backend/tests/unit/test_import_endpoints.py
- **Verification:** Tests pass both independently and alongside test_excel_parser.py

---

**Total deviations:** 2 auto-fixed (both Rule 3 blocking)
**Impact on plan:** Both auto-fixes necessary for test correctness. No scope creep.

## Issues Encountered
- Test isolation with shared SQLite database required explicit table creation and row cleanup fixture

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Both import endpoints ready for frontend integration in Plan 71-02
- Preview endpoint returns structured JSON matching UI requirements (IMPT-02)
- Confirm endpoint creates draft tasks matching manual creation flow
- Frontend needs to build upload UI that calls these endpoints

---
*Phase: 71-批量导入工作流*
*Completed: 2026-04-08*

## Self-Check: PASSED

- FOUND: backend/api/routes/tasks.py
- FOUND: backend/tests/unit/test_import_endpoints.py
- FOUND: .planning/phases/71-批量导入工作流/71-01-SUMMARY.md
- FOUND: cfd0d11 (test commit)
- FOUND: 08f9e0c (feat commit)
