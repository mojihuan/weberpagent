# Roadmap: aiDriveUITest

## Milestones

- 🚧 **v0.10.10 表单填写优化** — Phases 114-115 (in progress)
- ✅ **v0.10.9 逐步代码生成** — Phases 111-113 (shipped 2026-04-29)
- ✅ **v0.10.8 生成测试代码前置条件与断言步骤** — Phases 108-110 (shipped 2026-04-27)
- ✅ **v0.10.7 生成测试代码行为优化** — Phases 105-107 (shipped 2026-04-27)
- ✅ **v0.10.6 生成测试代码稳定可用** — Phases 102-104 (shipped 2026-04-25)
- ✅ **v0.10.5 生成测试代码修复与优化** — Phases 99-101 (shipped 2026-04-24)
- ✅ **v0.10.4 Playwright 代码验证与任务管理集成** — Phases 97-98 (shipped 2026-04-24)
- ✅ **v0.10.3 DOM 深度修复 - 表格单元格选择精确性** — Phases 94-96 (shipped 2026-04-23)
- ✅ **v0.10.2 测试验证与代码可用性修复** — Phases 90-93 (shipped 2026-04-23)
- ✅ **v0.10.1 代码登录及 Agent 复用登录的浏览器状态** — Phases 86-89 (shipped 2026-04-21)
- ✅ **v0.10.0 Agent 执行速度优化** — Phases 82-85 (shipped 2026-04-18)
- ✅ **v0.9.2 Cookie 预注入免登录** — Phases 79-81 (shipped 2026-04-17)
- ✅ **v0.9.1 ERP 全面集成重构** — Phases 74-78 (shipped 2026-04-12)
- ✅ **v0.9.0 Excel 批量导入功能开发** — Phases 70-73 (shipped 2026-04-09)
- ✅ **v0.8.4 基于 v0.8.3 的研究优化** — Phases 67-69 (shipped 2026-04-07)
- ✅ **v0.8.3 分析报告差距对表格填写影响** — Phases 65-66 (shipped 2026-04-06)
- ✅ **v0.8.2 浏览器模式差异调查** — Phases 63-64 (shipped 2026-04-06)
- ✅ **v0.8.1 修复销售出库表格填写问题** — Phase 62 (shipped 2026-04-06)
- ✅ **v0.8.0 报告完善与 UI 优化** — Phases 57-61 (shipped 2026-04-03)
- ✅ **v0.7.0 更多操作边界测试** — Phases 52-56 (shipped 2026-04-01)
- ✅ **v0.6.3 Agent 可靠性优化** — Phases 48-51 (shipped 2026-04-03)
- ✅ **v0.6.2 回归原生 browser-use** — Phases 45-47 (shipped 2026-04-03)

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

### v0.10.10 表单填写优化 (In Progress)

**Milestone Goal:** 修复 ERP 表格内 input DOM 检测机制，不再依赖 placeholder 精确匹配，使 Agent 能正确操作表格内的表单字段

- [ ] **Phase 114: DOM Patch 核心修复** — 重构 td 内 input 检测逻辑，消除 placeholder 依赖
- [ ] **Phase 115: Prompt 优化与 E2E 验证** — 更新 Section 9 prompt 并验证销售出库表单填写

## Phase Details

### Phase 114: DOM Patch 核心修复
**Goal**: td 内所有可见 input 都能被 DOM patch 正确检测并分配独立 interactive index，Agent 不再误点 td 单元格
**Depends on**: Nothing (first phase of milestone, builds on v0.10.3 DOM patch work)
**Requirements**: DOM-01, DOM-02, DOM-03, DOM-04
**Success Criteria** (what must be TRUE):
  1. `find_elements('table tr td input')` 返回的每个可见 input 都分配了独立的 interactive index，无论其 placeholder 值是什么
  2. 包含可见 input 的 td 单元格不再被标记为 interactive（Agent 不会点击 td 而跳过内部 input）
  3. 每个被检测到的 td 内 input 在 DOM dump 中带有列头语义注释（如 `<!-- 列: 销售金额 -->`），而非依赖 placeholder 关键字
  4. 运行日志中记录了实际发现的 td 内 input placeholder 值列表，便于排查后续不匹配问题
**Plans**: 1 plan

Plans:
- [x] 114-01-PLAN.md — 重构 input 检测 + td guard + 诊断日志 + 列头注释 (DOM-01/02/03/04)

