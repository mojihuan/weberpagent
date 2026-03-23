# Phase 33: 人工验证断言执行 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-22
**Phase:** 33-人工验证断言执行
**Areas discussed:** 验证执行流程, 测试数据准备, 成功/失败判定, 问题记录方式

---

## 验证执行流程

| Option | Description | Selected |
|--------|-------------|----------|
| 完整 UI 验证 | 在前端创建任务 → 配置断言参数 → 执行测试 → 查看 ReportDetail 页面结果 | ✓ |
| E2E 自动化验证 | 使用 Playwright E2E 测试自动执行验证，生成测试报告 | |
| API 直接调用 | 使用 curl/Postman 直接调用 API 端点，验证后端响应 | |

**User's choice:** 完整 UI 验证 (推荐)
**Notes:** 人工验证阶段，通过完整 UI 流程验证端到端功能

---

## 测试数据准备

### 断言参数

| Option | Description | Selected |
|--------|-------------|----------|
| 使用默认参数 | 使用 docs/测试步骤.md 中的默认值 (salesOrder='SA', articlesStateStr='已销售', saleTime='now') | ✓ |
| 根据实际数据调整 | 需要先检查 ERP 中已有的销售出库记录，根据实际数据配置断言参数 | |
| 创建新数据后验证 | 先执行前置条件创建新记录，然后对新记录进行断言 | |

**User's choice:** 使用默认参数 (推荐)

### 数据依赖

| Option | Description | Selected |
|--------|-------------|----------|
| 数据已存在 | ERP 中已有销售出库记录，可以直接验证断言 | |
| 需要创建数据 | 需要先执行完整测试流程创建销售出库记录，再执行断言 | ✓ |
| 不确定，先试 | 先尝试断言，失败后再创建数据 | |

**User's choice:** 需要创建数据
**Notes:** 验证流程需要包含数据创建步骤

---

## 成功/失败判定

### 验证通过标准 (多选)

| Option | Description | Selected |
|--------|-------------|----------|
| 断言被正确调用 | 断言被调用，返回结构包含 success/passed/fields 字段 | ✓ |
| 'now' 时间转换正确 | saleTime='now' 在结果中显示为实际时间字符串（如 '2026-03-22 10:30:00'） | ✓ |
| 结果显示在报告中 | 断言结果卡片显示在 ReportDetail 页面（绿色或红色） | ✓ |
| 字段级结果清晰 | 每个字段显示 name/expected/actual/passed 四个属性 | ✓ |

**User's choice:** 全选（全部四项）

### 失败处理

| Option | Description | Selected |
|--------|-------------|----------|
| 记录为正常结果 | 断言失败是因为数据不匹配，这是正常的测试结果，不是 bug | |
| 需要分析原因 | 如果断言失败，需要分析是参数错误还是系统 bug | ✓ |
| 调整参数重试 | 尝试调整参数值后重新执行，直到断言通过 | |

**User's choice:** 需要分析原因

---

## 问题记录方式

### Bug 记录位置

| Option | Description | Selected |
|--------|-------------|----------|
| ISSUES.md 文件 | 在 .planning/phases/33-*/ 目录下创建 ISSUES.md 文件记录 | ✓ |
| 更新 REQUIREMENTS.md | 在 REQUIREMENTS.md 中添加新需求项 | |
| 留到 Phase 34 | 直接在 Phase 34 的计划中记录 | |

**User's choice:** ISSUES.md 文件 (推荐)

### Bug 记录内容 (多选)

| Option | Description | Selected |
|--------|-------------|----------|
| 问题描述 | 简要描述问题现象 | ✓ |
| 复现步骤 | 复现步骤、期望结果、实际结果 | ✓ |
| 错误信息/证据 | 相关的 API 响应、日志、截图 | ✓ |
| 优先级 | P0 (阻塞), P1 (严重), P2 (一般), P3 (轻微) | ✓ |

**User's choice:** 全选（四项）

---

## Claude's Discretion

- 具体验证用例的选择
- 测试执行的超时设置
- 报告截图的命名规则

## Deferred Ideas

- 自动化 E2E 测试 — Phase 34 或后续版本
- 断言参数智能推荐 — 未来需求
- 断言结果对比分析 — 未来需求

---
*Discussion logged: 2026-03-22*
