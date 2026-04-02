---
phase: 59
slug: report-steps
status: draft
shadcn_initialized: false
preset: none
created: 2026-04-02
---

# Phase 59 — UI Design Contract

> Visual and interaction contract for displaying precondition and assertion steps interleaved with UI steps in the report detail page. Extends the existing StepItem card component into a unified timeline, removes three independent display sections, and adds backend data persistence for precondition results.

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none (raw Tailwind CSS v4) |
| Preset | not applicable |
| Component library | none |
| Icon library | Lucide React (FileCode, ShieldCheck, CheckCircle, XCircle, Clock, ChevronDown, ChevronRight) |
| Font | system default (sans-serif) |

Note: No shadcn detected. `components.json` not present. All styling via Tailwind utility classes, consistent with existing project pattern.

---

## Spacing Scale

Declared values (must be multiples of 4):

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px (`gap-1`) | Icon-to-label gap within type badges |
| sm | 8px (`gap-2`, `p-2`) | Compact element internal gap, badge padding |
| md | 16px (`gap-4`, `p-4`) | Card horizontal padding (`px-4`), expanded content padding |
| lg | 24px | Not used in this phase |
| xl | 32px | Not used in this phase |
| 2xl | 48px | Not used in this phase |
| 3xl | 64px | Not used in this phase |

Exceptions: none

Note: Spacing aligns with the existing StepItem card layout (`px-4 py-3`, `p-4` in expanded area, `gap-3` between items in `space-y-3`). Matches Phase 58 UI-SPEC spacing tokens.

---

## Typography

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Card header label | 14px (`text-sm`, `font-medium`) | 500 | default (1.5) |
| Card description / action text | 14px (`text-sm`) | 400 | default (1.5) |
| Duration text | 14px (`text-sm`) | 400 | default (1.5) |
| Section heading ("执行步骤") | 18px (`text-lg`, `font-medium`) | 500 | default (1.4) |
| Error text | 14px (`text-sm`) | 400 | default (1.5) |
| Expanded content heading | 14px (`text-sm`, `font-medium`) | 500 | default (1.5) |
| Code block / variables | 12px (`text-xs`, `font-mono`) | 400 | default (1.33) |
| Variable key | 14px (`text-sm`, `font-mono`, `text-blue-600`) | 400 | default (1.5) |
| Variable value | 14px (`text-sm`, `font-mono`, `text-green-600`) | 400 | default (1.5) |

Notes:
- Typography matches the existing StepItem.tsx pattern exactly: `font-medium text-gray-900` for header labels, `text-gray-700` for action text, `text-sm text-gray-500` with Clock icon for duration.
- Code blocks use `text-xs font-mono` matching Phase 58 StepTimeline detail panels.
- Section heading uses `text-lg font-medium text-gray-900 mb-3` matching the existing "执行步骤" heading in ReportDetail.tsx line 95.

---

## Color

### Surface Colors (existing, unchanged)

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | `bg-white` / `bg-gray-50` | Page background, card background, expanded content background |
| Secondary (30%) | `border-gray-200` / `bg-gray-200` | Card borders, section dividers |
| Destructive | `bg-red-50` / `border-red-200` / `text-red-500` / `text-red-600` | Failed status cards, error messages |

### Timeline Card Type Colors (matching Phase 58 StepTimeline)

| Item Type | Type Icon | Label Color | Card border (success) | Card border (failed) | Expanded panel bg |
|-----------|-----------|------------|-----------------------|----------------------|-------------------|
| step (UI) | CheckCircle/XCircle | `text-gray-900` | `border-gray-200` | `border-gray-200` | `bg-gray-50` |
| precondition | FileCode (`text-amber-500`) | `text-amber-700` | `border-gray-200` with `text-amber-500` status icon | `border-gray-200` with `text-red-500` status icon | `bg-amber-50` |
| assertion | ShieldCheck (`text-purple-500`) | `text-purple-700` | `border-gray-200` with `text-purple-500` status icon | `border-gray-200` with `text-red-500` status icon | `bg-purple-50` |

Accent reserved for: assertion type badge (`text-purple-700`, `ShieldCheck icon`) and assertion expanded panel background (`bg-purple-50`). Purple is reserved specifically for assertion-related visual differentiation. Amber is reserved for precondition-related visual differentiation.

Color source: CONTEXT.md D-08 (locked: amber for precondition, purple for assertion, matching Phase 58).

### Status Icon Colors