### Phase 115: Prompt 优化与 E2E 验证
**Goal**: Agent prompt 能指导两种表格 input 模式，销售出库场景表单填写 E2E 通过且全量回归无破坏
**Depends on**: Phase 114
**Requirements**: PRMT-01, VAL-01, VAL-02
**Success Criteria** (what must be TRUE):
  1. prompts.py Section 9 同时包含 click-to-edit 和始终可见 input 两种模式的操作指导，带有行+列注释定位示例
  2. 销售出库场景 E2E 测试中，销售金额、物流费用等表格字段被 Agent 正确填写（不再出现 10+ 步重试失败）
  3. 全量回归测试通过（pytest suite 0 failed, 0 errors）
**Plans**: 2 plans

Plans:
- [x] 115-01-PLAN.md — Rewrite Section 9 with dual-mode five-segment structure (PRMT-01)
- [ ] 115-02-PLAN.md — Add logistics fee E2E test + full regression (VAL-01, VAL-02)

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 114. DOM Patch 核心修复 | v0.10.10 | 1/1 | Complete    | 2026-04-29 |
| 115. Prompt 优化与 E2E 验证 | v0.10.10 | 1/2 | In Progress|  |

<details>
<summary>✅ v0.10.9 逐步代码生成 (Phases 111-113) — SHIPPED 2026-04-29</summary>

- [x] Phase 111: StepCodeBuffer 核心实现 (2/2 plans) — completed 2026-04-28
- [x] Phase 112: 集成接入 (2/2 plans) — completed 2026-04-28
- [x] Phase 113: E2E 验证与回归 (2/2 plans) — completed 2026-04-29

</details>

<details>
<summary>✅ v0.10.8 生成测试代码前置条件与断言步骤 (Phases 108-110) — SHIPPED 2026-04-27</summary>

- [x] Phase 108: 前置条件注入 (1/1 plans) — completed 2026-04-27
- [x] Phase 109: 断言步骤生成 (1/1 plans) — completed 2026-04-27
- [x] Phase 110: E2E 验证 (1/1 plans) — completed 2026-04-27

</details>

<details>
<summary>✅ v0.10.7 生成测试代码行为优化 (Phases 105-107) — SHIPPED 2026-04-27</summary>

- [x] Phase 105: 代码生成质量修复 (2/2 plans) — completed 2026-04-25
- [x] Phase 106: 定位器质量优化 (2/2 plans) — completed 2026-04-26
- [x] Phase 107: 自治修复增强E2E (2/2 plans) — completed 2026-04-27

</details>

<details>
<summary>✅ Older milestones (v0.10.6 — v0.6.2)</summary>

- ✅ **v0.10.6 生成测试代码稳定可用** — Phases 102-104 (shipped 2026-04-25)
- ✅ **v0.10.5 生成测试代码修复与优化** — Phases 99-101 (shipped 2026-04-24)
- ✅ **v0.10.4 Playwright 代码验证与任务管理集成** — Phases 97-98 (shipped 2026-04-24)
- ✅ **v0.10.3 DOM 深度修复 - 表格单元格选择精确性** — Phases 94-96 (shipped 2026-04-23)
- ✅ **v0.10.2 测试验证与代码可用性修复** — Phases 90-93 (shipped 2026-04-23)
- ✅ **v0.10.1 代码登录及 Agent 复用登录的浏览器状态** — Phases 86-89 (shipped 2026-04-21)
- ✅ **v0.10.0 Agent 执行速度优化** — Phases 82-85 (shipped 2026-04-18)
- ✅ **v0.9.2 Cookie 预注入免登录** — Phases 79-81 (shipped 2026-04-17)
- ✅ **v0.9.1 ERP 全面集成重构** — Phases 74-78 (shipped 2026-04-12)
- ✅ **v0.9.0 Excel 批量导入功能开发** — Phases 70-73 (shipped 2026-04-09)
- ✅ **v0.8.4 基于 v0.8.3 的研究优化** — Phases 67-69 (shipped 2026-04-07)
- ✅ **v0.8.3 分析报告差距对表格填写影响** — Phases 65-66 (shipped 2026-04-06)
- ✅ **v0.8.2 浏览器模式差异调查** — Phases 63-64 (shipped 2026-04-06)
- ✅ **v0.8.1 修复销售出库表格填写问题** — Phase 62 (shipped 2026-04-06)
- ✅ **v0.8.0 报告完善与 UI 优化** — Phases 57-61 (shipped 2026-04-03)
- ✅ **v0.7.0 更多操作边界测试** — Phases 52-56 (shipped 2026-04-01)
- ✅ **v0.6.3 Agent 可靠性优化** — Phases 48-51 (shipped 2026-04-03)
- ✅ **v0.6.2 回归原生 browser-use** — Phases 45-47 (shipped 2026-04-03)

</details>

---
*Roadmap updated: 2026-04-29 — Phase 115 planned*
