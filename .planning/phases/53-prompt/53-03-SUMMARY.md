---
phase: 53-prompt
plan: 03
subsystem: agent
tags: [browser-use, monkey-patch, dom-serializer, erp-table]

# Dependency graph
requires:
  - phase: 53-prompt-01
    provides: ENHANCED_SYSTEM_MESSAGE Section 7 initial table interaction prompt
  - phase: 53-prompt-02
    provides: ERP table interaction test results identifying root cause
provides:
  - dom_patch.py monkey-patch for browser-use DOM serializer
  - Unit tests for dom_patch (18 tests)
  - Agent creation integration with apply_dom_patch()
  - Updated prompt Section 7 with click(index) priority + evaluate JS fallback
affects: [phase-54, phase-56]

# Tech tracking
tech-stack:
  added: []
  patterns: [monkey-patching third-party library methods, idempotent patch guard]

key-files:
  created:
    - backend/agent/dom_patch.py
    - backend/tests/unit/test_dom_patch.py
  modified:
    - backend/agent/browser_agent.py
    - backend/agent/proxy_agent.py
    - backend/agent/prompts.py
    - backend/tests/unit/test_enhanced_prompt.py

key-decisions:
  - "Patching PaintOrderRemover post-execution + _should_exclude_child pre-check covers both DOM filtering mechanisms"
  - "Prompt Section 7 updated to prioritize click(index) since patch gives elements independent indices"
  - "evaluate JS retained as fallback in prompt for robustness"

patterns-established:
  - "Monkey-patch pattern: _PATCHED flag for idempotency, wrap original methods, restore ERP nodes post-filtering"
  - "ERP class detection via _has_erp_clickable_class with substring matching on split class list"

requirements-completed: [TBL-01, TBL-02, TBL-03, TBL-04]

# Metrics
duration: 8min + 15min gap closure
completed: 2026-03-31
---

# Phase 53 Plan 03: DOM Serializer Patch Summary

**Monkey-patch browser-use DOM serializer to give span.hand and .el-checkbox independent clickable indices, integrated into Agent creation with updated prompt**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-31T00:57:32Z
- **Completed:** 2026-03-31T01:05:55Z
- **Tasks:** 3 of 4 (Task 4 is checkpoint:human-verify, pending)
- **Files modified:** 6

## Accomplishments
- Created dom_patch.py patching PaintOrderRemover and DOMTreeSerializer to preserve ERP clickable sub-elements
- 18 unit tests covering class detection, idempotency, paint order reset, and exclusion logic
- Integrated apply_dom_patch() into both browser_agent.py and proxy_agent.py before Agent creation
- Updated prompt Section 7: click(index) primary, evaluate JS as fallback strategy

## Task Commits

Each task was committed atomically:

1. **Task 1: Create dom_patch.py** - `ce593e7` (feat)
2. **Task 2: Write dom_patch unit tests** - `d5020e0` (test)
3. **Task 3: Integrate dom_patch + update prompt** - `af07192` (feat)

## Files Created/Modified
- `backend/agent/dom_patch.py` - Monkey-patches PaintOrderRemover and DOMTreeSerializer for ERP elements
- `backend/tests/unit/test_dom_patch.py` - 18 unit tests for dom_patch
- `backend/agent/browser_agent.py` - Added apply_dom_patch() call before Agent creation
- `backend/agent/proxy_agent.py` - Added apply_dom_patch() call before Agent creation
- `backend/agent/prompts.py` - Section 7 updated: click(index) primary, evaluate JS fallback
- `backend/tests/unit/test_enhanced_prompt.py` - Updated keyword assertions for new prompt

## Decisions Made
- Patching both PaintOrderRemover (post-execution reset) and _should_exclude_child (pre-check bypass) to cover both DOM filtering mechanisms that absorb sub-elements
- Prompt Section 7 now prioritizes click(index=N) since the patch gives elements their own indices; evaluate JS retained as fallback
- _has_erp_clickable_class uses substring matching on class tokens to catch compound class names like "el-checkbox__inner"

## Deviations from Plan

None - plan executed exactly as written for Tasks 1-3.

## Issues Encountered

### Gap 1: Missing third patch for ClickableElementDetector.is_interactive
- **Problem:** Original patch only covered paint order removal and bounding box exclusion (pipeline stages 2-3), but interactive element detection (stage 4) still skipped `<span class="hand">` and `<span class="el-checkbox__inner">` because they lack form controls, event handlers, ARIA roles, or interactive tag names.
- **Fix:** Added `_patch_is_interactive()` that patches `ClickableElementDetector.is_interactive()` to return True for ERP-classed nodes.
- **Commit:** `501a5f1`

### Gap 2: apply_dom_patch() not called in actual execution path
- **Problem:** `apply_dom_patch()` was only called in `browser_agent.py` and `proxy_agent.py`, but the actual execution path uses `MonitoredAgent` via `agent_service.py` which never called the patch. All three DOM serializer patches were never applied during real task execution.
- **Fix:** Added `apply_dom_patch()` call in `agent_service.py` before `MonitoredAgent` creation.
- **Commit:** `b586b54`

### Human Verification Result
- All four scenarios (TBL-01 checkbox single select, TBL-02 checkbox select-all, TBL-03 hyperlink click, TBL-04 icon button) **PASSED** after gap closure fixes.

## Next Phase Readiness
- dom_patch module fully integrated and human-verified in ERP
- All TBL requirements (TBL-01 through TBL-04) verified passing

## Self-Check: PASSED
- All 6 files verified as existing
- All 3 task commits verified in git log (ce593e7, d501e0, af07192)
- Docs commit verified (9b2f927)

---
*Phase: 53-prompt*
*Completed: 2026-03-31*