| Status | Step | Precondition | Assertion |
|--------|------|-------------|-----------|
| success | `text-green-500` (CheckCircle) | `text-amber-500` (CheckCircle) | `text-purple-500` (CheckCircle) |
| failed | `text-red-500` (XCircle) | `text-red-500` (XCircle) | `text-red-500` (XCircle) |

### Field Result Colors (assertion expanded panel)

| Field Status | Color |
|-------------|-------|
| Passed | `text-green-600` |
| Failed | `text-red-600` |

---

## Component Inventory

### New Types (in existing file)

| File | Change |
|------|--------|
| `frontend/src/types/index.ts` | Add `ReportTimelineStep`, `ReportTimelinePrecondition`, `ReportTimelineAssertion`, `ReportTimelineItem` union type. Update `ReportDetailResponse` to include `timeline_items: ReportTimelineItem[]`. |

### New Components

| File | Purpose |
|------|---------|
| `frontend/src/components/Report/TimelineItemCard.tsx` | Generic card component that renders a ReportTimelineItem with type-specific header (icon, label, status, duration) and type-specific expanded content |

### Modified Files

| File | Change | Scope |
|------|--------|-------|
| `frontend/src/components/Report/StepItem.tsx` | Extract shared card shell pattern; may remain for backward compat or be replaced by TimelineItemCard | Major |
| `frontend/src/pages/ReportDetail.tsx` | Replace three independent sections + step list with unified timeline_items rendering using TimelineItemCard | Major |
| `frontend/src/api/reports.ts` | Update ReportDetailResponse type to include `timeline_items`; handle new response shape | Moderate |

### Removed Files

| File | Reason |
|------|--------|
| `frontend/src/components/Report/PreconditionSection.tsx` | D-10: Replaced by unified timeline rendering |
| `frontend/src/components/Report/AssertionResults.tsx` | D-10: Replaced by unified timeline rendering |
| `frontend/src/components/Report/ApiAssertionResults.tsx` | D-10: Replaced by unified timeline rendering |

### Backend Files (for data model, not visual)

| File | Change |
|------|--------|
| `backend/db/models.py` | Add `PreconditionResult` model; add `sequence_number` to Step and AssertionResult |
| `backend/db/schemas.py` | Add `ReportTimelineItem` discriminated union schemas |
| `backend/db/repository.py` | Add `PreconditionResultRepository` |
| `backend/core/report_service.py` | Merge-sort logic for unified timeline |
| `backend/api/routes/runs.py` | Global sequence_number allocation + precondition persistence |
| `backend/api/routes/reports.py` | Return `timeline_items` in API response |

---

## Visual Specification

### ReportTimelineItem Type Definition

```typescript
// frontend/src/types/index.ts additions

export interface ReportTimelineStep {
  type: 'step'
  id: string
  sequence_number: number
  action: string
  reasoning: string | null
  screenshot_url: string | null
  status: string
  error: string | null
  duration_ms: number | null
}

export interface ReportTimelinePrecondition {
  type: 'precondition'
  id: string
  sequence_number: number
  index: number
  code: string
  status: string
  error: string | null
  duration_ms: number | null
  variables: Record<string, unknown> | null
}

export interface ReportTimelineAssertion {
  type: 'assertion'
  id: string
  sequence_number: number
  assertion_id: string
  assertion_name: string | null
  status: string
  message: string | null
  actual_value: string | null
  field_results: Array<{
    field_name: string
    expected: unknown
    actual: unknown
    passed: boolean
    message: string
    assertion_type: string
  }> | null
  duration_ms: number | null
}

export type ReportTimelineItem =
  | ReportTimelineStep
  | ReportTimelinePrecondition
  | ReportTimelineAssertion
```

### ReportDetailResponse Update

```typescript
// Updated ReportDetailResponse
export interface ReportDetailResponse extends Report {
  timeline_items: ReportTimelineItem[]
  // Kept for backward compat during transition:
  steps: Step[]
  assertion_results?: AssertionResult[]
  ui_assertion_results?: AssertionResult[]
  api_assertion_results?: AssertionResult[]
  pass_rate?: string
  api_pass_rate?: string
  precondition_results?: any[]  // legacy, always null for old reports
}
```

### Unified Timeline Card Layout (all three item types)

The unified timeline replaces the three independent sections + step list with a single `space-y-3` container. Each card uses a collapsible button pattern identical to the existing StepItem.

```
+-------------------------------------------------------------------+
| [v] [StatusIcon] [TypeIcon] [Type Label] - [Action/Code]   [ms]  |
+-------------------------------------------------------------------+
| Expanded content area (type-specific)                             |
+-------------------------------------------------------------------+
```

