---
phase: 131-后端内存与错误处理
plan: 01
subsystem: backend
tags: [memory-leak, sse, event-manager, stall-detector, asyncio, tdd]

# Dependency graph
requires: []
provides:
  - EventManager cleanup integration in run pipeline (_finalize_run + finally block)
  - EventManager heartbeat task cancellation on re-subscribe
  - StallDetector _history bounded at 1000 entries
affects: [131-02, 133-前端SSE健壮性]

# Tech tracking
tech-stack:
  added: []
  patterns: [run-lifecycle-cleanup, bounded-history-collection, heartbeat-task-cancellation]

key-files:
  created:
    - backend/tests/test_event_manager.py
    - backend/tests/test_stall_detector_history.py
  modified:
    - backend/core/event_manager.py
    - backend/api/routes/run_pipeline.py
    - backend/agent/stall_detector.py

key-decisions:
  - "Slice assignment for _history truncation creates new list (immutable pattern per CLAUDE.md)"
  - "Cleanup in both _finalize_run and finally block ensures resources freed on success and failure paths"
  - "Heartbeat cancellation in subscribe() uses await-after-cancel pattern to ensure clean shutdown"

patterns-established:
  - "Run lifecycle cleanup: event_manager.cleanup(run_id) at end of run pipeline"
  - "Bounded collection: _MAX_HISTORY class constant with slice truncation"
  - "Task cancellation guard: cancel + await CancelledError before creating replacement task"

requirements-completed: [MEM-01, MEM-02, MEM-04]

# Metrics
duration: 7min
completed: 2026-05-04
---

# Phase 131 Plan 01: EventManager Memory Leak + SSE Protection Summary

**EventManager cleanup integration with run lifecycle, heartbeat task cancellation on re-subscribe, StallDetector history bounded at 1000 entries**

## Performance

- **Duration:** 7 min
- **Started:** 2026-05-04T08:49:03Z
- **Completed:** 2026-05-04T08:55:54Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- Fixed EventManager._events memory leak by calling cleanup(run_id) in both _finalize_run() and run_agent_background finally block
- Fixed heartbeat task leak by cancelling old task before creating new one on re-subscribe
- Fixed StallDetector._history unbounded growth with 1000-entry cap preserving most recent records
- cleanup() now also removes _heartbeat_tasks entries (was missing from original cleanup)

## Task Commits

Each task was committed atomically:

1. **Task 1: TDD RED -- Write failing tests** - `7673cbc` (test)
2. **Task 2: Implement fixes (GREEN)** - `ee27a07` (feat)

_TDD: RED (5 tests defined, 4 failing) -> GREEN (all 15 tests passing)_

## Files Created/Modified
- `backend/tests/test_event_manager.py` - 3 tests: cleanup removes all data, heartbeat cancellation on re-subscribe, _finalize_run calls cleanup
- `backend/tests/test_stall_detector_history.py` - 2 tests: _history capped at 1000, most recent preserved
- `backend/core/event_manager.py` - subscribe() cancels old heartbeat before new; cleanup() handles _heartbeat_tasks
- `backend/api/routes/run_pipeline.py` - cleanup(run_id) in _finalize_run and finally block
- `backend/agent/stall_detector.py` - _MAX_HISTORY constant + slice truncation after append

## Decisions Made
- Slice assignment (`self._history = self._history[-self._MAX_HISTORY:]`) creates a new list, following immutability pattern from CLAUDE.md
- Cleanup placed in both _finalize_run (normal success path) and finally block (error path) to cover all exit scenarios
- Heartbeat cancellation uses cancel + await pattern to ensure clean task shutdown before replacement

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Initial test for test_subscribe_cancels_old_heartbeat needed careful async generator driving: used call_soon + Queue.put to unblock generator iteration without triggering heartbeat sleep timeout

## Next Phase Readiness
- EventManager memory leak fixed, ready for 131-02 (SSE error handling + assertion service)
- Heartbeat cancellation tested and working
- All 15 backend tests passing

---
*Phase: 131-后端内存与错误处理*
*Completed: 2026-05-04*

## Self-Check: PASSED

- All 5 created/modified files verified present
- Commit 7673cbc (test RED) verified
- Commit ee27a07 (feat GREEN) verified
