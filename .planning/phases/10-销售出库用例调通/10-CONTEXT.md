# Phase 10: 销售出库用例调通 - Context

**Gathered:** 2026-03-17
**Status:** Ready for planning

<domain>
## Phase Boundary

验证复杂测试用例的端到端执行：前置条件 + 动态数据 + API 断言。

这是一个 **调通/验证阶段**，验证 v0.2 已实现的功能能否协同工作完成一个销售出库测试。不开发新语法，使用现有机制。

</domain>

<decisions>
## Implementation Decisions

### 前置条件配置
- 使用 **现有 context['变量名']** 语法，不实现 self.pre 新语法
- 代码示例：`context['operations'] = get_operations(['FA1', 'HC1'])`
- ERP API 通过外部模块调用 (ERP_API_MODULE_PATH 已配置)

### 动态数据引用
- 步骤描述中使用 **Jinja2 {{变量名}}** 语法
- 示例：`输入销售单号 {{order_no}}`
- 随机数使用全局函数：`sf_waybill()`、`random_phone()`、`random_imei()` 等

### 数据传递
- **自动传递**：context 在 PreconditionService 和 ApiAssertionService 之间共享
- 无需显式调用传递方法

### 用例规模
- **简版 5-8 步**：创建销售单 → 审核 → 出库 → 验证
- 核心流程验证，不追求完整业务流程覆盖

### API 断言范围
- **完整验证**：
  - 销售单号存在
  - 状态正确
  - 创建时间合理
  - 库存扣减正确
- 使用 ApiAssertionService 现有能力（时间断言、精确匹配、包含匹配）

### 失败处理
- **Fail-fast**：任一前置条件失败，立即终止整个测试（现有行为）
- 每次执行创建新 Run，保留调通记录
- 发现的 Bug 记录，留给 Phase 11 修复

### Claude's Discretion
- 具体的销售出库步骤描述
- API 断言的具体字段名和期望值
- 截图验证点选择

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 执行引擎
- `backend/core/agent_service.py` — AgentService，Browser-Use 封装
- `backend/core/precondition_service.py` — 前置条件执行，context 共享
- `backend/core/api_assertion_service.py` — API 断言，时间/数据验证

### 前端组件
- `frontend/src/components/TaskModal/TaskForm.tsx` — 任务创建表单，支持前置条件和 API 断言配置
- `frontend/src/pages/RunMonitor.tsx` — 实时监控页面
- `frontend/src/pages/ReportDetail.tsx` — 报告详情页面
- `frontend/src/components/Report/ApiAssertionResults.tsx` — API 断言结果展示

### 随机数生成
- `backend/core/random_generators.py` — sf_waybill, random_phone, random_imei 等

### 环境配置
- `.env.example` — 环境变量模板 (ERP_API_MODULE_PATH)
- `backend/config/__init__.py` — 配置加载

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **PreconditionService** — exec() 执行 Python 代码，context 存储变量
- **ApiAssertionService** — 时间断言、精确匹配、包含匹配、小数近似
- **TaskForm.tsx** — 已支持前置条件和 API 断言的多行文本输入
- **Jinja2 变量替换** — substitute_variables() 方法已实现

### Established Patterns
- 前置条件通过 `context['变量名']` 存储结果
- 步骤描述中用 `{{变量名}}` 引用
- 前置条件失败时立即终止 (Fail-fast)
- API 断言收集所有结果，不终止执行

### Integration Points
- 前端创建任务 → `/api/tasks` POST (含 preconditions, api_assertions)
- 执行任务 → `/api/runs/start` POST
- 前置条件执行 → PreconditionService.execute_all()
- API 断言执行 → ApiAssertionService.execute_all()
- 查看报告 → `/reports/{run_id}` GET

</code_context>

<specifics>
## Specific Ideas

- 销售出库是验证 v0.2 功能的复杂场景，包含前置条件、动态数据、API 断言
- 使用已有的外部 ERP API 模块进行前置条件数据准备
- 简版流程足够验证系统功能，不需要完整业务流程

</specifics>

<deferred>
## Deferred Ideas

- **self.pre 新语法** — 如需要更友好的 API，可在后续版本实现
- **完整业务流程** — 10-15 步骤的完整销售流程，可在后续扩展
- **Bug 修复** — 调通过程中发现的 Bug 留给 Phase 11 修复
- **文档指南** — Phase 12 提供 QA 填写指南

</deferred>

---

*Phase: 10-销售出库用例调通*
*Context gathered: 2026-03-17*
