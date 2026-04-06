# Phase 60: 任务表单优化 - Research

**Researched:** 2026-04-02
**Domain:** Frontend/Backend code removal (api_assertions feature deletion)
**Confidence:** HIGH

## Summary

Phase 60 is a straightforward code removal phase: delete all traces of the "接口断言" (API assertions) feature from both frontend and backend. The feature uses free-form Python code in textareas, which is being replaced entirely by the structured business assertions (external_assertions) that were added in Phase 25.

The scope covers 7 files to modify and 3 files to delete entirely. The changes are mechanical -- remove fields, remove UI, remove event handlers, remove execution logic, and remove the database column. No new features are being added. The primary risk is missing a reference that causes a runtime error.

**Primary recommendation:** Execute removal in dependency order -- backend types first (schemas, models), then backend logic (runs.py, service file), then frontend types, then frontend UI, then database migration.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 全面清理 -- 前端 tab 移除 + 后端执行逻辑删除 + SSE 事件移除 + 数据库字段移除
- **D-02:** 不兼容旧数据 -- 旧报告中已有的 API 断言结果不再渲染，不做向后兼容处理
- **D-03:** 删除 `backend/core/api_assertion_service.py` 整个文件
- **D-04:** 移除 TaskForm 中的 `assertionTab` 状态和 tab 切换 UI，业务断言区域始终可见
- **D-05:** 移除 api_assertions 相关的 state/handler（handleAddApiAssertion, handleRemoveApiAssertion, handleApiAssertionChange）
- **D-06:** 从 CreateTaskDto / UpdateTaskDto 中移除 api_assertions 字段
- **D-07:** 删除 `frontend/src/components/Report/ApiAssertionResults.tsx`
- **D-08:** 从 `useRunStream.ts` 中移除 api_assertion SSE 事件监听
- **D-09:** 从 StepTimeline/TimelineItem 类型中移除 api_assertion 相关的 assertion 类型（保留 external_assertion）
- **D-10:** 从 `run_agent_background()` 中移除 api_assertions 执行循环
- **D-11:** 从 schemas.py 中移除 api_assertions 字段和 SSEApiAssertionEvent
- **D-12:** 从 models.py 中移除 Task.api_assertions 列（需要 Alembic migration 或直接 ALTER TABLE）
- **D-13:** 从 runs.py 的 create_run() 中移除 api_assertions 解析

### Claude's Discretion
- 具体文件删除顺序和分步策略
- TimelineItem 类型是否需要重命名或调整字段
- 数据库 migration 方式（Alembic vs 直接 SQL）

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| FORM-01 | 任务表单中移除"接口断言"和"业务断言"的 tab 切换，仅保留业务断言配置区域 | TaskForm.tsx lines 458-586: remove assertionTab state (L63), tab switcher UI (L458-481), api_assertions content (L484-519); business assertions section (L521-585) becomes always-visible |
| FORM-02 | 移除表单中 api_assertions 相关的 textarea 列表 | TaskForm.tsx: remove FormData.api_assertions (L24), initial state (L40), useEffect reset (L73), submit filter (L108), handlers (L137-153), textarea UI (L484-519) |
</phase_requirements>

## Standard Stack

No new libraries are needed for this phase. The work is pure removal.

### Core (Existing, Unchanged)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| React | 18+ | UI framework | Project standard |
| FastAPI | 0.100+ | Backend framework | Project standard |
| SQLAlchemy | 2.0+ | ORM | Project standard |
| SQLite | 3.51.0 | Database | Project standard, supports DROP COLUMN (3.35.0+) |

### Supporting (Existing, Unchanged)
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Pydantic | 2.0+ | Schema validation | Backend request/response models |
| aiosqlite | - | Async SQLite driver | All DB operations |

## Architecture Patterns

### Recommended Execution Order (Wave Strategy)

