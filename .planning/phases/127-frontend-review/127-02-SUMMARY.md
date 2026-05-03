---
phase: 127-frontend-review
plan: 02
subsystem: ui
tags: [react, typescript, sse, eventsource, hooks, forms, components]

# Dependency graph
requires:
  - phase: 127-01
    provides: breadth scan results, ESLint baseline, SSE cross-validation, risk priority matrix
provides:
  - P1 deep-dive findings for 5 frontend files (25 actionable findings)
  - useRunStream.ts SSE edge case analysis with backend cross-validation
  - client.ts retry/error handling analysis
  - DataMethodSelector/TaskForm/AssertionSelector state management assessment
affects: [127-03, frontend-refactoring]

# Tech tracking
tech-stack:
  added: []
  patterns: []

key-files:
  created:
    - .planning/phases/127-frontend-review/127-02-SUMMARY.md
  modified:
    - .planning/phases/127-frontend-review/127-FINDINGS.md

key-decisions:
  - "P1 deep-dive confirms JSON.parse without try/catch is the highest-risk frontend issue (DD-USE-01)"
  - "client.ts FormData Content-Type override is a real bug affecting Excel import (DD-CLI-01)"
  - "DataMethodSelector 829-line component is complex but functionally correct; state management is the main concern"
  - "Retry toast persistence bug in client.ts (DD-CLI-03) could confuse users during network errors"

patterns-established: []

requirements-completed: [CORR-03, PERF-02]

# Metrics
duration: 7min
completed: 2026-05-03
---

# Phase 127 Plan 02: P1 Deep-Dive Review Summary

**25 findings from line-by-line review of 5 highest-risk frontend files: useRunStream.ts (SSE edge cases), client.ts (HTTP retry), DataMethodSelector.tsx (829-line component), TaskForm.tsx (modal composition), AssertionSelector.tsx (external assertions)**

## Performance

- **Duration:** 7 min
- **Started:** 2026-05-03T12:17:04Z
- **Completed:** 2026-05-03T12:24:18Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Line-by-line review of useRunStream.ts covering all 8 D-02 areas: JSON.parse safety, event ordering, deduplication, reconnect state, timeline growth, useEffect cleanup, SSE cross-validation with backend, set-state-in-effect
- SSE cross-validation table confirming all 7 backend event types match frontend listeners with field-level comparison; identified external_assertions error-path format mismatch
- client.ts review identifying FormData Content-Type bug, retry toast persistence, and linear (not exponential) backoff
- DataMethodSelector.tsx state management assessment: 11 useState + 1 useMemo, int/float parse behavior, modal state reset issue, single preview state limitation
- TaskForm.tsx modal composition analysis: initialData reset gap, double-submit risk, shared operations state across rows
- AssertionSelector.tsx analysis: nested setState pattern, initialConfigs reference instability, redundant field_params state

## Task Commits

Each task was committed atomically:

1. **Task 1: Deep-dive review useRunStream.ts and client.ts** - `8d08145` (docs)
2. **Task 2: Deep-dive review DataMethodSelector.tsx, TaskForm.tsx, AssertionSelector.tsx** - `4698f9a` (docs)

## Files Created/Modified
- `.planning/phases/127-frontend-review/127-FINDINGS.md` - Appended 25 deep-dive findings (DD-USE-01 through DD-AS-06)

## Decisions Made
- useRunStream.ts JSON.parse without try/catch confirmed as the single highest-risk frontend issue -- malformed JSON silently kills event processing and corrupts run state
- client.ts FormData Content-Type override (DD-CLI-01) is a real correctness bug that affects Excel import; should be prioritized for fix
- DataMethodSelector.tsx at 829 lines is complex but the 4-step wizard structure is rational; main issues are state management patterns not architectural
- Retry toast persistence (DD-CLI-03) is a usability bug -- loading toast remains visible after successful retry due to recursive control flow

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Deep-Dive Findings Summary

### By File

| File | Findings | High | Medium | Low |
|------|----------|------|--------|-----|
| useRunStream.ts (215 lines) | 9 | 1 | 4 | 4 |
| client.ts (61 lines) | 5 | 1 | 2 | 2 |
| DataMethodSelector.tsx (829 lines) | 7 | 0 | 3 | 4 |
| TaskForm.tsx (560 lines) | 5 | 0 | 2 | 3 |
| AssertionSelector.tsx (546 lines) | 6 | 0 | 4 | 2 |
| **Total** | **32** | **2** | **15** | **15** |

Note: Total includes 7 findings from SSE cross-validation table (documented as structured data, not individual DD- entries). The 25 DD- findings are the actionable items.

### By Category

| Category | Count |
|----------|-------|
| Correctness | 14 |
| Architecture | 10 |
| Performance | 1 |

### Top Findings for Fix Priority

1. **DD-USE-01** [High] All 7 JSON.parse in useRunStream.ts lack try/catch -- malformed JSON silently corrupts run state
2. **DD-CLI-01** [High] client.ts sets Content-Type: application/json for FormData requests -- breaks Excel import
3. **DD-USE-03** [Medium] Step handler does not deduplicate by index -- duplicate steps from backend retries
4. **DD-USE-05** [Medium] onerror handler does not handle CONNECTING state -- UI shows "connected" during reconnection failures
5. **DD-CLI-03** [Medium] Retry loading toast persists after successful retry -- recursive control flow skips dismiss

## Next Phase Readiness
- 127-FINDINGS.md now contains both breadth scan results (Plan 01) and P1 deep-dive findings (Plan 02)
- Plan 03 will quick-scan P2/P3 files and produce the final consolidated summary with total statistics

---
*Phase: 127-frontend-review*
*Completed: 2026-05-03*

## Self-Check: PASSED

- [x] 127-02-SUMMARY.md exists
- [x] 127-FINDINGS.md exists with Deep-Dive Findings section
- [x] Commit 8d08145 (Task 1) found in git log
- [x] Commit 4698f9a (Task 2) found in git log
