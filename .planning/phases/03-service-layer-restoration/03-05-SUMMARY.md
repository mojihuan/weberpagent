---
phase: 03-service-layer-restoration
plan: "05"
subsystem: background-tasks
tags: [integration, status-updates, report-service, assertion-service]
requires: [03-01, 03-02]
provides: [ReportService integration, AssertionService integration, status updates]
affects: [run-agent-background, test-reports]
tech_stack:
  added:
    - ReportService integration in background task
    - AssertionService.evaluate_all() before final status
  patterns:
    - Service layer pattern
    - Repository pattern
    - try/except/finally status updates
key_files:
  created:
    - backend/tests/integration/test_runs_background.py
  modified:
    - backend/api/routes/runs.py
decisions:
  - ReportService.generate_report() called after agent execution completes
  - AssertionService.evaluate_all() called before final status determination
  - Failed assertions change overall status to "failed"
  - Status updates in all paths (success, error)
  - Error events published via SSE on failure
metrics:
  duration: 5 min
  tasks_completed: 1
  files_modified: 2
  tests_added: 5
  completed_date: 2026-03-14
---

# Phase 3 Plan 5: Background Task Status Updates Summary

## One-liner

Integrated ReportService and AssertionService into background task with proper status updates on completion/error, replacing inline report generation with service-based approach.

## What Was Done

### Task 1: Integrate ReportService into Background Task

Modified `backend/api/routes/runs.py` to integrate both services:

**Added imports:**
```python
from backend.core.report_service import ReportService
from backend.core.assertion_service import AssertionService
```

**Service instantiation:**
```python
report_service = ReportService(session)
assertion_service = AssertionService(session)
```

**Assertion evaluation before final status:**
```python
# Evaluate assertions if task has any
run = await run_repo.get_with_task(run_id)
if run and run.task and run.task.assertions:
    assertion_results = await assertion_service.evaluate_all(
        run_id=run_id,
        assertions=run.task.assertions,
        history=result,
    )
    # If any assertion failed, overall status is failed
    if any(ar.status == "fail" for ar in assertion_results):
        final_status = "failed"
```

**Report generation:**
```python
# Generate report using ReportService
await report_service.generate_report(run_id)
```

**Removed inline report generation code** (30+ lines of inline report creation replaced with single service call)

### Tests Created

Created `backend/tests/integration/test_runs_background.py` with 5 tests:
1. `test_run_status_updated_on_success` - Verifies status is "success" after successful run
2. `test_run_status_updated_on_error` - Verifies status is "failed" after error
3. `test_error_event_published_on_failure` - Verifies SSE error event is published
4. `test_report_service_integrated` - Verifies ReportService.generate_report() is called
5. `test_assertion_service_evaluates_before_status` - Verifies assertion evaluation before final status

## Key Decisions

1. **Service-based report generation** - Replaced 30+ lines of inline report creation with single `report_service.generate_report(run_id)` call
2. **Assertion evaluation affects status** - Failed assertions change overall run status to "failed"
3. **All paths update status** - Both success and error paths properly update database status
4. **Error events via SSE** - Failures publish error events for real-time client notification

## Files Changed

| File | Change |
|------|--------|
| `backend/api/routes/runs.py` | Added ReportService/AssertionService imports, service instantiation, assertion evaluation, report generation |
| `backend/tests/integration/test_runs_background.py` | New test file (5 tests) |

## Verification

```bash
# Verify ReportService is used
grep -n "report_service.generate_report" backend/api/routes/runs.py
# 153:            await report_service.generate_report(run_id)

# Verify AssertionService is used
grep -n "assertion_service.evaluate_all" backend/api/routes/runs.py
# 127:                assertion_results = await assertion_service.evaluate_all(

# Verify imports
grep -n "from backend.core.report_service import ReportService" backend/api/routes/runs.py
# 25:from backend.core.report_service import ReportService

grep -n "from backend.core.assertion_service import AssertionService" backend/api/routes/runs.py
# 26:from backend.core.assertion_service import AssertionService
```

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check

- [x] ReportService imported in runs.py
- [x] AssertionService imported in runs.py
- [x] report_service.generate_report(run_id) called after execution
- [x] assertion_service.evaluate_all() called before final status
- [x] Status updates in success path
- [x] Status updates in error path
- [x] Error events published on failure
- [x] Test file created with 5 tests
- [x] Commits exist: e767e6f (test), 0903156 (feat)
