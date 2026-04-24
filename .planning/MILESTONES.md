# Milestones

## v0.10.4 Playwright 代码验证与任务管理集成 (Shipped: 2026-04-24)

**Phases completed:** 2 phases, 4 plans, 8 tasks

**Key accomplishments:**

- GET /runs/{run_id}/code endpoint returning line-numbered Python code with path traversal protection and TaskUpdate schema expansion
- POST /execute-code endpoint with Semaphore(1) concurrency guard, async SelfHealingRunner execution, and automatic Task.status="success" on passed result
- Backend TaskResponse extended with has_code/latest_run_id computed from runs, frontend Task type updated, context-aware StatusBadge, and code API functions for Plan 02 UI components
- TaskTable "代码" column with blue/gray Code2 icons, CodeViewerModal with react-syntax-highlighter Python display, and execution controls with 2-second polling

---

## v0.10.3 DOM 深度修复 - 表格单元格选择精确性 (Shipped: 2026-04-23)

**Phases completed:** 3 phases, 4 plans

**Key accomplishments:**

- _td_child_depth helper and extended _patch_should_exclude_child to protect div/span inside td up to 2 layers from bbox flattening
- _get_column_header helper and Patch 8 injecting <!-- 列: {header} --> comments above td nodes via thead th position mapping, with full DEPTH-02 regression pass
- Rewrote ENHANCED_SYSTEM_MESSAGE Section 9 with row+column annotation cross-positioning, replacing placeholder matching with four-segment logical chain (locate/operate/verify/recover)
- DEPTH-05 E2E test confirming Agent correctly selects sales amount column (not profit column) via step reasoning analysis and run outcome validation

---

## v0.10.2 测试验证与代码可用性修复 (Shipped: 2026-04-23)

**Phases completed:** 4 phases, 7 plans, 13 tasks

**Key accomplishments:**

- Deleted 37 obsolete test files and 4 stale test methods, eliminating all ImportError errors from the pytest suite
- Audited all 8 test files with autouse fixtures and added 2 missing get_settings cache reset fixtures for hermetic test isolation
- Top-level conftest.py with db_session fixture and autouse cache reset, plus alignment of 4 test files with current execute_assertion_method (headers as string identifier, GROUP_RULES priority)
- sys.modules/sys.path cleanup fixtures, bridge early-return guard, and repository assertions pop -- achieving 876 passed, 0 failed, 0 errors
- Docstring-based method discovery with ImportApi._module_map alias patching to resolve webseleniumerp obfuscated method name changes
- Add docstring_id field to data methods API response with Optional[str] backward compatibility
- E2E tests validating full pipeline (task -> run -> report), docstring method mapping, and PcAssert assertion execution with three-phase ImportApi alias patching fix

---

## v0.10.1 代码登录及 Agent 复用登录的浏览器状态 (Shipped: 2026-04-21)

**Phases completed:** 4 phases, 6 plans, 12 tasks

**Key accomplishments:**

- POC scripts confirm localStorage injection fails (Vuex/Pinia store timing) but programmatic form login works with dispatchEvent(new MouseEvent) instead of native .click()
- Comprehensive ERP login mechanism research report confirming 方案 A (programmatic form login with MouseEvent dispatch) as the viable path for Phase 87, with root cause analysis proving 方案 C (localStorage injection) fails due to Vuex/Pinia store initialization timing
- 修复 Vue SPA 编程式登录：dispatchEvent(MouseEvent) 替代 btn.click() + 完整表单事件序列 + 回退日志角色名增强
- Purged dead auth branches and relocated storage_state construction to its sole consumer (self_healing_runner)
- Aligned test suite with Plan 01 auth cleanup: deleted E2E tests, replaced auth_session_factory mocks with pre_navigate/create_browser_session mocks, 27 unit tests pass
- 5 unit tests for _build_storage_state and _get_storage_state_for_role covering token injection, origin parsing, error propagation, and full pipeline verification

---

## v0.9.0 Excel 批量导入功能开发 (Shipped: 2026-04-09)

**Phases completed:** 4 phases, 8 plans, 15 tasks

**Key accomplishments:**

- TEMPLATE_COLUMNS column contract + generate_template() producing styled .xlsx with DataValidation + GET /tasks/template StreamingResponse endpoint
- ExcelParser with collect-all error strategy, lenient type coercion (_coerce_string/_coerce_int/_coerce_json_list), ParsedRow/ParseResult frozen dataclasses, and template round-trip validation
- Two-phase Excel import: POST /import/preview returns row-level validation, POST /import/confirm atomically creates Tasks in a single db.begin() transaction
- ImportModal with 3-step state machine (upload/preview/result), raw fetch FormData upload, drag-and-drop with .xlsx validation
- Batch ORM model, BatchExecutionService with Semaphore concurrency (default 2, cap 4), and POST/GET /batches API routes for parallel task execution
- Batch execution UI with Play icon button, confirmation dialog with concurrency slider (1-4), and API client wired to POST /batches
- Extended BatchRunSummary with started_at/finished_at nullable datetime fields across backend schema, API routes, and frontend TypeScript type
- Batch progress page with 2s polling, task status cards with elapsed time, progress bar, click-to-navigate to run details, and completion toast notification

---

## v0.8.3 分析报告差距对表格填写影响 (Shipped: 2026-04-06)

**Phases completed:** 2 phases, 2 plans, 3 tasks

**Key accomplishments:**

- 四项 Agent 表格交互优化策略设计文档，覆盖行标识定位、反重复机制、三级策略优先级和失败恢复规则，输出 16 项可直接转化的代码任务

