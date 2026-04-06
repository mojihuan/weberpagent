# Phase 58: 执行步骤展示 - Research

**Researched:** 2026-04-02
**Domain:** React frontend - SSE event stream unified timeline display
**Confidence:** HIGH

## Summary

Phase 58 要求在执行监控页面（RunMonitor）的 StepTimeline 组件中，将前置条件（precondition）和 API 断言（api_assertion）步骤与普通 UI 操作步骤按实际执行顺序交错排列展示。这完全是前端改动——后端 SSE 事件流已按正确顺序发送所有三类事件（precondition -> step -> api_assertion），前端只需将三个独立数组合并为统一时间线并渲染。

核心改动涉及三个文件：`types/index.ts`（新增 TimelineItem 联合类型）、`useRunStream.ts`（SSE 事件转换为统一时间线数组）、`StepTimeline.tsx`（渲染三种类型的 timeline item）。`RunMonitor.tsx` 页面组件也需要更新传递给子组件的 props。

**Primary recommendation:** 新建 `TimelineItem` 联合类型，在 `useRunStream` 中将 SSE 事件按接收顺序 append 到统一的 `timeline: TimelineItem[]` 数组，StepTimeline 改为渲染该数组。利用后端已按执行顺序发送事件的特性，前端无需排序逻辑。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 新建统一的 `TimelineItem` 联合类型（type: 'step' | 'precondition' | 'assertion' + 对应数据字段），不复用现有 Step 类型
- **D-02:** SSE 接收事件时实时将三种事件转换为 `TimelineItem` 并 append 到统一时间线数组
- **D-03:** StepTimeline 组件改为接收 `TimelineItem[]` 而非 `Step[]`
- **D-04:** 前置条件步骤显示代码摘要（前 N 个字符 + "..."），断言步骤显示断言名称/索引标识
- **D-05:** 三类步骤用不同图标 + 不同颜色区分：前置条件（黄色/橙色 + 文件图标）、断言（绿色/紫色 + 盾牌图标）、UI 操作（保持现有蓝色）
- **D-06:** Claude 决定具体图标选择和 Tailwind 色值
- **D-07:** 利用后端已有的按执行顺序发送事件的特性，前端 SSE 接收时直接 append 到统一时间线数组，不需要额外排序逻辑
- **D-08:** 不需要在渲染时合并排序——后端执行顺序就是展示顺序
- **D-09:** 点击前置条件步骤：展开显示完整代码 + 变量输出（variables）
- **D-10:** 点击断言步骤：展开显示断言代码 + 结果详情（field_results）
- **D-11:** 点击 UI 步骤保持现有行为（跳转截图面板）
- **D-12:** 前置条件/断言步骤不展示 AI 推理文本（reasoning）——它们是代码执行结果，无 AI 推理过程

### Claude's Discretion
- 具体图标选择（Lucide React 图标库）
- Tailwind 颜色值
- TimelineItem 类型的具体字段设计
- 代码摘要截取长度（N 个字符）
- 详情面板的展开/折叠动画

### Deferred Ideas (OUT OF SCOPE)
None
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| EXEC-01 | 执行监控的 StepTimeline 中展示前置条件执行步骤（包含状态、耗时、代码摘要） | TimelineItemPrecondition 类型设计、Lucide FileCode 图标 + 橙色配色方案、code 截断逻辑 |
| EXEC-02 | 执行监控的 StepTimeline 中展示断言执行步骤（包含状态、耗时、断言名称） | TimelineItemAssertion 类型设计、Lucide ShieldCheck 图标 + 紫色配色方案、field_results 展示 |
| EXEC-03 | 前置条件和断言步骤与普通 UI 步骤按执行顺序交错显示在时间线中 | 后端已按执行顺序发送事件（precondition -> step -> api_assertion），前端在 useRunStream 中 append 到统一 timeline 数组 |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| lucide-react | ^0.577.0 | Icon library | Already in project, provides FileCode/ShieldCheck etc. |
| React | ^19.2.0 | UI framework | Project standard |
| Tailwind CSS | ^4.2.1 | Styling | Project standard, all components use Tailwind |
| Vite | ^7.3.1 | Build tool | Project standard |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| EventSource (native) | - | SSE connection | Already used in useRunStream.ts |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| N/A | N/A | No alternatives needed - pure frontend change using existing stack |

**Installation:**
No new dependencies needed. All required libraries are already installed.

## Architecture Patterns

