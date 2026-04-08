# Roadmap: aiDriveUITest

## Milestones

- 🚧 **v0.9.0 Excel 批量导入功能开发** — Phases 70-73 (in progress)
- ✅ **v0.8.4 基于 v0.8.3 的研究优化** — Phases 67-69 (shipped 2026-04-07)
- ✅ **v0.8.3 分析报告差距对表格填写影响** — Phases 65-66 (shipped 2026-04-06)
- ✅ **v0.8.2 浏览器模式差异调查** — Phases 63-64 (shipped 2026-04-06)
- ✅ **v0.8.1 修复销售出库表格填写问题** — Phase 62 (shipped 2026-04-06)
- ✅ **v0.8.0 报告完善与 UI 优化** — Phases 57-61 (shipped 2026-04-03)
- ✅ **v0.7.0 更多操作边界测试** — Phases 52-56 (shipped 2026-04-01)
- ✅ **v0.6.3 Agent 可靠性优化** — Phases 48-51 (shipped 2026-03-28)
- ✅ **v0.6.2 回归原生 browser-use** — Phases 45-47 (shipped 2026-03-27)

## Phases

### 🚧 v0.9.0 Excel 批量导入功能开发 (In Progress)

**Milestone Goal:** 支持 QA 通过 Excel 模版批量创建测试用例，并可勾选用例批量执行

- [ ] **Phase 70: Excel 模版设计** — 生成标准化 .xlsx 模版 + openpyxl 解析器，建立列合约
- [ ] **Phase 71: 批量导入工作流** — 上传解析 → 预览校验 → 确认批量创建 Task
- [ ] **Phase 72: 批量执行引擎** — 勾选执行 + Semaphore 并发控制
- [ ] **Phase 73: 批量进度 UI** — 前端批量进度页面，逐任务状态展示 + 跳转

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

## Phase Details

### Phase 70: Excel 模版设计
**Goal**: QA 可以下载标准化的 Excel 模版来填写测试用例，后端拥有经过单元测试的 Excel 解析器，建立模版列名/类型/顺序的合约
**Depends on**: Nothing (first phase of v0.9.0)
**Requirements**: TMPL-01, TMPL-02
**Success Criteria** (what must be TRUE):
  1. 用户点击"下载模版"按钮后，浏览器下载一个 .xlsx 文件，包含"测试用例"sheet（列头：任务名称、任务描述、目标URL、最大步数、前置条件、断言）+ 2 行示例数据 + "README" sheet 填写说明
  2. 模版中"最大步数"列配置了 1-100 的下拉验证，输入超出范围的值时 Excel 显示错误提示
  3. ExcelParser 解析合法 .xlsx 文件返回结构化的行数据列表，每行包含完整的 TaskCreate 字段
  4. ExcelParser 遇到空白行跳过、类型不匹配的单元格做类型强制转换（如数字转字符串）、合并单元格报错提示
**Plans**: 2 plans

Plans:
- [x] 70-01-PLAN.md — Template generator + column contract + unit tests + download endpoint (TMPL-01, TMPL-02)
- [ ] 70-02-PLAN.md — ExcelParser with collect-all errors + comprehensive unit tests + round-trip validation (TMPL-01, TMPL-02)

### Phase 71: 批量导入工作流
**Goal**: QA 上传填写好的 Excel 后，可以在确认前预览解析结果（有效行绿色、无效行红色+错误信息），确认后系统批量创建所有 Task
**Depends on**: Phase 70 (使用 ExcelParser)
**Requirements**: IMPT-01, IMPT-02, IMPT-03
**Success Criteria** (what must be TRUE):
  1. 用户上传 .xlsx 文件后，系统逐行解析并返回预览结果：有效行显示绿色带解析数据，无效行显示红色 + 具体错误信息（行号 + 字段 + 原因）
  2. 上传非 .xlsx 文件或超过 5MB 的文件时，系统拒绝并返回明确的文件格式/大小错误提示
  3. 预览页面存在无效行时，"确认导入"按钮不可点击，防止脏数据进入系统
  4. 用户确认导入后（全部有效），系统在一个数据库事务中批量创建所有 Task，状态为 draft，任一行创建失败则全部回滚
**Plans**: 2 plans

Plans:
- [x] 71-01-PLAN.md — Backend import preview + confirm endpoints with atomic batch create (IMPT-01, IMPT-03)
- [x] 71-02-PLAN.md — Frontend ImportModal component + API integration + Tasks page wiring (IMPT-01, IMPT-02, IMPT-03)

### Phase 72: 批量执行引擎
**Goal**: QA 可以在任务列表勾选多个 Task 后一键启动并行执行，系统使用 Semaphore 控制并发数防止服务器 OOM
**Depends on**: Phase 71 (需要已导入的 Task)
**Requirements**: BATCH-01, BATCH-02
**Success Criteria** (what must be TRUE):
  1. 用户在 TaskTable 勾选多个 Task 后，出现"批量执行"按钮，点击后启动所有勾选任务的并行执行
  2. 批量执行使用 asyncio.Semaphore 控制并发数，默认 2 个浏览器实例同时运行，用户可通过参数配置（硬上限 4）
  3. 每个任务在批量执行中有独立的状态追踪（等待/执行中/完成/失败），后端提供批量进度查询 API
  4. 单个任务执行失败不影响其他任务继续执行，失败任务的错误信息被完整记录
**Plans**: TBD

### Phase 73: 批量进度 UI
**Goal**: QA 可以在前端查看批量执行的进度，看到每个任务的状态，点击可跳转到该任务的执行监控详情
**Depends on**: Phase 72 (需要批量执行 API)
**Requirements**: BATCH-03
**Success Criteria** (what must be TRUE):
  1. 用户启动批量执行后，跳转到批量进度页面，页面以列表/网格形式展示每个任务的状态标签（等待/执行中/完成/失败）
  2. 页面每 2 秒轮询后端 API 更新状态，任务从"等待"变为"执行中"再到"完成/失败"的转换实时可见
  3. 用户点击任意任务条目，跳转到该任务的执行监控详情页（复用现有 RunMonitor）
**Plans**: TBD
**UI hint**: yes

## Progress

**Execution Order:**
Phases execute in numeric order: 70 -> 71 -> 72 -> 73

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 70. Excel 模版设计 | v0.9.0 | 1/2 | Complete    | 2026-04-08 |
| 71. 批量导入工作流 | v0.9.0 | 2/2 | Complete    | 2026-04-08 |
| 72. 批量执行引擎 | v0.9.0 | 0/? | Not started | - |
| 73. 批量进度 UI | v0.9.0 | 0/? | Not started | - |

---
*Roadmap updated: 2026-04-08 — Phase 71 planned (2 plans)*
