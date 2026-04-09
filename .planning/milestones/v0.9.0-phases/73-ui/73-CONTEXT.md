# Phase 73: 批量进度 UI - Context

**Gathered:** 2026-04-09
**Status:** Ready for planning

<domain>
## Phase Boundary

QA 启动批量执行后，在前端独立页面查看每个任务的实时状态（等待/执行中/完成/失败），点击卡片可跳转到该任务的执行监控详情（复用现有 RunMonitor）。

**Scope:**
- 独立批量进度页面 `/batches/:id`
- 批量执行启动后自动跳转到进度页面
- 卡片式任务列表展示（任务名 + 状态标签 + 耗时）
- 顶部整体进度统计（X/Y 完成）
- 每 2 秒轮询后端 API 更新状态
- 点击卡片跳转到 `/runs/:id`（复用 RunMonitor）
- 全部完成时 Toast 通知 + 摘要

**NOT in scope:**
- 批量取消操作（v2 BATCH-05）
- 批量重试失败任务（v2 BATCH-06）
- 批量执行汇总报告（v2 BATCH-04）
- SSE 实时推送（已决定用轮询）

</domain>

<decisions>
## Implementation Decisions

### 页面形式与入口
- **D-01:** 独立页面 `/batches/:id`，不在 Tasks 页内嵌或用弹窗。专注展示进度，用户可在侧边栏导航回任务列表
- **D-02:** 批量执行启动后（`batchesApi.create()` 返回 batch id 后）立即跳转到 `/batches/:id`，不等所有 run 创建完成
- **D-03:** 侧边栏导航不添加「批量进度」入口（批量进度通过跳转进入，不需要独立导航入口）

### 进度列表布局
- **D-04:** 卡片布局，每个任务一张卡片，展示任务名称 + 状态标签 + 耗时
- **D-05:** 顶部显示整体进度统计（如「3/10 完成」），可能带进度条
- **D-06:** 4 种状态视觉样式：等待（灰色）、执行中（蓝色动画）、完成（绿色勾）、失败（红色叉）

### 状态展示与交互
- **D-07:** 点击卡片任意位置直接跳转到 `/runs/:id`，复用现有 RunMonitor 页面查看执行详情
- **D-08:** 全部任务完成时 Toast 通知 + 摘要（如「全部完成：8 成功，2 失败」）
- **D-09:** 轮询每 2 秒获取最新状态，全部完成后停止轮询

### Claude's Discretion
- 卡片的具体 UI 样式和间距
- 状态标签的动画效果
- 整体进度统计的展示形式（纯文字 vs 带进度条）
- 卡片排列方式（单列 vs 响应式多列）
- 加载态和空状态的处理

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 后端 API（Phase 72 已实现）
- `backend/api/routes/batches.py` — GET /batches/{id} 返回 batch 状态 + runs 列表，GET /batches/{id}/runs 返回 run 摘要
- `backend/db/schemas.py` — BatchResponse、BatchRunSummary 的 Pydantic schema 定义
- `backend/db/repository.py` — BatchRepository.get_with_runs() 方法

### 前端已有代码
- `frontend/src/api/batches.ts` — batchesApi.getStatus() 和 batchesApi.getRuns() 已实现
- `frontend/src/types/index.ts` — Batch、BatchRunSummary 类型定义
- `frontend/src/pages/Tasks.tsx` — 批量执行启动逻辑（需修改：创建后跳转）
- `frontend/src/pages/RunMonitor.tsx` — 现有单任务执行监控页面（跳转目标）
- `frontend/src/App.tsx` — 路由配置（需添加 /batches/:id 路由）
- `frontend/src/components/TaskList/BatchExecuteDialog.tsx` — 批量执行确认弹窗

### 需求文档
- `.planning/REQUIREMENTS.md` — BATCH-03 需求定义
- `.planning/STATE.md` — 关键决策：轮询每 2 秒、Semaphore 默认 2 硬上限 4

### 前置阶段上下文
- `.planning/phases/72-批量执行引擎/72-CONTEXT.md` — Phase 72 所有决策，包含 Batch 模型、API 设计、前端组件

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `batchesApi.getStatus(batchId)` — 已实现，返回 Batch + runs 列表
- `batchesApi.getRuns(batchId)` — 已实现，返回 BatchRunSummary[]
- `BatchRunSummary` 类型 — 包含 id, task_id, task_name, status（前端类型已定义）
- `RunMonitor` 页面 — 完整的单任务执行监控，跳转目标
- `useTasks` hook — 轮询模式参考（setInterval + fetch）
- `TaskTable` 组件 — 复选框和行点击模式参考
- `toast` (sonner) — 已有 Toast 通知基础设施

### Established Patterns
- React Router 路由配置（App.tsx 中 BrowserRouter + Routes）
- `useNavigate()` 用于编程式导航
- `apiClient` 统一 API 调用和错误处理
- Tailwind CSS 样式（卡片、标签、布局）
- `useState` + `useEffect` 管理组件状态和副作用

### Integration Points
- `frontend/src/App.tsx` — 添加 `/batches/:id` 路由
- `frontend/src/pages/Tasks.tsx` — 修改 `handleBatchExecute`：创建批次后 navigate 到 `/batches/:id`
- `frontend/src/pages/BatchProgress.tsx` — 新建批量进度页面组件
- `frontend/src/api/batches.ts` — 已有 API 方法，可能需要补充字段
- `frontend/src/components/Layout.tsx` — 侧边栏不需要添加导航入口（通过跳转进入）

### Known Constraints
- 轮询每 2 秒，不做 SSE（STATE.md 已决定）
- BatchRunSummary 当前只有 id, task_id, task_name, status — 如果需要显示耗时，可能需要后端补充 started_at/finished_at 字段
- 点击卡片跳转到 RunMonitor 时，如果任务还在等待状态（未开始执行），RunMonitor 可能显示空内容

</code_context>

<specifics>
## Specific Ideas

- 卡片布局让每个任务有足够的视觉空间，状态标签颜色区分一目了然
- 顶部整体进度统计帮助 QA 快速把握批次整体进展
- 执行中任务可以显示动态效果（如脉冲动画），增强实时感
- 全部完成后的 Toast 摘要让 QA 立即知道结果，不用逐个查看

</specifics>

<deferred>
## Deferred Ideas

- 批量取消操作（BATCH-05）— v2 需求，一键停止所有等待和执行中的任务
- 批量重试失败任务（BATCH-06）— v2 需求
- 批量执行汇总报告（BATCH-04）— v2 需求，完成后显示通过/失败/错误数量
- 侧边栏添加「批量进度」导航入口 — 可在 v2 添加，当前通过跳转进入即可

</deferred>

---

*Phase: 73-ui*
*Context gathered: 2026-04-09*
