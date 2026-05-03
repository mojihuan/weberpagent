---
phase: 126-api
plan: 02
subsystem: api
tags: [fastapi, security-audit, parameter-validation, sse, cors, subprocess, external-modules]

# Dependency graph
requires:
  - phase: 126-api
    plan: 01
    provides: "Breadth scan findings, risk priority matrix, P1/P2/P3 file classification"
provides:
  - "Deep-dive findings for all 7 P1 API route files"
  - "Per-endpoint security audit with dual severity assessment"
  - "SSE stream error handling analysis"
  - "Code execution surface documentation for external_* routes"
affects: [126-api-plan-03, codebase-concerns]

# Tech tracking
tech-stack:
  added: []
  patterns: [per-endpoint-security-audit, dual-severity-assessment]

key-files:
  created: []
  modified:
    - ".planning/phases/126-api/126-FINDINGS.md"

key-decisions:
  - "P1 deep-dive covers API-layer concerns only for run_pipeline.py (no Phase 125 duplication)"
  - "All security findings assessed against public internet standard with dual severity"
  - "Fire-and-forget, SSRF, and code execution surface patterns documented per route"

patterns-established:
  - "Per-endpoint audit: param validation, error handling, security, SSE stream"
  - "Dual severity: current impact (single-user) + public internet impact"

requirements-completed: [CORR-02, SEC-01]

# Metrics
duration: 7min
completed: 2026-05-03
---

# Phase 126 Plan 02: P1 Deep-Dive Audit Summary

**Deep-dive audit of 7 P1 API route files: 47 findings across parameter validation, error handling, security, and SSE stream handling with per-endpoint severity ratings**

## Performance

- **Duration:** 7 min
- **Started:** 2026-05-03T05:05:57Z
- **Completed:** 2026-05-03T05:13:43Z
- **Tasks:** 2
- **Files modified:** 1 (126-FINDINGS.md)

## Accomplishments
- Audited all 7 P1 route files (main.py, runs_routes.py, run_pipeline.py, batches.py, external_assertions.py, external_data_methods.py, external_operations.py) with 47 deep-dive findings
- Identified 1 High severity issue: execute_run_code endpoint missing _validate_code_path before subprocess.run (DD-runs-06)
- Documented 12 Medium severity issues including CORS misconfiguration, hardcoded DEBUG logging, SSE stream error handling gaps, SSRF via api_params/params, fire-and-forget batch execution
- All security findings include dual severity assessment (current single-user impact + public internet impact)
- Verified 6 CONCERNS.md entries with updated severity assessments per public internet standard

## Task Commits

Each task was committed atomically:

1. **Task 1: Deep-dive audit main.py, runs_routes.py, run_pipeline.py** - `e2ed314` (docs)
2. **Task 2: Deep-dive audit batches.py and external_* routes** - `d93b3ef` (docs)

## Files Created/Modified
- `.planning/phases/126-api/126-FINDINGS.md` - Appended 47 deep-dive findings with severity, category, file:line references, recommendations, and RESEARCH pitfall references

## Decisions Made
- Followed D-01 strictly: run_pipeline.py API-layer concerns only, no duplication of Phase 125 business logic findings
- Applied D-03: all security findings have dual severity assessment (current + public internet)
- Cross-referenced all findings with RESEARCH.md pitfalls where applicable
- Included 8 findings at Low severity that document architecture concerns (unused imports, inconsistent naming, print statements)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - all source files read successfully, findings appended to existing FINDINGS.md without overwrite.

## User Setup Required

None - review-only phase, no code changes.

## Next Phase Readiness
- All 7 P1 files have complete deep-dive findings appended to 126-FINDINGS.md
- Plan 03 (P2+P3+summary) can proceed to audit P2 routes (tasks.py, reports.py, runs.py) and produce the phase summary
- CONCERNS.md verification complete: 6 entries confirmed, 8 new issues identified not in CONCERNS.md

## Finding Statistics

| File | Findings | Critical | High | Medium | Low |
|------|----------|----------|------|--------|-----|
| main.py | 8 | 0 | 0 | 4 | 4 |
| runs_routes.py | 12 | 0 | 1 | 6 | 5 |
| run_pipeline.py (API layer) | 8 | 0 | 0 | 2 | 6 |
| batches.py | 6 | 0 | 0 | 3 | 3 |
| external_assertions.py | 4 | 0 | 0 | 2 | 2 |
| external_data_methods.py | 4 | 0 | 0 | 2 | 2 |
| external_operations.py | 5 | 0 | 0 | 1 | 4 |
| **Total** | **47** | **0** | **1** | **20** | **26** |

## Self-Check: PASSED

- FOUND: 126-02-SUMMARY.md
- FOUND: 126-FINDINGS.md
- FOUND: e2ed314 (Task 1 commit)
- FOUND: d93b3ef (Task 2 commit)

---
*Phase: 126-api*
*Completed: 2026-05-03*
