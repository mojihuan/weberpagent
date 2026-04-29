---
phase: 122-重复逻辑合并
plan: 01
subsystem: api, database
tags: [refactoring, deduplication, base-class, fastapi, sqlalchemy]

# Dependency graph
requires:
  - phase: 121-dead-code-cleanup
    provides: pyflakes-clean codebase with zero warnings
provides:
  - backend/api/helpers.py shared helpers (_build_task_dict, _parse_task_json_fields, raise_not_found)
  - BaseRepository base class with _persist method for all 8 repository classes
  - _check_attribute unified assertion check pattern
  - Two deprecated methods deleted (create_with_sequence, run_all_assertions)
affects: [122-02-PLAN, future phase 123 naming normalization]

# Tech tracking
tech-stack:
  added: []
  patterns: [BaseRepository inheritance for SQLAlchemy repositories, shared API helpers module, generic attribute check pattern]

key-files:
  created:
    - backend/api/helpers.py
  modified:
    - backend/api/routes/tasks.py
    - backend/api/routes/runs.py
    - backend/api/routes/batches.py
    - backend/db/repository.py
    - backend/core/assertion_service.py

key-decisions:
  - "Only applied _check_attribute to check_url_contains and check_text_exists; kept check_no_errors and check_element_exists as-is since their patterns differ enough that the abstraction would reduce readability"
  - "Created backend/api/__init__.py as empty file (was missing, needed for module imports)"
  - "Kept Chinese error messages in runs.py (代码文件不存在, 执行记录不存在, etc.) unchanged since raise_not_found is for generic entity-not-found patterns only"

patterns-established:
  - "BaseRepository._persist(entity): centralizes session.add/commit/refresh for all repository create methods"
  - "raise_not_found(entity_type, entity_id): standard 404 error raising across all API routes"
  - "_build_task_dict(task): single source of truth for task response dict construction"
  - "_parse_task_json_fields(task): single source of truth for JSON field parsing"

requirements-completed: [DUP-01, DUP-02, DUP-03]

# Metrics
duration: 7min
completed: 2026-04-29
---

# Phase 122 Plan 01: API Routes + Repository + Assertion Dedup Summary

**Extracted shared helpers module, BaseRepository base class with _persist, unified assertion _check_attribute pattern, deleted 2 deprecated methods -- eliminating 6 of 13 duplicate patterns across routes, repositories, and assertions**

## Performance

- **Duration:** 7 min
- **Started:** 2026-04-29T13:52:30Z
- **Completed:** 2026-04-29T13:59:49Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments
- Created backend/api/helpers.py with 3 shared functions, eliminating duplicate task dict construction (#1), JSON parse blocks (#2), and 404 guard patterns (#12)
- Introduced BaseRepository base class with _persist method, applied to all 8 repository classes (#8, #9)
- Deleted AssertionResultRepository.create_with_sequence (100% identical to create) and AssertionService.run_all_assertions (deprecated, zero callers)
- Extracted _check_attribute helper to unify check_url_contains and check_text_exists (#6)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create API helpers + refactor routes for #1, #2, #12** - `5d083d0` (refactor)
2. **Task 2: BaseRepository + delete deprecated methods for #6, #7, #8, #9** - `41cfa56` (refactor)

## Files Created/Modified
- `backend/api/helpers.py` - New shared helpers module (_build_task_dict, _parse_task_json_fields, raise_not_found)
- `backend/api/routes/tasks.py` - Replaced duplicate dict construction and 404 guards with helpers
- `backend/api/routes/runs.py` - Replaced JSON parse block and 404 guards with helpers
- `backend/api/routes/batches.py` - Replaced JSON parse block and 404 guards with helpers, removed unused json/HTTPException imports
- `backend/db/repository.py` - Added BaseRepository base class, all repos inherit and use _persist, deleted create_with_sequence
- `backend/core/assertion_service.py` - Added _check_attribute helper, deleted run_all_assertions and import warnings

## Decisions Made
- Only applied _check_attribute to check_url_contains and check_text_exists; kept check_no_errors and check_element_exists as-is since their patterns (boolean is_done check, CSS selector check) differ enough that forcing the abstraction would reduce readability
- Kept domain-specific Chinese error messages in runs.py (e.g., "代码文件不存在") unchanged; raise_not_found handles only generic entity-not-found patterns
- Used judgment per plan instructions: did not force _check_attribute where it doesn't fit cleanly

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- 6 of 13 duplicate patterns resolved; remaining 7 patterns (#3, #4, #5, #10, #11, #13 in external_precondition_bridge.py + #5 in agent/) are in plan 122-02
- All route imports verified, FastAPI starts cleanly, pyflakes zero warnings on all modified files

## Self-Check: PASSED

All 7 files exist on disk. Both task commits (5d083d0, 41cfa56) found in git log.

---
*Phase: 122-重复逻辑合并*
*Completed: 2026-04-29*
