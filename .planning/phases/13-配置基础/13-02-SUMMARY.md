---
phase: 13-配置基础
plan: 02
subsystem: config
tags: [validation, startup, fastapi, pathlib, ast]

# Dependency graph
requires:
  - phase: 13-01
    provides: weberp_path field in Settings class
provides:
  - validate_weberp_path function for startup validation
  - Clear error messages with solution hints
  - .env.example documentation for WEBSERP_PATH
affects: [14-external-bridge, 15-frontend-selector]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Fail-fast validation at startup
    - ast.parse for shallow syntax validation without code execution
    - [CONFIG ERROR] prefix for user-friendly error messages

key-files:
  created:
    - backend/config/validators.py
    - backend/tests/unit/test_config/conftest.py
    - backend/tests/unit/test_config/test_validators.py
  modified:
    - backend/api/main.py
    - .env.example

key-decisions:
  - "Use ast.parse instead of importlib for syntax validation to avoid executing external code"
  - "Validation only runs when WEBSERP_PATH is set (not None) - optional feature"

patterns-established:
  - "Shallow validation: use ast.parse to validate Python syntax without executing code"
  - "Error messages: use [CONFIG ERROR] prefix with solution suggestions"

requirements-completed: [CONFIG-02]

# Metrics
duration: 55min
completed: 2026-03-17
---

# Phase 13 Plan 02: WEBSERP_PATH Startup Validation Summary

**Startup validation for WEBSERP_PATH with fail-fast behavior, using ast.parse for safe syntax checking and clear error messages with solution hints**

## Performance

- **Duration:** 55 min
- **Started:** 2026-03-17T13:24:34Z
- **Completed:** 2026-03-17T14:19:26Z
- **Tasks:** 4
- **Files modified:** 4

## Accomplishments
- validate_weberp_path function with 4 validation checks (directory, base_prerequisites.py, config/settings.py, syntax)
- FastAPI lifespan integration for startup validation
- Clear error messages with [CONFIG ERROR] prefix and solution hints
- .env.example documentation for WEBSERP_PATH configuration

## Task Commits

Each task was committed atomically:

1. **Task 1: Create test scaffolding** - `552faf0` (test)
2. **Task 2: Implement validate_weberp_path function** - `772afe7` (feat)
3. **Task 3: Add startup validation to FastAPI lifespan** - `8f00871` (feat)
4. **Task 4: Update .env.example** - `3bd10c2` (docs)

## Files Created/Modified
- `backend/config/validators.py` - validate_weberp_path function with 4 validation checks
- `backend/api/main.py` - Startup validation hook in lifespan
- `backend/tests/unit/test_config/conftest.py` - Test fixtures for mock paths
- `backend/tests/unit/test_config/test_validators.py` - 5 unit tests for validation
- `.env.example` - WEBSERP_PATH configuration documentation

## Decisions Made
- Used ast.parse instead of importlib.util.spec_from_file_location for syntax validation because spec_from_file_location does not actually parse/validate the file content
- Validation only runs when WEBSERP_PATH is set (not None) - feature is optional

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed import test to actually validate Python syntax**
- **Found during:** Task 2 (GREEN phase - test_validate_unimportable_module failed)
- **Issue:** importlib.util.spec_from_file_location creates a spec even for files with invalid Python syntax because it doesn't actually parse the file
- **Fix:** Replaced with ast.parse to actually validate Python syntax without executing code
- **Files modified:** backend/config/validators.py
- **Verification:** All 5 tests pass including test_validate_unimportable_module
- **Committed in:** 772afe7 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Necessary fix for correct behavior. No scope creep.

## Issues Encountered
- Test for unimportable module initially failed because spec_from_file_location doesn't validate syntax - fixed by using ast.parse

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Configuration validation foundation complete
- validate_weberp_path ready to be used by ExternalPreconditionBridge (Phase 14)
- All 8 config tests pass (3 from 13-01 + 5 from 13-02)

---
*Phase: 13-配置基础*
*Completed: 2026-03-17*
