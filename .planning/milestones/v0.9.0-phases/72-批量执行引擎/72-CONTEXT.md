# Phase 72: 批量执行引擎 - Context

**Gathered:** 2026-04-08
**Status:** Ready for planning

<domain>
## Phase Boundary

QA 勾选多个 Task 后一键启动并行执行，系统使用 Semaphore 控制并发数防止服务器 OOM，Batch 模型追踪整个批次进度。

**Scope:**
- Batch 确认弹窗（任务数量摘要 + 并发数滑块）
- Batch 数据模型（batch_id、并发数、状态、关联 runs）
- BatchExecutionService（Semaphore 并发控制、任务调度、错误隔离）
- 独立 batches 路由（创建批次、查询进度、查询包含的 runs）
- 二级状态追踪（batch pending/running/completed + run pending/running/success/failed）
- 前端 BatchActions 扩展（添加「批量执行」按钮 + 确认弹窗）

**NOT in scope:**
- 批量进度 UI 页面（Phase 73）
- 批量取消（v2 BATCH-05）
- 批量重试（v2 BATCH-06）
- 汇总报告（v2 BATCH-04）

</domain>

<decisions>
## Implementation Decisions

### 触发方式
- **D-01:** 点击「批量执行」弹出确认弹窗，弹窗显示已选任务数量 + 并发数滑块（1-4，默认 2）+ 确认/取消按钮
- **D-02:** 「批量执行」按钮添加到现有 BatchActions 组件中，与「设为就绪」和「批量删除」并列
- **D-03:** 确认弹窗为简单摘要形式（任务数量 + 并发数），不列出任务清单

### Batch 模型设计
- **D-04:** 引入 Batch 数据库表，字段包括 id、concurrency（并发数）、status、created_at、finished_at
- **D-05:** Batch 与 Run 为一对多关系，Batch 包含多个 Run，每个 Run 关联一个 Batch
- **D-06:** 二级状态流转 — Batch 有 pending/running/completed 三种状态；Run 保持 pending/running/success/failed/stopped
- **D-07:** Batch 状态由子 Run 状态聚合：所有 Run 终态（success/failed/stopped）后 Batch 变为 completed

### 后端并发架构
- **D-08:** 创建独立 BatchExecutionService 类封装 Semaphore、任务调度、错误隔离、进度更新
- **D-09:** BatchExecutionService 使用 asyncio.Semaphore 控制并发，默认 2，硬上限 4（防止服务器 OOM）
- **D-10:** 单个任务执行失败不影响其他任务继续执行，错误信息记录到对应 Run
- **D-11:** 复用现有 run_agent_background 函数执行单个任务，BatchExecutionService 负责协调调度

### API 路由设计
- **D-12:** 创建独立的 batches 路由模块（backend/api/routes/batches.py），不挂在现有 runs 路由下
- **D-13:** POST /batches — 创建批次（接收 task_ids + concurrency），创建 Batch 记录 + 为每个 task 创建 Run，启动并行执行
- **D-14:** GET /batches/{id} — 查询批次进度（返回 batch 状态 + 各 run 的状态摘要）
- **D-15:** GET /batches/{id}/runs — 查询批次包含的 run 列表（用于 Phase 73 批量进度 UI）

### Claude's Discretion
- Batch 模型具体字段类型和默认值
- 确认弹窗组件的具体 UI 样式和布局
- 并发数滑块的步长和默认值展示
- BatchExecutionService 的内部实现细节（信号量分配、错误处理流程）
- API 响应的具体 JSON 结构

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 执行引擎核心
- `backend/api/routes/runs.py` — 现有单任务执行流程（create_run、run_agent_background），批量执行复用此逻辑
- `backend/core/agent_service.py` — AgentService.run_with_cleanup() 单任务执行核心，每次独立 browser session
- `backend/core/event_manager.py` — SSE 事件管理器，per-run 事件发布/订阅

### 数据模型与仓库
- `backend/db/models.py` — 现有 ORM 模型（Task, Run, Step），Batch 模型在此添加
- `backend/db/schemas.py` — Pydantic schemas，Batch 相关 schema 在此添加
- `backend/db/repository.py` — 现有 Repository 模式（TaskRepository, RunRepository），BatchRepository 在此添加
- `backend/db/database.py` — async_session 工厂函数，BatchExecutionService 需要独立的数据库会话

