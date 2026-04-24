# Roadmap: aiDriveUITest

## Milestones

- 🚧 **v0.10.4 Playwright 代码验证与任务管理集成** — Phases 97-98 (in progress)
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
- ✅ **v0.6.3 Agent 可靠性优化** — Phases 48-51 (shipped 2026-03-28)
- ✅ **v0.6.2 回归原生 browser-use** — Phases 45-47 (shipped 2026-03-27)

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

### 🚧 v0.10.4 Playwright 代码验证与任务管理集成 (In Progress)

**Milestone Goal:** 验证生成的 Playwright 代码可执行测试任务，并在任务管理中提供代码查看和运行能力

- [ ] **Phase 97: 后端 API** — 代码查看/执行 API + 任务状态扩展
- [ ] **Phase 98: 前端 UI** — 代码列/查看器/执行按钮 + 状态徽章

<details>
<summary>✅ v0.10.3 DOM 深度修复 - 表格单元格选择精确性 (Phases 94-96) — SHIPPED 2026-04-23</summary>

- [x] Phase 94: DOM Patch 增强 (2/2 plans) — completed 2026-04-23
- [x] Phase 95: Prompt 更新 (1/1 plans) — completed 2026-04-23
- [x] Phase 96: E2E 验证 (1/1 plans) — completed 2026-04-23

</details>

<details>
<summary>✅ v0.10.2 测试验证与代码可用性修复 (Phases 90-93) — SHIPPED 2026-04-23</summary>

- [x] Phase 90: 过时测试清理 (2/2 plans) — completed 2026-04-21
- [x] Phase 91: 测试代码修复 (2/2 plans) — completed 2026-04-21
- [x] Phase 92: DataMethodError 修复 (2/2 plans) — completed 2026-04-21
- [x] Phase 93: 端到端可用性验证 (1/1 plan) — completed 2026-04-22

</details>

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
- [x] Phase 83: 定位器回放 (completed 2026-04-18)
- [x] Phase 84: LLM 修复 (completed 2026-04-18)
- [x] Phase 85: Agent 重执行 (completed 2026-04-18)

</details>

## Phase Details

### Phase 97: 后端 API
**Goal**: QA 可以通过 API 查看已生成的 Playwright 代码内容，触发 pytest 执行，并获取执行结果（包含成功/失败状态）
**Depends on**: Phase 96 (v0.10.3 completed)
**Requirements**: CODE-01, CODE-02, CODE-03, STATUS-01
**Success Criteria** (what must be TRUE):
  1. GET /runs/{run_id}/code 返回该 run 生成的 Python 代码文件内容（文本格式，带行号信息）
  2. POST /runs/{run_id}/execute-code 触发 pytest 执行，复用 SelfHealingRunner（storage_state 注入 + 超时保护），返回执行 ID
  3. 代码执行完成后，GET /runs/{run_id} 返回 healing_status="success"/"failed" 和 healing_error 错误信息
  4. 代码执行成功时，对应 Task.status 自动更新为 "success"
  5. 并发执行请求返回 HTTP 409，防止服务器内存耗尽
**Plans**: 2 plans

Plans:
- [x] 97-01-PLAN.md -- GET /code endpoint + schema expansion + CODE-01 tests
- [x] 97-02-PLAN.md -- POST /execute-code + concurrency guard + status auto-update + CODE-02/03/STATUS-01 tests

### Phase 98: 前端 UI
**Goal**: QA 在任务列表中能看到哪些任务有可用代码，点击即可查看代码或运行 Playwright 测试
**Depends on**: Phase 97
**Requirements**: UI-01, UI-02, UI-03
**Success Criteria** (what must be TRUE):
  1. 任务列表 TaskTable 新增"代码"列，有代码的任务显示可用标识，无代码的任务显示灰色占位
  2. 点击"查看代码"按钮打开 CodeViewerModal，以语法高亮 + 行号方式只读展示 Python 代码
  3. 点击"运行代码"按钮触发 Playwright 执行，显示执行状态（等待/运行中/成功/失败），执行失败时展示错误信息
  4. Task.status 为 "success" 时，StatusBadge 显示绿色"成功"标签
**Plans**: 2 plans

Plans:
- [x] 98-01-PLAN.md -- Backend schema extension (has_code/latest_run_id) + frontend types + StatusBadge + API functions
- [ ] 98-02-PLAN.md -- TaskTable code column + CodeViewerModal + CodeExecutionStatus + human verification

## Progress

**Execution Order:**
Phases execute in numeric order: 97 → 98

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 97. 后端 API | v0.10.4 | 2/2 | Complete    | 2026-04-23 |
| 98. 前端 UI | v0.10.4 | 1/2 | In Progress|  |

---
*Roadmap updated: 2026-04-23 -- Phase 98 plans created (2 plans)*
