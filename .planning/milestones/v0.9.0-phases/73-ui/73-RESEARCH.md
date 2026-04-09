# Phase 73: 批量进度 UI - Research

**Researched:** 2026-04-09
**Domain:** Frontend React page with polling-based status updates
**Confidence:** HIGH

## Summary

Phase 73 builds a dedicated `/batches/:id` page that displays batch execution progress as a card grid. Each card shows a task's name, status badge, and elapsed time. The page polls `GET /batches/{id}` every 2 seconds, updating task statuses from "pending" through "running" to terminal states. Clicking a card navigates to the existing RunMonitor page (`/runs/:id`). When all tasks finish, a toast notification displays a summary.

The backend API is already fully implemented in Phase 72. The `GET /batches/{id}` endpoint returns `BatchResponse` with an embedded `runs` list (each with id, task_id, task_name, status). The frontend `batchesApi` client, `Batch`/`BatchRunSummary` types, and `BatchExecuteDialog` are also in place. The primary work is creating the new page component, wiring the route, and modifying `handleBatchExecute` to navigate after batch creation.

A known gap: `BatchRunSummary` currently lacks `started_at` and `finished_at` fields, so elapsed time display requires a backend schema extension (adding these two nullable datetime fields to the response). Alternatively, elapsed time can be computed client-side from the batch's `created_at` and the current poll time for running tasks.

**Primary recommendation:** Create `BatchProgress.tsx` as a standalone page with a `useBatchProgress` polling hook. Extend `BatchRunSummary` on the backend with `started_at`/`finished_at` for accurate timing. Use existing `StatusBadge` (already covers pending/running/success/failed states), `useNavigate` for card click navigation, and `sonner` toast for completion notification.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 独立页面 `/batches/:id`，不在 Tasks 页内嵌或用弹窗
- **D-02:** 批量执行启动后立即跳转到 `/batches/:id`，不等所有 run 创建完成
- **D-03:** 侧边栏导航不添加「批量进度」入口（通过跳转进入）
- **D-04:** 卡片布局，每个任务一张卡片，展示任务名称 + 状态标签 + 耗时
- **D-05:** 顶部显示整体进度统计（如「3/10 完成」），可能带进度条
- **D-06:** 4 种状态视觉样式：等待（灰色）、执行中（蓝色动画）、完成（绿色勾）、失败（红色叉）
- **D-07:** 点击卡片任意位置直接跳转到 `/runs/:id`，复用现有 RunMonitor 页面
- **D-08:** 全部任务完成时 Toast 通知 + 摘要（如「全部完成：8 成功，2 失败」）
- **D-09:** 轮询每 2 秒获取最新状态，全部完成后停止轮询

### Claude's Discretion
- 卡片的具体 UI 样式和间距
- 状态标签的动画效果
- 整体进度统计的展示形式（纯文字 vs 带进度条）
- 卡片排列方式（单列 vs 响应式多列）
- 加载态和空状态的处理

### Deferred Ideas (OUT OF SCOPE)
- 批量取消操作（BATCH-05）— v2 需求
- 批量重试失败任务（BATCH-06）— v2 需求
- 批量执行汇总报告（BATCH-04）— v2 需求
- 侧边栏添加「批量进度」导航入口 — v2
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| BATCH-03 | 用户可以在批量进度页面查看每个任务的状态（等待/执行中/完成/失败），点击可跳转到该任务的执行监控详情 | Backend API `GET /batches/{id}` already returns runs with status; new `BatchProgress.tsx` page with polling hook; card click navigates to `/runs/:id` |
</phase_requirements>

## Standard Stack

### Core (all already installed, no new dependencies)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| react-router-dom | 7.13.1 | Route config + `useNavigate` + `useParams` | Already used for all routing in the project |
| sonner | 2.0.7 | Toast notifications for batch completion | Already used project-wide (`toast` from sonner) |
| lucide-react | 0.577.0 | Icons (check, x, clock, loader) for status badges | Already used in all components |
| tailwindcss | 4.2.1 | Styling for cards, layout, animations | Project standard, all components use Tailwind |
| @tanstack/react-query | 5.90.21 | Available but NOT required -- polling uses setInterval | Listed for awareness; existing pattern uses raw `useEffect` + `setInterval` |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| setInterval polling | @tanstack/react-query refetchInterval | react-query adds complexity for a single-page polling case; project already uses raw `useEffect` + `setInterval` pattern in `useTasks` |
| SSE streaming | Polling | Already decided: polling only, SSE deferred to v2 |

