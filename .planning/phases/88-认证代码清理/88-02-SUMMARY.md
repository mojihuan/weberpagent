---
phase: 88-认证代码清理
plan: 02
subsystem: testing
tags: [auth, cleanup, dead-code, test-cleanup, mock-refactor]

# Dependency graph
requires:
  - phase: 88-认证代码清理
    plan: 01
    provides: Clean production code (auth_service, agent_service, self_healing_runner) with auth_session_factory deleted
provides:
  - Test files aligned with Plan 01 production code cleanup
  - No test references to deleted auth_session_factory or run_simple
  - Unit tests mocking current programmatic login path (pre_navigate + create_browser_session)
affects: [test_auth_service, test_runs_login_role_integration, test_self_healing_runner, test_agent_service]

# Tech tracking
tech-stack:
  added: []
  patterns: [mock-pre_navigate-instead-of-auth_session_factory, mock-_get_storage_state_for_role-module-function]

key-files:
  created: []
  modified:
    - backend/tests/unit/test_auth_service.py
    - backend/tests/unit/test_runs_login_role_integration.py
    - backend/tests/unit/test_self_healing_runner.py
    - backend/tests/test_agent_service.py

key-decisions:
  - "Deleted entire e2e test directory (conftest.py fixtures only served deleted E2E tests)"
  - "Updated test 9 (preinjection_failure) assertion to match new log format from runs.py line 194"

patterns-established:
  - "Integration tests for runs.py mock create_browser_session + pre_navigate instead of auth_session_factory"

requirements-completed: [CLEAN-01, CLEAN-02]

# Metrics
duration: 11min
completed: 2026-04-21
---

# Phase 88 Plan 02: Test Cleanup Summary

**Aligned test suite with Plan 01 auth cleanup: deleted E2E tests, replaced auth_session_factory mocks with pre_navigate/create_browser_session mocks, 27 unit tests pass**

## Performance

- **Duration:** 11 min
- **Started:** 2026-04-21T01:38:27Z
- **Completed:** 2026-04-21T01:49:25Z
- **Tasks:** 2
- **Files modified:** 7 (4 modified, 3 deleted + 1 directory removed)

## Accomplishments
- Deleted 3 E2E test files (test_auth_roles, test_batch_injection, test_compat_regression) and entire e2e test directory including conftest.py
- Deleted integration test_agent_service.py (both tests called deleted run_simple method)
- Removed test_run_simple_mock from test_agent_service.py
- Removed build_storage_state, get_storage_state_for_role, and all 3 create_authenticated_session tests from test_auth_service.py
- Updated all 10 tests in test_runs_login_role_integration.py to mock pre_navigate/create_browser_session instead of auth_session_factory
- Updated 5 tests in test_self_healing_runner.py to mock _get_storage_state_for_role module function instead of auth_service.get_storage_state_for_role

## Task Commits

Each task was committed atomically:

1. **Task 1: Delete E2E test files and remove run_simple tests** - `7e7820a` (refactor)
2. **Task 2: Update unit tests for auth_service and runs.py integration** - `19a02a6` (refactor)

## Files Created/Modified
- `backend/tests/unit/test_auth_service.py` - Removed build_storage_state, get_storage_state_for_role, and create_authenticated_session tests; kept only fetch_token (4 tests) + _extract_origin (2 tests)
- `backend/tests/unit/test_runs_login_role_integration.py` - Rewrote all 10 tests to mock create_browser_session + pre_navigate instead of auth_session_factory
- `backend/tests/unit/test_self_healing_runner.py` - Updated 5 tests to mock _get_storage_state_for_role module-level function instead of auth_service.get_storage_state_for_role
- `backend/tests/test_agent_service.py` - Removed test_run_simple_mock; test_agent_service_creation preserved
- `backend/tests/e2e/test_auth_roles.py` - DELETED
- `backend/tests/e2e/test_batch_injection.py` - DELETED
- `backend/tests/e2e/test_compat_regression.py` - DELETED
- `backend/tests/e2e/conftest.py` - DELETED
- `backend/tests/e2e/__init__.py` - DELETED
- `backend/tests/e2e/` - DIRECTORY REMOVED
- `backend/tests/integration/test_agent_service.py` - DELETED

## Decisions Made
- Deleted entire e2e test directory since conftest.py fixtures (erp_base_url, auth_service, skip_if_erp_unreachable) only served the 3 deleted E2E test files
- Updated test 9 (preinjection_failure_logs_warning_and_fallback) log assertion to match current runs.py format ("代码登录回退" instead of old "Cookie预注入失败" format)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Pre-existing test_run_with_callback failure (TypeError: missing run_id argument) -- out of scope, not caused by this plan's changes

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- All test files aligned with Plan 01 production code cleanup
- No test references to deleted auth_session_factory module
- No test references to deleted run_simple method
- Phase 88 (认证代码清理) is now complete

---
*Phase: 88-认证代码清理*
*Completed: 2026-04-21*

## Self-Check: PASSED

- All 4 modified test files exist and are valid
- 3 E2E test files confirmed deleted
- integration/test_agent_service.py confirmed deleted
- e2e directory confirmed removed
- Commit 7e7820a (Task 1) found in git log
- Commit 19a02a6 (Task 2) found in git log
- SUMMARY.md file exists at expected path
