# Phase 61: E2E 验证 - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning

<domain>
## Phase Boundary

验证 v0.8.0 所有变更（Phase 57-60）在端到端流程中正确工作，无退化。纯验证 Phase，不修改代码。

**包含：**
- 自动化预检查（pytest + 前端 build）
- 手动 E2E 验证：通过平台 UI 创建/执行测试任务
- 按 ROADMAP 4 条 Success Criteria 逐条验证
- 历史报告向后兼容性检查
- 验证结果文档记录

**不包含：**
- 修改代码或配置
- 修复发现的 bug（仅记录分析）
- 新增测试用例或功能

</domain>

<decisions>
## Implementation Decisions

### 测试用例设计
- **D-01:** 一个综合测试用例覆盖全部 v0.8.0 变更。创建一个采购相关场景（如采购入库），配置前置条件（查询供应商信息）+ 业务断言（验证入库数量），确保能触发 AI 推理生成 Eval/Verdict/Memory/Goal
- **D-02:** 综合用例覆盖 Phase 57-60 所有功能：执行监控中查看推理格式+步骤时间线，完成后查看报告时间线，创建过程中确认表单无 tab

### 验证方法与环境
- **D-03:** 本地开发机执行。方便查看日志和调试，与 Phase 56 验证模式一致（Phase 56 D-03）
- **D-04:** 通过平台 UI 手动执行。创建任务 → 执行 → 观察监控 → 查看报告，人工判断每个场景是否通过。与 Phase 51/56 验证模式一致（Phase 51 D-03）
- **D-05:** 手动 E2E 之前先跑自动化预检查：`uv run pytest backend/tests/ -v` + `cd frontend && npm run build`。确保代码层面无回归问题

### 通过标准
- **D-06:** 按 ROADMAP Phase 61 的 4 条 Success Criteria 逐条验证：
  1. 创建含前置条件+断言的测试任务，执行后监控中正确显示所有步骤（含推理格式化）
  2. 执行完成后，报告详情页正确展示前置条件步骤、断言步骤和普通步骤，推理文本格式化显示
  3. 创建新任务时表单中断言区域直接显示业务断言配置，无 tab 切换
  4. 已有任务的报告数据不受影响，历史报告正常展示

### 结果记录
- **D-07:** 在 `docs/test-steps/` 下新建 v0.8.0 验证结果文档，记录每个 Success Criteria 的验证结果和截图证据。与 Phase 56 验证报告模式一致（Phase 56 D-05）
- **D-08:** 发现问题仅记录分析，不做自动修复。保持验证 Phase 纯洁性（Phase 56 D-06）

### Plan 结构
- **D-09:** 两个 Plan。Plan 61-01: 运行自动化预检查 + 创建综合测试用例，Plan 61-02: 执行 E2E 测试并生成验证结果文档

### Claude's Discretion
- 综合测试用例的具体测试步骤描述
- 验证结果文档的具体格式
- 失败原因分析的具体深度

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求与路线图
- `.planning/REQUIREMENTS.md` — v0.8.0 完整需求定义（FMT-01/02/03, EXEC-01/02/03, RPT-01/02/03, FORM-01/02）
- `.planning/ROADMAP.md` — Phase 61 成功标准和计划结构

### 先前阶段 Context（验证目标）
- `.planning/phases/57-ai/57-CONTEXT.md` — Phase 57 AI 推理格式优化决策
- `.planning/phases/58-exec-display/58-CONTEXT.md` — Phase 58 执行步骤展示决策
- `.planning/phases/59-report-steps/59-CONTEXT.md` — Phase 59 报告步骤展示决策
- `.planning/phases/60-task-form-opt/60-CONTEXT.md` — Phase 60 任务表单优化决策

### 先前 E2E 验证参考
- `.planning/phases/56-e2e/56-CONTEXT.md` — Phase 56 E2E 验证模式参考
- `.planning/phases/51-e2e-verification/51-CONTEXT.md` — Phase 51 E2E 验证模式参考

### 前端核心文件（验证时观察目标）
- `frontend/src/components/RunMonitor/ReasoningLog.tsx` — 推理格式化展示
- `frontend/src/components/RunMonitor/StepTimeline.tsx` — 统一执行时间线
- `frontend/src/components/Report/TimelineItemCard.tsx` — 报告步骤卡片
- `frontend/src/pages/ReportDetail.tsx` — 报告详情页
- `frontend/src/components/TaskModal/TaskForm.tsx` — 任务表单（无 tab）

### 后端核心文件（自动化测试覆盖）
- `backend/tests/unit/` — 全量测试目录
- `backend/core/report_service.py` — 报告数据服务（timeline_items 构建）
- `backend/api/routes/runs.py` — 执行路由（global_seq + SSE 事件）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- 全量测试已有 28+ 个测试文件（`backend/tests/unit/` 和 `backend/tests/`），可直接运行 `uv run pytest backend/tests/ -v`
- 前端 build 验证：`cd frontend && npm run build`
- 平台 UI 已部署，本地可通过 `uv run uvicorn backend.api.main:app --reload --port 8080` 启动
- 已有测试步骤文档目录 `docs/test-steps/` 用于存放验证结果

### Established Patterns
- E2E 验证通过平台 UI 手动执行（Phase 51 D-03）
- 逐场景判定通过/失败（Phase 56 D-04）
- 验证结果文档记录格式：场景名 + 状态 + 说明 + 截图证据
- 本地开发机验证 + 日志查看（Phase 56 D-03）
- per-run 日志存储在 `outputs/` 目录

### Integration Points
- 平台前端 → API → AgentService.run_with_streaming() → MonitoredAgent → browser-use
- SSE 事件流：precondition → step → external_assertions → finished
- 报告数据：DB → report_service.get_report_data() → API → ReportDetail.tsx
- 任务表单：TaskForm.tsx → API → runs.py

### 注意事项
- REQUIREMENTS.md 中 FMT-01/02/03 仍标记为 pending，但 Phase 57 已 Complete。E2E 验证时需确认推理格式化确实生效，并更新 REQUIREMENTS.md 状态
- Phase 60 移除了 api_assertions 列，历史任务的报告可能受影响——需验证旧报告展示无异常

</code_context>

<specifics>
## Specific Ideas

- 验证顺序：先自动化预检查 → 创建综合测试任务（确认表单 D） → 执行任务（观察监控 A+B） → 完成后查看报告（C） → 打开历史报告（D）
- 验证重点：推理文本是否显示彩色 badge（Eval 紫/Verdict 绿/Memory 橙/Goal 蓝），时间线中三类步骤是否交错排列，历史报告是否正常回退展示

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 61-e2e*
*Context gathered: 2026-04-02*
