# Phase 39: 循环干预优化 (基础) - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-24
**Phase:** 39-loop-intervention-basics
**Areas discussed:** 干预策略, 诊断日志内容, 报告展示方式, 重试次数

---

## 干预策略

| Option | Description | Selected |
|--------|-------------|----------|
| 跳过并继续 | 直接跳过当前困难步骤，让 Agent 继续执行后续步骤 | |
| 注入提示后重试 | 向 LLM 注入提示让它尝试不同方法 | ✓ |
| 标记失败+继续 | 记录当前步骤失败但不中断，类似 try-catch | |

**User's choice:** 注入提示后重试
**Notes:** 通过 step callback 检测循环并返回提示信息

---

## 提示注入方式

| Option | Description | Selected |
|--------|-------------|----------|
| step callback 返回提示 | 通过 register_new_step_callback 检测到循环时返回提示 | ✓ |
| 扩展系统消息 | 通过 extend_system_message 添加循环检测相关的系统提示 | |
| 添加自定义 action | 通过 Controller 添加一个特殊的 skip_loop_action | |

**User's choice:** step callback 返回提示
**Notes:** 利用现有的回调机制实现

---

## 诊断日志内容

| Option | Description | Selected |
|--------|-------------|----------|
| 循环状态值 | stagnation 值、max_repetition_count 等 | ✓ |
| 最近动作序列 | 最近 N 次动作的类型和参数 | ✓ |
| 页面状态快照 | URL、标题、DOM hash、可点击元素数量 | ✓ |
| 全部记录 | 包含上述所有信息 | ✓ |

**User's choice:** 全部记录
**Notes:** 完整的诊断信息有助于后续分析和优化

---

## 报告展示方式

| Option | Description | Selected |
|--------|-------------|----------|
| 添加字段存储 | 在 Step 表中添加 loop_intervention 字段（需要迁移） | ✓ |
| 使用特殊状态标记 | 使用特殊的 status 值如 'loop_intervention' | |
| 仅日志记录 | 只在后端日志中记录，不在报告中展示 | |

**User's choice:** 添加字段存储
**Notes:** JSON 类型字段存储完整诊断信息

---

## 重试次数

| Option | Description | Selected |
|--------|-------------|----------|
| 1 次 | 注入提示后只给 Agent 一次机会 | |
| 2 次 | 注入提示后给 Agent 两次机会尝试不同方法 | ✓ |
| 不限制 | 一直重试直到成功或达到 max_steps | |

**User's choice:** 2 次
**Notes:** 平衡重试机会和执行效率

---

## Claude's Discretion

None — all decisions were explicitly made by user.

## Deferred Ideas

None — discussion stayed within phase scope.