### Recommended Project Structure
```
frontend/src/
├── types/index.ts              # Add TimelineItem union type
├── hooks/useRunStream.ts       # Modify: append to unified timeline array
├── pages/RunMonitor.tsx        # Modify: pass timeline to StepTimeline
├── components/RunMonitor/
│   ├── StepTimeline.tsx        # Major rewrite: render TimelineItem[]
│   ├── index.ts                # No change
│   ├── ReasoningLog.tsx        # No change (only shows Step reasoning)
│   ├── ScreenshotPanel.tsx     # May need minor change (viewIndex logic)
│   └── RunHeader.tsx           # May need minor change (step count)
```

### Pattern 1: Discriminated Union Type for Timeline Items
**What:** Use a TypeScript discriminated union with `type` field to distinguish timeline item kinds.
**When to use:** When rendering heterogeneous items in a single list with type-specific behavior.
**Example:**
```typescript
// frontend/src/types/index.ts
export interface TimelineItemStep {
  type: 'step'
  data: Step
}

export interface TimelineItemPrecondition {
  type: 'precondition'
  data: SSEPreconditionEvent
}

export interface TimelineItemAssertion {
  type: 'assertion'
  data: SSEApiAssertionEvent
}

export type TimelineItem =
  | TimelineItemStep
  | TimelineItemPrecondition
  | TimelineItemAssertion
```

### Pattern 2: SSE Event to TimelineItem Conversion
**What:** In useRunStream, convert each SSE event to a TimelineItem and append to a single timeline array.
**When to use:** When multiple SSE event types need to be displayed in a unified chronological list.
**Example:**
```typescript
// Inside useRunStream.ts event handlers
const addTimelineItem = (item: TimelineItem) => {
  setRun(prev => {
    if (!prev) return prev
    return {
      ...prev,
      timeline: [...prev.timeline, item],
    }
  })
}

// step event handler
eventSource.addEventListener('step', (e: MessageEvent) => {
  const stepData = JSON.parse(e.data)
  const newStep: Step = { /* ... */ }
  addTimelineItem({ type: 'step', data: newStep })
})

// precondition event handler
eventSource.addEventListener('precondition', (e: MessageEvent) => {
  const data: SSEPreconditionEvent = JSON.parse(e.data)
  addTimelineItem({ type: 'precondition', data })
})

// api_assertion event handler
eventSource.addEventListener('api_assertion', (e: MessageEvent) => {
  const data: SSEApiAssertionEvent = JSON.parse(e.data)
  addTimelineItem({ type: 'assertion', data })
})
```

### Pattern 3: Type-Specific Rendering in StepTimeline
**What:** Use a switch on `item.type` to render different UI for each timeline item kind.
**When to use:** When rendering a discriminated union in a list.
**Example:**
```typescript
// Inside StepTimeline.tsx
const renderTimelineItem = (item: TimelineItem, index: number) => {
  switch (item.type) {
    case 'step':
      return renderStepItem(item.data, index)
    case 'precondition':
      return renderPreconditionItem(item.data, index)
    case 'assertion':
      return renderAssertionItem(item.data, index)
  }
}
```

### Anti-Patterns to Avoid
- **Mutating state arrays:** Always create new arrays with spread (`[...prev.timeline, newItem]`), never push to existing arrays (per CLAUDE.md immutability requirement)
- **Sorting timeline after receiving:** Backend sends events in execution order. Do not add client-side sorting.
- **Separate timeline sections:** Do not split precondition/step/assertion into separate visual groups. They must be interleaved.
- **Modifying backend SSE events:** Backend code is out of scope. All changes are frontend-only.
- **Adding reasoning display to precondition/assertion items:** Per D-12, these items have no AI reasoning.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Icon rendering | Custom SVG components | Lucide React (FileCode, ShieldCheck, etc.) | Consistent design, already installed |
| SSE connection | Custom WebSocket | EventSource (native browser API) | Already implemented in useRunStream |
| Status color mapping | Hardcoded color strings | Tailwind CSS classes | Already used throughout project |
| Timeline layout | Custom layout engine | Existing StepTimeline layout pattern | Just add new item renderers |

**Key insight:** This phase is mostly about data structure transformation (three arrays -> one timeline) and conditional rendering (switch on item.type). No complex algorithms or external dependencies needed.

## Common Pitfalls

