# Phase 48: 监控模块与 Agent 子类 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-27
**Phase:** 48-agent
**Areas discussed:** PreSubmitGuard 校验机制, 检测器架构与状态管理, 干预消息格式与语言, 测试策略, 错误处理

---

## PreSubmitGuard 校验机制

| Option | Description | Selected |
|--------|-------------|----------|
| JavaScript 执行 | 在 _execute_actions() 中通过 self.browser_context 执行 JS 读取 input/select 值，精确校验 | ✓ |
| DOM 文本解析 | 从 browser_state.dom_state 解析字段值 | |
| LLM 自校验提示 | 注入提示消息让 LLM 自己检查字段 | |
| 混合策略 | 结合多种方式 | |

**User's choice:** JavaScript 执行
**Notes:** 最精确的方式，但需要知道字段定位方式

### JS 脚本策略

| Option | Description | Selected |
|--------|-------------|----------|
| ERP 专用 JS 脚本 | 为当前 ERP 系统编写特定的 JS 校验脚本 | ✓ |
| 通用 DOM 扫描 | 扫描所有 input/select 提取值 | |

**User's choice:** ERP 专用 JS 脚本
**Notes:** REQUIREMENTS.md 已明确 JS 校验脚本针对当前 ERP 适配

---

## 文件组织

| Option | Description | Selected |
|--------|-------------|----------|
| 独立文件 | 每个检测器独立文件 + MonitoredAgent | ✓ |
| 检测器合并 | 3 个检测器合并到 monitors.py | |
| monitors/ 子目录 | 子目录结构 | |

**User's choice:** 独立文件
**Notes:** 符合高内聚低耦合原则，每个文件 < 200 行

---

## 状态管理

| Option | Description | Selected |
|--------|-------------|----------|
| 检测器自管理状态 | 每个检测器内部维护自己的状态 | ✓ |
| Agent 集中管理 | 状态存在 MonitoredAgent 实例上 | |

**User's choice:** 检测器自管理状态
**Notes:** 符合单一职责原则

---

## 干预消息语言

| Option | Description | Selected |
|--------|-------------|----------|
| 中文 | 与 ERP 系统和现有提示词一致 | ✓ |
| 英文 | 与 browser-use 内置消息一致 | |
| 混合（中英） | 关键指令中文，结构化部分英文 | |

**User's choice:** 中文
**Notes:** 系统提示词 CHINESE_ENHANCEMENT 和 ERP 系统都是中文

### 消息格式

| Option | Description | Selected |
|--------|-------------|----------|
| 结构化（标签+问题+建议） | [类型标签] + 问题描述 + 建议动作 | ✓ |
| 简约（仅描述） | 只包含问题描述 | |
| Claude 决定 | 由实现者决定 | |

**User's choice:** 结构化（标签+问题+建议）
**Notes:** 示例：【停滞警告】连续2次对元素#5操作失败。建议：尝试滚动页面、使用其他选择器、或跳过当前步骤。

---

## 测试策略

| Option | Description | Selected |
|--------|-------------|----------|
| 纯单元测试（模拟） | 用模拟数据测试，不需要真实浏览器 | ✓ |
| 单元+集成测试 | 单元 + 与真实 browser-use Agent 集成 | |
| Claude 决定 | 由实现者决定 | |

**User's choice:** 纯单元测试（模拟）
**Notes:** 检测器是纯 Python 逻辑，模拟即可。覆盖率 >= 80%

---

## 错误处理

| Option | Description | Selected |
|--------|-------------|----------|
| 容错（不阻塞） | 检测器异常不阻塞 Agent 执行 | ✓ |
| 严格（向上冒泡） | 异常向上冒泡可能导致测试中断 | |

**User's choice:** 容错（不阻塞）
**Notes:** 测试执行不应因监控模块崩溃而中断

---

## Claude's Discretion

- StallDetector 内部数据结构选择
- PreSubmitGuard JS 脚本的具体选择器
- TaskProgressTracker 步骤解析的正则实现
- 单元测试的具体 mock 数据设计
- 干预消息的具体措辞

## Deferred Ideas

None — discussion stayed within phase scope.