**Installation:** No new packages needed. All dependencies already installed.

## Architecture Patterns

### Recommended File Structure
```
frontend/src/
├── pages/
│   ├── BatchProgress.tsx      # NEW - main page component
│   ├── Tasks.tsx              # MODIFY - navigate after batch create
│   └── RunMonitor.tsx         # EXISTING - navigation target (no changes)
├── hooks/
│   └── useBatchProgress.ts    # NEW - polling hook for batch status
├── components/
│   └── BatchProgress/
│       ├── BatchTaskCard.tsx   # NEW - individual task card
│       ├── BatchSummary.tsx    # NEW - top progress bar/stats
│       └── index.ts           # NEW - barrel export
├── api/
│   └── batches.ts             # EXISTING - may need field additions
├── types/
│   └── index.ts               # EXISTING - may need type field additions
└── App.tsx                    # MODIFY - add /batches/:id route
```

### Pattern 1: Polling Hook (useBatchProgress)
**What:** Custom hook that polls `batchesApi.getStatus()` every 2 seconds, stops when batch status is `completed`.
**When to use:** This is the core data fetching pattern for the batch progress page.
**Example:**
```typescript
// Based on existing useTasks.ts pattern (useEffect + fetch + state)
// and useRunStream.ts pattern (useCallback + useRef for lifecycle)

export function useBatchProgress(batchId: string) {
  const [batch, setBatch] = useState<Batch | null>(null)
  const [runs, setRuns] = useState<BatchRunSummary[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let intervalId: ReturnType<typeof setInterval> | null = null

    const fetchData = async () => {
      try {
        const data = await batchesApi.getStatus(batchId)
        setBatch(data)
        setRuns(data.runs ?? [])
        setLoading(false)

        // Stop polling when batch is completed
        if (data.status === 'completed' && intervalId) {
          clearInterval(intervalId)
          intervalId = null
        }
      } catch (error) {
        // Handle error per existing apiClient pattern
      }
    }

    fetchData()
    intervalId = setInterval(fetchData, 2000)

    return () => {
      if (intervalId) clearInterval(intervalId)
    }
  }, [batchId])

  return { batch, runs, loading }
}
```

### Pattern 2: Card Grid Layout
**What:** Responsive grid of clickable cards, each representing a batch run.
**When to use:** The main content area of the batch progress page.
**Example:**
```tsx
// Using Tailwind CSS grid, consistent with project's card patterns
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {runs.map(run => (
    <BatchTaskCard
      key={run.id}
      run={run}
      onClick={() => navigate(`/runs/${run.id}`)}
    />
  ))}
</div>
```

### Pattern 3: Navigation After Batch Create
**What:** Modify `handleBatchExecute` in Tasks.tsx to navigate to batch progress page after successful creation.
**When to use:** The entry point for users reaching the batch progress page.
**Example:**
```typescript
// Current code in Tasks.tsx:
//   await batchesApi.create(selectedIds, concurrency)
//   toast.success(`已启动 ${selectedIds.length} 个任务的批量执行`)
// Modified to capture batch ID and navigate:
const response = await batchesApi.create(selectedIds, concurrency)
navigate(`/batches/${response.id}`)
```

### Anti-Patterns to Avoid
- **Polling forever without cleanup:** Always clear the interval in useEffect cleanup AND when batch completes. Missing cleanup causes memory leaks if user navigates away.
- **Navigating away without stopping poll:** The useEffect cleanup function must clear the interval -- this is the primary mechanism, not manual stop.
- **Showing RunMonitor for pending tasks:** If a task is still "pending" (not started), clicking it navigates to RunMonitor which shows "connecting..." with no content. Consider showing a tooltip or disabled state on pending task cards.
- **Mutating state objects:** Per project coding rules, always create new objects (`{...prev, field: value}`), never mutate.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Toast notifications | Custom toast system | `sonner` `toast` (already installed) | Already used project-wide, consistent UX |
| Status badge rendering | Custom status component | `StatusBadge` from `components/shared` | Already handles pending/running/success/failed with correct colors |
| API error handling | Custom fetch wrapper | `apiClient` from `api/client.ts` | Has retry logic, error parsing, toast display |
| Route params | Manual URL parsing | `useParams` from react-router-dom | Type-safe param extraction |
| Programmatic navigation | window.location | `useNavigate` from react-router-dom | SPA navigation without page reload |

