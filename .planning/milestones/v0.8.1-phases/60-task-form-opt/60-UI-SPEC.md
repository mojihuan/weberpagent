---
phase: 60
slug: task-form-opt
status: draft
shadcn_initialized: false
preset: none
created: 2026-04-02
---

# Phase 60 — UI Design Contract

> Visual and interaction contract for removing API assertions tab and simplifying the TaskForm to show only business assertions. Predominantly a code removal phase with one structural UI simplification.

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none (raw Tailwind CSS v4) |
| Preset | not applicable |
| Component library | none |
| Icon library | Lucide React (existing, unchanged) |
| Font | system default (sans-serif) |

---

## Spacing Scale

Declared values (must be multiples of 4):

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px (`gap-1`) | Icon-to-text gaps in assertion cards |
| sm | 8px (`gap-2`, `p-2`) | Assertion card internal spacing |
| md | 16px (`gap-4`, `p-4`) | Form section spacing (`space-y-5` = 20px close enough to 16px, existing) |
| lg | 24px | Not changed in this phase |
| xl | 32px | Not changed in this phase |
| 2xl | 48px | Not changed in this phase |
| 3xl | 64px | Not changed in this phase |

Exceptions: none. All spacing values inherited from existing TaskForm patterns (`space-y-5`, `mb-1`, `mb-2`, `gap-2`, `gap-3`, `p-3`).

---

## Typography

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Section label | 14px (`text-sm`, `font-medium`) | 500 | default (1.5) |
| Helper text | 12px (`text-xs`) | 400 | default (1.33) |
| Assertion method name | 14px (`text-sm`, `font-mono`) | 400 | default (1.5) |
| Assertion params | 14px (`text-sm`) | 400 | default (1.5) |
| Empty state text | 14px (`text-sm`) | 400 | default (1.5) |
| Delete button | 14px (`text-sm`) | 400 | default (1.5) |
| CTA button (add) | 14px (`text-sm`) | 400 | default (1.5) |

Notes:
- Typography values match the existing TaskForm business assertions section exactly (lines 521-585 of TaskForm.tsx).
- No new typographic roles introduced. The "tab switcher" typography (14px `text-sm font-medium`) is removed, not replaced.

---

## Color

### Surface Colors (existing, unchanged)

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | `bg-white` / `bg-gray-50` | Page background, form background |
| Secondary (30%) | `border-gray-200` / `text-gray-500` | Form borders, helper text, section dividers |
| Destructive | `text-red-500` / `hover:bg-red-50` | Delete buttons for assertion cards |

### Business Assertion Card Colors (existing, unchanged)

| Element | Color | Tailwind Class |
|---------|-------|----------------|
| Card border | Light orange | `border-orange-200` |
| Card background | Pale orange | `bg-orange-50` |
| Method name | Blue | `text-blue-600 font-mono` |
| Add button border | Light orange | `border-orange-200` |
| Add button text | Orange | `text-orange-600` |
| Add button hover | Pale orange | `hover:bg-orange-50` |

Accent reserved for: orange (`orange-200/50/600`) reserved exclusively for business assertion cards and the "添加断言" button. This is the existing accent from Phase 24 business assertion implementation, carried forward unchanged.

### Colors Being REMOVED

| Element | Previous Color | Action |
|---------|---------------|--------|
| Tab "接口断言" active | `bg-blue-100 text-blue-700` | Removed entirely |
| Tab "业务断言" active | `bg-orange-100 text-orange-700` | Removed entirely |
| Tab inactive | `bg-gray-100 text-gray-600` | Removed entirely |

Note: The blue accent previously used for the "接口断言" tab active state is removed. Blue remains in use for other form elements (focus rings, method name display in assertion cards) and is not affected.

---

## Copywriting Contract

| Element | Copy |
|---------|------|
| Section label | "断言" with optional tag "(可选)" in `text-gray-400 text-xs` |
| Helper text | "选择业务断言方法，配置参数后系统自动执行验证" |
| Add button | "添加断言" with plus icon |
| Empty state | "暂无业务断言配置，点击\"添加断言\"开始配置" |
| Delete button (per card) | "删除" |
| Separator in card | "\|" (pipe character between method name and params) |

### Copy Being REMOVED

