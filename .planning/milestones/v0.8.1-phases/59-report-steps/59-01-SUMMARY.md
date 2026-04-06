---
phase: 59-report-steps
plan: 01
status: complete
---

# Plan 59-01: Backend Persistence + Timeline API

## What was built

Backend infrastructure for persisting precondition results and exposing a unified timeline through the report detail API.

## Key Changes

- **PreconditionResult ORM model**: New model with columns: id, run_id, sequence_number, index, code, status, error, duration_ms, variables, created_at
- **PreconditionResultRepository**: `create()` and `list_by_run()` methods
- **sequence_number columns**: Added to Step and AssertionResult models (nullable Integer)
- **Run.precondition_results relationship**: Cascade delete-orphan
- **Migration logic**: `init_db()` now uses ALTER TABLE to add sequence_number to existing steps and assertion_results tables
- **Global sequence counter**: `run_agent_background` maintains `global_seq` counter, assigns sequence numbers to preconditions, steps, and assertions
- **report_service timeline_items**: `get_report_data()` builds unified timeline sorted by sequence_number
- **API assertion grouping**: Field-level API assertion results grouped into single timeline entries
- **ReportDetailResponse**: Added optional `timeline_items` field

## Verification

- 4/4 tests pass in `test_precondition_result.py`
- 3/3 tests pass in `test_report_timeline.py`
- Frontend builds successfully
- All existing backend tests unaffected

## Decisions

- D-01: Persist precondition results in new table (not in run metadata)
- D-02: Global sequence_number for cross-type ordering
- D-03: Backend merges and sorts into timeline_items
- D-04: Type discriminator field for timeline items
- D-05: timeline_items returned alongside existing fields (backward compat)
- D-06: Preserved existing summary stats (pass_rate, api_pass_rate)
- D-07: API assertion field_results grouped by assertion index

## Files Modified

- backend/db/models.py - Added PreconditionResult, Run.precondition_results, Step.sequence_number, AssertionResult.sequence_number
- backend/db/repository.py - Added PreconditionResultRepository, updated AssertionResultRepository.create signature
- backend/db/database.py - Added migration logic for existing columns
- backend/db/schemas.py - Added timeline_items to ReportDetailResponse
- backend/core/report_service.py - Added timeline_items construction in get_report_data()
- backend/api/routes/runs.py - Added global_seq counter and precondition persistence
- backend/api/routes/reports.py - Pass timeline_items to response
- backend/tests/unit/test_precondition_result.py - New test file (4 tests)
- backend/tests/unit/test_report_timeline.py - New test file (3 tests)