### 路由注册
- `backend/api/main.py` — FastAPI app 初始化和路由注册，batches 路由在此 include

### 前端参考
- `frontend/src/components/TaskList/BatchActions.tsx` — 现有批量操作组件，「批量执行」按钮在此添加
- `frontend/src/components/TaskList/TaskTable.tsx` — 已有多选 checkbox + selectedIds 机制
- `frontend/src/api/tasks.ts` — tasksApi 模式参考，batch API 方法按同样模式添加
- `frontend/src/api/client.ts` — apiClient 基础配置
- `frontend/src/pages/Tasks.tsx` — Tasks 页面状态管理，控制 BatchActions 回调

### 需求文档
- `.planning/REQUIREMENTS.md` — BATCH-01, BATCH-02 需求定义
- `.planning/STATE.md` — 关键决策：Semaphore 默认 2 硬上限 4、轮询每 2 秒

### 前置阶段上下文
- `.planning/phases/71-批量导入工作流/71-CONTEXT.md` — Phase 71 决策和代码上下文

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `BatchActions.tsx` — 已有批量操作栏框架（selectedCount, onBatchDelete, onBatchSetReady），添加 onBatchExecute prop 即可扩展
- `TaskTable.tsx` — 已有完整多选机制（selectedIds, onSelectAll, onToggleSelect），无需修改
- `run_agent_background()` — 完整的单任务执行链（前置条件 → agent → 断言 → 报告 → SSE 事件），批量执行直接复用
- `AgentService.run_with_cleanup()` — 每次创建独立 browser session，天然支持并行（无共享状态）
- `event_manager` — per-run 事件发布/订阅，各 run 的事件独立
- `TaskRepository.create()` / `RunRepository.create()` — 数据库操作模式参考

### Established Patterns
- FastAPI BackgroundTasks 用于后台异步执行
- APIRouter + Depends 模式用于路由
- Repository 模式封装数据库操作
- Pydantic BaseModel 用于请求/响应验证
- SQLite WAL 模式（注意并发写锁竞争）
- 前端 apiClient 统一 API 调用

### Integration Points
- `backend/db/models.py` — 添加 Batch ORM 模型，Run 模型添加 batch_id 外键
- `backend/db/repository.py` — 添加 BatchRepository
- `backend/api/routes/batches.py` — 新建独立路由文件
- `backend/api/main.py` — include batches 路由
- `frontend/src/components/TaskList/BatchActions.tsx` — 添加「批量执行」按钮
- `frontend/src/api/tasks.ts`（或新建 batches.ts）— 添加 batch API 方法
- `frontend/src/pages/Tasks.tsx` — 添加批量执行回调 + 确认弹窗状态管理

### Known Constraints
- Semaphore 默认 2，硬上限 4 — 防止单服务器 OOM（STATE.md 已决定）
- 批量进度使用轮询每 2 秒，不做 SSE multiplexing（STATE.md 已决定）
- SQLite WAL 模式下并发写锁竞争 — 批量执行中多个 Run 并行写入步骤数据需注意
- 每个 Run 需要独立的数据库会话（async_session 工厂函数）

</code_context>

<specifics>
## Specific Ideas

- 确认弹窗为简单摘要形式：显示「已选 X 个任务」，并发数滑块 1-4 默认 2，确认/取消按钮
- 「批量执行」按钮放在 BatchActions 组件中「设为就绪」和「批量删除」按钮旁边
- BatchExecutionService 作为独立服务类，与 AgentService 同级放在 backend/core/

</specifics>

<deferred>
## Deferred Ideas

- 批量取消操作（BATCH-05）— v2 需求，一键停止所有等待和执行中的任务
- 批量重试失败任务（BATCH-06）— v2 需求
- 批量执行汇总报告（BATCH-04）— v2 需求，完成后显示通过/失败/错误数量
- 批量进度 UI 页面 — Phase 73 范围

</deferred>

---

*Phase: 72-批量执行引擎*
*Context gathered: 2026-04-08*
