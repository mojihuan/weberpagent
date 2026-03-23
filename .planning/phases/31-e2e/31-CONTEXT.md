# Phase 31: E2E 测试 - Context

**Gathered:** 2026-03-22
**Status:** Ready for planning

<domain>
## Phase Boundary

扩展 E2E 测试覆盖 v0.4.1 新增的三层参数结构（data/api_params/field_params）和 "now" 时间转换功能。通过端到端测试验证完整的断言配置 → 执行 → 结果展示流程。

**Scope:**
- 在现有 assertion-flow.spec.ts 中添加新测试用例
- 测试 field_params 配置功能
- 测试 "now" 时间转换功能
- 测试断言成功场景（三层参数）
- 使用真实 ERP 环境（与 Phase 26 一致）

**Out of Scope:**
- Mock ERP（使用真实 ERP，与 Phase 26 一致）
- 创建新测试文件（扩展现有文件）
- 单元测试（Phase 27 已完成）
- 断言失败场景（已有测试覆盖）

</domain>

<decisions>
## Implementation Decisions

### 测试环境策略
- **D-01:** 使用**真实 ERP 环境**（需要 ERP_BASE_URL 环境变量）
- **D-02:** 不实现 Mock ERP 模式（与 ROADMAP.md 原计划不同，改为真实 ERP）
- **D-03:** 环境变量缺失时跳过测试（test.skip），与 Phase 26 一致

### 测试文件组织
- **D-04:** **扩展现有 assertion-flow.spec.ts**，不创建新文件
- **D-05:** 新增 3 个测试用例覆盖 v0.4.1 功能
- **D-06:** 复用现有测试模式（创建任务 → 配置断言 → 执行 → 查看报告）

### 测试场景
- **D-07:** **field_params 配置测试** — 在 UI 配置 field_params（如 statusStr='已完成'），验证传递正确
- **D-08:** **"now" 时间转换测试** — 配置时间字段为 "now"，验证断言结果通过
- **D-09:** **断言成功场景** — 验证所有字段通过，结果为 passed: true

### 验证方式
- **D-10:** **通过 UI 验证结果**（报告页面），不直接检查 API 响应
- **D-11:** 验证断言结果卡片显示绿色（bg-green-50 border-green-200）
- **D-12:** 验证字段级详情正确展示（name/expected/actual/passed）

### Claude's Discretion
- **D-13:** 具体选择哪个断言方法进行测试
- **D-14:** 测试用例的具体实现细节
- **D-15:** 超时设置（建议 5 分钟，与现有测试一致）
- **D-16:** 失败诊断信息格式

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心实现参考
- `.planning/ROADMAP.md` — Phase 31 定义、API Contract（Request Body/Response 结构）
- `.planning/phases/26-e2e-testing/26-CONTEXT.md` — Phase 26 E2E 测试模式（真实 ERP、超时设置）
- `.planning/phases/30-assertion-execution-adapter/30-CONTEXT.md` — Phase 30 决策（三层参数结构、"now" 转换）

### 现有 E2E 测试参考
- `e2e/tests/assertion-flow.spec.ts` — 现有断言测试（5 个测试用例）
- `e2e/playwright.config.ts` — Playwright 配置，超时设置
- `e2e/tests/smoke.spec.ts` — 基础测试模式

### 前端组件参考
- `frontend/src/components/TaskModal/AssertionSelector.tsx` — 断言选择器组件（含 FieldParamsEditor）
- `frontend/src/components/TaskModal/FieldParamsEditor.tsx` — 字段参数配置组件
- `frontend/src/pages/ReportPage.tsx` — 报告页面断言结果展示

### API 参考
- `backend/api/routes/external_assertions.py` — POST /execute 端点
- `backend/core/external_precondition_bridge.py`:
  - `execute_assertion_method()` — 三层参数处理
  - `_convert_now_values()` — "now" 转换逻辑
  - `_parse_assertion_error()` — 响应结构

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `e2e/tests/assertion-flow.spec.ts`:
  - 5 个现有测试用例（单断言成功/失败、多断言、Modal 工作流、参数保留）
  - 测试模式：创建任务 → 配置断言 → 执行 → 查看报告
  - 5 分钟超时（300000ms）
  - ERP 环境变量检测（test.skip）
- `e2e/playwright.config.ts`:
  - 自动启动前后端服务
  - Chromium 单浏览器
  - trace/screenshot/video 失败诊断
- `frontend/src/components/TaskModal/FieldParamsEditor.tsx`:
  - 字段搜索、分组浏览
  - "now" 快捷按钮
  - 添加/删除字段配置

### Established Patterns
- **E2E 测试模式**: Playwright + 真实 ERP + 长超时（5 分钟）
- **断言配置**: 切换到 "业务断言" Tab → 点击 "添加断言" → 选择方法 → 配置参数
- **验证模式**: 检查报告页面元素（bg-green-50/bg-red-50 状态样式）
- **失败处理**: 截图 + trace + video

### Integration Points
- E2E 测试需要 ERP 环境变量: ERP_BASE_URL, ERP_USERNAME, ERP_PASSWORD
- 断言配置字段: `assertions: AssertionConfig[]`（含 field_params）
- 报告查看: `/reports/{run_id}` 页面
- 断言结果 UI: 断言结果卡片（绿色/红色背景）

### 需要新增的测试用例
| 测试用例 | 目的 | 验证点 |
|----------|------|--------|
| `field_params configuration` | 验证字段参数配置 | 配置 field_params → 执行 → 报告展示正确 |
| `now time conversion` | 验证 "now" 转换 | 配置时间字段为 "now" → 断言通过 |
| `three-layer params success` | 验证三层参数成功场景 | 所有字段通过 → 绿色卡片展示 |

</code_context>

<specifics>
## Specific Ideas

- field_params 测试应配置 2-3 个字段（包括时间字段和非时间字段）
- "now" 测试使用时间字段（如 createTime）配置为 "now"
- 断言成功测试验证所有字段都显示绿色勾号
- 测试超时与现有测试一致（5 分钟）
- 复用现有断言方法（如 attachment_inventory_list_assert）

</specifics>

<deferred>
## Deferred Ideas

- Mock ERP 模式 — 使用真实 ERP 替代
- 断言失败场景测试 — 已有测试覆盖
- 并行断言执行测试 — 已有 multiple assertions 测试
- API 响应验证 — 仅通过 UI 验证

</deferred>

---
*Phase: 31-e2e*
*Context gathered: 2026-03-22*
