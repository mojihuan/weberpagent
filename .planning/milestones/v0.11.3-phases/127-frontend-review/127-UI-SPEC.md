---
phase: 127
slug: frontend-review
status: draft
shadcn_initialized: false
preset: none
created: "2026-05-03"
---

# Phase 127 -- UI Design Contract (Review Baseline)

> This is a review-only phase. This contract documents the **existing** design system as reverse-engineered from the codebase, providing a baseline against which review findings are assessed. No new UI is built in this phase.

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none (no shadcn detected, no components.json) |
| Preset | not applicable |
| Component library | none (custom components with Tailwind CSS utility classes) |
| Icon library | lucide-react 0.577.0 |
| Font | system default (no custom font declared in index.css or tailwind config) |
| Toast library | sonner 2.0.7 (configured in main.tsx, position: top-center, richColors: true) |
| Chart library | recharts 3.8.0 (Dashboard visualizations) |
| CSS framework | Tailwind CSS 4.2.1 with @tailwindcss/vite plugin (no tailwind.config file -- uses v4 zero-config) |

---

## Spacing Scale

Existing values observed in codebase (all multiples of 4):

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Icon gaps (`gap-1`), inline badge padding (`px-1`) |
| sm | 8px | Compact element spacing (`gap-2`, `px-2`, `py-1`), badge padding |
| md | 12px | Component internal spacing (`gap-3`, `px-3`, `p-3`) |
| base | 16px | Default element spacing (`gap-4`, `px-4`, `p-4`, `py-3`), page padding (`p-6` via Layout) |
| lg | 20px | Card padding (`p-5`), section heading margins (`mb-5`) |
| xl | 24px | Page-level padding (`p-6`), section gaps (`mb-6`) |
| 2xl | 32px | Sidebar width (`w-60`), icon sizes (`w-8 h-8`) |
| 3xl | 48px | Empty state vertical padding (`py-12`), large icon size (`w-12 h-12`) |

Exceptions: `h-9` (36px) for button height in Button.tsx, `h-10` (40px) for nav items in NavItem.tsx, `w-60` (240px) for sidebar width. These are component-specific, not scale violations.

---

## Typography

Observed font sizes from codebase (Tailwind utility classes):

| Role | Size | Tailwind Class | Weight | Line Height |
|------|------|----------------|--------|-------------|
| Display | 30px | `text-3xl` | 600 (semibold) | default (1) |
| Heading | 24px | `text-2xl` | 600 (semibold) | default (1) |
| Subheading | 18px | `text-lg` | 500 (medium) | default (1.5) |
| Body | 14px | `text-sm` | 400 (regular) | default (1.5) |
| Label | 12px | `text-xs` | 500 (medium) | default (1.5) |

Weight usage: only 400 (regular/default) and 500-600 (medium/semibold) observed. No 700+ (bold) usage found.

**Review baseline note:** The codebase uses `text-sm` (14px) as the primary body text size rather than the conventional `text-base` (16px). This is consistent across all pages and components. Any findings about readability should note this is an intentional project convention, not a bug.

---

## Color

