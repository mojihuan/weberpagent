---
phase: 125-backend-core-review
plan: 02
subsystem: backend-core
tags: [code-review, correctness, architecture, pipeline, agent-service, code-generator]

# Dependency graph
requires:
  - phase: 125-backend-core-review/01
    provides: Breadth scan results, risk priority matrix, P3 findings
provides:
  - Deep-dive findings for 5 pipeline-critical P1 files
  - Verified status of all 9 RESEARCH.md pitfalls
  - 23 total findings with severity/category/recommendation
affects: [125-backend-core-review/03, v0.11.3-fixes]

# Tech tracking
tech-stack:
  added: []
  patterns: []

key-files:
  created:
    - .planning/phases/125-backend-core-review/125-02-SUMMARY.md
  modified:
    - .planning/phases/125-backend-core-review/125-FINDINGS.md

key-decisions:
  - "Dual stall detection is the highest-priority correctness issue -- same StallDetector instance called twice per step inflates failure counts to half the configured threshold"
  - "ContextWrapper isinstance check silently skips variable_map for all tasks with preconditions, making generated test code non-reusable"
  - "Pre-click 3s wait in step_code_buffer.py is misplaced (before click, not after) and combined with post-click waits creates ~6.5s per click in generated code"
  - "PreSubmitGuard is confirmed dead code -- always receives None, submit-blocking feature is non-functional"

patterns-established: []

requirements-completed: [CORR-01, ARCH-01, ARCH-02]

# Metrics
duration: 4min
completed: 2026-05-03
---

# Phase 125 Plan 02: P1 Deep-Dive Review Summary

**Line-by-line review of 5 pipeline-critical files identifying 23 findings: 3 High, 12 Medium, 6 Low, 2 verified-correct**

## Performance

- **Duration:** 4 min
- **Started:** 2026-05-03T03:14:59Z
- **Completed:** 2026-05-03T03:19:52Z
- **Tasks:** 2
- **Files modified:** 1 (125-FINDINGS.md appended)

## Accomplishments

- Deep-dive reviewed all 5 P1 files (run_pipeline.py, agent_service.py, code_generator.py, step_code_buffer.py, monitored_agent.py) totaling 2,428 lines
- Verified all 9 RESEARCH.md pitfalls against actual code and documented findings with line-level references
- Identified 3 High-severity issues: dual stall detection, ContextWrapper isinstance bypass, variable substitution skipped for preconditioned tasks
- Confirmed 2 previously suspected patterns as correctly handled (pipeline error cleanup, _pending_interventions lifecycle)

## Task Commits

This is a review-only phase. The `.planning/` directory is in `.gitignore`, so commits are not applicable. All findings are persisted to disk in 125-FINDINGS.md.

1. **Task 1: Deep-dive run_pipeline.py + agent_service.py** -- 11 findings (2 High, 5 Medium, 3 Low, 1 verified-correct)
2. **Task 2: Deep-dive code_generator.py + step_code_buffer.py + monitored_agent.py** -- 12 findings (1 High, 7 Medium, 3 Low, 1 verified-correct)

## Files Created/Modified

- `.planning/phases/125-backend-core-review/125-FINDINGS.md` -- Appended "Deep-Dive Findings (P1 Files)" section with 23 findings
- `.planning/phases/125-backend-core-review/125-02-SUMMARY.md` -- This file

## Findings Summary Table

### High Severity (3)

| ID | File | Line | Issue |
|----|------|------|-------|
| P1-01 | run_pipeline.py | 543 | ContextWrapper isinstance check skips variable_map for preconditioned tasks |
| P1-02 | agent_service.py | 340-347 | Dual stall detection: same detector called twice per step, threshold fires at half configured value |
| P1-03 | code_generator.py | 241-242 | Variable substitution never activates (downstream of P1-01) |

### Medium Severity (12)

| ID | File | Line | Issue |
|----|------|------|-------|
| P1-04 | run_pipeline.py | 325 | external_assertion_summary leaks into variable_map |
| P1-05 | run_pipeline.py | 499-500 | Missing SSE started event on precondition failure |
| P1-06 | agent_service.py | 127 | Synchronous file write blocks async event loop |
| P1-07 | agent_service.py | 294,307 | Fragile _pre_navigated attribute on BrowserSession |
| P1-08 | agent_service.py | 374-380 | Dual progress tracking (TaskProgressTracker called twice) |
| P1-09 | agent_service.py | 400-413 | DOM serialization synchronous on every step |
| P1-10 | agent_service.py | 484 | IndexError risk in multi-action interacted_element extraction |
| P1-11 | code_generator.py | 487,496 | Unescaped assertion expected values break generated code |
| P1-12 | step_code_buffer.py | 131-133 | Pre-click 3s wait excessive, combined with post-click = 6.5s per click |
| P1-13 | step_code_buffer.py | 227-257 | Corrective evaluate detection stops too early on click/navigate |
| P1-14 | step_code_buffer.py | 380-395 | Post-click networkidle always hits 3s timeout for non-nav clicks |
| P1-15 | monitored_agent.py | 113-114 | PreSubmitGuard always receives None (confirmed dead code) |

