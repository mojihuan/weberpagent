---
phase: 23-backend-assertion-discovery
plan: 02
subsystem: backend
tags: [assertions, discovery, parsing, metadata-extraction, tdd]

# Dependency graph
requires:
  - phase: 23-01
    provides: load_base_assertions_class() function for loading PcAssert/MgAssert/McAssert
provides:
  - get_assertion_methods_grouped() - returns methods grouped by class name
  - _parse_data_options_from_source() - extracts data options from methods dictionary
  - _parse_param_options() - extracts parameter options from docstring
  - extract_assertion_method_info() - combines all metadata for a method
affects: [24-frontend-assertion-ui, 25-assertion-execution-engine]

# Tech tracking
tech-stack:
  added: []
  patterns: [TDD, source-code-parsing, regex-extraction, module-caching]

key-files:
  created: []
  modified:
    - backend/core/external_precondition_bridge.py
    - backend/tests/unit/test_external_assertion_bridge.py

key-decisions:
  - "Default data_options to ['main'] when parsing fails for graceful degradation"
  - "Use regex pattern (\\d+)([^\\d]+) to parse i/j/k options from docstrings"
  - "Filter internal methods via INTERNAL_ASSERTION_METHODS set"

patterns-established:
  - "Pattern: Parse source code with inspect.getsource() + regex for method metadata"
  - "Pattern: Use caching for discovered methods (_assertion_methods_cache)"
  - "Pattern: Return empty list on error for graceful API responses"

requirements-completed: [DISC-02, DISC-03, DISC-04]

# Metrics
duration: 8min
completed: 2026-03-20
---

# Phase 23 Plan 02: Assertion Method Discovery Summary

**Implemented assertion method discovery with data options and parameter options parsing for PcAssert/MgAssert/McAssert classes**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-20T05:10:25Z
- **Completed:** 2026-03-20T05:18:30Z
- **Tasks:** 3
- **Files modified:** 2

## Accomplishments

- Added `_parse_data_options_from_source()` to extract method data variants from source code
- Added `_parse_param_options()` to parse i/j/k parameter options from docstrings
- Added `get_assertion_methods_grouped()` to return methods grouped by class with full metadata
- Added `extract_assertion_method_info()` to combine description, data_options, and parameters
- Added `INTERNAL_ASSERTION_METHODS` set to filter out utility methods like assert_time, assert_contains

## Task Commits

Each task was committed atomically:

1. **Task 1: Add _parse_data_options_from_source() function** - `822e75c` (test)
2. **Task 2: Add _parse_param_options() function for i/j/k options** - `3bb3fb4` (test)
3. **Task 3: Add extract_assertion_method_info() and get_assertion_methods_grouped()** - `563415c` (feat)

_Note: TDD tasks have test commits for failing tests, then feat commits for implementation_

## Files Created/Modified

- `backend/core/external_precondition_bridge.py` - Added 4 new functions and INTERNAL_ASSERTION_METHODS set
- `backend/tests/unit/test_external_assertion_bridge.py` - Added 12 new tests across 3 test classes

## Decisions Made

- Default `data_options` to `['main']` when parsing fails - ensures graceful degradation
- Use regex pattern `(\d+)([^\d]+)` to parse options like "1待发货 2待取件" from docstrings
- Filter internal methods (assert_time, assert_contains, etc.) via `INTERNAL_ASSERTION_METHODS` set
- Cache discovered methods in `_assertion_methods_cache` for performance

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed test for module unavailability detection**
- **Found during:** Task 3 (get_assertion_methods_grouped tests)
- **Issue:** Original test used monkeypatch to set WEBSERP_PATH to empty string, but .env file still provided the value
- **Fix:** Changed test to directly set `_assertion_import_error` to simulate unavailable module
- **Files modified:** backend/tests/unit/test_external_assertion_bridge.py
- **Verification:** All 16 tests pass
- **Committed in:** 563415c (Task 3 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Minor test adjustment. No scope creep.

## Issues Encountered

None - all tasks executed smoothly following TDD approach.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Assertion method discovery complete with metadata extraction
- Ready for Phase 24 (Frontend Assertion UI) to consume `get_assertion_methods_grouped()` API
- Ready for Phase 25 (Execution Engine) to use extracted metadata for assertion configuration

---
*Phase: 23-backend-assertion-discovery*
*Completed: 2026-03-20*