Observed color palette from codebase:

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | white (#fff) | Page backgrounds (`bg-white`), card surfaces, main content area |
| Secondary (30%) | gray-50 (#f9fafb) | Sidebar (`bg-gray-50`), table headers (`bg-gray-50`), sub-sections, hover states |
| Border | gray-200 (#e5e7eb) | Card borders, table borders, dividers |
| Muted text | gray-500 (#6b7280) | Secondary text, labels, timestamps, metadata |
| Body text | gray-900 (#111827) | Primary text, headings, values |
| Accent (10%) | blue-500 (#3b82f6) | Primary actions, active nav, links, focus rings, CTA buttons |
| Accent hover | blue-600 (#2563eb) | Hover state for primary actions |
| Success | green-500 (#22c55e) | Status badges (success), positive trends |
| Warning | yellow-500 (#eab308) | Status badges (pending), warning states |
| Error | red-500 (#ef4444) | Status badges (failed), error messages, destructive borders |
| Error surface | red-50 (#fef2f2) | Error backgrounds, assertion failure panels |
| Info surface | blue-50 (#eff6ff) | Running status badge, drag-active states |
| Special | purple-50 (#faf5ff) | Precondition timeline items (unique to TimelineItemCard) |

Accent reserved for: primary CTA buttons, active navigation item, links, focus ring indicator, running status badge.

**Review baseline note:** Color usage is consistent across components. Status colors follow a standard semantic pattern (green=success, red=failed, yellow=pending, blue=running). The purple-50 for preconditions is the only non-standard color choice.

---

## Copywriting Contract

Observed copywriting patterns from existing codebase:

| Element | Copy | Source |
|---------|------|--------|
| Page headings | Chinese: "仪表盘", "执行监控", "报告查看" | pages/*.tsx |
| Empty state default | "暂无数据" (No data) | EmptyState.tsx |
| Empty state (RunList) | "暂无执行记录" / "创建任务后可启动执行" | RunList.tsx:144-145 |
| Error state (Reports) | Red panel with error message from API | Reports.tsx:30 |
| Status labels | Chinese: "等待中", "执行中", "成功", "失败", "已停止" | RunList.tsx:9-13 |
| Primary CTA (quick start) | "快速执行" (Quick Execute) | QuickStart.tsx |
| Primary CTA (empty runs) | "创建任务" (Create Task) | RunList.tsx:148 |
| Confirmation (ConfirmModal) | Generic confirmation with confirm/cancel | shared/ConfirmModal.tsx |
| Batch execute | "批量执行" (Batch Execute) | TaskList/BatchExecuteDialog.tsx |

**Review baseline note:** All user-facing copy is in Chinese. The codebase does not use i18n -- strings are hardcoded in components. Findings about internationalization are out of scope for this phase (single-user, Chinese-language product).

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| shadcn official | none (not initialized) | not applicable |
| Third-party | none | not applicable |

No shadcn detected. No components.json found. The project uses a custom component library built on Tailwind CSS utility classes. No third-party registry vetting required.

---

## Review-Specific Baseline

### Component Inventory (Existing -- for review reference)

| Category | Count | Key Files |
|----------|-------|-----------|
| Pages | 8 | Dashboard, Tasks, TaskDetail, RunList, RunMonitor, BatchProgress, Reports, ReportDetail |
| TaskModal components | 6 | TaskForm, TaskFormModal, DataMethodSelector, AssertionSelector, OperationCodeSelector, FieldParamsEditor, JsonTreeViewer |
| RunMonitor components | 4 | StepTimeline, RunHeader, ScreenshotPanel, ReasoningLog |
| Report components | 7 | ReportHeader, ReportTable, SummaryCard, StepItem, TimelineItemCard, AssertionResults, PreconditionSection |
| TaskList components | 5 | TaskTable, TaskRow, TaskFilters, TaskListHeader, BatchActions, BatchExecuteDialog |
| Shared components | 5 | Button, EmptyState, LoadingSpinner, Pagination, ConfirmModal, ImageViewer |
| Hooks | 5 | useRunStream, useTasks, useReports, useDashboard, useBatchProgress |
| API modules | 9 | client + 8 domain modules |

### Known Anti-Patterns (from RESEARCH.md -- for review verification)

| Pattern | Files | Description |
|---------|-------|-------------|
| set-state-in-effect | RunMonitor.tsx:26, CodeViewerModal.tsx:26 | setState inside useEffect causes cascading renders |
| no-explicit-any | types/index.ts (4), DataMethodSelector.tsx (1) | `any` type usage bypasses type safety |
| exhaustive-deps | AssertionSelector.tsx:276, DataMethodSelector.tsx:283,299 | Missing hook dependencies |
| Manual fetch pattern | useTasks, useReports, useDashboard | useState+useEffect+fetch instead of React Query useQuery |
| JSON.parse unprotected | useRunStream.ts (7 handlers) | No try/catch around JSON.parse in SSE event handlers |
| Array index as key | StepTimeline.tsx | Using `key={index}` for timeline items |

### Cross-Validation Targets

| Frontend File | Backend File | What to Verify |
|---------------|--------------|----------------|
| useRunStream.ts | event_manager.py | SSE event type names match; JSON data structure alignment |
| useRunStream.ts | run_pipeline.py | Event sequence (started -> step -> finished) matches frontend handler expectations |
| types/index.ts | db/schemas.py | TypeScript interfaces match Pydantic schemas for SSE events |
| api/client.ts | api/routes/*.py | Request format and error response structure match |

---

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS (documented existing copy patterns)
- [ ] Dimension 2 Visuals: PASS (documented existing component inventory)
- [ ] Dimension 3 Color: PASS (documented existing color palette with 60/30/10 split)
- [ ] Dimension 4 Typography: PASS (documented 5 sizes, 2 weight levels)
- [ ] Dimension 5 Spacing: PASS (documented 8-point scale with component-specific exceptions)
- [ ] Dimension 6 Registry Safety: PASS (no registries, shadcn not initialized)

**Approval:** pending
