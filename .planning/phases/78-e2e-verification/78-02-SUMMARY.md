---
phase: 78-e2e-verification
plan: 02
subsystem: testing
tags: [regression, login_role, test-flow-service, build_login_prefix, step-ordering]

# Dependency graph
requires:
  - phase: 77-01
    provides: TestFlowService with build_login_prefix and _build_description
  - phase: 77-02
    provides: login_role branching in runs.py with AccountService integration
provides:
  - Core regression test suite verifying login_role=None path and report step ordering
  - 5 regression tests in TestCoreRegression class
affects: [78-e2e-verification, future login_role changes]

# Tech tracking
tech-stack:
  added: []
  patterns: [unittest.mock.patch + AsyncMock pattern for run_agent_background testing]

key-files:
  created:
    - backend/tests/integration/test_regression_core.py
  modified: []

key-decisions:
  - "Inline mock setup in each test (no helper) to avoid Python 3.11 limitations with tuple unpacking in with statements"
  - "PreconditionResultRepository.create mocked as AsyncMock since the real method is async"
  - "Tests 3 and 4 test TestFlowService directly without mocking (pure function testing)"

patterns-established:
  - "Standard mock pattern for run_agent_background: patch async_session, AgentService, ReportService, AssertionService, repos, event_manager with AsyncMock publish"

requirements-completed: [FLOW-03, FLOW-04, CACHE-01, ACCT-04]

# Metrics
duration: 6min
completed: 2026-04-12
---

# Phase 78 Plan 02: Core Regression Tests Summary

**5 regression tests verifying login_role=None zero-regression path and login step ordering in report generation**

## Performance

- **Duration:** 6 min
- **Started:** 2026-04-12T02:59:45Z
- **Completed:** 2026-04-12T03:06:26Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments
- Confirmed login_role=None tasks pass through without any login prefix injection (no "打开", "登录按钮", "登录成功" in task text)
- Confirmed original task description is preserved exactly when login_role=None (no prefix, no step renumbering, no variable substitution)
- Verified login steps appear before business steps in TestFlowService._build_description output with correct step number offset (+5)
- Verified build_login_prefix produces correct 5-line sequential output with proper content
- Confirmed preconditions execute correctly when login_role=None (no interference from login_role branching)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create core regression tests** - `ac280f8` (test)

## Files Created/Modified
- `backend/tests/integration/test_regression_core.py` - 5 regression tests for login_role=None path and report step ordering

## Decisions Made
- Inline mock setup in each test rather than using a helper function, avoiding Python 3.11 limitation where tuple unpacking with `as` aliases in `with` statements is not supported
- Tests 3-4 (step ordering and prefix sequence) use direct TestFlowService/build_login_prefix calls since they are pure functions requiring no mocking
- Test 5 (preconditions) requires PreconditionResultRepository.create to be AsyncMock since the real repository method is async

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Removed dead helper function causing SyntaxError**
- **Found during:** Task 1 (test file creation)
- **Issue:** `_apply_mocks` helper used `as` aliases inside a tuple return from `with` statement, which is invalid Python 3.11 syntax
- **Fix:** Removed the unused helper function; used inline mock setup pattern matching existing tests
- **Files modified:** backend/tests/integration/test_regression_core.py
- **Verification:** All 5 tests pass
- **Committed in:** ac280f8

**2. [Rule 1 - Bug] Fixed mock setup -- event_manager.publish must be AsyncMock**
- **Found during:** Task 1 (test execution)
- **Issue:** Initial helper-based approach created pre-configured mocks but patch `as` rebinding replaced them with plain MagicMock lacking AsyncMock publish
- **Fix:** Switched to inline mock setup where each `as` variable is configured after patch creation (same pattern as existing tests)
- **Files modified:** backend/tests/integration/test_regression_core.py
- **Verification:** All 5 tests pass
- **Committed in:** ac280f8

**3. [Rule 1 - Bug] PreconditionResultRepository.create must be AsyncMock**
- **Found during:** Task 1 (test 5 execution)
- **Issue:** `precondition_result_repo.create` is awaited in runs.py but mock was plain MagicMock
- **Fix:** Set `mock_pr.create = AsyncMock()` for the precondition test
- **Files modified:** backend/tests/integration/test_regression_core.py
- **Verification:** Test 5 now passes
- **Committed in:** ac280f8

---

**Total deviations:** 3 auto-fixed (all Rule 1 - bugs in test setup)
**Impact on plan:** All auto-fixes necessary for test correctness. No scope creep.

## Issues Encountered
- Mock setup patterns for async code require careful attention to which methods are awaited vs synchronous. Followed the established pattern from test_runs_login_role_integration.py.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All 10 regression/integration tests pass (5 existing + 5 new)
- login_role=None path fully verified for zero regression
- Report step ordering verified for login-before-business sequence
- Ready for E2E verification or further feature development

---
*Phase: 78-e2e-verification*
*Completed: 2026-04-12*