| Element | Previous Copy | Action |
|---------|--------------|--------|
| Tab 1 label | "接口断言" | Removed |
| Tab 2 label | "业务断言" | Removed |
| API assertion helper text | "输入 Python 代码进行 API 断言，支持时间断言、数据匹配等" | Removed |
| API assertion placeholder | "例如：result = api.get_order({{order_id}}); assert result['status'] == 'success'" | Removed |
| API assertion add button | "+ 添加接口断言" | Removed |

---

## Component Inventory

### Files to DELETE (2 frontend files)

| File | Lines | Reason |
|------|-------|--------|
| `frontend/src/components/Report/ApiAssertionResults.tsx` | 67 | Entire component for API assertion result display; no longer imported |
| `frontend/src/components/TaskModal/index.ts` (partial) | -- | Remove ApiAssertionResults export line (but keep file) |

### Files to MODIFY — Frontend (6 files)

| File | Change Summary | Scope |
|------|---------------|-------|
| `frontend/src/components/TaskModal/TaskForm.tsx` | Remove assertionTab state, tab switcher UI, api_assertions state/handlers; unwrap business assertions to always-visible | Major (~100 lines removed) |
| `frontend/src/types/index.ts` | Remove `ApiAssertionFieldResult`, `SSEApiAssertionEvent`, `TimelineItemAssertion`, `api_assertions` from Task/Create/Update/Run types; remove `api_assertion_results` from ReportDetailResponse | Moderate (~30 lines removed) |
| `frontend/src/hooks/useRunStream.ts` | Remove `api_assertion` SSE event listener block (lines 111-137); remove `SSEApiAssertionEvent` import; remove `api_assertions` from Run initialization | Moderate (~30 lines removed) |
| `frontend/src/components/RunMonitor/StepTimeline.tsx` | Remove `renderAssertionItem` function; remove `assertion` type handling from `getStatusIcon` colorMap and `handleItemClick`; remove `SSEApiAssertionEvent` from import | Moderate (~50 lines removed) |
| `frontend/src/components/Report/index.ts` | Remove `ApiAssertionResults` export line | Minor (1 line removed) |
| `frontend/src/api/reports.ts` | Remove `api_assertion_results` and `api_pass_rate` from response types and mapping; remove `SSEApiAssertionEvent` from types import if present | Minor (~5 lines removed) |

### Files to MODIFY — Backend (5 files)

| File | Change Summary | Scope |
|------|---------------|-------|
| `backend/core/api_assertion_service.py` | DELETE entire file (262 lines) | Delete |
| `backend/db/schemas.py` | Remove `api_assertions` fields from TaskBase/TaskCreate/TaskUpdate/TaskResponse; remove `SSEApiAssertionEvent`; remove from validators | Moderate |
| `backend/db/models.py` | Remove `api_assertions` column from Task model | Minor |
| `backend/api/routes/runs.py` | Remove `ApiAssertionService` import; remove api_assertions parameter and parsing in create_run(); remove execution loop (lines 247-321) | Major |
| `backend/core/report_service.py` | Remove `api_assertion_results` and `api_pass_rate` computation | Moderate |

### Files UNCHANGED (confirmed)

| File | Reason |
|------|--------|
| `frontend/src/components/TaskModal/AssertionSelector.tsx` | Business assertion selector, not affected |
| `frontend/src/components/TaskModal/FieldParamsEditor.tsx` | Business assertion field editor, not affected |
| `frontend/src/api/externalAssertions.ts` | Business assertion API client, not affected |
| `backend/api/routes/external_assertions.py` | Business assertion routes, not affected |

---

## Visual Specification

### TaskForm Simplification (Primary Change)

**BEFORE (current):** Tab state controls which section renders

```
+----------------------------------------------------------+
| 断言 (可选)                                               |
|                                                          |
| [接口断言]  [业务断言]   <-- tab switcher (REMOVE)       |
|                                                          |
| === if "接口断言" tab active ===                         |
| 输入 Python 代码...                                      |
| [textarea 1]                              [删除]         |
| [textarea 2]                              [删除]         |
| + 添加接口断言                                            |
|                                                          |
| === if "业务断言" tab active ===                         |
| 选择业务断言方法...                                      |
| [+ 添加断言]                                             |
| [card: methodName | params]              [删除]         |
| 暂无业务断言配置...                                       |
+----------------------------------------------------------+
```

**AFTER (target):** Business assertions always visible, no tab wrapper

```
+----------------------------------------------------------+
| 断言 (可选)                                               |
|                                                          |
| 选择业务断言方法，配置参数后系统自动执行验证              |
|                                                          |
| [+ 添加断言]                                             |
|                                                          |
| [card: methodName | params]              [删除]         |
|                                                          |
| 暂无业务断言配置，点击"添加断言"开始配置                  |
+----------------------------------------------------------+
```

