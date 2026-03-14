---
phase: 03-service-layer-restoration
plan: "01"
subsystem: assertion
tags: [orm, repository, service-layer, tdd]
requires: [02-01, 02-02, 02-03]
provides: [AssertionResultRepository, AssertionService ORM integration]
affects: [assertion-evaluation, test-reporting]
tech_stack:
  added:
    - sqlalchemy.ext.asyncio.AsyncSession
    - AssertionResultRepository pattern
  patterns:
    - Repository pattern for AssertionResult
    - Service-Repository-Model layering
    - Async/await throughout service layer
key_files:
  created:
    - backend/tests/unit/test_assertion_result_repo.py
    - backend/tests/unit/test_assertion_service.py
  modified:
    - backend/db/repository.py
    - backend/core/assertion_service.py
decisions:
  - AssertionService accepts AsyncSession in constructor
  - Check methods return tuple (passed, message, actual_value)
  - evaluate_all() returns list[AssertionResult] ORM objects
  - Failed assertion messages in Chinese format
  - run_all_assertions deprecated but kept for backward compatibility
  - element_exists assertion type added (fallback implementation)
metrics:
  duration: 5 min
  tasks_completed: 2
  files_modified: 4
  tests_added: 25
  completed_date: 2026-03-14
---

# Phase 3 Plan 1: AssertionService ORM Adaptation Summary

## One-liner

Adapted AssertionService to ORM pattern with AsyncSession, created AssertionResultRepository for persistent assertion results, and added element_exists assertion type.

## What Was Done

### Task 1: AssertionResultRepository Implementation

Added `AssertionResultRepository` class to `backend/db/repository.py` following the existing repository pattern:

- `create(run_id, assertion_id, status, message, actual_value)` - Creates and persists AssertionResult
- `list_by_run(run_id)` - Lists all assertion results for a run, ordered by created_at

### Task 2: AssertionService ORM Adaptation

Modified `backend/core/assertion_service.py` to integrate with the ORM layer:

- Constructor now accepts `AsyncSession` and creates `AssertionResultRepository` internally
- All check methods now return `tuple[bool, str, str]` (passed, message, actual_value)
- Added `check_element_exists()` method for new assertion type
- Added `evaluate_all()` method that returns `list[AssertionResult]` ORM objects
- Failed assertions include detailed Chinese messages (e.g., "URL 不包含 'dashboard'，实际为 'login'")
- `run_all_assertions()` marked as deprecated but kept for backward compatibility

## Key Decisions

1. **AsyncSession in constructor** - AssertionService now requires a database session, making it a proper service layer component
2. **Tuple return type for check methods** - Provides rich information (pass/fail, message, actual value) for each assertion
3. **Chinese error messages** - Failed assertions use format "URL 不包含 'X'，实际为 'Y'" for QA user friendliness
4. **Backward compatibility** - `run_all_assertions()` kept but deprecated, allowing gradual migration

## Files Changed

| File | Change |
|------|--------|
| `backend/db/repository.py` | Added AssertionResultRepository class |
| `backend/core/assertion_service.py` | ORM integration, tuple returns, evaluate_all() |
| `backend/tests/unit/test_assertion_result_repo.py` | New test file (5 tests) |
| `backend/tests/unit/test_assertion_service.py` | New test file (20 tests) |

## Test Coverage

- **AssertionResultRepository**: 5 tests covering create and list_by_run
- **AssertionService**: 20 tests covering initialization, all check methods, evaluate_all, and backward compatibility
- **Total**: 25 tests, all passing

## Verification

```bash
# All tests pass
uv run pytest backend/tests/unit/test_assertion_result_repo.py backend/tests/unit/test_assertion_service.py -v
# 25 passed

# Imports verified
uv run python -c "from backend.db.repository import AssertionResultRepository; print('OK')"
uv run python -c "from backend.core.assertion_service import AssertionService; print(hasattr(AssertionService, 'evaluate_all'))"
```

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check

- [x] AssertionResultRepository class exists with create() and list_by_run() methods
- [x] AssertionService accepts AsyncSession, has evaluate_all() returning list[AssertionResult]
- [x] element_exists assertion type implemented
- [x] Failed assertion messages follow format: "URL 不包含 'X'，实际为 'Y'"
- [x] All unit tests pass (25 tests)
- [x] Commits exist: 24ec37b, a9ff46a
