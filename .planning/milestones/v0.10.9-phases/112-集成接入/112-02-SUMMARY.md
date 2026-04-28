---
phase: 112-集成接入
plan: 02
subsystem: testing
tags: [playwright, code-generator, step-code-buffer, integration-tests, tdd]

# Dependency graph
requires:
  - phase: 111-stepcodebuffer
    provides: "StepCodeBuffer with append_step_async and assemble methods"
  - phase: 112-01
    provides: "runs.py integration with buffer.append_step_async"

provides:
  - "Slimmed code_generator.py with generate() only (no generate_and_save/_heal_weak_steps)"
  - "TestIntegration class with 7 VAL-02 integration tests"
  - "Updated test_assertion_translation and test_precondition_injection to use buffer pattern"

affects: [113-codegen-e2e]

# Tech tracking
tech-stack:
  added: []
  patterns: [closure-captured-buffer, step-callback-context-testing]

key-files:
  created: []
  modified:
    - backend/core/code_generator.py
    - backend/tests/unit/test_code_generator.py
    - backend/tests/unit/test_step_code_buffer.py
    - backend/tests/unit/test_assertion_translation.py
    - backend/tests/unit/test_precondition_injection.py

key-decisions:
  - "Removed generate_and_save and _heal_weak_steps from code_generator.py since logic moved to StepCodeBuffer.append_step_async"
  - "Updated 2 downstream tests to use StepCodeBuffer.assemble() pattern instead of removed generate_and_save"

patterns-established:
  - "TestIntegration class pattern: simulate step_callback context with buffer creation, multi-step accumulation, and assembly verification"
  - "Closure-captured buffer test: inner async function captures outer buffer, validates indirection works"

requirements-completed: [INTEG-03, VAL-02]

# Metrics
duration: 6min
completed: 2026-04-28
---

# Phase 112 Plan 02: Integration Cleanup Summary

**Removed deprecated generate_and_save/_heal_weak_steps from code_generator.py, added 7 VAL-02 integration tests simulating step_callback context with closure-captured buffer pattern**

## Performance

- **Duration:** 6 min
- **Started:** 2026-04-28T05:28:40Z
- **Completed:** 2026-04-28T05:34:49Z
- **Tasks:** 2 (+ 1 auto-fix)
- **Files modified:** 5

## Accomplishments
- Removed generate_and_save and _heal_weak_steps from code_generator.py (229 lines deleted)
- Cleaned up unused imports (LLMHealer, Path, Any, os, tempfile, AsyncMock)
- Added TestIntegration class with 7 tests covering VAL-02: accumulation, assembly, weak-step healing, graceful failure, precondition config, assertions config, closure-captured buffer
- Updated 2 downstream tests (test_assertion_translation, test_precondition_injection) that referenced removed generate_and_save

## Task Commits

Each task was committed atomically:

1. **Task 1: Delete generate_and_save and _heal_weak_steps** - `1a18e84` (refactor)
2. **Task 2: Add TestIntegration class** - `ef9b465` (test)
3. **Auto-fix: Update 2 broken downstream tests** - `2c4b9dd` (fix)

## Files Created/Modified
- `backend/core/code_generator.py` - Removed generate_and_save, _heal_weak_steps, LLMHealer import, Path import, Any import; generate() preserved
- `backend/tests/unit/test_code_generator.py` - Removed 2 deprecated tests, 4 unused imports; 8 remaining tests pass
- `backend/tests/unit/test_step_code_buffer.py` - Added TestIntegration class with 7 new tests; 30 total tests pass
- `backend/tests/unit/test_assertion_translation.py` - Rewrote test_generate_and_save_passes_assertions_config as test_buffer_assemble_passes_assertions_config
- `backend/tests/unit/test_precondition_injection.py` - Rewrote test_generate_and_save_passes_config as test_buffer_assemble_passes_config

## Decisions Made
- Removed generate_and_save and _heal_weak_steps since their logic is fully replicated in StepCodeBuffer.append_step_async
- Downstream tests for config passthrough (assertions_config, precondition_config) updated to use StepCodeBuffer.assemble() pattern instead of the removed generate_and_save method
- All 7 integration tests use append_step_async (async pattern) to match the real step_callback context

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Updated 2 downstream tests referencing removed generate_and_save**
- **Found during:** Post-task full unit test suite run (244 passed, 2 failed)
- **Issue:** test_assertion_translation and test_precondition_injection called generator.generate_and_save() which was removed in Task 1
- **Fix:** Rewrote both tests to use StepCodeBuffer().append_step() + .assemble() pattern, validating same config passthrough behavior
- **Files modified:** backend/tests/unit/test_assertion_translation.py, backend/tests/unit/test_precondition_injection.py
- **Verification:** uv run pytest backend/tests/unit/ --timeout=30 exits 0 with 246 passed
- **Committed in:** 2c4b9dd

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Auto-fix necessary for correctness. Downstream tests needed updating to match the removal of generate_and_save. No scope creep.

## Issues Encountered
None beyond the auto-fixed downstream test references.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- code_generator.py is slimmed to generate() only, ready for Phase 113 E2E validation
- TestIntegration class validates buffer accumulation and closure-captured pattern for VAL-02
- All 246 unit tests pass with zero regressions

---
*Phase: 112-集成接入*
*Completed: 2026-04-28*
