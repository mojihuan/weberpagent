# Phase 59: 报告步骤展示 - Research

**Researched:** 2026-04-02
**Domain:** Report detail page timeline unification (backend persistence + frontend component refactoring)
**Confidence:** HIGH

## Summary

This phase unifies three separate display sections in the report detail page (preconditions, assertions, UI steps) into a single interleaved timeline. The core challenge is a data gap: precondition results are currently only sent as SSE events and never persisted to the database. The `report_service.py:134` line contains an explicit TODO for this. API assertion results ARE persisted (to `assertion_results` table via `AssertionResultRepository`), but UI assertion results use the same table with non-`api_` prefixed `assertion_id` values. Neither entity has a global sequence number for interleaving. The implementation requires: (1) a new `PreconditionResult` database model, (2) a global `sequence_number` field added to all three entity types, (3) a backend merge-and-sort API response using a `ReportTimelineItem` discriminated union, and (4) a frontend refactoring to remove three independent sections and render a unified step list.

**Primary recommendation:** Add a `PreconditionResult` ORM model mirroring the SSE event shape, assign global sequence numbers during `run_agent_background` execution, create a `ReportTimelineItem` Pydantic discriminated union, and extend `StepItem.tsx` into a generic `TimelineItemCard` component that renders different expanded content per type.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 前置条件结果需要持久化到数据库 — 当前只作为 SSE 事件发送，未存储。报告中 `precondition_results` 始终为 None
- **D-02:** 为三类步骤（UI 操作、前置条件、断言）分配全局递增的 sequence_number，用于确定交错排序
- **D-03:** 后端负责合并三类数据并按全局序号排序，返回统一的 ReportTimelineItem[] 列表
- **D-04:** 新增 `ReportTimelineItem` 联合类型，包含 type 字段区分 'step' | 'precondition' | 'assertion' + 对应数据
- **D-05:** 报告详情 API (GET /api/reports/{id}) 返回 `timeline_items: ReportTimelineItem[]` 替代三个独立数组
- **D-06:** 保留现有的汇总统计字段在 API 响应中
- **D-07:** 前置条件/断言步骤复用 StepItem 的可展开卡片风格
- **D-08:** 三类步骤用不同颜色/图标区分（与 Phase 58 执行监控保持一致）
- **D-09:** 展开内容因类型不同：UI 步骤 = 截图+AI 推理；前置条件 = 代码+变量输出；断言 = 断言名称+字段结果详情
- **D-10:** 移除 PreconditionSection、AssertionResults、ApiAssertionResults 三个独立区块
- **D-11:** 保留顶部汇总统计区域

### Claude's Discretion
- PreconditionResult 数据库表的具体字段设计
- 全局 sequence_number 的分配机制（共享计数器 vs 时间戳回退）
- ReportTimelineItem 的具体类型定义（字段细节）
- 卡片展开/折叠的默认行为
- 具体图标和 Tailwind 颜色值

### Deferred Ideas (OUT OF SCOPE)
None
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| RPT-01 | 报告详情页的步骤列表中展示前置条件步骤及其执行结果（成功/失败、耗时、变量输出） | New `PreconditionResult` ORM model + persistence in `run_agent_background` + `PreconditionResultRepository` for data access + new `ReportTimelineItemPrecondition` schema |
| RPT-02 | 报告详情页的步骤列表中展示断言步骤及其执行结果（通过/失败、断言名称、失败信息） | Existing `assertion_results` table already stores API assertion results with `field_results` data. Need `sequence_number` on assertion results + `ReportTimelineItemAssertion` schema |
| RPT-03 | 前置条件和断言步骤在报告步骤列表中按实际执行顺序与其他步骤交错展示 | Global `sequence_number` counter in `run_agent_background` + backend merge-sort in `ReportService.get_report_data()` + frontend unified timeline rendering |
</phase_requirements>

## Standard Stack