### Pitfall 1: viewIndex Desync Between Timeline and ScreenshotPanel
**What goes wrong:** `viewIndex` currently maps to `run.steps[viewIndex]` for screenshot display. After unifying to `TimelineItem[]`, a timeline index may point to a precondition/assertion item that has no screenshot.
**Why it happens:** RunMonitor uses `viewIndex` for both StepTimeline highlighting and ScreenshotPanel navigation. Precondition/assertion items don't have screenshots.
**How to avoid:** Keep a separate mapping: `viewIndex` in the unified timeline, and derive the corresponding `stepIndex` (only for Step-type items) for ScreenshotPanel. When clicking a non-Step item, do not navigate ScreenshotPanel.
**Warning signs:** ScreenshotPanel crashes or shows wrong screenshot when clicking precondition/assertion items.

### Pitfall 2: Precondition Running State Shows Before started Event
**What goes wrong:** Backend sends `precondition` events with `status: "running"` before sending the `started` event. The `started` event handler initializes the Run object. If `setRun` is called before `started`, `prev` is null and the item is lost.
**Why it happens:** Backend code flow: precondition loop runs first, then sends `started`, then agent runs. See `runs.py` lines 84-146.
**How to avoid:** Either (a) initialize the Run object in the `precondition` handler if `prev` is null (same as `started` handler), or (b) check if the backend can be changed to send `started` first (but backend is out of scope). The `started` event IS sent after preconditions in current code, so the first precondition `running` event will hit null prev. However, looking at the code more carefully: the backend sends `precondition` events BEFORE `started`, so the frontend must handle this. The simplest approach: initialize run in `precondition` handler as well.
**Warning signs:** First precondition item missing from timeline.

### Pitfall 3: Duplicate Precondition Events
**What goes wrong:** Backend sends TWO events per precondition: one with `status: "running"` and one with `status: "success"/"failed"`. Both get appended to the timeline, causing two entries per precondition.
**Why it happens:** This is the current backend behavior - it sends a "running" event when starting execution, then a final event with the result.
**How to avoid:** In the `precondition` event handler, if the new event has the same `index` as an existing precondition in the timeline, UPDATE it (replace) rather than APPEND. Same logic applies to `api_assertion` events.
**Warning signs:** Two timeline entries for each precondition/assertion (one "running", one final result).

### Pitfall 4: RunHeader Step Count Confusion
**What goes wrong:** RunHeader displays "X / Y 步" where Y is totalSteps. After unifying timeline, the count should reflect all timeline items or just steps.
**Why it happens:** RunHeader.currentStep and RunHeader.totalSteps currently only count `run.steps`.
**How to avoid:** Decide what "step count" means in the header. Likely: total timeline items, and current progress through the timeline. Update RunHeader to receive timeline length instead of steps length.
**Warning signs:** Header shows "0 / 0 步" even when precondition items are visible in timeline.

### Pitfall 5: Auto-Scroll Behavior
**What goes wrong:** `useEffect` in RunMonitor auto-scrolls to latest step by watching `run.steps.length`. After switching to `run.timeline`, the auto-scroll should watch `run.timeline.length`.
**Why it happens:** The auto-scroll dependency needs to change.
**How to avoid:** Update the useEffect to watch `run?.timeline?.length` instead of `run?.steps.length`.
**Warning signs:** Timeline doesn't auto-scroll to latest item during execution.

## Code Examples

### TimelineItem Type Definition
```typescript
// Source: Types designed based on existing SSEPreconditionEvent/SSEApiAssertionEvent/Step types
// frontend/src/types/index.ts additions

export interface TimelineItemStep {
  type: 'step'
  data: Step
}

export interface TimelineItemPrecondition {
  type: 'precondition'
  data: SSEPreconditionEvent
}

export interface TimelineItemAssertion {
  type: 'assertion'
  data: SSEApiAssertionEvent
}

export type TimelineItem =
  | TimelineItemStep
  | TimelineItemPrecondition
  | TimelineItemAssertion
```

### Updated Run Type
```typescript
// Modify existing Run interface to add timeline field
export interface Run {
  id: string
  task_id: string
  status: RunStatus
  started_at: string
  finished_at?: string
  steps: Step[]           // Keep for backward compat (ScreenshotPanel, ReasoningLog)
  preconditions?: SSEPreconditionEvent[]  // Keep for backward compat
  api_assertions?: SSEApiAssertionEvent[] // Keep for backward compat
  timeline: TimelineItem[]  // NEW: unified timeline
}
```

### Icon and Color Selection (Claude's Discretion)

Based on Lucide React 0.577.0 icons available (verified from node_modules):

| Item Type | Icon | Status Running | Status Success | Status Failed |
|-----------|------|---------------|----------------|---------------|
| step (UI) | MousePointer (current: no specific icon, uses status icons) | Loader2 (blue) | CheckCircle (green) | XCircle (red) |
| precondition | FileCode | Loader2 (amber) | CheckCircle (amber) | XCircle (red) |
| assertion | ShieldCheck | Loader2 (purple) | CheckCircle (purple) | XCircle (red) |

