# Phase 56: E2E 综合验证 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-31
**Phase:** 56-e2e
**Areas discussed:** 测试用例定义, 执行方式与环境, 通过标准与报告, 范围调整

---

## 测试用例定义

| Option | Description | Selected |
|--------|-------------|----------|
| 全部 9 个用例 | 包含 Phase 52-54 全部 9 个测试用例，包括未独立验证的 Escape 和 Control+a | ✓ |
| 只跑 8 个 | 去掉 1 个未独立验证场景 | |
| 只跑已验证的 7 个 | 不再验证未独立验证的键盘场景 | |

**User's choice:** 全部 9 个用例
**Notes:** 实际测试用例数为 9 个（非 Roadmap 中的 8 个），加上 2 个断言用例共 11 个

---

## 执行方式

| Option | Description | Selected |
|--------|-------------|----------|
| 平台 UI 手动执行 | 通过平台 UI 逐个创建/执行，人工观察过程，与 Phase 51 模式一致 | ✓ |
| API 自动执行 | 调用 API 批量执行，自动记录结果 | |
| 服务器上执行 | 在 121.40.191.49 上执行 | |

**User's choice:** 平台 UI 手动执行

---

## 执行环境

| Option | Description | Selected |
|--------|-------------|----------|
| 服务器 (121.40.191.49) | 与部署环境一致 | |
| 本地开发机 | 方便调试和查看日志 | ✓ |

**User's choice:** 本地开发机

---

## 通过标准

| Option | Description | Selected |
|--------|-------------|----------|
| 逐场景判定 | 每个用例独立判定通过/失败，可以部分通过 | ✓ |
| 全通过才算成功 | 9 个全部通过才算成功 | |

**User's choice:** 逐场景判定

---

## 报告格式

| Option | Description | Selected |
|--------|-------------|----------|
| 沿用现有模板 | 复用现有验证结果文档格式 | |
| 新建综合报告 | 生成一个新的综合验证报告，汇总 11 个场景结果 | ✓ |

**User's choice:** 新建综合报告

---

## 失败处理

| Option | Description | Selected |
|--------|-------------|----------|
| 记录+分析，不修复 | 记录失败原因，分析是否 prompt/环境/数据问题，保持验证纯洁性 | ✓ |
| 修复后重跑 | 失败时尝试调整 prompt 并重跑 | |

**User's choice:** 记录+分析，不修复

---

## 范围调整（Phase 55 跳过）

| Option | Description | Selected |
|--------|-------------|----------|
| 只验证 Phase 52-54 | 去掉断言与缓存验证，与 Phase 55 跳过决策一致 | |
| 包含断言验证 | 额外添加 AST-01/02 断言场景验证 | ✓ |

**User's choice:** 包含断言验证
**Notes:** 即使 Phase 55 跳过，也在 E2E 中验证现有断言功能是否正常工作

---

## 断言测试步骤文档

| Option | Description | Selected |
|--------|-------------|----------|
| 新建断言测试步骤文档 | 在 docs/test-steps/ 下新建断言测试步骤文档 | ✓ |
| 嵌入综合报告中 | 断言场景嵌入综合验证报告 | |

**User's choice:** 新建断言测试步骤文档

---

## Claude's Discretion

- AST-01/02 测试步骤文档的具体内容
- 综合验证报告的具体格式
- 各用例执行的具体 ERP 操作流程
- 失败原因分析的具体深度

## Deferred Ideas

- CAC-01/02 缓存断言功能 — 推迟到有实际需求时实现
- 自动化回归测试框架 — 当前手动执行满足需求
