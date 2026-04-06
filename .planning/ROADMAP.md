# Roadmap: aiDriveUITest

## Milestones

- 🚧 **v0.8.2 浏览器模式差异调查** — Phases 63-64 (in progress)
- ✅ **v0.8.1 修复销售出库表格填写问题** — Phase 62 (shipped 2026-04-06)
- ✅ **v0.8.0 报告完善与 UI 优化** — Phases 57-61 (shipped 2026-04-03)
- ✅ **v0.7.0 更多操作边界测试** — Phases 52-56 (shipped 2026-04-01)
- ✅ **v0.6.3 Agent 可靠性优化** — Phases 48-51 (shipped 2026-03-28)
- ✅ **v0.6.2 回归原生 browser-use** — Phases 45-47 (shipped 2026-03-27)

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

### v0.8.2 浏览器模式差异调查 (In Progress)

**Milestone Goal:** 对比 v0.4.0 与当前版本在 browser 使用上的代码差异，找出为什么本地开发不再弹出浏览器窗口。只做分析，不修复。

- [x] **Phase 63: 代码对比分析** — 对比 v0.4.0 与当前版本 browser-use 初始化、Playwright 配置、版本升级、Agent 配置演变
- [ ] **Phase 64: 分析报告输出** — 输出结构化分析报告，含差异列表、根因分析、关联性评估

## Phase Details

### Phase 63: 代码对比分析
**Goal**: 完成所有维度的代码差异对比，识别导致浏览器窗口不再弹出的具体变更
**Depends on**: Nothing (first phase in milestone)
**Requirements**: DIFF-01, DIFF-02, DIFF-03, DIFF-04
**Success Criteria** (what must be TRUE):
  1. v0.4.0 和当前版本的 Agent 构造参数对比结果已记录，差异点明确列出
  2. v0.4.0 和当前版本的 Playwright 配置（headless/headed、启动参数）对比结果已记录，差异点明确列出
  3. browser-use 库版本变更记录完整，相关 API 变更（特别是 headless 默认值变化）已识别
  4. agent_service.py 中 Agent/Browser 配置的完整演变历史已梳理，每个版本的配置快照可追溯
**Plans**: 2 plans

Plans:
- [x] 63-01: 逐项对比 Agent 构造参数和 Playwright 配置 + headless DOM 渲染差异分析 (DIFF-01, DIFF-02)
- [x] 63-02: browser-use 版本对比 + Agent/Browser 配置演变时间线 (DIFF-03, DIFF-04)

### Phase 64: 分析报告输出
**Goal**: 将代码对比发现整理为结构化分析报告，给出根因分析和后续建议
**Depends on**: Phase 63
**Requirements**: RPT-01
**Success Criteria** (what must be TRUE):
  1. 报告包含完整的差异列表，每项差异附带 v0.4.0 值和当前值
  2. 报告包含根因分析，明确指出最可能导致浏览器窗口消失的变更
  3. 报告包含表格输入框定位问题与浏览器模式变更的关联性评估
  4. 报告给出后续修复建议（修复留给后续 milestone，本阶段不实施）
**Plans**: 1 plan

Plans:
- [ ] 64-01: Write structured analysis report with diff list, root cause, and recommendations

## Progress

**Execution Order:**
Phases execute in numeric order: 63 → 64

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 63. 代码对比分析 | 2/2 | Complete    | 2026-04-06 |
| 64. 分析报告输出 | 0/1 | Not started | - |

<details>
<summary>v0.8.1 修复销售出库表格填写问题 (Phase 62) — SHIPPED 2026-04-06</summary>

- [x] Phase 62: DOM Patch + Prompt 增强 — td cell 交互 + Section 9 click-to-edit 指导 (1/1 plan)

</details>

<details>
<summary>v0.8.0 报告完善与 UI 优化 (Phases 57-61) — SHIPPED 2026-04-03</summary>

- [x] Phase 57: AI 推理格式优化 — Eval/Verdict/Memory/Goal 分行彩色 badge (1/1 plan)
- [x] Phase 58: 执行步骤展示 — StepTimeline 统一时间线，前置条件/断言步骤交错排列 (1/1 plan)
- [x] Phase 59: 报告步骤展示 — 报告详情时间线，PreconditionResult + global sequence_number (2/2 plans)
- [x] Phase 60: 任务表单优化 — 删除 api_assertions，业务断言直接展示 (2/2 plans)
- [x] Phase 61: E2E 验证 — 6/6 检查 PASS (2/2 plans)

</details>

<details>
<summary>v0.7.0 更多操作边界测试 (Phases 52-56) — SHIPPED 2026-04-01</summary>

- [x] Phase 52: Prompt 增强 — 键盘操作 (3/3 plans) — completed 2026-03-30
- [x] Phase 53: Prompt 增强 — 表格交互 (3/3 plans) — completed 2026-03-31
- [x] Phase 54: 文件导入 (2/2 plans) — completed 2026-03-31
- [x] Phase 55: 断言参数调优与缓存断言 (skipped) — skipped 2026-04-01
- [x] Phase 56: E2E 综合验证 (2/2 plans) — completed 2026-03-31

</details>

<details>
<summary>v0.6.3 Agent 可靠性优化 (Phases 48-51) — SHIPPED 2026-03-28</summary>

- [x] Phase 48: 监控模块与 Agent 子类 (4/4 plans) — completed 2026-03-28
- [x] Phase 49: 提示词优化与参数调优 (2/2 plans) — completed 2026-03-28
- [x] Phase 50: AgentService 集成 (2/2 plans) — completed 2026-03-28
- [x] Phase 51: 端到端验证 (2/2 plans) — completed 2026-03-28

</details>

<details>
<summary>v0.6.2 回归原生 browser-use (Phases 45-47) — SHIPPED 2026-03-27</summary>

- [x] Phase 45: 代码移除 (5/5 plans) — completed 2026-03-26
- [x] Phase 46: 代码简化与测试 (2/2 plans) — completed 2026-03-26
- [x] Phase 47: 验证 (0/1 plans) — completed 2026-03-26

</details>

---

*Roadmap updated: 2026-04-06 — Phase 64 plans finalized*
