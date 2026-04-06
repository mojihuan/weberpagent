# Phase 59: 报告步骤展示 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-02
**Phase:** 59-report-steps
**Areas discussed:** 步骤卡片外观, 现有独立区块处理, 交错排序数据来源, 合并排序责任方, 汇总统计区域

---

## 步骤卡片外观

| Option | Description | Selected |
|--------|-------------|----------|
| 复用 StepItem 卡片风格 | 前置条件/断言用与 StepItem 相同的可展开卡片样式，内容区域不同，颜色/图标区分 | ✓ |
| 更紧凑的行内样式 | 前置条件/断言用更紧凑的行内样式，不展开 | |
| 复用时间线样式 | 复用 Phase 58 的时间线样式（带连接线） | |

**User's choice:** 复用 StepItem 卡片风格
**Notes:** 统一视觉风格，展开内容因类型不同（前置条件显示代码+变量，断言显示名称+结果）

---

## 现有独立区块处理

| Option | Description | Selected |
|--------|-------------|----------|
| 移除独立区块 | 移除 PreconditionSection、AssertionResults、ApiAssertionResults 三个独立区块 | ✓ |
| 保留断言汇总摘要 | 保留断言汇总区块（通过率统计），前置条件详情只出现在步骤列表 | |
| 全部保留 | 保留所有三个独立区块作为概览，信息重复 | |

**User's choice:** 移除独立区块
**Notes:** 页面更简洁，无重复信息

---

## 交错排序数据来源

| Option | Description | Selected |
|--------|-------------|----------|
| 全局序号 | 后端存储时为每个步骤/前置条件/断言分配全局递增的 sequence_number | ✓ |
| 时间戳排序 | 用 created_at 时间戳排序，实现简单但精度可能不够 | |
| 固定分组顺序 | 按固定顺序展示：前置条件→UI步骤→断言，简单但不完全交错 | |

**User's choice:** 全局序号
**Notes:** 前置条件结果当前未持久化到 DB，需要先解决存储问题。这是实现的前提阻塞项。

---

## 合并排序责任方

| Option | Description | Selected |
|--------|-------------|----------|
| 后端返回统一列表 | 报告 API 返回新的 ReportTimelineItem[] 联合类型 | ✓ |
| 前端合并排序 | 后端只返回全局序号字段，前端仍接收三个数组自己合并 | |

**User's choice:** 后端返回统一列表

---

## 汇总统计区域

| Option | Description | Selected |
|--------|-------------|----------|
| 保留摘要统计 | 保留顶部的汇总统计（步骤数、成功率、耗时等卡片） | ✓ |
| 移除所有汇总 | 页面只有步骤列表，没有顶部汇总信息 | |

**User's choice:** 保留摘要统计

---

## Claude's Discretion

- PreconditionResult 数据库表的具体字段设计
- 全局 sequence_number 的分配机制
- ReportTimelineItem 的具体类型定义
- 卡片展开/折叠的默认行为
- 具体图标和 Tailwind 颜色值

## Deferred Ideas

None — discussion stayed within phase scope
