# Phase 60: 任务表单优化 - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning

<domain>
## Phase Boundary

移除任务表单中的"接口断言"tab 及 api_assertions 相关功能，仅保留业务断言配置区域。全面清理前端 UI、后端执行逻辑、SSE 事件、数据库字段。不保留旧数据兼容。

**Scope:**
- 前端：移除 TaskForm 中的 tab 切换和 api_assertions textarea，业务断言始终可见
- 后端：停止执行 api_assertions，删除 ApiAssertionService
- SSE：移除 api_assertion 事件类型
- 报告：移除 ApiAssertionResults 组件
- 数据库：移除 Task.api_assertions 列

**Out of Scope:**
- 业务断言（external_assertions）功能保持不变
- 前置条件功能保持不变
- 断言方法发现 API（/external-assertions/*）保持不变

</domain>

<decisions>
## Implementation Decisions

### 清理策略
- **D-01:** 全面清理 — 前端 tab 移除 + 后端执行逻辑删除 + SSE 事件移除 + 数据库字段移除
- **D-02:** 不兼容旧数据 — 旧报告中已有的 API 断言结果不再渲染，不做向后兼容处理
- **D-03:** 删除 `backend/core/api_assertion_service.py` 整个文件

### 前端改造
- **D-04:** 移除 TaskForm 中的 `assertionTab` 状态和 tab 切换 UI，业务断言区域始终可见
- **D-05:** 移除 api_assertions 相关的 state/handler（handleAddApiAssertion, handleRemoveApiAssertion, handleApiAssertionChange）
- **D-06:** 从 CreateTaskDto / UpdateTaskDto 中移除 api_assertions 字段
- **D-07:** 删除 `frontend/src/components/Report/ApiAssertionResults.tsx`
- **D-08:** 从 `useRunStream.ts` 中移除 api_assertion SSE 事件监听
- **D-09:** 从 StepTimeline/TimelineItem 类型中移除 api_assertion 相关的 assertion 类型（保留 external_assertion）

### 后端改造
- **D-10:** 从 `run_agent_background()` 中移除 api_assertions 执行循环
- **D-11:** 从 schemas.py 中移除 api_assertions 字段和 SSEApiAssertionEvent
- **D-12:** 从 models.py 中移除 Task.api_assertions 列（需要 Alembic migration 或直接 ALTER TABLE）
- **D-13:** 从 runs.py 的 create_run() 中移除 api_assertions 解析

### Claude's Discretion
- 具体文件删除顺序和分步策略
- TimelineItem 类型是否需要重命名或调整字段
- 数据库 migration 方式（Alembic vs 直接 SQL）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 前端核心文件
- `frontend/src/components/TaskModal/TaskForm.tsx` — 主表单组件，含 assertionTab 状态和双 tab UI（需大幅简化）
- `frontend/src/components/Report/ApiAssertionResults.tsx` — API 断言结果展示组件（需删除）
- `frontend/src/hooks/useRunStream.ts` — SSE hook，含 api_assertion 事件监听（需移除）
- `frontend/src/components/RunMonitor/StepTimeline.tsx` — 时间线组件，含 assertion 类型渲染
- `frontend/src/types/index.ts` — 类型定义，含 api_assertions 相关类型

### 后端核心文件
- `backend/core/api_assertion_service.py` — API 断言执行服务（需删除）
- `backend/api/routes/runs.py` — 运行路由，含 api_assertions 执行循环（需移除相关代码）
- `backend/db/schemas.py` — Pydantic schema，含 api_assertions 字段和 SSEApiAssertionEvent（需清理）
- `backend/db/models.py` — SQLAlchemy 模型，含 api_assertions 列（需移除）

### 前置阶段参考
- `.planning/phases/24-frontend-assertion-ui/24-CONTEXT.md` — Phase 24 创建了 tab 结构的决策
- `.planning/phases/58-exec-display/58-CONTEXT.md` — Phase 58 将 api_assertion 整合到统一时间线
- `.planning/phases/59-report-steps/59-CONTEXT.md` — Phase 59 报告步骤展示

</canonical_refs>

<code_context>
## Existing Code Insights

### 需要删除的文件
- `backend/core/api_assertion_service.py` — 整个文件
- `frontend/src/components/Report/ApiAssertionResults.tsx` — 整个文件

### 需要修改的前端文件
- `TaskForm.tsx` — 移除 assertionTab 状态(第63行)、tab 切换 UI(第458-481行)、API 断言内容区(第484-519行)、api_assertions 相关 handler(第137-153行)
- `types/index.ts` — 移除 api_assertions 字段、SSEApiAssertionEvent 类型、ApiAssertionFieldResult 类型
- `useRunStream.ts` — 移除 api_assertion 事件监听(第111-137行)
- `tasks.ts` — API 客户端，移除 api_assertions 请求字段

### 需要修改的后端文件
- `runs.py` — 移除 api_assertions 解析(第56-384行中的相关部分)和执行循环(第247-321行)
- `schemas.py` — 移除 api_assertions 字段和 SSEApiAssertionEvent
- `models.py` — 移除 api_assertions 列

### 需要保留不变
- `backend/api/routes/external_assertions.py` — 业务断言 API
- `backend/core/external_precondition_bridge.py` — 业务断言桥接
- `frontend/src/components/TaskModal/AssertionSelector.tsx` — 业务断言选择器
- `frontend/src/components/TaskModal/FieldParamsEditor.tsx` — 字段参数编辑器
- `frontend/src/api/externalAssertions.ts` — 业务断言 API 客户端

### 数据库变更
- `Task` 表的 `api_assertions` 列（TEXT 类型）需移除
- SQLite ALTER TABLE 支持 DROP COLUMN（SQLite 3.35.0+）

</code_context>

<specifics>
## Specific Ideas

- 业务断言区域不再需要 tab 外壳，直接作为表单的一个 section 展示
- 清理后 TaskForm 代码量预计减少约 100 行

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 60-task-form-opt*
*Context gathered: 2026-04-02*
