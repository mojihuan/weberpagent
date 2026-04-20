---
phase: 86-登录机制研究
plan: 02
subsystem: auth
tags: [vue, spa-login, localstorage, mouseevent, browser-use, root-cause-analysis, research-report]

# Dependency graph
requires:
  - phase: 86-01
    provides: POC diagnostic results for 方案 C (localStorage injection) and 方案 A (form login)
provides:
  - Comprehensive research report covering all 4 success criteria (SC-1 through SC-4)
  - Root cause analysis: SPA Vuex/Pinia store reads localStorage on init, router guard checks store not localStorage
  - Confirmed Phase 87 fix: dispatchEvent(new MouseEvent) instead of btn.click() for Vue SPA login button
  - Actionable implementation plan with exact file paths, function signatures, and code patterns
affects: [87-代码登录修复与集成, 88-认证代码清理]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true, view:window})) for Vue SPA button clicks"
    - "JSON.stringify/json.loads pattern for browser-use page.evaluate complex objects"

key-files:
  created:
    - .planning/phases/86-登录机制研究/86-RESEARCH-REPORT.md
  modified:
    - .planning/ROADMAP.md
    - .planning/phases/86-登录机制研究/86-VALIDATION.md

key-decisions:
  - "方案 C (localStorage injection) confirmed NOT viable -- SPA store ignores direct localStorage writes"
  - "方案 A (programmatic form login) confirmed viable with dispatchEvent(MouseEvent) fix"
  - "Phase 87 needs only one code change: btn.click() -> dispatchEvent(new MouseEvent) in agent_service.py:244"

patterns-established:
  - "Research report as Phase 87 specification: evidence-backed root cause + exact implementation targets"

requirements-completed: [SC-1, SC-2, SC-4]

# Metrics
duration: 7min
completed: 2026-04-20
---

# Phase 86 Plan 02: Research Report Summary

**Comprehensive ERP login mechanism research report confirming 方案 A (programmatic form login with MouseEvent dispatch) as the viable path for Phase 87, with root cause analysis proving 方案 C (localStorage injection) fails due to Vuex/Pinia store initialization timing**

## Performance

- **Duration:** 7 min
- **Started:** 2026-04-20T06:57:55Z
- **Completed:** 2026-04-20T07:05:10Z
- **Tasks:** 2 of 2
- **Files modified:** 3

## Accomplishments
- Created comprehensive research report (86-RESEARCH-REPORT.md) covering all 4 success criteria with evidence-backed content
- Documented complete ERP login flow: HTTP API chain, JWT HS512 token format, localStorage keys, SPA Vuex/Pinia consumption pattern
- Identified root cause of injection failure: SPA store checks reactive state (not localStorage), store initializes before consuming localStorage
- Provided exact Phase 87 implementation plan: single-line fix in `_programmatic_login()` changing `btn.click()` to `dispatchEvent(new MouseEvent)`
- Updated ROADMAP.md to mark Phase 86 complete (2/2 plans) and VALIDATION.md with nyquist_compliant=true

## Task Commits

1. **Task 1: Write comprehensive research report** - `c3cd4aa` (docs)
2. **Task 2: Update ROADMAP.md and VALIDATION.md** - `0edfa1b` (docs)

## Files Created/Modified
- `.planning/phases/86-登录机制研究/86-RESEARCH-REPORT.md` - Comprehensive research report (SC-1 through SC-4)
- `.planning/ROADMAP.md` - Phase 86 marked complete, progress table updated
- `.planning/phases/86-登录机制研究/86-VALIDATION.md` - nyquist_compliant=true, all tasks marked green

## Decisions Made
- **Phase 87 follows 方案 A only** -- 方案 C (localStorage injection) confirmed not viable by POC evidence; no need to investigate further
- **Minimal change scope for Phase 87** -- Only `_programmatic_login()` button click logic needs modification; form filling and fallback logic are already correct
- **auth_session_factory.py cleanup deferred to Phase 88** -- storage_state injection is confirmed non-functional; Phase 88 should remove the temp file workaround and dead code path

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- **Phase 87 implementation path is fully specified:** Change `btn.click()` to `btn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}))` in `agent_service.py:244`
- Optional enhancement: Add composition events to form fill (compositionstart/compositionend before input/change)
- ROADMAP.md Phase 87 entry has requirements (AUTH-03, AUTH-04, AUTH-05) and success criteria ready
- Fallback logic in runs.py does not need modification

---
*Phase: 86-登录机制研究*
*Completed: 2026-04-20*

## Self-Check: PASSED

- FOUND: .planning/phases/86-登录机制研究/86-RESEARCH-REPORT.md
- FOUND: .planning/phases/86-登录机制研究/86-02-SUMMARY.md
- FOUND: .planning/ROADMAP.md
- FOUND: commit c3cd4aa (Task 1)
- FOUND: commit 0edfa1b (Task 2)