- Card container: `border border-gray-200 rounded-lg overflow-hidden`
- Header button: `w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition`
- Chevron: `ChevronDown`/`ChevronRight` (`w-5 h-5 text-gray-400`)
- Status icon: type-specific CheckCircle/XCircle (`w-5 h-5`)
- Type icon (precondition/assertion only): FileCode/ShieldCheck (`w-4 h-4`) displayed before the label
- Label area: `flex-1 text-left`
- Duration: `flex items-center gap-1 text-sm text-gray-500` with `Clock` icon (`w-4 h-4`)
- Expanded content: `border-t border-gray-200 p-4` with type-specific background

### UI Step Card (existing StepItem pattern, extended)

Header:
- Chevron + CheckCircle/XCircle + "步骤 {step.index}" + " - " + step.action + Clock + duration

Expanded content (existing, unchanged):
- Error block (if any): `mb-4 p-3 bg-red-50 border border-red-200 rounded-lg`
- Step stats badges (if any): inline flex wrap badges
- Screenshot + Reasoning grid: `grid grid-cols-2 gap-4`
  - Left: screenshot image with hover overlay
  - Right: `ReasoningText` component in scrollable container
- ImageViewer modal

Background: `bg-gray-50`

### Precondition Card

Header:
- Chevron + CheckCircle(amber)/XCircle(red) + FileCode(amber) + "前置条件 {index + 1}" + truncated code + Clock + duration

```
+-------------------------------------------------------------------+
| [v] [O amber/red] [FileCode amber] 前置条件 1 - login(...)  1.2s |
+-------------------------------------------------------------------+
| Expanded area (bg-amber-50)                                       |
+-------------------------------------------------------------------+
```

- Label: `font-medium text-amber-700` -- "前置条件 {index + 1}"
- Separator: `text-gray-400 mx-2` -- "-"
- Code summary: `text-gray-700 font-mono truncate` -- first 80 chars of code
- Type icon: `FileCode` `w-4 h-4 text-amber-500`

Expanded content (`bg-amber-50`):

```
+-------------------------------------------------------------------+
| 错误信息 (if failed)                                              |
|   Error message in red box                                        |
|                                                                   |
| 完整代码:                                                         |
| login(username="admin", password="secret123")                     |
|                                                                   |
| 变量输出:                                                         |
|   token = abc123                                                  |
|   session_id = xyz789                                             |
+-------------------------------------------------------------------+
```

- Container: `bg-amber-50` (matches Phase 58 `bg-amber-50` for precondition detail panel)
- Error: `mb-4 p-3 bg-red-50 border border-red-200 rounded-lg` (same pattern as StepItem error block)
- Code heading: `text-sm font-medium text-gray-700 mb-2` -- "完整代码:"
- Code block: `p-2 bg-gray-100 rounded text-xs font-mono whitespace-pre-wrap overflow-auto`
- Variables heading: `text-sm font-medium text-gray-700 mb-2` -- "变量输出:"
- Variables container: `bg-gray-50 rounded p-2 font-mono text-sm`
- Each variable: `flex gap-2` with `text-blue-600` key + `text-gray-400` "=" + `text-green-600` value
- Object values: `JSON.stringify(value)` for nested objects

### Assertion Card

Header:
- Chevron + CheckCircle(purple)/XCircle(red) + ShieldCheck(purple) + "断言 {assertion_name or index + 1}" + status summary + Clock + duration

```
+-------------------------------------------------------------------+
| [v] [O purple/red] [ShieldCheck purple] 断言 1 - Login验证  0.8s |
+-------------------------------------------------------------------+
```

- Label: `font-medium text-purple-700` -- "断言 {assertion_name || index + 1}"
- Separator: `text-gray-400 mx-2` -- "-"
- Summary: `text-gray-700` -- status text or assertion name
- Type icon: `ShieldCheck` `w-4 h-4 text-purple-500`

Expanded content (`bg-purple-50`):

```
+-------------------------------------------------------------------+
| 错误信息 (if failed)                                              |
|   Error message in red box                                        |
|                                                                   |
| 字段结果:                                                         |
|   [PASS] status_code: Expected 200, got 200                      |
|   [FAIL] body.count: Expected > 0, got 0                         |
+-------------------------------------------------------------------+
```

- Container: `bg-purple-50` (matches Phase 58 `bg-purple-50` for assertion detail panel)
- Error: `mb-4 p-3 bg-red-50 border border-red-200 rounded-lg` (same pattern as StepItem error block)
- Field results heading: `text-sm font-medium text-gray-700 mb-2` -- "字段结果:"
- Each field result: `text-xs font-mono`
  - Passed: `text-green-600` -- "[PASS] {field_name}: {message}"
  - Failed: `text-red-600` -- "[FAIL] {field_name}: {message}"
