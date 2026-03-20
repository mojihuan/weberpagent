---
phase: 23-backend-assertion-discovery
plan: 01
subsystem: backend
tags: [bridge, assertions, discovery, webseleniumerp, caching, lazy-loading]

# Dependency graph
requires:
  - phase: 17-backend-data-bridge
    provides: ExternalPreconditionBridge pattern with lazy loading and caching
provides:
  - load_base_assertions_class() function for loading PcAssert/MgAssert/McAssert
  - Assertion class cache with reset_cache() support
affects: [24-frontend-assertion-ui, 25-assertion-execution-engine]

# Tech tracking
tech-stack:
  added: []
  patterns: [lazy-loading, module-level-cache, bridge-pattern]

key-files:
  created:
    - backend/tests/unit/test_external_assertion_bridge.py
  modified:
    - backend/core/external_precondition_bridge.py

key-decisions:
  - "Follow exact pattern of load_base_params_class() for consistency"
  - "Return dict mapping class names to classes instead of single class"

patterns-established:
  - "Bridge module pattern: lazy load external classes with caching and error handling"
  - "reset_cache() clears all module-level singleton state for test isolation"

requirements-completed: [DISC-01]

# Metrics
duration: 3min
completed: "2026-03-20"
---

# Phase 23 Plan 01: Assertion Class Loading Summary

**Added load_base_assertions_class() function to ExternalPreconditionBridge following the exact pattern established for data method loading, enabling discovery and loading of PcAssert/MgAssert/McAssert classes from webseleniumerp.**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-20T02:56:34Z
- **Completed:** 2026-03-20T02:59:17Z
- **Tasks:** 1
- **Files modified:** 2

## Accomplishments

- Added assertion class loading capability with lazy loading and caching
- Implemented load_base_assertions_class() returning dict of PcAssert/MgAssert/McAssert
- Added cache variables _assertion_classes_cache and _assertion_import_error
- Updated reset_cache() to clear assertion-related state for test isolation
- Created comprehensive unit tests following TDD approach (4 tests, all passing)

## Task Commits

Each task was committed atomically:

1. **Task 1: Add assertion class cache variables and load function** - `8f698e8` (feat)

## Files Created/Modified

- `backend/core/external_precondition_bridge.py` - Added load_base_assertions_class(), cache variables, reset_cache() update
- `backend/tests/unit/test_external_assertion_bridge.py` - Unit tests for assertion class discovery (4 tests)

## Decisions Made

- **Return dict instead of single class:** Unlike load_base_params_class() which returns a single class, load_base_assertions_class() returns a dict mapping class names to classes because there are three assertion classes (PcAssert, MgAssert, McAssert) that need to be discovered together.
- **Follow exact pattern:** Replicated the lazy loading, caching, and error handling pattern from load_base_params_class() for consistency and maintainability.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - implementation followed established patterns without issues.

## User Setup Required

None - no external service configuration required for this plan.

## Next Phase Readiness

- Assertion class loading is ready for use by subsequent plans
- Plan 02 can now implement get_assertion_methods_grouped() using load_base_assertions_class()
- Plan 03 can implement the API endpoint /external-assertions/methods

---

*Phase: 23-backend-assertion-discovery*
*Completed: 2026-03-20*
