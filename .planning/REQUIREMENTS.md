# Requirements: aiDriveUITest v0.9.1

**Defined:** 2026-04-11
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告
**Milestone:** v0.9.1 ERP 全面集成重构

## v1 Requirements

### Cache（参数缓存）

- [x] **CACHE-01**: CacheService 提供 cache(key, value) 存储和 cached(key) 读取，返回不可变副本
- [x] **CACHE-02**: CacheService 生命周期绑定单个 Run，Run 结束自动销毁
- [x] **CACHE-03**: ContextWrapper 新增 cache/cached 方法委托到 CacheService
- [ ] **CACHE-04**: 前置条件支持 cache 类型 JSON 配置，调用外部数据方法并缓存提取字段
- [x] **CACHE-05**: 任务描述中 {{cached:key}} 语法引用缓存值

### Account（多账号登录）

- [ ] **ACCT-01**: AccountService 从 webseleniumerp/config/user_info.py 读取 7 种 UI 登录角色配置（main/special/vice/camera/platform/super/idle），bot 角色因登录方式不同不适用 UI 自动登录
- [ ] **ACCT-02**: AccountService.resolve(role) 返回 AccountInfo(account, password, role) frozen dataclass
- [ ] **ACCT-03**: 登录 URL 从 settings.py 的 ERP_LOGIN_URL 读取，不暴露在 Excel 中
- [x] **ACCT-04**: TestFlowService 自动注入登录步骤（打开URL → 输入账号 → 输入密码 → 点击登录）

### Flow（流程编排）

- [x] **FLOW-01**: TestFlowService 编排完整流程：解析角色 → 创建缓存 → 执行前置 → 构建描述 → Agent执行 → 断言
- [x] **FLOW-02**: 两阶段变量替换：regex 处理 {{cached:key}}，Jinja2 处理 {{variable}}
- [ ] **FLOW-03**: run_agent_background 通过 task.login_role 分支：有值走新流程，无值走现有流程
- [ ] **FLOW-04**: 共享 CacheService 实例贯穿前置条件和断言阶段

### Data（数据层）

- [x] **DATA-01**: Task 模型增加 login_role VARCHAR(20) nullable 字段
- [x] **DATA-02**: TaskCreate/TaskUpdate/TaskResponse schema 支持 login_role
- [ ] **DATA-03**: Excel 模板 TEMPLATE_COLUMNS 新增「登录角色」列（第二列）
- [ ] **DATA-04**: Excel 解析器正确映射 login_role 列到 Task 字段
- [ ] **DATA-05**: 前端任务表单新增 login_role 下拉选择（8 种角色）

## v2 Requirements

### Cache（高级缓存）

- **CACHE-06**: 断言支持 cache_verify 类型，验证缓存值在查询结果中存在
- **CACHE-07**: 缓存过期机制（TTL）
- **CACHE-08**: 持久化缓存（跨 Run 复用）

### Account（账号管理）

- **ACCT-05**: 前端账号管理 UI（添加/编辑角色）
- **ACCT-06**: 每个 Run 支持多账号切换（中途重新登录）

### Flow（高级编排）

- **FLOW-05**: 登录步骤凭据脱敏（日志和报告中隐藏密码）
- **FLOW-06**: 登录失败自动重试机制
- **FLOW-07**: 步骤编号动态偏移（根据实际登录步数调整）

## Out of Scope

| Feature | Reason |
|---------|--------|
| 修改 agent_service.py | Agent 执行逻辑不变，只改输入 |
| 修改 batch_execution.py | 批量执行逻辑不变，login_role 自然传递 |
| 修改 webseleniumerp/ | 不修改外部项目代码 |
| Redis/memcached 缓存 | 单进程部署，内存 dict 足够 |
| Alembic 数据库迁移 | SQLite nullable 列无需正式迁移框架 |
| 用户认证/权限管理 | 单用户本地使用 |
| 多语言支持 | 只支持中文 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CACHE-01 | Phase 74 | Complete |
| CACHE-02 | Phase 74 | Complete |
| CACHE-03 | Phase 74 | Complete |
| CACHE-04 | Phase 77 | Pending |
| CACHE-05 | Phase 77 | Complete |
| ACCT-01 | Phase 75 | Pending |
| ACCT-02 | Phase 75 | Pending |
| ACCT-03 | Phase 75 | Pending |
| ACCT-04 | Phase 77 | Complete |
| FLOW-01 | Phase 77 | Complete |
| FLOW-02 | Phase 77 | Complete |
| FLOW-03 | Phase 77 | Pending |
| FLOW-04 | Phase 77 | Pending |
| DATA-01 | Phase 76 | Complete |
| DATA-02 | Phase 76 | Complete |
| DATA-03 | Phase 76 | Pending |
| DATA-04 | Phase 76 | Pending |
| DATA-05 | Phase 76 | Pending |

**Coverage:**
- v1 requirements: 18 total
- Mapped to phases: 18
- Unmapped: 0

---
*Requirements defined: 2026-04-11*
*Last updated: 2026-04-11 after roadmap creation*
