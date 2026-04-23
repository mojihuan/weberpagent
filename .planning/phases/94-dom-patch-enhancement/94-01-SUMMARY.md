---
phase: 94-dom-patch-enhancement
plan: 01
subsystem: dom
tags: [browser-use, dom-patch, bbox-filtering, table-cell, ant-design]

# Dependency graph
requires:
  - phase: 68
    provides: "Existing dom_patch.py with _patch_should_exclude_child() and _is_inside_table_cell()"
provides:
  - "_td_child_depth() helper function for counting parent chain distance to td/th"
  - "Extended _patch_should_exclude_child() protecting div/span inside td up to 2 layers"
  - "_TD_CHILD_TAGS and _MAX_TD_CHILD_DEPTH constants"
affects: [94-02, 95, 96]

# Tech tracking
tech-stack:
  added: []
  patterns: ["parent_node chain depth counting for td-child exclusion bypass"]

key-files:
  created: []
  modified:
    - "backend/agent/dom_patch.py"
    - "backend/tests/unit/test_dom_patch.py"

key-decisions:
  - "depth < _MAX_TD_CHILD_DEPTH (strict less-than) ensures depth 0 and 1 are protected, depth 2+ falls through"
  - "_td_child_depth returns None for non-div/span tags to avoid interfering with existing input/label logic"

patterns-established:
  - "parent_node chain depth counting: walk chain incrementing counter until td/th found"
  - "frozenset constants for tag whitelists following _ERP_CLICKABLE_CLASSES pattern"

requirements-completed: [DEPTH-01]

# Metrics
duration: 4min
completed: 2026-04-23
---

# Phase 94 Plan 01: DOM td-child depth protection Summary

**_td_child_depth helper and extended _patch_should_exclude_child to protect div/span inside td up to 2 layers from bbox flattening**

## Performance

- **Duration:** 4 min
- **Started:** 2026-04-23T02:07:26Z
- **Completed:** 2026-04-23T02:12:00Z
- **Tasks:** 1
- **Files modified:** 2

## Accomplishments
- Implemented _td_child_depth() helper counting parent_node chain distance to nearest td/th ancestor
- Extended patched_should_exclude_child() to protect div/span elements inside td up to 2 layers deep (depth < 2)
- Added 11 new unit tests (7 for _td_child_depth, 4 for patched exclusion logic) -- all 33 tests pass

## Task Commits

Each task was committed atomically:

1. **Task 1: TDD - Add _td_child_depth() helper and extend _patch_should_exclude_child()** - `00665e9` (test), `289b525` (feat)

_Note: TDD task has RED (test) and GREEN (feat) commits._

## Files Created/Modified
- `backend/agent/dom_patch.py` - Added _TD_CHILD_TAGS, _MAX_TD_CHILD_DEPTH constants, _td_child_depth() helper, extended patched_should_exclude_child()
- `backend/tests/unit/test_dom_patch.py` - Added MockChainNode, MockSimplifiedNodeWithChain mocks, TestTdChildDepth and TestShouldExcludeChildTdPatch test classes

## Decisions Made
- depth < _MAX_TD_CHILD_DEPTH (strict less-than) ensures depth 0 (direct child) and depth 1 (grandchild) are protected; depth 2+ falls through to original browser-use logic
- _td_child_depth returns None for non-div/span tags to avoid interfering with existing input/label/checkbox logic inside td cells

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed _make_node_in_td test helper depth chain construction**
- **Found during:** Task 1 (GREEN phase - test_span_in_div_in_td_not_excluded failed)
- **Issue:** Original helper used `range(depth_from_td - 1)` which produced wrong chain depth for depth=1 (no intermediate nodes created, target attached directly to td giving depth 0 instead of 1)
- **Fix:** Rewrote helper to use `range(depth_from_td)` creating correct number of intermediate div nodes before the target element
- **Files modified:** backend/tests/unit/test_dom_patch.py
- **Verification:** All 33 tests pass including test_span_in_div_in_td_not_excluded
- **Committed in:** 289b525 (part of feat commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Minor test helper fix, no impact on production code correctness.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- DEPTH-01 complete, ready for Plan 02 (DEPTH-02: td input visibility)
- _td_child_depth can be reused for future td-related DOM patches

## Self-Check: PASSED
- backend/agent/dom_patch.py: FOUND
- backend/tests/unit/test_dom_patch.py: FOUND
- 00665e9 (test commit): FOUND
- 289b525 (feat commit): FOUND

---
*Phase: 94-dom-patch-enhancement*
*Completed: 2026-04-23*
