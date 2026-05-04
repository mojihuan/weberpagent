# Phase 127: Frontend Review - Research

**Researched:** 2026-05-03
**Domain:** React frontend correctness and performance review
**Confidence:** HIGH

## Summary

Phase 127 reviews the React frontend codebase (~60 files, ~8,900 lines) for correctness (CORR-03) and rendering performance (PERF-02). This is a review-only phase producing findings without code changes. The frontend consists of 8 page components, ~30 sub-components, 5 custom hooks, 9 API modules, and a centralized types file.

The critical review targets are: (1) `useRunStream.ts` -- the SSE hook that consumes real-time execution events from the backend, which has multiple known edge-case risks (no JSON.parse error handling, no auto-reconnect, timeline array unbounded growth); (2) three oversized components (DataMethodSelector 829 lines, TaskForm 560 lines, AssertionSelector 546 lines) with complex internal state management; (3) the `api/client.ts` HTTP client with its retry and error handling logic.

ESLint scan already reveals 18 problems (15 errors, 3 warnings) including `any` type usage, missing hook dependencies, and a `set-state-in-effect` anti-pattern. TypeScript compilation is clean (no errors). Cross-validation with the backend `event_manager.py` and `run_pipeline.py` confirms the SSE event format uses `event: <type>\ndata: <json>\n\n` which matches the frontend's `addEventListener` approach.

