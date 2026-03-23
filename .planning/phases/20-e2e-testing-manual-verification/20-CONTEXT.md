# Phase 20: E2E Testing + Manual Verification - Context

**Gathered:** 2026-03-19
**Status:** Ready for planning

<domain>
## Phase Boundary

验证 v0.3.1 数据获取方法集成的端到端流程可用。通过 E2E 自动化测试和手动验证，确保：
1. DataMethodSelector 组件选择与配置功能正常
2. 数据获取方法执行返回预期数据
3. 变量替换（`{{变量名}}`）在测试步骤和 API 断言中正确工作
4. 完整测试用例端到端执行成功

**Scope:**
- 使用真实 ERP 环境进行 E2E 测试
- 复用现有销售出库用例进行验证
- 测试正常流程（错误场景留给 Phase 21 单元测试）
- 创建详细的手动验证检查清单

**Out of Scope:**
- 单元测试覆盖（Phase 21）
- Bug 修复（Phase 22）
- 新功能开发
- 性能测试

</domain>

<decisions>
## Implementation Decisions

### E2E 测试环境
- **使用真实 ERP 环境**: 必须配置 ERP_BASE_URL、ERP_USERNAME、ERP_PASSWORD
- **配置缺失处理**: 直接失败，强制要求 ERP 配置
- **测试隔离**: 不创建专用测试数据，复用现有用例

### E2E 测试范围
- **正常流程优先**: 只测试正常流程，错误场景留给单元测试
- **复用现有用例**: 使用销售出库用例作为测试场景
- **变量替换验证**: 检查报告页面中的实际值是否与获取的数据匹配

### E2E 测试失败处理
- **保存详细诊断信息**: 截图、网络请求、控制台日志
- **Playwright trace**: on-first-retry 模式
- **失败截图**: only-on-failure 模式
- **视频保留**: retain-on-failure 模式

### 手动验证
- **执行时机**: E2E 测试全部通过后执行
- **验证场景**: 完整销售出库用例（前置条件 → 数据获取 → 变量替换 → AI 执行）
- **检查清单详细度**: 每个UI元素、交互、状态变化都有明确的验证点
- **环境要求**: 真实 ERP 环境

### 测试结果记录
- **格式**: 创建 VERIFICATION.md 记录验证结果
- **内容**: 测试通过情况、发现的问题、验证截图

### Claude's Discretion
- E2E 测试用例的具体实现细节
- 手动验证检查清单的具体条目
- VERIFICATION.md 的具体格式
- 失败诊断信息的具体内容

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心实现参考
- `backend/core/precondition_service.py` — ContextWrapper 类、get_data() 方法、变量替换逻辑
- `backend/core/external_precondition_bridge.py` — execute_data_method API
- `backend/api/routes/runs.py` — 测试执行入口，变量替换调用点
- `frontend/src/components/TaskModal/DataMethodSelector.tsx` — 4 步向导组件
- `frontend/src/components/TaskModal/TaskForm.tsx` — 代码生成逻辑

### E2E 测试参考
- `e2e/playwright.config.ts` — Playwright 配置，超时设置，webServer 配置
- `e2e/tests/smoke.spec.ts` — 现有 E2E 测试模式（创建 → 执行 → 监控 → 报告）
- `e2e/tests/task-flow.spec.ts` — UI 验证测试模式

### 前置阶段参考
- `.planning/phases/17-后端数据获取桥接/17-CONTEXT.md` — execute_data_method API 定义
- `.planning/phases/18-前端数据选择器/18-CONTEXT.md` — DataMethodConfig 类型定义
- `.planning/phases/19-集成与变量传递/19-CONTEXT.md` — ContextWrapper 实现，变量替换逻辑

### 类型定义
- `frontend/src/types/index.ts` — DataMethodConfig 接口

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
- `backend/core/precondition_service.py`:
  - ContextWrapper 类已实现
  - get_data() 方法可用
  - substitute_variables() 静态方法可用

### Established Patterns
- **E2E 测试模式**: Playwright + 自动启动服务 + 长超时
- **验证模式**: 检查页面元素可见性、URL 变化、状态文本
- **失败处理**: 截图 + trace + video
- **环境配置**: 通过环境变量传递 ERP 配置

### Integration Points
- E2E 测试需要 ERP 环境变量: ERP_BASE_URL, ERP_USERNAME, ERP_PASSWORD
- 测试执行入口: `/api/runs` 端点
- 变量替换调用点: `runs.py` 第 124-129 行
- 报告查看: `/reports/{run_id}` 页面

### 需要新增的测试
1. DataMethodSelector 选择与配置测试
2. 数据获取执行与返回验证
3. 变量替换集成测试（报告页面验证）
4. 完整用例执行流程测试

</code_context>

<specifics>
## Specific Ideas

- E2E 测试应该验证报告页面中显示的变量值与 ContextWrapper.get_data() 返回的数据一致
- 手动验证检查清单应覆盖 DataMethodSelector 4 步向导的每一步
- 使用现有的销售出库用例作为测试场景，验证完整流程

</specifics>

<deferred>
## Deferred Ideas

- Mock 数据支持（可选回退）— v2 需求
- 错误场景 E2E 测试 — Phase 21 单元测试
- 性能测试 — 后续版本
- 多浏览器兼容性测试 — 后续版本

</deferred>

---
*Phase: 20-e2e-testing-manual-verification*
*Context gathered: 2026-03-19*
