---
phase: 107-自愈修复增强E2E
plan: 01
subsystem: testing
tags: [playwright, self-healing, llm-repair, ast-parse, dom-snapshot, json-response]

# Dependency graph
requires:
  - phase: 103-自愈改进
    provides: ErrorClassifier + HealingResult error_category
  - phase: 106-定位器质量优化
    provides: LocatorChainBuilder improved locators in generated code
provides:
  - Content-matching multi-line _apply_fix replacing line-number based single-line fix
  - Code locator to DOM mapping via _extract_locator_from_code + _search_dom_for_text
  - Structured LLM repair prompt (REPAIR_SYSTEM_PROMPT_V2) requesting JSON target_snippet/replacement
  - 20-line context window for LLM repair (up from 10)
  - _parse_repair_response with robust JSON extraction from LLM output
affects: [107-02 E2E test, future self-healing improvements]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Content-matching code replacement: str.find() target_snippet + ast.parse validation"
    - "Code locator extraction: regex patterns for get_by_text/get_by_role/locator"
    - "Structured LLM response: JSON {target_snippet, replacement} with fallback extraction"

key-files:
  created: []
  modified:
    - backend/core/llm_healer.py
    - backend/core/self_healing_runner.py
    - backend/tests/unit/test_llm_healer.py
    - backend/tests/unit/test_self_healing_runner.py

key-decisions:
  - "Content matching via str.find() for target_snippet -- simplest, most predictable"
  - "Minimum target_snippet length 20 chars to avoid ambiguous matches"
  - "ast.parse validation inside _apply_fix with None return on failure (rollback)"
  - "Keep old REPAIR_SYSTEM_PROMPT as reference, add REPAIR_SYSTEM_PROMPT_V2"
  - "LLMHealResult new fields with defaults for backward compatibility"

patterns-established:
  - "Content-matching _apply_fix: target_snippet + replacement replaces line-number fix"
  - "Locator text extraction from failing code line for DOM search"
  - "Structured JSON repair response with fallback extraction chain"

requirements-completed: [HEAL-01, HEAL-02, HEAL-03, HEAL-04]

# Metrics
duration: 11min
completed: 2026-04-27
---

# Phase 107 Plan 01: SelfHealingRunner Repair Pipeline Rewrite Summary

**Content-matching multi-line _apply_fix, code locator to DOM mapping, structured JSON LLM repair prompt with 20-line context window**

## Performance

- **Duration:** 11 min
- **Started:** 2026-04-27T01:24:59Z
- **Completed:** 2026-04-27T01:36:30Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Rewrote _apply_fix from line-number single-line to content-matching multi-line replacement with ast.parse rollback
- Implemented code locator extraction (_extract_locator_from_code) and DOM search (_search_dom_for_text) for precise DOM snapshot matching
- Redesigned LLM repair prompt (REPAIR_SYSTEM_PROMPT_V2) requesting structured JSON {target_snippet, replacement}
- Extended LLMHealResult with target_snippet and replacement fields (backward compatible defaults)
- Expanded context window from 10 to 20 lines for better LLM repair quality
- Added robust _parse_repair_response with JSON extraction from markdown fences and embedded text

## Task Commits

Each task was committed atomically (TDD: RED then GREEN):

1. **Task 1 RED: test structured repair prompt + LLMHealResult extension** - `6ef5563` (test)
2. **Task 1 GREEN: implement structured repair prompt V2** - `b60437f` (feat)
3. **Task 2 RED: test _apply_fix content match + locator extraction** - `0ec9ca1` (test)
4. **Task 2 GREEN: rewrite _apply_fix + DOM locator extraction** - `4abf79d` (feat)

## Files Created/Modified
- `backend/core/llm_healer.py` - REPAIR_SYSTEM_PROMPT_V2, _parse_repair_response, LLMHealResult extension, repair_code V2 integration
- `backend/core/self_healing_runner.py` - _apply_fix rewrite, _extract_locator_from_code, _search_dom_for_text, _read_dom_snapshot enhancement, _llm_repair update
- `backend/tests/unit/test_llm_healer.py` - 13 new tests for parse, structured response, context window, frozen dataclass
- `backend/tests/unit/test_self_healing_runner.py` - 15 new tests for apply_fix, locator extraction, DOM search, snapshot reading

## Decisions Made
- Used str.find() for exact substring matching in _apply_fix (simplest, most predictable)
- Set minimum target_snippet length to 20 chars to avoid ambiguous multi-matches
- ast.parse validation inside _apply_fix returns None on SyntaxError (rollback pattern)
- Kept old REPAIR_SYSTEM_PROMPT as reference constant, added V2 alongside
- LLMHealResult new fields (target_snippet, replacement) have default empty strings for backward compatibility
- _parse_repair_response tries direct JSON parse then regex extraction from surrounding text

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- All 4 HEAL requirements (HEAL-01 through HEAL-04) implemented and tested
- 256 tests pass in full suite (0 regressions)
- 34 focused unit tests (15 test_llm_healer + 19 test_self_healing_runner)
- Ready for Plan 02: E2E verification

---
*Phase: 107-自愈修复增强E2E*
*Completed: 2026-04-27*

## Self-Check: PASSED

All 4 implementation files verified on disk. All 4 task commits verified in git log.
