---
phase: 06-接口断言集成
plan: 04
subsystem: 执行流程 + 报告系统
tags: [execution-flow, api-assertions, sse-events, frontend]
dependency_graph:
  requires:
    - 06-02 (ApiAssertionService)
    - 06-03 (时间断言实现)
  provides:
    - 接口断言执行流程集成
    - 报告中接口断言结果展示
  affects:
    - backend/api/routes/runs.py
    - backend/core/report_service.py
    - frontend/src/pages/ReportDetail.tsx
tech_stack:
  added:
    - SSEApiAssertionEvent schema
    - ApiAssertionResults React component
  patterns:
    - SSE event streaming for API assertions
    - Separation of UI/API assertion results in reports
key_files:
  created:
    - frontend/src/components/Report/ApiAssertionResults.tsx
  modified:
    - backend/db/schemas.py
    - backend/api/routes/runs.py
    - backend/core/report_service.py
    - frontend/src/types/index.ts
    - frontend/src/components/Report/index.ts
    - frontend/src/pages/ReportDetail.tsx
decisions:
  - API assertions execute after UI test completion
  - Assertion results stored to AssertionResult table with api_ prefix
  - Separate pass rates for UI and API assertions in reports
  - SSE events sent for each API assertion execution status
metrics:
  duration: 55 min
  tasks_completed: 5
  files_modified: 6
  commits: 5
  completed_date: "2026-03-17"
---

# Phase 06 Plan 04: 接口断言执行流程与报告集成 Summary

## One-liner

将接口断言集成到执行流程中，在 UI 测试完成后执行 API 断言，并将断言结果展示在测试报告中。

## What Was Done

### Task 1: SSEApiAssertionEvent Schema
- Added `SSEApiAssertionEvent` class to `backend/db/schemas.py`
- Fields: index, code, status, error, duration_ms, field_results

### Task 2: 执行流程集成
- Modified `run_agent_background` to accept `api_assertions` parameter
- Integrated `ApiAssertionService` for executing API assertions after UI test
- Added SSE event publishing for API assertion status updates
- Stored assertion results to database with `api_` prefix
- Updated `create_run` endpoint to parse and pass `api_assertions`

### Task 3: 报告服务扩展
- Extended `get_report_data` to separate UI and API assertions
- Added `ui_assertion_results` and `api_assertion_results` to response
- Added `api_pass_rate` calculation

### Task 4: 前端组件创建
- Created `ApiAssertionResults.tsx` component
- Added type definitions: `ApiAssertionFieldResult`, `SSEApiAssertionEvent`
- Updated `ReportDetailResponse` to include API assertion fields

### Task 5: 报告页面集成
- Integrated `ApiAssertionResults` component into `ReportDetail.tsx`
- Displays API assertion results after UI assertions

## Deviations from Plan

None - plan executed exactly as written.

## Files Changed

| File | Changes |
|------|---------|
| backend/db/schemas.py | Added SSEApiAssertionEvent class |
| backend/api/routes/runs.py | Integrated API assertions into execution flow |
| backend/core/report_service.py | Added API assertion result separation |
| frontend/src/types/index.ts | Added API assertion types |
| frontend/src/components/Report/ApiAssertionResults.tsx | New component |
| frontend/src/components/Report/index.ts | Export new component |
| frontend/src/pages/ReportDetail.tsx | Integrated API assertion display |

## Verification Results

```
1. api_assertions in runs.py: 10 occurrences
2. ApiAssertionService in runs.py: 2 occurrences
3. SSEApiAssertionEvent in runs.py: 3 occurrences
4. api_assertion_results in report_service.py: 3 occurrences
5. ApiAssertionResults in component: 2 occurrences
6. Component file exists: yes
```

## Key Decisions

1. **API assertions execute after UI test completion** - Ensures UI state is stable before API validation
2. **Results stored with api_ prefix** - Easy separation of UI and API assertion results
3. **SSE events for each assertion** - Real-time feedback during execution
4. **Separate pass rates** - Clear visibility into UI vs API assertion status

## Self-Check: PASSED

- [x] All files created/modified exist
- [x] All commits recorded
- [x] Verification criteria met
