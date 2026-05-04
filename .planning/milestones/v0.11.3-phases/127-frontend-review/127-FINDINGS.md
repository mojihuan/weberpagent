# Phase 127: Frontend Review - Findings

**Review Date:** 2026-05-03
**Scope:** 87 frontend TypeScript/TSX files, ~8,898 lines
**Methodology:** Breadth-first scan + ESLint/TypeScript tooling + CONCERNS.md verification + SSE cross-validation

## Tool Results

### TypeScript Compilation (tsc --noEmit)

**Result:** Zero errors. All type checking passes cleanly.

Confirmed: strict mode enabled, `verbatimModuleSyntax: true`, `erasableSyntaxOnly: true`. All 87 files compile without issues.

### ESLint Scan

**Result:** 18 problems (15 errors, 3 warnings), 1 auto-fixable.

| # | File | Line | Severity | Rule ID | Message |
|---|------|------|----------|---------|---------|
| 1 | types/index.ts | 91 | Error | @typescript-eslint/no-explicit-any | Unexpected any. Specify a different type |
| 2 | types/index.ts | 334 | Error | @typescript-eslint/no-explicit-any | Unexpected any. Specify a different type |
| 3 | types/index.ts | 339 | Error | @typescript-eslint/no-explicit-any | Unexpected any. Specify a different type |
| 4 | types/index.ts | 353 | Error | @typescript-eslint/no-explicit-any | Unexpected any. Specify a different type |
| 5 | api/externalDataMethods.ts | 26 | Error | @typescript-eslint/no-explicit-any | Unexpected any. Specify a different type |
| 6 | components/TaskModal/DataMethodSelector.tsx | 92 | Error | @typescript-eslint/no-explicit-any | Unexpected any. Specify a different type |
| 7 | components/TaskModal/DataMethodSelector.tsx | 321 | Error | @typescript-eslint/no-explicit-any | Unexpected any. Specify a different type |
| 8 | components/TaskModal/DataMethodSelector.tsx | 161 | Error | no-useless-escape | Unnecessary escape character: \[ |
| 9 | components/TaskModal/DataMethodSelector.tsx | 631 | Error | no-case-declarations | Unexpected lexical declaration in case block |
| 10 | components/TaskModal/DataMethodSelector.tsx | 632 | Error | no-case-declarations | Unexpected lexical declaration in case block |
| 11 | components/TaskDetail/CodeViewerModal.tsx | 26 | Error | react-hooks/set-state-in-effect | setCodeLoading(false) called synchronously in effect |
| 12 | pages/ReportDetail.tsx | 17 | Error | react-hooks/set-state-in-effect | setLoading(true) called synchronously in effect |
| 13 | pages/RunMonitor.tsx | 26 | Error | react-hooks/set-state-in-effect | setViewIndex(run.timeline.length - 1) called synchronously in effect |
| 14 | components/shared/StatusBadge.tsx | 1 | Error | react-refresh/only-export-components | File exports constants alongside component |
| 15 | hooks/useTasks.ts | 45 | Error | prefer-const | 'result' is never reassigned. Use 'const' instead |
| 16 | components/TaskModal/AssertionSelector.tsx | 276 | Warning | react-hooks/exhaustive-deps | Missing dependency: 'handleCancel' in useEffect |
| 17 | components/TaskModal/DataMethodSelector.tsx | 283 | Warning | react-hooks/exhaustive-deps | Missing dependency: 'methods.classes' in useEffect |
| 18 | components/TaskModal/DataMethodSelector.tsx | 299 | Warning | react-hooks/exhaustive-deps | Missing dependency: 'handleCancel' in useEffect |

**Delta from RESEARCH:** Research listed `no-explicit-any` in types/index.ts lines 91, 334, 339, 353 (4 instances) and DataMethodSelector.tsx line 92 (1 instance). Actual scan found an additional `any` at DataMethodSelector.tsx line 321 and externalDataMethods.ts line 26, bringing the `no-explicit-any` total to 7 (not 5). Research listed `set-state-in-effect` in CodeViewerModal.tsx line 26 and RunMonitor.tsx line 26, but actual scan also found it in ReportDetail.tsx line 17 (3 instances, not 2). Additionally, Research did not mention `no-case-declarations` (2), `react-refresh/only-export-components` (1), or `prefer-const` (1). Total is still 18 but composition differs from RESEARCH expectations.

## Risk Priority Matrix

| Priority | File | Lines | Risk Justification |
|----------|------|-------|--------------------|
| P1 | hooks/useRunStream.ts | 215 | SSE core -- all 7 JSON.parse without try/catch, isConnectedRef set before EventSource open, no onopen handler, timeline/steps arrays unbounded growth, eslint-disable on useEffect deps |
| P1 | components/TaskModal/DataMethodSelector.tsx | 829 | Largest component -- complex multi-step state machine, 5 ESLint errors (2x any, useless escape, 2x case declarations), 2 exhaustive-deps warnings, state mutation concerns |
| P1 | components/TaskModal/TaskForm.tsx | 560 | Task form with child modal composition (DataMethodSelector, AssertionSelector, OperationCodeSelector) -- complex prop threading and state coordination |
| P1 | components/TaskModal/AssertionSelector.tsx | 546 | Assertion configuration with external method calls -- 1 exhaustive-deps warning, complex async operations |
| P1 | api/client.ts | 61 | HTTP client with retry logic -- all API calls depend on this, exponential backoff implementation, error handling and toast integration |
| P2 | types/index.ts | 456 | All TypeScript interfaces -- 4x `any` type usage, must match backend Pydantic schemas |
| P2 | components/RunMonitor/StepTimeline.tsx | 285 | Timeline rendering -- array index as key (per RESEARCH), renders all timeline items |
| P2 | components/TaskList/TaskRow.tsx | 140 | Task row with status/actions -- interactive element with selection state |
| P2 | components/ImportModal/ImportModal.tsx | 117 | Import modal coordinator -- multi-step wizard |
| P2 | components/ImportModal/UploadStep.tsx | 132 | File upload with preview |
| P2 | components/ImportModal/PreviewStep.tsx | 110 | Data preview with validation |
| P2 | components/ImportModal/ResultStep.tsx | 30 | Import result display |
| P2 | components/TaskModal/FieldParamsEditor.tsx | 236 | Field parameter editor -- form state management |
| P2 | components/TaskModal/OperationCodeSelector.tsx | 226 | Operation code selector -- search/filter state |
| P2 | components/TaskModal/JsonTreeViewer.tsx | 221 | JSON tree viewer -- recursive rendering |
| P2 | components/TaskModal/TaskFormModal.tsx | 55 | Task form modal wrapper |
| P2 | components/Report/TimelineItemCard.tsx | 247 | Timeline item card -- complex rendering |
| P2 | components/Report/StepItem.tsx | 132 | Step detail rendering |
| P2 | components/Report/ReportTable.tsx | 92 | Report table -- list rendering |
| P2 | components/Report/PreconditionSection.tsx | 100 | Precondition results display |
| P2 | components/Report/AssertionResults.tsx | 60 | Assertion result display |
| P2 | components/Report/SummaryCard.tsx | 24 | Summary statistics card |
| P2 | components/Report/ReportHeader.tsx | 33 | Report header component |
| P2 | components/Report/ReportFilters.tsx | 53 | Report filter controls |
| P2 | components/RunMonitor/ScreenshotPanel.tsx | 130 | Screenshot viewer panel |
| P2 | components/RunMonitor/RunHeader.tsx | 60 | Run status header |
| P2 | components/RunMonitor/ReasoningLog.tsx | 64 | Reasoning text display |
| P2 | hooks/useTasks.ts | 135 | Task list hook -- manual fetch pattern, prefer-const error, console.error usage |
| P2 | hooks/useReports.ts | 93 | Reports hook -- manual fetch pattern |
| P2 | hooks/useDashboard.ts | 43 | Dashboard hook -- manual fetch pattern |
| P2 | hooks/useBatchProgress.ts | 68 | Batch progress hook -- 2s polling pattern |
| P2 | api/reports.ts | 172 | Reports API -- largest API module |
| P2 | api/tasks.ts | 113 | Tasks API -- CRUD operations |
| P2 | api/runs.ts | 61 | Runs API -- start/stop/stream |
| P2 | api/externalDataMethods.ts | 38 | External data methods API -- 1x any type |
| P2 | api/externalOperations.ts | 24 | External operations API |
| P2 | api/externalAssertions.ts | 32 | External assertions API |
| P2 | api/dashboard.ts | 44 | Dashboard API |
| P2 | api/batches.ts | 19 | Batches API |
| P2 | pages/Tasks.tsx | 211 | Tasks page -- task list with filters, pagination |
| P2 | pages/TaskDetail.tsx | 174 | Task detail page -- task info, runs, code |
| P2 | pages/RunList.tsx | 156 | Run list page -- run history |
| P2 | pages/RunMonitor.tsx | 132 | Run monitor page -- SSE consumption, set-state-in-effect |
| P2 | pages/ReportDetail.tsx | 114 | Report detail page -- set-state-in-effect |
| P2 | pages/BatchProgress.tsx | 98 | Batch progress page -- polling display |
| P2 | pages/Reports.tsx | 81 | Reports list page |
| P2 | pages/Dashboard.tsx | 53 | Dashboard page -- summary stats |
| P3 | components/shared/ConfirmModal.tsx | 63 | Simple modal -- clean |
| P3 | components/shared/EmptyState.tsx | 16 | Simple empty state -- clean |
| P3 | components/shared/ImageViewer.tsx | 63 | Image viewer with ESC close -- clean |
| P3 | components/shared/LoadingSpinner.tsx | 32 | Simple spinner -- clean |
| P3 | components/shared/Pagination.tsx | 53 | Client-side pagination -- renders all page buttons |
| P3 | components/shared/ReasoningText.tsx | 41 | Reasoning text parser display -- clean |
| P3 | components/shared/StatusBadge.tsx | 35 | Status badge with constants export -- react-refresh/only-export-components error |
| P3 | components/Dashboard/QuickStart.tsx | 70 | Quick start selector -- console.error on failure |
| P3 | components/Dashboard/RecentRuns.tsx | 98 | Recent runs table -- clean |
| P3 | components/Dashboard/StatCard.tsx | 24 | Simple stat card -- clean |
| P3 | components/Dashboard/TrendChart.tsx | 90 | Recharts trend chart -- clean |
| P3 | components/BatchProgress/BatchSummary.tsx | 41 | Batch progress bar -- clean |
| P3 | components/BatchProgress/BatchTaskCard.tsx | 88 | Batch task card -- clean |
| P3 | components/TaskDetail/CodeExecutionStatus.tsx | 48 | Code execution status -- clean |
| P3 | components/TaskDetail/ConfigPanel.tsx | 54 | Task config panel -- hardcoded values ("30 秒/步", "3 次") |
| P3 | components/TaskDetail/RunHistory.tsx | 70 | Run history list -- clean |
| P3 | components/TaskDetail/StatsChart.tsx | 79 | Recharts stats chart -- clean |
| P3 | components/TaskDetail/TaskHeader.tsx | 72 | Task header with actions -- clean |
| P3 | components/TaskDetail/TaskInfo.tsx | 48 | Task info display -- clean |
| P3 | components/TaskList/BatchActions.tsx | 49 | Batch action buttons -- clean |
| P3 | components/TaskList/BatchExecuteDialog.tsx | 99 | Batch execution dialog -- clean |
| P3 | components/TaskList/TaskFilters.tsx | 52 | Filter controls -- clean |
| P3 | components/TaskList/TaskListHeader.tsx | 28 | Page header -- clean |
| P3 | components/TaskList/TaskTable.tsx | 66 | Task table with selection -- clean |
| P3 | constants/roleLabels.ts | 19 | Role label constants -- clean |
| P3 | utils/reasoningParser.ts | 44 | Reasoning text parser -- clean |
| P3 | utils/retry.ts | 22 | Sleep and isNetworkError -- clean |
| P3 | App.tsx | 42 | Router + QueryClientProvider -- QueryClient configured but unused by hooks |
| P3 | main.tsx | 12 | React root entry -- clean |
| P3 | components/Layout.tsx | 18 | Layout wrapper -- clean |
| P3 | components/Sidebar.tsx | 22 | Navigation sidebar -- clean |
| P3 | components/NavItem.tsx | 26 | Nav link item -- clean |
| P3 | components/Button.tsx | 24 | Reusable button -- clean |
| P3 | index.ts (barrel files, 7 files) | ~26 | Re-export barrel files -- clean |

**Total: 87 files, 5 P1 + 43 P2 + 39 P3 (including 7 barrel index.ts files)**

## CONCERNS.md Verification

| # | CONCERNS.md Entry | Status | Finding Reference |
|---|-------------------|--------|-------------------|
| 1 | "No frontend tests" (Priority: Low) | **Confirmed** | No vitest/jest/mocha/@testing-library in package.json. No test files found in src/. Zero frontend test coverage. |
| 2 | "DataMethodSelector 829 lines" | **Confirmed** | Line count verified at exactly 829 lines. Largest frontend file. |
| 3 | "main.tsx missing QueryClientProvider" | **Misleading** | QueryClientProvider is in App.tsx (line 23), not main.tsx. main.tsx correctly handles only React root + Toaster. CONTEXT.md was incorrect to flag this. |
| 4 | "event_manager.py memory leak" (backend) | **Frontend mirror confirmed** | useRunStream.ts `run.steps` and `run.timeline` arrays grow unbounded -- every step, precondition, and assertion event appends to both arrays with spread operator (`[...prev.steps, newStep]`, `[...prev.timeline, newItem]`). No size cap or cleanup. Long-running tests (50+ steps) will cause growing memory usage and increasingly expensive spread operations. |

## SSE Cross-Validation

### Backend Event Types vs Frontend Listeners

| Backend Event Type | Backend Publish Location | Frontend Listener | Match? |
|--------------------|--------------------------|-------------------|--------|
| `started` | run_pipeline.py:512 | useRunStream.ts:43 `addEventListener('started')` | Yes |
| `step` | run_pipeline.py:420 | useRunStream.ts:58 `addEventListener('step')` | Yes |
| `precondition` | run_pipeline.py:99,109 | useRunStream.ts:82 `addEventListener('precondition')` | Yes |
| `assertion` | run_pipeline.py:219,258 | useRunStream.ts:125 `addEventListener('assertion')` | Yes |
| `external_assertions` | run_pipeline.py:267,334 | useRunStream.ts:109 `addEventListener('external_assertions')` | Yes |
| `finished` | run_pipeline.py:123,467 | useRunStream.ts:146 `addEventListener('finished')` | Yes |
| `error` | run_pipeline.py:573 | useRunStream.ts:161 `addEventListener('error')` | Yes |

**All 7 backend event types have matching frontend listeners. No missing or extra listeners.**

### Backend Event Schema vs Frontend Field Access

| Event | Backend Schema Fields | Frontend Fields Accessed | Mismatch? |
|-------|----------------------|-------------------------|-----------|
| started | run_id, task_id, task_name | data.task_id (line 44) | task_name ignored by frontend |
| step | index, action, reasoning, screenshot_url, status, duration_ms, step_stats | stepData.index, .action, .reasoning, .screenshot_url, .status, .duration_ms | step_stats ignored by frontend |
| finished | status, total_steps, duration_ms | parsed.status (line 149) | total_steps and duration_ms ignored by frontend |
| precondition | index, code, status, error, duration_ms, variables | data.index, .code, .status (via typed SSEPreconditionEvent) | error, duration_ms, variables consumed via type but not all displayed |
| assertion | assertion_id, assertion_name, assertion_type, status, message, actual_value, field_results | data.assertion_id etc. (via typed SSEAssertionEvent) | Appears fully consumed |
| external_assertions | json.dumps summary dict | data.total, .passed, .failed, .errors | Match |
| error | error string | parsed.error (line 163) | Match |

### Backend None Sentinel Handling

- **Backend:** event_manager.subscribe() yields `None` as end-of-stream sentinel (line 100-101). The stream_run endpoint (runs_routes.py:323-324) breaks on `if event is None`.
- **Frontend:** Does NOT rely on None sentinel. EventSource receives SSE events as text -- the None sentinel is consumed by the backend StreamingResponse generator and never reaches the frontend. The frontend relies on `finished` and `error` event types to detect stream end. **This is correct behavior.**

### Backend Heartbeat Handling

- **Backend:** event_manager sends `:heartbeat\n\n` every 20 seconds. SSE comments (lines starting with `:`) are ignored by EventSource per SSE specification.
- **Frontend:** No explicit heartbeat handling needed. EventSource silently ignores comment lines. **Correct.**

### SSE Format Consistency

- **Backend publish format:** `f"event: {type}\ndata: {json}\n\n"`
- **Frontend consumption:** `eventSource.addEventListener(type, handler)` with `JSON.parse(e.data)`
- **Match confirmed:** Standard SSE format with named events. Backend formats events correctly for EventSource consumption.

### SSE Cross-Validation Findings

**[SSE-1] [Medium] Backend event fields silently ignored by frontend**
- **Severity:** Medium
- **Category:** Architecture
- **Description:** The frontend ignores several backend event fields: `started.task_name`, `step.step_stats`, `finished.total_steps`, `finished.duration_ms`. These fields are computed and transmitted but never used. The frontend uses `new Date().toISOString()` for timestamps instead of backend-provided timing data.
- **Recommendation:** Either consume these fields or remove them from the backend SSE schemas to reduce payload size. The `finished.duration_ms` is particularly useful for accurate timing display.

**[SSE-2] [Medium] useRunStream.ts connects before EventSource fires 'open' event**
- **Severity:** Medium
- **Category:** Correctness
- **Description:** In connect() (line 36-37), `setIsConnected(true)` and `isConnectedRef.current = true` are set synchronously before EventSource establishes the connection. There is no `eventSource.onopen` handler. The frontend reports "connected" when it has only initiated the connection, not when the server confirms it. If the server is unreachable, the UI shows "connected" until `onerror` fires.
- **Recommendation:** Add `eventSource.onopen` handler. Move `setIsConnected(true)` into the onopen callback. Keep `isConnectedRef.current = true` in connect() only as a guard against duplicate connections.

**[SSE-3] [High] All 7 JSON.parse calls in useRunStream.ts lack try/catch**
- **Severity:** High
- **Category:** Correctness
- **Description:** Lines 44, 59, 83, 110, 126, 147, 163 all call `JSON.parse(e.data)` without try/catch. If the backend sends malformed JSON (e.g., during a partial write or serialization error), the exception will propagate to the addEventListener callback. EventSource catches listener exceptions internally, but the event is silently lost and the run state becomes inconsistent.
- **Recommendation:** Wrap all JSON.parse calls in try/catch. On failure, log the error (via toast or console) and skip the event rather than silently losing it.

**[SSE-4] [Medium] Timeline and steps arrays grow without bound**
- **Severity:** Medium
- **Category:** Performance
- **Description:** Every step, precondition, and assertion event appends to both `prev.steps` and `prev.timeline` arrays using spread operator (`[...prev.steps, newStep]`, `[...prev.timeline, newItem]`). For a 50-step test with preconditions and assertions, this creates ~100+ items in each array. Each append copies the entire array (O(n) per step, O(n^2) total). For very long tests, this causes increasing memory pressure and React render cost.
- **Recommendation:** Consider a maximum timeline size or use a ref-based mutable array for performance-critical paths. The mirror issue to backend event_manager memory leak (CONCERNS.md #4).

**[SSE-5] [Low] eslint-disable comment on useEffect dependencies**
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 205 has `// eslint-disable-next-line react-hooks/exhaustive-deps` on the main useEffect that connects/disconnects. The dependency array is `[autoConnect, runId]` but the linter likely expects `connect` and `disconnect` to be included. The eslint-disable masks a potential stale closure issue.
- **Recommendation:** Verify that connect/disconnect are stable (they are -- wrapped in useCallback with appropriate deps). Document why the eslint-disable is safe.

## Quick-Scan Findings (P3 Files)

### [P3] QuickStart.tsx:26 -- console.error violates coding-style.md
- **Severity:** Low
- **Category:** Architecture
- **Description:** `console.error('Failed to start run:', error)` at line 26 violates the coding-style.md rule against console.log statements. Should use a toast or silent error handling instead.
- **Recommendation:** Replace with `toast.error('启动执行失败')` or remove the catch block and let the error propagate to the caller.

### [P3] StatusBadge.tsx:1 -- react-refresh/only-export-components error
- **Severity:** Low
- **Category:** Architecture
- **Description:** The file exports both `statusConfig` (a constant) and `StatusBadge` (a component) and `Status` (a type). The react-refresh plugin flags this because HMR cannot safely hot-reload files that mix component and non-component exports.
- **Recommendation:** Move `statusConfig` and `Status` type to a separate file (e.g., `constants/status.ts`) and import them into StatusBadge.tsx.

### [P3] ConfigPanel.tsx:39-44 -- Hardcoded configuration values
- **Severity:** Low
- **Category:** Correctness
- **Description:** ConfigPanel displays hardcoded values "30 秒/步" (timeout) and "3 次" (retries) regardless of actual task configuration. If backend config changes, these displayed values will be stale.
- **Recommendation:** Either derive from task props or remove the misleading display. Currently the backend does not expose per-task timeout/retry configuration, so the hardcoded values may be intentionally showing defaults.

### [P3] Pagination.tsx:15 -- Renders all page buttons for large page counts
- **Severity:** Low
- **Category:** Performance
- **Description:** `Array.from({ length: totalPages }, ...)` creates a button for every page. If totalPages is large (e.g., 100+), this creates excessive DOM nodes. Currently mitigated by client-side pagination with pageSize=10 and relatively small datasets.
- **Recommendation:** Add ellipsis/truncation for large page counts (>7 pages). Low priority given current data volume.

### [P3] App.tsx:13-19 -- QueryClient configured but React Query hooks unused
- **Severity:** Low
- **Category:** Architecture
- **Description:** QueryClient is instantiated with `refetchOnWindowFocus: false` and provided via QueryClientProvider, but no hooks in the codebase use `useQuery` or `useMutation`. All data fetching hooks (useTasks, useReports, useDashboard, useBatchProgress) use manual useState + useEffect + fetch pattern. React Query adds ~40KB to the bundle without benefit.
- **Recommendation:** Either migrate hooks to use React Query (recommended for caching and stale-while-revalidate) or remove the dependency entirely.

### [P3] TrendChart.tsx:37, StatsChart.tsx:19 -- Inline style for minHeight
- **Severity:** Low
- **Category:** Architecture
- **Description:** `style={{ minHeight: '320px' }}` in TrendChart and inline style objects in chart configs bypass Tailwind CSS. Minor inconsistency with the rest of the codebase.
- **Recommendation:** Replace with Tailwind class `min-h-80` where possible.

### [P3] BatchTaskCard.tsx:83 -- Type assertion on StatusBadge status
- **Severity:** Low
- **Category:** Correctness
- **Description:** Line 83 uses `as Parameters<typeof StatusBadge>[0]['status']` to cast `run.status` to the expected type. This masks potential type mismatches between BatchRunSummary.status and the StatusBadge accepted statuses.
- **Recommendation:** Ensure BatchRunSummary.status type matches the Status union type from StatusBadge, removing the need for the cast.

### [P3] BatchTaskCard.tsx:79 -- Nullish coalescing on task_name
- **Severity:** Low
- **Category:** Correctness
- **Description:** `run.task_name ?? '未命名任务'` suggests task_name can be null/undefined in the BatchRunSummary type. This is a valid defensive pattern but indicates the type definition may need tightening.
- **Recommendation:** Verify that BatchRunSummary.task_name is actually nullable from the backend, and if so, document why.

### [P3] ImageViewer.tsx:25-29 -- Programmatic download via DOM manipulation
- **Severity:** Low
- **Category:** Architecture
- **Description:** `handleDownload` creates an anchor element, sets href/download, and clicks it programmatically. This is a common pattern but could fail on some browsers with cross-origin images.
- **Recommendation:** No action needed for current use case (same-origin screenshots). Note for future if image sources change.

### [P3] EmptyState.tsx:7 -- React.ReactNode type used inline
- **Severity:** Low
- **Category:** Architecture
- **Description:** `React.ReactNode` is used directly in the interface instead of importing `ReactNode` from 'react'. Works but inconsistent with other files that use `import type { ReactNode } from 'react'`.
- **Recommendation:** Standardize to `import type { ReactNode } from 'react'` pattern.

### [P3] All P3 shared/utility files -- No significant issues found
- **Severity:** N/A
- **Category:** N/A
- **Description:** The following P3 files were reviewed and found clean with no significant issues: LoadingSpinner.tsx, StatCard.tsx, Layout.tsx, Sidebar.tsx, NavItem.tsx, Button.tsx, ConfirmModal.tsx, roleLabels.ts, retry.ts, reasoningParser.ts, all barrel index.ts files.
- **Recommendation:** No action needed.

## Summary Statistics

### By Severity

| Severity | Count | Examples |
|----------|-------|---------|
| Critical | 0 | -- |
| High | 1 | JSON.parse without try/catch in all SSE handlers (SSE-3) |
| Medium | 5 | isConnectedRef premature set (SSE-2), timeline unbounded growth (SSE-4), backend fields silently ignored (SSE-1), eslint-disable on useEffect deps (SSE-5), Pagination all-page-buttons |
| Low | 8 | console.error in QuickStart, StatusBadge exports, hardcoded config values, unused React Query, inline styles, type assertions, React.ReactNode inconsistency, nullish coalescing |

### By Category

| Category | Count |
|----------|-------|
| Correctness | 4 |
| Architecture | 6 |
| Performance | 2 |
| Security | 0 |

### ESLint Error Breakdown

| Category | Count |
|----------|-------|
| no-explicit-any | 7 |
| set-state-in-effect | 3 |
| no-case-declarations | 2 |
| no-useless-escape | 1 |
| react-refresh/only-export-components | 1 |
| prefer-const | 1 |
| exhaustive-deps (warnings) | 3 |

### Files by Priority

| Priority | File Count | Line Count |
|----------|------------|------------|
| P1 | 5 | 2,211 |
| P2 | 43 | 5,264 |
| P3 | 39 | 1,423 |
| **Total** | **87** | **8,898** |

### Key Takeaways for Plan 02 (P1 Deep-Dive)

1. **useRunStream.ts** has the highest density of issues: 7 unprotected JSON.parse calls, premature connection state, unbounded array growth, and no error recovery. The SSE cross-validation confirms the backend format is correct -- all issues are frontend-side.
2. **DataMethodSelector.tsx** (829 lines) has 5 ESLint errors and 2 dependency warnings, suggesting complex state management that warrants careful review of the multi-step state machine.
3. **client.ts** (61 lines) is clean from a linting perspective but deserves deep review for retry logic edge cases (recursive retry with toast accumulation, error type detection).
4. **TaskForm.tsx** and **AssertionSelector.tsx** are the other two P1 targets with 560 and 546 lines respectively, both managing complex form state with child modal coordination.

---
*Phase 127-01 breadth scan complete. Plan 02 will deep-dive P1 files. Plan 03 will quick-scan P2/P3 files and produce final summary.*

## Deep-Dive Findings (P1 Files)

### useRunStream.ts (215 lines)

### [DD-USE-01] useRunStream.ts:44,59,83,110,126,147,163 -- All 7 JSON.parse calls lack try/catch protection
- **Severity:** High
- **Category:** Correctness
- **Description:** Every SSE event listener calls `JSON.parse(e.data)` without try/catch. The 7 unprotected locations are:
  - Line 44: `started` handler -- `JSON.parse(e.data)`
  - Line 59: `step` handler -- `JSON.parse(e.data)`
  - Line 83: `precondition` handler -- `JSON.parse(e.data)`
  - Line 110: `external_assertions` handler -- `JSON.parse(e.data)`
  - Line 126: `assertion` handler -- `JSON.parse(e.data)`
  - Line 147: `finished` handler -- `JSON.parse(e.data)`
  - Line 163: `error` handler -- `JSON.parse(e.data)`
  When the backend sends malformed JSON (e.g., partial write, serialization error in Pydantic, or a heartbeat comment leaking through), the exception propagates to the EventSource listener callback. EventSource internally catches listener exceptions, so the connection stays open, but the event is silently lost. The run state becomes inconsistent -- e.g., a missing `started` event means `run` stays null, causing all subsequent handlers to return `prev` unchanged (the `if (!prev) return prev` guard on lines 61, 112, 128, 149). This means one malformed event can cause the entire run stream to stop updating while the UI shows "connected."
- **Recommendation:** Wrap each `JSON.parse(e.data)` in try/catch. On failure, log to console and optionally show a toast. Continue processing subsequent events. Pattern:
  ```typescript
  let data
  try { data = JSON.parse(e.data) } catch { console.error('SSE parse error', e.data); return }
  ```

### [DD-USE-02] useRunStream.ts:36-37 -- isConnected state set true before EventSource connection established
- **Severity:** Medium
- **Category:** Correctness
- **Description:** In `connect()` at lines 36-37, `setIsConnected(true)` and `isConnectedRef.current = true` are called synchronously immediately after creating the `new EventSource(...)` constructor. There is no `eventSource.onopen` handler. The EventSource constructor initiates the connection asynchronously -- the HTTP request has not completed at this point. If the backend server is unreachable or returns an error status, the UI will show "connected" for potentially several seconds until `onerror` fires (line 180-186). The `onerror` handler only updates state if `readyState === EventSource.CLOSED`, but EventSource with default `withCredentials=false` auto-reconnects, meaning `readyState` will be `CONNECTING` (0) not `CLOSED` (2) during reconnection attempts. This means a temporarily unreachable server leaves the UI in a permanent "connected" state.
- **Recommendation:** Add `eventSource.onopen = () => { setIsConnected(true) }` to confirm connection after server acknowledgment. Keep the ref guard (`isConnectedRef.current = true`) at line 37 to prevent duplicate connect() calls, but remove the premature `setIsConnected(true)` at line 36. Also handle `readyState === CONNECTING` in onerror to set disconnected state during reconnection failures.

### [DD-USE-03] useRunStream.ts:74-78 -- Step handler does not deduplicate by index
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The `step` event handler (lines 58-80) appends every step to both `prev.steps` and `prev.timeline` using spread: `[...prev.steps, newStep]` and `[...prev.timeline, { type: 'step', data: newStep }]`. Unlike the `precondition` handler (lines 96-101) which uses `findIndex` to find existing entries by index and update them in-place, the `step` handler has no deduplication logic. If the backend sends two step events with `index: 3` (e.g., due to a retry in run_pipeline.py), the frontend will display duplicate entries. The precondition handler correctly handles this (lines 96-105), suggesting the step handler was not given the same treatment.
- **Recommendation:** Add deduplication logic similar to the precondition handler. Check if a step with the same index already exists in `prev.steps` and update it rather than appending.

### [DD-USE-04] useRunStream.ts:74-77 -- Steps and timeline arrays grow unbounded with O(n^2) copy cost
- **Severity:** Medium
- **Category:** Performance
- **Description:** Each step event creates new arrays via spread: `steps: [...prev.steps, newStep]` and `timeline: [...prev.timeline, { type: 'step', data: newStep }]`. For a 50-step test with 5 preconditions and 5 assertions, the timeline accumulates ~60 entries. Each append copies the entire array, making the total copy cost O(n^2) across all steps: 1+2+3+...+50 = 1,275 element copies for steps alone. Combined with React re-rendering the entire timeline on each update, this causes noticeable lag for long-running tests. The `precondition` handler uses `.map()` which is also O(n) per update but at least doesn't grow the array for duplicate updates.
- **Recommendation:** For long tests (50+ steps), consider using `useRef` for the mutable array and triggering a separate render via a version counter. Alternatively, use `immer` or a mutable-then-freeze pattern to avoid copying the entire array on each append.

### [DD-USE-05] useRunStream.ts:180-186 -- onerror handler does not handle all EventSource failure modes
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The `onerror` handler (line 180-186) only updates state when `readyState === EventSource.CLOSED`. However, EventSource enters three states: `CONNECTING` (0), `OPEN` (1), `CLOSED` (2). During a network interruption, EventSource auto-reconnects with `readyState = CONNECTING`. The handler ignores this state, leaving the UI showing "connected" during reconnection attempts. If the reconnection succeeds, this is fine, but if the server is permanently down, the UI never transitions to "disconnected" because EventSource never reaches `CLOSED` state during reconnection -- it stays in `CONNECTING` indefinitely. The user sees "connected" with no data flowing, with no indication that the connection is broken.
- **Recommendation:** Track the last event timestamp. If no event is received within a timeout (e.g., 60 seconds after the last heartbeat should have arrived), set isConnected to false and show a reconnection indicator. Alternatively, set a maximum reconnection attempt count and force-close the EventSource after exceeding it.

### [DD-USE-06] useRunStream.ts:198-206 -- useEffect cleanup race condition on runId change
- **Severity:** Low
- **Category:** Correctness
- **Description:** The main useEffect (lines 198-206) has dependency array `[autoConnect, runId]` with an `eslint-disable-next-line` comment. When `runId` changes, the cleanup function calls `disconnect()` which closes the EventSource. Then `connect()` runs with the new `runId`. However, `connect()` is a `useCallback` with `[runId]` dependency. Between the cleanup and the new effect, there is a render cycle where `connect` from the previous render (with old runId) is still the closure in scope. React guarantees that cleanup runs before the new effect, so the actual `connect()` call uses the new closure. The `eslint-disable` is technically safe here because `connect` is stable per runId, and the dependency on runId captures the relevant change. However, the eslint-disable comment should include a brief explanation of why it is safe.
- **Recommendation:** Add a comment explaining why the eslint-disable is safe: `// connect/disconnect are useCallback-wrapped with runId dependency, so runId change triggers re-creation`.

### [DD-USE-07] useRunStream.ts:45-56 -- started handler ignores task_name, uses client-side timestamp
- **Severity:** Low
- **Category:** Architecture
- **Description:** The `started` handler (lines 43-56) receives `{ run_id, task_id, task_name }` from the backend (SSEStartedEvent schema). It reads `data.task_id` but ignores `data.task_name` and `data.run_id`. It sets `started_at: new Date().toISOString()` instead of using any server-provided timestamp. This means the frontend's "started at" time reflects when the client received the event, not when the backend actually started the run. For slow networks, this could be seconds off from the actual start time.
- **Recommendation:** Consider using server-provided timing if accurate start time matters. At minimum, document that `started_at` is client-receipt time, not server-start time.

### [DD-USE-08] useRunStream.ts:147-158 -- finished handler ignores total_steps and duration_ms from backend
- **Severity:** Low
- **Category:** Architecture
- **Description:** The `finished` handler (lines 146-158) parses the event data and reads only `parsed.status`. The backend SSEFinishedEvent schema includes `total_steps` and `duration_ms` fields that the frontend ignores. These fields are computed and transmitted by the backend but never displayed. The frontend uses `run.steps.length` for step count and `new Date().toISOString()` for timing, losing the server-authoritative values.
- **Recommendation:** Store `total_steps` and `duration_ms` in the run state for potential display in the UI. The backend-computed `duration_ms` is more accurate than client-side timing.

### SSE Cross-Validation Detail (useRunStream.ts vs backend event_manager.py + run_pipeline.py)

| Frontend Listener | Line | Backend Publish | Backend Schema | Field Match |
|---|---|---|---|---|
| `started` | 43 | run_pipeline.py:512 | SSEStartedEvent{run_id, task_id, task_name} | Frontend reads task_id, ignores run_id and task_name |
| `step` | 58 | run_pipeline.py:420 | SSEStepEvent{index, action, reasoning, screenshot_url, status, duration_ms, step_stats} | Frontend reads index/action/reasoning/screenshot_url/status/duration_ms, ignores step_stats |
| `precondition` | 82 | run_pipeline.py:99,109 | SSEPreconditionEvent{index, code, status, error, duration_ms, variables} | Frontend reads all fields (typed as SSEPreconditionEvent). Backend sends two precondition events per index (running + final status), frontend correctly deduplicates |
| `external_assertions` | 109 | run_pipeline.py:267,334 | json.dumps summary dict | Frontend reads total/passed/failed/errors. Match confirmed. Error path (line 334) sends {type: 'error', message: str} which frontend does not handle (no `error` field access) |
| `assertion` | 125 | run_pipeline.py:219,258 | SSEAssertionEvent{assertion_id, assertion_name, assertion_type, status, message, actual_value, field_results} | Frontend reads all fields (typed as SSEAssertionEvent). Full match |
| `finished` | 146 | run_pipeline.py:467,123 | SSEFinishedEvent{status, total_steps, duration_ms} | Frontend reads status only, ignores total_steps and duration_ms |
| `error` | 161 | run_pipeline.py:573 | SSEErrorEvent{error: str} | Frontend reads parsed.error. Match confirmed |

**Frontend consumes all 7 backend event types. No missing listeners. No extra listeners.**

### [DD-USE-09] useRunStream.ts:109-123 -- external_assertions error-path format mismatch
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The backend has two publish paths for `external_assertions` events:
  - Normal path (run_pipeline.py:267): sends `{ total, passed, failed, errors, timestamp }` via `json.dumps(summary_event)`
  - Error path (run_pipeline.py:334): sends `{ type: 'error', message: str(e) }` via `json.dumps({'type': 'error', 'message': str(e)})`
  The frontend handler (lines 109-123) reads `data.total`, `data.passed`, `data.failed`, `data.errors` -- all of which will be `undefined` when the error-path payload arrives. The `?? 0` fallback handles this gracefully (total/failed/errors default to 0), but the user sees an assertion summary of "0 total, 0 passed, 0 failed" with no indication that an error occurred. The `message` field from the error path is silently ignored.
- **Recommendation:** Add a check for `data.type === 'error'` in the external_assertions handler. If the error type is detected, show an error toast with `data.message` and set assertion_summary to indicate an error state rather than all-zeros.

### client.ts (61 lines)

### [DD-CLI-01] client.ts:23-29 -- Content-Type header set to application/json for all requests including FormData
- **Severity:** High
- **Category:** Correctness
- **Description:** The `apiClient` function always sets `Content-Type: application/json` in headers (line 25), even when the request body is `FormData`. When sending `FormData` with `Content-Type: application/json`, the browser does not set the `multipart/form-data` boundary, causing the server to receive malformed data. The `...options?.headers` spread (line 26) allows callers to override, but no caller in the codebase explicitly overrides Content-Type for FormData requests. The task import endpoint (tasks.ts importExcel) sends FormData through apiClient. The correct behavior for FormData is to omit the Content-Type header entirely, letting the browser set `multipart/form-data` with the proper boundary.
- **Recommendation:** Detect FormData in the options body and conditionally omit the Content-Type header:
  ```typescript
  const isFormData = options?.body instanceof FormData
  const headers = { ...(!isFormData && { 'Content-Type': 'application/json' }), ...options?.headers }
  ```

### [DD-CLI-02] client.ts:41 -- No try/catch around response.json() for successful responses
- **Severity:** Medium
- **Category:** Correctness
- **Description:** Line 41 `return response.json()` is called after `response.ok` is confirmed, but there is no try/catch around it. If the server returns a 200 status with an empty body or non-JSON body, `response.json()` throws a `SyntaxError`. This error propagates to the outer catch block (line 42), which treats it as a network error and attempts retry. Since the response was successful (status 200), retrying will likely produce the same non-JSON response, burning all 3 retries before ultimately throwing. The `isNetworkError` check (line 44) correctly filters out `SyntaxError` (which is not a `TypeError`), so the retry is actually skipped and the generic toast fires. However, the error message shown to the user is the generic "请求失败，请稍后重试" rather than a meaningful message about the response being non-JSON.
- **Recommendation:** Wrap `response.json()` in a try/catch and throw an `ApiError` with a descriptive message if parsing fails.

### [DD-CLI-03] client.ts:44-49 -- Retry logic shows loading toast that can persist after success
- **Severity:** Medium
- **Category:** Correctness
- **Description:** When a network error occurs, a loading toast with id `'network-retry'` is shown (line 46). After successful retry, `toast.dismiss('network-retry')` is called on line 52, but only if the retry loop exhausts all retries and the error is not a network error or ApiError. If the retry succeeds on the second attempt (retries=2), the recursive call at line 49 returns successfully, and `toast.dismiss('network-retry')` on line 52 is never reached because execution returns from line 49 before reaching line 52. The loading toast remains visible after a successful retry.
- **Recommendation:** Move `toast.dismiss('network-retry')` to execute before the successful return on line 41, or restructure the retry logic to use a loop instead of recursion to ensure cleanup always runs.

### [DD-CLI-04] client.ts:48 -- Retry delay is linear (1s, 2s, 3s) not exponential
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 48 uses `await sleep(1000 * attempt)` where `attempt = MAX_RETRIES - retries + 1`. This produces delays of 1s, 2s, 3s -- which is linear, not exponential. The code comment in RESEARCH described this as "exponential backoff" but it is actually linear. True exponential backoff would be 1s, 2s, 4s (doubling). The distinction matters because linear backoff may not give the server enough recovery time on later retries.
- **Recommendation:** Either rename to "linear backoff" in documentation, or change to true exponential: `sleep(1000 * Math.pow(2, attempt - 1))` for 1s, 2s, 4s delays.

### [DD-CLI-05] client.ts:17-20 -- apiClient does not validate response structure against generic type T
- **Severity:** Low
- **Category:** Architecture
- **Description:** The function signature `apiClient<T>(endpoint, options, retries): Promise<T>` suggests type-safe responses, but `response.json()` returns `Promise<any>` which is implicitly cast to `T`. There is no runtime validation of the response structure. If the server returns a response that does not match the expected type, TypeScript will not catch this at compile time and there is no runtime check. This is a common pattern in TypeScript but worth noting for a code review.
- **Recommendation:** For critical API responses, consider using zod or io-ts schemas to validate the response at runtime. Low priority since this is a single-user tool with known backend API contracts.

### DataMethodSelector.tsx (829 lines)

**State variable count: 11 useState + 1 useMemo**
- `currentStep` (number) -- wizard step index, 0-3
- `methods` (DataMethodsResponse) -- API response data
- `loading` (boolean) -- API loading state
- `error` (string | null) -- API error state
- `searchQuery` (string) -- Step 1 search filter
- `selectedMethodKeys` (Set\<string\>) -- Step 1 multi-select
- `methodConfigs` (Map\<string, DataMethodConfig\>) -- Step 2 parameter configs
- `previewData` (unknown) -- Step 3 API execution result
- `previewLoading` (boolean) -- Step 3 execution loading
- `previewError` (string | null) -- Step 3 execution error
- `currentPreviewKey` (string | null) -- Step 3 which method is being previewed
- `expandedPanels` (Set\<string\>) -- collapsible class group panels
- `initialExpandDone` (boolean) -- one-time expand guard
- `filteredClasses` (useMemo) -- filtered methods from search

### [DD-DMS-01] DataMethodSelector.tsx:519-524 -- int/float parse converts empty string to 0
- **Severity:** Medium
- **Category:** Correctness
- **Description:** Lines 519-524 in the Step 2 parameter input onChange handler: when the user clears an int/float input, `parseInt('')` returns `NaN`, and the code converts it to `0` via `isNaN(parsed) ? 0 : parsed`. This means the user cannot distinguish between "intentionally set to 0" and "field is empty". When the input is empty, the user sees a `0` appear in the field (because `value` is bound to `config.parameters[param.name] ?? ''` and the stored value is now `0`). This creates a confusing UX where clearing a numeric field immediately fills it with 0.
- **Recommendation:** Store `NaN` or `undefined` for empty inputs, and display empty string when the value is `NaN`/`undefined`. Only convert to 0 at submission time.

### [DD-DMS-02] DataMethodSelector.tsx:92,321 -- `any` type usage in parameter value and config
- **Severity:** Medium
- **Category:** Architecture
- **Description:** Two `any` usages:
  - Line 92: `updateParameter(key: string, paramName: string, value: any)` -- the value parameter is typed as `any` because it can be string or number. Should be `string | number`.
  - Line 321: `const params: Record<string, any> = {}` -- initialized when creating method configs. Should be `Record<string, string | number>` to match the `DataMethodConfig.parameters` type definition.
  Both are flagged by ESLint `no-explicit-any` and should use a proper union type.
- **Recommendation:** Replace `any` with `string | number` at both locations.

### [DD-DMS-03] DataMethodSelector.tsx:161 -- no-useless-escape in regex
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 161 in `addExtraction`: `path.split(/[.\[\]]/).filter(Boolean)`. The `\[` and `\]` inside a character class `[...]` are unnecessary escapes -- `[` and `]` inside a character class are literal characters (except at the start/end position). ESLint flags this as `no-useless-escape`. The regex itself works correctly, but the escape is unnecessary.
- **Recommendation:** Change to `path.split(/[.\][]/).filter(Boolean)` to remove unnecessary escapes.

### [DD-DMS-04] DataMethodSelector.tsx:283,299 -- exhaustive-deps warnings in useEffect hooks
- **Severity:** Low
- **Category:** Correctness
- **Description:** Two useEffect hooks have missing dependencies:
  - Line 283 (expand-all effect): depends on `[methods.classes.length, initialExpandDone]` but uses `methods.classes.map(c => c.name)`. If a class name changes without changing the count, the panels won't re-expand. Low risk since class names are fetched from API and don't change between renders.
  - Line 299 (Escape key handler): depends on `[open]` but calls `handleCancel()` which references `onCancel`. If `onCancel` changes between renders (unlikely since it's typically a stable callback from parent), the handler calls a stale version. This is a common pattern but technically a stale closure.
- **Recommendation:** Add `methods.classes` to the expand-all effect dependencies. Add `handleCancel` (or `onCancel`) to the Escape key handler dependencies. Both are low risk in practice.

### [DD-DMS-05] DataMethodSelector.tsx:629-633 -- Lexical declarations in case block without braces
- **Severity:** Low
- **Category:** Architecture
- **Description:** Lines 629-633 (the `case 3:` block in `renderStepContent`) declare `const conflicts` and `const hasExtractions` inside a switch case without wrapping in a block `{}`. ESLint flags these as `no-case-declarations` because lexical declarations in case blocks can cause confusion about scope -- they're visible in subsequent cases. While this is a style issue not a correctness bug, it triggers 2 ESLint errors.
- **Recommendation:** Wrap the `case 3:` body in curly braces `{}` to create a block scope.

### [DD-DMS-06] DataMethodSelector.tsx:244-274 -- Modal open resets all state, discarding unsaved work
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The useEffect at lines 244-274 fires when `open` changes to `true` and unconditionally resets all state: step to 0, search, selections, configs, preview data, expanded panels. If the user accidentally closes the modal (e.g., clicking the backdrop at line 706) and reopens it, all work is lost. The `OperationCodeSelector` has the same pattern (line 44 resets selection), but that component has fewer steps of configuration.
- **Recommendation:** Either preserve state when modal closes (don't reset until explicit cancel), or add a confirmation dialog when closing with unsaved changes. At minimum, don't reset on re-open -- only reset on explicit Cancel.

### [DD-DMS-07] DataMethodSelector.tsx:128-152 -- Single preview state shared across multiple methods
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The Step 3 preview state (`previewData`, `previewLoading`, `previewError`, `currentPreviewKey`) is shared across all selected methods. When the user clicks "Preview Data" for method A, then clicks "Preview Data" for method B, method A's preview result is discarded. The UI only shows the preview for `currentPreviewKey`. If the user needs to see previews side-by-side or switch between methods, they must re-execute the API call each time. The `previewData` is stored as a single value rather than a Map keyed by method key.
- **Recommendation:** Store preview data in a Map keyed by method key, similar to how `methodConfigs` stores configurations. This allows the user to see the last preview for each method without re-executing.

### TaskForm.tsx (560 lines)

**State variable count: 12 useState + 1 useEffect**
- `formData` (FormData) -- main form state object with name, description, target_url, max_steps, preconditions, assertions, login_role
- `errors` (FormErrors) -- validation errors
- `selectorOpen` (boolean) -- OperationCodeSelector modal open
- `selectorIndex` (number | null) -- which precondition row is active for OperationCodeSelector
- `operationsLoading` (boolean) -- operations API loading
- `operationsAvailable` (boolean) -- operations API availability
- `operationsError` (string | null) -- operations API error
- `dataSelectorOpen` (boolean) -- DataMethodSelector modal open
- `dataSelectorIndex` (number | null) -- which precondition row is active for DataMethodSelector
- `dataMethodsLoading` (boolean) -- data methods API loading
- `dataMethodsAvailable` (boolean) -- data methods API availability
- `dataMethodsError` (string | null) -- data methods API error
- `assertionSelectorOpen` (boolean) -- AssertionSelector modal open

### [DD-TF-01] TaskForm.tsx:63-75 -- initialData useEffect does not reset on null/undefined
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The useEffect at lines 63-75 only runs when `initialData` is truthy. If the form is reused for a different task (e.g., switching from edit mode with a task to create mode with no task), the old form data persists because the effect does not fire when `initialData` becomes undefined. This means switching from "edit task A" to "create new task" leaves task A's data in the form. The form `mode` prop changes but is not checked.
- **Recommendation:** Add a reset branch when `initialData` is falsy. Alternatively, add `mode` to the dependency array and reset to defaults when mode is 'create'.

### [DD-TF-02] TaskForm.tsx:100-109 -- No double-submit prevention during loading
- **Severity:** Low
- **Category:** Correctness
- **Description:** The `handleSubmit` function (lines 100-109) calls `onSubmit(formData)` after validation. The submit button is disabled when `loading` is true (line 531), but the `loading` prop is controlled by the parent, not by the form itself. If the parent does not immediately set `loading=true` after receiving the call, or if there's a React render cycle delay, a rapid double-click could trigger `onSubmit` twice. The button has `disabled={loading}` which should prevent this if the parent synchronously sets loading, but there is no local submission-in-progress guard.
- **Recommendation:** Add a local `isSubmitting` ref or state that is set immediately in `handleSubmit` and checked before calling `onSubmit`.

### [DD-TF-03] TaskForm.tsx:134-152 -- Operations availability state persists across precondition rows
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The `operationsLoading`, `operationsAvailable`, and `operationsError` state variables are shared across all precondition rows. When the user clicks "选择操作码" for precondition row 1, the API call runs and sets `operationsAvailable`. If the API returns unavailable, ALL precondition rows show the disabled button and error message (lines 374-394). The availability check is done once and cached for the entire form lifetime, which is correct from an API perspective (the external module availability doesn't change per row), but the loading/error state is coupled to the row-specific action. If row 1's check fails, row 2's button is permanently disabled without the user ever clicking it.
- **Recommendation:** The availability check is appropriate as a shared concern. However, the loading spinner (line 383) should only show on the specific row that triggered the check, not on all rows. Track `selectorIndex` during loading to conditionally show the spinner only on the active row.

### [DD-TF-04] TaskForm.tsx:200-229 -- Data selector code generation duplicates TaskForm and DataMethodSelector logic
- **Severity:** Low
- **Category:** Architecture
- **Description:** The `handleDataSelectorConfirm` function (lines 200-229) generates Python code from DataMethodConfig by iterating over configs, building method call strings, and joining path segments. This same logic exists in DataMethodSelector.tsx `generateCode()` function (lines 223-241). Both functions produce identical Python code from the same DataMethodConfig input, violating DRY. If the code generation format changes, both must be updated.
- **Recommendation:** Extract the code generation logic into a shared utility function (e.g., `utils/codegen.ts:generateGetDataCode(configs: DataMethodConfig[]): string`) and call it from both locations.

### [DD-TF-05] TaskForm.tsx:369 -- Array index used as key in precondition list
- **Severity:** Low
- **Category:** Performance
- **Description:** Line 369: `{formData.preconditions.map((precondition, index) => (<div key={index}>...))}`. Using array index as key in a dynamic list where items can be removed (via `handleRemovePrecondition`) causes React to misassociate DOM elements with list items. When precondition 1 is removed, React updates the DOM for precondition 0 (which stays) and unmounts the last node, rather than removing the specific node. This can cause stale state in controlled textareas if the user is actively typing in a precondition when another is removed.
- **Recommendation:** Use a stable identifier for each precondition (e.g., a counter-based ID assigned at creation time).

### AssertionSelector.tsx (546 lines)

**State variable count: 8 useState + 2 useEffect + 1 useMemo**
- `methods` (AssertionMethodsResponse) -- API response data
- `loading` (boolean) -- API loading state
- `error` (string | null) -- API error state
- `searchQuery` (string) -- search filter
- `selectedKeys` (Set\<string\>) -- multi-select
- `expandedPanels` (Set\<string\>) -- collapsible class group panels
- `configs` (Map\<string, AssertionConfig\>) -- per-method configurations
- `fieldParamsMap` (Map\<string, Map\<string, {name, value}>>) -- field params per method
- `filteredClasses` (useMemo) -- filtered methods from search

### [DD-AS-01] AssertionSelector.tsx:276 -- exhaustive-deps warning: handleCancel missing from Escape key useEffect
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The Escape key handler useEffect (lines 263-276) depends on `[open]` but calls `handleCancel()` (line 268) which wraps `onCancel()`. If `onCancel` is a new function reference on each parent render, the handler captures a stale `onCancel`. In practice, React EventSource handles this correctly because the effect re-runs when `open` changes (which is the typical trigger for `onCancel` to become relevant). However, the ESLint warning is valid -- if the parent re-renders without `open` changing, the handler calls the old `onCancel`. Compare with OperationCodeSelector.tsx line 62 which correctly includes `onCancel` in dependencies.
- **Recommendation:** Add `handleCancel` (or directly `onCancel`) to the dependency array: `[open, handleCancel]`.

### [DD-AS-02] AssertionSelector.tsx:72-115 -- Nested setState calls in toggleMethod create inconsistent intermediate states
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The `toggleMethod` function (lines 72-115) calls `setSelectedKeys`, and inside its callback, also calls `setConfigs` and `setFieldParamsMap`. React batches state updates within event handlers, so these three setState calls trigger a single re-render. However, the `setConfigs` and `setFieldParamsMap` calls are nested inside `setSelectedKeys`'s callback, which means they access the `prev` state from `setSelectedKeys` rather than the current component state. While React batches these, the nesting makes the code harder to reason about and could lead to bugs if the state dependencies change. The `removeMethod` function (lines 118-135) correctly separates the three setState calls without nesting.
- **Recommendation:** Separate the three setState calls to be sequential at the top level of `toggleMethod`, similar to how `removeMethod` does it. Compute the new key first, then update all three states independently.

### [DD-AS-03] AssertionSelector.tsx:201-260 -- Modal open effect resets state even when initialConfigs provided
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The useEffect at lines 201-260 handles modal open. It fetches methods AND initializes state from `initialConfigs`. However, the dependency array is `[open, initialConfigs]`. If the parent re-renders while the modal is open (e.g., due to a state change in the parent), and `initialConfigs` is an inline array (e.g., `initialConfigs={task.assertions}`), the reference changes on every render, causing this effect to re-fire. This re-fetches methods and re-initializes state, potentially overwriting the user's current edits. The `open` dependency correctly gates the fetch, but `initialConfigs` reference instability could cause unexpected re-initialization.
- **Recommendation:** Either memoize `initialConfigs` in the parent, or use a ref to track whether initialization has already happened for the current open session.

### [DD-AS-04] AssertionSelector.tsx:150-162 -- updateParam stores number|string but parseInt converts empty to 0
- **Severity:** Low
- **Category:** Correctness
- **Description:** Similar to DD-DMS-01, the `updateParam` function (lines 150-162) calls `parseInt(e.target.value) || 0` at line 497. When the user clears a numeric input, `parseInt('')` returns `NaN`, and `|| 0` converts it to 0. The config type is `Record<string, number | string>`, so 0 is valid. The user sees "0" appear after clearing the field, which is confusing.
- **Recommendation:** Same as DD-DMS-01: store undefined/NaN for empty inputs, convert to 0 at submission time.

### [DD-AS-05] AssertionSelector.tsx:397-399 -- Split key by ':' assumes no colons in class/method names
- **Severity:** Low
- **Category:** Correctness
- **Description:** Lines 397-399 and 419-420: `const [className, methodName] = key.split(':')`. The key format is `${className}:${methodName}`. If a class name or method name contains a colon, `split(':')` would produce more than 2 segments, and the destructuring `[className, methodName]` would only capture the first two. The remaining segments would be silently lost, causing `getMethodInfo` to fail to find the method. In practice, Python class/method names cannot contain colons, so this is safe for the current use case, but the pattern is fragile.
- **Recommendation:** Use `split(':', 2)` or `split(':')` with `.slice(0, 2)` to make the intent explicit. This same pattern exists in DataMethodSelector.tsx lines 109, 318, 448, 479.

### [DD-AS-06] AssertionSelector.tsx:165-188 -- updateFieldParams calls setConfigs inside setFieldParamsMap callback
- **Severity:** Medium
- **Category:** Architecture
- **Description:** The `updateFieldParams` function (lines 165-188) nests `setConfigs` inside the `setFieldParamsMap` callback (line 173). This creates a two-level nested setState chain: `setFieldParamsMap(prev => { ... setConfigs(prevConfigs => { ... }) ... })`. The `updatedFieldParams` variable from the outer callback is used inside the inner callback, creating a closure dependency. While React batches these correctly, this pattern is fragile and hard to test. The field_params synchronization between `fieldParamsMap` (Map) and `configs.field_params` (Record) is redundant state that must be kept in sync manually.
- **Recommendation:** Derive `configs.field_params` from `fieldParamsMap` at confirm time (in `handleConfirm`) rather than keeping them synchronized in real-time. This eliminates the nested setState and the redundant state.

## P2 Findings

### types/index.ts (456 lines)

### [P2-TYP-01] types/index.ts:91,334,339,353 -- Four `any` type usages in SSE event and API request types
- **Severity:** Medium
- **Category:** Architecture
- **Description:** Four locations use `any` type, all flagged by ESLint `no-explicit-any`:
  - Line 91: `variables?: Record<string, any>` in `SSEPreconditionEvent` -- should be `Record<string, unknown>` since variable types are dynamic
  - Line 334: `params: Record<string, any>` in `ExecuteDataMethodRequest` -- should be `Record<string, string | number>` to match the backend's parameter types
  - Line 339: `data?: Array<Record<string, any>>` in `ExecuteDataMethodResponse` -- should be `Array<Record<string, unknown>>` since the response shape is dynamic
  - Line 353: `parameters: Record<string, any>` in `DataMethodConfig` -- should be `Record<string, string | number>` since parameters are user inputs of string or number type
- **Recommendation:** Replace all `any` with appropriate types. Use `unknown` for truly dynamic data and `string | number` for known union types.

### [P2-TYP-02] types/index.ts:91 vs backend schemas.py:51 -- TypeScript `SSEPreconditionEvent.variables` typed as `Record<string, any>` but backend sends `Optional[dict]`
- **Severity:** Low
- **Category:** Correctness
- **Description:** The frontend type declares `variables?: Record<string, any>` while the backend `SSEPreconditionEvent` schema uses `variables: Optional[dict]`. The types are compatible, but the `any` on the frontend side means any property access on `variables` is untyped. The backend can return nested dicts, arrays, or primitives as variable values, so `Record<string, unknown>` is more appropriate.
- **Recommendation:** Change to `Record<string, unknown>` and add type narrowing at usage sites.

### [P2-TYP-03] types/index.ts:42 -- RunStatus type does not include 'stopped' status used in RunList.tsx
- **Severity:** Medium
- **Category:** Correctness
- **Description:** `RunStatus` is defined as `'pending' | 'running' | 'success' | 'failed'` (line 42). However, `RunList.tsx` line 9 defines a `statusConfig` that includes a `'stopped'` status with label "已停止". At line 105, `run.status` is cast via `as keyof typeof statusConfig`, which would map `'stopped'` to the `stopped` config if the backend ever returns it. The backend `Run.status` field does not have a 'stopped' value in its current schema, but the frontend anticipates it. This is a type mismatch that TypeScript does not catch because of the cast.
- **Recommendation:** Either add `'stopped'` to the `RunStatus` type (if the backend can produce it) or remove the `'stopped'` entry from `statusConfig` (if it cannot).

### [P2-TYP-04] types/index.ts -- Task status type 'success' differs from backend which allows 'draft' | 'ready' | 'success' for read but 'draft' | 'ready' for write
- **Severity:** Low
- **Category:** Correctness
- **Description:** The `Task.status` type (line 11) is `'draft' | 'ready' | 'success'` which matches the backend `TaskResponse`. However, `UpdateTaskDto.status` (line 35) restricts to `'draft' | 'ready'`, matching the backend's `TaskUpdate.status` pattern `^(draft|ready)$`. The `success` status is set by the system, not by user updates. This is correctly modeled. No issue.
- **Recommendation:** No action needed. The types correctly reflect backend constraints.

### [P2-TYP-05] types/index.ts:45-60 -- Run interface mixes SSE-received data with frontend-computed data
- **Severity:** Low
- **Category:** Architecture
- **Description:** The `Run` interface includes `steps: Step[]`, `preconditions?: SSEPreconditionEvent[]`, `timeline: TimelineItem[]`, and `assertion_summary?`. These fields are assembled by `useRunStream` from individual SSE events, not received as a single response from the backend. The `Run` type is also used in `api/runs.ts` for `listRuns()` and `getRun()` which return persisted run data. The SSE-assembled Run and the API-returned Run may have different shapes (e.g., API returns `steps` with persisted data, SSE assembles `timeline` from events). This dual use of the same type is a potential source of confusion.
- **Recommendation:** Consider separating `SSEStreamRun` (built incrementally from events) from `APIRun` (returned from REST endpoints). The current approach works because the shared fields overlap sufficiently, but it conflates two different data sources.

### hooks/useTasks.ts (135 lines)

### [P2-HK-01] hooks/useTasks.ts:34 -- console.error violates coding-style.md
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 34: `console.error('Failed to fetch tasks:', error)` violates the project coding style rule against console.log statements. Should use toast or silent error handling.
- **Recommendation:** Replace with `toast.error('加载任务失败')` or remove the catch block and let the error propagate.

### [P2-HK-02] hooks/useTasks.ts:25-38 -- No AbortController for fetch cancellation on unmount
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The `fetchTasks` function (lines 25-38) does not use an AbortController. If the component unmounts while the fetch is in-flight (e.g., user navigates away quickly), the response will arrive and call `setTasks` and `setLoading` on an unmounted component. In React 18+ this does not cause a console warning, but it still performs unnecessary state updates and can cause issues with tests. The `useReports.ts` and `useDashboard.ts` hooks have the same pattern.
- **Recommendation:** Add an AbortController in the useEffect that calls fetchTasks, and abort on cleanup.

### [P2-HK-03] hooks/useTasks.ts:44-75 -- Client-side sorting of entire task list on every filter change
- **Severity:** Medium
- **Category:** Performance
- **Description:** The `filteredTasks` useMemo (lines 44-75) sorts the entire `tasks` array on every render when `tasks`, `sortBy`, or `sortOrder` change. The `tasks` array comes from the API call which returns ALL tasks without pagination (the API has no server-side pagination). For a task list of 100+ items, this sort runs on every filter change. The sort itself is O(n log n) but the real issue is that the API returns all tasks instead of paginating server-side.
- **Recommendation:** Add server-side pagination and sorting to the task list API. The client-side sort is fine for current scale (~50 tasks) but will degrade with more data.

### [P2-HK-04] hooks/useTasks.ts:96-101 -- batchDelete uses Promise.all without error handling per-item
- **Severity:** Low
- **Category:** Correctness
- **Description:** `batchDelete` (lines 96-101) calls `tasksApi.batchDelete(selectedIds)` which internally uses `Promise.all(ids.map(id => apiClient(...)))`. If one deletion fails, `Promise.all` rejects immediately and the remaining deletions are not attempted. The user sees an error but some tasks may already be deleted while others are not. The `selectedIds` are cleared regardless (line 99), so the user cannot easily retry the failed deletions.
- **Recommendation:** Use `Promise.allSettled` in `tasksApi.batchDelete` and report partial failures to the user.

### hooks/useReports.ts (93 lines)

### [P2-HK-05] hooks/useReports.ts:59 -- console.error violates coding-style.md
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 59: `console.error('Failed to fetch reports:', err)` violates coding style.
- **Recommendation:** Same as P2-HK-01 -- replace with toast or remove.

### [P2-HK-06] hooks/useReports.ts:34-63 -- No abort controller, fetch races with filter changes
- **Severity:** Medium
- **Category:** Correctness
- **Description:** When the user rapidly changes filters (e.g., switching status from 'all' to 'failed' to 'success'), each change triggers a new `fetchReports` call. Without an AbortController, the responses may arrive out of order. If the 'success' filter response arrives before the 'failed' filter response, the UI briefly shows the correct data then overwrites it with stale data from the 'failed' filter. The `filters` object is included in `fetchReports` dependency array (line 63), but the response handler does not verify that the response corresponds to the current filter state.
- **Recommendation:** Use an AbortController in the useEffect, aborting the previous fetch when filters change. Alternatively, add a request sequence counter and ignore stale responses.

### [P2-HK-07] hooks/useReports.ts:70-72 -- setPage(1) on filter change triggers redundant re-render
- **Severity:** Low
- **Category:** Performance
- **Description:** The `setPage(1)` call in the useEffect (lines 70-72) triggers when `filters` changes. This causes an additional re-render cycle: filter change -> render -> setPage(1) -> render -> fetchReports -> render. The page reset could be combined with the filter update in `updateFilter` (line 78) where `setPage(1)` is already called (line 79 in useTasks pattern), but useReports uses a separate useEffect instead.
- **Recommendation:** Move the `setPage(1)` call into the filter update path rather than using a separate useEffect, eliminating the redundant render.

### hooks/useDashboard.ts (43 lines)

### [P2-HK-08] hooks/useDashboard.ts:22 -- console.error violates coding-style.md
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 22: `console.error('Failed to fetch dashboard data:', err)` violates coding style.
- **Recommendation:** Same as P2-HK-01.

### [P2-HK-09] hooks/useDashboard.ts:35-41 -- refetch function creates new closures on every render
- **Severity:** Low
- **Category:** Performance
- **Description:** The `refetch` function (lines 35-41) is defined inline in the return object rather than using `useCallback`. A new function reference is created on every render. Any component receiving this refetch as a prop will re-render. Currently, no component passes refetch as a prop, so this is not an active issue.
- **Recommendation:** Wrap in `useCallback` for consistency with other hooks, or document that refetch is intentionally unstable.

### [P2-HK-10] All 4 manual-fetch hooks -- React Query installed but unused
- **Severity:** Medium
- **Category:** Architecture
- **Description:** All four data-fetching hooks (useTasks, useReports, useDashboard, useBatchProgress) use manual `useState + useEffect + fetch` pattern instead of React Query's `useQuery`. The project has `@tanstack/react-query` installed and `QueryClientProvider` configured in App.tsx. React Query provides automatic caching, stale-while-revalidate, retry, and refetch-on-window-focus out of the box. The manual hooks re-implement some of these features (e.g., useBatchProgress polling, useReports loading state) but miss others (no background refetch, no cache invalidation, no optimistic updates). CONVENTIONS.md claims the project uses "TanStack React Query (server state) + useState (local state)" but this is not reflected in the actual code.
- **Recommendation:** Migrate hooks to use React Query's useQuery/useMutation. This eliminates the manual loading/error state management, adds caching, and aligns with the documented architecture. Alternatively, remove the @tanstack/react-query dependency and update CONVENTIONS.md.

### hooks/useBatchProgress.ts (68 lines)

### [P2-HK-11] hooks/useBatchProgress.ts:65 -- eslint-disable on useEffect dependencies
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 65: `// eslint-disable-line react-hooks/exhaustive-deps` suppresses the warning about missing `loading` in the dependency array. The `loading` variable is used inside the effect (line 35) but is not in the dependency array `[batchId, refetchCounter]`. If `loading` changes from `true` to `false` without `batchId` or `refetchCounter` changing, the effect does not re-run and `loading` retains its stale value within the effect closure. This is safe because `loading` is only read for the conditional `setLoading(false)` which is idempotent, but the eslint-disable masks the dependency issue.
- **Recommendation:** Document why the eslint-disable is safe, or restructure to avoid referencing `loading` inside the effect.

### [P2-HK-12] hooks/useBatchProgress.ts:55-57 -- Interval starts before first fetch completes
- **Severity:** Low
- **Category:** Correctness
- **Description:** `fetchData()` is called at line 55, then `setInterval(fetchData, 2000)` starts at line 57 immediately after, without waiting for the initial fetch to complete. If the initial fetch takes longer than 2 seconds (unlikely but possible on slow networks), the interval fires before the first response arrives, causing concurrent fetches to the same endpoint. The `completedRef` guard prevents this after completion, but there is no guard for in-flight requests.
- **Recommendation:** Start the interval only after the initial fetch completes, using `await fetchData()` followed by `setInterval` in a try/finally block.

### pages/RunMonitor.tsx (132 lines)

### [P2-PG-01] pages/RunMonitor.tsx:24-28 -- set-state-in-effect auto-follows timeline, triggers on every timeline update
- **Severity:** Medium
- **Category:** Performance
- **Description:** The useEffect at lines 24-28 runs on every `run?.timeline?.length` change and calls `setViewIndex(run.timeline.length - 1)`. This is the "auto-follow latest step" feature. However, if the user manually clicks an earlier step (changing `viewIndex` via `handleTimelineItemClick` or `handleViewChange`), the next SSE event will override their selection and jump back to the latest step. The user cannot browse earlier steps while the run is in progress because every new event resets their position. Additionally, the ESLint `react-hooks/set-state-in-effect` rule flags line 26 because `setViewIndex` is called synchronously in the effect body rather than in an event handler.
- **Recommendation:** Add a "follow mode" flag that disables auto-scroll when the user manually selects a step. Re-enable follow mode when the user scrolls to the bottom or clicks a "follow latest" button.

### [P2-PG-02] pages/RunMonitor.tsx:38 -- console.error in task name fetch
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 38: `console.error('Failed to fetch task:', error)` violates coding style. The comment says "Keep default task name instead of crashing" which is a good fallback, but the console.error should be replaced.
- **Recommendation:** Remove the console.error or replace with a silent catch.

### [P2-PG-03] pages/RunMonitor.tsx:88 -- Complex inline filter expression for RunHeader currentStep count
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 88 computes `currentStep` for RunHeader using a complex inline expression: `run.timeline.filter(i => i.type === 'step' ? (i.data.status === 'success' || i.data.status === 'failed') : (i.data.status === 'success' || i.data.status === 'failed')).length`. This filter counts completed timeline items (steps, preconditions, and assertions all use the same status check). The duplicated ternary with identical branches `(i.data.status === 'success' || i.data.status === 'failed')` is unnecessary -- it could be simplified to `run.timeline.filter(i => i.data.status === 'success' || i.data.status === 'failed').length`. Also, this computation runs on every render without memoization.
- **Recommendation:** Simplify to `run.timeline.filter(i => i.data.status === 'success' || i.data.status === 'failed').length` and wrap in `useMemo` if performance matters.

### pages/TaskDetail.tsx (174 lines)

### [P2-PG-04] pages/TaskDetail.tsx:41,59,78,93 -- Four console.error statements violate coding-style.md
- **Severity:** Low
- **Category:** Architecture
- **Description:** Lines 41, 59, 78, 93 all contain `console.error('Failed to ...:', error)` for task loading, runs loading, stats loading, and run execution. Four violations in one file.
- **Recommendation:** Replace with toast.error for user-facing errors, or remove console.error for non-critical failures.

### [P2-PG-05] pages/TaskDetail.tsx:32-84 -- Three parallel useEffect hooks load data independently without coordination
- **Severity:** Medium
- **Category:** Architecture
- **Description:** Three separate useEffect hooks (lines 32-48, 50-66, 68-84) each independently load task data, runs, and stats. Each has its own loading state (`loading`, `runsLoading`, `statsLoading`). This means the page renders three times with incremental data, and the initial render shows three separate loading spinners. A coordinated approach (e.g., `Promise.all` in a single useEffect) would reduce render cycles and provide a single loading state. The current approach also makes three separate network requests that could potentially be batched.
- **Recommendation:** Consider using a single useEffect with `Promise.all` to load all data simultaneously, providing a unified loading state.

### pages/ReportDetail.tsx (114 lines)

### [P2-PG-06] pages/ReportDetail.tsx:17 -- set-state-in-effect ESLint error
- **Severity:** Low
- **Category:** Correctness
- **Description:** Line 17: `setLoading(true)` is flagged by `react-hooks/set-state-in-effect` as a synchronous setState in an effect. This is a common pattern for setting loading state before an async fetch. The ESLint rule flags it because effects should ideally not trigger re-renders synchronously. However, this is the standard pattern used throughout the codebase.
- **Recommendation:** This is a false positive in the ESLint rule for the standard loading pattern. Consider adding an eslint-disable comment with explanation, or restructuring to initialize loading state as true.

### [P2-PG-07] pages/ReportDetail.tsx:22 -- console.error violates coding-style.md
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 22: `console.error('Failed to fetch report:', err)` violates coding style.
- **Recommendation:** Same as P2-HK-01.

### [P2-PG-08] pages/ReportDetail.tsx:88-109 -- Legacy fallback creates inline objects without stable identity
- **Severity:** Low
- **Category:** Performance
- **Description:** When `timeline_items` is not available (lines 88-101), the code maps `data.steps` to create inline `ReportTimelineStep` objects. These objects are created fresh on every render because they are inside the JSX expression. Each object gets a `key` of `${item.type}-${item.id}` where `id` is `legacy-${idx}`, which is stable. The inline creation is fine for the fallback path since it only runs when `timeline_items` is absent, but the IIFE wrapper `(()) => { ... })()` in JSX is unusual.
- **Recommendation:** Extract the `displayItems` computation to a `useMemo` above the return statement for cleaner JSX and memoization.

### pages/RunList.tsx (156 lines)

### [P2-PG-09] pages/RunList.tsx:57 -- console.error violates coding-style.md
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 57: `console.error('Failed to fetch runs:', err)` violates coding style.
- **Recommendation:** Same as P2-HK-01.

### [P2-PG-10] pages/RunList.tsx:105 -- Type assertion on status with keyof typeof statusConfig
- **Severity:** Low
- **Category:** Correctness
- **Description:** Line 105: `run.status as keyof typeof statusConfig` casts `run.status` to one of the statusConfig keys. If the backend returns a status not in statusConfig (e.g., 'stopped'), the `|| statusConfig.pending` fallback handles it gracefully. However, the cast hides the type mismatch between `Run.status` (RunStatus) and the statusConfig keys (which include 'stopped').
- **Recommendation:** This is a symptom of P2-TYP-03. Fix the RunStatus type to include all possible statuses.

### pages/Dashboard.tsx (53 lines)

### [P2-PG-11] pages/Dashboard.tsx:7 -- useTasks() loads ALL tasks just for QuickStart selector
- **Severity:** Medium
- **Category:** Performance
- **Description:** Dashboard.tsx calls `useTasks()` at line 7 solely to get `allTasks` for the `QuickStart` component. This triggers a full task list API call (with no server-side pagination) on every Dashboard mount. The `useTasks` hook also computes sorting and pagination that Dashboard doesn't need. If there are 100+ tasks, this is wasteful.
- **Recommendation:** Create a lightweight `useTaskNames()` hook that only fetches task names and IDs for the QuickStart selector, or add a dedicated API endpoint for the QuickStart dropdown.

### pages/Tasks.tsx (211 lines)

### [P2-PG-12] pages/Tasks.tsx -- No significant issues found
- **Severity:** N/A
- **Category:** N/A
- **Description:** The Tasks page is well-structured with proper modal composition, confirmation dialogs, and state management. Uses `useTasks` hook correctly. Error handling uses toast for batch execution errors. No significant findings beyond the underlying hook issues documented above.
- **Recommendation:** No action needed.

### pages/BatchProgress.tsx (98 lines)

### [P2-PG-13] pages/BatchProgress.tsx:15 -- useBatchProgress called with batchId! non-null assertion
- **Severity:** Low
- **Category:** Correctness
- **Description:** Line 15: `useBatchProgress(batchId!)` uses the `!` non-null assertion on `batchId` which comes from `useParams`. If the route parameter is missing (e.g., navigating to `/batches/` without an ID), `batchId` is undefined and the hook will receive `undefined` instead of a string. The hook does not guard against undefined `batchId`, so the API call will fail with a malformed URL.
- **Recommendation:** Add a guard: `if (!batchId) return <Navigate to="/" />` before calling the hook, or add a guard inside the hook.

### pages/Reports.tsx (81 lines)

### [P2-PG-14] pages/Reports.tsx -- No significant issues found
- **Severity:** N/A
- **Category:** N/A
- **Description:** Clean implementation using `useReports` hook with proper filter handling and pagination. Error state includes retry button. No significant findings.
- **Recommendation:** No action needed.

### components/RunMonitor/StepTimeline.tsx (285 lines)

### [P2-CMP-01] StepTimeline.tsx:248 -- Array index used as key for timeline items
- **Severity:** Medium
- **Category:** Performance
- **Description:** Line 248: `key={index}` uses the array index as the React key for timeline items. When items are stable (appending only), index keys work correctly. However, if the timeline ever supports reordering, removal, or insertion, index keys cause React to misassociate DOM elements. For the current append-only pattern, this is safe but fragile. Combined with the fact that each timeline item has unique data (step index, precondition index, assertion_id), a stable key could be constructed.
- **Recommendation:** Use a composite key like `key={`${item.type}-${item.type === 'step' ? item.data.index : item.type === 'precondition' ? item.data.index : item.data.assertion_id}`}` for more stable identity.

### [P2-CMP-02] StepTimeline.tsx:171,194 -- Array index used as key for field_results
- **Severity:** Low
- **Category:** Performance
- **Description:** Lines 171 and 194: `key={idx}` for field result items. Field results are static (received once per assertion event, never reordered), so index keys are safe. However, if two field results have identical content, React may not distinguish them correctly during reconciliation.
- **Recommendation:** Use `key={fr.field_name || fr.name || idx}` for more stable identity.

### [P2-CMP-03] StepTimeline.tsx:46-285 -- No React.memo on StepTimeline component
- **Severity:** Medium
- **Category:** Performance
- **Description:** The `StepTimeline` component re-renders every time the parent `RunMonitor` re-renders, which happens on every SSE event (because `run` state changes). The component receives `items`, `currentStepIndex`, `onItemClick`, and `isRunning` as props. `items` is a new array reference on every SSE event (because useRunStream creates a new timeline via spread). Without `React.memo`, StepTimeline re-renders on every step, including re-rendering all existing timeline items. For a 50-step run, this means 50 timeline items re-render on every new step.
- **Recommendation:** Wrap StepTimeline in `React.memo`. For the `items` prop, consider passing a version counter or using a ref-based approach to avoid unnecessary re-renders.

### components/RunMonitor/ReasoningLog.tsx (64 lines)

### [P2-CMP-04] ReasoningLog.tsx:31 -- Array index used as key for step items
- **Severity:** Low
- **Category:** Performance
- **Description:** Line 31: `key={index}` for reasoning step divs. Steps are append-only, so index keys are safe for the current use case.
- **Recommendation:** Use `key={step.index}` for more stable identity, since step indices are unique.

### components/RunMonitor/ScreenshotPanel.tsx (130 lines)

### [P2-CMP-05] ScreenshotPanel.tsx:18 -- imageLoaded state not reset when steps change
- **Severity:** Low
- **Category:** Correctness
- **Description:** `imageLoaded` state (line 18) is initialized as `false` and set to `true` on `onLoad`. When the user navigates between steps via prev/next buttons, `setImageLoaded(false)` is correctly called (lines 29, 35). However, if a new step arrives via SSE while viewing the current step (because `currentViewIndex` hasn't changed but `steps[currentViewIndex]` is a new object with a different screenshot URL), the `onLoad` event won't fire for the old image, and `imageLoaded` stays `true` while the new image loads. The `src` attribute change should trigger a new load, but the transition effect (`opacity-0` to `opacity-100`) may flash.
- **Recommendation:** Add a `useEffect` that resets `imageLoaded` to `false` when the `steps[currentViewIndex]?.screenshot` URL changes.

### components/RunMonitor/RunHeader.tsx (60 lines)

### [P2-CMP-06] RunHeader.tsx -- No significant issues found
- **Severity:** N/A
- **Category:** N/A
- **Description:** Clean component with proper prop types. Inline style for progress bar width is acceptable for dynamic values. No significant findings.
- **Recommendation:** No action needed.

### components/Report/TimelineItemCard.tsx (247 lines)

### [P2-CMP-07] TimelineItemCard.tsx:32 -- API_BASE for screenshot URL computed inside component body
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 32: `const API_BASE = import.meta.env.VITE_API_BASE?.replace('/api', '') || 'http://localhost:11002'` is computed inside `StepExpandedContent`. This creates a new string on every render. The same computation exists in `api/reports.ts` line 82 as a module-level constant. The component should use the API module's constant rather than duplicating the URL construction logic.
- **Recommendation:** Export the `API_BASE_FOR_IMAGES` constant from `api/reports.ts` and import it in TimelineItemCard, or create a shared `config.ts` for API base URLs.

### [P2-CMP-08] TimelineItemCard.tsx:143,195 -- Array index used as key for field results
- **Severity:** Low
- **Category:** Correctness
- **Description:** Lines 143 and 195: `key={idx}` for field results. Same pattern as P2-CMP-02.
- **Recommendation:** Use `key={field.field_name || idx}` for more stable identity.

### components/TaskDetail/CodeViewerModal.tsx (175 lines)

### [P2-CMP-09] CodeViewerModal.tsx:123 -- "Retry" button reloads entire page instead of retrying the API call
- **Severity:** Medium
- **Category:** Correctness
- **Description:** Line 123: `<button onClick={() => window.location.reload()}>` reloads the entire page when code loading fails. This is poor UX -- the user loses their position and all state. The modal has access to `task.latest_run_id`, so it could retry `getRunCode(task.latest_run_id)` instead.
- **Recommendation:** Replace `window.location.reload()` with a retry function that calls `getRunCode(task.latest_run_id)` again, resetting `codeLoading` and `codeError` states.

### [P2-CMP-10] CodeViewerModal.tsx:48-67 -- Polling interval not cleared when execState changes away from waiting/running
- **Severity:** Low
- **Category:** Correctness
- **Description:** The polling useEffect (lines 48-67) creates a `setInterval` when `execState` is 'waiting' or 'running'. The cleanup function clears the interval when the effect re-runs or unmounts. However, if the component unmounts between the `execState` change (e.g., user closes the modal while polling) and the next effect execution, the interval is cleared by the cleanup. This is correctly handled by React's effect cleanup. No issue.
- **Recommendation:** No action needed. The cleanup pattern is correct.

### components/TaskList/TaskRow.tsx (140 lines)

### [P2-CMP-11] TaskRow.tsx:30 -- console.error in handleExecute
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 30: `console.error('Failed to start run:', error)` violates coding style. The error is silently swallowed -- the user sees no feedback when run execution fails from the task row.
- **Recommendation:** Replace with `toast.error('启动执行失败')` for user feedback.

### [P2-CMP-12] TaskRow.tsx:17-140 -- No React.memo on TaskRow component
- **Severity:** Medium
- **Category:** Performance
- **Description:** TaskRow is rendered in a list by TaskTable. When the parent re-renders (e.g., due to selection state change in a sibling row), all TaskRow instances re-render. Each TaskRow has a `handleExecute` async function that captures `task.id` in a closure. Without `React.memo`, every parent state change causes all rows to re-render and recreate their event handlers.
- **Recommendation:** Wrap TaskRow in `React.memo`. Extract `handleExecute` to a stable callback (passed from parent) to avoid closure recreation.

### api/tasks.ts (113 lines)

### [P2-API-01] api/tasks.ts:27-56 -- Import functions bypass apiClient for FormData, using raw fetch with hardcoded API_BASE
- **Severity:** Medium
- **Category:** Architecture
- **Description:** The `importPreview` and `importConfirm` functions (lines 29-56) bypass the `apiClient` wrapper and use raw `fetch` directly. They correctly handle FormData (not setting Content-Type). However, they duplicate error handling logic from apiClient and use a separate `IMPORT_API_BASE` constant (line 27) instead of the shared apiClient configuration. This means retry logic, toast notifications, and error formatting from apiClient are not applied to import operations.
- **Recommendation:** This is actually a workaround for DD-CLI-01 (client.ts always sets Content-Type: application/json for FormData). Once DD-CLI-01 is fixed, these functions can be migrated back to apiClient.

### [P2-API-02] api/tasks.ts:93-95 -- batchDelete sends parallel DELETE requests instead of a batch endpoint
- **Severity:** Low
- **Category:** Architecture
- **Description:** `batchDelete` (line 93) and `batchUpdateStatus` (line 97) send individual API requests per task via `Promise.all(ids.map(id => apiClient(...)))`. There is no batch delete/update API endpoint on the backend. For 50 selected tasks, this creates 50 concurrent HTTP requests. The backend has no rate limiting, so this works but is inefficient.
- **Recommendation:** Add batch API endpoints to the backend (DELETE /tasks/batch, PUT /tasks/batch/status) or use sequential requests with a concurrency limit.

### api/reports.ts (172 lines)

### [P2-API-03] api/reports.ts:82 -- API_BASE_FOR_IMAGES duplicated across reports.ts and TimelineItemCard.tsx
- **Severity:** Low
- **Category:** Architecture
- **Description:** The `API_BASE_FOR_IMAGES` constant (line 82) is duplicated in `TimelineItemCard.tsx` line 32 and `reports.ts` line 82. If the URL construction logic changes, both must be updated.
- **Recommendation:** Extract to a shared config module (e.g., `api/config.ts`).

### [P2-API-04] api/reports.ts:82 -- VITE_API_BASE env variable used inconsistently
- **Severity:** Low
- **Category:** Correctness
- **Description:** Line 82: `import.meta.env.VITE_API_BASE?.replace('/api', '') || 'http://localhost:11002'` strips '/api' from the env variable. Other files (runs.ts:33, tasks.ts:27) use `import.meta.env.VITE_API_BASE || 'http://localhost:11002/api'` with '/api' included. The inconsistency means `VITE_API_BASE` is expected to include '/api' in some files but not in others.
- **Recommendation:** Standardize the env variable meaning: either always include '/api' or never include it. Use a single shared config for the base URL.

### api/runs.ts (61 lines)

### [P2-API-05] api/runs.ts:44-53 -- getRunCode bypasses apiClient for plain text response
- **Severity:** Low
- **Category:** Architecture
- **Description:** `getRunCode` (lines 44-53) uses raw `fetch` instead of `apiClient` because the endpoint returns plain text (Python code), not JSON. It handles errors with `toast.error` and throws. This is a valid reason to bypass apiClient, but it duplicates the error handling pattern.
- **Recommendation:** Add a `apiClientText` variant that handles non-JSON responses, or document why raw fetch is used here.

### [P2-API-06] api/runs.ts:38 -- startRun labeled "Mock" but is the actual implementation
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 37-41: The comment says `// Mock: 启动执行 (保留向后兼容)` but the function calls `createRun` which is a real API call. The "Mock" label is misleading -- this is the production implementation.
- **Recommendation:** Remove the "Mock" label and update the comment to accurately describe the function.

### api/externalDataMethods.ts (38 lines)

### [P2-API-07] api/externalDataMethods.ts:26 -- `any` type for execute params
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 26: `params: Record<string, any> = {}` uses `any`. Should be `Record<string, string | number>` to match the type constraint in `DataMethodConfig.parameters`.
- **Recommendation:** Change to `Record<string, string | number>`.

### api/externalOperations.ts (24 lines)

### [P2-API-08] api/externalOperations.ts -- No significant issues found
- **Severity:** N/A
- **Category:** N/A
- **Description:** Clean API module with proper types and apiClient usage.
- **Recommendation:** No action needed.

### api/externalAssertions.ts (32 lines)

### [P2-API-09] api/externalAssertions.ts -- No significant issues found
- **Severity:** N/A
- **Category:** N/A
- **Description:** Clean API module with proper types and apiClient usage.
- **Recommendation:** No action needed.

### api/dashboard.ts (44 lines)

### [P2-API-10] api/dashboard.ts:39-42 -- Status type cast from string to union
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 41: `status: run.status as 'success' | 'failed' | 'running'` casts the API string response to the frontend union type. If the backend adds a new status, this cast silently passes it through without type checking.
- **Recommendation:** Add runtime validation or use a type guard for API responses.

### api/batches.ts (19 lines)

### [P2-API-11] api/batches.ts -- No significant issues found
- **Severity:** N/A
- **Category:** N/A
- **Description:** Clean API module with proper types and apiClient usage.
- **Recommendation:** No action needed.

### components/Report/StepItem.tsx (132 lines)

### [P2-CMP-13] StepItem.tsx -- No significant issues found
- **Severity:** N/A
- **Category:** N/A
- **Description:** Clean component with proper expand/collapse state, screenshot viewer, and reasoning display.
- **Recommendation:** No action needed.

### components/Report/ReportTable.tsx (92 lines)

### [P2-CMP-14] ReportTable.tsx -- No significant issues found
- **Severity:** N/A
- **Category:** N/A
- **Description:** Clean table component with proper status badges and navigation.
- **Recommendation:** No action needed.

## Final Summary Statistics

*Summary compiled: 2026-05-03*
*Includes findings from Plan 01 (breadth scan + ESLint/SSE cross-validation), Plan 02 (P1 deep-dive), Plan 03 (P2/P3 review)*

| Metric | Value |
|--------|-------|
| Total files reviewed | 87 |
| Total lines scanned | ~8,898 |
| ESLint issues | 18 (15 errors, 3 warnings) |
| TypeScript compilation errors | 0 |
| P1 files (deep-dive) | 5 |
| P2 files (quick scan) | 43 |
| P3 files (lint/type only) | 39 |
| **Critical issues** | **0** |
| **High issues** | **3** |
| **Medium issues** | **34** |
| **Low issues** | **58** |
| **Total actionable findings** | **95** |

### Findings by Priority Tier

| Tier | Files | Findings | Actionable | Description |
|------|-------|----------|------------|-------------|
| P1 | 5 | 37 | 37 | SSE core (useRunStream), HTTP client, oversized modal components |
| P2 | 43 | 56 | 48 | Pages, hooks, API modules, complex components |
| P3 | 39 | 11 | 3 | Shared components, simple API modules, utilities |

### Findings by Category

| Category | Count |
|----------|-------|
| Correctness | 41 |
| Architecture | 39 |
| Performance | 15 |
| Security | 0 |

### Findings by Layer

| Layer | Count |
|-------|-------|
| SSE Streaming (useRunStream.ts) | 9 |
| API Client (client.ts) | 5 |
| Task Modal Components (DataMethodSelector, TaskForm, AssertionSelector) | 18 |
| Page Components | 14 |
| Custom Hooks (4 hooks) | 12 |
| API Modules (8 files) | 11 |
| Types (index.ts) | 5 |
| Run Monitor Components (StepTimeline, ScreenshotPanel, RunHeader, ReasoningLog) | 6 |
| Report Components (TimelineItemCard, StepItem, ReportTable) | 4 |
| Other Components (TaskRow, CodeViewerModal) | 4 |
| SSE Cross-Validation | 5 |
| P3 Shared/Utility Components | 2 |

### Top 5 Findings (by severity + impact)

1. **[DD-USE-01] useRunStream.ts:44,59,83,110,126,147,163 -- All 7 JSON.parse calls lack try/catch protection.** A single malformed SSE event silently breaks the entire run stream because EventSource catches the listener exception internally, leaving the UI in an inconsistent state with no user feedback. (High/Correctness)

2. **[DD-CLI-01] client.ts:23-29 -- Content-Type header set to application/json for all requests including FormData.** The apiClient always sets Content-Type: application/json, breaking multipart form uploads. The task import endpoint works only because it bypasses apiClient with raw fetch. (High/Correctness)

3. **[SSE-3] useRunStream.ts -- All 7 JSON.parse calls in SSE handlers lack try/catch.** (Duplicate of DD-USE-01, confirmed from breadth scan.) Combined with DD-USE-02 (premature isConnected) and DD-USE-05 (onerror doesn't handle all failure modes), the SSE stream has the highest density of issues in the frontend. (High/Correctness)

4. **[P2-HK-10] All 4 manual-fetch hooks -- React Query installed but unused.** TanStack React Query is configured with QueryClientProvider but no hooks use useQuery/useMutation. All data fetching uses manual useState+useEffect+fetch, reimplementing caching and loading states. CONVENTIONS.md claims React Query is used, which is misleading. (Medium/Architecture)

5. **[DD-USE-04] useRunStream.ts:74-77 -- Steps and timeline arrays grow unbounded with O(n^2) copy cost.** Each step event copies the entire arrays via spread. Combined with missing React.memo on StepTimeline (P2-CMP-03), every step triggers re-rendering of all timeline items. Long-running tests (50+ steps) will cause noticeable UI lag. (Medium/Performance)

### Confirmed CONCERNS.md Issues

| CONCERNS.md Entry | Status | Finding Reference |
|-------------------|--------|-------------------|
| "No frontend tests" (Priority: Low) | **Confirmed** | No vitest/jest/mocha/@testing-library in package.json. Zero test files. |
| "DataMethodSelector 829 lines" | **Confirmed** | 7 findings (DD-DMS-01 through DD-DMS-07), including 5 ESLint errors and 2 dependency warnings |
| "main.tsx QueryClientProvider" | **Corrected -- in App.tsx** | SSE-3 cross-validation confirmed QueryClientProvider is in App.tsx, not main.tsx. CONTEXT.md was misleading. |
| "event_manager.py memory leak" (backend mirror) | **Confirmed** | DD-USE-04: timeline/steps arrays grow unbounded in useRunStream. Same pattern as backend EventManager._events. |

### New Issues Not in CONCERNS.md

1. **JSON.parse without try/catch in all SSE handlers** (High) -- 7 unprotected parse calls silently lose events on malformed data (DD-USE-01)
2. **FormData Content-Type header bug in apiClient** (High) -- breaks file upload, worked around by bypassing apiClient (DD-CLI-01)
3. **SSE connection state premature set** (Medium) -- isConnected set true before EventSource opens (DD-USE-02, SSE-2)
4. **Step handler does not deduplicate by index** (Medium) -- backend retries produce duplicate timeline entries (DD-USE-03)
5. **external_assertions error-path format mismatch** (Medium) -- frontend shows all-zeros summary on backend error (DD-USE-09)
6. **Retry toast persists after successful retry** (Medium) -- recursive retry logic skips toast.dismiss on success path (DD-CLI-03)
7. **TaskForm initialData does not reset on null** (Medium) -- edit-to-create switch leaves stale data (DD-TF-01)
8. **DataMethodSelector empty-to-0 conversion** (Medium) -- clearing numeric input shows 0 (DD-DMS-01)
9. **DataMethodSelector modal resets all state on close** (Medium) -- accidental close discards all configuration (DD-DMS-06)
10. **AssertionSelector initialConfigs reference instability** (Medium) -- inline array causes re-initialization (DD-AS-03)
11. **RunMonitor auto-follow overrides manual selection** (Medium) -- user cannot browse earlier steps during active run (P2-PG-01)
12. **Dashboard loads all tasks for QuickStart** (Medium) -- no lightweight API for dropdown data (P2-PG-11)
13. **console.error used in 9+ files** (Low) -- violates coding-style.md across useTasks, useReports, useDashboard, RunMonitor, RunList, TaskDetail, ReportDetail, TaskRow, QuickStart
14. **React Query gap: installed but unused** (Medium) -- 4 manual hooks should use useQuery (P2-HK-10)
15. **Missing React.memo on list components** (Medium) -- StepTimeline, TaskRow re-render on every parent update (P2-CMP-03, P2-CMP-12)
16. **No AbortController in fetch hooks** (Medium) -- unmounted component state updates, response race conditions (P2-HK-02, P2-HK-06)
17. **CodeViewerModal retry reloads entire page** (Medium) -- window.location.reload() instead of API retry (P2-CMP-09)

### Requirements Coverage

| Requirement ID | Description | Coverage |
|---------------|-------------|----------|
| CORR-03 | React component state management, event handling, data flow, SSE event processing | 41 Correctness findings across 87 frontend files |
| PERF-02 | Rendering performance, large list optimization, unnecessary re-renders, React Query cache strategy | 15 Performance findings covering missing React.memo/useMemo/useCallback, unbounded arrays, missing AbortController |

### Files Requiring No Further Review

The following files had no significant findings:
- **api/externalOperations.ts** (24 lines) -- clean, well-typed
- **api/externalAssertions.ts** (32 lines) -- clean, well-typed
- **api/batches.ts** (19 lines) -- clean, well-typed
- **pages/Tasks.tsx** (211 lines) -- well-structured with proper modal composition
- **pages/Reports.tsx** (81 lines) -- clean filter/pagination usage
- **components/RunMonitor/RunHeader.tsx** (60 lines) -- clean props and rendering
- **components/Report/StepItem.tsx** (132 lines) -- clean expand/collapse
- **components/Report/ReportTable.tsx** (92 lines) -- clean table rendering
- **All P3 shared/utility files** -- LoadingSpinner, StatCard, Layout, Sidebar, NavItem, Button, ConfirmModal, roleLabels, retry.ts, reasoningParser.ts, barrel index files

### Cross-Phase Correlation

| Phase 125/126 Finding | Phase 127 Frontend Mirror |
|----------------------|--------------------------|
| event_manager.py memory leak: _events dict grows without cleanup (125) | DD-USE-04: useRunStream timeline/steps arrays grow unbounded with O(n^2) spread copy cost |
| SSE stream missing try/except in event_generator (126, DD-runs-04) | DD-USE-01: All 7 JSON.parse calls in SSE handlers lack try/catch -- frontend mirror of backend error handling gap |
| Precondition failure skips "started" SSE event (125, P1) | DD-USE-07: started handler ignores task_name/run_id; if "started" event is skipped, frontend run stays null, all subsequent handlers return prev unchanged |
| Batch fire-and-forget in asyncio.create_task (126, DD-batch-01) | P2-HK-11/P2-HK-12: useBatchProgress polls with 2s interval, no abort on unmount, no guard against in-flight request overlap |
| client.ts retry is linear not exponential (127-02, DD-CLI-04) | N/A -- frontend-only finding with no backend mirror |
| PreSubmitGuard dead code (125) | N/A -- backend-only, no frontend mirror |

---

*Plan 01 breadth scan completed: 2026-05-03*
*Plan 02 P1 deep-dive completed: 2026-05-03*
*Plan 03 P2/P3 review completed: 2026-05-03*
*Final summary compiled: 2026-05-03*
