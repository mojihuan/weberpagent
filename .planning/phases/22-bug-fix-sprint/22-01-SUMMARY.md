---
phase: 22-bug-fix-sprint
plan: 01
subsystem: testing
tags: [pytest, monkeypatch, test-isolation, mock-signatures]

# Dependency graph
requires:
  - phase: 21-unit-test-coverage
    provides: Unit test infrastructure and patterns
provides:
  - All 16 previously failing tests now pass
  - Test isolation pattern using pytest monkeypatch
  - Mock signature updates for API contract changes
affects: [testing, bug-fix-sprint]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "monkeypatch.setenv('WEBSERP_PATH', '') to override .env file in tests"
    - "get_settings.cache_clear() before tests requiring environment isolation"
    - "reset_cache() after environment changes in bridge module tests"

key-files:
  created: []
  modified:
    - backend/tests/unit/test_external_bridge.py
    - backend/tests/unit/test_browser_cleanup.py
    - backend/tests/unit/test_config/test_settings.py
    - backend/tests/unit/test_config/conftest.py

key-decisions:
  - "Use monkeypatch.setenv with empty string to override .env file values (pydantic-settings reads from both env and .env)"
  - "Accept empty string as equivalent to None for unconfigured weberp_path in settings tests"
  - "Create base_prerequisites.py in common/ subdirectory (correct location per validator logic)"

patterns-established:
  - "Test isolation pattern: monkeypatch.setenv -> get_settings.cache_clear() -> reset_cache() -> test"
  - "Mock signatures must match current API contracts including all optional parameters"

requirements-completed: [BUG-01]

# Metrics
duration: 15min
completed: 2026-03-19
---

# Phase 22 Plan 01: Fix Failing Tests Summary

**Fixed 16 failing tests by ensuring proper test isolation via monkeypatch and updating mock signatures to match current API contracts.**

## Performance

- **Duration:** 15 min
- **Started:** 2026-03-19T12:13:21Z
- **Completed:** 2026-03-19T12:28:00Z
- **Tasks:** 4
- **Files modified:** 4

## Accomplishments
- All 16 previously failing tests now pass
- Established test isolation pattern using pytest monkeypatch for environment variables
- Updated mock signatures to match current API contracts
- Fixed conftest.py fixtures to create files in correct directory structure

## Task Commits

Each task was committed atomically:

1. **Task 1: Fix test_external_bridge.py isolation (7 tests)** - `7e0a5f2` (test)
2. **Task 2: Fix test_browser_cleanup.py mock signatures (2 tests)** - `e20882c` (test)
3. **Task 3: Fix test_config/test_settings.py isolation (3 tests)** - `c7b8634` (test)
4. **Task 4: Fix test_config/conftest.py fixture paths (5 tests)** - `5a8fcfe` (fix)

## Files Created/Modified
- `backend/tests/unit/test_external_bridge.py` - Added monkeypatch isolation for 7 tests expecting unavailable state
- `backend/tests/unit/test_browser_cleanup.py` - Updated mock signatures to include target_url parameter
- `backend/tests/unit/test_config/test_settings.py` - Replaced patch.dict with monkeypatch for environment isolation
- `backend/tests/unit/test_config/conftest.py` - Fixed fixture to create common/base_prerequisites.py in correct location

## Decisions Made
- Use `monkeypatch.setenv('WEBSERP_PATH', '')` to override .env file values since pydantic-settings reads from both environment and .env file
- Accept empty string (`''`) as equivalent to `None` for unconfigured weberp_path in settings tests
- Create `common/base_prerequisites.py` instead of `base_prerequisites.py` at root (matches validator logic)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] pydantic-settings reads from .env file, not just environment**
- **Found during:** Task 1 (test_external_bridge.py isolation)
- **Issue:** Using `monkeypatch.delenv('WEBSERP_PATH')` doesn't work because pydantic-settings also reads from the .env file
- **Fix:** Use `monkeypatch.setenv('WEBSERP_PATH', '')` to set an empty value which overrides the .env file value
- **Files modified:** backend/tests/unit/test_external_bridge.py, backend/tests/unit/test_config/test_settings.py
- **Verification:** All tests pass with proper isolation
- **Committed in:** 7e0a5f2, c7b8634

**2. [Rule 1 - Bug] conftest.py fixtures create files in wrong location**
- **Found during:** Task 4 (test_validators.py tests)
- **Issue:** Fixtures created `base_prerequisites.py` at root level but validator expects `common/base_prerequisites.py`
- **Fix:** Updated fixtures to create `common/` subdirectory and place `base_prerequisites.py` there
- **Files modified:** backend/tests/unit/test_config/conftest.py
- **Verification:** All 5 validator tests pass
- **Committed in:** 5a8fcfe

---

**Total deviations:** 2 auto-fixed (1 blocking, 1 bug)
**Impact on plan:** All auto-fixes necessary for correct test behavior. No scope creep.

## Issues Encountered
- Initial approach using `monkeypatch.delenv` didn't work because pydantic-settings reads from .env file in addition to environment variables. Solution was to use `setenv` with empty string to override.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Test suite now healthy with all 16 previously failing tests passing
- Ready for subsequent bug fix work in Phase 22

---
*Phase: 22-bug-fix-sprint*
*Completed: 2026-03-19*
