---
phase: 49-prompt-optimization
plan: 01
subsystem: agent
tags: [prompt-engineering, browser-use, erp, chinese, qwen]

# Dependency graph
requires:
  - phase: 48-agent
    provides: MonitoredAgent, StallDetector, PreSubmitGuard intervention message format
provides:
  - ENHANCED_SYSTEM_MESSAGE constant for extend_system_message injection
  - Unit tests verifying prompt structure and content
  - CHINESE_ENHANCEMENT backward compat alias
affects: [49-02, 50-agent-integration]

# Tech tracking
tech-stack:
  added: []
  patterns: [keyword-based prompt testing, bilingual test assertions]

key-files:
  created:
    - backend/tests/unit/test_enhanced_prompt.py
  modified:
    - backend/agent/prompts.py

key-decisions:
  - "Chinese-first prompt content per D-03, with English technical terms (evaluate, find_elements) preserved"
  - "Test assertions check bilingual keywords (Chinese OR English) since prompt is Chinese but tests use .lower()"
  - "CHINESE_ENHANCEMENT kept as alias to ENHANCED_SYSTEM_MESSAGE for backward compatibility"

patterns-established:
  - "Keyword-based prompt testing: assert keyword presence rather than exact string matching"
  - "Bilingual test assertions: check both English .lower() and Chinese Unicode characters"

requirements-completed: [PRM-01, PRM-02, PRM-03, PRM-04, PRM-05]

# Metrics
duration: 3min
completed: 2026-03-28
---

# Phase 49 Plan 01: ENHANCED_SYSTEM_MESSAGE Summary

**ENHANCED_SYSTEM_MESSAGE replacing CHINESE_ENHANCEMENT with 5-section ERP-specific guidance: click-to-edit tables, failure recovery, field verification, pre-submit validation, and merged selector strategy**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-28T07:24:05Z
- **Completed:** 2026-03-28T07:27:05Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Created ENHANCED_SYSTEM_MESSAGE with 5 concise Chinese-language sections addressing 5 core ERP reliability problems
- Merged valuable CHINESE_ENHANCEMENT content (form field mapping, selector strategy) into new prompt
- Removed redundant JSON output format template (browser-use has built-in format)
- All 8 keyword-based structural tests pass

## Task Commits

Each task was committed atomically:

1. **Task 1: Write ENHANCED_SYSTEM_MESSAGE structure tests** - `f1ae484` (test)
2. **Task 2: Create ENHANCED_SYSTEM_MESSAGE in prompts.py** - `99bb948` (feat)

## Files Created/Modified
- `backend/agent/prompts.py` - Replaced CHINESE_ENHANCEMENT with ENHANCED_SYSTEM_MESSAGE (5 sections, under 60 lines), added backward compat alias
- `backend/tests/unit/test_enhanced_prompt.py` - 8 test methods verifying prompt structure and keyword content

## Decisions Made
- Chinese-first prompt content with English technical terms (evaluate, find_elements) preserved for accuracy
- Test assertions check bilingual keywords (Chinese OR English) since prompt is Chinese but tests use .lower()
- Kept CHINESE_ENHANCEMENT as alias to ENHANCED_SYSTEM_MESSAGE for backward compatibility with browser_agent.py and proxy_agent.py

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed bilingual keyword assertions in failure recovery test**
- **Found during:** Task 2 (GREEN phase)
- **Issue:** Test checked for English "fail" and "skip" but prompt uses Chinese "失败" and "跳过" per D-03
- **Fix:** Updated assertions to check both English .lower() and Chinese Unicode characters
- **Files modified:** backend/tests/unit/test_enhanced_prompt.py
- **Verification:** All 8 tests pass

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Minimal - test keyword assertions needed bilingual support for Chinese prompt content

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- ENHANCED_SYSTEM_MESSAGE ready for injection via extend_system_message in agent_service.py (Plan 49-02)
- CHINESE_ENHANCEMENT backward compat alias ensures no import breakage
- Phase 50 will integrate ENHANCED_SYSTEM_MESSAGE with MonitoredAgent

## Self-Check: PASSED

- FOUND: backend/agent/prompts.py
- FOUND: backend/tests/unit/test_enhanced_prompt.py
- FOUND: f1ae484 (Task 1 commit)
- FOUND: 99bb948 (Task 2 commit)

---
*Phase: 49-prompt-optimization*
*Completed: 2026-03-28*