- No field results: show message text and actual_value if available

### ReportDetail Page Layout (modified)

```
+-------------------------------------------------------------------+
| ReportHeader (existing, unchanged)                                |
+-------------------------------------------------------------------+
| SummaryCard grid (4 cols, existing, unchanged per D-11)           |
+-------------------------------------------------------------------+
| Section heading: "执行步骤" (text-lg font-medium)                 |
+-------------------------------------------------------------------+
| TimelineItemCard (precondition)                                   |
| TimelineItemCard (step)                                           |
| TimelineItemCard (step)                                           |
| TimelineItemCard (assertion)                                      |
| TimelineItemCard (step)                                           |
| ...                                                               |
+-------------------------------------------------------------------+
```

- The three independent sections (PreconditionSection, AssertionResults, ApiAssertionResults) are REMOVED
- All items render in a single `space-y-3` container
- Items appear in `sequence_number` order (backend-sorted)
- Section heading remains "执行步骤" at `text-lg font-medium text-gray-900 mb-3`

---

## Interaction Specification

### Card Expand/Collapse

| Property | Value |
|----------|-------|
| Default state | First item expanded + any failed items expanded |
| Toggle trigger | Click anywhere on card header button |
| Animation | None (instant expand/collapse, matching Phase 58 pattern) |
| Expanded icon | `ChevronDown` (`w-5 h-5 text-gray-400`) |
| Collapsed icon | `ChevronRight` (`w-5 h-5 text-gray-400`) |

Default expansion logic (Claude's discretion, matching existing StepItem default behavior from ReportDetail.tsx line 100):

```typescript
defaultExpanded={index === 0 || item.status === 'failed'}
```

### Data Loading

| State | Visual |
|-------|--------|
| Loading | Centered spinner: `w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin` in `flex items-center justify-center h-64` |
| Error | `<Navigate to="/reports" replace />` (existing behavior, redirect to reports list) |
| Empty timeline | No special empty state needed -- old reports with no timeline_items fall back to steps array rendering |
| Success | Full timeline rendering |

### Backward Compatibility for Old Reports

Reports generated before Phase 59 will have no `timeline_items` or an empty array. The frontend must handle this gracefully:

```typescript
// In ReportDetail.tsx:
const displayItems = data.timeline_items?.length > 0
  ? data.timeline_items
  : data.steps.map(step => ({ type: 'step' as const, ...stepToReportTimelineStep(step) }))
```

Old reports render only UI steps using the existing StepItem pattern. No precondition or assertion cards appear for old data.

### Screenshot Interaction (UI step cards only)

- Screenshot click opens `ImageViewer` modal (existing behavior)
- Precondition and assertion cards do not have screenshots

---

## Copywriting Contract

| Element | Copy |
|---------|------|
| Primary CTA | Not applicable -- this phase has no new buttons or CTAs |
| Empty state heading | Not applicable -- old reports fall back to step list |
| Empty state body | Not applicable |
| Error state | Error message from backend displayed in `text-sm text-red-600` card inline |
| Destructive confirmation | Not applicable -- no destructive actions |
| Section heading | "执行步骤" (existing, unchanged) |
| Step label | "步骤 {index}" (existing, unchanged) |
| Precondition label | "前置条件 {index + 1}" (matching Phase 58) |
| Assertion label | "断言 {assertion_name || index + 1}" |
| Detail: error heading | "错误信息" (matching StepItem.tsx existing pattern) |
| Detail: code heading (precondition) | "完整代码:" (matching Phase 58) |
| Detail: variables heading (precondition) | "变量输出:" (matching Phase 58) |
| Detail: field results heading (assertion) | "字段结果:" (matching Phase 58) |
| Field result pass | "[PASS] {field_name}: {message}" |
| Field result fail | "[FAIL] {field_name}: {message}" |
| No reasoning text | "暂无推理记录" (existing from StepItem.tsx, italic) |
| Screenshot hover | "点击查看大图" (existing from StepItem.tsx) |

All copy in Chinese to match existing UI convention.

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | not applicable | shadcn not initialized; no third-party registries; all dependencies (lucide-react, tailwind, react) already installed |

---

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS
- [ ] Dimension 2 Visuals: PASS
- [ ] Dimension 3 Color: PASS
- [ ] Dimension 4 Typography: PASS
- [ ] Dimension 5 Spacing: PASS
- [ ] Dimension 6 Registry Safety: PASS

**Approval:** pending
