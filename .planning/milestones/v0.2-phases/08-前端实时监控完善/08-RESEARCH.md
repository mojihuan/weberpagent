# Phase 8: 前端实时监控完善 - Research

**Researched:** 2026-03-17
**Domain:** Frontend SSE Event Handling, Backend API Response Format
**Confidence:** HIGH

## Summary

This is a **Gap Closure phase** addressing two specific integration issues identified in the v0.2 milestone audit:

1. **SSE Event Handling Gap** - The frontend `useRunStream.ts` hook only handles `started`, `step`, `finished`, `error` events but NOT `precondition` or `api_assertion` events. The backend correctly sends these events (verified in `runs.py` lines 91-112 and 220-251).

2. **Report Data Flow Gap** - The backend `reports.py` endpoint directly queries repositories instead of using `ReportService.get_report_data()`, which returns separated `ui_assertion_results`, `api_assertion_results`, `pass_rate`, and `api_pass_rate` fields.

**Primary recommendation:** Follow the existing patterns - the backend SSE event format and ReportService are already correct. Only frontend needs updates to consume the existing data.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### SSE 事件处理器（必须实现）

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

#### Run 类型扩展（必须实现）

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

#### 报告 API 响应完善（必须实现）

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

#### 前端类型更新（必须实现）

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

### Claude's Discretion

- RunMonitor UI 扩展 - 可选择添加 PreconditionTimeline 和 ApiAssertionTimeline 组件，或添加到现有 StepTimeline

### Deferred Ideas (OUT OF SCOPE)

- RunMonitor UI 显示 precondition/api_assertion 进度条（可选增强）
- 前端单元测试更新（可在验证阶段补充）

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| API-01 | 用户可以通过 API 调用进行接口断言 | Backend SSE events for api_assertion exist in runs.py; ReportService.get_report_data() separates UI/API assertions; Frontend types already support these fields |
</phase_requirements>

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| React | 19.2.0 | UI framework | Project standard |
| EventSource API | Native | SSE client | Browser native, no additional deps needed |
| FastAPI | 0.135.1+ | Backend framework | Project standard |
| Pydantic | 2.4.0+ | Data validation | Backend schemas use this |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| SQLAlchemy | 2.0.0+ | Database ORM | Repository pattern |
| pytest | 8.0.0+ | Testing | Unit/integration tests |
| pytest-asyncio | 0.24.0+ | Async testing | For async test fixtures |

### Existing Project Patterns

| Pattern | Location | Purpose |
|---------|----------|---------|
| SSE Event Format | backend/db/schemas.py | Pydantic models for all SSE events |
| Event Publishing | backend/api/routes/runs.py | SSE event stream via event_manager |
| Event Consumption | frontend/src/hooks/useRunStream.ts | React hook for SSE subscription |
| Report Data | backend/core/report_service.py | get_report_data() with separated assertions |
| API Transformation | frontend/src/api/reports.ts | Transform backend response to frontend types |

## Architecture Patterns

### Current SSE Flow (Working)

```
Backend runs.py                    Frontend useRunStream.ts
----------------                   -----------------------
event_manager.publish()  ------->  eventSource.addEventListener()
SSEStartedEvent                   'started' handler
SSEStepEvent                      'step' handler
SSEFinishedEvent                  'finished' handler
SSEErrorEvent                     'error' handler
SSEPreconditionEvent              MISSING
SSEApiAssertionEvent              MISSING
```

### Required Changes

**1. useRunStream.ts - Add Event Handlers**

```typescript
// Source: Pattern from existing handlers (lines 43-102)
// Add after line 77, following the same pattern

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

**2. frontend/src/types/index.ts - Extend Run Interface**

```typescript
// Source: Already has SSEApiAssertionEvent (lines 81-89)
// Add SSEPreconditionEvent and extend Run interface

export interface SSEPreconditionEvent {
  index: number
  code: string
  status: 'running' | 'success' | 'failed'
  error?: string
  duration_ms?: number
  variables?: Record<string, any>
}

