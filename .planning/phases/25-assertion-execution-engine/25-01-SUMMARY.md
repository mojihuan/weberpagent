---
phase: 25-assertion-execution-engine
plan: 01
subsystem: api
tags: [assertion, execution, headers, timeout, asyncio]

# Dependency graph
requires:
  - phase: 24-frontend-assertion-ui
    provides: AssertionConfig structure for assertion execution
provides:
  - resolve_headers() function for header identifier resolution
  - execute_assertion_method() async function with timeout protection
  - _parse_assertion_error() helper for field-level result extraction
affects: [assertion-execution, api-endpoints]

# Tech tracking
tech-stack:
  added: []
  patterns: [async-executor-with-timeout, header-resolution, assertion-error-parsing]

key-files:
  created:
    - backend/tests/core/test_external_precondition_bridge_assertion.py
  modified:
    - backend/core/external_precondition_bridge.py

key-decisions:
  - "Use LoginApi singleton pattern for cached header resolution"
  - "30-second default timeout via asyncio.wait_for for assertion execution"
  - "Parse AssertionError messages with regex to extract field-level comparison results"

patterns-established:
  - "Header resolution via identifier strings ('main', 'vice', etc.) to actual auth tokens"
  - "Structured assertion result with success/passed/field_results/error/error_type/duration"

requirements-completed: [EXEC-01, EXEC-02, EXEC-03]

# Metrics
duration: 8min
completed: 2026-03-20
---

# Phase 25 Plan 01: Assertion Execution Core Functions Summary

**resolve_headers() and execute_assertion_method() functions with 30-second timeout protection and LoginApi header resolution**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-20T08:17:55Z
- **Completed:** 2026-03-20T08:26:00Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- resolve_headers() resolves header identifiers ('main', 'vice', etc.) to actual auth token dicts via LoginApi
- execute_assertion_method() executes assertion methods with 30-second timeout via asyncio.wait_for
- _parse_assertion_error() extracts field-level comparison results from Chinese assertion error messages

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement resolve_headers() function** - `10ac724` (feat)
2. **Task 2: Implement execute_assertion_method() with timeout** - `3f94668` (feat)

## Files Created/Modified
- `backend/core/external_precondition_bridge.py` - Added resolve_headers(), execute_assertion_method(), _parse_assertion_error(), _get_login_api(), VALID_HEADER_IDENTIFIERS constant
- `backend/tests/core/test_external_precondition_bridge_assertion.py` - Comprehensive unit tests for all assertion execution functions (13 tests)

## Decisions Made
- Used LoginApi singleton pattern with caching for efficient header resolution
- 30-second default timeout for assertion execution (configurable via parameter)
- Regex pattern for parsing Chinese field comparison error messages from AssertionError
- VALID_HEADER_IDENTIFIERS constant contains all 7 identifiers: main, idle, vice, special, platform, super, camera

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed regex pattern in _parse_assertion_error()**
- **Found during:** Task 2 (execute_assertion_method tests)
- **Issue:** Original regex pattern used optional quotes that failed to capture actual values
- **Fix:** Changed pattern to use mandatory quotes for expected/actual values
- **Files modified:** backend/core/external_precondition_bridge.py
- **Verification:** test_parses_field_comparison_message passes
- **Committed in:** 3f94668 (Task 2 commit)

**2. [Rule 1 - Bug] Fixed mock setup in test_resolves_headers_before_calling_assertion**
- **Found during:** Task 2 (execute_assertion_method tests)
- **Issue:** Mock class not properly configured, causing ValueError on unpacking
- **Fix:** Properly instantiate mock_class outside patch and configure return_value correctly
- **Files modified:** backend/tests/core/test_external_precondition_bridge_assertion.py
- **Verification:** test_resolves_headers_before_calling_assertion passes
- **Committed in:** 3f94668 (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (2 bug fixes)
**Impact on plan:** Both fixes were test implementation issues. No scope creep.

## Issues Encountered
- Initial regex pattern failed to match Chinese assertion error format - fixed by requiring quotes in pattern
- Mock setup in test required proper class instantiation outside of patch context

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Assertion execution core functions complete with full test coverage
- Ready for API endpoint integration (25-02)
- Headers resolution blocker resolved via resolve_headers() function

---
*Phase: 25-assertion-execution-engine*
*Completed: 2026-03-20*
