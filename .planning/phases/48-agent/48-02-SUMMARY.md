---
phase: 48-agent
plan: 02
subsystem: agent
tags: [regex, form-validation, tdd, frozen-dataclass, submit-guard]

# Dependency graph
requires:
  - phase: 48-agent
    provides: "plan 01 StallDetector pattern (frozen result dataclass, separate file per detector)"
provides:
  - "PreSubmitGuard with check() method and regex-based expectation extraction"
  - "GuardResult frozen dataclass (immutable)"
  - "EXPECTATION_PATTERNS and SUBMIT_KEYWORDS constants"
  - "12 unit tests covering MON-04, MON-05, MON-06"
affects: [48-agent-plan-03, 48-agent-plan-04, "MonitoredAgent integration"]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Frozen dataclass for immutable results", "Span-tracked regex extraction to prevent overlapping matches"]

key-files:
  created:
    - "backend/agent/pre_submit_guard.py"
    - "backend/tests/unit/test_pre_submit_guard.py"
  modified: []

key-decisions:
  - "Overlap-tracked regex extraction prevents '金额' matching inside '销售金额'"
  - "PreSubmitGuard.check() accepts actual_values as parameter, enabling pure unit testing without browser"

patterns-established:
  - "Detector pattern: frozen result dataclass + mutable state dataclass (consistent with StallDetector)"
  - "Span-tracked extraction: iterate specific-to-generic patterns, skip overlapping matches"

requirements-completed: [MON-04, MON-05, MON-06]

# Metrics
duration: 6min
completed: 2026-03-28
---

# Phase 48 Plan 02: PreSubmitGuard Summary

**Regex-based form field validation guard with frozen GuardResult, blocking submit clicks on value mismatch**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-28T05:35:05Z
- **Completed:** 2026-03-28T05:41:14Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- PreSubmitGuard extracts 4 field types from task descriptions (sales amount, logistics fee, amount, payment status)
- Blocks submit clicks when extracted expectations mismatch actual page values
- Skips validation when no expectations found (MON-06) or actual_values unavailable
- 98% test coverage, 12/12 tests passing

## Task Commits

Each task was committed atomically:

1. **Task 1: RED -- Write failing PreSubmitGuard tests** - `909569a` (test)
2. **Task 2: GREEN -- Implement PreSubmitGuard to pass all tests** - `371e28c` (feat)

_Note: TDD flow -- RED (tests fail with ModuleNotFoundError) then GREEN (all 12 tests pass)_

## Files Created/Modified
- `backend/agent/pre_submit_guard.py` - PreSubmitGuard dataclass with check() and _extract_expectations(), GuardResult frozen dataclass, EXPECTATION_PATTERNS, SUBMIT_KEYWORDS
- `backend/tests/unit/test_pre_submit_guard.py` - 12 tests in 3 classes: extraction (4), check behavior (6), immutability (2)

## Decisions Made
- **Span-tracked regex extraction:** The generic "金额" pattern also matches inside "销售金额", causing false extraction overlap. Implemented span tracking so once a more specific pattern consumes a text region, less specific patterns skip overlapping matches. This was discovered during GREEN phase when `test_allows_submit_on_match` failed because both "销售金额" and "金额" matched the same text.
- **actual_values as parameter:** PreSubmitGuard.check() receives actual_values as a parameter rather than fetching them internally, enabling pure unit testing without a browser. Phase 50 integration will provide real values via `page.evaluate()`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed overlapping regex extraction for '金额' inside '销售金额'**
- **Found during:** Task 2 (GREEN phase)
- **Issue:** The generic "金额" pattern matched "销售金额150元" alongside the specific "销售金额" pattern, extracting both fields from the same text region. This caused `test_allows_submit_on_match` to fail because actual_values only had "销售金额" but expectations had both "销售金额" and "金额".
- **Fix:** Added span tracking to `_extract_expectations()` -- iterate patterns specific-to-generic, track consumed text spans, skip any match that overlaps with an already-consumed span.
- **Files modified:** backend/agent/pre_submit_guard.py
- **Verification:** All 12 tests pass, 98% coverage
- **Committed in:** 371e28c (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Bug fix essential for correctness. No scope creep.

## Issues Encountered
None beyond the overlapping regex issue documented above.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- PreSubmitGuard ready for MonitoredAgent._execute_actions() integration (Phase 48 plan 04)
- GuardResult follows same frozen dataclass pattern as StallResult, consistent API
- check() method signature designed for easy integration: action_name, target_index, task, actual_values, submit_button_text

## Self-Check: PASSED

All created files verified present. Both task commits verified in git log.

---
*Phase: 48-agent*
*Completed: 2026-03-28*