**Tailwind color scheme:**

| Item Type | Accent Color | Badge Background |
|-----------|-------------|-----------------|
| step | blue-500 | blue-100 text-blue-700 |
| precondition | amber-500 | amber-100 text-amber-700 |
| assertion | purple-500 | purple-100 text-purple-700 |

### StepTimeline Item Rendering (Conceptual)
```typescript
// Precondition item rendering
const renderPreconditionItem = (data: SSEPreconditionEvent, index: number) => {
  const statusIcon = getPreconditionIcon(data.status)
  const label = `前置条件 ${data.index + 1}`
  const summary = data.code.length > 60 ? data.code.slice(0, 60) + '...' : data.code

  return (
    <div className="relative flex gap-3 pb-4">
      <div className="relative z-10 bg-white">{statusIcon}</div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <span className="text-sm font-medium text-amber-700">{label}</span>
          {data.duration_ms != null && data.duration_ms > 0 && (
            <span className="text-xs text-gray-500">{formatDuration(data.duration_ms)}</span>
          )}
        </div>
        <p className="text-sm text-gray-600 font-mono truncate">{summary}</p>
        {data.error && (
          <p className="text-xs text-red-500 mt-1 truncate">{data.error}</p>
        )}
      </div>
    </div>
  )
}

// Assertion item rendering
const renderAssertionItem = (data: SSEApiAssertionEvent, index: number) => {
  const statusIcon = getAssertionIcon(data.status)
  const label = `断言 ${data.index + 1}`
  const summary = data.code.length > 60 ? data.code.slice(0, 60) + '...' : data.code

  return (
    <div className="relative flex gap-3 pb-4">
      <div className="relative z-10 bg-white">{statusIcon}</div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <span className="text-sm font-medium text-purple-700">{label}</span>
          {data.duration_ms > 0 && (
            <span className="text-xs text-gray-500">{formatDuration(data.duration_ms)}</span>
          )}
        </div>
        <p className="text-sm text-gray-600 font-mono truncate">{summary}</p>
        {data.error && (
          <p className="text-xs text-red-500 mt-1 truncate">{data.error}</p>
        )}
      </div>
    </div>
  )
}
```

### Expanded Detail Panel (Click Handler)
```typescript
// Expanded precondition detail
const PreconditionDetail = ({ data }: { data: SSEPreconditionEvent }) => (
  <div className="mt-2 p-3 bg-gray-50 rounded-lg text-sm space-y-2">
    <div>
      <span className="font-medium text-gray-700">完整代码:</span>
      <pre className="mt-1 text-xs text-gray-600 whitespace-pre-wrap font-mono">
        {data.code}
      </pre>
    </div>
    {data.variables && Object.keys(data.variables).length > 0 && (
      <div>
        <span className="font-medium text-gray-700">变量输出:</span>
        <pre className="mt-1 text-xs text-gray-600 whitespace-pre-wrap font-mono">
          {JSON.stringify(data.variables, null, 2)}
        </pre>
      </div>
    )}
  </div>
)

// Expanded assertion detail
const AssertionDetail = ({ data }: { data: SSEApiAssertionEvent }) => (
  <div className="mt-2 p-3 bg-gray-50 rounded-lg text-sm space-y-2">
    <div>
      <span className="font-medium text-gray-700">断言代码:</span>
      <pre className="mt-1 text-xs text-gray-600 whitespace-pre-wrap font-mono">
        {data.code}
      </pre>
    </div>
    {data.field_results && data.field_results.length > 0 && (
      <div>
        <span className="font-medium text-gray-700">字段结果:</span>
        <div className="mt-1 space-y-1">
          {data.field_results.map((fr, i) => (
            <div key={i} className={`text-xs font-mono ${fr.passed ? 'text-green-600' : 'text-red-600'}`}>
              {fr.passed ? '[PASS]' : '[FAIL]'} {fr.field_name}: {fr.message}
            </div>
          ))}
        </div>
      </div>
    )}
  </div>
)
```

