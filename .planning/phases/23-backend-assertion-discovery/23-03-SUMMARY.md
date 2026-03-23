---
phase: 23-backend-assertion-discovery
plan: 03
subsystem: api
tags: [fastapi, pydantic, assertions, external-bridge, tdd]

requires:
  - phase: 23-backend-assertion-discovery
    provides: Assertion method discovery functions in external_precondition_bridge.py

provides:
  - GET /api/external-assertions/methods endpoint
  - AssertionMethodsResponse Pydantic model with headers_options field
  - 7 tests for assertion API coverage

affects:
  - Phase 24 (Frontend Assertion UI) - uses this API for method selection
  - Phase 25 (Assertion Execution Engine) - consumes assertion method info

tech-stack:
  added: []
  patterns:
    - FastAPI router with Pydantic response models
    - 503 HTTPException pattern for external module unavailability
    - TDD with pytest and mocking

key-files:
  created:
    - backend/api/routes/external_assertions.py
    - backend/tests/api/test_external_assertions_api.py
  modified:
    - backend/api/main.py

key-decisions:
  - "Fixed headers_options list: main, idle, vice, special, platform, super, camera"
  - "Response structure mirrors external_data_methods.py with additional headers_options field"
  - "Pydantic models include data_options and parameters with options for UI dropdowns"

patterns-established:
  - "Assertion API pattern: same structure as external_data_methods API"
  - "Error handling: 503 with message, reason, and fix suggestion"

requirements-completed: [DISC-05]

duration: 6min
completed: "2026-03-20"
---

# Phase 23 Plan 03: External Assertions API Summary

**GET /api/external-assertions/methods endpoint exposing assertion methods with headers_options, data_options, and parameter options for frontend configuration**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-20T05:21:43Z
- **Completed:** 2026-03-20T05:27:42Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Created external_assertions.py route file following external_data_methods.py pattern
- Added headers_options field with 7 fixed identifier strings for header selection
- Implemented AssertionMethodsResponse with data_options and parameters with options
- Registered route in main.py with /api prefix
- All 7 integration tests pass covering 503 error, 200 response, headers_options, and total count

## Task Commits

Each task was committed atomically:

1. **Task 1: Create external_assertions.py route file with Pydantic models** - `9806b82` (test)
2. **Task 2: Register route in main.py and verify end-to-end** - `3d70e54` (feat)

## Files Created/Modified
- `backend/api/routes/external_assertions.py` - New route file with GET /methods endpoint and Pydantic models
- `backend/tests/api/test_external_assertions_api.py` - 7 integration tests for assertion API
- `backend/api/main.py` - Route registration with /api prefix

## Decisions Made
- Fixed headers_options list of 7 identifiers (main, idle, vice, special, platform, super, camera)
- Response structure mirrors external_data_methods.py for consistency
- Added headers_options field to AssertionMethodsResponse for frontend header selection dropdown
- Parameters include options field with value/label pairs for UI dropdowns

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None - implementation followed external_data_methods.py pattern exactly.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- API endpoint ready for Phase 24 (Frontend Assertion UI) to consume
- headers_options field provides header identifier list for dropdown
- data_options field provides method variant options for each assertion
- parameters with options field provides i/j/k parameter dropdown options

## Self-Check: PASSED

- [x] backend/api/routes/external_assertions.py exists
- [x] backend/tests/api/test_external_assertions_api.py exists
- [x] external_assertions.router registration in main.py verified
- [x] commit 9806b82 exists
- [x] commit 3d70e54 exists
- [x] All 7 tests pass

---
*Phase: 23-backend-assertion-discovery*
*Completed: 2026-03-20*