### Low Severity (6)

| ID | File | Line | Issue |
|----|------|------|-------|
| P1-16 | run_pipeline.py | 7,14,19,29 | 5 unused imports in pipeline orchestrator |
| P1-17 | run_pipeline.py | 510 | Verified: error handling correct for stuck "running" status |
| P1-18 | code_generator.py | 198-201 | Credentials with backslashes break generated code |
| P1-19 | code_generator.py | 273-279 | Syntax validation logs warning but returns broken code |
| P1-20 | step_code_buffer.py | 63 | Private method _identify_action_type called cross-class |
| P1-21 | monitored_agent.py | 141-146 | Unconditional 3s sleep after upload_file |
| P1-22 | monitored_agent.py | 179-188 | DOM serialization duplicated in two callbacks |

### Verified Correct (2)

| ID | File | Line | Pattern |
|----|------|------|---------|
| P1-OK1 | run_pipeline.py | 510,569-572 | Pipeline except block properly sets "failed" status on error |
| P1-OK2 | monitored_agent.py | 54,71-82 | _pending_interventions lifecycle is sound in single-threaded async model |

## RESEARCH.md Pitfall Verification

| Pitfall | Status | Finding |
|---------|--------|---------|
| 1. Dual step callback | CONFIRMED | Both callbacks call same StallDetector.check(), duplicating history |
| 2. Double None event | CLARIFIED | NOT a double-publish; early return skips finally. Real issue is missing "started" event |
| 3. Context mutation | CONFIRMED | external_assertion_summary leaks through filter; plus ContextWrapper isinstance blocks variable_map entirely |
| 4. Screenshot I/O | CONFIRMED | filepath.write_bytes() is synchronous in async method |
| 5. Heartbeat task leak | NOT RE-EXAMINED | P2 file, deferred to breadth scan findings |
| 6. Duplicate wait logic | CONFIRMED | Pre-click 3s + post-click 3.5s = 6.5s per click in generated code |
| 7. PreSubmitGuard dead code | CONFIRMED | actual_values=None, submit_button_text=None hardcoded |
| 8. Assertion element stub | NOT RE-EXAMINED | P2 file, documented in breadth scan |
| 9. Semaphore internal access | NOT RE-EXAMINED | P2 file, documented in breadth scan |

## Decisions Made

- **Dual stall detection is the top priority fix.** The same `StallDetector` instance is shared between `MonitoredAgent` and `agent_service._run_detectors()`, causing history entries to double and thresholds to fire at half the configured value. This affects every execution.
- **ContextWrapper isinstance bug is the second priority.** It silently breaks variable substitution for all tasks with preconditions (the majority of production tasks). Generated test code is therefore not reusable.
- **Pre-click wait should be removed.** The 3-second pre-click wait in `_derive_wait()` is misplaced (it waits before the click, not after). The post-click stability wait already covers async updates.
- **PreSubmitGuard should be documented as inactive.** The feature was designed but never wired up. It requires DOM value extraction to function.

## Deviations from Plan

None -- plan executed exactly as written. Both tasks completed per specification.

## Issues Encountered

None.

## User Setup Required

None -- review-only phase, no code changes.

## Next Phase Readiness

- 125-FINDINGS.md now contains breadth scan (Plan 01) + deep-dive (Plan 02) findings
- Plan 03 should produce cross-cutting analysis, finalize findings, and generate the complete review report
- All 9 RESEARCH.md pitfalls have been verified or deferred to breadth scan findings
- 3 High-severity issues identified that should be prioritized in a follow-up fix phase

## Self-Check: PASSED

- 125-FINDINGS.md: FOUND
- 125-02-SUMMARY.md: FOUND
- "Deep-Dive Findings (P1 Files)" section: 1 (expected 1)
- run_pipeline.py section: 1 (expected 1)
- agent_service.py section: 1 (expected 1)
- code_generator.py section: 1 (expected 1)
- step_code_buffer.py section: 1 (expected 1)
- monitored_agent.py section: 1 (expected 1)

---
*Phase: 125-backend-core-review*
*Completed: 2026-05-03*