---

## v0.8.1 修复销售出库表格填写问题 (Shipped: 2026-04-06)

**Phases completed:** 7 phases, 9 plans, 11 tasks

**Key accomplishments:**

- Unified TimelineItem with precondition (amber/FileCode), assertion (purple/ShieldCheck), and UI step rendering interleaved in execution order via replace-not-append SSE stream
- Unified timeline in report detail replaces 3 separate sections with single interleaved list of steps, preconditions, and assertions using Phase 58-consistent color scheme
- Removed all backend api_assertions feature traces: service file, schema fields, model column, execution logic, report computation, and 3 test files
- Removed all frontend api_assertions traces: types, SSE hook, StepTimeline rendering, TaskForm tab switcher, and ApiAssertionResults component; TaskForm now shows business assertions unconditionally
- DOM Patch marks td cells as interactive for click-to-edit tables, plus Section 9 prompt guidance for ERP sales outbound filling

---

## v0.8.0 报告完善与 UI 优化 (Shipped: 2026-04-03)

**Phases completed:** 5 phases, 6 plans, E2E verified

**Key accomplishments:**

- Phase 57: parseReasoning() utility + ReasoningText component — Eval/Verdict/Memory/Goal 分行彩色 badge 展示（紫/绿/橙/蓝），替代 `|` 分隔单行文本
- Phase 58: StepTimeline 统一时间线 — TimelineItem discriminated union (step|precondition|assertion)，前置条件/断言步骤与普通步骤交错排列，auto-scroll 滚动
- Phase 59: 报告详情时间线 — PreconditionResult model + global sequence_number + timeline API，ReportTimelineItem union (step|precondition|assertion)，向后兼容 fallback 渲染
- Phase 60: 任务表单优化 — 删除 api_assertions 相关全部代码（backend + frontend），AssertionSelector 直接展示，无 tab 切换
- Phase 61: E2E 验证 — 6/6 检查全部 PASS（SC-1 执行监控、SC-2 报告详情、SC-3 任务表单、SC-4 向后兼容），FMT-01/02/03 经手动验证完成

**Tech Debt:** 无新增

---

## v0.7.0 更多操作边界测试 (Shipped: 2026-04-01)

**Phases completed:** 5 phases, 10 plans, 22 tasks

**Key accomplishments:**

- Added 3-line keyboard operation section to ENHANCED_SYSTEM_MESSAGE with send_keys guidance for Enter search, Escape close, and Control+a select-all
- Verified Agent send_keys('Enter') compliance in purchase order ERP scenario; keyboard prompt enhancement confirmed effective, 1/3 scenarios passing
- Strengthened Escape and Control+a keyboard prompt with negation instructions; verified Escape PASS and Control+a PARTIAL PASS (browser runtime limitation)
- Added section 7 table interaction guidance to ENHANCED_SYSTEM_MESSAGE covering checkbox (thead/tbody), hyperlink text clicks, and icon button title/aria-label positioning
- All 4 ERP purchase order table interaction scenarios verified passing — checkbox single-row (TBL-01), checkbox select-all (TBL-02), hyperlink text click (TBL-03), icon button title/aria-label (TBL-04)
- Monkey-patch browser-use DOM serializer to give span.hand and .el-checkbox independent clickable indices, integrated into Agent creation with updated prompt
- scan_test_files() scans data/test-files/ for absolute paths, available_file_paths injected into MonitoredAgent, and Section 8 file upload prompt added with upload_file guidance and negation instructions
- Excel import (IMP-01) and image upload (IMP-02) both verified passing in ERP -- Agent correctly uses upload_file action for both file types, confirming Section 8 prompt and scan_test_files infrastructure work end-to-end
- Created AST-01/02 assertion verification test steps document and confirmed all E2E test environment dependencies are ready
- 11/11 E2E test cases passed (100%) covering keyboard, table, file upload, and assertion scenarios with no regressions

---

## v0.6.3 Agent 可靠性优化 (Shipped: 2026-03-28)

**Phases completed:** 4 phases, 10 plans, 20 tasks

**Key accomplishments:**

- StallDetector with consecutive failure detection (2 same-target failures) and stagnant DOM detection (3 identical hashes), frozen StallResult, 100% test coverage
- Regex-based form field validation guard with frozen GuardResult, blocking submit clicks on value mismatch
- TDD-built TaskProgressTracker with 4 step format parsers and budget-aware warning/urgent thresholds
- MonitoredAgent(Agent) subclass wiring StallDetector, PreSubmitGuard, TaskProgressTracker via _pending_interventions bridge and _execute_actions() blocking
- ENHANCED_SYSTEM_MESSAGE replacing CHINESE_ENHANCEMENT with 5-section ERP-specific guidance: click-to-edit tables, failure recovery, field verification, pre-submit validation, and merged selector strategy
- ENHANCED_SYSTEM_MESSAGE wired into Agent constructor with 4 tuned browser-use parameters (loop_detection, max_failures, replan_on_stall, enable_planning)
- MonitoredAgent replaces Agent in run_with_streaming() with 3 fresh detector instances per run and run_logger for structured monitor logging
- Detector wiring in step_callback: StallDetector.check(), TaskProgressTracker.check_progress()/update_from_evaluation() called with monitor-category structured logging and non-blocking error handling
- 60/60 Phase 48-50 unit tests pass, 94% coverage across 5 target modules (all >= 80%), full regression suite confirms zero Phase 48-50 regressions
- E2E ERP sales outbound test confirmed StallDetector stall detection works in production, with run_logger argument bug fixed mid-verification

---

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
