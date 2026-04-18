# Roadmap: aiDriveUITest

## Milestones

- 🚧 **v0.10.0 Agent 执行速度优化** — Phases 82-85 (in progress)
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

### v0.9.2 Cookie 预注入免登录 (In Progress)

**Milestone Goal:** 通过 HTTP API 预先获取登录 token 并注入浏览器，让 browser-use Agent 跳过 5 步登录直接执行业务操作，失败时自动回退

- [x] **Phase 79: Token 获取与 Storage State 构造** — LoginApi HTTP 获取 token，构造 browser-use 可用的 storage_state (completed 2026-04-16)
- [x] **Phase 80: 执行流程集成** — Cookie 注入成功跳过登录、失败自动回退 + warning 日志 (completed 2026-04-17)
- [x] **Phase 81: 批量执行与兼容性验证** — 批量任务独立注入、7 种角色覆盖、零回归保证 (completed 2026-04-17)

## Phase Details

### Phase 79: Token 获取与 Storage State 构造
**Goal**: 系统能通过 HTTP API 获取 ERP 登录 token 并构造为 browser-use BrowserProfile 可直接使用的 storage_state，浏览器启动即携带认证信息
**Depends on**: Phase 78 (v0.9.1 complete)
**Requirements**: AUTH-01, AUTH-02
**Success Criteria** (what must be TRUE):
  1. 对任意有效角色（如 "main"）调用 token 获取函数，返回包含 access_token 的认证数据，不依赖浏览器实例
  2. 返回的认证数据能被正确转换为 Playwright storage_state 格式（包含 cookies 或 localStorage 条目），browser-use BrowserProfile 可直接接受
  3. 使用注入 storage_state 的 BrowserProfile 创建 Agent，浏览器启动后访问 ERP 首页时已处于登录状态，无需手动登录操作
  4. token 获取函数在 HTTP 请求超时（>10s）或返回异常状态码时，抛出明确异常，不返回空值或部分数据
**Plans**: 1 plan

Plans:
- [x] 79-01-PLAN.md — AuthService HTTP token 获取 + storage_state 构造 + 认证会话工厂 (AUTH-01, AUTH-02)

### Phase 80: 执行流程集成
**Goal**: Cookie 预注入成功时 QA 的测试任务跳过 5 步登录直接执行业务操作，注入失败时自动回退到现有文字登录流程
**Depends on**: Phase 79
**Requirements**: FLOW-01, FLOW-02
**Success Criteria** (what must be TRUE):
  1. 设置了 login_role 的任务，Cookie 预注入成功后，Agent 收到的指令不包含 5 步登录文字，直接从 ERP 首页开始业务操作
  2. Cookie 预注入失败（API 超时/网络错误/返回异常）时，任务自动回退到现有 5 步文字登录流程，任务不会因注入失败而中断
  3. 预注入失败时日志中出现包含角色名称和失败原因的 warning 级别日志，便于排查问题
  4. runs.py 执行单个任务时，先尝试预注入，再决定是否跳过登录步骤，整个过程对 QA 用户透明
**Plans**: 1 plan

Plans:
- [x] 80-01-PLAN.md — Cookie 预注入分支逻辑 + TestFlowService 解耦 + AgentService 外部 session (FLOW-01, FLOW-02)

### Phase 81: 批量执行与兼容性验证
**Goal**: 批量执行时每个任务独立获取 token 并注入，无 login_role 的任务行为与 v0.9.1 完全一致，全部 7 种 UI 角色均可正常使用
**Depends on**: Phase 80
**Requirements**: FLOW-03, COMPAT-01, COMPAT-02
**Success Criteria** (what must be TRUE):
  1. 批量执行多个任务时，每个任务独立获取 token 并注入到独立 BrowserSession，不跨任务复用浏览器实例或 token
  2. login_role 为 None 的任务执行路径与 v0.9.1 完全一致 — 不调用 token 获取、不尝试注入、走现有 5 步文字登录
  3. 7 种 UI 角色（main/special/vice/camera/platform/super/idle）均可成功获取 token 并构造 storage_state，不出现角色不支持错误
  4. 批量执行中部分任务注入失败时，失败任务回退到文字登录，其他任务不受影响继续执行
**Plans**: 2 plans

Plans:
- [x] 81-01-PLAN.md — Fix browser-use dict storage_state bug + E2E test infrastructure + 7-role verification (COMPAT-02)
- [x] 81-02-PLAN.md — Batch independent injection E2E tests + no-role regression tests (FLOW-03, COMPAT-01)

### v0.10.0 Agent 执行速度优化 (In Progress)

**Milestone Goal:** Agent 执行完成后自动生成可运行的 Playwright Python 测试代码，实现三层自愈管线（定位器回退 → LLM 修复 → Agent 重执行）

- [x] **Phase 82: 代码生成基础** — ActionTranslator 翻译 6 种核心操作 + PlaywrightCodeGenerator 组装完整测试文件 + 管线集成 (completed 2026-04-18)
- [x] **Phase 83: 定位器回退** — 主定位器失效时自动尝试备选定位器链（XPath → CSS → text），提高生成代码鲁棒性 (completed 2026-04-18)
- [x] **Phase 84: LLM 修复** — 定位器全部失败时 LLM 分析当前页面 DOM，自动生成修复后的定位器和代码 (completed 2026-04-18)
- [ ] **Phase 85: Agent 重执行** — 修复后代码自动重跑验证，通过后替换原始代码，形成完整自愈闭环