### Core (Existing - No New Dependencies)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| SQLAlchemy (async) | existing | ORM for new `PreconditionResult` model | Already used for all models in `backend/db/models.py` |
| Pydantic | existing | API schema for `ReportTimelineItem` union | Already used for all request/response schemas in `backend/db/schemas.py` |
| React | 19.2 | Frontend component rendering | Project standard |
| Tailwind CSS | 4.2 | Styling for card components | Project standard, matches Phase 58 StepTimeline colors |
| lucide-react | 0.577 | Icons (FileCode, ShieldCheck, CheckCircle, etc.) | Already used in StepTimeline for type-specific icons |

### No New Packages Required
All dependencies are already installed. This phase extends existing patterns.

## Architecture Patterns

### Recommended Project Structure (Changes Only)

```
backend/
  db/
    models.py              # ADD: PreconditionResult model
    schemas.py             # ADD: ReportTimelineItem discriminated union schemas
    repository.py          # ADD: PreconditionResultRepository
  core/
    report_service.py      # MODIFY: merge-sort logic for timeline
  api/routes/
    runs.py                # MODIFY: global sequence_number allocation + precondition persistence
    reports.py             # MODIFY: return timeline_items instead of separate arrays

frontend/src/
  types/
    index.ts               # ADD: ReportTimelineItem types for report page
  api/
    reports.ts             # MODIFY: new timeline_items response handling
  components/Report/
    StepItem.tsx           # EXTEND: support precondition/assertion rendering
    ReportTimelineItem.tsx # NEW: wrapper component for type-specific card rendering
    PreconditionSection.tsx # REMOVE (D-10)
    AssertionResults.tsx    # REMOVE (D-10)
    ApiAssertionResults.tsx # REMOVE (D-10)
    index.ts               # UPDATE: exports
  pages/
    ReportDetail.tsx       # MODIFY: use unified timeline
```

### Pattern 1: Discriminated Union for Timeline Items (Backend)

**What:** A Pydantic model with a `type` literal field that selects which data variant applies.
**When to use:** API responses that need to return heterogeneous items in a single list.
**Example:**

```python
# Source: Adapted from Phase 58's frontend TimelineItem pattern, applied to backend
from typing import Literal, Union, Annotated
from pydantic import BaseModel, Tag, Discriminator

class ReportTimelineStep(BaseModel):
    type: Literal["step"]
    id: str
    sequence_number: int
    action: str
    reasoning: str | None = None
    screenshot_url: str | None = None
    status: str
    error: str | None = None
    duration_ms: int | None = None

class ReportTimelinePrecondition(BaseModel):
    type: Literal["precondition"]
    id: str
    sequence_number: int
    index: int
    code: str
    status: str
    error: str | None = None
    duration_ms: int | None = None
    variables: dict | None = None

class ReportTimelineAssertion(BaseModel):
    type: Literal["assertion"]
    id: str
    sequence_number: int
    assertion_id: str
    assertion_name: str | None = None
    status: str
    message: str | None = None
    actual_value: str | None = None
    field_results: list[dict] | None = None
    duration_ms: int | None = None

ReportTimelineItem = Annotated[
    Union[ReportTimelineStep, ReportTimelinePrecondition, ReportTimelineAssertion],
    Discriminator("type")
]
```

### Pattern 2: Global Sequence Number Counter

**What:** A shared integer counter incremented for every event during `run_agent_background` execution, persisted as a column on each entity.
**When to use:** When multiple entity types need a unified ordering.
**Example:**

```python
# In run_agent_background, maintain a global counter:
global_seq = 0

# Before each precondition execution:
global_seq += 1
# Store precondition result with sequence_number=global_seq

# Before each step (in on_step callback):
global_seq += 1
# Step's step_index already serves as ordering, but add sequence_number too

# Before each API assertion execution:
global_seq += 1
# Store assertion result with sequence_number=global_seq
```

**Key insight:** The counter must be a `nonlocal` variable inside `run_agent_background` and captured by the `on_step` closure. The `on_step` callback already exists and uses `nonlocal step_count`, so adding `nonlocal global_seq` follows the same pattern.

### Pattern 3: StepItem Extension for Multiple Types

**What:** Extend the existing `StepItem` component (or create a wrapper) to render type-specific expanded content while sharing the collapsible card structure.
**When to use:** When visual consistency is required across different data types in the same list.

**Type-specific content areas:**
- **UI step (existing):** Screenshot grid + ReasoningText component
- **Precondition:** Full code block + extracted variables (key-value pairs)
- **Assertion:** Assertion name + pass/fail status + field_results detail table

