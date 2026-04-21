# Roadmap: aiDriveUITest

## Milestones

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
- ✅ **v0.6.3 Agent 可靠性优化** — Phases 48-51 (shipped 2026-03-28)
- ✅ **v0.6.2 回归原生 browser-use** — Phases 45-47 (shipped 2026-03-27)

## Phases

<details>
<summary>✅ v0.10.1 代码登录及 Agent 复用登录的浏览器状态 (Phases 86-89) — SHIPPED 2026-04-21</summary>

- [x] Phase 86: 登录机制研究 (2/2 plans) — completed 2026-04-20
- [x] Phase 87: 代码登录修复与集成 (1/1 plans) — completed 2026-04-21
- [x] Phase 88: 认证代码清理 (2/2 plans) — completed 2026-04-21
- [x] Phase 89: 测试覆盖 (1/1 plans) — completed 2026-04-21

</details>

<details>
<summary>✅ v0.9.1 ERP 全面集成重构 (Phases 74-78) — SHIPPED 2026-04-12</summary>

- [x] Phase 74: CacheService + ContextWrapper — 内存KV缓存基础层，绑定 Run 生命周期 (completed 2026-04-11)
- [x] Phase 75: AccountService + Settings — 多角色账号解析与登录URL配置 (completed 2026-04-11)
- [x] Phase 76: DB Migration + Excel + Frontend — 数据层变更：login_role 字段、Excel模板、前端下拉 (completed 2026-04-11)
- [x] Phase 77: TestFlowService + runs.py Integration — 流程编排层，串联缓存+账号+前置+Agent+断言 (completed 2026-04-12)
- [x] Phase 78: E2E Verification — 销售出库场景端到端验证 (completed 2026-04-12)

</details>

<details>
<summary>✅ v0.9.0 Excel 批量导入功能开发 (Phases 70-73) — SHIPPED 2026-04-09</summary>

- [x] Phase 70: Excel 模版设计 (2/2 plans) — completed 2026-04-08
- [x] Phase 71: 批量导入工作流 (2/2 plans) — completed 2026-04-08
- [x] Phase 72: 批量执行引擎 (2/2 plans) — completed 2026-04-09
- [x] Phase 73: 批量进度 UI (2/2 plans) — completed 2026-04-09

</details>

<details>
<summary>✅ v0.8.4 基于 v0.8.3 的研究优化 (Phases 67-69) — SHIPPED 2026-04-07</summary>

- [x] Phase 67: 基础层 — 行标识检测、失败追踪状态、失败模式检测器
- [x] Phase 68: DOM Patch 增强 — 行标识注入、策略标注、失败动态标注
- [x] Phase 69: 服务集成与 Prompt 规则 — step_callback 集成、Section 9 规则追加

</details>

<details>
<summary>✅ v0.8.3 分析报告差距对表格填写影响 (Phases 65-66) — SHIPPED 2026-04-06</summary>

- [x] Phase 65: 差距关联分析 — 1/1 plans
- [x] Phase 66: 优化方案设计 — 1/1 plan

</details>

<details>
<summary>✅ v0.8.2 浏览器模式差异调查 (Phases 63-64) — SHIPPED 2026-04-06</summary>

- [x] Phase 63: 代码对比分析 — 识别 f951791 为根因 commit (2/2 plans)
- [x] Phase 64: 分析报告输出 — 完整技术报告 + 精简摘要 (1/1 plan)

</details>

<details>
<summary>✅ v0.8.1 修复销售出库表格填写问题 (Phase 62) — SHIPPED 2026-04-06</summary>

- [x] Phase 62: DOM Patch + Prompt 增强 — td cell 交互 + Section 9 click-to-edit 指导 (1/1 plan)

</details>

<details>
<summary>✅ v0.8.0 报告完善与 UI 优化 (Phases 57-61) — SHIPPED 2026-04-03</summary>

- [x] Phase 57: AI 推理格式优化 — Eval/Verdict/Memory/Goal 分行彩色 badge (1/1 plan)
- [x] Phase 58: 执行步骤展示 — StepTimeline 统一时间线 (1/1 plan)
- [x] Phase 59: 报告步骤展示 — 报告详情时间线 (2/2 plans)
- [x] Phase 60: 任务表单优化 — 删除 api_assertions (2/2 plans)
- [x] Phase 61: E2E 验证 — 6/6 检查 PASS (2/2 plans)

</details>

<details>
<summary>✅ v0.7.0 更多操作边界测试 (Phases 52-56) — SHIPPED 2026-04-01</summary>

- [x] Phase 52: Prompt 增强 — 键盘操作 (3/3 plans)
- [x] Phase 53: Prompt 增强 — 表格交互 (3/3 plans)
- [x] Phase 54: 文件导入 (2/2 plans)
- [x] Phase 55: 断言参数调优 (skipped)
- [x] Phase 56: E2E 综合验证 (2/2 plans)

</details>

<details>
<summary>✅ v0.6.3 Agent 可靠性优化 (Phases 48-51) — SHIPPED 2026-03-28</summary>

- [x] Phase 48: 监控模块与 Agent 子类 (4/4 plans)
- [x] Phase 49: 提示词优化与参数调优 (2/2 plans)
- [x] Phase 50: AgentService 集成 (2/2 plans)
- [x] Phase 51: 端到端验证 (2/2 plans)

</details>

<details>
<summary>✅ v0.6.2 回归原生 browser-use (Phases 45-47) — SHIPPED 2026-03-27</summary>

- [x] Phase 45: 代码移除 (5/5 plans)
- [x] Phase 46: 代码简化与测试 (2/2 plans)
- [x] Phase 47: 验证 (0/1 plans)

