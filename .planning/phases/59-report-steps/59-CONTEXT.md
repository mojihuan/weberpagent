# Phase 59: 报告步骤展示 - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning

<domain>
## Phase Boundary

报告详情页的步骤列表中展示前置条件和断言步骤及其执行结果，按执行顺序交错排列。涉及后端数据持久化（前置条件结果存储）+ 后端 API 改动（统一排序列表）+ 前端报告页重构（移除独立区块，统一步骤列表）。

</domain>

<decisions>
## Implementation Decisions

### 后端数据持久化
- **D-01:** 前置条件结果需要持久化到数据库 — 当前只作为 SSE 事件发送，未存储。报告中 `precondition_results` 始终为 None（report_service.py:134 有 TODO 注释）
- **D-02:** 为三类步骤（UI 操作、前置条件、断言）分配全局递增的 sequence_number，用于确定交错排序
- **D-03:** 后端负责合并三类数据并按全局序号排序，返回统一的 ReportTimelineItem[] 列表

### 报告 API 改动
- **D-04:** 新增 `ReportTimelineItem` 联合类型（类似前端的 TimelineItem），包含 type 字段区分 'step' | 'precondition' | 'assertion' + 对应数据
- **D-05:** 报告详情 API (GET /api/reports/{id}) 返回 `timeline_items: ReportTimelineItem[]` 替代三个独立数组
- **D-06:** 保留现有的汇总统计字段（pass_rate、api_pass_rate、总步骤数、耗时等）在 API 响应中

### 前端步骤列表外观
- **D-07:** 前置条件/断言步骤复用 StepItem 的可展开卡片风格，与 UI 操作步骤视觉一致
- **D-08:** 三类步骤用不同颜色/图标区分（与 Phase 58 执行监控保持一致）：
  - UI 操作：蓝色 + 现有图标
  - 前置条件：黄色/橙色 + 文件图标
  - 断言：绿色/紫色 + 盾牌图标
- **D-09:** 展开内容因类型不同：
  - UI 步骤：截图 + AI 推理文本（现有行为不变）
  - 前置条件：代码 + 变量输出（variables）
  - 断言：断言名称 + 字段结果详情（field_results/actual_value）

### 现有独立区块处理
- **D-10:** 移除 `PreconditionSection`、`AssertionResults`、`ApiAssertionResults` 三个独立区块
- **D-11:** 保留顶部汇总统计区域（步骤数、成功率、耗时等卡片）

### Claude's Discretion
- PreconditionResult 数据库表的具体字段设计
- 全局 sequence_number 的分配机制（共享计数器 vs 时间戳回退）
- ReportTimelineItem 的具体类型定义（字段细节）
- 卡片展开/折叠的默认行为
- 具体图标和 Tailwind 颜色值

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心前端组件（需改动）
- `frontend/src/pages/ReportDetail.tsx` — 报告详情页面，需重构步骤列表区域
- `frontend/src/components/Report/StepItem.tsx` — 步骤卡片组件，需扩展支持前置条件/断言
- `frontend/src/components/Report/PreconditionSection.tsx` — 前置条件独立区块（将移除）
- `frontend/src/components/Report/AssertionResults.tsx` — UI 断言独立区块（将移除）
- `frontend/src/components/Report/ApiAssertionResults.tsx` — API 断言独立区块（将移除）
- `frontend/src/api/reports.ts` — 报告 API 模块，需更新类型和数据获取逻辑

### 类型定义
- `frontend/src/types/index.ts` — Step 类型、TimelineItem 联合类型（Phase 58 已创建）
- `backend/db/schemas.py` — 后端 Pydantic schemas，需新增 ReportTimelineItem

### 后端（需改动）
- `backend/api/routes/runs.py` — run_agent_background 函数，需添加全局序号分配 + 前置条件结果持久化
- `backend/api/routes/reports.py` — 报告 API 路由，需返回统一时间线列表
- `backend/db/models.py` — 数据库模型，需新增 PreconditionResult 模型 + 全局序号字段
- `backend/db/repository.py` — 数据访问层，需新增前置条件 CRUD
- `backend/services/report_service.py` — 报告服务，需实现合并排序逻辑

### 后端参考（不改）
- `backend/core/precondition_service.py` — 前置条件执行服务（执行逻辑不变）
- `backend/core/api_assertion_service.py` — API 断言执行服务（执行逻辑不变）
- `backend/core/agent_service.py` — Agent 服务（reasoning 文本生成逻辑不变，Phase 57 参考）

### Phase 58 参考
- `frontend/src/components/RunMonitor/StepTimeline.tsx` — 执行监控时间线，已实现三类步骤的视觉区分
- `frontend/src/hooks/useRunStream.ts` — SSE hook，TimelineItem 转换逻辑参考

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `StepItem.tsx` 的可展开卡片结构（状态图标、点击展开、内容区域）可直接复用/扩展
- Phase 58 的 `TimelineItem` 联合类型设计模式可参考
- Phase 58 的三类步骤视觉区分（图标+颜色）保持一致
- 现有的 `PreconditionSection` 中的变量展示代码可提取复用
- `ApiAssertionResults` 中的断言结果展示代码可提取复用
- Phase 57 的 `ReasoningText` 解析组件 — UI 步骤推理文本需要继续使用

### Established Patterns
- 后端 Pydantic schemas 用于 API 响应定义
- SQLAlchemy ORM 模型 + repository 模式用于数据访问
- 前端 React functional components + hooks + Tailwind CSS
- 报告详情页使用 `useEffect` 获取数据，非 SWR/React Query

### Integration Points
- `run_agent_background` — 执行过程中需要为每个事件分配全局序号并持久化前置条件结果
- `report_service.get_report_data()` — 需要从三张表查询数据并合并排序
- `ReportDetail.tsx` — 需要将三个独立区块替换为统一的步骤列表
- `StepItem.tsx` — 需要扩展为支持三种类型的泛化组件

### 关键发现：前置条件结果未持久化
后端 `report_service.py:134` 返回 `"precondition_results": None` 并注释 `TODO: Extract from run metadata when storage is implemented`。前置条件执行结果（成功/失败、变量输出、耗时）只作为 SSE 事件发送给前端，从未存入数据库。这是实现报告展示的前提阻塞项。

### 关键发现：无全局排序字段
Steps 有 `step_index`（整数序号），Assertion results 只有 `created_at`（时间戳），Precondition results 未存储。没有跨实体的全局排序机制。需要新增全局 sequence_number 或等效方案。

</code_context>

<specifics>
## Specific Ideas

- 前置条件/断言没有截图，展开内容区域不显示截图列
- 前置条件变量输出（variables）是 dict 格式，需友好展示（key-value pairs）
- 断言的 field_results 包含各字段断言的通过/失败详情
- 视觉风格与 Phase 58 执行监控保持一致（相同图标+配色方案）

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 59-report-steps*
*Context gathered: 2026-04-02*
