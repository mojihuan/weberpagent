---
phase: 02-data-layer-enhancement
plan: 02
subsystem: data-layer
tags: [repository, tdd, run-steps]
dependency_graph:
  requires: [02-00]
  provides: [RunRepository.get_steps]
  affects: [run-management, step-retrieval]
tech_stack:
  added: []
  patterns: [SQLAlchemy async query, TDD]
key_files:
  created: []
  modified:
    - backend/db/repository.py
    - backend/tests/unit/test_repository.py
    - backend/tests/conftest.py
decisions:
  - Added db_session fixture to conftest.py for repository tests
  - get_steps follows existing StepRepository.list_by_run pattern
metrics:
  duration: 4 min
  completed_date: 2026-03-14
  task_count: 1
  file_count: 3
---

# Phase 02 Plan 02: RunRepository get_steps Method Summary

## One-liner

Added `RunRepository.get_steps()` method that returns all steps for a run ordered by step_index, following TDD workflow.

## What Was Built

Implemented `RunRepository.get_steps()` method following the existing repository pattern. The method:
- Accepts a `run_id` parameter
- Returns `List[Step]` ordered by `step_index` ascending
- Returns empty list for non-existent run_id
- Follows the same pattern as `StepRepository.list_by_run`

## Changes Made

### backend/db/repository.py
Added `get_steps` method to `RunRepository` class:
```python
async def get_steps(self, run_id: str) -> List[Step]:
    """Get all steps for a run, ordered by step_index."""
    stmt = select(Step).where(Step.run_id == run_id).order_by(Step.step_index)
    result = await self.session.execute(stmt)
    return list(result.scalars())
```

### backend/tests/conftest.py
Added `db_session` fixture for repository tests that creates fresh database tables for each test.

### backend/tests/unit/test_repository.py
Added `TestRunRepositoryGetSteps` class with 4 test cases:
1. `test_get_steps_returns_steps_for_run` - Returns list of Step objects
2. `test_get_steps_ordered_by_step_index` - Steps ordered by step_index ascending
3. `test_get_steps_empty_for_nonexistent_run` - Empty list for non-existent run
4. `test_get_steps_only_returns_steps_for_specified_run` - Only returns steps for specified run

## Deviations from Plan

None - plan executed exactly as written.

## Test Results

All 4 tests pass:
```
backend/tests/unit/test_repository.py::TestRunRepositoryGetSteps::test_get_steps_returns_steps_for_run PASSED
backend/tests/unit/test_repository.py::TestRunRepositoryGetSteps::test_get_steps_ordered_by_step_index PASSED
backend/tests/unit/test_repository.py::TestRunRepositoryGetSteps::test_get_steps_empty_for_nonexistent_run PASSED
backend/tests/unit/test_repository.py::TestRunRepositoryGetSteps::test_get_steps_only_returns_steps_for_specified_run PASSED
```

## Commits

1. `b427293` - test(02-02): add tests for RunRepository.get_steps method
2. `beb6126` - feat(02-02): implement RunRepository.get_steps method

## Self-Check: PASSED

- SUMMARY.md exists: FOUND
- Test commit b427293: FOUND
- Implementation commit beb6126: FOUND
