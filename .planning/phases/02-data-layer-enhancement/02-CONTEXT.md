# Phase 2: Data Layer Enhancement - Context

**Gathered:** 2026-03-14
**Status:** Ready for planning

<domain>
## Phase Boundary

数据库模型和存储优化 — 添加 Assertion/AssertionResult ORM 模型，配置 Run-Assertion 关系，确认截图文件存储方式，实现 RunRepository.get_steps() 方法。

**不包含：** 断言服务逻辑（Phase 3）、前端显示（Phase 4）

</domain>

<decisions>
## Implementation Decisions

### 断言模型关联层级
- **关联 Task** — 断言定义在 Task 上，所有 Run 共享同一组断言
- **优点**：修改断言后新执行自动应用，适合回归测试场景
- **关系**：Task → Assertion（一对多）

### 断言结果存储层级
- **Run 级别** — AssertionResult 关联到 Run，每个 Run 有一组断言结果
- **字段**：status (pass/fail), message (说明), assertion_id (关联断言), run_id
- **优点**：简单直接，适合"整体通过/失败"的测试场景

### 截图存储路径
- **保持现有格式**：`{run_id}_{step_index}.png`
- **存储位置**：`backend/data/screenshots/`
- **无需修改**：现有实现已满足需求

### 数据库迁移策略
- **自动创建表** — 使用 SQLAlchemy create_all 在应用启动时自动创建/更新表
- **不使用 Alembic** — 开发阶段简单优先
- **适用场景**：v0.1 本地开发环境，SQLite 数据库

### Claude's Discretion
- Assertion 模型字段设计（type, expected_value, actual_value 具体类型）
- AssertionResult 模型字段细节
- RunRepository.get_steps() 返回格式
- 外键约束和级联删除策略

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/db/models.py`: 现有 Task, Run, Step, Report ORM 模型
- `backend/db/repository.py`: TaskRepository, RunRepository, StepRepository 模式
- `backend/core/assertion_service.py`: 已有断言服务逻辑
- `backend/api/schemas/index.py`: Assertion Pydantic 模型

### Established Patterns
- Repository pattern for data access
- SQLAlchemy async engine with aiosqlite
- 8-char UUID for primary keys
- Pydantic schemas for API validation

### Integration Points
- 新模型添加到 `backend/db/models.py`
- 新 repository 方法添加到 `backend/db/repository.py`
- 断言结果通过 RunRepository 查询

### 已实现功能（无需修改）
- ✓ 截图文件存储 (`backend/data/screenshots/`)
- ✓ 断言服务逻辑 (`AssertionService`)
- ✓ 断言 Schema (`Assertion` Pydantic)

</code_context>

<specifics>
## Specific Ideas

- 断言类型参考现有 `AssertionService`：url_contains, text_exists, no_errors
- 模型设计参考现有 Task/Run/Step 模式
- Repository 方法参考现有 TaskRepository 模式

</specifics>

<deferred>
## Deferred Ideas

None — 讨论保持在 Phase 范围内

</deferred>

---

*Phase: 02-data-layer-enhancement*
*Context gathered: 2026-03-14*
