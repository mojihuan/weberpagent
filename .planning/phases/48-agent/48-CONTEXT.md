# Phase 48: 监控模块与 Agent 子类 - Context

**Gathered:** 2026-03-27
**Status:** Ready for planning

<domain>
## Phase Boundary

创建 MonitoredAgent(Agent) 子类和 3 个检测器（StallDetector、PreSubmitGuard、TaskProgressTracker），实现并通过单元测试。

**不包含：**
- 集成到 AgentService（Phase 50）
- 提示词优化（Phase 49）
- 参数调优（Phase 49）
- 端到端验证（Phase 51）

</domain>

<decisions>
## Implementation Decisions

### PreSubmitGuard 校验机制
- **D-01:** 通过 JavaScript 执行获取页面实际字段值。在 `_execute_actions()` 中通过 `self.browser_context` 执行 JS 读取 input/select 值，与期望值精确比较
- **D-02:** 使用 ERP 专用 JS 校验脚本。为当前 ERP 系统编写特定的 JS 脚本，知道每个字段对应的 input selector。不使用通用 DOM 扫描

### 文件组织
- **D-03:** 每个检测器独立文件。文件结构：
  - `backend/agent/monitored_agent.py` — MonitoredAgent 子类
  - `backend/agent/stall_detector.py` — StallDetector
  - `backend/agent/pre_submit_guard.py` — PreSubmitGuard
  - `backend/agent/task_progress_tracker.py` — TaskProgressTracker

### 状态管理
- **D-04:** 检测器自管理状态。每个检测器内部维护自己的状态（StallDetector 的连续失败计数器、DOM 指纹历史等）。MonitoredAgent 只负责创建实例和调用 check() 方法

### 干预消息格式
- **D-05:** 干预消息使用中文。与 ERP 系统和现有 CHINESE_ENHANCEMENT 提示词一致
- **D-06:** 结构化消息格式。每条消息包含：`[类型标签]` + 问题描述 + 建议动作
  - 示例：`【停滞警告】连续2次对元素#5操作失败。建议：尝试滚动页面、使用其他选择器、或跳过当前步骤。`

### 测试策略
- **D-07:** 纯单元测试（模拟）。检测器是纯 Python 逻辑，用模拟的 step_callback 参数测试。MonitoredAgent 测试模拟 browser-use Agent 的方法。不需要真实浏览器。覆盖率 >= 80%

### 错误处理
- **D-08:** 容错处理。检测器异常不阻塞 Agent 执行，只记录错误日志（category="monitor"）。Agent 继续运行但没有干预功能

### Claude's Discretion
- StallDetector 内部数据结构选择（deque vs list）
- PreSubmitGuard JS 脚本的具体选择器（由代码库和 ERP 页面决定）
- TaskProgressTracker 步骤解析的正则具体实现
- 单元测试的具体 mock 数据设计
- 干预消息的具体措辞

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求与路线图
- `.planning/REQUIREMENTS.md` — v0.6.3 完整需求定义（SUB-01~03, MON-01~08）
- `.planning/ROADMAP.md` — Phase 48 成功标准和计划结构

### 设计文档
- `docs/plans/2026-03-27-agent-reliability-design.md` — 5 个问题分析、3 个检测器设计、消息注入机制
- `docs/plans/2026-03-27-agent-reliability-impl.md` — 完整实施方案（6 个任务、TDD 代码、集成模式）

### 代码参考
- `backend/core/agent_service.py` — 当前 AgentService 实现，step_callback 是主要集成点
- `backend/agent/prompts.py` — 现有 CHINESE_ENHANCEMENT 提示词（Phase 49 将替换）
- `backend/agent/browser_agent.py` — UIBrowserAgent 封装（已废弃但可参考 extend_system_message 用法）

### browser-use 内部 API（只读参考）
- `.venv/lib/python3.11/site-packages/browser_use/agent/service.py` — Agent 类：_prepare_context()、_execute_actions()、_message_manager、register_new_step_callback
- `.venv/lib/python3.11/site-packages/browser_use/agent/message_manager/service.py` — MessageManager：_add_context_message()、prepare_step_state()（每步清空 context_messages）

### 先前阶段上下文
- `.planning/phases/39-loop-intervention-basics/39-CONTEXT.md` — Phase 39 循环干预设计（已被 Phase 45 清理，但设计理念可参考）
- `.planning/phases/46-code-simplification-and-testing/46-CONTEXT.md` — Phase 46 确认保留详细 step_callback 日志

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `agent_service.py` step_callback：已有 DOM hash 计算（SHA256 前 12 位）、元素计数、动作提取、截图保存等逻辑，新检测器可复用这些数据
- `browser_use.Agent.message_manager`：公共 @property，可直接访问 `_add_context_message()`
- `browser_use.Agent._prepare_context()`：可重写的标准方法，在 context_messages 清空后注入自定义消息的时机
- `browser_use.Agent._execute_actions()`：5 行方法调用 `self.multi_act()`，可在执行前拦截

### Established Patterns
- 数据库操作通过 Repository 模式
- 日志使用 Python logging 模块
- 异步回调使用 `asyncio.iscoroutinefunction()` 检测
- 文件命名：snake_case，类名 PascalCase

### Integration Points
- `run_with_streaming()` 中的 `step_callback` 是主要集成点（Phase 50 将替换为 MonitoredAgent）
- `_pending_interventions` 列表是 step_callback 与 _prepare_context() 之间的桥梁
- `extend_system_message` 参数在 Agent 构造时传入（Phase 50 使用）

### 关键技术约束
- `context_messages` 在每步开始时被 `prepare_step_state()` 清空，因此必须在 `_prepare_context()` 的 `super()` 调用之后注入
- `step_callback` 在 LLM 返回输出后、action 执行前调用，可以检测但不能阻止 action
- 要阻止 action 执行，必须重写 `_execute_actions()`
- browser-use 内置循环检测阈值偏弱（5/8/12），我们的 StallDetector 用更激进的阈值（2 次）

</code_context>

<specifics>
## Specific Ideas

- 干预消息示例：`【停滞警告】连续2次对元素#5操作失败。建议：尝试滚动页面、使用其他选择器、或跳过当前步骤。`
- PreSubmitGuard 校验示例：从 task 描述 "销售金额150元" 提取期望值 150，通过 JS 读取 ERP 页面对应 input 的值，不匹配时阻止提交
- Phase 39 的设计理念可参考（stagnation 检测、诊断日志），但代码已全部清理

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 48-agent*
*Context gathered: 2026-03-27*