## Common Pitfalls

### Pitfall 1: Interval Not Cleared on Unmount
**What goes wrong:** If user navigates away from `/batches/:id` while polling is active, the interval continues firing API calls in the background.
**Why it happens:** Forgetting to return a cleanup function from useEffect, or not clearing interval when batch completes.
**How to avoid:** Always store intervalId in a variable and clear it in both the useEffect cleanup return AND when batch status reaches `completed`.
**Warning signs:** Network tab shows continuous requests after navigating away from the page.

### Pitfall 2: Stale Closure Over Batch Status
**What goes wrong:** The `fetchData` callback captures the initial batch status. When it later checks `data.status === 'completed'`, the interval may already be cleared by the cleanup function, or may not clear at all.
**Why it happens:** React closure captures the value at effect creation time.
**How to avoid:** Use a ref to track whether polling should stop, or check status inside the fetch callback and clear the interval directly (the pattern shown above is correct -- check `data.status` inside `fetchData` and clear `intervalId` there).

### Pitfall 3: BatchRunSummary Missing Timing Fields
**What goes wrong:** The UI wants to show elapsed time per task, but `BatchRunSummary` only has `id`, `task_id`, `task_name`, `status` -- no `started_at` or `finished_at`.
**Why it happens:** Backend schema was designed for minimal data transfer; timing fields were not included.
**How to avoid:** Either (a) extend the backend `BatchRunSummary` schema to include `started_at` and `finished_at`, or (b) compute elapsed time client-side from `Batch.created_at` for running tasks and show nothing for pending tasks. Option (a) is more accurate.
**Warning signs:** Cards show "0s" or no time for running tasks.

### Pitfall 4: Clicking Pending Task Shows Empty RunMonitor
**What goes wrong:** User clicks a "pending" task card, navigates to `/runs/:id`, but the run hasn't started yet. RunMonitor shows a loading spinner with "正在连接..." indefinitely because the SSE stream hasn't started.
**Why it happens:** RunMonitor's `useRunStream` hook connects to `EventSource` for the run, but the run backend hasn't started executing yet.
**How to avoid:** Either (a) disable click on pending tasks, (b) show a tooltip explaining the task hasn't started, or (c) let RunMonitor handle it (it already has a "正在连接..." state that is somewhat usable).
**Warning signs:** User sees an eternal loading spinner on RunMonitor for pending tasks.

### Pitfall 5: Batch Not Yet Populated with Runs
**What goes wrong:** Per D-02, the page navigates immediately after `batchesApi.create()` returns. But the backend creates the batch first, then creates runs. If the first poll happens before all runs are inserted, `runs` may be empty or partial.
**Why it happens:** Race condition between navigation and backend run creation.
**How to avoid:** The page should handle `runs` being an empty array gracefully (show "loading tasks..." state). The next poll 2 seconds later will have the full list. This is acceptable per D-02.
**Warning signs:** Page briefly shows "no tasks" before populating.

## Code Examples

### Backend Schema Extension (if timing fields needed)
```python
# backend/db/schemas.py - extend BatchRunSummary
class BatchRunSummary(BaseModel):
    """批量执行中的 Run 摘要"""
    id: str
    task_id: str
    task_name: Optional[str] = None
    status: str
    started_at: Optional[datetime] = None      # NEW
    finished_at: Optional[datetime] = None      # NEW
```

### Backend Route Update (to include timing fields)
```python
# backend/api/routes/batches.py - update run summary construction
run_summaries.append(BatchRunSummary(
    id=run.id,
    task_id=run.task_id,
    task_name=run.task.name if run.task else None,
    status=run.status,
    started_at=run.started_at,      # NEW
    finished_at=run.finished_at,    # NEW
))
```

### Frontend Type Update
```typescript
// frontend/src/types/index.ts - extend BatchRunSummary
export interface BatchRunSummary {
  id: string
  task_id: string
  task_name: string | null
  status: string
  started_at: string | null     // NEW
  finished_at: string | null    // NEW
}
```

