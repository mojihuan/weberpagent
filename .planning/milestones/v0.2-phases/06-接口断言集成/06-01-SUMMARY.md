---
phase: 06-接口断言集成
plan: "01"
subsystem: database
tags: [sqlalchemy, pydantic, typescript, react, forms]

# Dependency graph
requires: []
provides:
  - Task.api_assertions field in database model
  - TaskCreate/TaskUpdate/TaskResponse schemas with api_assertions
  - Repository serialize/deserialize methods for api_assertions
  - Frontend types with api_assertions field
  - TaskForm UI for api_assertions input
affects: [06-02, 06-03, 06-04]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - JSON string storage for list fields (same as preconditions)
    - Serialize/deserialize pattern in repository

key-files:
  created: []
  modified:
    - backend/db/models.py
    - backend/db/schemas.py
    - backend/db/repository.py
    - frontend/src/types/index.ts
    - frontend/src/components/TaskModal/TaskForm.tsx

key-decisions:
  - "Store api_assertions as JSON string in Text column, same pattern as preconditions"
  - "Use Optional[List[str]] type in schemas for consistency"

patterns-established:
  - "Repository serialize/deserialize pattern for JSON fields"

requirements-completed: [API-01]

# Metrics
duration: 4min
completed: "2026-03-16"
---

# Phase 06 Plan 01: Task Model Extension Summary

**Extended Task model and frontend forms to support API assertions with JSON string storage, following the same pattern as preconditions.**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-16T13:49:14Z
- **Completed:** 2026-03-16T13:53:00Z
- **Tasks:** 5
- **Files modified:** 5

## Accomplishments

- Added api_assertions field to Task SQLAlchemy model (Text column, nullable)
- Extended Pydantic schemas (TaskBase, TaskUpdate, TaskResponse) with api_assertions
- Implemented serialize/deserialize methods in TaskRepository for api_assertions
- Updated frontend TypeScript types (Task, CreateTaskDto, UpdateTaskDto)
- Added complete UI section in TaskForm with add/remove/change handlers

## Task Commits

Each task was committed atomically:

1. **Task 1: Add api_assertions field to Task model** - `646e434` (feat)
2. **Task 2: Add api_assertions field to Pydantic schemas** - `72941ea` (feat)
3. **Task 3: Add serialize/deserialize methods to repository** - `3da2041` (feat)
4. **Task 4: Add api_assertions field to frontend types** - `891c628` (feat)
5. **Task 5: Add api_assertions input area to TaskForm** - `3f6c982` (feat)

**Plan metadata:** (pending final commit)

## Files Created/Modified

- `backend/db/models.py` - Added api_assertions: Mapped[Optional[str]] field to Task model
- `backend/db/schemas.py` - Added api_assertions field to TaskBase, TaskUpdate, TaskResponse
- `backend/db/repository.py` - Added _serialize_api_assertions and _deserialize_api_assertions methods, updated create/update
- `frontend/src/types/index.ts` - Added api_assertions to Task, CreateTaskDto, UpdateTaskDto interfaces
- `frontend/src/components/TaskModal/TaskForm.tsx` - Added FormData field, handlers, and UI section for api_assertions

## Decisions Made

- Followed existing preconditions pattern for api_assertions storage (JSON string in Text column)
- Used Optional[List[str]] type in all schemas for consistency with preconditions
- Added textarea with monospace font for code input, matching preconditions UI style

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - straightforward implementation following established patterns.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Task model extended with api_assertions field, ready for API assertion execution service
- Frontend forms can capture API assertion code
- Repository layer handles serialization/deserialization

---
*Phase: 06-接口断言集成*
*Completed: 2026-03-16*

## Self-Check: PASSED

All files exist and commits verified.
