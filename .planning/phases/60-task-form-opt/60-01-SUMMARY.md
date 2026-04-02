---
phase: 60-task-form-opt
plan: 01
subsystem: api
tags: [cleanup, sqlite, fastapi, pydantic, sqlalchemy]

# Dependency graph
requires:
  - phase: prior
    provides: api_assertions feature code that needs removal
provides:
  - Clean backend with zero api_assertions references
  - API contract updated (no api_assertions in task CRUD, runs, or reports)
affects: [60-02-PLAN, frontend-task-form]

# Tech tracking
tech-stack:
  added: []
  patterns: []

key-files:
  created: []
  modified:
    - backend/db/schemas.py
    - backend/db/models.py
    - backend/db/repository.py
    - backend/api/routes/runs.py
    - backend/core/report_service.py
    - backend/api/routes/reports.py
    - backend/tests/unit/test_browser_cleanup.py

key-decisions:
  - "Kept ui_assertion_results in report data as alias for assertion_results for backward compatibility"
  - "Added AssertionResultRepository as top-level variable in run_agent_background after removing api_assertions block"

patterns-established: []

requirements-completed: [FORM-02]

# Metrics
duration: 9min
completed: 2026-04-02
---

# Phase 60 Plan 01: Backend api_assertions Cleanup Summary

**Removed all backend api_assertions feature traces: service file, schema fields, model column, execution logic, report computation, and 3 test files**

## Performance

- **Duration:** 9 min
- **Started:** 2026-04-02T12:53:07Z
- **Completed:** 2026-04-02T13:02:33Z
- **Tasks:** 2
- **Files modified:** 10 (7 modified, 3 deleted)

## Accomplishments
- Deleted api_assertion_service.py (262 lines) and all associated test files (730+ lines of tests)
- Removed api_assertions field from TaskBase, TaskUpdate, TaskResponse schemas and SSEApiAssertionEvent class
- Removed api_assertions column from Task model and serialization methods from repository
- Cleaned runs.py: removed import, parameter, JSON parsing, and entire 75-line execution block
- Cleaned report_service.py: removed api/ui assertion separation, api_pass_rate, and API assertion timeline generation
- Cleaned reports.py route: removed api_assertion_results and api_pass_rate from response
- Verified zero api_assertion references remain in entire backend via grep

## Task Commits

Each task was committed atomically:

1. **Task 1: Delete api_assertion_service.py, clean schemas/models/repository, drop DB column** - `9f2168d` (feat)
2. **Task 2: Clean runs.py execution logic, report_service.py, reports.py route, and test files** - `ce221e6` (feat)

## Files Created/Modified
- `backend/core/api_assertion_service.py` - DELETED (262 lines removed)
- `backend/db/schemas.py` - Removed api_assertions fields, SSEApiAssertionEvent, api_pass_rate
- `backend/db/models.py` - Removed api_assertions column from Task model
- `backend/db/repository.py` - Removed _serialize/_deserialize_api_assertions methods
- `backend/api/routes/runs.py` - Removed import, parameter, execution block, JSON parsing
- `backend/core/report_service.py` - Removed assertion separation, api timeline, api_pass_rate
- `backend/api/routes/reports.py` - Removed api_assertion_results and api_pass_rate from response
- `backend/tests/unit/test_api_assertion_service.py` - DELETED (580 lines)
- `backend/tests/integration/test_api_assertion_integration.py` - DELETED (150 lines)
- `backend/tests/api/routes/test_runs_assertion_integration.py` - DELETED (242 lines)
- `backend/tests/unit/test_browser_cleanup.py` - Removed api_assertions=None parameter

## Decisions Made
- Kept `ui_assertion_results` key in report data dict as alias for `assertion_results` to maintain backward compatibility with any existing frontend code
- Added `AssertionResultRepository` as a top-level variable in `run_agent_background` (was previously inside the api_assertions block) since it is still needed for UI assertion sequence number updates

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] AssertionResultRepository missing in run_agent_background**
- **Found during:** Task 2 (cleaning runs.py execution logic)
- **Issue:** Removing the api_assertions block also removed `assertion_result_repo = AssertionResultRepository(session)` which was used by the UI assertion evaluation block for `update_sequence_number`
- **Fix:** Added `assertion_result_repo = AssertionResultRepository(session)` as a top-level variable alongside the other repository instantiations
- **Files modified:** backend/api/routes/runs.py
- **Verification:** grep confirms assertion_result_repo is still referenced, imports clean, tests pass
- **Committed in:** ce221e6 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Necessary fix - the variable was co-located inside the api_assertions block but used elsewhere. Moving it to top-level is correct.

## Issues Encountered
- Database was empty (no tables), so DROP COLUMN was not needed - column will simply not be created on next init_db()
- 3 pre-existing test failures unrelated to this change (test_external_precondition_bridge_assertion, test_agent_service, test_assertion_service) - documented as out of scope

## Next Phase Readiness
- Backend is clean of all api_assertions references, ready for frontend cleanup (60-02-PLAN)
- API contract changed: task CRUD no longer includes api_assertions field
- Report detail response no longer includes api_assertion_results or api_pass_rate

---
*Phase: 60-task-form-opt*
*Completed: 2026-04-02*

## Self-Check: PASSED

- All 7 modified files exist on disk
- All 4 deleted files confirmed absent
- Both task commits (9f2168d, ce221e6) found in git log