</details>

<details>
<summary>✅ v0.9.2 Cookie 预注入免登录 (Phases 79-81) — SHIPPED 2026-04-17</summary>

- [x] Phase 79: Token 获取与 Storage State 构造 (completed 2026-04-16)
- [x] Phase 80: 执行流程集成 (completed 2026-04-17)
- [x] Phase 81: 批量执行与兼容性验证 (completed 2026-04-17)

</details>

<details>
<summary>✅ v0.10.0 Agent 执行速度优化 (Phases 82-85) — SHIPPED 2026-04-18</summary>

- [x] Phase 82: 代码生成基础 (completed 2026-04-18)
- [x] Phase 83: 定位器回退 (completed 2026-04-18)
- [x] Phase 84: LLM 修复 (completed 2026-04-18)
- [x] Phase 85: Agent 重执行 (completed 2026-04-18)

</details>

### v0.10.2 测试验证与代码可用性修复 (In Progress)

**Milestone Goal:** 验证前面阶段任务的完成度，更新过时的测试代码，修复反复出现的 DataMethodError，确保端到端流程可用

- [x] **Phase 90: 过时测试清理** — 删除与当前架构不符的过时测试，消除不可修复的噪音 (completed 2026-04-21)
- [ ] **Phase 91: 测试代码修复** — 修复剩余测试失败，mock 路径与当前代码对齐
- [ ] **Phase 92: DataMethodError 修复** — 诊断并解决 webseleniumerp 混淆方法名变化导致的前置条件执行失败
- [ ] **Phase 93: 端到端可用性验证** — 验证完整链路（自然语言 -> AI 执行 -> 报告）在修复后可用

## Phase Details

### Phase 90: 过时测试清理
**Goal**: 测试套件中不再有过时或不可修复的测试文件，后续修复工作不会浪费在将被删除的测试上
**Depends on**: Nothing (first phase in milestone, clean before fix)
**Requirements**: CLEAN-01, CLEAN-02
**Success Criteria** (what must be TRUE):
  1. 所有 ImportError 测试文件被识别并删除 — pytest 运行时不再出现 ImportError 错误
  2. 与当前架构不符的过时测试文件被删除 — 测试文件全部引用当前存在的模块路径
  3. 跨测试状态泄漏被修复 — 同一测试文件中的测试可独立运行且结果一致
**Plans**: 2 plans

Plans:
- [x] 90-01-PLAN.md — git rm 删除 ImportError 文件、_archived/ 目录、工具脚本、顶层 conftest.py，删除部分过时测试方法
- [x] 90-02-PLAN.md — 审查 conftest fixture 隔离性，验证测试状态无泄漏，运行全量验证

### Phase 91: 测试代码修复
**Goal**: 所有保留的测试文件通过，mock 路径和 fixture 与当前代码完全对齐
**Depends on**: Phase 90
**Requirements**: TEST-01, TEST-02, TEST-03, TEST-04, TEST-05
**Success Criteria** (what must be TRUE):
  1. 所有外部断言桥接测试通过 — test_external_assertion_bridge.py 中 mock 目标路径与当前代码对齐
  2. auth_service 和 precondition_service 测试通过 — mock 路径指向当前模块结构
  3. 其他零散失败测试（agent_service, self_healing_runner, llm_healer, browser_cleanup, repository 等）全部通过
  4. `uv run pytest backend/tests/ -v` 零失败零错误
**Plans**: TBD

Plans:
- [ ] 91-01: 修复外部断言桥接和 auth_service 测试
- [ ] 91-02: 修复 precondition_service 和其他零散测试

### Phase 92: DataMethodError 修复
**Goal**: 前置条件执行不再因 webseleniumerp 混淆方法名变化而失败，系统具备方法名自动发现能力
**Depends on**: Phase 91
**Requirements**: DATA-01, DATA-02
**Success Criteria** (what must be TRUE):
  1. PcImport 前置条件执行不再报 `'ImportApi' object has no attribute` 错误 — context.get_data() 调用链路完整
  2. 方法名不再硬编码混淆名称 — 系统能自动发现当前可用的方法名或动态映射
  3. webseleniumerp 上游更新后，只需更新依赖版本，无需手动查找和替换方法名
**Plans**: TBD

Plans:
- [ ] 92-01: 诊断 PcImport 混淆方法名失效根因
- [ ] 92-02: 实现方法名自动发现或动态映射

### Phase 93: 端到端可用性验证
**Goal**: 自然语言到报告的完整链路在修复后可用，验证核心产品价值不被回归破坏
**Depends on**: Phase 92
**Requirements**: E2E-01, E2E-02, E2E-03
**Success Criteria** (what must be TRUE):
  1. 自然语言测试步骤经 AI 执行后生成完整测试报告 — 从输入到报告输出的全链路畅通
  2. 前置条件系统正常工作 — context.get_data() 调用返回预期数据，变量替换正确
  3. 断言系统正常工作 — 业务断言执行并返回 pass/fail 结果
**Plans**: TBD

Plans:
- [ ] 93-01: 端到端链路验证

## Progress

**Execution Order:**
Phases execute in numeric order: 90 -> 91 -> 92 -> 93

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 90. 过时测试清理 | v0.10.2 | 2/2 | Complete    | 2026-04-21 |
| 91. 测试代码修复 | v0.10.2 | 0/2 | Not started | - |
| 92. DataMethodError 修复 | v0.10.2 | 0/2 | Not started | - |
| 93. 端到端可用性验证 | v0.10.2 | 0/1 | Not started | - |

---
*Roadmap updated: 2026-04-21 — Phase 90 plans created*
