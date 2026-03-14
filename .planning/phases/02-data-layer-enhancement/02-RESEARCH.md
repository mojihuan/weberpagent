# Phase 2: Data Layer Enhancement - Research

**Researched:** 2026-03-14
**Domain:** SQLAlchemy 2.0 ORM models, async database patterns, file storage
**Confidence:** HIGH

## Summary

This phase focuses on completing the database schema for the AI-driven UI testing platform. The core work involves adding two new ORM models (Assertion and AssertionResult), configuring proper relationships with cascade delete, and implementing the `RunRepository.get_steps()` method. The existing codebase uses SQLAlchemy 2.0 async patterns with aiosqlite, and already has established patterns for models, repositories, and Pydantic schemas.

**Primary recommendation:** Follow the existing ORM patterns exactly - use `Mapped[]` type hints, `mapped_column()`, and `relationship()` with `back_populates`. For cascade delete, use `cascade="all, delete-orphan"` on the parent side relationship.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **关联 Task** — 断言定义在 Task 上，所有 Run 共享同一组断言
- **优点**：修改断言后新执行自动应用，适合回归测试场景
- **关系**：Task → Assertion（一对多）
- **Run 级别** — AssertionResult 关联到 Run，每个 Run 有一组断言结果
- **字段**：status (pass/fail), message (说明), assertion_id (关联断言), run_id
- **保持现有格式**：`{run_id}_{step_index}.png`
- **存储位置**：`backend/data/screenshots/`
- **无需修改**：现有实现已满足需求
- **自动创建表** — 使用 SQLAlchemy create_all 在应用启动时自动创建/更新表
- **不使用 Alembic** — 开发阶段简单优先
- **适用场景**：v0.1 本地开发环境，SQLite 数据库

### Claude's Discretion
- Assertion 模型字段设计（type, expected_value, actual_value 具体类型）
- AssertionResult 模型字段细节
- RunRepository.get_steps() 返回格式
- 外键约束和级联删除策略

### Deferred Ideas (OUT OF SCOPE)
None — 讨论保持在 Phase 范围内
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DATA-01 | Assertion model exists with type, expected_value, actual_value fields | SQLAlchemy 2.0 Mapped patterns, existing Task model as template |
| DATA-02 | AssertionResult model exists with status, message fields | SQLAlchemy 2.0 Mapped patterns, ForeignKey to Run and Assertion |
| DATA-03 | Run-Assertion relationship is properly configured | SQLAlchemy cascade patterns, relationship() with back_populates |
| DATA-04 | Screenshot storage uses file system (not BLOB in database) | Already implemented in `backend/data/screenshots/`, no changes needed |
| DATA-05 | RunRepository.get_steps() method exists and works | Follow existing repository patterns in RunRepository |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| SQLAlchemy | 2.0+ | ORM and async database | Already in use, modern typed API with `Mapped[]` |
| aiosqlite | 0.20+ | Async SQLite driver | Already in use, required for async engine |
| Pydantic | 2.4+ | Schema validation | Already in use, `ConfigDict(from_attributes=True)` pattern |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest | 8.0+ | Testing framework | All repository tests |
| pytest-asyncio | 0.24+ | Async test support | Repository method tests |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| SQLAlchemy ORM | Raw SQL | No type safety, no relationship management |
| aiosqlite | aiosqlite + Alembic | Adds complexity for v0.1 single-developer project |

**Installation:**
Already installed via `uv sync`. No additional packages needed.

## Architecture Patterns

### Recommended Project Structure (Existing)
```
backend/
├── db/
│   ├── models.py          # Add Assertion, AssertionResult here
│   ├── repository.py      # Add get_steps() to RunRepository
│   ├── schemas.py         # Add AssertionResponse, AssertionResultResponse
│   └── database.py        # No changes needed
├── core/
│   └── assertion_service.py  # Already exists, no changes
└── api/
    └── schemas/
        └── index.py       # Pydantic Assertion already exists
```

### Pattern 1: SQLAlchemy 2.0 Model with Mapped Types
**What:** Use `Mapped[]` type hints with `mapped_column()` for type-safe ORM models
**When to use:** All new ORM models
**Example:**
```python
# Source: Existing backend/db/models.py pattern
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Assertion(Base):
    """断言模型 - 定义在 Task 级别"""
    __tablename__ = "assertions"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    task_id: Mapped[str] = mapped_column(String(8), ForeignKey("tasks.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # url_contains, text_exists, no_errors
    expected: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string or plain text

    # Relationship - Task has many Assertions
    task: Mapped["Task"] = relationship("Task", back_populates="assertions")
```