### Status to RunMonitor Navigation
```typescript
// Already existing pattern in RunMonitor.tsx:
const navigate = useNavigate()
// Navigate to RunMonitor for run details
navigate(`/runs/${runId}`)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| SSE for batch progress | Polling every 2s | STATE.md decision | Simpler implementation, no multiplexer needed |
| react-router v6 patterns | react-router v7.13.1 | package.json | Same API for `useParams`, `useNavigate`, `Routes` -- no breaking changes for our usage |

**Deprecated/outdated:**
- None relevant. The stack is current.

## Open Questions

1. **Timing fields in BatchRunSummary**
   - What we know: `Run` model has `started_at`/`finished_at` in DB. `BatchRunSummary` schema omits them. CONTEXT.md mentions this gap.
   - What's unclear: Whether to extend the backend or compute client-side.
   - Recommendation: Extend backend schema. It is a minimal change (2 fields) and provides accurate timing. Client-side computation would be inaccurate for queued tasks.

2. **Pending task click behavior**
   - What we know: CONTEXT.md D-07 says "click card to navigate to /runs/:id". RunMonitor handles unstarted runs with "正在连接...".
   - What's unclear: Whether pending tasks should be clickable or disabled.
   - Recommendation: Make all cards clickable (per D-07). RunMonitor's loading state is acceptable for pending tasks. A "waiting to start" message could be added to RunMonitor in the future.

## Environment Availability

Step 2.6: SKIPPED (no external dependencies -- this phase only involves frontend React code changes and a minor backend schema extension, using only already-installed packages)

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | No frontend test framework installed |
| Config file | None |
| Quick run command | `cd frontend && npm run build` (type-check + build) |
| Full suite command | `cd backend && uv run pytest backend/tests/ -v` (backend only) |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| BATCH-03 | Batch progress page displays task statuses | manual-only | -- | No frontend test infra |
| BATCH-03 | Page polls every 2s and updates status | manual-only | -- | No frontend test infra |
| BATCH-03 | Click task card navigates to RunMonitor | manual-only | -- | No frontend test infra |
| BATCH-03 | Toast on batch completion | manual-only | -- | No frontend test infra |
| BATCH-03 | Backend BatchRunSummary includes timing fields | unit | `uv run pytest backend/tests/unit/test_batch_api.py -x` | Partially (test_batch_api.py exists) |

### Sampling Rate
- **Per task commit:** `cd frontend && npm run build` (type safety check)
- **Per wave merge:** `uv run pytest backend/tests/ -v` + `npm run build`
- **Phase gate:** Manual verification: navigate to Tasks, select tasks, batch execute, verify progress page works

### Wave 0 Gaps
- No frontend test framework -- all frontend validation is manual + TypeScript type checking via `npm run build`
- Backend: existing `test_batch_api.py` may need test cases for extended schema fields

## Sources

### Primary (HIGH confidence)
- Code reading: `frontend/src/api/batches.ts` -- verified API client methods
- Code reading: `frontend/src/types/index.ts` -- verified Batch/BatchRunSummary types
- Code reading: `backend/api/routes/batches.py` -- verified GET /batches/{id} returns runs
- Code reading: `backend/db/schemas.py` -- verified BatchRunSummary lacks timing fields
- Code reading: `backend/db/models.py` -- verified Run model has started_at/finished_at
- Code reading: `frontend/src/components/shared/StatusBadge.tsx` -- verified status coverage
- Code reading: `frontend/src/pages/Tasks.tsx` -- verified handleBatchExecute flow
- Code reading: `frontend/src/pages/RunMonitor.tsx` -- verified navigation target
- Code reading: `frontend/src/App.tsx` -- verified route structure
- Code reading: `frontend/package.json` -- verified all dependencies installed

### Secondary (MEDIUM confidence)
- `.planning/STATE.md` -- project decisions (polling every 2s, Semaphore limits)
- `.planning/REQUIREMENTS.md` -- BATCH-03 requirement definition

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - all dependencies already installed and verified in package.json
- Architecture: HIGH - existing patterns (useTasks polling, StatusBadge, apiClient) are well-established
- Pitfalls: HIGH - identified from code analysis of existing hooks and schemas

**Research date:** 2026-04-09
**Valid until:** 2026-05-09 (stable frontend patterns, no fast-moving dependencies)