### Anti-Patterns to Avoid
- **Three separate API calls for each type:** Do NOT fetch preconditions, assertions, and steps in separate requests. Merge on the backend, return one list.
- **Client-side interleaving:** Do NOT sort on the frontend. The backend owns the global sequence number; the frontend renders items in the order received.
- **Duplicating Phase 58's exact implementation:** Phase 58 uses a compact sidebar timeline with inline expansion. The report page uses larger expandable cards with screenshots. Share colors/icons, not layout code.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Precondition result storage | Ad-hoc JSON blob in Run metadata | New `PreconditionResult` ORM model with typed columns | Structured queries, individual record access, clean API responses |
| Timeline item type dispatch | if/else chain on type field | Pydantic discriminated union with `Discriminator` | Type safety, automatic serialization, clean FastAPI response models |
| Variable display formatting | Custom string builder | Extract `PreconditionSection`'s existing variable rendering code | Already handles nested objects, type formatting |

**Key insight:** The existing `PreconditionSection.tsx` and `ApiAssertionResults.tsx` contain reusable display logic for variables and field_results respectively. Extract these patterns rather than rewriting.

## Common Pitfalls

### Pitfall 1: Precondition Results Not Persisted for Existing Reports
**What goes wrong:** After implementing persistence, old reports will have `precondition_results = None` and no `PreconditionResult` rows.
**Why it happens:** Precondition results were only ever sent as SSE events; no historical data exists.
**How to avoid:** Frontend must gracefully handle empty precondition/assertion timeline items. Reports generated before this phase simply show only UI steps. No data migration needed.
**Warning signs:** 500 errors when loading old reports, or empty timeline for old reports.

### Pitfall 2: sequence_number Collision Across Concurrent Runs
**What goes wrong:** Two concurrent runs sharing a global counter could get interleaved sequence numbers.
**Why it happens:** Using a module-level or class-level counter instead of a per-run counter.
**How to avoid:** The `global_seq` counter is a local variable inside `run_agent_background`, scoped to a single run. Each background task has its own counter starting at 0. No cross-run contamination possible.
**Warning signs:** Steps appearing out of order in reports from concurrent runs.

### Pitfall 3: AssertionResult Foreign Key Constraint
**What goes wrong:** `AssertionResult.assertion_id` has a foreign key to `assertions.id`. API assertion results use `assertion_id=f"api_{index}_{field_name}"` which does NOT reference an actual `Assertion` row.
**Why it happens:** The `api_` prefixed IDs were never checked against the FK constraint because SQLite does not enforce FK constraints by default.
**How to avoid:** When creating the new `PreconditionResult` model, do NOT add a FK to `assertions` table. Use a plain `String` column for any reference fields. For assertion timeline items, the `assertion_id` from existing `assertion_results` already works (UI assertions have real FKs, API assertions have synthetic IDs).
**Warning signs:** If the project ever migrates to PostgreSQL or enables SQLite FK enforcement, API assertion inserts would fail.

### Pitfall 4: Losing API Assertion field_results Data
**What goes wrong:** API assertion results store individual field results as separate `AssertionResult` rows (one per field), but the timeline needs to group them back into a single assertion entry.
**Why it happens:** The current persistence model in `runs.py:269-277` creates one `AssertionResult` row per field_result, each with its own `sequence_number`. The timeline should show one assertion card, not N field cards.
**How to avoid:** Two options: (a) store field_results as a JSON column on a single assertion row, or (b) group field-level rows by assertion index when building the timeline. Option (a) is cleaner for the new model. For the existing assertion results, group by the `api_{index}` prefix of `assertion_id`.
**Warning signs:** Timeline showing 5 separate assertion cards for a single assertion that checked 5 fields.

