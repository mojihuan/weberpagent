# Phase 33: 人工验证断言执行 - Context

**Gathered:** 2026-03-22
**Status:** Ready for planning

<domain>
## Phase Boundary

人工执行销售出库测试用例，验证断言系统能正确执行 `sell_sale_item_list_assert`。此阶段专注于验证，不包含新功能开发。

**Scope:**
- 通过 UI 完整验证断言执行流程
- 验证三层参数传递正确（salesOrder、articlesStateStr、saleTime）
- 验证 "now" 时间转换功能
- 验证断言结果显示在报告中
- 记录发现的问题

**Out of Scope:**
- 新功能开发（仅验证现有功能）
- 自动化测试（人工执行）
- 修改断言方法本身

</domain>

<decisions>
## Implementation Decisions

### 验证执行流程
- **D-01:** 验证方式 = **完整 UI 验证**
  - 在前端创建任务
  - 配置断言参数（salesOrder, articlesStateStr, saleTime）
  - 执行测试
  - 查看 ReportDetail 页面结果

### 测试数据准备
- **D-02:** 断言参数 = **使用默认参数**
  - salesOrder='SA'
  - articlesStateStr='已销售'
  - saleTime='now'
- **D-03:** 数据准备 = **需要先创建数据**
  - 需要先执行完整测试流程创建销售出库记录
  - 然后执行断言验证

### 成功/失败判定
- **D-04:** 验证通过标准 = **全部四项**
  1. 断言被正确调用（返回结构包含 success/passed/fields）
  2. 'now' 时间转换正确（显示为实际时间字符串）
  3. 结果显示在报告中（断言结果卡片）
  4. 字段级结果清晰（name/expected/actual/passed）
- **D-05:** 失败处理 = **需要分析原因**
  - 如果 passed=false，需要分析是参数错误还是系统 bug

### 问题记录方式
- **D-06:** Bug 记录位置 = **ISSUES.md 文件**
  - 在 `.planning/phases/33-人工验证断言执行/` 目录下创建
- **D-07:** Bug 记录内容 = **四项**
  - 问题描述
  - 复现步骤
  - 错误信息/证据
  - 优先级 (P0-P3)

### Claude's Discretion
- 具体验证用例的选择
- 测试执行的超时设置
- 报告截图的命名规则

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心实现参考
- `.planning/ROADMAP.md` — Phase 33 定义、Success Criteria
- `.planning/REQUIREMENTS.md` — ASSERT-01~04 需求定义

### 前置阶段参考
- `.planning/phases/30-assertion-execution-adapter/30-CONTEXT.md` — Phase 30 决策（三层参数结构、"now" 转换）
- `.planning/phases/32-three-layer-params-gap-closure/32-VERIFICATION.md` — Phase 32 验证（execute_all_assertions 正确传递参数）

### 现有代码参考
- `backend/core/external_precondition_bridge.py`:
  - `execute_all_assertions()` — 执行所有断言，提取三层参数
  - `execute_assertion_method()` — 执行单个断言方法，处理 "now" 转换
- `frontend/src/components/TaskModal/FieldParamsEditor.tsx` — 字段参数配置 UI
- `frontend/src/pages/ReportDetail.tsx` — 报告详情页，显示断言结果

### 测试用例参考
- `docs/测试步骤.md` — 销售出库测试用例，包含断言配置示例

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `execute_all_assertions()` — 已正确提取 api_params, field_params, params
- `execute_assertion_method()` — 已支持三层参数，已实现 "now" 转换
- `_parse_assertion_error()` — 已解析字段级结果为 `fields/name` 格式
- `FieldParamsEditor` — 前端组件支持字段搜索、分组、配置
- `ReportDetail.tsx` — 报告页面已显示 `assertion_results`

### Established Patterns
- **三层参数结构**: api_params + field_params + params
- **"now" 转换**: 使用 `get_formatted_datetime()` 转换为 `YYYY-MM-DD HH:mm:ss`
- **断言执行模式**: 非 fail-fast，收集所有结果
- **响应结构**: `{ success, passed, fields: [{ name, expected, actual, passed }] }`

### Integration Points
- 前端任务配置 → 后端 `/api/tasks` → AI 执行 → 断言调用 → 结果存储 → 报告展示
- 断言配置存储在 `assertions: AssertionConfig[]` 中
- 断言结果存储在 `context.assertion_results` 中

### 验证流程
1. 启动后端服务: `uv run uvicorn backend.api.main:app --reload --port 8080`
2. 启动前端服务: `cd frontend && npm run dev`
3. 创建任务 → 配置前置条件 → 配置断言参数
4. 执行测试 → 等待完成 → 查看报告

</code_context>

<specifics>
## Specific Ideas

- 先执行一次完整测试流程创建销售出库记录
- 然后单独验证断言执行（或断点调试）
- 截图记录每个验证步骤
- 如果发现 bug，详细记录到 ISSUES.md

</specifics>

<deferred>
## Deferred Ideas

- 自动化 E2E 测试 — Phase 34 或后续版本
- 断言参数智能推荐 — 未来需求
- 断言结果对比分析 — 未来需求

</deferred>

---
*Phase: 33-人工验证断言执行*
*Context gathered: 2026-03-22*
