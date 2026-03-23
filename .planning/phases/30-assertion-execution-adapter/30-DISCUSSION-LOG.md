# Phase 30: 断言执行适配层 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in 30-CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-22
**Phase:** 30-assertion-execution-adapter
**Areas discussed:** 参数合并策略, now 转换逻辑, 响应结构统一, API 端点设计

---

## 参数合并策略

| Option | Description | Selected |
|--------|-------------|----------|
| 平级合并 | api_params 和 field_params 平级合并为 kwargs，传给断言方法 | ✓ |
| 分层合并 | 保持三层结构分离，按优先级处理 | |
| 默认值填充合并 | api_params 先合并默认值，再合并 field_params | |

**User's choice:** 平级合并（推荐）
**Notes:** 简单直接，符合现有模式

---

## "now" 转换逻辑

### 转换格式

| Option | Description | Selected |
|--------|-------------|----------|
| 标准格式 | 使用 BaseApi.get_formatted_datetime() 格式（YYYY-MM-DD HH:mm:ss） | ✓ |
| ISO 格式 | 使用 datetime.now().isoformat() | |
| 不转换 | 直接传 'now' 字符串给断言方法 | |

**User's choice:** 标准格式（推荐）
**Notes:** 与 webseleniumerp 一致

### 转换时机

| Option | Description | Selected |
|--------|-------------|----------|
| 调用前预处理 | 在调用断言方法前，遍历 field_params 转换所有 'now' 值 | ✓ |
| 断言方法内部 | 在断言方法内部处理（需修改 base_assert.py） | |

**User's choice:** 调用前预处理（推荐）
**Notes:** 保持适配层模式，不修改 base_assert.py

---

## 响应结构统一

| Option | Description | Selected |
|--------|-------------|----------|
| 统一为 fields/name | 字段名改为 'name'，整体改为 'fields' | ✓ |
| 保持 field_results/field | 保持现有结构，修改 ROADMAP.md | |
| 双格式兼容 | 同时返回两种格式，逐步迁移 | |

**User's choice:** 统一为 fields/name（推荐）
**Notes:** 符合 ROADMAP.md API Contract

---

## API 端点设计

| Option | Description | Selected |
|--------|-------------|----------|
| 修改现有端点 | 修改现有端点，向后兼容 | ✓ |
| 新建端点 | 新建 /execute-adapted 端点，保留原端点不变 | |

**User's choice:** 修改现有端点（推荐）
**Notes:** 避免端点冗余

### 向后兼容性

| Option | Description | Selected |
|--------|-------------|----------|
| 完全兼容 | 顶层 headers/data/params 继续工作，同时支持新结构 | ✓ |
| 不兼容 | 只支持新的三层结构 | |

**User's choice:** 完全兼容（推荐）
**Notes:** 前端可逐步迁移

---

## Claude's Discretion

以下决策由 Claude 自行决定：
- 时间字段容差范围（建议 ±1 分钟）
- API 参数验证逻辑
- 单元测试 mock 数据结构

---

## Deferred Ideas

- E2E 测试 — Phase 31
- 断言结果持久化 — 未来需求
- 并行断言执行 — 未来优化
