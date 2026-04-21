---
phase: 91-测试代码修复
plan: 02
subsystem: testing
tags: [pytest, sys.modules, sys.path, cache-isolation, sqlalchemy, bridge]

# Dependency graph
requires:
  - phase: 91-01
    provides: Top-level conftest.py with db_session fixture and autouse reset_cache
provides:
  - sys.modules and sys.path cleanup in precondition_service and e2e test autouse fixtures
  - Early return in bridge load functions when WEBSERP_PATH not configured
  - reset_cache() clears common.* and api.* from sys.modules
  - TaskRepository.create() correctly handles assertions=None
affects: [test-suite, future-phases]

# Tech tracking
tech-stack:
  added: []
patterns: [sys.path-restore-in-autouse, early-return-on-unconfigured-path, pop-assertions-before-orm-create]

key-files:
  created: []
  modified:
    - backend/tests/unit/test_precondition_service.py
    - backend/tests/integration/test_e2e_precondition_integration.py
    - backend/core/external_precondition_bridge.py
    - backend/db/repository.py

key-decisions:
  - "Bridge load functions (load_pre_front_class, load_base_params_class, _load_assertion_classes, _get_login_api) return early when WEBSERP_PATH is empty, preventing stale sys.modules from satisfying imports"
  - "reset_cache() clears common.* and api.* from sys.modules to prevent cross-test pollution from webseleniumerp imports"
  - "TaskRepository.create() uses pop('assertions') instead of get+del to safely remove relationship-colliding key"
  - "E2e precondition integration autouse fixture snapshots and restores sys.path alongside sys.modules cleanup"

patterns-established:
  - "Autouse fixtures that modify sys.path MUST snapshot and restore it in teardown"
  - "Bridge load functions must NOT attempt imports when WEBSERP_PATH is unconfigured -- stale sys.modules will satisfy the import"
  - "Pydantic schemas with fields that collide with SQLAlchemy relationship names must be popped from model_dump() before ORM object creation"

requirements-completed: [TEST-04, TEST-05]

# Metrics
duration: 28min
completed: 2026-04-21
---

# Phase 91 Plan 02: Remaining Test Fixtures and Full Suite Green Summary

**sys.modules/sys.path cleanup fixtures, bridge early-return guard, and repository assertions pop -- achieving 876 passed, 0 failed, 0 errors**

## Performance

- **Duration:** 28 min
- **Started:** 2026-04-21T08:25:08Z
- **Completed:** 2026-04-21T08:53:51Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Full test suite green: 876 passed, 0 failed, 0 errors, 1 xfailed (MgAssert known limitation)
- Fixed sys.modules and sys.path pollution from mock module tests in precondition_service and e2e integration
- Added early-return guard in 4 bridge load functions to prevent stale sys.modules imports
- Enhanced reset_cache() to clear common.* and api.* entries from sys.modules
- Fixed TaskRepository.create() TypeError when assertions=None assigned to SQLAlchemy relationship
- D-04 success criterion achieved: zero failures zero errors

## Task Commits

Each task was committed atomically:

1. **Task 1: Fix precondition_service and cache-sensitive test files** - `7547802` (fix)
2. **Task 2: Fix monitored_agent, agent_params, self_healing_runner, and run full suite verification** - `46c11ea` (fix)

## Files Created/Modified
- `backend/tests/unit/test_precondition_service.py` - Added autouse _cleanup_sys_modules fixture with sys.path restore
- `backend/tests/integration/test_e2e_precondition_integration.py` - Added sys.path snapshot/restore to autouse fixture
- `backend/core/external_precondition_bridge.py` - Added early-return in 4 load functions + sys.modules cleanup in reset_cache()
- `backend/db/repository.py` - Fixed TaskRepository.create() to use pop('assertions') instead of get+del

## Decisions Made
- Bridge load functions return early with "WEBSERP_PATH not configured" error when path is empty, preventing stale imports from succeeding
- reset_cache() clears all common.* and api.* from sys.modules since cached imports are invalidated by reset anyway
- E2e integration tests snapshot sys.path before each test and restore after, alongside sys.modules cleanup
- TaskRepository.create() uses dict.pop() to remove 'assertions' before passing to Task() constructor

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] TaskRepository.create() TypeError when assertions=None**
- **Found during:** Task 2 (full suite verification)
- **Issue:** TaskCreate.model_dump() produces assertions=None which is then passed as Task(assertions=None), but Task.assertions is a SQLAlchemy relationship (list-like), not a regular column. None is not list-like, causing TypeError.
- **Fix:** Changed from `if assertions is not None: del task_data["assertions"]` to `task_data.pop("assertions", None)` so the key is always removed before creating the ORM object.
- **Files modified:** backend/db/repository.py
- **Verification:** 36 passed (all previously failing repository, assertion, and report tests now pass)
- **Committed in:** 46c11ea (Task 2 commit)

**2. [Rule 1 - Bug] Bridge load functions import stale modules from sys.modules**
- **Found during:** Task 2 (full suite verification)
- **Issue:** When WEBSERP_PATH is cleared via monkeypatch but sys.path and sys.modules still have entries from prior tests (via configure_external_path), `from common.base_prerequisites import PreFront` succeeds from the stale cache, making is_available() return True when it should return False.
- **Fix:** Added early return in load_pre_front_class, load_base_params_class, _load_assertion_classes, and _get_login_api when settings.weberp_path is empty. Also added sys.modules cleanup in reset_cache() for common.* and api.* entries.
- **Files modified:** backend/core/external_precondition_bridge.py
- **Verification:** 876 passed, 0 failed, 0 errors
- **Committed in:** 46c11ea (Task 2 commit)

**3. [Rule 1 - Bug] E2e integration tests leave sys.path entries from configure_external_path**
- **Found during:** Task 2 (full suite verification)
- **Issue:** test_e2e_precondition_integration.py calls configure_external_path() which adds tmp_path to sys.path. The autouse fixture cleared sys.modules but not sys.path. Subsequent tests could find mock modules via the stale sys.path entry.
- **Fix:** Added sys.path snapshot/restore to the autouse fixture in test_e2e_precondition_integration.py.
- **Files modified:** backend/tests/integration/test_e2e_precondition_integration.py
- **Verification:** Full suite passes with 0 failures
- **Committed in:** 46c11ea (Task 2 commit)

---

**Total deviations:** 3 auto-fixed (all Rule 1 - Bug)
**Impact on plan:** All auto-fixes necessary for achieving D-04 success criterion. No scope creep.

## Issues Encountered
None beyond the documented deviations.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- D-04 success criterion met: full suite green (876 passed, 0 failed, 0 errors, 1 xfailed)
- Phase 91 complete, ready for Phase 92 (DataMethodError fix for webseleniumerp obfuscated method names)
- Known limitation: MgAssert not available in webseleniumerp upstream (1 xfail)

---
*Phase: 91-测试代码修复*
*Completed: 2026-04-21*

## Self-Check: PASSED

- All 4 modified files found on disk
- Both task commits found in git log (7547802, 46c11ea)
- Full suite: 876 passed, 0 failed, 0 errors, 1 xfailed
