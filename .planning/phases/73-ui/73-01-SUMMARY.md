---
phase: 73-ui
plan: 01
subsystem: api
tags: [pydantic, typescript, fastapi, batch]

# Dependency graph
requires:
  - phase: 72-batch-execution
    provides: BatchRunSummary schema, Run ORM model with started_at/finished_at
provides:
  - BatchRunSummary Pydantic schema with started_at/finished_at datetime fields
  - Backend route handlers passing timing fields in BatchRunSummary construction
  - Frontend BatchRunSummary TypeScript interface with started_at/finished_at nullable string fields
affects: [73-02, batch-progress-ui]

# Tech tracking
tech-stack:
  added: []
  patterns: [timing-fields-bridge-between-orm-and-api]

key-files:
  created: []
  modified:
    - backend/db/schemas.py
    - backend/api/routes/batches.py
    - frontend/src/types/index.ts

key-decisions:
  - "Nullable Optional[datetime] for timing fields (None before task starts, populated after)"

patterns-established:
  - "BatchRunSummary timing bridge: ORM datetime fields exposed as Optional[datetime] in Pydantic, string|null in TypeScript"

requirements-completed: [BATCH-03]

# Metrics
duration: 2min
completed: 2026-04-09
---

# Phase 73 Plan 01: BatchRunSummary Timing Fields Summary

**Extended BatchRunSummary with started_at/finished_at nullable datetime fields across backend schema, API routes, and frontend TypeScript type**

## Performance

- **Duration:** 2 min
- **Started:** 2026-04-09T01:15:02Z
- **Completed:** 2026-04-09T01:17:14Z
- **Tasks:** 1
- **Files modified:** 3

## Accomplishments
- Added started_at and finished_at Optional[datetime] fields to BatchRunSummary Pydantic schema
- Updated both BatchRunSummary construction sites in batches.py (get_batch and get_batch_runs) to pass timing fields
- Added started_at and finished_at nullable string fields to frontend BatchRunSummary TypeScript interface

## Task Commits

Each task was committed atomically:

1. **Task 1: Extend BatchRunSummary with timing fields** - `32b5b2a` (feat)

## Files Created/Modified
- `backend/db/schemas.py` - Added started_at/finished_at Optional[datetime] fields to BatchRunSummary
- `backend/api/routes/batches.py` - Pass run.started_at/run.finished_at in both BatchRunSummary constructions
- `frontend/src/types/index.ts` - Added started_at/finished_at string|null fields to BatchRunSummary interface

## Decisions Made
None - followed plan as specified.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- BatchRunSummary now includes timing data needed for batch progress UI elapsed time display
- Ready for Plan 73-02: Frontend batch progress page with polling, cards, navigation, toast

## Self-Check: PASSED

- All 3 modified files exist: backend/db/schemas.py, backend/api/routes/batches.py, frontend/src/types/index.ts
- Task commit 32b5b2a found in git log
- SUMMARY.md created at .planning/phases/73-ui/73-01-SUMMARY.md

---
*Phase: 73-ui*
*Completed: 2026-04-09*
