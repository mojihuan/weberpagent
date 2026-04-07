---
phase: 68-dom-patch
plan: 02
subsystem: dom-patch
tags: [dom, annotation, serialize-tree, row-identity, failure-tracker, strategy]

# Dependency graph
requires:
  - phase: 68-01
    provides: "_node_annotations sidecar dict, _detect_row_identity(), _failure_tracker"
provides:
  - "_patch_serialize_tree_annotations() combining Patch 6 (row identity comments) and Patch 7 (failure/strategy annotations)"
  - "_detect_row_identity_from_tr() for direct tr child IMEI scanning"
  - "_STRATEGY_NAMES dict for descriptive strategy names in DOM dump output"
affects: [future-phase-agent-prompt-consumption]

# Tech tracking
tech-stack:
  added: []
patterns:
  - "Combined serialize_tree wrapper: single wrapper handles both row identity comments and failure annotations, avoiding multi-layer wrapping chain"
  - "Direct tr scanning: _detect_row_identity_from_tr() for <tr> nodes that are not processed by Patch 4"

key-files:
  created: []
  modified:
    - backend/agent/dom_patch.py
    - backend/tests/unit/test_dom_patch_phase68.py

key-decisions:
  - "_detect_row_identity_from_tr() created separately from _detect_row_identity() because tr nodes are not processed by Patch 4 and have no parent chain to walk"
  - "Failure-based strategy downgrade re-applied live in serialize_tree (tracker may have updated since Patch 4 ran)"
  - "_STRATEGY_NAMES module-level dict for D-03 descriptive names shared across potential future uses"

patterns-established:
  - "Direct tr scanning pattern: for <tr> nodes in serialize_tree, scan td children directly rather than walking parent chain"
  - "Selective annotation pattern: only failed elements (in _failure_tracker) get strategy annotations, unfailed elements stay clean"

requirements-completed: [ROW-02, STRAT-02, ANTI-02]

# Metrics
duration: 10min
completed: 2026-04-07
---

# Phase 68 Plan 02: Serialize Tree Annotation Injection Summary

**Combined Patch 6+7 wrapping DOMTreeSerializer.serialize_tree to inject row identity comments (`<!-- 行: I... -->`) and failure/strategy annotations (`<!-- 行内 input [...] -->`) into DOM dump output**

## Performance

- **Duration:** 10 min
- **Started:** 2026-04-07T03:20:27Z
- **Completed:** 2026-04-07T03:30:27Z
- **Tasks:** 1 (TDD: RED + GREEN)
- **Files modified:** 2

## Accomplishments
- _patch_serialize_tree_annotations() combines Patch 6 (row identity) and Patch 7 (failure/strategy) into a single serialize_tree wrapper
- Row identity comments `<!-- 行: {IMEI} -->` prepended above `<tr>` elements with IMEI in td children
- Failure/strategy annotations `<!-- 行内 input [行: ...] [策略: ...] [已尝试 N 次 模式: ...] -->` appended only for ERP inputs in _failure_tracker
- Unfailed ERP inputs show no strategy annotations (D-04 selective annotation)
- Strategy names use descriptive format per D-03: "1-原生 input", "2-需先 click", "3-evaluate JS"
- Registered in apply_dom_patch() after _patch_assign_interactive_indices()

## Task Commits

Each task was committed atomically:

1. **Task 1 (RED): Failing tests for serialize_tree annotation injection** - `3ea31c7` (test)
2. **Task 1 (GREEN): Implement serialize_tree annotation injection (Patch 6+7)** - `e16f18d` (feat)

## Files Created/Modified
- `backend/agent/dom_patch.py` - Added _detect_row_identity_from_tr(), _STRATEGY_NAMES dict, _patch_serialize_tree_annotations(), registered in apply_dom_patch()
- `backend/tests/unit/test_dom_patch_phase68.py` - 13 new tests: TestRowIdentityComment (3), TestFailureAnnotation (6), TestStrategyNames (3), TestRegistrationInApplyDomPatch (1)

## Decisions Made
- Created _detect_row_identity_from_tr() as a separate helper because _detect_row_identity() walks the parent chain to find a <tr> ancestor, but when called from serialize_tree the node IS the <tr> itself
- Strategy downgrade logic re-applied live in serialize_tree (Pitfall 6 from RESEARCH.md: tracker may have been updated after Patch 4 ran)
- _STRATEGY_NAMES defined as module-level dict for reuse and testability

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed _detect_row_identity failing on <tr> nodes**
- **Found during:** Task 1 (GREEN phase)
- **Issue:** Plan specified calling _detect_row_identity(node) for <tr> elements, but this function walks the parent chain to find a <tr> ancestor. When called on a <tr> node itself, it checks parent_node (which is above the <tr>), never finds the <tr>, and returns None.
- **Fix:** Created _detect_row_identity_from_tr(tr_original) that directly scans td children of the passed <tr> node, without parent chain traversal.
- **Files modified:** backend/agent/dom_patch.py
- **Verification:** TestRowIdentityComment::test_tr_with_imei_gets_row_identity_comment passes with correct IMEI extraction; all 22 Phase 68 tests pass.
- **Committed in:** e16f18d (Task 1 GREEN commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Fix necessary for correctness. The original _detect_row_identity() works correctly for child nodes (input inside td inside tr); only the serialize_tree <tr> case needed the new direct-scanning variant.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All 6 DOM patches now applied in apply_dom_patch(): is_interactive, paint_order, should_exclude_child, assign_interactive_indices, serialize_tree_annotations
- Phase 68 complete: annotation sidecar + serialization layer both operational
- Ready for integration testing with live Agent execution

## Self-Check: PASSED
- All files exist: backend/agent/dom_patch.py, backend/tests/unit/test_dom_patch_phase68.py, 68-02-SUMMARY.md
- All commits found: 3ea31c7 (RED), e16f18d (GREEN)

---
*Phase: 68-dom-patch*
*Completed: 2026-04-07*