```
Wave 1: Backend types + service deletion
  1. Delete backend/core/api_assertion_service.py
  2. Clean backend/db/schemas.py (remove SSEApiAssertionEvent, api_assertions fields)
  3. Clean backend/db/models.py (remove api_assertions column)
  4. Clean backend/db/repository.py (remove serialize/deserialize helpers)

Wave 2: Backend logic cleanup
  5. Clean backend/api/routes/runs.py (remove api_assertions execution loop + import)
  6. Clean backend/core/report_service.py (remove api_assertion_results)
  7. Clean backend/api/routes/reports.py (remove api_assertion_results)

Wave 3: Frontend types + hooks
  8. Clean frontend/src/types/index.ts
  9. Clean frontend/src/hooks/useRunStream.ts
  10. Clean frontend/src/api/reports.ts

Wave 4: Frontend UI
  11. Clean frontend/src/components/TaskModal/TaskForm.tsx (main target)
  12. Delete frontend/src/components/Report/ApiAssertionResults.tsx
  13. Clean frontend/src/components/Report/index.ts (remove export)
  14. Clean frontend/src/components/RunMonitor/StepTimeline.tsx

Wave 5: Database + tests
  15. ALTER TABLE to drop column
  16. Delete test files for api_assertion_service
  17. Update any test files that reference api_assertions
```

### Pattern: Tab Removal to Always-Visible Section

**Before (current):** Tab state controls which section renders
```tsx
const [assertionTab, setAssertionTab] = useState<'api' | 'business'>('api')
// ... tab buttons ...
{assertionTab === 'api' ? (<api section>) : (<business section>)}
```

**After (target):** Business assertions always visible, no tab wrapper
```tsx
// No assertionTab state needed
<div>
  <p className="text-xs text-gray-500 mb-2">选择业务断言方法...</p>
  {/* Business assertion section content directly */}
</div>
```

### Pattern: SSE Event Listener Removal

In `useRunStream.ts`, the `api_assertion` event listener (lines 111-137) maintains three pieces of state:
1. `Run.api_assertions` array -- remove entirely
2. `Run.timeline` array with `{ type: 'assertion', data: SSEApiAssertionEvent }` -- remove this type
3. The EventSource listener itself -- remove the `addEventListener('api_assertion', ...)` block

### Anti-Patterns to Avoid
- **Partial removal:** Leaving dead imports (e.g., `SSEApiAssertionEvent` in StepTimeline.tsx import) causes TypeScript errors
- **Forgetting TimelineItem type cleanup:** The `TimelineItemAssertion` type and `'assertion'` discriminator must be removed from the union type, otherwise TypeScript compilation may still expect it
- **Dropping DB column before code cleanup:** If code still tries to read/write the column, errors occur. Remove code first, then alter table.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| DB migration | Custom SQL scripts | SQLite ALTER TABLE DROP COLUMN | Built-in since 3.35.0, safe for simple column removal |

**Key insight:** This phase is entirely about deletion. The only "building" is restructuring the TaskForm to show business assertions directly. No new abstractions needed.

## Runtime State Inventory

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | SQLite `tasks.api_assertions` column with TEXT data in existing records | ALTER TABLE DROP COLUMN (D-02: no backward compat needed) |
| Live service config | None -- no external services configure api_assertions | None |
| OS-registered state | None | None |
| Secrets/env vars | None | None |
| Build artifacts | `backend/tests/__pycache__/test_api_assertion_service.cpython-311-*.pyc` -- stale after file deletion | Removed by `__pycache__` cleanup or `git clean` |

**Nothing found in category:**
- Live service config: None -- verified, api_assertions is entirely inline code execution, no external service registration
- OS-registered state: None -- verified, no OS-level registrations for this feature
- Secrets/env vars: None -- verified, no secrets related to api_assertions

## Common Pitfalls

### Pitfall 1: TypeScript Compilation Failures from Stale Type References
**What goes wrong:** Removing `SSEApiAssertionEvent` from `types/index.ts` but leaving imports in `useRunStream.ts` or `StepTimeline.tsx` causes build failures.
**Why it happens:** Types are imported in multiple files; grep may miss re-exports.
**How to avoid:** After all edits, run `cd frontend && npm run build` to verify zero compilation errors.
**Warning signs:** TypeScript error: "Cannot find name 'SSEApiAssertionEvent'" or "Module has no exported member"

### Pitfall 2: StepTimeline References Removed Type
**What goes wrong:** `StepTimeline.tsx` imports `SSEApiAssertionEvent` from types and uses it in `renderAssertionItem()`. If the type is removed but the function remains, compilation fails.
**Why it happens:** The assertion timeline item renderer is a separate function in StepTimeline, easy to overlook.
**How to avoid:** Remove `renderAssertionItem` function and its `{item.type === 'assertion' && renderAssertionItem(...)}` call in StepTimeline.tsx. Also remove `SSEApiAssertionEvent` from the import on line 3.
**Warning signs:** `StepTimeline.tsx` references undefined type or function.

