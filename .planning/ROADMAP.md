# Roadmap: aiDriveUITest

## Milestones

- 🚧 **v0.8.0 报告完善与 UI 优化** — Phases 57-61 (in progress)
- ✅ **v0.7.0 更多操作边界测试** — Phases 52-56 (shipped 2026-04-01)
- ✅ **v0.6.3 Agent 可靠性优化** — Phases 48-51 (shipped 2026-03-28)
- ✅ **v0.6.2 回归原生 browser-use** — Phases 45-47 (shipped 2026-03-27)

## Phases

**Phase Numbering:**
- Integer phases (57, 58, 59...): Planned milestone work
- Decimal phases (57.1, 57.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

### 🚧 v0.8.0 报告完善与 UI 优化 (In Progress)

**Milestone Goal:** 修复报告中缺失前置条件/断言步骤的问题，优化 AI 推理展示格式和任务表单交互

- [ ] **Phase 57: AI 推理格式优化** — Eval/Verdict/Memory/Goal 分行展示
- [ ] **Phase 58: 执行步骤展示** — 前置条件/断言步骤在 StepTimeline 中显示
- [ ] **Phase 59: 报告步骤展示** — 前置条件/断言步骤在报告详情中显示
- [ ] **Phase 60: 任务表单优化** — 移除断言 tab，仅保留业务断言
- [ ] **Phase 61: E2E 验证** — 验证所有变更端到端工作

<details>
<summary>✅ v0.7.0 更多操作边界测试 (Phases 52-56) — SHIPPED 2026-04-01</summary>

- [x] Phase 52: Prompt 增强 — 键盘操作 (3/3 plans) — completed 2026-03-30
- [x] Phase 53: Prompt 增强 — 表格交互 (3/3 plans) — completed 2026-03-31
- [x] Phase 54: 文件导入 (2/2 plans) — completed 2026-03-31
- [x] Phase 55: 断言参数调优与缓存断言 (skipped) — skipped 2026-04-01
- [x] Phase 56: E2E 综合验证 (2/2 plans) — completed 2026-03-31

</details>

<details>
<summary>✅ v0.6.3 Agent 可靠性优化 (Phases 48-51) — SHIPPED 2026-03-28</summary>

- [x] Phase 48: 监控模块与 Agent 子类 (4/4 plans) — completed 2026-03-28
- [x] Phase 49: 提示词优化与参数调优 (2/2 plans) — completed 2026-03-28
- [x] Phase 50: AgentService 集成 (2/2 plans) — completed 2026-03-28
- [x] Phase 51: 端到端验证 (2/2 plans) — completed 2026-03-28

</details>

<details>
<summary>✅ v0.6.2 回归原生 browser-use (Phases 45-47) — SHIPPED 2026-03-27</summary>

- [x] Phase 45: 代码移除 (5/5 plans) — completed 2026-03-26
- [x] Phase 46: 代码简化与测试 (2/2 plans) — completed 2026-03-26
- [x] Phase 47: 验证 (0/1 plans) — completed 2026-03-26

</details>

## Phase Details

### Phase 57: AI 推理格式优化
**Goal**: AI 推理过程中的 Eval/Verdict/Memory/Goal 各项独占一行，带标签高亮展示，替代当前 `|` 分隔的单行纯文本
**Depends on**: Nothing (self-contained formatting change)
**Requirements**: FMT-01, FMT-02, FMT-03
**Success Criteria** (what must be TRUE):
  1. 用户在执行监控中查看 ReasoningLog 时，看到 Eval/Verdict/Memory/Goal 各自独占一行，而非 `|` 分隔的单行文本
  2. 用户在报告详情页查看 StepItem 推理文本时，Eval/Verdict/Memory/Goal 标签有视觉高亮（如加粗或颜色标记）
  3. 不含标准标签的推理文本仍以纯文本正常展示，不会报错或显示异常
**Plans**: 1 plan

Plans:
- [ ] 57-01-PLAN.md — Create parseReasoning utility + ReasoningText component, integrate into ReasoningLog and StepItem
**UI hint**: yes

### Phase 58: 执行步骤展示
**Goal**: 执行监控的 StepTimeline 中显示前置条件和断言的执行步骤，与普通 UI 步骤按执行顺序交错排列
**Depends on**: Nothing (reads from existing SSE event stream)
**Requirements**: EXEC-01, EXEC-02, EXEC-03
**Success Criteria** (what must be TRUE):
  1. 用户在执行监控页面看到前置条件步骤出现在 StepTimeline 中，显示状态（成功/失败）、耗时和代码摘要
  2. 用户在执行监控页面看到断言步骤出现在 StepTimeline 中，显示状态（通过/失败）、耗时和断言名称
  3. 前置条件步骤、断言步骤与普通 UI 操作步骤按实际执行顺序交错排列在时间线中（不是分区域展示）
**Plans**: 1 plan

Plans:
- [x] 58-01-PLAN.md — Add TimelineItem union type, update useRunStream to unified timeline, rewrite StepTimeline for 3 item types, wire RunMonitor/RunHeader
**UI hint**: yes

### Phase 59: 报告步骤展示
**Goal**: 报告详情页的步骤列表中展示前置条件和断言步骤及其执行结果，按执行顺序交错排列
**Depends on**: Nothing (reads from report data stored in DB)
**Requirements**: RPT-01, RPT-02, RPT-03
**Success Criteria** (what must be TRUE):
  1. 用户在报告详情页看到前置条件步骤，显示执行状态（成功/失败）、耗时和变量输出信息
  2. 用户在报告详情页看到断言步骤，显示执行状态（通过/失败）、断言名称和失败信息（如有）
  3. 前置条件和断言步骤与普通步骤按实际执行顺序交错展示在同一个步骤列表中
**Plans**: 2 plans

Plans:
- [ ] 59-01-PLAN.md — Backend: PreconditionResult model, global sequence_number, timeline API
- [ ] 59-02-PLAN.md — Frontend: TimelineItemCard component, unified report timeline, remove old sections
**UI hint**: yes

### Phase 60: 任务表单优化
**Goal**: 任务表单移除"接口断言"和"业务断言"的 tab 切换，仅保留业务断言配置区域，简化表单交互
**Depends on**: Nothing (independent UI cleanup)
**Requirements**: FORM-01, FORM-02
**Success Criteria** (what must be TRUE):
  1. 用户在任务表单中不再看到"接口断言"/"业务断言"的 tab 切换控件
  2. 用户在任务表单中断言配置区域直接展示业务断言（AssertionSelector），无需切换 tab
  3. 表单中不再显示 api_assertions 的自由代码输入 textarea
**Plans**: 1 plan

Plans:
- [ ] 60-01-PLAN.md — To be planned
**UI hint**: yes

### Phase 61: E2E 验证
**Goal**: 验证 v0.8.0 所有变更在端到端流程中正确工作，无退化
**Depends on**: Phase 57, Phase 58, Phase 59, Phase 60
**Requirements**: (cross-cutting verification, no new requirements)
**Success Criteria** (what must be TRUE):
  1. 创建一个包含前置条件和断言的测试任务，执行后执行监控中正确显示所有步骤（含推理格式化）
  2. 执行完成后，报告详情页正确展示前置条件步骤、断言步骤和普通步骤，推理文本格式化显示
  3. 创建新任务时表单中断言区域直接显示业务断言配置，无 tab 切换
  4. 已有任务的报告数据不受影响，历史报告正常展示
**Plans**: 1 plan

Plans:
- [ ] 61-01-PLAN.md — To be planned

## Progress

**Execution Order:**
Phases execute in numeric order: 57 → 58 → 59 → 60 → 61

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 57. AI 推理格式优化 | v0.8.0 | 0/? | Complete    | 2026-04-02 |
| 58. 执行步骤展示 | v0.8.0 | 1/1 | Complete    | 2026-04-02 |
| 59. 报告步骤展示 | v0.8.0 | 0/? | Not started | - |
| 60. 任务表单优化 | v0.8.0 | 0/? | Not started | - |
| 61. E2E 验证 | v0.8.0 | 0/? | Not started | - |

---
*Roadmap updated: 2026-04-02 — v0.8.0 milestone roadmap created*
