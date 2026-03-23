# Milestones

## v0.4.2 人工验证断言系统 (Shipped: 2026-03-23)

**Phases completed:** 2 phases, 2 plans, 0 tasks

**Key accomplishments:**

- Status:

---

## v0.4.1 断言系统调通 (Shipped: 2026-03-22)

**Phases completed:** 6 phases, 10 plans, 22 tasks

**Key accomplishments:**

- AST-based parser extracts assertion fields from base_assertions_field.py with grouping and Chinese descriptions
- 1. [Rule 1 - Bug] Test mock target mismatch
- File:
- Created FieldParamsEditor component with collapsible groups, search filtering, and "now" button for time fields, following the AssertionSelector pattern for consistent UX.
- Three-layer assertion parameter configuration with FieldParamsEditor integration for field_params support
- POST /api/external-assertions/execute endpoint with three-layer parameters (data, api_params, field_params) and backward compatibility
- Unit tests verifying three-layer parameters, "now" conversion, backward compatibility, and 'name' field in assertion error responses.
- Fixed execute_all_assertions() to extract and pass api_params, field_params, and params to execute_assertion_method(), closing the gap between UI field configuration (Phase 29) and assertion execution adapter (Phase 30).

---

## v0.4.0 断言系统集成 (Shipped: 2026-03-21)

**Phases completed:** 5 phases, 13 plans, 26 tasks

**Key accomplishments:**

- Added load_base_assertions_class() function to ExternalPreconditionBridge following the exact pattern established for data method loading, enabling discovery and loading of PcAssert/MgAssert/McAssert classes from webseleniumerp.
- Implemented assertion method discovery with data options and parameter options parsing for PcAssert/MgAssert/McAssert classes
- GET /api/external-assertions/methods endpoint exposing assertion methods with headers_options, data_options, and parameter options for frontend configuration
- Frontend types and API client for business assertions with backend schema support
- AssertionSelector modal component with grouped method browsing, search filtering, multi-select tags, and parameter configuration (headers, data, i/j/k)
- Tab switching UI in TaskForm integrating AssertionSelector for business assertions with separate API code assertions tab
- resolve_headers() and execute_assertion_method() functions with 30-second timeout protection and LoginApi header resolution
- Context storage infrastructure for assertion results with index-based naming and summary aggregation
- External assertion execution integrated into run_test flow with SSE events and context storage
- E2E test suite for assertion workflow with 5 tests covering configuration, execution, and report verification using Playwright
- Added 9 unit tests covering resolve_headers() header resolution and _parse_assertion_error() message parsing with full mocking isolation.
- TestExecuteAssertionMethod class with 7 async tests covering success, AssertionError, timeout, and all 4 error types (class/method not found, headers resolution error, import error)

---

## v0.3.2 测试与Bug修复 (Shipped: 2026-03-20)

**Phases completed:** 3 phases (Phase 20-22), 15 plans, 13 requirements

**Key accomplishments:**

1. E2E 测试覆盖 - DataMethodSelector、变量替换、完整执行流程
2. 单元测试覆盖 - ContextWrapper.get_data()、变量替换、API 端点
3. 测试修复 - 16 个失败测试修复，18 个遗留测试归档
4. UI 修复 - DataMethodSelector 折叠分组、类型提示、ESC 键
5. 报告增强 - 前置条件执行信息展示（状态、耗时、变量、代码视图）
6. UAT 全部通过 - 7/7 测试用例通过

**Tech Debt:**

- 5 pre-existing unit test isolation issues (documented in 22-06-SUMMARY.md)
- E2E tests deferred pending running servers

---

## v0.3.1 数据获取方法集成 (Shipped: 2026-03-19)

**Phases completed:** 3 phases, 11 plans, 2 tasks

**Key accomplishments:**

- (none recorded)

---

## v0.3 前置条件集成 (Shipped: 2026-03-18)

**Phases completed:** 6 phases, 18 plans, 6 tasks

**Key accomplishments:**

- (none recorded)

---

## v0.3 前置条件集成 (Shipped: 2026-03-18)

**Phases completed:** 6 phases, 18 plans, 6 tasks

**Key accomplishments:**

- (none recorded)

---

## v0.3.1 - 前置条件数据传递（待规划）

**目标**: 扩展前置条件系统，支持从 FA1/HC1 等操作获取返回数据（如 IMEI）并传递给后续步骤。

**需求**:

- [ ] 执行 FA1/HC1 后获取返回数据
- [ ] 自动提取关键字段（如 IMEI）存入 context
- [ ] 在后续步骤中使用 `{{imei}}` 引用
- [ ] 支持调用 webseleniumerp 的 `inventory_list_data()` 等数据获取方法

**用例**:

```
前置条件: FA1（新增采购入库） → 获取 IMEI
步骤: 输入 {{imei}} 到表单
```

---

## v0.3 前置条件集成 (Shipped: 2026-03-18)

**Phases completed:** 4 phases (Phase 13-16), 12 plans

**Key accomplishments:**

1. 配置基础 - WEBSERP_PATH 环境变量, 启动验证, 文档模板
2. 后端桥接模块 - ExternalPreconditionBridge, 操作码 API, PreconditionService 集成
3. 前端集成 - OperationCodeSelector 组件, 模块分组显示, 代码生成
4. 端到端验证 - E2E 测试, 错误场景测试, 手动测试检查清单

---

## v0.2.1 测试用例调通 (Shipped: 2026-03-18)

**Phases completed:** 2 phases (Phase 9-10), 6 plans

**Key accomplishments:**

1. 登录用例调通 - 端到端执行成功，报告正确展示
2. 销售出库用例 - 前置条件配置、动态数据生成、API 断言验证通过

**Note:** Phase 11-12 (Bug 修复、文档指南) 推迟到后续版本

---

## v0.2 前置条件、接口断言、动态数据 (Shipped: 2026-03-17)

**Phases completed:** 4 phases (Phase 5-8), 15 plans

**Key accomplishments:**

1. 前置条件系统 - 支持 Python 代码格式，Jinja2 变量替换，SSE 实时监控
2. 接口断言集成 - ApiAssertionService 支持时间和数据断言，断言结果独立展示
3. 动态数据支持 - 随机数生成器、时间计算、跨步骤数据缓存
4. 前端实时监控完善 - SSE 事件处理器、报告数据完整性修复

**Tech Debt:**

- Nyquist Wave 0 tasks pending (tests defined but not run)
- Pre-existing TypeScript errors in ApiAssertionResults.tsx, RunList.tsx (not blocking)

---

## v0.1 MVP (Shipped: 2026-03-14)

**Phases completed:** 4 phases (Phase 1-4), 22 plans

**Key accomplishments:**

- Foundation fixes, data layer enhancement, service layer restoration, frontend + E2E alignment
