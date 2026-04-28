# Roadmap: aiDriveUITest

## Milestones

- 🚧 **v0.10.9 逐步代码生成** — Phases 111-113 (in progress)
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

### v0.10.9 逐步代码生成 (In Progress)

**Milestone Goal:** 将 Playwright 代码生成从"事后一次性翻译"改为"每步即时翻译"，提高生成代码的可运行率。

- [ ] **Phase 111: StepCodeBuffer 核心实现** — 创建 StepCodeBuffer 数据结构 + 同步/异步翻译 + 智能等待 + 组装
- [ ] **Phase 112: 集成接入** — 将 buffer 接入 runs.py step_callback + 简化 code_generator
- [ ] **Phase 113: E2E 验证与回归** — 全量回归测试 + code_generator 现有测试更新

<details>
<summary>✅ v0.10.8 生成测试代码前置条件与断言步骤 (Phases 108-110) — SHIPPED 2026-04-27</summary>

- [x] Phase 108: 前置条件注入 (1/1 plans) — completed 2026-04-27
  - [x] 108-01-PLAN.md — _build_precondition() + runs.py 传递 + 单元测试

- [x] Phase 109: 断言步骤生成 (1/1 plans) — completed 2026-04-27
  - [x] 109-01-PLAN.md — _build_assertions() + 4种断言翻译 + runs.py传递 + 单元测试

- [x] Phase 110: E2E 验证 (1/1 plans) — completed 2026-04-27
  - [x] 110-01-PLAN.md — E2E组合验证测试 + 全量回归

</details>

<details>
<summary>✅ v0.10.7 生成测试代码行为优化 (Phases 105-107) — SHIPPED 2026-04-27</summary>

- [x] Phase 105: 代码生成质量修复 (2/2 plans) — completed 2026-04-25
- [x] Phase 106: 定位器质量优化 (2/2 plans) — completed 2026-04-26
- [x] Phase 107: 自愈修复增强E2E (2/2 plans) — completed 2026-04-27

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

## Phase Details

### Phase 111: StepCodeBuffer 核心实现
**Goal**: StepCodeBuffer 可独立使用，逐步累积翻译结果并组装完整测试文件
**Depends on**: Phase 110 (v0.10.8 shipped)
**Requirements**: CODEGEN-01, CODEGEN-02, CODEGEN-03, CODEGEN-04, VAL-01
**Success Criteria** (what must be TRUE):
  1. append_step() 接收 action_dict，通过 ActionTranslator 同步翻译为 TranslatedAction，存储翻译结果 + wait_before + step_index
  2. _derive_wait() 对 navigate 操作生成 wait_for_load_state("networkidle")，对耗时 >800ms 操作使用实际耗时，对 click 操作生成 300ms 等待
  3. append_step_async() 检测弱步骤（elem=None 或 <=1 locator），即时调用 LLMHealer 修复，修复后 DOM 上下文为最新
  4. buffer.assemble(header, precondition, assertions) 组装 import + header + precondition + 步骤代码 + assertions 为完整测试文件，ast.parse 语法验证通过
  5. 单元测试覆盖 append 同步/异步、wait 推导 3 种策略、assemble 组装、空 buffer 边界、语法验证
Plans:
- [x] 111-01-PLAN.md — StepRecord + append_step 同步翻译 + _derive_wait 三策略 + assemble 组装 + 单元测试
- [x] 111-02-PLAN.md — append_step_async 弱步骤修复 + 异步修复单元测试

### Phase 112: 集成接入
**Goal**: runs.py 使用 StepCodeBuffer 替代旧的一次性翻译，code_generator 简化删除废弃方法
**Depends on**: Phase 111
**Requirements**: INTEG-01, INTEG-02, INTEG-03, VAL-02
**Success Criteria** (what must be TRUE):
  1. runs.py step_callback 中每步操作即时调用 buffer.append_step()，action_dict 正确传递
  2. runs.py 代码生成块使用 buffer.assemble() + import/header 组装替代旧 generate_and_save()，生成的 .py 文件语法正确
  3. code_generator.py 删除 generate_and_save 和 _heal_weak_steps 方法，runs.py 使用 buffer.assemble() + Path.write_text 写文件
  4. 集成测试验证 buffer 在 step_callback 上下文中累积步骤，弱步骤异步修复正常触发
**Plans**: 2 plans
- [x] 112-01-PLAN.md — runs.py buffer 接入 + agent_service action_dict 传递 (INTEG-01, INTEG-02)
- [x] 112-02-PLAN.md — code_generator 清理 + 集成测试 (INTEG-03, VAL-02)

### Phase 113: E2E 验证与回归
**Goal**: 全量回归通过，现有 code_generator 测试更新完毕，逐步代码生成端到端可用
**Depends on**: Phase 112
**Requirements**: VAL-03
**Success Criteria** (what must be TRUE):
  1. 全量 pytest 回归测试通过（0 failed, 0 errors）
  2. code_generator 现有测试全部更新 — generate_and_save 和 _heal_weak_steps 相关测试已删除，generate() 测试保留
  3. AI 执行任务后生成的 Playwright 代码文件包含正确的逐步翻译结果（非空操作），语法验证通过
**Plans**: 2 plans
Plans:
- [x] 113-01-PLAN.md — Docstring cleanup + Pydantic ConfigDict fix
- [ ] 113-02-PLAN.md — E2E integration test + full regression

## Progress

**Execution Order:**
Phases execute in numeric order: 111 -> 112 -> 113

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 111. StepCodeBuffer 核心实现 | 2/2 | Complete    | 2026-04-28 |
| 112. 集成接入 | 2/2 | Complete    | 2026-04-28 |
| 113. E2E 验证与回归 | 1/2 | In Progress|  |

---
*Roadmap updated: 2026-04-28 — Phase 112 plans created (2 plans, 1 wave, parallel)*