### Pitfall 3: ReportDetailResponse Still References api_assertion_results
**What goes wrong:** Frontend `reports.ts` still maps `api_assertion_results` from the API response. If backend stops returning it, the frontend field becomes `undefined` (benign but messy).
**Why it happens:** The report API response mapping in `reports.ts` line 169 still transforms `api_assertion_results`.
**How to avoid:** Remove `api_assertion_results` from both the frontend response types and the mapping function. Clean the backend `ReportDetailResponse` schema too.
**Warning signs:** Console warnings about unexpected response fields, or TypeScript unused variable warnings.

### Pitfall 4: Backend Import Still References Deleted Service
**What goes wrong:** `runs.py` line 32 imports `ApiAssertionService` from the deleted file, causing ImportError at module load.
**Why it happens:** The import is at the top of `runs.py`, so it fails before any function runs.
**How to avoid:** Remove the import line AND all usages of `ApiAssertionService` in `runs.py` simultaneously.
**Warning signs:** `ImportError: cannot import name 'ApiAssertionService'` on server startup.

### Pitfall 5: Database Column Drop with Active Connections
**What goes wrong:** ALTER TABLE DROP COLUMN on SQLite may fail if there are active readers/writers.
**Why it happens:** SQLite WAL mode allows concurrent reads, but DDL operations need exclusive access briefly.
**How to avoid:** Run the migration when the server is stopped, or during a maintenance window. The ALTER TABLE is fast (< 1 second for typical table sizes).
**Warning signs:** `sqlite3.OperationalError: database is locked`

## Code Examples

### TaskForm.tsx Simplification (lines 452-587)

**Remove entirely (lines 63, 458-481, 484-519):**
```tsx
// REMOVE: assertionTab state
const [assertionTab, setAssertionTab] = useState<'api' | 'business'>('api')

// REMOVE: entire tab switcher div (lines 458-481)
<div className="flex gap-2 mb-3">
  <button onClick={() => setAssertionTab('api')} ...>接口断言</button>
  <button onClick={() => setAssertionTab('business')} ...>业务断言</button>
</div>

// REMOVE: entire api_assertions section (lines 484-519)
{assertionTab === 'api' ? ( <div>...api textareas...</div> ) : ( <div>...business section...</div> )}
```

**Replace with (business assertions always visible):**
```tsx
<div>
  <label className="block text-sm font-medium text-gray-700 mb-1">
    断言 <span className="text-gray-400 text-xs">(可选)</span>
  </label>
  <div>
    <p className="text-xs text-gray-500 mb-2">
      选择业务断言方法，配置参数后系统自动执行验证
    </p>
    {/* Add assertion button */}
    <button type="button" onClick={() => setAssertionSelectorOpen(true)} ...>
      添加断言
    </button>
    {/* Assertion cards */}
    {formData.assertions.length > 0 && (
      <div className="space-y-2">
        {formData.assertions.map((config, index) => (
          // ... existing assertion card rendering ...
        ))}
      </div>
    )}
    {/* Empty state */}
    {formData.assertions.length === 0 && (
      <div className="text-center py-4 text-gray-500 text-sm">
        暂无业务断言配置，点击"添加断言"开始配置
      </div>
    )}
  </div>
</div>
```

### TimelineItem Type Cleanup (types/index.ts)

**Remove these types:**
```tsx
// REMOVE: ApiAssertionFieldResult (lines 78-85)
export interface ApiAssertionFieldResult { ... }

// REMOVE: SSEApiAssertionEvent (lines 88-95)
export interface SSEApiAssertionEvent { ... }

// REMOVE: TimelineItemAssertion (lines 163-166)
export interface TimelineItemAssertion {
  type: 'assertion'
  data: SSEApiAssertionEvent
}

// UPDATE: TimelineItem union (lines 167-170)
export type TimelineItem =
  | TimelineItemStep
  | TimelineItemPrecondition
  // REMOVE: | TimelineItemAssertion
```

### Run Type Cleanup (types/index.ts)

**Remove from Run interface (line 51):**
```tsx
api_assertions?: SSEApiAssertionEvent[]  // REMOVE
```

