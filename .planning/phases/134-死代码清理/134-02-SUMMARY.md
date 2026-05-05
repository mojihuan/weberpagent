---
phase: 134-死代码清理
plan: 02
subsystem: ui
tags: [react-query, hooks, useQuery, refetchInterval, frontend]

# Dependency graph
requires:
  - phase: 133-前端SSE健壮性
    provides: "useRunStream hook (not modified, separate concern)"
provides:
  - "4 frontend data hooks migrated to React Query useQuery"
  - "Consolidated server state management pattern via @tanstack/react-query"
affects: [frontend-hooks, dashboard, tasks, reports, batch-progress]

# Tech tracking
tech-stack:
  added: []
  patterns: ["useQuery for server state + useState for local state separation", "refetchInterval for polling", "queryKey hierarchical format ['resource', {params}]"]

key-files:
  created: []
  modified:
    - frontend/src/hooks/useDashboard.ts
    - frontend/src/hooks/useBatchProgress.ts
    - frontend/src/hooks/useReports.ts
    - frontend/src/hooks/useTasks.ts

key-decisions:
  - "useQuery refetchInterval callback with query.state.data check replaces manual setInterval + completedRef pattern"
  - "useTasks local state (sorting, pagination, selection) kept as useState/useMemo per D-04 separation of concerns"
  - "useReports page reset via prevFilters comparison pattern instead of useEffect to avoid extra render cycle"
  - "fetchTasks alias preserved as refetch for backward compatibility with Tasks.tsx consumer"

patterns-established:
  - "useQuery for server state + useState for local state: server data (API responses) via useQuery, UI state (sorting, pagination, selection) via useState/useMemo"
  - "Hierarchical queryKey: ['resource', {param1, param2, ...}] for automatic refetch on param change"
  - "refetchInterval callback pattern: check query.state.data for dynamic polling control"

requirements-completed: [DEAD-02]

# Metrics
duration: 5min
completed: 2026-05-05
---

# Phase 134 Plan 02: React Query Migration Summary

**Migrated 4 frontend data hooks to @tanstack/react-query useQuery, reducing 340 lines to 244 lines (~28% reduction) with zero consumer page changes**

## Performance

- **Duration:** 5min
- **Started:** 2026-05-05T03:05:34Z
- **Completed:** 2026-05-05T03:10:39Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- useDashboard: 43 -> 22 lines (49% reduction), useState+useEffect+manual fetch replaced by useQuery
- useBatchProgress: 68 -> 31 lines (54% reduction), setInterval polling replaced by useQuery+refetchInterval
- useReports: 93 -> 68 lines (27% reduction), manual fetch+error state replaced by useQuery with reactive queryKey
- useTasks: 136 -> 123 lines (10% reduction), server fetch replaced by useQuery while preserving local sorting/pagination/selection state

## Task Commits

Each task was committed atomically:

1. **Task 1: Migrate useDashboard and useBatchProgress** - `0f1b49c` (refactor)
2. **Task 2: Migrate useReports and useTasks** - `ae6fb86` (refactor)

## Files Created/Modified
- `frontend/src/hooks/useDashboard.ts` - Single useQuery call replacing useState+useEffect+manual fetch, with DEFAULT_DATA fallback
- `frontend/src/hooks/useBatchProgress.ts` - useQuery with refetchInterval callback checking data.status for dynamic polling stop
- `frontend/src/hooks/useReports.ts` - useQuery with reactive queryKey [reports, {status, dateRange, page, pageSize}], prevFilters page reset pattern
- `frontend/src/hooks/useTasks.ts` - useQuery for server data + useMemo for sorting/pagination, batch operations use refetch()

## Decisions Made
- Used refetchInterval callback (query) => query.state.data?.status pattern instead of useEffect+setInterval+completedRef for cleaner polling control
- Kept local state (sorting, pagination, selection) as useState/useMemo in useTasks since these are UI concerns, not server state (per D-04)
- Used prevFilters comparison pattern in useReports for page reset on filter change instead of useEffect to avoid extra render cycle
- Preserved fetchTasks as alias for refetch in useTasks return for backward compatibility with Tasks.tsx consumer

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Removed unused Task type import from useTasks.ts**
- **Found during:** Task 2 (useReports and useTasks migration)
- **Issue:** After migration, Task type was only used implicitly via tasksApi.list() return type inference, triggering noUnusedLocals error with verbatimModuleSyntax
- **Fix:** Removed `import type { Task }` since the type is correctly inferred by useQuery from the queryFn return
- **Files modified:** frontend/src/hooks/useTasks.ts
- **Verification:** tsc --noEmit passes clean
- **Committed in:** ae6fb86 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Trivial fix for build compliance. No scope creep.

## Issues Encountered
- Pre-existing useRunStream.ts build errors (TS2304, TS2322) are unrelated to this plan -- from Phase 133, out of scope

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 134 complete. All 4 React Query consumers are active (useDashboard, useBatchProgress, useReports, useTasks)
- React Query auto-caching, retry, and refetch capabilities now available across all data-fetching hooks
- v0.11.4 milestone complete -- all 5 systemic patterns (CP-1 through CP-5) addressed

---
*Phase: 134-死代码清理*
*Completed: 2026-05-05*

## Self-Check: PASSED

All 5 modified files verified present. Both task commits (0f1b49c, ae6fb86) verified in git log.
