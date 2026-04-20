# Roadmap: aiDriveUITest

## Milestones

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
- 🚧 **v0.10.1 代码登录及 Agent 复用登录的浏览器状态** — Phases 86-89 (in progress)

## Phases

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

### v0.10.1 代码登录及 Agent 复用登录的浏览器状态 (In Progress)

**Milestone Goal:** 修复代码登录流程，让 Agent 执行时复用已登录的浏览器状态，跳过文字登录步骤，节省 LLM token 和执行时间

- [x] **Phase 86: 登录机制研究** — 研究 webseleniumerp 代码登录机制和 browser-use 状态复用方案 (completed 2026-04-20)
- [ ] **Phase 87: 代码登录修复与集成** — 实现工作的代码登录 + Agent 状态复用 + 失败回退
- [ ] **Phase 88: 认证代码清理** — 移除死代码，重构认证模块职责清晰
- [ ] **Phase 89: 测试覆盖** — 单元测试 + E2E 验证代码登录和状态复用路径

## Phase Details

### Phase 86: 登录机制研究
**Goal**: 确定 ERP 代码登录和 browser-use 状态复用的可行技术方案，输出可直接执行的实现步骤
**Depends on**: Phase 85 (v0.10.0 shipped)
**Requirements**: (research phase — enables AUTH-03 delivery in Phase 87)
**Success Criteria** (what must be TRUE):
  1. webseleniumerp 项目的登录流程被完整记录：HTTP API 调用链、token 格式、session/cookie 机制、SPA 前端如何消费 token
  2. 当前 cookie 注入失败的根因被明确识别（SPA 拒绝注入 token 的技术原因）
  3. browser-use storage_state / cookie 注入的正确用法通过最小 POC 验证（浏览器访问 ERP 时处于登录状态）
  4. 输出可执行的代码登录实现方案，覆盖 token 获取、状态构造、状态传递到 Agent 全链路
**Plans**: 2 plans

Plans:
- [x] 86-01-PLAN.md — POC 验证：page.evaluate localStorage 注入 + 编程式表单登录
- [x] 86-02-PLAN.md — 综合研究报告：登录流程文档 + 根因分析 + Phase 87 实现方案

### Phase 87: 代码登录修复与集成
**Goal**: Agent 执行任务时使用已登录的浏览器状态直接操作 ERP，跳过 5 步文字登录；代码登录失败时自动回退不中断任务
**Depends on**: Phase 86
**Requirements**: AUTH-03, AUTH-04, AUTH-05
**Success Criteria** (what must be TRUE):
  1. 设置了 login_role 的任务，代码登录成功后，Agent 启动浏览器时已处于 ERP 登录状态，无跳转到 /login 页面的现象
  2. 代码登录成功时，Agent 收到的指令不包含 5 步登录文字，直接从业务操作开始，LLM 调用步骤数减少 5 步
  3. 代码登录失败（API 超时/网络错误/token 无效）时，任务自动回退到文字登录模式，任务不会中断
  4. 回退时日志中出现包含角色名和失败原因的 warning 级别日志
**Plans**: TBD

### Phase 88: 认证代码清理
**Goal**: auth 相关代码（auth_service, auth_session_factory, agent_service 登录部分）结构清晰、职责分明，无冗余分支和死代码
**Depends on**: Phase 87
**Requirements**: CLEAN-01, CLEAN-02
**Success Criteria** (what must be TRUE):
  1. auth_service 职责单一：只负责 HTTP token 获取，无登录状态构造或 Agent 集成逻辑
  2. auth_session_factory 或等效模块职责单一：只负责将 token 转换为 browser-use 可用的浏览器状态
  3. agent_service 的登录分支逻辑清晰：代码登录 -> 回退到文字登录，无多层嵌套 if/else
  4. 已确认不工作的代码路径（如旧的 cookie 直接注入方式）被完全移除，不留死代码
**Plans**: TBD

### Phase 89: 测试覆盖
**Goal**: 代码登录流程和 Agent 状态复用路径有单元测试和 E2E 测试覆盖，回归安全有保障
**Depends on**: Phase 88
**Requirements**: TEST-01, TEST-02
**Success Criteria** (what must be TRUE):
  1. 单元测试覆盖 token 获取成功/失败/超时场景，mock HTTP 调用，验证返回值和异常行为
  2. 单元测试覆盖状态构造：给定 token，构造的浏览器状态格式正确、browser-use 可接受
  3. 单元测试覆盖状态传递到 Agent 的路径：mock Agent 构造，验证 storage_state 参数正确传入
  4. E2E 验证：设置 login_role 的任务执行时 Agent 跳过登录步骤，直接完成业务操作（如访问 ERP 首页可见业务菜单）
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 86 -> 87 -> 88 -> 89

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 86. 登录机制研究 | v0.10.1 | 2/2 | Complete   | 2026-04-20 |
| 87. 代码登录修复与集成 | v0.10.1 | 0/? | Not started | - |
| 88. 认证代码清理 | v0.10.1 | 0/? | Not started | - |
| 89. 测试覆盖 | v0.10.1 | 0/? | Not started | - |

---
*Roadmap updated: 2026-04-20 — Phase 86 complete*