### Backend runs.py Cleanup (lines 247-321)

**Remove the entire api_assertions execution block:**
```python
# REMOVE lines 247-321: entire api_assertions execution section
# Starting at: "# === 接口断言执行（新增） ==="
# Ending at: "# === 接口断言执行结束 ==="
```

Also remove:
- Line 32: `from backend.core.api_assertion_service import ApiAssertionService`
- Line 25: `SSEApiAssertionEvent` from schemas import
- Lines 63, 468-474: api_assertions parameter and parsing in `create_run()`
- Line 494: `api_assertions` argument in `background_tasks.add_task()`

### Database Migration

```sql
-- Safe for SQLite 3.35.0+ (current version: 3.51.0)
ALTER TABLE tasks DROP COLUMN api_assertions;
```

No Alembic needed -- direct SQL is simpler for a single column removal. Execute when server is stopped.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| api_assertions (free Python code) | external_assertions (structured business assertions) | Phase 25 | Structured assertions are safer and more user-friendly |

**Deprecated/outdated:**
- `ApiAssertionService`: Being fully removed this phase
- `SSEApiAssertionEvent`: Being fully removed this phase
- `api_assertions` DB column: Being dropped this phase

## Files Inventory

### Files to DELETE (3)
| File | Lines | Reason |
|------|-------|--------|
| `backend/core/api_assertion_service.py` | 262 | Entire service no longer used |
| `frontend/src/components/Report/ApiAssertionResults.tsx` | 67 | Component no longer imported anywhere |
| `backend/tests/unit/test_api_assertion_service.py` | ~100+ | Tests for deleted service |

### Files to MODIFY (14)

| File | Change Summary | Risk |
|------|---------------|------|
| `frontend/src/components/TaskModal/TaskForm.tsx` | Remove tab UI, api_assertions state/handlers, simplify to always-show business assertions | MEDIUM (biggest change, ~100 lines removed) |
| `frontend/src/types/index.ts` | Remove api_assertion-related types (5 interfaces + 1 union member) | LOW |
| `frontend/src/hooks/useRunStream.ts` | Remove api_assertion listener, Run.api_assertions state | LOW |
| `frontend/src/components/RunMonitor/StepTimeline.tsx` | Remove renderAssertionItem, SSEApiAssertionEvent import, assertion type handling | LOW |
| `frontend/src/components/Report/index.ts` | Remove ApiAssertionResults export | LOW |
| `frontend/src/api/reports.ts` | Remove api_assertion_results from types and mapping | LOW |
| `backend/db/schemas.py` | Remove api_assertions fields from TaskBase/TaskCreate/TaskUpdate/TaskResponse, remove SSEApiAssertionEvent, remove from validator | MEDIUM |
| `backend/db/models.py` | Remove api_assertions column from Task model | LOW |
| `backend/db/repository.py` | Remove _serialize/_deserialize_api_assertions helpers, remove from create/update | LOW |
| `backend/api/routes/runs.py` | Remove ApiAssertionService import, api_assertions parameter, parsing, execution loop | MEDIUM |
| `backend/core/report_service.py` | Remove api_assertion_results computation | LOW |
| `backend/api/routes/reports.py` | Remove api_assertion_results from response | LOW |
| `backend/tests/integration/test_api_assertion_integration.py` | Delete or clean | LOW |
| `backend/tests/api/routes/test_runs_assertion_integration.py` | Clean api_assertions references | LOW |

### Files UNCHANGED (verified)
| File | Reason |
|------|--------|
| `frontend/src/components/TaskModal/AssertionSelector.tsx` | Business assertion selector, not affected |
| `frontend/src/components/TaskModal/FieldParamsEditor.tsx` | Business assertion field editor, not affected |
| `frontend/src/api/externalAssertions.ts` | Business assertion API client, not affected |
| `backend/api/routes/external_assertions.py` | Business assertion routes, not affected |
| `backend/core/external_precondition_bridge.py` | Business assertion bridge, not affected |

## Open Questions

1. **TimelineItem 'assertion' type after removal**
   - What we know: The `TimelineItemAssertion` with `type: 'assertion'` is currently used only for api_assertion events. External assertions use a different SSE event (`external_assertions`) that does not produce individual timeline items.
   - What's unclear: Whether the planner wants to keep the `'assertion'` discriminator type for future use by external assertions.
   - Recommendation: Remove it. External assertions currently send a summary event, not per-assertion timeline events. If needed later, it can be re-added with different data shape.

