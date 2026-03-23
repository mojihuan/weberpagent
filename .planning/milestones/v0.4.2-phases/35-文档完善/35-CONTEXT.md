# Phase 35: 文档完善 - Context

**Gathered:** 2026-03-23
**Status:** Ready for planning

<domain>
## Phase Boundary

为断言系统编写用户文档，帮助 QA 测试人员和开发人员理解如何配置和使用三层参数断言功能。

**Scope:**
- 创建断言系统使用指南文档
- 记录三层参数（api_params/field_params/params）的配置方式
- 提供销售出库断言示例
- 记录常见问题和解决方案

**Out of Scope:**
- 修改现有代码
- 新功能开发
- 自动化测试

</domain>

<decisions>
## Implementation Decisions

### 文档目标受众
- **D-01:** 受众 = **两者兼顾（QA + 开发人员）**
  - QA 部分：简单易懂的步骤说明
  - 开发部分：API 参考和数据结构说明

### 文档位置和格式
- **D-02:** 文档位置 = **`docs/断言系统使用指南.md`**
  - 与现有 `docs/测试步骤.md` 并列
- **D-03:** 文档形式 = **纯 Markdown**
  - 文字说明 + 代码块示例
  - 暂不包含截图

### 内容结构
- **D-04:** 主要章节 = **三个核心部分**
  1. 完整工作流程（从前端配置到执行到查看结果）
  2. 三层参数详解（api_params/field_params/params）
  3. 报告解读（如何理解断言结果）
- **D-05:** 开发者内容 = **基础 API 参考和数据结构**
  - `execute_assertion_method()` 函数签名
  - 断言结果在 context 中的存储格式

### 示例和讲解风格
- **D-06:** 讲解风格 = **示例驱动**
  - 用具体用例演示每个参数的作用
- **D-07:** 示例场景 = **销售出库断言**
  - 使用 `sell_sale_item_list_assert` 作为主要示例
  - 与 `docs/测试步骤.md` 保持一致，便于理解

### FAQ 部分
- **D-08:** FAQ 范围 = **预防性 FAQ**
  - 包含可能遇到的常见错误和解决方案
- **D-09:** FAQ 深度 = **精简版（5-8 个问题）**
  - 只涵盖最常见的问题
  - 简洁解答

### Claude's Discretion
- 具体文档的排版和措辞
- FAQ 问题的选择和解答方式
- 代码示例的详细程度

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心实现参考
- `.planning/ROADMAP.md` — Phase 35 定义、Success Criteria (DOC-01~02)
- `.planning/REQUIREMENTS.md` — DOC-01/02 需求定义

### 前置阶段参考
- `.planning/phases/33-人工验证断言执行/33-CONTEXT.md` — Phase 33 验证流程
- `.planning/phases/30-assertion-execution-adapter/30-CONTEXT.md` — Phase 30 决策（三层参数结构、"now" 转换）

### 现有代码参考
- `backend/core/external_precondition_bridge.py`:
  - `execute_all_assertions()` — 执行所有断言，提取三层参数
  - `execute_assertion_method()` — 执行单个断言方法，处理 "now" 转换
- `frontend/src/components/TaskModal/FieldParamsEditor.tsx` — 字段参数配置 UI
- `frontend/src/pages/ReportDetail.tsx` — 报告详情页，显示断言结果

### 现有文档参考
- `docs/测试步骤.md` — 销售出库测试用例，断言配置示例
- `docs/README.md` — 现有文档结构

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

</code_context>

<specifics>
## Specific Ideas

- 文档以销售出库断言为例，展示完整配置流程
- 三层参数用表格形式对比说明用途
- FAQ 包含：时间参数配置、字段找不到、断言失败排查等常见问题
- 开发者部分简要说明函数签名和数据结构

</specifics>

<deferred>
## Deferred Ideas

- 含截图的详细教程 — 后续版本考虑
- 前端应用内嵌帮助文档 — 未来需求
- 完整故障排查指南 — 后续版本考虑
- 多场景示例（库存、采购等） — 后续版本考虑

</deferred>

---
*Phase: 35-文档完善*
*Context gathered: 2026-03-23*