// Run interface extension (line 40-47)
export interface Run {
  id: string
  task_id: string
  status: RunStatus
  started_at: string
  finished_at?: string
  steps: Step[]
  preconditions?: SSEPreconditionEvent[]     // NEW
  api_assertions?: SSEApiAssertionEvent[]    // NEW
}
```

**3. backend/api/routes/reports.py - Use ReportService**

```python
# Source: backend/core/report_service.py lines 91-134
# Replace lines 61-107 with:

from backend.core.report_service import ReportService

@router.get("/{report_id}", response_model=ReportDetailResponse)
async def get_report(
    report_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取报告详情"""
    report_repo = ReportRepository(db)
    report = await report_repo.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Use ReportService for complete data
    report_service = ReportService(db)
    data = await report_service.get_report_data(report.run_id)

    if not data:
        raise HTTPException(status_code=404, detail="Report data not found")

    # Transform steps
    step_responses = [
        StepResponse(
            id=s.id,
            run_id=s.run_id,
            step_index=s.step_index,
            action=s.action,
            reasoning=s.reasoning,
            screenshot_url=f"/api/run/{s.run_id}/screenshots/{s.step_index}" if s.screenshot_path else None,
            status=s.status,
            error=s.error,
            duration_ms=s.duration_ms,
            created_at=s.created_at,
        )
        for s in data["steps"]
    ]

    # Transform assertion results
    def transform_assertion_results(results):
        return [
            AssertionResultResponse(
                id=ar.id,
                run_id=ar.run_id,
                assertion_id=ar.assertion_id,
                status=ar.status,
                message=ar.message,
                actual_value=ar.actual_value,
                created_at=ar.created_at,
            )
            for ar in results
        ]

    return ReportDetailResponse(
        id=report.id,
        run_id=report.run_id,
        task_id=report.task_id,
        task_name=report.task_name,
        status=report.status,
        total_steps=report.total_steps,
        success_steps=report.success_steps,
        failed_steps=report.failed_steps,
        duration_ms=report.duration_ms,
        created_at=report.created_at,
        steps=step_responses,
        assertion_results=transform_assertion_results(data["assertion_results"]),
        ui_assertion_results=transform_assertion_results(data["ui_assertion_results"]),
        api_assertion_results=transform_assertion_results(data["api_assertion_results"]),
        pass_rate=data["pass_rate"],
        api_pass_rate=data["api_pass_rate"],
    )
```

**4. frontend/src/api/reports.ts - Transform New Fields**

```typescript
// Source: Existing transformReport function pattern (lines 61-66)
// Update ReportDetailApiResponse interface (lines 41-44):

interface ReportDetailApiResponse extends ReportApiResponse {
  steps: StepApiResponse[]
  assertion_results: AssertionResultApiResponse[]
  ui_assertion_results?: AssertionResultApiResponse[]   // NEW
  api_assertion_results?: AssertionResultApiResponse[]  // NEW
  pass_rate?: string                                     // NEW
  api_pass_rate?: string                                 // NEW
}

// Update getReport function (lines 114-122):
export async function getReport(reportId: string): Promise<ReportDetailResponse> {
  const response = await apiClient<ReportDetailApiResponse>(`/reports/${reportId}`)

  return {
    ...transformReport(response),
    steps: response.steps.map(transformStep),
    assertion_results: (response.assertion_results || []).map(transformAssertionResult),
    ui_assertion_results: (response.ui_assertion_results || []).map(transformAssertionResult),
    api_assertion_results: (response.api_assertion_results || []).map(transformAssertionResult),
    pass_rate: response.pass_rate,
    api_pass_rate: response.api_pass_rate,
  }
}
```

### Anti-Patterns to Avoid

- **DO NOT** add new dependencies for SSE - EventSource is browser native
- **DO NOT** change backend SSE event format - it's correct, only frontend needs updates
- **DO NOT** create new service methods - ReportService.get_report_data() already exists
- **DO NOT** mutate state in React - always create new objects when updating run state

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| SSE client | Custom WebSocket | EventSource API | Native, simpler, works with FastAPI StreamingResponse |
| State updates | Mutable push | Immutable spread | React state must be immutable |
| Report data | Custom query | ReportService.get_report_data() | Already handles UI/API separation |

## Common Pitfalls

### Pitfall 1: EventSource Event Type Mismatch
**What goes wrong:** Backend sends `event: precondition\ndata: {...}` but frontend only listens for message events
**Why it happens:** Using `eventSource.onmessage` instead of `addEventListener`
**How to avoid:** Always use `eventSource.addEventListener('eventname', handler)` for named events
**Warning signs:** Events appear in Network tab but UI doesn't update

### Pitfall 2: Immutable State Violation
**What goes wrong:** `prev.preconditions.push(data)` causes React to not re-render
**Why it happens:** Direct mutation of state object
**How to avoid:** Always use spread operator: `[...(prev.preconditions || []), data]`
**Warning signs:** Console shows data but UI doesn't update

### Pitfall 3: Missing Optional Chaining
**What goes wrong:** `prev.preconditions.length` throws "Cannot read property of undefined"
**Why it happens:** preconditions may be undefined initially
**How to avoid:** Use `(prev.preconditions || [])` pattern
**Warning signs:** Runtime errors in browser console

### Pitfall 4: ReportDetailResponse Schema Mismatch
**What goes wrong:** Backend returns new fields but Pydantic validation fails
**Why it happens:** ReportDetailResponse doesn't include ui_assertion_results, api_pass_rate fields
**How to avoid:** Update backend/db/schemas.py ReportDetailResponse to include optional fields
**Warning signs:** 422 Validation Error from backend

## Code Examples

### Adding SSE Event Handler (Verified Pattern)

```typescript
// Source: frontend/src/hooks/useRunStream.ts lines 56-77
// Pattern to follow for new handlers

eventSource.addEventListener('step', (e: MessageEvent) => {
  const stepData = JSON.parse(e.data)
  setRun(prev => {
    if (!prev) return prev
    // Build screenshot URL
    const screenshotUrl = stepData.screenshot_url
      ? `${API_BASE}${stepData.screenshot_url}`
      : ''
    const newStep: Step = {
      index: stepData.index,
      action: stepData.action,
      reasoning: stepData.reasoning,
      screenshot: screenshotUrl,
      status: stepData.status,
      duration_ms: stepData.duration_ms || 0,
    }
    return {
      ...prev,
      steps: [...prev.steps, newStep],  // Immutable append
    }
  })
})
```

### Backend Report Service Usage (Verified)

```python
# Source: backend/core/report_service.py lines 91-134

async def get_report_data(self, run_id: str) -> Optional[dict]:
    """Get full report data including steps and assertions."""
    report = await self.report_repo.get_by_run_id(run_id)
    if not report:
        return None

    steps = await self.run_repo.get_steps(run_id)
    assertion_results = await self.assertion_result_repo.list_by_run(run_id)

    # Separate UI assertions from API assertions
    ui_assertion_results = [
        ar for ar in assertion_results
        if not ar.assertion_id.startswith("api_")
    ]
    api_assertion_results = [
        ar for ar in assertion_results
        if ar.assertion_id.startswith("api_")
    ]

    pass_rate = self.calculate_pass_rate(assertion_results)
    api_pass_rate = self.calculate_pass_rate(api_assertion_results) if api_assertion_results else "N/A"

    return {
        "report": report,
        "steps": steps,
        "assertion_results": assertion_results,
        "ui_assertion_results": ui_assertion_results,
        "api_assertion_results": api_assertion_results,
        "pass_rate": pass_rate,
        "api_pass_rate": api_pass_rate,
    }
```

### Backend SSE Event Publishing (Verified)

```python
# Source: backend/api/routes/runs.py lines 91-112 (precondition)
# Source: backend/api/routes/runs.py lines 220-251 (api_assertion)

# Precondition event
pre_event = SSEPreconditionEvent(
    index=i,
    code=code_display,
    status="success" if result.success else "failed",
    error=result.error,
    duration_ms=result.duration_ms,
    variables=result.variables if result.success else None,
)
await event_manager.publish(run_id, f"event: precondition\ndata: {pre_event.model_dump_json()}\n\n")

# API assertion event
api_event = SSEApiAssertionEvent(
    index=i,
    code=code_display,
    status="success" if api_result.success else "failed",
    error=api_result.error,
    duration_ms=api_result.duration_ms,
    field_results=[...],
)
await event_manager.publish(run_id, f"event: api_assertion\ndata: {api_event.model_dump_json()}\n\n")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Mixed assertion_results | Separated ui_assertion_results + api_assertion_results | Phase 6 | Cleaner report display |
| Direct repository queries in routes | Service layer pattern | Phase 3 | Better separation of concerns |
| No precondition/api_assertion events | Full SSE event coverage | Phase 5, 6 | Real-time monitoring capability |

**Deprecated/outdated:**
- Direct repository queries in report routes: Use ReportService.get_report_data() instead

## Open Questions

1. **Should RunMonitor display precondition/api_assertion progress in real-time?**
   - What we know: CONTEXT.md marks this as Claude's discretion
   - What's unclear: Whether to add new UI components or integrate into existing StepTimeline
   - Recommendation: For Phase 8, focus on data flow fixes. UI enhancement can be a follow-up.

2. **Should backend ReportDetailResponse schema be updated?**
   - What we know: Frontend types already have ui_assertion_results, api_pass_rate fields
   - What's unclear: Whether Pydantic schema needs explicit optional fields
   - Recommendation: Add optional fields to backend/db/schemas.py ReportDetailResponse to ensure proper serialization

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 8.0.0+ with pytest-asyncio 0.24.0+ |
| Config file | pyproject.toml (no pytest.ini) |
| Quick run command | `uv run pytest backend/tests/unit/test_report_service.py -v -x` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| API-01 | SSE precondition events handled | integration | `uv run pytest backend/tests/integration/test_precondition_flow.py -v -x` | Yes |
| API-01 | SSE api_assertion events handled | integration | `uv run pytest backend/tests/integration/test_api_assertion_integration.py -v -x` | Yes |
| API-01 | Report returns api_assertion_results | unit | `uv run pytest backend/tests/unit/test_report_service.py -v -x` | Yes |

### Sampling Rate

- **Per task commit:** `uv run pytest backend/tests/unit/ -v -x` (unit tests only)
- **Per wave merge:** `uv run pytest backend/tests/unit/ backend/tests/integration/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `frontend/src/__tests__/useRunStream.test.ts` - Frontend hook tests (project has no frontend test infrastructure)
- [ ] Frontend test framework config - Vitest or Jest not configured

**Note:** Frontend testing infrastructure not present. Backend tests cover the service layer. Consider manual E2E verification for frontend changes.

## Sources

### Primary (HIGH confidence)

- backend/db/schemas.py lines 122-140 - SSEPreconditionEvent, SSEApiAssertionEvent definitions (verified)
- backend/api/routes/runs.py lines 91-112, 220-251 - SSE event publishing code (verified)
- backend/core/report_service.py lines 91-134 - get_report_data() method (verified)
- frontend/src/types/index.ts lines 71-89, 160-168 - Frontend type definitions (verified)
- frontend/src/hooks/useRunStream.ts - Current SSE handling (verified)
- backend/api/routes/reports.py - Current report endpoint (verified)

### Secondary (MEDIUM confidence)

- .planning/v0.2-MILESTONE-AUDIT.md - Gap analysis identifying the issues
- frontend/src/api/reports.ts - API client transformation layer (verified)

### Tertiary (LOW confidence)

- None required - all critical information from primary sources

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Using existing project patterns, no new dependencies
- Architecture: HIGH - Backend already correct, only frontend consumption needed
- Pitfalls: HIGH - Based on verified code patterns and React best practices

**Research date:** 2026-03-17
**Valid until:** 30 days - stable patterns, no external API dependencies