### Update/Replace Logic for Running -> Final Events
```typescript
// In useRunStream.ts - handle precondition event (same pattern for api_assertion)
eventSource.addEventListener('precondition', (e: MessageEvent) => {
  const data: SSEPreconditionEvent = JSON.parse(e.data)
  setRun(prev => {
    if (!prev) {
      // Initialize run if not yet started (precondition events arrive before 'started')
      return {
        id: runId,
        task_id: '',
        status: 'running',
        started_at: new Date().toISOString(),
        steps: [],
        preconditions: [data],
        api_assertions: [],
        timeline: [{ type: 'precondition', data }],
      }
    }
    // Check if this is an update to an existing precondition (same index)
    const existingIndex = prev.timeline.findIndex(
      item => item.type === 'precondition' && item.data.index === data.index
    )

    if (existingIndex >= 0) {
      // Replace existing item (running -> success/failed)
      const newTimeline = [...prev.timeline]
      newTimeline[existingIndex] = { type: 'precondition', data }
      return {
        ...prev,
        preconditions: [...(prev.preconditions || []), data],
        timeline: newTimeline,
      }
    }

    // New item
    return {
      ...prev,
      preconditions: [...(prev.preconditions || []), data],
      timeline: [...prev.timeline, { type: 'precondition', data }],
    }
  })
})
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Separate arrays for steps/preconditions/assertions | Unified TimelineItem[] array | This phase | Enables interleaved display |
| StepTimeline renders Step[] only | StepTimeline renders TimelineItem[] | This phase | Three item types in one timeline |

**Deprecated/outdated:**
- Passing `run.steps` directly to StepTimeline: replaced by `run.timeline`

## Open Questions

1. **ScreenshotPanel and ReasoningLog backward compatibility**
   - What we know: ScreenshotPanel takes `steps: Step[]` and `currentViewIndex: number`. ReasoningLog takes `steps: Step[]`.
   - What's unclear: Whether to keep `run.steps` populated alongside `run.timeline` for backward compatibility, or refactor ScreenshotPanel/ReasoningLog to derive their data from timeline.
   - Recommendation: Keep `run.steps` populated for backward compatibility. ScreenshotPanel and ReasoningLog continue using `run.steps`. Only StepTimeline switches to `run.timeline`. This minimizes blast radius.

2. **viewIndex mapping for ScreenshotPanel**
   - What we know: viewIndex currently maps 1:1 to `run.steps` array index for screenshot navigation.
   - What's unclear: How to derive the correct step index when clicking a timeline item that may be a precondition or assertion.
   - Recommendation: When clicking a Step-type timeline item, compute its position within only the Step-type items in the timeline to get the correct `steps[]` index. When clicking non-Step items, expand detail inline but do NOT update ScreenshotPanel's viewIndex.

## Environment Availability

Step 2.6: SKIPPED (no external dependencies identified - pure frontend TypeScript/React changes using existing installed packages)

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None detected |
| Config file | None |
| Quick run command | N/A |
| Full suite command | N/A |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| EXEC-01 | Precondition steps render in StepTimeline with status, duration, code summary | Manual visual verification | N/A | No test infrastructure |
| EXEC-02 | Assertion steps render in StepTimeline with status, duration, assertion name | Manual visual verification | N/A | No test infrastructure |
| EXEC-03 | All three item types interleaved by execution order | Manual visual verification | N/A | No test infrastructure |

### Sampling Rate
- **Per task commit:** Visual verification in browser
- **Per wave merge:** Visual verification in browser
- **Phase gate:** All three success criteria visually confirmed

### Wave 0 Gaps
- No frontend test infrastructure exists (no vitest/jest config, no test files)
- Given the visual nature of this phase (UI rendering of timeline items), manual testing is appropriate
- Recommendation: No test framework setup for this phase; focus on manual verification

## Sources

### Primary (HIGH confidence)
- `frontend/src/types/index.ts` - Verified SSEPreconditionEvent, SSEApiAssertionEvent, Step type definitions (lines 87-148)
- `frontend/src/hooks/useRunStream.ts` - Verified SSE event handling pattern (lines 43-97)
- `frontend/src/components/RunMonitor/StepTimeline.tsx` - Verified current timeline rendering (lines 1-104)
- `frontend/src/pages/RunMonitor.tsx` - Verified page layout and component wiring (lines 1-125)
- `backend/api/routes/runs.py` - Verified SSE event send order: precondition -> started -> step -> api_assertion (lines 56-295)
- `node_modules/lucide-react/dist/esm/icons/` - Verified FileCode, ShieldCheck icon availability

### Secondary (MEDIUM confidence)
- `backend/db/schemas.py` - Verified Pydantic SSE event schemas match frontend types (lines 186-203)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - all libraries already installed and verified
- Architecture: HIGH - three files to modify, data flow is clear, patterns well established
- Pitfalls: HIGH - identified 5 specific pitfalls from reading actual source code

**Research date:** 2026-04-02
**Valid until:** 2026-05-02 (stable project, no fast-moving dependencies)