**Implementation detail:**
- Remove `assertionTab` state (line 63)
- Remove tab switcher `<div className="flex gap-2 mb-3">` block (lines 458-481)
- Remove entire `api_assertions` content branch (lines 484-519)
- Remove ternary `{assertionTab === 'api' ? (...) : (...)}` wrapper
- Keep business assertions content (lines 521-585) directly under the section label
- Result: the business assertions section renders unconditionally

### TimelineItem Type Simplification

**BEFORE:**
```typescript
export type TimelineItem =
  | TimelineItemStep
  | TimelineItemPrecondition
  | TimelineItemAssertion  // REMOVE this member
```

**AFTER:**
```typescript
export type TimelineItem =
  | TimelineItemStep
  | TimelineItemPrecondition
```

Remove entirely:
- `ApiAssertionFieldResult` interface
- `SSEApiAssertionEvent` interface
- `TimelineItemAssertion` interface
- `api_assertions` field from `Task`, `CreateTaskDto`, `UpdateTaskDto`, `Run` interfaces
- `api_assertion_results` and `api_pass_rate` from `ReportDetailResponse`

### StepTimeline Assertion Rendering Removal

Remove from StepTimeline.tsx:
- `assertion` entry in `colorMap` object (line 18)
- `renderAssertionItem` function (lines 135-179)
- `{item.type === 'assertion' && renderAssertionItem(item.data, index)}` call (line 231)
- `SSEApiAssertionEvent` from import (line 3)
- `assertion` parameter handling in `handleItemClick` (lines 183-188)

After removal, StepTimeline renders only `step` and `precondition` item types.

### useRunStream SSE Listener Removal

Remove from useRunStream.ts:
- `SSEApiAssertionEvent` from import (line 3)
- `api_assertions: []` from Run initialization in `started` handler (line 53) and `precondition` early-init handler (line 93)
- Entire `api_assertion` event listener block (lines 111-137)

---

## Interaction Specification

### State Changes

| State | Before | After |
|-------|--------|-------|
| `assertionTab` | `useState<'api' \| 'business'>('api')` | Removed entirely |
| `formData.api_assertions` | `string[]` in FormData | Removed from FormData interface |
| `formData.assertions` | `AssertionConfig[]` in FormData | Unchanged |
| Run.api_assertions | `SSEApiAssertionEvent[]` on Run | Removed from Run interface |
| TimelineItem union | 3 members (step, precondition, assertion) | 2 members (step, precondition) |

### Form Submission

**Before:** `onSubmit` filters both `api_assertions` and `assertions`:
```typescript
onSubmit({
  ...formData,
  preconditions: formData.preconditions.filter(p => p.trim()),
  api_assertions: formData.api_assertions.filter(a => a.trim()),
  assertions: formData.assertions,
})
```

**After:** `api_assertions` line removed:
```typescript
onSubmit({
  ...formData,
  preconditions: formData.preconditions.filter(p => p.trim()),
  assertions: formData.assertions,
})
```

### Edit Mode Initialization

**Before:** `useEffect` sets `api_assertions` from `initialData`:
```typescript
api_assertions: initialData.api_assertions || [''],
```

**After:** Line removed from useEffect. Only `assertions: initialData.assertions || []` remains.

### Click Behavior (StepTimeline)

After removal, StepTimeline click handling simplifies:
- `step` items: set viewIndex for ScreenshotPanel (unchanged)
- `precondition` items: toggle inline expansion (unchanged)
- `assertion` items: no longer exist in the timeline

---

## Database Migration

| Operation | SQL | Timing |
|-----------|-----|--------|
| Drop column | `ALTER TABLE tasks DROP COLUMN api_assertions;` | After code cleanup, server stopped |

Note: SQLite 3.51.0 supports DROP COLUMN (since 3.35.0+). No Alembic needed. Execute when server is stopped to avoid "database is locked" errors.

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | not applicable | shadcn not initialized; no third-party registries; no new dependencies |

---

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS
- [ ] Dimension 2 Visuals: PASS
- [ ] Dimension 3 Color: PASS
- [ ] Dimension 4 Typography: PASS
- [ ] Dimension 5 Spacing: PASS
- [ ] Dimension 6 Registry Safety: PASS

**Approval:** pending