### Pitfall 5: Database Schema Migration Without Alembic
**What goes wrong:** Adding columns to existing models or creating new tables requires `init_db()` to be called.
**Why it happens:** The project uses `Base.metadata.create_all` in `database.py:41` which only creates NEW tables, it does NOT add columns to existing tables.
**How to avoid:** For new models (`PreconditionResult`), `create_all` works perfectly. For adding `sequence_number` to existing models (`Step`, `AssertionResult`), SQLite does not support `ALTER TABLE ADD COLUMN` easily through SQLAlchemy. **Recommendation:** Store sequence_number only on the new `PreconditionResult` model and add it to `Step` model. For `AssertionResult`, use `created_at` timestamp as fallback ordering within the assertion group, and assign the sequence_number when creating assertion result rows.
**Warning signs:** Missing columns in production, old data without sequence numbers.

## Code Examples

### PreconditionResult ORM Model

```python
# backend/db/models.py - New model
class PreconditionResult(Base):
    """前置条件执行结果模型"""
    __tablename__ = "precondition_results"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    run_id: Mapped[str] = mapped_column(String(8), ForeignKey("runs.id"), nullable=False)
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    index: Mapped[int] = mapped_column(Integer, nullable=False)  # 前置条件在列表中的位置
    code: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # success, failed
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    variables: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # 关系
    run: Mapped["Run"] = relationship("Run", back_populates="precondition_results")
```

### Adding sequence_number to Step model

```python
# In models.py Step class, add:
    sequence_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
```

Since `create_all` won't add columns to existing tables, the Step table needs a manual migration or a startup check:

```python
# In database.py init_db(), after create_all:
# Check if sequence_number column exists on steps table
async def _ensure_columns(conn):
    # SQLite-specific: check column existence
    result = await conn.execute(text("PRAGMA table_info(steps)"))
    columns = [row[1] for row in result]
    if "sequence_number" not in columns:
        await conn.execute(text("ALTER TABLE steps ADD COLUMN sequence_number INTEGER"))
    # Same for assertion_results
    result = await conn.execute(text("PRAGMA table_info(assertion_results)"))
    columns = [row[1] for row in result]
    if "sequence_number" not in columns:
        await conn.execute(text("ALTER TABLE assertion_results ADD COLUMN sequence_number INTEGER"))
```

### Persistence in run_agent_background

```python
# In runs.py run_agent_background, add:
from backend.db.repository import PreconditionResultRepository

# Add to the function body:
precondition_result_repo = PreconditionResultRepository(session)
global_seq = 0

# Inside precondition loop (after execution):
global_seq += 1
await precondition_result_repo.create(
    run_id=run_id,
    sequence_number=global_seq,
    index=i,
    code=code,
    status="success" if result.success else "failed",
    error=result.error,
    duration_ms=result.duration_ms,
    variables=json.dumps(result.variables) if result.variables else None,
)

# Inside on_step callback (add nonlocal global_seq):
nonlocal global_seq
global_seq += 1
# Include sequence_number in step_data dict

# Inside API assertion loop (after execution):
global_seq += 1
# Store with sequence_number on the assertion result
```

### Backend Merge-Sort in ReportService

```python
# backend/core/report_service.py - Modified get_report_data
async def get_report_data(self, run_id: str) -> Optional[dict]:
    # ... existing code ...

    # Get precondition results
    precondition_results = await self.precondition_result_repo.list_by_run(run_id)

    # Build timeline items
    timeline_items: list[dict] = []

    for s in steps:
        timeline_items.append({
            "type": "step",
            "sequence_number": s.sequence_number or s.step_index,  # fallback for old data
            "data": s,
        })

    for pr in precondition_results:
        timeline_items.append({
            "type": "precondition",
            "sequence_number": pr.sequence_number,
            "data": pr,
        })

    # Group assertion results by assertion index, use sequence_number
    # ... assertion grouping logic ...

    # Sort by sequence_number
    timeline_items.sort(key=lambda x: x["sequence_number"])

    return {
        # ... existing fields ...
        "timeline_items": timeline_items,
    }
```

### Frontend ReportTimelineItem Types

```typescript
// frontend/src/types/index.ts - Add report-specific timeline types

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

### Type-Specific Card Rendering (Extending StepItem Pattern)

```typescript
// Phase 58 StepTimeline uses these colors/icons — replicate for report cards:
// step:        CheckCircle/XCircle, green/red, border-gray-200
// precondition: FileCode + CheckCircle/XCircle, amber-500/700, bg-amber-50
// assertion:   ShieldCheck + CheckCircle/XCircle, purple-500/700, bg-purple-50
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Three separate display sections | Unified timeline with interleaved items | Phase 58 (execution monitor) | Phase 59 applies same pattern to report page |
| SSE-only precondition data | Persisted precondition results | This phase | Enables report page display |
| No global ordering | Global sequence_number | This phase | Enables correct interleaving |

