---
phase: 99-核心键名修复
plan: 01
subsystem: code-generation
tags: [playwright, action-translator, locator-chain, browser-use, model-actions]

# Dependency graph
requires:
  - phase: 83-action-translator
    provides: ActionTranslator with multi-locator fallback
  - phase: 84-llm-fallback
    provides: translate_with_llm() LLM fourth layer
provides:
  - ActionTranslator._CORE_TYPES using "click"/"input" matching browser-use model_actions() output
  - Correct dispatch on action_type == "click" and action_type == "input"
  - LocatorChainBuilder using "input" for placeholder detection
  - All 48 tests passing with correct key names
affects: [99-02, code-generator, test-code-pipeline]

# Tech tracking
tech-stack:
  added: []
  patterns: [action-type-key-alignment, browser-use-model-actions-compat]

key-files:
  created: []
  modified:
    - backend/core/action_translator.py
    - backend/core/locator_chain_builder.py
    - backend/tests/unit/test_action_translator.py
    - backend/tests/unit/test_locator_chain_builder.py

key-decisions:
  - "Renamed action type strings from click_element/input_text to click/input to match browser-use model_actions() output"
  - "Kept private method names _translate_click/_translate_input unchanged (internal convention)"
  - "Updated all docstrings and test descriptions for consistency"

patterns-established:
  - "Action type key names: click, input, navigate, scroll, send_keys, go_back (matching browser-use output)"

requirements-completed: [KEY-01, KEY-03]

# Metrics
duration: 4min
completed: 2026-04-24
---

# Phase 99 Plan 01: Core Key Name Fix Summary

**Renamed action type keys from click_element/input_text to click/input in ActionTranslator and LocatorChainBuilder, matching browser-use model_actions() output so click/input actions are correctly translated to Playwright code**

## Performance

- **Duration:** 4 min
- **Started:** 2026-04-24T02:50:04Z
- **Completed:** 2026-04-24T02:54:40Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Fixed _CORE_TYPES set to use "click"/"input" matching browser-use model_actions() output
- Updated translate() and translate_with_llm() dispatch logic to route "click"/"input" correctly
- Updated _translate_click/_translate_input to pass correct key names to all downstream methods
- Updated LocatorChainBuilder placeholder detection to use action_type == "input"
- All 48 unit tests pass with updated key names (35 + 13)
- Zero occurrences of "click_element"/"input_text" string literals in modified files

## Task Commits

Each task was committed atomically:

1. **Task 1: Rename action type keys in action_translator.py and locator_chain_builder.py** - `20ad0c8` (fix)
2. **Task 2: Update test fixtures in test_action_translator.py and test_locator_chain_builder.py** - `179060b` (fix)

## Files Created/Modified
- `backend/core/action_translator.py` - Core action type strings renamed: _CORE_TYPES, dispatch, _translate_click, _translate_input, docstrings
- `backend/core/locator_chain_builder.py` - Placeholder check uses action_type == "input", docstring updated
- `backend/tests/unit/test_action_translator.py` - 28 action dict keys + 4 assertions + 4 docstrings updated
- `backend/tests/unit/test_locator_chain_builder.py` - 13 extract() calls + 3 method names/docstrings updated

## Decisions Made
- Kept private method names `_translate_click`/`_translate_input` unchanged -- they are internal naming convention and not part of the browser-use interface contract
- Updated docstrings and test descriptions alongside string literals for full consistency

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All core action type key names now match browser-use model_actions() output
- Ready for Plan 99-02 which will handle missing action type translations (wait, done, write_file, switch, extract, etc.)
- The code generator pipeline (action_translator -> code_generator) should now correctly process click/input actions instead of treating them as unknown

## Self-Check: PASSED

- backend/core/action_translator.py: FOUND
- backend/core/locator_chain_builder.py: FOUND
- backend/tests/unit/test_action_translator.py: FOUND
- backend/tests/unit/test_locator_chain_builder.py: FOUND
- .planning/phases/99-核心键名修复/99-01-SUMMARY.md: FOUND
- Commit 20ad0c8: FOUND
- Commit 179060b: FOUND

---
*Phase: 99-核心键名修复*
*Completed: 2026-04-24*