### Pattern 2: Cascade Delete Configuration
**What:** Use `cascade="all, delete-orphan"` on parent-side relationship for automatic cleanup
**When to use:** When child objects should be deleted when parent is deleted
**Example:**
```python
# Source: SQLAlchemy 2.0 Documentation - https://docs.sqlalchemy.org/en/20/orm/cascades.html
class Task(Base):
    # ... existing fields ...

    # Add assertions relationship with cascade delete
    assertions: Mapped[List["Assertion"]] = relationship(
        "Assertion",
        back_populates="task",
        cascade="all, delete-orphan"
    )
```

### Pattern 3: AssertionResult with Dual Foreign Keys
**What:** Model that references both Run and Assertion for result tracking
**When to use:** Storing assertion evaluation results per run
**Example:**
```python
class AssertionResult(Base):
    """断言结果模型 - 存储每次执行的断言结果"""
    __tablename__ = "assertion_results"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    run_id: Mapped[str] = mapped_column(String(8), ForeignKey("runs.id"), nullable=False)
    assertion_id: Mapped[str] = mapped_column(String(8), ForeignKey("assertions.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # pass, fail
    message: Mapped[str] = mapped_column(Text, nullable=True)  # 说明信息
    actual_value: Mapped[str] = mapped_column(Text, nullable=True)  # 实际值
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relationships
    run: Mapped["Run"] = relationship("Run", back_populates="assertion_results")
    assertion: Mapped["Assertion"] = relationship("Assertion", back_populates="results")
```

### Pattern 4: Repository get_steps() Method
**What:** Add method to RunRepository following existing repository patterns
**When to use:** Fetching all steps for a run with proper ordering
**Example:**
```python
# Source: Existing backend/db/repository.py pattern
class RunRepository:
    # ... existing methods ...

    async def get_steps(self, run_id: str) -> List[Step]:
        """获取执行记录的所有步骤"""
        stmt = select(Step).where(Step.run_id == run_id).order_by(Step.step_index)
        result = await self.session.execute(stmt)
        return list(result.scalars())
```

### Anti-Patterns to Avoid
- **Using BLOB for screenshots:** File paths only - existing implementation correct
- **Cascade on both sides of relationship:** Only configure cascade on parent side (Task->Assertion, Run->AssertionResult)
- **Forgetting back_populates:** Must match on both sides of bidirectional relationship
- **Using `class Config` in Pydantic v2:** Use `model_config = ConfigDict(from_attributes=True)` instead

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|------|
| UUID generation | Custom ID generator | `generate_id()` from models.py | Consistent 8-char format |
| Async session management | Custom session wrapper | `async_session` from database.py | Proper pool configuration |
| Cascade delete | Manual DELETE queries | SQLAlchemy cascade | Handles unloaded collections |
| Relationship loading | Manual JOIN queries | `selectinload()` or `refresh()` | Eager loading, N+1 prevention |

**Key insight:** SQLAlchemy 2.0's cascade with `delete-orphan` handles the complexity of deleting child objects automatically, including edge cases with unloaded collections.

## Common Pitfalls

### Pitfall 1: Cascade Delete Not Working
**What goes wrong:** Deleting parent doesn't delete children, or children are orphaned
**Why it happens:** Cascade not configured, or configured on wrong side of relationship
**How to avoid:** Always put `cascade="all, delete-orphan"` on the **parent** side (one-to-many), not the child side
**Warning signs:** Foreign key violations, orphan rows remaining in database

### Pitfall 2: Missing back_populates
**What goes wrong:** Relationship works one direction but not the other
**Why it happens:** `back_populates` string doesn't match the actual relationship name
**How to avoid:** Copy-paste relationship names exactly, test bidirectional access
**Warning signs:** AttributeError when accessing reverse relationship

### Pitfall 3: SQLite Foreign Key Constraints
**What goes wrong:** CASCADE DELETE at database level doesn't work
**Why it happens:** SQLite has foreign keys disabled by default
**How to avoid:** For v0.1, rely on SQLAlchemy cascade (not database-level ON DELETE). SQLAlchemy handles it in Python.
**Warning signs:** Orphaned rows after parent deletion

### Pitfall 4: Pydantic v2 Config Syntax
**What goes wrong:** `class Config` causes deprecation warnings or errors
**Why it happens:** Pydantic v2 uses different configuration syntax
**How to avoid:** Use `model_config = ConfigDict(from_attributes=True)` instead of `class Config`
**Warning signs:** Pydantic warnings in logs, schema validation failures

## Code Examples

Verified patterns from existing codebase:

### Existing Task Model (Template for Assertion)
```python
# Source: backend/db/models.py
class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    # ... other fields ...

    # 关系
    runs: Mapped[List["Run"]] = relationship("Run", back_populates="task")
```

### Existing Repository Pattern (Template for get_steps)
```python
# Source: backend/db/repository.py
class StepRepository:
    async def list_by_run(self, run_id: str) -> List[Step]:
        stmt = select(Step).where(Step.run_id == run_id).order_by(Step.step_index)
        result = await self.session.execute(stmt)
        return list(result.scalars())
```

### Existing Pydantic Schema Pattern
```python
# Source: backend/db/schemas.py
class StepResponse(BaseModel):
    """步骤响应"""
    id: str
    run_id: str
    step_index: int
    # ... other fields ...

    model_config = ConfigDict(from_attributes=True)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `class Config` | `model_config = ConfigDict()` | Pydantic v2 | Better type safety |
| SQLAlchemy 1.4 `Column()` | SQLAlchemy 2.0 `mapped_column()` | SQLAlchemy 2.0 | Better type inference |
| Sync SQLite | Async with aiosqlite | Phase 1 | Non-blocking I/O |

**Deprecated/outdated:**
- `class Config` in Pydantic v2: Use `model_config = ConfigDict(from_attributes=True)`
- `Column()` without `Mapped[]`: Use `mapped_column()` with `Mapped[]` type hint

## Open Questions

1. **Should AssertionResult have an `actual_value` field?**
   - What we know: REQUIREMENTS.md says Assertion needs expected_value, actual_value
   - What's unclear: Whether AssertionResult should also store actual_value (context from CONTEXT.md mentions it)
   - Recommendation: Include `actual_value` in AssertionResult since that's where the evaluation result is stored. Assertion only needs `expected`.

2. **Should we add an AssertionRepository or extend existing repositories?**
   - What we know: Existing pattern uses separate repository classes
   - What's unclear: Whether Assertion needs its own repository
   - Recommendation: For v0.1, add methods to TaskRepository for assertion CRUD (since assertions belong to tasks). Add AssertionResult methods to RunRepository.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.0+ with pytest-asyncio 0.24+ |
| Config file | pyproject.toml (tool.pytest.ini_options) |
| Quick run command | `uv run pytest backend/tests/unit/test_models.py -v -x` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DATA-01 | Assertion model with type, expected_value, actual_value fields | unit | `uv run pytest backend/tests/unit/test_models.py::test_assertion_model -v` | No - Wave 0 |
| DATA-02 | AssertionResult model with status, message fields | unit | `uv run pytest backend/tests/unit/test_models.py::test_assertion_result_model -v` | No - Wave 0 |
| DATA-03 | Run-Assertion relationship properly configured | unit | `uv run pytest backend/tests/unit/test_models.py::test_assertion_relationships -v` | No - Wave 0 |
| DATA-04 | Screenshot storage uses file system | integration | `uv run pytest backend/tests/integration/test_screenshot_storage.py -v` | Existing impl, verify |
| DATA-05 | RunRepository.get_steps() method exists and works | unit | `uv run pytest backend/tests/unit/test_repository.py::test_run_repository_get_steps -v` | No - Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/ -v -x`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_models.py` - test Assertion and AssertionResult models
- [ ] `backend/tests/unit/test_repository.py` - test RunRepository.get_steps() method
- [ ] Test fixtures for creating Task with Assertions, Run with AssertionResults

## Sources

### Primary (HIGH confidence)
- SQLAlchemy 2.0 Cascades Documentation - https://docs.sqlalchemy.org/en/20/orm/cascades.html
- Existing codebase: `backend/db/models.py` - established model patterns
- Existing codebase: `backend/db/repository.py` - established repository patterns
- Existing codebase: `backend/db/schemas.py` - established Pydantic patterns

### Secondary (MEDIUM confidence)
- SQLAlchemy 2.0 Basic Relationship Patterns - http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
- FastAPI + SQLAlchemy 2.0 Async Patterns - https://dev-faizan.medium.com/fastapi-sqlalchemy-2-0-modern-async-database-patterns-7879d39b6843

### Tertiary (LOW confidence)
- None - all findings verified against primary sources

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All libraries already in use, versions confirmed in pyproject.toml
- Architecture: HIGH - Existing codebase provides clear patterns to follow
- Pitfalls: HIGH - SQLAlchemy 2.0 cascade documentation is comprehensive

**Research date:** 2026-03-14
**Valid until:** 30 days - SQLAlchemy 2.0 is stable, patterns unlikely to change
