# Phase 50: AgentService 集成 - Context

**Gathered:** 2026-03-28
**Status:** Ready for planning

<domain>
## Phase Boundary

将 Phase 48 的 MonitoredAgent + 3 个检测器（StallDetector、PreSubmitGuard、TaskProgressTracker）集成到 AgentService.run_with_streaming()，接通 step_callback，实现干预消息注入和结构化日志记录。

**不包含：**
- ENHANCED_SYSTEM_MESSAGE 内容修改（Phase 49 已完成）
- 参数调优（Phase 49 已完成）
- 端到端验证（Phase 51）
- 新增检测器或监控能力

</domain>

<decisions>
## Implementation Decisions

### step_callback 整合方式
- **D-01:** 保留现有 step_callback 不变，在其中添加检测器调用。不使用 MonitoredAgent.create_step_callback()
- **D-02:** 在现有 step_callback 末尾（日志逻辑之后、on_step 回调之前），通过 `agent._stall_detector.check()` 和 `agent._task_tracker.check_progress()` 调用检测器
- **D-03:** 检测器结果存入 `agent._pending_interventions`（由 MonitoredAgent._prepare_context() 自动注入）

### Monitor 日志记录
- **D-04:** 将 run_logger 传入 MonitoredAgent 构造，使检测器干预和拦截事件通过 run_logger.log(category="monitor") 记录
- **D-05:** 在 _prepare_context() 注入干预消息时记录，在 _execute_actions() PreSubmitGuard 拦截时记录

### Agent 替换
- **D-06:** 将 `Agent(...)` 替换为 `MonitoredAgent(...)`，保留 Phase 49 的所有参数（extend_system_message、loop_detection_window 等）
- **D-07:** 3 个检测器实例在 MonitoredAgent 创建前初始化，通过关键字参数传入

### Claude's Discretion
- 检测器调用的具体位置（step_callback 中哪个时机最优）
- run_logger 在 MonitoredAgent 中的传递方式（构造参数 vs 属性注入）
- 单元测试的具体 mock 设计

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求与路线图
- `.planning/REQUIREMENTS.md` — v0.6.3 完整需求定义（INTEG-01~05）
- `.planning/ROADMAP.md` — Phase 50 成功标准和计划结构

### 设计文档
- `docs/plans/2026-03-27-agent-reliability-design.md` — 5 个问题分析、集成模式设计
- `docs/plans/2026-03-27-agent-reliability-impl.md` — 完整实施方案、集成模式

### 代码参考（核心修改文件）
- `backend/core/agent_service.py` — AgentService.run_with_streaming()，Agent 创建处（:297），step_callback（:155-288）
- `backend/agent/monitored_agent.py` — MonitoredAgent 子类，create_step_callback()（不使用）
- `backend/agent/stall_detector.py` — StallDetector.check() 接口
- `backend/agent/pre_submit_guard.py` — PreSubmitGuard.check() 接口
- `backend/agent/task_progress_tracker.py` — TaskProgressTracker.check_progress() 接口
- `backend/agent/prompts.py` — ENHANCED_SYSTEM_MESSAGE（Phase 49 已完成）
- `backend/utils/run_logger.py` — RunLogger 结构化日志记录器

### browser-use 内部 API（只读参考）
- `.venv/lib/python3.11/site-packages/browser_use/agent/service.py` — Agent 类：register_new_step_callback 参数

### 先前阶段上下文
- `.planning/phases/48-agent/48-CONTEXT.md` — Phase 48 监控模块设计决策
- `.planning/phases/49-prompt-optimization/49-CONTEXT.md` — Phase 49 参数调优决策

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `agent_service.py:155-288` step_callback：已有 DOM hash 计算、元素计数、动作提取、截图保存、run_logger 日志逻辑。检测器调用可直接复用这些已提取的数据（action_name、target_index、evaluation、dom_hash）
- `monitored_agent.py` MonitoredAgent：已实现 _prepare_context() 注入和 _execute_actions() 拦截。create_step_callback() 包含检测器调用逻辑可参考但不直接使用
- `run_logger.py` RunLogger：已有 log()、log_agent()、log_browser() 方法，支持 category 参数

### Established Patterns
- Agent 构造在 agent_service.py:297，Phase 49 已注入 ENHANCED_SYSTEM_MESSAGE 和调优参数
- step_callback 是闭包，可访问 run_logger、agent（创建后）等外部变量
- 检测器异常不阻塞执行（Phase 48 D-08 容错处理）

### Integration Points
- `agent_service.py:297` Agent() 构造 → 替换为 MonitoredAgent()
- `agent_service.py:155-288` step_callback → 添加检测器调用
- `monitored_agent.py:123-215` create_step_callback() → 参考但不直接使用（D-01）
- MonitoredAgent._prepare_context() → 通过子类重写自动生效
- MonitoredAgent._execute_actions() → PreSubmitGuard 拦截自动生效

</code_context>

<specifics>
## Specific Ideas

- step_callback 中检测器调用示例：`stall_result = agent._stall_detector.check(action_name=action_name, target_index=target_index, evaluation=evaluation, dom_hash=dom_hash)`
- 已提取的 action_name、target_index、evaluation、dom_hash 可直接传给检测器，无需重复提取
- run_logger 记录示例：`run_logger.log("warning", "monitor", "Stall detected", step=step, message=stall_result.message)`

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 50-agentservice*
*Context gathered: 2026-03-28*
