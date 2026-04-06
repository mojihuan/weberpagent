# Phase 60: 任务表单优化 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-02
**Phase:** 60-任务表单优化
**Areas discussed:** 清理范围, 旧数据兼容

---

## 清理范围

| Option | Description | Selected |
|--------|-------------|----------|
| 仅前端表单 | 只移除 TaskForm 中的 tab 和 textarea，后端保持不变 | |
| 前端 + 后端执行 | 前端移除 tab，后端停止执行，保留数据库字段和 SSE | |
| 全面清理 | 前端 + 后端执行 + SSE + 数据库字段全部移除 | ✓ |

**User's choice:** 全面清理
**Notes:** 用户选择了最干净的方案，彻底移除 api_assertions 相关代码

---

## 旧数据兼容

| Option | Description | Selected |
|--------|-------------|----------|
| 不兼容旧数据 | 旧报告 API 断言结果不再渲染，完全不留痕迹 | ✓ |
| 保留旧数据渲染 | 报告页保留对旧 API 断言结果的只读展示能力 | |

**User's choice:** 不兼容旧数据
**Notes:** 用户确认不需要向后兼容，旧数据可以忽略

---

## Claude's Discretion

- 清理后 TimelineItem 类型如何处理 api_assertion 部分
- 数据库 migration 方式
- 文件删除和修改的具体顺序

## Deferred Ideas

None — discussion stayed within phase scope
