---
phase: 58
slug: exec-display
status: draft
shadcn_initialized: false
preset: none
created: 2026-04-02
---

# Phase 58 — UI Design Contract

> Visual and interaction contract for displaying precondition and assertion steps interleaved with UI steps in the execution monitor's StepTimeline. Creates a unified TimelineItem union type and updates three frontend files.

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none (raw Tailwind CSS v4) |
| Preset | not applicable |
| Component library | none |
| Icon library | Lucide React (FileCode, ShieldCheck, plus existing status icons) |
| Font | system default (sans-serif) |

---

## Spacing Scale

Declared values (must be multiples of 4):

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px (`gap-1`) | Badge-to-content inline gap |
| sm | 8px (`gap-2`, `p-2`) | Detail panel internal gap, badge padding |
| md | 16px (`gap-4`, `p-4`) | Timeline item gap (`gap-3` + `pb-4`), container padding |
| lg | 24px | Not used in this phase |
| xl | 32px | Not used in this phase |
| 2xl | 48px | Not used in this phase |
| 3xl | 64px | Not used in this phase |

Exceptions: none

Note: Spacing values align with Phase 57 UI-SPEC and the existing StepTimeline layout pattern (`gap-3`, `pb-4`, `p-4`).

---

## Typography

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Item label | 14px (`text-sm`, `font-medium`) | 500 | default (1.5) |
| Item description | 14px (`text-sm`) | 400 | default (1.5) |
| Duration | 12px (`text-xs`) | 400 | default (1.33) |
| Error text | 12px (`text-xs`) | 400 | default (1.33) |
| Detail panel heading | 14px (`text-sm`, `font-medium`) | 500 | default (1.5) |
| Detail panel code | 12px (`text-xs`, `font-mono`) | 400 | default (1.33) |

Notes:
- Typography matches the existing StepTimeline pattern exactly: `text-sm font-medium` for labels, `text-xs text-gray-500` for duration, `text-sm text-gray-600` for descriptions.
- Detail panel code uses `text-xs font-mono` matching the existing badge/label pattern from Phase 57.

---

## Color

### Surface Colors (existing, unchanged)

| Role | Value | Usage |
|------|-------||
| Dominant (60%) | `bg-white` / `bg-gray-50` | Page background, timeline item background, detail panel background |
| Secondary (30%) | `bg-gray-200` / `border-gray-200` | Timeline connector lines, section borders |
| Destructive | `text-red-500` / `text-red-600` | Error text, failed status icons |

### Timeline Item Type Colors (new for this phase)

| Item Type | Label Color | Status Icon Color (success) | Status Icon Color (running) | Status Icon Color (failed) | Badge Background |
|-----------|------------|---------------------------|----------------------------|---------------------------|-----------------|
| step (UI) | `text-gray-900` | `text-green-500` (CheckCircle) | `text-blue-500 animate-spin` (Loader2) | `text-red-500` (XCircle) | none |
| precondition | `text-amber-700` | `text-amber-500` (CheckCircle) | `text-amber-500 animate-spin` (Loader2) | `text-red-500` (XCircle) | `bg-amber-50` (detail panel) |
| assertion | `text-purple-700` | `text-purple-500` (CheckCircle) | `text-purple-500 animate-spin` (Loader2) | `text-red-500` (XCircle) | `bg-purple-50` (detail panel) |

Accent reserved for: assertion type badge (`text-purple-700`) as the primary differentiator for assertion items. The purple accent is reserved specifically for assertion-related visual elements (label text, success icons, detail panel background).

Color source: CONTEXT.md D-05 (locked: amber for precondition, purple for assertion). Specific Tailwind values at Claude's discretion, mapped from the amber-500/700 and purple-500/700 palettes.

### Field Result Colors (assertion detail panel)

| Field Status | Color |
|-------------|-------|
| Passed | `text-green-600` |
| Failed | `text-red-600` |

---

## Component Inventory

### New Types (in existing file)

| File | Change |
|------|--------|
| `frontend/src/types/index.ts` | Add `TimelineItemStep`, `TimelineItemPrecondition`, `TimelineItemAssertion`, `TimelineItem` union type. Add `timeline` field to `Run` interface. |

### Modified Files

| File | Change | Scope |
|------|--------|-------|
| `frontend/src/hooks/useRunStream.ts` | Convert SSE events to unified timeline array; handle running->final event replacement; initialize Run on precondition events | Major |
| `frontend/src/components/RunMonitor/StepTimeline.tsx` | Accept `TimelineItem[]` instead of `Step[]`; render three item types with type-specific icons, colors, and click behaviors; add expandable detail panels | Major rewrite |
| `frontend/src/pages/RunMonitor.tsx` | Pass `run.timeline` to StepTimeline; update auto-scroll to watch `run.timeline.length`; handle viewIndex for ScreenshotPanel backward compatibility; update RunHeader step counts | Moderate |
| `frontend/src/components/RunMonitor/RunHeader.tsx` | Update `currentStep` and `totalSteps` to reflect timeline item count (or keep step-only count; see interaction spec) | Minor |