**Primary recommendation:** Follow the 3-plan structure (Plan 1: breadth scan + ESLint/TS, Plan 2: P1 deep-dive on 5 files, Plan 3: P2/P3 scan + summary). The SSE cross-validation with backend event_manager is the highest-value activity.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Files ranked by risk into 3 priority levels:
  - P1 (deep line-by-line): useRunStream.ts, DataMethodSelector.tsx, TaskForm.tsx, AssertionSelector.tsx, client.ts
  - P2 (quick scan): pages/*.tsx, types/index.ts, StepTimeline.tsx, TaskRow.tsx, ImportModal/*.tsx, other TaskModal/*.tsx, Report/*.tsx, RunMonitor/*.tsx
  - P3 (lint/type check only): shared/*.tsx, Dashboard/*.tsx, constants/*, utils/*, simple API modules
- **D-02:** useRunStream.ts (215 lines) gets deep review covering: JSON.parse without try/catch, event ordering (step before started), duplicate events (step no dedup), disconnect/reconnect (isConnectedRef state desync), timeline array unbounded growth
- **D-03:** Cross-validate with backend event_manager.py -- confirm frontend-expected event format matches backend-pushed format, verify event type and data structure alignment
- **D-04:** Static code analysis only, no runtime performance testing. Identify: missing React.memo/useMemo/useCallback, large lists without virtualization, React Query misconfiguration, too-coarse state updates, unnecessary re-renders
- **D-05:** Focus on 3 oversized components (DataMethodSelector 829 lines, TaskForm 560 lines, AssertionSelector 546 lines) for internal state management and component splitting rationality
- **D-06:** Follow Phase 125/126 "breadth-first + focused deep-dive" strategy: Plan 1 breadth scan all files + ESLint/TS check, Plan 2 P1 deep review, Plan 3 P2/P3 review + summary
- **D-07:** Findings output to `127-FINDINGS.md`, continuing Phase 125/126 4-level severity (Critical/High/Medium/Low) and category labels (Correctness/Architecture/Performance/Security)

### Claude's Discretion
- Specific risk scoring criteria during breadth scan
- Threshold for escalating P2 file findings to deep review
- Specific ESLint/TypeScript check commands and configuration

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CORR-03 | Review React component state management, event handling, data flow, SSE event processing | useRunStream.ts (215 lines) analyzed with 6 event handlers, all JSON.parse without try/catch; 3 oversized components analyzed with state management patterns; SSE cross-validation with backend event_manager.py completed |
| PERF-02 | Review rendering performance, large list optimization, unnecessary re-renders, React Query cache strategy | ESLint reveals set-state-in-effect anti-pattern in 2 files; no React.memo found in component analysis; client-side pagination in useTasks handles only pageSize=10; useBatchProgress uses polling (2s interval); React Query configured with refetchOnWindowFocus:false only |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| React | 19.2.0 | UI framework | Latest stable, concurrent features available |
| React Router DOM | 7.13.1 | Client routing | v7 with data APIs |
| TanStack React Query | 5.90.21 | Server state caching | Industry standard for async state |
| Vite | 7.3.1 | Build tool | Fast HMR, native ESM |
| TypeScript | ~5.9.3 | Type safety | strict mode enabled |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Tailwind CSS | 4.2.1 | Utility CSS | All component styling |
| sonner | 2.0.7 | Toast notifications | API error feedback |
| recharts | 3.8.0 | Chart library | Dashboard visualizations |
| lucide-react | 0.577.0 | Icon library | UI icons |
| react-syntax-highlighter | 16.1.1 | Code display | Report/test views |

### Frontend Tooling
| Tool | Version | Purpose |
|------|---------|---------|
| ESLint | 9.39.1 | Linting with typescript-eslint 8.48.0 |
| typescript-eslint | 8.48.0 | TypeScript-specific lint rules |
| react-hooks plugin | bundled | Hook dependency and rules enforcement |

**Version verification:**
```
React 19.2.0, React Router DOM 7.13.1, TanStack React Query 5.90.21, Vite 7.3.1, TypeScript ~5.9.3
```

## Architecture Patterns

### Frontend Project Structure
```
frontend/src/
  main.tsx              -- React root (StrictMode + Toaster, NO QueryClientProvider here)
  App.tsx               -- Router + QueryClientProvider (QueryClient defined here)
  pages/                -- 8 page-level components
  components/           -- ~30 sub-components in feature directories
  hooks/                -- 5 custom hooks (useRunStream, useTasks, useReports, useDashboard, useBatchProgress)
  api/                  -- 9 API modules (client.ts + per-domain)
  types/index.ts        -- 456 lines, all TypeScript interfaces
  constants/            -- roleLabels.ts
  utils/                -- reasoningParser.ts, retry.ts
```

### Pattern 1: SSE Streaming (useRunStream)
**What:** EventSource connects to `GET /api/runs/{run_id}/stream`, listens for typed events via `addEventListener`
**When to use:** Real-time run execution monitoring
**Backend format:** `event: <type>\ndata: <json>\n\n`
**Frontend listeners:** started, step, precondition, assertion, external_assertions, finished, error

```typescript
// Backend publishes (run_pipeline.py):
await event_manager.publish(run_id, f"event: step\ndata: {event.model_dump_json()}\n\n")

// Frontend consumes (useRunStream.ts):
eventSource.addEventListener('step', (e: MessageEvent) => {
  const stepData = JSON.parse(e.data)  // No try/catch
  setRun(prev => ({ ...prev, steps: [...prev.steps, newStep], timeline: [...] }))
})
```

### Pattern 2: Custom Hooks for Data Fetching
**What:** useState + useCallback + useEffect pattern (NOT using React Query's useQuery)
**When to use:** Tasks, Reports, Dashboard data
**Key insight:** Despite having React Query installed, most hooks use manual fetch patterns with useState/useEffect. Only the QueryClient configuration exists in App.tsx but no `useQuery`/`useMutation` calls were found in the codebase.

### Pattern 3: Component-Modal Composition
**What:** TaskForm renders OperationCodeSelector, DataMethodSelector, AssertionSelector as child modals
**When to use:** Task creation/editing with complex sub-workflows
**State flow:** Parent passes open/onConfirm/onCancel props; child manages its own internal multi-step state

### Anti-Patterns to Avoid
- **set-state-in-effect:** ESLint flagged `setViewIndex(run.timeline.length - 1)` inside useEffect in RunMonitor.tsx and CodeViewerModal.tsx -- causes cascading renders
- **No React Query usage:** QueryClientProvider is configured but hooks use manual useState+useEffect+fetch -- the React Query dependency adds bundle size without benefit
- **Array index as key:** StepTimeline uses `key={index}` for timeline items -- can cause incorrect rendering when items are reordered or updated

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| SSE reconnection | Custom reconnect logic in useRunStream | EventSource built-in reconnect or react-sse library | EventSource auto-reconnects by default; custom logic risks race conditions |
| Data fetching + caching | useState + useEffect + manual fetch | React Query useQuery/useMutation | Already installed (5.90.21) but unused; provides cache, stale-while-revalidate, refetch, error handling |
| Large list rendering | Full DOM for all items | react-window or similar | For lists over 100 items; current task list is client-paginated (pageSize=10) so not urgent |

**Key insight:** The codebase has React Query installed and configured but uses manual fetch patterns everywhere except possibly internal React Query features. This is a gap between declared architecture (CONVENTIONS.md says "server state: @tanstack/react-query") and actual implementation.

## Common Pitfalls

### Pitfall 1: JSON.parse Without try/catch in SSE Handlers
**What goes wrong:** If backend sends malformed JSON or connection drops mid-event, `JSON.parse(e.data)` throws uncaught exception
**Why it happens:** All 7 event handlers in useRunStream.ts parse without protection
**How to avoid:** Wrap all JSON.parse calls in try/catch; on failure, log and skip the event
**Warning signs:** Runtime error crashes the SSE listener; EventSource may auto-reconnect but state is inconsistent

### Pitfall 2: isConnectedRef Desync with State
**What goes wrong:** `isConnectedRef.current` is set to true in `connect()` before the EventSource actually connects. If connection fails, `isConnected` state says true but EventSource is in CONNECTING state.
**Why it happens:** connect() sets both ref and state synchronously at call start (line 36-37), not on EventSource open event
**How to avoid:** Set connected state only after EventSource fires `open` event, not on connect() call
**Warning signs:** UI shows "connected" but no events arrive; no `open` event listener exists

### Pitfall 3: Timeline Array Unbounded Growth
**What goes wrong:** `run.timeline` grows by appending every step, precondition, and assertion event. For long-running tests (50+ steps), this creates a large array that is spread on every update (`[...prev.timeline, newItem]`)
**Why it happens:** No size limit or cleanup on the timeline array
**How to avoid:** Cap timeline size or use a ring buffer; memoize timeline rendering
**Warning signs:** Browser memory grows linearly during long test runs; StepTimeline renders slow down

### Pitfall 4: Missing EventSource `open` Event Handler
**What goes wrong:** There is no `onopen` handler on the EventSource. The frontend assumes connection succeeds immediately.
**Why it happens:** connect() optimistically sets isConnected=true before SSE connection is established
**How to avoid:** Add `eventSource.onopen` handler to confirm connection
**Warning signs:** isConnected shows true when server is down

### Pitfall 5: useEffect Cleanup Race with EventSource
**What goes wrong:** When runId changes, the useEffect cleanup calls disconnect(), but the new connect() may fire before cleanup completes if React batches the effect
**Why it happens:** useEffect deps are `[autoConnect, runId]` with eslint-disable comment, suggesting the dependency was intentionally restricted
**How to avoid:** Use a ref to track the "current runId" and ignore events from stale connections
**Warning signs:** Events from a previous run appear in the new run's state

### Pitfall 6: set-state-in-effect Anti-pattern
**What goes wrong:** ESLint's `react-hooks/set-state-in-effect` rule flags direct setState calls inside useEffect bodies that cause cascading renders
**Why it happens:** RunMonitor.tsx line 26 calls `setViewIndex(run.timeline.length - 1)` in effect; CodeViewerModal.tsx line 26 calls `setCodeLoading(false)` in effect
**How to avoid:** Derive viewIndex from run.timeline.length using useMemo, or use useRef for imperative values
**Warning signs:** Double renders on every timeline update

### Pitfall 7: Custom Hook Not Using React Query
**What goes wrong:** useTasks, useReports, useDashboard all implement manual fetch+loading+error state instead of using React Query's useQuery hook
**Why it happens:** React Query is installed and QueryClientProvider configured, but hooks were written before React Query adoption or without knowledge of its API
**How to avoid:** Use useQuery for data fetching, useMutation for mutations -- eliminates useState for loading/error, automatic cache management
**Warning signs:** Loading/error state boilerplate repeated in every hook; no cache invalidation strategy

## Code Examples

### SSE Event Format Cross-Validation

Backend publishes (from run_pipeline.py):
```python
# started event
started = SSEStartedEvent(run_id=run_id, task_id=task_id, task_name=task_name)
await event_manager.publish(run_id, f"event: started\ndata: {started.model_dump_json()}\n\n")

# step event
await event_manager.publish(run_id, f"event: step\ndata: {event.model_dump_json()}\n\n")

# finished event
finished = SSEFinishedEvent(status=final_status, total_steps=step_count, duration_ms=0)
await event_manager.publish(run_id, f"event: finished\ndata: {finished.model_dump_json()}\n\n")
```

Frontend consumes (from useRunStream.ts):
```typescript
eventSource.addEventListener('started', (e: MessageEvent) => {
  const data = JSON.parse(e.data)  // expects { run_id, task_id, task_name }
})

eventSource.addEventListener('step', (e: MessageEvent) => {
  const stepData = JSON.parse(e.data)  // expects { index, action, reasoning, screenshot_url, status, duration_ms }
})
```

**Mismatch note:** Backend `SSEStartedEvent` includes `task_name` field, but frontend `started` handler accesses `data.task_id` (which is present) and does NOT use `task_name`. The frontend also uses `new Date().toISOString()` for `started_at` instead of any timestamp from the backend event. This is not a bug but a data loss -- the backend-provided timing is ignored.

### React Query Configuration (App.tsx)
```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
  },
})
```

**Note:** Only `refetchOnWindowFocus: false` is configured. No `staleTime`, `gcTime`, or retry settings are customized. Despite being configured, no hooks actually use `useQuery`/`useMutation`.

### Manual Fetch Pattern (useTasks.ts)
```typescript
export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(false)

  const fetchTasks = useCallback(async () => {
    setLoading(true)
    try {
      const data = await tasksApi.list({ status: filters.status, search: filters.search })
      setTasks(data)
    } catch (error) {
      console.error('Failed to fetch tasks:', error)
    } finally {
      setLoading(false)
    }
  }, [filters.status, filters.search])

  useEffect(() => { fetchTasks() }, [fetchTasks])
}
```

### Polling Pattern (useBatchProgress.ts)
```typescript
useEffect(() => {
  let intervalId: ReturnType<typeof setInterval> | null = null
  const fetchData = async () => { /* fetch batch status */ }
  fetchData()
  if (!completedRef.current) {
    intervalId = setInterval(fetchData, 2000)
  }
  return () => { if (intervalId) clearInterval(intervalId) }
}, [batchId, refetchCounter])
```

**Note:** Polling every 2 seconds until batch completes. Could use React Query's `refetchInterval` option instead.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| React 18 | React 19.2 | 2024-2025 | Concurrent features, improved ref handling |
| React Query v4 | React Query v5 | 2023 | `useQuery` API simplified, `gcTime` replaces `cacheTime` |
| ESLint 8 | ESLint 9 flat config | 2024 | New config format, better plugin resolution |
| React Router v6 | React Router v7 | 2024 | Data APIs, framework mode available |
| Tailwind CSS v3 | Tailwind CSS v4 | 2024 | `@import "tailwindcss"` syntax, `@tailwindcss/vite` plugin |

**Deprecated/outdated:**
- None critical -- all dependencies are current major versions

## Open Questions

1. **React Query unused?**
   - What we know: QueryClientProvider configured in App.tsx, but all hooks use manual useState+useEffect+fetch pattern. CONVENTIONS.md claims React Query is used for server state.
   - What's unclear: Whether React Query was ever used and removed, or was installed but never adopted.
   - Recommendation: Document this as a finding. The gap between documentation and implementation is itself a maintainability concern.

2. **EventSource auto-reconnect behavior**
   - What we know: useRunStream.ts has no explicit reconnect logic. EventSource has built-in reconnection but the frontend does not handle reconnection state (isConnected stays false after onerror).
   - What's unclear: Whether the `onerror` handler correctly restores connection state when EventSource auto-reconnects.
   - Recommendation: Flag as a Medium-severity finding for SSE robustness.

3. **Form data type mismatch for int parameters**
   - What we know: DataMethodSelector converts input values to int/float on change (line 518-525), but stores `0` for NaN instead of keeping the invalid string for user correction.
   - What's unclear: Whether this causes confusing UX when user types non-numeric input.
   - Recommendation: Flag as Low-severity UX issue.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Node.js | Frontend build/lint | Yes | v22.22.0 | -- |
| npm | Package management | Yes | 10.9.4 | -- |
| TypeScript compiler | Type checking | Yes | ~5.9.3 | -- |
| ESLint | Code analysis | Yes | 9.39.1 | -- |

**Missing dependencies with no fallback:**
- None

**Missing dependencies with fallback:**
- None

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None (no frontend test framework configured) |
| Config file | None |
| Quick run command | `cd frontend && npx tsc --noEmit` (type check only) |
| Full suite command | `cd frontend && npx eslint src/` (lint only) |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CORR-03 | React state management correctness | Manual static review | N/A (review-only) | N/A |
| CORR-03 | SSE event handling edge cases | Manual static review + cross-validation | N/A | N/A |
| PERF-02 | Unnecessary re-render identification | Manual static review | N/A | N/A |
| PERF-02 | React Query cache strategy assessment | Manual static review | N/A | N/A |

**Note:** This phase is review-only. No automated tests are needed. Validation is through static code analysis and cross-referencing with backend SSE implementation.

### Sampling Rate
- **Per task commit:** `cd frontend && npx tsc --noEmit && npx eslint src/`
- **Per wave merge:** Same as above (review phase has no code changes)
- **Phase gate:** Findings document reviewed for completeness

### Wave 0 Gaps
- None -- this is a review-only phase. No test infrastructure needed.

## Project Constraints (from CLAUDE.md)

- **Review-only phase:** Only output findings and recommendations, no code modifications
- **Frontend conventions:** Named function exports, Tailwind CSS utilities, TypeScript strict mode
- **API response format:** `{"success": true, "data": {...}}` / `{"success": false, "error": {"code": "...", "message": "..."}}`
- **State management:** React Query (server state) + useState (local state), no Redux
- **Immutable patterns:** Spread operator for state updates, no mutation
- **No console.log in production:** Per coding-style.md rules
- **TypeScript strict:** `strict: true`, `verbatimModuleSyntax: true`, `erasableSyntaxOnly: true` (no enums)

## Pre-Existing Findings to Verify

From CONCERNS.md and previous phases:

| Finding | Source | Verification Action |
|---------|--------|---------------------|
| "No frontend tests" (Priority: Low) | CONCERNS.md | Confirm -- no vitest/jest found |
| "DataMethodSelector 829 lines" | CONCERNS.md | Verify line count, assess state complexity |
| "main.tsx missing QueryClientProvider" | CONTEXT.md specifics | Verify -- actually in App.tsx, not main.tsx. CONTEXT.md was incorrect. |
| event_manager.py memory leak (no cleanup) | Phase 125 | Frontend side: timeline array also grows without bound -- mirror issue |
| Dual stall detection | Phase 125 | No frontend impact (backend-only) |

## ESLint Results (Pre-Scan)

18 problems found (15 errors, 3 warnings):

**Errors:**
- `no-explicit-any` (4 instances): types/index.ts lines 91, 334, 339, 353; DataMethodSelector.tsx line 92
- `no-useless-escape` (1): DataMethodSelector.tsx line 161
- `set-state-in-effect` (2): CodeViewerModal.tsx line 26, RunMonitor.tsx line 26
- Other type errors from react-hooks plugin

**Warnings:**
- `react-hooks/exhaustive-deps` (3): AssertionSelector.tsx line 276, DataMethodSelector.tsx lines 283 and 299

## TypeScript Compilation

Clean -- zero errors from `npx tsc --noEmit`. All type checking passes.

## Key File Line Counts

| File | Lines | Priority |
|------|-------|----------|
| DataMethodSelector.tsx | 829 | P1 |
| TaskForm.tsx | 560 | P1 |
| AssertionSelector.tsx | 546 | P1 |
| types/index.ts | 456 | P2 |
| useRunStream.ts | 215 | P1 |
| StepTimeline.tsx | 285 | P2 |
| Tasks.tsx (page) | 211 | P2 |
| client.ts | 61 | P1 |
| TimelineItemCard.tsx | 247 | P2 |
| TaskDetail.tsx (page) | 174 | P2 |
| useTasks.ts | 135 | P2 |
| tasks.ts (API) | 113 | P2 |

## Sources

### Primary (HIGH confidence)
- Source code analysis of all ~60 frontend files
- Backend event_manager.py and run_pipeline.py (SSE format verification)
- ESLint 9 + typescript-eslint 8.48 scan results (2026-05-03)
- TypeScript tsc --noEmit results (2026-05-03)
- Phase 125-FINDINGS.md and Phase 126-FINDINGS.md (format reference)

### Secondary (MEDIUM confidence)
- CONCERNS.md pre-identified frontend issues
- CONVENTIONS.md declared patterns vs actual implementation
- CONTEXT.md canonical references

### Tertiary (LOW confidence)
- None -- all findings are from direct source analysis

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - verified from package.json and source imports
- Architecture: HIGH - directly analyzed all key files
- Pitfalls: HIGH - ESLint pre-scan confirmed 3 warnings; cross-validation with backend confirmed SSE format alignment
- SSE patterns: HIGH - both backend publish and frontend consume code reviewed line-by-line

**Research date:** 2026-05-03
**Valid until:** 2026-06-03 (stable codebase under review milestone)