**Deprecated/outdated:**
- `ReportDetailResponse.precondition_results: Optional[List[SSEPreconditionEvent]]` — was always None, replaced by `timeline_items`
- `ReportDetailResponse.ui_assertion_results` / `api_assertion_results` — replaced by unified timeline

## Open Questions

1. **Assertion grouping strategy for timeline**
   - What we know: API assertions store one `AssertionResult` row per field (e.g., `api_0_fieldName`). UI assertions store one row per assertion.
   - What's unclear: Should the timeline show one card per assertion (grouping fields) or one card per field?
   - Recommendation: Group by assertion index. Show one "Assertion N" card with all field_results inside. This matches Phase 58's `SSEApiAssertionEvent` structure.

2. **Step.sequence_number backward compatibility**
   - What we know: Existing Step rows have no `sequence_number`. `create_all` won't add the column.
   - What's unclear: Whether to add a startup migration or use `step_index` as fallback.
   - Recommendation: Add `sequence_number` column with a startup ALTER TABLE check in `init_db()`. Fall back to `step_index` for old rows where `sequence_number` is NULL.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | Backend | Yes | 3.14 (per pycache) | -- |
| Node.js | Frontend | Yes | -- | -- |
| SQLite | Database | Yes | bundled | -- |
| pytest | Backend tests | Yes | 9.0+ | -- |
| uv | Python package manager | Yes | -- | -- |

**Missing dependencies with no fallback:** None

**Missing dependencies with fallback:** None

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (backend), no frontend test framework |
| Config file | None (conftest.py exists at `backend/tests/conftest.py`) |
| Quick run command | `uv run pytest backend/tests/unit/ -v -x` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| RPT-01 | PreconditionResult persistence and retrieval | unit | `uv run pytest backend/tests/unit/test_precondition_result_repo.py -x` | No — Wave 0 |
| RPT-02 | Assertion timeline item construction | unit | `uv run pytest backend/tests/unit/test_report_timeline.py -x` | No — Wave 0 |
| RPT-03 | Timeline merge-sort ordering | unit | `uv run pytest backend/tests/unit/test_report_timeline.py::test_interleaved_ordering -x` | No — Wave 0 |
| RPT-03 | Frontend renders unified timeline | manual | Visual inspection in browser | N/A |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/ -v -x`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full backend suite green + manual frontend visual check

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_precondition_result_repo.py` — CRUD tests for new PreconditionResultRepository
- [ ] `backend/tests/unit/test_report_timeline.py` — timeline item construction and merge-sort tests
- [ ] `backend/tests/unit/test_db_schemas.py` — add ReportTimelineItem schema validation tests

## Sources

### Primary (HIGH confidence)
- Direct code reading of all canonical reference files (models.py, schemas.py, repository.py, report_service.py, runs.py, ReportDetail.tsx, StepItem.tsx, StepTimeline.tsx, PreconditionSection.tsx, AssertionResults.tsx, ApiAssertionResults.tsx, reports.ts, types/index.ts)
- Phase 58 execution monitor implementation as pattern reference (StepTimeline.tsx, useRunStream.ts)

### Secondary (MEDIUM confidence)
- CONTEXT.md decisions verified against actual code structure

### Tertiary (LOW confidence)
- None — all findings are from direct source code inspection

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all dependencies already exist in project, no new packages
- Architecture: HIGH — patterns established by Phase 58's TimelineItem discriminated union, direct code analysis confirms feasibility
- Pitfalls: HIGH — identified from actual code (report_service.py:134 TODO, assertion_id FK pattern, create_all limitation)
- Data model: HIGH — new PreconditionResult model mirrors existing PreconditionResult dataclass in precondition_service.py

**Research date:** 2026-04-02
**Valid until:** 2026-05-02 (stable — no fast-moving dependencies)
