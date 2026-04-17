# Requirements: aiDriveUITest v0.9.2

**Defined:** 2026-04-16
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告
**Milestone:** v0.9.2 Cookie 预注入免登录

## v1 Requirements

### PREAUTH (预认证)

- [x] **AUTH-01**: 系统能通过 LoginApi HTTP 接口获取指定角色的 ERP 登录 token，并构造为 browser-use BrowserProfile 可用的 storage_state 格式（含 Cookie/localStorage）
- [x] **AUTH-02**: browser-use Agent 创建时接受外部传入的 storage_state，浏览器启动即携带认证信息，打开 ERP 页面时已处于登录状态

### FLOW (执行流程)

- [x] **FLOW-01**: Cookie 预注入成功时，跳过 TestFlowService 的 5 步登录文字指令，Agent 直接从 ERP 首页开始业务操作
- [x] **FLOW-02**: Cookie 预注入失败时（API 超时/网络错误/返回异常），自动回退到现有 5 步文字登录流程，并记录 warning 日志
- [x] **FLOW-03**: 批量执行时，每个任务独立获取 token 并注入到新 BrowserSession，不跨任务复用浏览器实例

### COMPAT (兼容性)

- [x] **COMPAT-01**: 无 login_role 的任务执行路径完全不变，行为与 v0.9.1 一致
- [x] **COMPAT-02**: 支持 v0.9.1 定义的全部 7 种 UI 角色 (main/special/vice/camera/platform/super/idle)

## v2 Requirements

### Session Reuse

- **SESS-01**: 批量执行同角色任务时复用浏览器实例，避免重复创建/销毁浏览器
- **SESS-02**: Token 缓存机制，同角色多次执行时复用未过期的 token

## Out of Scope

| Feature | Reason |
|---------|--------|
| 浏览器实例复用 | 用户选择每次独立注入，复杂度高，推迟到 v2 |
| Token 持久缓存 | 单次执行场景不需要，批量执行用独立注入更可靠 |
| 前端 UI 变更 | 预注入对 QA 用户透明，无需前端改动 |
| headless/headed 切换 | 与 Cookie 注入无关，不在本里程碑范围 |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | Phase 79 | Complete |
| AUTH-02 | Phase 79 | Complete |
| FLOW-01 | Phase 80 | Complete |
| FLOW-02 | Phase 80 | Complete |
| FLOW-03 | Phase 81 | Complete |
| COMPAT-01 | Phase 81 | Complete |
| COMPAT-02 | Phase 81 | Complete |

**Coverage:**
- v1 requirements: 7 total
- Mapped to phases: 7
- Unmapped: 0

---
*Requirements defined: 2026-04-16*
*Last updated: 2026-04-16 after roadmap creation*