## Phase Details

### Phase 82: 代码生成基础
**Goal**: Agent 执行完成后，系统自动从 browser-use model_actions() 历史生成可运行的 Playwright Python 测试代码文件
**Requirements**: CODE-01, CODE-06
**Success Criteria** (what must be TRUE):
  1. ActionTranslator 处理 6 种核心操作类型（click, input, navigate, scroll, send_keys, go_back）为正确 Playwright API 调用
  2. 缺失 interacted_element 生成占位符而非崩溃
  3. PlaywrightCodeGenerator 生成语法有效的 Python 测试文件（含元数据头部、import、test 函数）
  4. 代码生成在 Agent 执行后自动触发，失败不阻塞管线
  5. 生成代码路径存入数据库 Run 记录

Plans:
- [x] 82-01-PLAN.md — ActionTranslator: browser-use 操作翻译为 Playwright 代码 (CODE-06)
- [x] 82-02-PLAN.md — PlaywrightCodeGenerator + DB 迁移 + 管线集成 (CODE-01)

### Phase 83: 定位器回退
**Goal**: 生成的 Playwright 代码执行时，主定位器失效自动尝试备选定位器链，提高代码在页面变更下的鲁棒性
**Depends on**: Phase 82
**Requirements**: HEAL-01
**Success Criteria** (what must be TRUE):
  1. Playwright 代码生成时为每个操作附带多个备选定位器（主 XPath + CSS + text），形成定位器链
  2. 执行生成的代码时，主定位器失败后自动尝试下一个备选定位器，无需人工干预
  3. 定位器回退过程记录日志，包含失败的定位器和最终成功的定位器
  4. 所有备选定位器都失败时，抛出明确的 HealerError 而非 Playwright 原生超时错误
**Plans**: 2 plans

Plans:
- [ ] 83-01-PLAN.md — LocatorChainBuilder + HealerError + ActionTranslator 多定位器回退 (HEAL-01)
- [ ] 83-02-PLAN.md — PlaywrightCodeGenerator logging 集成 + 完整文件语法验证 (HEAL-01)

### Phase 84: LLM 修复
**Goal**: 定位器全部失败时，LLM 分析当前页面 DOM 结构，自动生成修复后的定位器和代码
**Depends on**: Phase 83
**Requirements**: HEAL-02
**Success Criteria** (what must be TRUE):
  1. 定位器链全部失败时，系统自动捕获当前页面 HTML/DOM 快照和失败的操作描述
  2. LLM 接收页面快照 + 失败上下文，返回修复后的定位器和代码片段
  3. LLM 修复结果经过语法校验后才应用，不引入无效代码
  4. LLM 修复失败或超时时，记录原始错误信息，不阻塞后续操作
**Plans**: 2 plans

Plans:
- [x] 84-01-PLAN.md — LLMHealer class: LLM 调用 + DOM 分析 + ast.parse 验证 + 超时处理 (HEAL-02)
- [x] 84-02-PLAN.md — ActionTranslator 4th fallback layer + PlaywrightCodeGenerator LLM 集成 + runs.py 传参 (HEAL-02)

### Phase 85: Agent 重执行
**Goal**: 修复后的代码自动重跑验证，通过后存入数据库替换原始代码，形成完整的自愈闭环
**Depends on**: Phase 84
**Requirements**: HEAL-03
**Success Criteria** (what must be TRUE):
  1. LLM 修复后生成的代码自动重跑 Playwright 执行验证
  2. 验证通过后，修复后的代码路径存入数据库替换原始生成代码
  3. 验证失败时，记录失败原因并支持最多 2 次重试（LLM 修复 → 重跑）
  4. 自愈管线整体状态（尝试次数、最终结果）可在前端查看
**Plans**: 2 plans

Plans:
- [x] 85-01-PLAN.md — Data layer + SelfHealingRunner service + unit tests (HEAL-03)
- [ ] 85-02-PLAN.md — runs.py pipeline integration + frontend healing badge (HEAL-03)

## Progress

**Execution Order:**
Phases execute in numeric order: 79 -> 80 -> 81 -> 82 -> 83 -> 84 -> 85

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 79. Token 获取与 Storage State 构造 | v0.9.2 | 1/1 | Complete    | 2026-04-16 |
| 80. 执行流程集成 | v0.9.2 | 1/1 | Complete | 2026-04-17 |
| 81. 批量执行与兼容性验证 | v0.9.2 | 2/2 | Complete   | 2026-04-17 |
| 82. 代码生成基础 | v0.10.0 | 2/2 | Complete   | 2026-04-18 |
| 83. 定位器回退 | v0.10.0 | 0/2 | Complete    | 2026-04-18 |
| 84. LLM 修复 | v0.10.0 | 2/2 | Complete   | 2026-04-18 |
| 85. Agent 重执行 | v0.10.0 | 1/2 | In Progress|  |

---
*Roadmap updated: 2026-04-18 — Phase 85 plans created (Agent re-execution)*
