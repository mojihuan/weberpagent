# Roadmap: aiDriveUITest

## Milestones

- 🚧 **v0.9.1 ERP 全面集成重构** — Phases 74-78 (in progress)
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

### 🚧 v0.9.1 ERP 全面集成重构 (In Progress)

**Milestone Goal:** 跑通「Excel导入 → 前置API(含缓存) → AI执行UI → 断言(含缓存验证)」完整链路

- [x] **Phase 74: CacheService + ContextWrapper** — 内存KV缓存基础层，绑定 Run 生命周期 (completed 2026-04-11)
- [x] **Phase 75: AccountService + Settings** — 多角色账号解析与登录URL配置 (completed 2026-04-11)
- [x] **Phase 76: DB Migration + Excel + Frontend** — 数据层变更：login_role 字段、Excel模板、前端下拉 (completed 2026-04-11)
- [x] **Phase 77: TestFlowService + runs.py Integration** — 流程编排层，串联缓存+账号+前置+Agent+断言 (completed 2026-04-12)
- [ ] **Phase 78: E2E Verification** — 销售出库场景端到端验证

## Phase Details

### Phase 74: CacheService + ContextWrapper
**Goal**: QA 测试用例可以通过 CacheService 在步骤间传递参数，缓存数据在 Run 结束后自动清理
**Depends on**: Nothing (foundation layer for v0.9.1)
**Requirements**: CACHE-01, CACHE-02, CACHE-03
**Success Criteria** (what must be TRUE):
  1. CacheService.cache("order_no", "SO-2026-001") 后调用 cached("order_no") 返回 "SO-2026-001"
  2. cached() 返回的数据是原始值的深拷贝，外部修改不影响缓存内部状态
  3. ContextWrapper.context.cache() 和 context.cached() 正确委托到 CacheService
  4. 同一个 CacheService 实例的所有缓存数据在 clear() 调用后全部清除
**Plans:** 2/2 plans complete

Plans:
- [x] 74-01-PLAN.md — CacheService class with bidirectional deepcopy + unit tests
- [x] 74-02-PLAN.md — ContextWrapper cache/cached delegation + integration tests

### Phase 75: AccountService + Settings
**Goal**: 系统能根据角色名称解析出对应的 ERP 登录凭据和登录 URL，供后续自动登录使用
**Depends on**: Nothing (independent of Phase 74, can run in parallel)
**Requirements**: ACCT-01, ACCT-02, ACCT-03
**Success Criteria** (what must be TRUE):
  1. AccountService.resolve("main") 返回包含正确 account、password、role 的不可变 AccountInfo 对象
  2. 对不存在的角色名称调用 resolve() 抛出明确的错误信息，列出所有可用角色
  3. 登录 URL 从 settings.py ERP_LOGIN_URL 配置读取，不在任何 Excel 或前端代码中硬编码
  4. AccountInfo 是 frozen dataclass，创建后无法修改字段值
**Plans:** 1/1 plans complete

**源码验证修正 (2026-04-11):**
  - ROLE_MAP 中 platform 角色密码字段为 `password`（非 `super_admin_password`），已通过 `api_login.py:100-103` 确认
  - bot 角色使用完全不同的登录方式（phone/wechatId/miniOpenid 等 9 字段 + 不同 URL），不适用 UI 自动登录注入，从 ROLE_MAP 中排除
  - 有效 UI 登录角色为 7 种：main, special, vice, camera, platform, super, idle
  - 所有角色的 INFO 字段映射已通过 `user_info.py` 和 `api_login.py` 双重验证

Plans:
- [x] 75-01-PLAN.md — AccountService (ROLE_MAP + resolve + get_login_url) + AccountInfo frozen dataclass + TDD unit tests (ACCT-01, ACCT-02, ACCT-03)

### Phase 76: DB Migration + Excel + Frontend
**Goal**: Task 模型、Excel 导入导出和前端表单三端一致支持 login_role 字段，QA 可以为任务指定登录角色
**Depends on**: Nothing (data layer, independent of Phases 74-75)
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04, DATA-05
**Success Criteria** (what must be TRUE):
  1. Task 表新增 login_role VARCHAR(20) nullable 列，现有 Task 数据不受影响（login_role 为 NULL）
  2. 通过 API 创建 Task 时传入 login_role="main" 能正确存储，GET 响应中包含 login_role 字段
  3. 导出的 Excel 模板第二列为「登录角色」，带有 7 种角色的下拉验证（排除 bot）
  4. 导入含 login_role 的 Excel 文件能正确创建带角色的 Task
  5. 前端任务表单显示 login_role 下拉选择器，列出 7 种中文角色名称
