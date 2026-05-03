---
phase: 126-api
plan: 01
subsystem: api
tags: [security, review, api-routes, fastapi, ruff, mypy]

# Dependency graph
requires:
  - phase: 125-backend-core-review
    provides: "Phase 125 FINDINGS.md with 32 backend core findings, CONCERNS.md verification baseline"
provides:
  - "126-FINDINGS.md with risk priority matrix for all 13 API files"
  - "Security check matrix covering 8 categories across 10 route files"
  - "CONCERNS.md verification with dual severity assessment (current + public internet)"
  - "12 API-layer findings with P1/P2/P3 classification"
affects: [126-api, security, code-review]

# Tech tracking
tech-stack:
  added: []
  patterns: ["8-category security check matrix per route file", "P1/P2/P3 risk classification for route files"]

key-files:
  created:
    - .planning/phases/126-api/126-FINDINGS.md
  modified: []

key-decisions:
  - "P1 files: 7 files involving code execution, external modules, or subprocess calls"
  - "P2 files: 3 CRUD routes with moderate validation concerns"
  - "P3 files: 3 simple/read-only routes with minimal attack surface"
  - "API-01 (path validation gap in code execution) rated High -- highest priority fix for Plan 2"

patterns-established:
  - "Security check matrix: 8 categories (param validation, error handling, path traversal, CORS/auth, code execution, SSRF, credential exposure, SSE stream errors)"
  - "Dual severity assessment: current impact (single-user internal) + public internet impact"

requirements-completed: [CORR-02, SEC-01]

# Metrics
duration: 12min
completed: 2026-05-03
---

# Phase 126 Plan 01: API Breadth Scan Summary

**Breadth scan of 13 API layer files producing risk matrix, security check matrix, and CONCERNS.md verification**

## Performance

- **Duration:** 12 min
- **Started:** 2026-05-03T04:57:34Z
- **Completed:** 2026-05-03T05:09:33Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments
- All 13 API files read and assessed across 8 security categories
- Risk priority matrix classifies 7 P1, 3 P2, 3 P3 files with justification
- Security check matrix covers 8 categories across all 10 route files
- All 6 CONCERNS.md security issues verified with dual severity assessment
- 12 API-layer findings documented (1 High, 6 Medium, 5 Low)
- ruff (17 issues) and mypy (58 errors) tool results captured
- P3 quick-scan findings documented for dashboard.py, response.py, __init__.py, runs.py

## Task Commits

Each task was committed atomically:

1. **Task 1: Read all 13 API files, run ruff/mypy, produce risk matrix and CONCERNS.md verification** - `3469544` (docs)

## Files Created/Modified
- `.planning/phases/126-api/126-FINDINGS.md` - Complete breadth scan results with risk matrix, security check matrix, CONCERNS.md verification, P3 findings, 12 API-layer findings

## Decisions Made
- P1 files include all 4 external_* routes due to code execution surface (execute_assertion_method, execute_data_method, generate_precondition_code)
- API-01 (execute_run_code path validation gap) rated as the highest-priority finding at High severity
- SSE stream error handling (API-03) rated Medium since EventManager has its own try/finally that handles most cases
- Response format inconsistency (API-08) rated Low since the frontend already handles both formats

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- .planning directory is in .gitignore, requiring `git add -f` to stage the findings file

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- 126-FINDINGS.md provides complete risk matrix and finding inventory for Plan 2 deep-dive
- P1 files (7) identified for deep-dive review: main.py, run_pipeline.py, runs_routes.py, batches.py, external_assertions.py, external_data_methods.py, external_operations.py
- Top finding (API-01: path validation gap) should be primary focus of Plan 2
- Plan 3 will cover P2 files (tasks.py, reports.py, runs.py) and P3 files plus overall summary

---
*Phase: 126-api*
*Completed: 2026-05-03*