2. **Database migration timing**
   - What we know: SQLite 3.51.0 supports DROP COLUMN. Server should be stopped during migration.
   - What's unclear: Whether the planner prefers a startup migration or a manual step.
   - Recommendation: Add a simple startup migration in the app initialization (check if column exists, drop if so), so it's automatic on next deploy.

3. **ReportDetailResponse.api_assertion_results in backend schemas**
   - What we know: The `ReportDetailResponse` Pydantic schema has `api_assertion_results` and `api_pass_rate` fields. Old reports may have data in the DB.
   - What's unclear: Whether to remove these fields entirely from the response schema.
   - Recommendation: Remove them per D-02 (no backward compatibility). Old report data in `assertion_results` table with `api_*` prefixed assertion_ids will remain in DB but won't be surfaced.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| SQLite | DB column drop | ✓ | 3.51.0 | -- |
| Node.js | Frontend build | ✓ | -- | -- |
| Python 3.11 | Backend | ✓ | -- | -- |
| pytest | Tests | ✓ | 9.0.2 | -- |

**Missing dependencies with no fallback:** None

**Missing dependencies with fallback:** N/A

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 9.0.2 (asyncio_mode=auto) |
| Config file | pyproject.toml [tool.pytest.ini_options] |
| Quick run command | `uv run pytest backend/tests/ -x -q` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| FORM-01 | TaskForm has no tab switcher, business assertions always visible | Manual (UI) | Visual inspection | N/A |
| FORM-02 | TaskForm has no api_assertions textarea | Manual (UI) | Visual inspection | N/A |
| -- | Backend rejects api_assertions in create/update | unit | `uv run pytest backend/tests/ -k "task" -x -q` | Partial |
| -- | Frontend build succeeds after type removal | build | `cd frontend && npm run build` | N/A |
| -- | Backend starts without ImportError | smoke | `uv run python -c "from backend.api.routes.runs import router"` | N/A |

### Sampling Rate
- **Per task commit:** `cd frontend && npm run build && cd ../ && uv run pytest backend/tests/ -x -q`
- **Per wave merge:** Full suite + build
- **Phase gate:** `cd frontend && npm run build && cd ../ && uv run pytest backend/tests/ -v`

### Wave 0 Gaps
- [ ] Delete `backend/tests/unit/test_api_assertion_service.py` -- entire file for removed service
- [ ] Delete `backend/tests/integration/test_api_assertion_integration.py` -- entire file for removed service
- [ ] Clean `backend/tests/api/routes/test_runs_assertion_integration.py` -- remove api_assertions test cases
- [ ] Clean `backend/tests/unit/test_browser_cleanup.py` -- has 1 api_assertion reference

## Project Constraints (from CLAUDE.md)

- Backend: FastAPI + SQLite (aiosqlite) + SQLAlchemy
- Frontend: React + Vite + TypeScript
- Package management: uv (Python), npm (Node.js)
- Testing: pytest for backend, Playwright for E2E
- Backend run: `uv run uvicorn backend.api.main:app --reload --port 8080`
- Frontend build: `cd frontend && npm run build`
- Tests: `uv run pytest backend/tests/ -v`
- Immutability: Use immutable patterns (spread operator), no mutation
- File size: Keep files under 800 lines
- Error handling: Comprehensive try/catch with descriptive messages
- No console.log statements
- No hardcoded values

## Sources

### Primary (HIGH confidence)
- Source code analysis of all 14+ affected files
- CONTEXT.md canonical references with exact line numbers
- SQLite version verification (3.51.0 supports DROP COLUMN since 3.35.0+)

### Secondary (MEDIUM confidence)
- N/A -- all findings verified directly from source code

### Tertiary (LOW confidence)
- N/A -- no unverified claims

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new libraries, only removal from existing codebase
- Architecture: HIGH -- removal order and patterns are clear from direct code inspection
- Pitfalls: HIGH -- pitfalls identified from tracing all cross-file references via grep
- File inventory: HIGH -- every file verified by reading source code, not just relying on CONTEXT.md

**Research date:** 2026-04-02
**Valid until:** 2026-05-02 (stable -- no external dependencies)
