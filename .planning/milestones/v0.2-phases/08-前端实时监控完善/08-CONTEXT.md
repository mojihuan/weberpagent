# Phase 8: 前端实时监控完善 - Context

**Gathered:** 2026-03-17
**Status:** Ready for planning
**Source:** Gap Closure from v0.2-MILESTONE-AUDIT.md

<domain>
## Phase Boundary

本阶段修复 v0.2 里程碑审计中发现的前端集成差距：

1. **SSE 事件处理缺失** - 前端 useRunStream.ts 不处理 `precondition` 和 `api_assertion` SSE 事件
2. **报告数据流不完整** - 后端 reports.py 未使用 ReportService.get_report_data()，导致 api_assertion_results 和 api_pass_rate 未返回前端

**Gap Closure Targets:**
- API-01: 用户可以通过 API 调用进行接口断言（当前状态：partial）
- PRE-04, API-04: 断言结果展示在测试报告中（实时显示不完整）

</domain>

<decisions>
## Implementation Decisions

### SSE 事件处理器（必须实现）

**Gap:** useRunStream.ts 只处理 started, step, finished, error 事件

**Required handlers:**

```typescript
// precondition 事件格式 (from backend/db/schemas.py SSEPreconditionEvent)
interface SSEPreconditionEvent {
  index: number
  code: string
  status: 'running' | 'success' | 'failed'
  error?: string
  duration_ms?: number
  variables?: Record<string, any>
}

// api_assertion 事件格式 (from backend/db/schemas.py SSEApiAssertionEvent)
interface SSEApiAssertionEvent {
  index: number
  code: string
  status: 'running' | 'success' | 'failed'
  error?: string
  duration_ms: number
  field_results?: ApiAssertionFieldResult[]
}
```

**Implementation location:** frontend/src/hooks/useRunStream.ts

**Action:** Add event listeners for 'precondition' and 'api_assertion' events

### Run 类型扩展（必须实现）

**Gap:** Run 接口不包含 preconditions 和 api_assertions 字段

**Required fields in Run interface:**

```typescript
interface Run {
  // existing fields...
  preconditions?: SSEPreconditionEvent[]
  api_assertions?: SSEApiAssertionEvent[]
}
```

**Implementation location:** frontend/src/types/index.ts

### 报告 API 响应完善（必须实现）

**Gap:** reports.py 直接查询数据，未使用 ReportService.get_report_data()

**Current reports.py behavior:**
- Returns ReportDetailResponse with assertion_results (mixed)
- Missing api_assertion_results, ui_assertion_results
- Missing api_pass_rate, pass_rate

**ReportService.get_report_data() returns:**
- ui_assertion_results
- api_assertion_results
- pass_rate (UI assertions)
- api_pass_rate (API assertions)

**Implementation location:** backend/api/routes/reports.py

**Action:** Use ReportService.get_report_data() instead of direct repository queries

### 前端类型更新（必须实现）

**Gap:** frontend/src/api/reports.ts ReportDetailResponse 不包含新字段

**Required fields:**

```typescript
interface ReportDetailResponse extends Report {
  steps: Step[]
  assertion_results?: AssertionResult[]
  ui_assertion_results?: AssertionResult[]  // NEW
  api_assertion_results?: AssertionResult[] // NEW
  pass_rate?: string                         // NEW
  api_pass_rate?: string                     // NEW
}
```

**Note:** frontend/src/types/index.ts already has these fields defined!

**Action:** Ensure backend returns these fields, frontend api/reports.ts transforms them

### RunMonitor UI 扩展（可选但推荐）

**Gap:** RunMonitor 组件不显示 precondition/api_assertion 进度

**Implementation location:** frontend/src/pages/RunMonitor.tsx

**Action options:**
1. Add PreconditionTimeline and ApiAssertionTimeline components
2. Or add to existing StepTimeline with different visual style

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### SSE Event Format
- `backend/db/schemas.py` lines 122-140 — SSEPreconditionEvent, SSEApiAssertionEvent definitions
- `backend/api/routes/runs.py` lines 91-112, 220-251 — SSE event publishing code

### Frontend Types
- `frontend/src/types/index.ts` lines 71-89 — ApiAssertionFieldResult, SSEApiAssertionEvent
- `frontend/src/types/index.ts` lines 160-168 — ReportDetailResponse with api_assertion_results

### Backend Services
- `backend/core/report_service.py` lines 91-134 — get_report_data() method
- `backend/api/routes/reports.py` lines 49-107 — get_report endpoint (needs update)

### Frontend Hooks
- `frontend/src/hooks/useRunStream.ts` — SSE event handling hook (needs update)
- `frontend/src/pages/RunMonitor.tsx` — Run monitor page (may need update)

### Audit Context
- `.planning/v0.2-MILESTONE-AUDIT.md` — Gap analysis source

</canonical_refs>

<specifics>
## Specific Ideas

### useRunStream.ts Changes

```typescript
// Add to existing event listeners (after line 77)

eventSource.addEventListener('precondition', (e: MessageEvent) => {
  const data: SSEPreconditionEvent = JSON.parse(e.data)
  setRun(prev => {
    if (!prev) return prev
    const preconditions = [...(prev.preconditions || []), data]
    return { ...prev, preconditions }
  })
})

eventSource.addEventListener('api_assertion', (e: MessageEvent) => {
  const data: SSEApiAssertionEvent = JSON.parse(e.data)
  setRun(prev => {
    if (!prev) return prev
    const api_assertions = [...(prev.api_assertions || []), data]
    return { ...prev, api_assertions }
  })
})
```

### reports.py Changes

```python
# Replace direct queries with ReportService
from backend.core.report_service import ReportService

@router.get("/{report_id}", response_model=ReportDetailResponse)
async def get_report(report_id: str, db: AsyncSession = Depends(get_db)):
    report_repo = ReportRepository(db)
    report = await report_repo.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Use ReportService for complete data
    report_service = ReportService(db)
    data = await report_service.get_report_data(report.run_id)

    # Build response with separated assertion results
    return ReportDetailResponse(
        ...,
        ui_assertion_results=data["ui_assertion_results"],
        api_assertion_results=data["api_assertion_results"],
        pass_rate=data["pass_rate"],
        api_pass_rate=data["api_pass_rate"],
    )
```

</specifics>

<deferred>
## Deferred Ideas

- RunMonitor UI 显示 precondition/api_assertion 进度条（可选增强）
- 前端单元测试更新（可在验证阶段补充）

</deferred>

---
*Phase: 08-前端实时监控完善*
*Context gathered: 2026-03-17 from v0.2-MILESTONE-AUDIT.md*
