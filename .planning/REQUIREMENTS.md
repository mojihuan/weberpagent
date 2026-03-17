# Requirements: aiDriveUITest

**Defined:** 2026-03-14
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

---

## v0.1 Requirements (Complete)

### Foundation

- [x] **FND-01**: Environment configuration is centralized (no hardcoded URLs/API keys)
- [x] **FND-02**: API responses use consistent format (success, data, error, meta)
- [x] **FND-03**: All async database operations use async engine (no blocking)
- [x] **FND-04**: LLM temperature is set to 0 for deterministic test execution
- [x] **FND-05**: Browser cleanup uses try/finally pattern (no memory leaks)

### Database

- [x] **DATA-01**: Assertion model exists with type, expected fields (links to Task via task_id)
- [x] **DATA-02**: AssertionResult model exists with status, message, actual_value fields (links to Run and Assertion)
- [x] **DATA-03**: Run-Assertion relationship is properly configured
- [x] **DATA-04**: Screenshot storage uses file system (not BLOB in database) — **Already implemented**
- [x] **DATA-05**: RunRepository.get_steps() method exists and works

### Service Layer

- [x] **SVC-01**: AssertionService validates assertions against Run results
- [x] **SVC-02**: ReportService generates test reports with all step details
- [x] **SVC-03**: AgentService uses proper LLM configuration (Temperature=0)
- [x] **SVC-04**: SSE EventManager includes heartbeat events (15-30s interval)
- [x] **SVC-05**: All background tasks update database status on completion/error

### Frontend

- [x] **UI-01**: API types match backend response schemas exactly
- [x] **UI-02**: Task list displays all tasks with correct data
- [x] **UI-03**: Execution Monitor shows real-time step updates via SSE
- [x] **UI-04**: Screenshot panel displays images from correct paths
- [x] **UI-05**: Report page shows assertion results and step details
- [x] **UI-06**: API base URL is configurable via environment variable

### End-to-End Flow

- [x] **E2E-01**: User can create a new test task with natural language description
- [x] **E2E-02**: User can execute a task and see real-time progress
- [x] **E2E-03**: User can view execution screenshots for each step
- [x] **E2E-04**: User can view final test report with assertion results
- [x] **E2E-05**: Complete flow works without errors (create -> execute -> monitor -> report)

---

## v0.2 Requirements (Current Milestone)

### 前置条件系统

- [x] **PRE-01**: 用户可以在测试用例中定义前置条件步骤
- [x] **PRE-02**: 前置条件通过 API 调用执行（不用 UI）
- [x] **PRE-03**: 支持复用现有项目的 API 封装方法
- [x] **PRE-04**: 前置条件执行结果可用于后续步骤

### 接口断言集成

- [ ] **API-01**: 用户可以通过 API 调用进行接口断言
- [x] **API-02**: 用户可以进行时间断言（±1 分钟范围）
- [x] **API-03**: 用户可以进行数据断言（匹配预期值）
- [x] **API-04**: 断言结果展示在测试报告中

### 动态数据支持

- [x] **DYN-01**: 支持随机数生成（SF 物流单号、手机号等）
- [x] **DYN-02**: 支持从 API 接口获取动态数据
- [x] **DYN-03**: 支持跨步骤数据缓存和复用
- [x] **DYN-04**: 支持时间计算（now ± 1 分钟）

---

## v0.3 Requirements (Future)

Deferred to future release.

### 批量执行

- **BATCH-01**: Excel 用例导入
- **BATCH-02**: 批量运行测试用例
- **BATCH-03**: 批量执行结果汇总

---

## Out of Scope

Explicitly excluded from v0.2.

| Feature | Reason |
|---------|--------|
| 用户认证/权限管理 | v0.2 单用户本地使用 |
| 服务器部署 | 仅需本地开发环境 |
| 批量执行 | 推迟到 v0.3 |
| 多语言支持 | 只支持中文 |

---

## Traceability

Which phases cover which requirements.

| Requirement | Phase | Status |
|-------------|-------|--------|
| FND-01 | Phase 1 | Complete |
| FND-02 | Phase 1 | Complete |
| FND-03 | Phase 1 | Complete |
| FND-04 | Phase 1 | Complete |
| FND-05 | Phase 1 | Complete |
| DATA-01 | Phase 2 | Complete |
| DATA-02 | Phase 2 | Complete |
| DATA-03 | Phase 2 | Complete |
| DATA-04 | Phase 2 | Complete |
| DATA-05 | Phase 2 | Complete |
| SVC-01 | Phase 3 | Complete |
| SVC-02 | Phase 3 | Complete |
| SVC-03 | Phase 3 | Complete |
| SVC-04 | Phase 3 | Complete |
| SVC-05 | Phase 3 | Complete |
| UI-01 | Phase 4 | Complete |
| UI-02 | Phase 4 | Complete |
| UI-03 | Phase 4 | Complete |
| UI-04 | Phase 4 | Complete |
| UI-05 | Phase 4 | Complete |
| UI-06 | Phase 4 | Complete |
| E2E-01 | Phase 4 | Complete |
| E2E-02 | Phase 4 | Complete |
| E2E-03 | Phase 4 | Complete |
| E2E-04 | Phase 4 | Complete |
| E2E-05 | Phase 4 | Complete |
| PRE-01 | Phase 5 | Complete |
| PRE-02 | Phase 5 | Complete |
| PRE-03 | Phase 5 | Complete |
| PRE-04 | Phase 5 | Complete |
| API-01 | Phase 8 (Gap Closure) | Pending |
| API-02 | Phase 6 | Complete |
| API-03 | Phase 6 | Complete |
| API-04 | Phase 6 | Complete |
| DYN-01 | Phase 7 | Complete |
| DYN-02 | Phase 7 | Complete |
| DYN-03 | Phase 7 | Complete |
| DYN-04 | Phase 7 | Complete |

**Coverage:**
- v0.1 requirements: 26 total, 26 mapped, 0 unmapped ✓
- v0.2 requirements: 12 total, 12 mapped, 0 unmapped ✓

---
*Requirements defined: 2026-03-14*
*Last updated: 2026-03-17 - API-01 assigned to Phase 8 gap closure*
