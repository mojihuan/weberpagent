# Phase 69: 服务集成与 Prompt 规则 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-07
**Phase:** 69-prompt
**Areas discussed:** step_callback 集成方式, Section 9 Prompt 规则内容, 集成测试策略

---

## step_callback 集成方式

### 调用顺序

| Option | Description | Selected |
|--------|-------------|----------|
| 检测后再写入 | 先 detect_failure_mode() 检测失败，有结果则 update_failure_tracker() 写入 | ✓ |
| 复用 stall_detector 结果 | 从 check() 提取失败模式，不额外调用 detect_failure_mode() | |
| Claude's Discretion | 来决定 | |

**User's choice:** 检测后再写入
**Notes:** 逻辑清晰：检测→写入→下游 dom_patch 读取。避免无谓写入。

### dom_hash 存储

| Option | Description | Selected |
|--------|-------------|----------|
| 闭包变量存储 | step_callback 用闭包变量存上一步 dom_hash | ✓ |
| StallDetector 内部管理 | StallDetector 维护 dom_hash_history | |
| Claude's Discretion | 来决定 | |

**User's choice:** 闭包变量存储
**Notes:** 简单直接，参考 stall_detector._history 的模式。

### 调用条件

| Option | Description | Selected |
|--------|-------------|----------|
| 仅失败时调用 | evaluation 包含失败关键词时才调用 | ✓ |
| 每步都调用 | 所有 step 都调用 | |
| Claude's Discretion | 来决定 | |

**User's choice:** 仅失败时调用
**Notes:** 避免成功 step 的无谓计算。

### 修改范围

| Option | Description | Selected |
|--------|-------------|----------|
| 只改 agent_service.py | 不碰 monitored_agent.py 死代码 | ✓ |
| 两个都更新 | 保持一致性 | |
| Claude's Discretion | 来决定 | |

**User's choice:** 只改 agent_service.py
**Notes:** monitored_agent.py 的 create_step_callback 当前未使用，减少变更范围。

---

## Section 9 Prompt 规则内容

### 规则风格

| Option | Description | Selected |
|--------|-------------|----------|
| 简洁操作指令 | 每组 2-4 行，"看到 X → 做 Y" 格式 | ✓ |
| 详细指导 | 每组 5-8 行，含解释和背景 | |
| Claude's Discretion | 来决定 | |

**User's choice:** 简洁操作指令
**Notes:** 与现有 Section 9 风格一致，Prompt 空间有限。

### 规则顺序

| Option | Description | Selected |
|--------|-------------|----------|
| 定位→操作→异常 | 行标识→反重复→策略优先级→失败恢复 | ✓ |
| 异常优先 | 失败恢复→反重复→策略优先级→行标识 | |
| Claude's Discretion | 来决定 | |

**User's choice:** 定位→操作→异常
**Notes:** 定位→操作→异常的逻辑链，Agent 先学会定位再操作。

### 规则范围

| Option | Description | Selected |
|--------|-------------|----------|
| 只追加新规则 | 不修改现有 Section 9 内容 | ✓ |
| 追加+修改现有 | 使新旧规则更协调 | |
| Claude's Discretion | 来决定 | |

**User's choice:** 只追加新规则
**Notes:** 现有内容已验证有效，修改可能引入回归。

---

## 集成测试策略

### 测试方式

| Option | Description | Selected |
|--------|-------------|----------|
| Mock 单元测试 | mock step_callback 输入，验证调用链路和数据正确性 | ✓ |
| Mock + 集成测试 | mock + 完整链路集成测试 | |
| E2E 测试 | 端到端 ERP 表格填写测试 | |
| Claude's Discretion | 来决定 | |

**User's choice:** Mock 单元测试
**Notes:** 快速可重复，覆盖核心集成逻辑。E2E 留给后续里程碑。

---

## Claude's Discretion

- 具体的失败关键词列表确定
- dom_hash 前后对比的边界条件处理（_prev_dom_hash 为 None 的第一步）
- Section 9 每组规则的具体措辞

## Deferred Ideas

None — discussion stayed within phase scope.
