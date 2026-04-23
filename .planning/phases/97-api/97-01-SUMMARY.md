---
phase: 97-api
plan: 01
subsystem: api
tags: [fastapi, pytest, playwright, path-traversal, code-viewer]

# Dependency graph
requires:
  - phase: 88-auth-cleanup
    provides: "self_healing_runner with generated_code_path storage"
provides:
  - "GET /runs/{run_id}/code endpoint returning line-numbered code text"
  - "TaskUpdate.status expanded to accept 'success' value"
  - "Path traversal protection via _validate_code_path helper"
  - "5 unit tests for CODE-01 code endpoint"
affects: [98-frontend]

# Tech tracking
tech-stack:
  added: []
  patterns: ["FastAPI dependency_overrides for test injection", "Path.resolve() containment check for path traversal"]

key-files:
  created:
    - backend/tests/unit/test_code_api.py
  modified:
    - backend/db/schemas.py
    - backend/api/routes/runs.py

key-decisions:
  - "Used FastAPI app.dependency_overrides instead of patch() for test injection (patch does not affect resolved Depends)"
  - "Path traversal check runs before file existence check in _validate_code_path"
  - "Patched _validate_code_path in success test to decouple from CWD-dependent outputs/ resolution"

patterns-established:
  - "Module-level helper functions (_format_code_with_line_numbers, _validate_code_path) for endpoint logic"
  - "PlainTextResponse for code content with text/plain content-type"

requirements-completed: [CODE-01]

# Metrics
duration: 8min
completed: 2026-04-23
---

# Phase 97 Plan 01: Code API Endpoint Summary

**GET /runs/{run_id}/code endpoint returning line-numbered Python code with path traversal protection and TaskUpdate schema expansion**

## Performance

- **Duration:** 8 min
- **Started:** 2026-04-23T12:44:14Z
- **Completed:** 2026-04-23T12:52:24Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Created GET /runs/{run_id}/code endpoint returning line-numbered Playwright code as text/plain
- Added path traversal protection via _validate_code_path with Path.resolve() containment check
- Expanded TaskUpdate.status pattern to accept "success" alongside "draft" and "ready"
- Wrote 5 unit tests covering success, no code, file not found, path traversal, and run not found cases

## Task Commits

Each task was committed atomically:

1. **Task 1: Expand TaskUpdate schema + create test scaffold** - `3d6825a` (test)
2. **Task 2: Implement GET /runs/{run_id}/code endpoint** - `011afca` (feat)

## Files Created/Modified
- `backend/db/schemas.py` - Expanded TaskUpdate.status pattern from `^(draft|ready)$` to `^(draft|ready|success)$`
- `backend/api/routes/runs.py` - Added GET /{run_id}/code endpoint, _format_code_with_line_numbers helper, _validate_code_path helper, PlainTextResponse import
- `backend/tests/unit/test_code_api.py` - 5 unit tests (137 lines) for CODE-01 using FastAPI dependency_overrides

## Decisions Made
- Used FastAPI `app.dependency_overrides` for test injection instead of `unittest.mock.patch` -- patch does not affect already-resolved `Depends()` references
- Patched `_validate_code_path` in success test to decouple from CWD-dependent `outputs/` resolution (tests should not depend on project directory structure)
- Path traversal check (`startswith` on resolved paths) runs before file existence check -- any path outside outputs/ is rejected regardless of whether the file exists

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Fixed test URL prefix missing /api**
- **Found during:** Task 2 (running tests after endpoint implementation)
- **Issue:** Plan test code used `/runs/{run_id}/code` but the app mounts runs router under `/api` prefix
- **Fix:** Changed all test URLs to `/api/runs/{run_id}/code`
- **Files modified:** backend/tests/unit/test_code_api.py
- **Verification:** Tests pass after URL correction
- **Committed in:** 011afca (Task 2 commit)

**2. [Rule 3 - Blocking] Switched from patch() to dependency_overrides for DI mocking**
- **Found during:** Task 2 (debugging test_get_code_success 404 response)
- **Issue:** `patch("backend.api.routes.runs.get_run_repo")` does not affect FastAPI's already-resolved `Depends()` calls
- **Fix:** Used `app.dependency_overrides[get_run_repo]` to properly override FastAPI dependency injection
- **Files modified:** backend/tests/unit/test_code_api.py
- **Verification:** All 5 tests pass with dependency_overrides approach
- **Committed in:** 011afca (Task 2 commit)

**3. [Rule 3 - Blocking] Adjusted file_not_found test to use outputs/ relative path**
- **Found during:** Task 2 (test_get_code_file_not_found returned 403 instead of 404)
- **Issue:** _validate_code_path checks path traversal before file existence; `/nonexistent/path/test.py` fails traversal first
- **Fix:** Changed test path to `outputs/nonexistent_test_file.py` (passes traversal check but fails existence check)
- **Files modified:** backend/tests/unit/test_code_api.py
- **Verification:** test_get_code_file_not_found returns 404 as expected
- **Committed in:** 011afca (Task 2 commit)

---

**Total deviations:** 3 auto-fixed (3 blocking)
**Impact on plan:** All fixes were test infrastructure adjustments, no scope creep or architectural changes.

## Issues Encountered
- Global exception handler wraps HTTPException detail in `{"success": false, "error": {"message": ...}}` format, not standard `{"detail": ...}`. Tests adjusted to check `error.message` instead.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- GET /runs/{run_id}/code endpoint ready for Phase 98 frontend CodeViewerModal consumption
- TaskUpdate schema ready for STATUS-01 "success" status marking
- 5 unit tests provide regression coverage for CODE-01

---
*Phase: 97-api*
*Completed: 2026-04-23*

## Self-Check: PASSED
- FOUND: backend/tests/unit/test_code_api.py
- FOUND: .planning/phases/97-api/97-01-SUMMARY.md
- FOUND: 3d6825a (Task 1 commit)
- FOUND: 011afca (Task 2 commit)
- FOUND: TaskUpdate pattern expansion in backend/db/schemas.py
- FOUND: get_run_code endpoint in backend/api/routes/runs.py
- FOUND: _validate_code_path helper in backend/api/routes/runs.py
