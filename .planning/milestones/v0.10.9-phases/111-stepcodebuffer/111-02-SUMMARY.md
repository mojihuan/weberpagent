---
phase: 111-stepcodebuffer
plan: 02
subsystem: codegen
tags: [playwright, code-generation, step-buffer, llm-healing, weak-step, async, tdd]

# Dependency graph
requires:
  - phase: 111-stepcodebuffer
    provides: StepCodeBuffer core (append_step, _derive_wait, assemble) from Plan 01
  - phase: 83-action-translator
    provides: ActionTranslator.translate() + translate_with_llm() + TranslatedAction
  - phase: 84-code-generator
    provides: PlaywrightCodeGenerator.generate() + _heal_weak_steps pattern
provides:
  - append_step_async() with weak-step LLM healing via LLMHealer.heal()
  - _is_weak_step() detecting elem=None or <=1 locator
  - DOM snapshot reading from {base_dir}/{run_id}/dom/step_{n}.txt
  - 9 async unit tests covering CODEGEN-02 and VAL-01
affects: [112-stepcodeasync, 113-integration]

# Tech tracking
tech-stack:
  added: []
  patterns: [weak-step-detection, incremental-llm-healing, dom-snapshot-read, async-fallback]

key-files:
  created: []
  modified:
    - backend/core/step_code_buffer.py
    - backend/tests/unit/test_step_code_buffer.py

key-decisions:
  - "__init__ uses keyword-only args (*, base_dir, run_id, llm_config) for backward compatibility (per D-02)"
  - "_is_weak_step() reuses LocatorChainBuilder.extract() for locator counting, matching code_generator pattern"
  - "append_step_async falls back silently on heal failure/exception/missing DOM -- no crashes (per D-03)"
  - "Only click/input actions undergo weak-step detection (per D-07)"

patterns-established:
  - "Weak-step detection: elem=None or LocatorChainBuilder.extract() returns <=1 locator"
  - "Async healing with graceful fallback: DOM read -> heal() -> translate_with_llm(), catch Exception"
  - "DOM snapshot path convention: {base_dir}/{run_id}/dom/step_{n}.txt (1-indexed)"

requirements-completed: [CODEGEN-02, VAL-01]

# Metrics
duration: 4min
completed: 2026-04-28
---

# Phase 111 Plan 02: append_step_async Weak-Step Healing Summary

**append_step_async() detects weak steps (elem=None or <=1 locator), reads DOM snapshots, calls LLMHealer.heal() for click/input, falls back gracefully on failure**

## Performance

- **Duration:** 4 min
- **Started:** 2026-04-28T02:46:13Z
- **Completed:** 2026-04-28T02:50:22Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- append_step_async() implements incremental LLM healing per step (replaces batch _heal_weak_steps pattern)
- _is_weak_step() uses LocatorChainBuilder.extract() to count locators, matching code_generator.py detection logic
- DOM snapshot reading from {base_dir}/{run_id}/dom/step_{n}.txt (1-indexed) with missing file fallback
- 9 new async tests covering weak detection, DOM read, heal success/failure/exception, non-click/input skip
- All 23 tests passing (14 Plan 01 + 9 Plan 02), zero regressions

## Task Commits

Each task was committed atomically:

1. **Task 1+2: append_step_async + async tests** - `9f100f0` (feat)

_Note: TDD flow -- RED (9 test errors, __init__ missing keyword args) -> GREEN (implementation + tests pass 23/23)_

## Files Created/Modified
- `backend/core/step_code_buffer.py` - Added append_step_async(), _is_weak_step(), updated __init__ with base_dir/run_id/llm_config keyword-only args, added LLMHealer/LocatorChainBuilder/Path imports
- `backend/tests/unit/test_step_code_buffer.py` - Added 9 async tests in TestAppendStepAsyncWeakHealing class plus async_buffer/mock_elem_weak/mock_elem_strong fixtures

## Decisions Made
- Keyword-only __init__ args ensure Plan 01's StepCodeBuffer() call still works without changes (backward compatible)
- _is_weak_step() extracted as private method for testability and reuse
- LLMHealer created per-heal call (not cached) to avoid stale LLM state across steps
- Exception catch is broad (Exception) because any LLM error should silently fallback, not crash the buffer

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None - implementation followed code_generator.py _heal_weak_steps pattern closely.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- StepCodeBuffer complete with sync (Plan 01) and async (Plan 02) translation + healing
- Ready for Phase 112 (stepcodeasync) integration into runs.py step_callback
- Ready for Phase 113 (integration) replacing generate_and_save batch translation

## Self-Check: PASSED

- FOUND: backend/core/step_code_buffer.py
- FOUND: backend/tests/unit/test_step_code_buffer.py
- FOUND: 111-02-SUMMARY.md
- FOUND: commit 9f100f0

---
*Phase: 111-stepcodebuffer*
*Completed: 2026-04-28*
