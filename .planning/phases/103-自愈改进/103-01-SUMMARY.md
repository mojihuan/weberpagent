---
phase: 103-自愈改进
plan: 01
subsystem: testing
tags: [pytest, error-classification, self-healing, llm-optimization]

# Dependency graph
requires:
  - phase: 102-执行修复
    provides: SelfHealingRunner with fixed pytest args and newline handling
provides:
  - Error classifier pure function (classify_pytest_error) with 6 categories
  - HealingResult.error_category field for error type tracking
  - Env error fast-fail in SelfHealingRunner retry loop (skip LLM calls)
affects: [self-healing, code-execution, llm-cost]

# Tech tracking
tech-stack:
  added: []
  patterns: [pure-function-classifier, frozen-dataclass-result, enum-based-categorization]

key-files:
  created:
    - backend/core/error_classifier.py
    - backend/tests/unit/test_error_classifier.py
  modified:
    - backend/core/self_healing_runner.py
    - backend/tests/unit/test_self_healing_runner.py

key-decisions:
  - "ErrorCategoryResult uses frozen dataclass per project convention"
  - "error_category default empty string on HealingResult for backward compatibility"
  - "Unknown exit codes default to CODE_RUNTIME to avoid missing LLM repair opportunities"
  - "Exit code 3 classified as ENV_PYTEST_ERROR (pytest INTERNALERROR, LLM cannot fix)"

patterns-established:
  - "Pure function error classification: classify_pytest_error(exit_code, error_output) -> ErrorCategoryResult"
  - "Classifier inserted before LLM repair in retry loop for early termination"

requirements-completed: [HEAL-01]

# Metrics
duration: 12min
completed: 2026-04-24
---

# Phase 103 Plan 01: Error Classifier Summary

**Pure function error classifier that distinguishes pytest environment errors (exit 2/3/4/5) from code errors (exit 1), saving LLM calls on unfixable failures**

## Performance

- **Duration:** 12 min
- **Started:** 2026-04-24T12:26:59Z
- **Completed:** 2026-04-24T12:39:01Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Error classifier module with 6 categories and pure function classify_pytest_error()
- SelfHealingRunner skips LLM repair on env errors (exit 2/3/4/5), attempts LLM on code errors (exit 1)
- 13 new tests (10 classifier + 3 integration), all 801 unit tests pass with 0 regressions

## Task Commits

Each task was committed atomically:

1. **Task 1: Create error classifier module + unit tests** - `fde07e6` (feat)
2. **Task 2: Integrate classifier into SelfHealingRunner + update tests** - `22fb3ee` (feat)

## Files Created/Modified
- `backend/core/error_classifier.py` - ErrorCategory enum, ErrorCategoryResult frozen dataclass, classify_pytest_error() pure function
- `backend/tests/unit/test_error_classifier.py` - 10 tests covering all 9 classification paths + frozen verification
- `backend/core/self_healing_runner.py` - Added import, HealingResult.error_category field, classifier call in retry loop
- `backend/tests/unit/test_self_healing_runner.py` - Updated frozen test, added 3 integration tests for env/code error handling

## Decisions Made
- Used frozen dataclass for ErrorCategoryResult per project-wide immutability convention
- error_category field defaults to empty string on HealingResult for backward compatibility with existing callers
- Unknown exit codes default to CODE_RUNTIME (skip_llm_healing=False) to avoid missing LLM repair opportunities
- Exit code 3 (pytest INTERNALERROR) classified as environment error per research finding that LLM cannot fix pytest internals

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

Pre-existing E2E test failure (test_e2e_code_generation_login) unrelated to this plan -- caused by --timeout=60 being an invalid pytest argument in that test environment. The error classifier correctly identifies this as ENV_PYTEST_ERROR, which is the expected behavior.

## Next Phase Readiness
- Error classifier is fully integrated and tested
- SelfHealingRunner now efficiently skips LLM calls on environment errors
- Ready for E2E verification or subsequent self-healing improvements

## Self-Check: PASSED

- [x] backend/core/error_classifier.py exists
- [x] backend/tests/unit/test_error_classifier.py exists
- [x] backend/core/self_healing_runner.py exists
- [x] backend/tests/unit/test_self_healing_runner.py exists
- [x] Commit fde07e6 exists (Task 1)
- [x] Commit 22fb3ee exists (Task 2)

---
*Phase: 103-自愈改进*
*Completed: 2026-04-24*
