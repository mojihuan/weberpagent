# Requirements: aiDriveUITest v0.11.3

**Defined:** 2026-05-02
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v0.11.3 Requirements — 代码彻底的 Review

### 正确性 (CORR)

- [x] **CORR-01**: 审查后端核心业务逻辑正确性 — agent 层 (MonitoredAgent, detectors, prompts)、core services (agent_service, code_generator, precondition_service)、pipeline 编排 (run_pipeline.py) 的逻辑错误、边界条件、潜在 bug
- [x] **CORR-02**: 审查 API 路由层正确性 — routes 目录下所有路由文件的参数验证、错误处理、边界条件、异常路径
- [x] **CORR-03**: 审查前端组件逻辑正确性 — React 组件状态管理、事件处理、数据流、SSE 事件处理

### 安全性 (SEC)

- [x] **SEC-01**: 审查安全风险 — 路径遍历、CSRF 防护、exec() 安全、不安全配置、SSRF 风险

### 性能 (PERF)

- [ ] **PERF-01**: 审查异步/并发性能 — 阻塞操作混入 async 代码、资源竞争、内存泄漏、SSE 连接管理
- [x] **PERF-02**: 审查前端性能 — 渲染性能、大列表优化、不必要重渲染、React Query 缓存策略

### 可维护性 (MAINT)

- [ ] **MAINT-01**: 审查 DRY/SOLID 违反 — 代码重复、单一职责违反、开闭原则违反
- [ ] **MAINT-02**: 审查代码结构复杂度 — 函数长度、文件大小、循环复杂度、嵌套深度
- [ ] **MAINT-03**: 审查命名规范性 — 变量/函数/模块命名不一致、误导性命名

### 设计与架构 (ARCH)

- [x] **ARCH-01**: 审查模块耦合度 — 跨层直接依赖、循环依赖、紧耦合模块
- [x] **ARCH-02**: 审查抽象合理性 — 过度抽象、不足抽象、错误的抽象层次
- [ ] **ARCH-03**: 审查横切关注点 — 错误处理策略一致性、配置管理、日志策略

### 测试 (TEST)

- [ ] **TEST-01**: 识别关键测试缺失 — 哪些核心业务流程缺少测试保护、高 ROI 测试场景
- [ ] **TEST-02**: 识别边界情况覆盖不足 — 边界值、异常路径、竞态条件、超时场景

## Out of Scope

| Feature | Reason |
|---------|--------|
| SQL 注入审查 | SQLAlchemy ORM + parameterized queries，风险极低 |
| XSS 审查 | React 默认转义 + 后端不渲染 HTML |
| 敏感信息泄露审查 | 单用户本地部署，无公开暴露面 |
| 数据库性能审查 | SQLite 单用户场景，无高并发需求 |
| 修复实施 | 本里程碑仅输出发现和建议，不实施修复 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CORR-01 | Phase 125 | Complete |
| CORR-02 | Phase 126 | Complete |
| CORR-03 | Phase 127 | Complete |
| SEC-01 | Phase 126 | Complete |
| PERF-01 | Phase 128 | Pending |
| PERF-02 | Phase 127 | Complete |
| MAINT-01 | Phase 128 | Pending |
| MAINT-02 | Phase 128 | Pending |
| MAINT-03 | Phase 128 | Pending |
| ARCH-01 | Phase 125 | Complete |
| ARCH-02 | Phase 125 | Complete |
| ARCH-03 | Phase 128 | Pending |
| TEST-01 | Phase 129 | Pending |
| TEST-02 | Phase 129 | Pending |

**Coverage:**
- v0.11.3 requirements: 14 total
- Mapped to phases: 14
- Unmapped: 0

---
*Requirements defined: 2026-05-02*
*Last updated: 2026-05-02 — traceability updated after roadmap creation*
