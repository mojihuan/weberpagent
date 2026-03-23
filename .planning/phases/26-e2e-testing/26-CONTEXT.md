# Phase 26: E2E Testing - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary

验证 Phase 23-25 断言系统的端到端流程。通过 E2E 自动化测试和手动验证，确保：
1. QA 能创建带断言配置的测试任务并端到端执行
2. 断言成功/失败结果正确显示在测试报告中
3. 多个断言在单个测试中都执行（验证非 fail-fast）
4. 断言结果可通过 context 变量访问

**Scope:**
- 使用真实 ERP 环境进行 E2E 测试
- 复用销售出库用例进行验证
- 测试单个断言成功 + 单个断言失败场景
- 验证报告页面 UI 元素正确显示断言结果
- 创建手动验证检查清单

**Out of Scope:**
- 单元测试覆盖（Phase 27）
- Bug 修复（如有问题则创建新 phase）
- 新功能开发
- Context 变量引用验证（后续需求）
- Mock 数据支持

</domain>

<decisions>
## Implementation Decisions

### E2E 测试环境
- **使用真实 ERP 环境**: 必须配置 ERP_BASE_URL、ERP_USERNAME、ERP_PASSWORD
- **配置缺失处理**: 直接失败，强制要求 ERP 配置
- **测试隔离**: 复用销售出库用例，不创建专用测试数据

### E2E 测试范围
- **测试场景**:
  1. 单个断言成功 — 验证成功状态展示
  2. 单个断言失败 — 验证失败状态展示 + 字段详情
- **非 fail-fast 验证**: 确保多个断言都执行，不会因为第一个失败而终止
- **断言方法选择**: Claude 根据实际环境选择合适的断言方法

### 报告验证方式
- **UI 元素检查**: 检查报告页面显示断言结果卡片、通过/失败状态、字段详情
- **不验证 API 响应**: 专注 UI 展示验证
- **不验证 Context 变量引用**: context 变量引用功能不在 E2E 范围

### 测试用例复用
- **复用销售出库用例**: 在现有用例基础上添加断言配置
- **减少开发量**: 不创建专用断言测试用例

### E2E 测试失败处理
- **保存详细诊断信息**: 截图、网络请求、控制台日志
- **Playwright trace**: on-first-retry 模式
- **失败截图**: only-on-failure 模式
- **视频保留**: retain-on-failure 模式

### 手动验证
- **执行时机**: E2E 测试全部通过后执行
- **验证场景**: 完整销售出库用例（前置条件 + 断言配置 + AI 执行 + 报告查看）
- **检查清单详细度**: 每个断言 UI 元素、状态变化都有明确的验证点
- **环境要求**: 真实 ERP 环境

### 测试结果记录
- **格式**: 创建 VERIFICATION.md 记录验证结果
- **内容**: 测试通过情况、发现的问题、验证截图

### Claude's Discretion
- 具体选择哪个断言方法进行测试
- E2E 测试用例的具体实现细节
- 手动验证检查清单的具体条目
- VERIFICATION.md 的具体格式
- 失败诊断信息的具体内容

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心实现参考
- `backend/core/external_precondition_bridge.py` — execute_assertion_method() 实现
- `backend/core/agent_service.py` — 断言执行集成点、SSE 事件推送
- `backend/api/routes/external_assertions.py` — 断言方法 API 端点
- `frontend/src/components/TaskModal/AssertionSelector.tsx` — 断言选择器组件
- `frontend/src/components/TaskModal/TaskForm.tsx` — 断言 Tab 集成
- `frontend/src/pages/ReportPage.tsx` — 报告页面断言结果展示

### E2E 测试参考
- `e2e/playwright.config.ts` — Playwright 配置，超时设置，webServer 配置
- `e2e/tests/smoke.spec.ts` — 现有 E2E 测试模式（创建 → 执行 → 监控 → 报告）
- `e2e/tests/full-flow.spec.ts` — 完整流程测试模式
- `e2e/tests/data-method-execution.spec.ts` — 数据方法执行测试参考

### 前置阶段参考
- `.planning/phases/20-e2e-testing-manual-verification/20-CONTEXT.md` — Phase 20 E2E 模式
- `.planning/phases/24-frontend-assertion-ui/24-CONTEXT.md` — AssertionConfig 结构
- `.planning/phases/25-assertion-execution-engine/25-CONTEXT.md` — 断言执行、结果结构

### 类型定义
- `frontend/src/types/index.ts` — AssertionConfig 接口
- `backend/api/routes/runs.py` — RunResponse 结构

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `e2e/playwright.config.ts`:
  - 自动启动前后端服务（uvicorn + npm run dev）
  - 120 秒超时（AI 执行可能较慢）
  - Chromium 单浏览器配置
- `e2e/tests/smoke.spec.ts`:
  - 完整用户流程测试模式
  - 创建任务 → 执行 → 监控 → 查看报告
  - 使用 test.setTimeout() 处理长时间执行
- `e2e/tests/full-flow.spec.ts`:
  - 销售出库用例完整流程
  - 可直接复用并添加断言配置
- `backend/core/external_precondition_bridge.py`:
  - execute_assertion_method() 已实现
  - resolve_headers() 已实现

### Established Patterns
- **E2E 测试模式**: Playwright + 自动启动服务 + 长超时
- **验证模式**: 检查页面元素可见性、状态文本、结果卡片
- **失败处理**: 截图 + trace + video
- **环境配置**: 通过环境变量传递 ERP 配置

### Integration Points
- E2E 测试需要 ERP 环境变量: ERP_BASE_URL, ERP_USERNAME, ERP_PASSWORD
- 测试执行入口: `/api/runs` 端点
- 断言配置字段: `assertions: AssertionConfig[]`
- 报告查看: `/reports/{run_id}` 页面

### 需要新增的测试
1. 断言配置 E2E 测试 — 创建任务时配置断言
2. 断言执行 E2E 测试 — 执行并验证断言执行
3. 断言结果展示 E2E 测试 — 报告页面断言结果卡片验证

</code_context>

<specifics>
## Specific Ideas

- 断言结果卡片应显示通过/失败状态、断言方法名、字段级详情
- 失败断言用红色边框或背景标识
- E2E 测试应该验证报告页面中断言结果区域可见且内容正确
- 手动验证检查清单应覆盖 AssertionSelector Modal 的每个交互

</specifics>

<deferred>
## Deferred Ideas

- Context 变量引用验证（{{assertion_result_0.passed}}）— 后续需求
- 多断言混合结果测试 — 当前只测试单断言成功/失败
- 错误场景 E2E 测试（超时、无效参数）— Phase 27 单元测试
- Mock 数据支持 — v2 需求

</deferred>

---
*Phase: 26-e2e-testing*
*Context gathered: 2026-03-20*
