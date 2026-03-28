# Phase 50: AgentService 集成 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-28
**Phase:** 50-agentservice
**Areas discussed:** step_callback 整合方式, Monitor 日志记录

---

## step_callback 整合方式

| Option | Description | Selected |
|--------|-------------|----------|
| 现有 callback + 检测器调用 | 在现有 step_callback 中直接调用 agent._stall_detector.check() 和 agent._task_tracker.check_progress() | ✓ |
| MonitoredAgent callback 为主 | 使用 create_step_callback() 替换现有 callback，将日志逻辑移入 | |
| 组合 wrapper callback | 创建组合回调函数，内部调用两个逻辑块 | |

**User's choice:** 现有 callback + 检测器调用（推荐）
**Notes:** 保留所有现有日志逻辑不变，在末尾添加检测器调用。MonitoredAgent.create_step_callback() 不再使用。

---

## Monitor 日志记录

| Option | Description | Selected |
|--------|-------------|----------|
| run_logger 传入 MonitoredAgent | 将 run_logger 通过构造参数传入 MonitoredAgent，在 _prepare_context() 和 _execute_actions() 中记录 category="monitor" | ✓ |
| Python logging 即可 | 检测器只通过 Python logging 记录，不传 run_logger | |

**User's choice:** run_logger 传入 MonitoredAgent（推荐）
**Notes:** 满足 INTEG-04 要求，干预消息通过结构化日志记录（category="monitor"）。

---

## Claude's Discretion

- 检测器调用的具体位置（step_callback 中哪个时机最优）
- run_logger 在 MonitoredAgent 中的传递方式
- 单元测试的具体 mock 设计

## Deferred Ideas

None — discussion stayed within phase scope.