### Unchanged Files

| File | Reason |
|------|--------|
| `frontend/src/components/RunMonitor/ReasoningLog.tsx` | Continues to use `run.steps` — only Step-type items have reasoning |
| `frontend/src/components/RunMonitor/ScreenshotPanel.tsx` | Continues to use `run.steps` — only Step-type items have screenshots |
| All backend files | Backend SSE event stream is unchanged; pure frontend modification |

---

## Visual Specification

### TimelineItem Type Definition

```typescript
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

### Run Type Update

```typescript
// Add to existing Run interface:
export interface Run {
  // ... existing fields unchanged ...
  steps: Step[]                        // Keep for ScreenshotPanel + ReasoningLog backward compat
  preconditions?: SSEPreconditionEvent[]  // Keep for backward compat
  api_assertions?: SSEApiAssertionEvent[] // Keep for backward compat
  timeline: TimelineItem[]             // NEW: unified timeline for StepTimeline
}
```

### Timeline Layout (all three item types share this structure)

```
+-----+-----------------------------------------------+
| O   | [Type Label]                        [duration] |
| |   | [code summary / action text]                  |
| |   | [error message if any]                        |
+-----+-----------------------------------------------+
```

- Container: `relative flex gap-3 pb-4`
- Connector line: `absolute left-[10px] top-[22px] w-0.5 h-full bg-gray-200` (not on last item)
- Status icon: `relative z-10 bg-white` containing the type-specific status icon
- Content area: `flex-1 min-w-0`

### Precondition Item Rendering

```
+-----+-----------------------------------------------+
| O   | 前置条件 1                          1.2s      |
| |   | login(username="admin", password="...")       |
+-----+-----------------------------------------------+
```

- Label: `text-sm font-medium text-amber-700` — "前置条件 {index + 1}"
- Type icon: `FileCode` from Lucide (w-5 h-5, amber color, displayed alongside status icon or as secondary indicator)
- Code summary: `text-sm text-gray-600 font-mono truncate` — first 60 characters of `data.code` + "..." if longer
- Duration: `text-xs text-gray-500` — only shown when `data.duration_ms > 0`
- Error: `text-xs text-red-500 mt-1 truncate` — shown when `data.error` exists
- Status icon colors: success=amber CheckCircle, running=amber Loader2-spin, failed=red XCircle, pending=gray Circle

### Assertion Item Rendering

```
+-----+-----------------------------------------------+
| O   | 断言 1                              0.8s      |
| |   | assert_response_code(response, 200)...         |
+-----+-----------------------------------------------+
```

- Label: `text-sm font-medium text-purple-700` — "断言 {index + 1}"
- Type icon: `ShieldCheck` from Lucide (w-5 h-5, purple color)
- Code summary: `text-sm text-gray-600 font-mono truncate` — first 60 characters of `data.code` + "..." if longer
- Duration: `text-xs text-gray-500` — only shown when `data.duration_ms > 0`
- Error: `text-xs text-red-500 mt-1 truncate` — shown when `data.error` exists
- Status icon colors: success=purple CheckCircle, running=purple Loader2-spin, failed=red XCircle, pending=gray Circle

### UI Step Item Rendering (existing, unchanged visually)

- Label: `text-sm font-medium text-gray-900` — "步骤 {step.index}"
- Action text: `text-sm text-gray-600 truncate`
- Status icons: existing pattern (blue Loader2, green CheckCircle, red XCircle, gray Circle)

### Click Behavior

| Item Type | Click Action | Detail Shown |
|-----------|-------------|-------------|
| step (UI) | Set viewIndex for ScreenshotPanel | No inline expansion — existing screenshot navigation behavior |
| precondition | Toggle inline expansion | Full code + variables output |
| assertion | Toggle inline expansion | Full code + field_results |

### Expanded Precondition Detail Panel

```
+-----------------------------------------------------+
| 完整代码:                                           |
| login(username="admin", password="secret123")       |
|                                                     |
| 变量输出:                                           |
| {                                                   |
|   "token": "abc123",                                |
|   "session_id": "xyz789"                            |
| }                                                   |
+-----------------------------------------------------+
```

- Container: `mt-2 p-3 bg-gray-50 rounded-lg text-sm space-y-2`
- Heading: `font-medium text-gray-700` — "完整代码:" / "变量输出:"
- Code block: `mt-1 text-xs text-gray-600 whitespace-pre-wrap font-mono`
- Variables: JSON.stringify with 2-space indent
- Animation: no animation (instant expand/collapse to keep implementation simple per "out of scope: 折叠" in REQUIREMENTS.md)

### Expanded Assertion Detail Panel

```
+-----------------------------------------------------+
| 断言代码:                                           |
| assert_response_code(response, 200)                 |
|                                                     |
| 字段结果:                                           |
| [PASS] status_code: Expected 200, got 200           |
| [FAIL] body.count: Expected > 0, got 0              |
+-----------------------------------------------------+
```

- Container: `mt-2 p-3 bg-gray-50 rounded-lg text-sm space-y-2`
- Heading: `font-medium text-gray-700` — "断言代码:" / "字段结果:"
- Code block: `mt-1 text-xs text-gray-600 whitespace-pre-wrap font-mono`
- Field results: each on its own line
  - Passed: `text-xs font-mono text-green-600` — "[PASS] {field_name}: {message}"
  - Failed: `text-xs font-mono text-red-600` — "[FAIL] {field_name}: {message}"
- Animation: no animation (instant expand/collapse)

---

## Interaction Specification

### State Management: Running -> Final Event Replacement

Backend sends two events per precondition/assertion: one `status: "running"` and one `status: "success"/"failed"`. The implementation must REPLACE the existing timeline entry (matching by `type` + `data.index`) rather than APPEND a duplicate.

```typescript
// In useRunStream.ts precondition handler:
const existingIndex = prev.timeline.findIndex(
  item => item.type === 'precondition' && item.data.index === data.index
)
if (existingIndex >= 0) {
  // Replace: running -> success/failed
  const newTimeline = [...prev.timeline]
  newTimeline[existingIndex] = { type: 'precondition', data }
  return { ...prev, timeline: newTimeline }
}
// New item: append
return { ...prev, timeline: [...prev.timeline, { type: 'precondition', data }] }
```

Same pattern applies to `api_assertion` events.

### Early Precondition Event Handling

Backend sends precondition events BEFORE the `started` event. The `started` handler initializes the Run object. If a precondition event arrives when `prev` is null, initialize the Run inline (same structure as `started` handler).

### viewIndex Mapping for ScreenshotPanel

`viewIndex` must remain a `steps[]` array index for ScreenshotPanel backward compatibility. When a Step-type timeline item is clicked, compute its position among only Step-type items:

```typescript
const handleTimelineItemClick = (item: TimelineItem, timelineIndex: number) => {
  if (item.type === 'step') {
    // Count how many Step-type items come before this one
    const stepIndex = run.timeline
      .slice(0, timelineIndex + 1)
      .filter(i => i.type === 'step').length - 1
    setViewIndex(stepIndex)
  }
  // For precondition/assertion: toggle expanded state, do NOT update viewIndex
}
```

### Auto-Scroll

Update the auto-scroll `useEffect` to watch `run?.timeline?.length` instead of `run?.steps.length`:

```typescript
useEffect(() => {
  if (run?.timeline?.length) {
    // Auto-scroll to latest timeline item
    // (specific scroll implementation depends on StepTimeline's ref)
  }
}, [run?.timeline?.length])
```

### RunHeader Step Count

RunHeader currently shows `{currentStep} / {totalSteps} 步`. With the unified timeline, this should reflect all timeline items:

- `currentStep`: number of completed (non-running, non-pending) timeline items
- `totalSteps`: total timeline items count

This provides a more accurate progress indication. Alternatively, if the team prefers step-only counting, keep counting only Step-type items. The RESEARCH.md recommends counting all timeline items.

---

## Copywriting Contract

| Element | Copy |
|---------|------|
| Primary CTA | Not applicable — this phase has no new buttons or CTAs |
| Empty state heading | "等待执行开始..." (existing, unchanged from StepTimeline empty state) |
| Empty state body | Not applicable — single-line text only |
| Error state | `{data.error}` displayed as `text-xs text-red-500 mt-1 truncate` — error message comes directly from backend event data |
| Destructive confirmation | Not applicable — no destructive actions in this phase |
| Precondition label | "前置条件 {index + 1}" |
| Assertion label | "断言 {index + 1}" |
| Step label | "步骤 {step.index}" (existing, unchanged) |
| Detail: code heading (precondition) | "完整代码:" |
| Detail: variables heading (precondition) | "变量输出:" |
| Detail: code heading (assertion) | "断言代码:" |
| Detail: field results heading (assertion) | "字段结果:" |
| Field result pass | "[PASS] {field_name}: {message}" |
| Field result fail | "[FAIL] {field_name}: {message}" |

All copy in Chinese to match existing UI convention (步骤, 暂无推理记录, 等待执行开始).

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | not applicable | shadcn not initialized; no third-party registries; all dependencies (lucide-react, tailwind) already installed |

---

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS
- [ ] Dimension 2 Visuals: PASS
- [ ] Dimension 3 Color: PASS
- [ ] Dimension 4 Typography: PASS
- [ ] Dimension 5 Spacing: PASS
- [ ] Dimension 6 Registry Safety: PASS

**Approval:** pending