**UI hint**: yes
**Plans:** 2/2 plans complete

Plans:
- [x] 76-01-PLAN.md — Task model login_role + Pydantic schemas + DB migration (DATA-01, DATA-02)
- [x] 76-02-PLAN.md — Excel template/parser + frontend login_role dropdown (DATA-03, DATA-04, DATA-05)

### Phase 77: TestFlowService + runs.py Integration
**Goal**: 指定了 login_role 的任务自动走完整编排流程：登录 → 前置条件(含缓存) → 变量替换 → Agent执行 → 断言，未指定角色的任务走现有流程不变
**Depends on**: Phase 74, Phase 75, Phase 76
**Requirements**: FLOW-01, FLOW-02, FLOW-03, FLOW-04, CACHE-04, CACHE-05, ACCT-04
**Success Criteria** (what must be TRUE):
  1. 设置 login_role 的任务执行时自动注入登录步骤（打开URL → 输入账号 → 输入密码 → 点击登录），无需手动编写登录操作
  2. 任务描述中的 {{cached:key}} 语法被正确替换为缓存中的实际值，不会触发 Jinja2 UndefinedError
  3. 前置条件中 cache 类型 JSON 配置调用外部数据方法后，提取的字段值可通过 cached() 在后续步骤读取
  4. 同一 Run 的前置条件阶段和断言阶段共享同一个 CacheService 实例，前置缓存的数据在断言中可访问
  5. 未设置 login_role 的任务完全走现有执行路径，行为与 v0.9.0 一致，无回归
**Plans:** 2/2 plans complete

Plans:
- [x] 77-01-PLAN.md — TestFlowService (build_login_prefix + _build_description with two-phase substitution) + TDD unit tests (FLOW-01, FLOW-02, CACHE-05, ACCT-04)
- [x] 77-02-PLAN.md — runs.py login_role branch + shared CacheService + batches.py integration + integration tests (FLOW-03, FLOW-04, CACHE-04)

### Phase 78: E2E Verification
**Goal**: Mock 集成测试验证 v0.9.1 完整集成链路（缓存传递、自动登录、变量替换、断言验证），核心回归确保零回归
**Depends on**: Phase 77
**Requirements**: (no new requirements — validates CACHE-01 through FLOW-04)
**Success Criteria** (what must be TRUE):
  1. 通过 Mock 集成测试验证 login_role="main" 的销售出库完整链路：登录注入 → 缓存传递 → 变量替换 → Agent 执行 → 断言缓存读取 (per D-01, corrected from "admin" to "main")
  2. 前置条件获取的数据（如订单号）通过 CacheService 传递到 AI 执行步骤中，{{cached:key}} 被正确替换为缓存值
  3. 任务执行完成后生成的报告步骤顺序正确，登录步骤出现在业务步骤之前
  4. 未设置 login_role 的任务在 v0.9.1 版本中执行结果与 v0.9.0 一致，无回归
**Plans:** 1/2 plans executed

Plans:
- [x] 78-01-PLAN.md — Mock 集成测试：销售出库完整链路（login injection + cache transfer + variable substitution + assertion cache read）
- [ ] 78-02-PLAN.md — 核心回归测试（login_role=None 现有路径 + 报告步骤顺序验证）

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 74. CacheService + ContextWrapper | v0.9.1 | 2/2 | Complete    | 2026-04-11 |
| 75. AccountService + Settings | v0.9.1 | 1/1 | Complete    | 2026-04-11 |
| 76. DB Migration + Excel + Frontend | v0.9.1 | 2/2 | Complete    | 2026-04-11 |
| 77. TestFlowService + runs.py | v0.9.1 | 2/2 | Complete    | 2026-04-12 |
| 78. E2E Verification | v0.9.1 | 1/2 | In Progress|  |

---
*Roadmap updated: 2026-04-12 — Phase 78 plans finalized*
