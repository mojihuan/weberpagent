# Phase 63: 代码对比分析 - Context

**Gathered:** 2026-04-06
**Status:** Ready for planning

<domain>
## Phase Boundary

对比 v0.4.0 与当前版本的 browser-use 初始化代码、Playwright 配置、browser-use 版本变更、agent_service.py 中 Agent/Browser 配置的演变。输出结构化对比结果供 Phase 64 报告使用。

**不包含：**
- 修复浏览器模式问题（留给后续 milestone）
- 恢复 headed 模式
- 代码修改

</domain>

<decisions>
## Implementation Decisions

### 对比输出格式
- **D-01:** 按配置项逐项对比，输出格式：`配置项 | v0.4.0 值 | 当前值 | 变更提交`
  - 对比维度：Agent 构造参数、BrowserSession/BrowserProfile 配置、Playwright 启动参数、browser-use 版本
  - 每个配置项独立一行，Phase 64 报告可直接引用

### 对比范围
- **D-02:** 快照对比 — 只看 v0.4.0 vs 当前版本的差异
  - 不追踪中间提交（约 20 个），只做两端对比
  - 中间提交信息用于标注变更提交 hash，不做逐一分析

### 表格输入关联分析
- **D-03:** 深入关联分析 — 研究	headless vs headed 模式下的 DOM 渲染差异
  - 对比 headless 和 headed 模式下 Ant Design 表格的 DOM 结构差异
  - 分析 headless 模式是否影响 input 元素的渲染时机（click-to-edit 表格是否在 headless 下不渲染 input）
  - 研究 headless 模式对元素定位、CSS 计算的影响
  - 评估 v0.8.1 的 DOM Patch（td 文本检测）是否为正确绕行方案

### Claude's Discretion
- 具体配置项的粒度划分（哪些合并、哪些独立列出）
- 中间提交 hash 的选择（标注关键变更即可）
- headless/headed 渲染差异的测试方法（代码分析 vs 实际运行对比）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求与路线图
- `.planning/REQUIREMENTS.md` — v0.8.2 需求定义（DIFF-01~04）
- `.planning/ROADMAP.md` — Phase 63 成功标准和计划结构

### 代码参考（核心对比文件）
- `backend/core/agent_service.py` — 当前版本 AgentService 实现
- `backend/agent/monitored_agent.py` — MonitoredAgent 子类
- `backend/agent/prompts.py` — ENHANCED_SYSTEM_MESSAGE
- `backend/agent/dom_patch.py` — v0.8.1 DOM 5 patches

### Git 历史参考
- `v0.4.0` tag — v0.4.0 时的 agent_service.py 快照
- `f951791` — 引入 BrowserSession + headless=True 的提交（v0.5.0 云端部署）
- `c84f4e1` — 添加 viewport 配置
- `e2157a1` — Agent 替换为 MonitoredAgent

### browser-use 内部 API
- `.venv/lib/python3.11/site-packages/browser_use/agent/service.py` — Agent 类构造参数
- `.venv/lib/python3.11/site-packages/browser_use/browser/session.py` — BrowserSession 类
- `.venv/lib/python3.11/site-packages/browser_use/browser/profile.py` — BrowserProfile 配置

### 先前阶段上下文
- `.planning/phases/46-code-simplification-and-testing/46-CONTEXT.md` — Phase 46 清理后的 Agent 创建模式
- `.planning/phases/48-agent/48-CONTEXT.md` — Phase 48 MonitoredAgent 设计决策
- `.planning/phases/50-agentservice/50-CONTEXT.md` — Phase 50 AgentService 集成决策

</canonical_refs>

<code_context>
## Existing Code Insights

### 关键差异已识别（v0.4.0 vs 当前）

**v0.4.0 Agent 创建（2 处）：**
```python
# run_simple
agent = Agent(task=task, llm=llm, max_actions_per_step=5)

# run_with_streaming
agent = Agent(task=actual_task, llm=llm, max_actions_per_step=5, register_new_step_callback=step_callback)
```
- 无 BrowserSession/BrowserProfile
- 无 headless 配置 → browser-use 默认 headed（弹出浏览器窗口）
- 无 extend_system_message
- 无 loop_detection_window 等监控参数

**当前版本 Agent 创建（2 处）：**
```python
# run_simple
browser_session = create_browser_session()  # BrowserProfile(headless=True, ...)
agent = Agent(task=task, llm=llm, browser_session=browser_session, max_actions_per_step=5)

# run_with_streaming
browser_session = create_browser_session()
agent = MonitoredAgent(task=..., llm=..., browser_session=browser_session,
    max_actions_per_step=5, register_new_step_callback=step_callback,
    extend_system_message=ENHANCED_SYSTEM_MESSAGE, loop_detection_window=10,
    max_failures=4, planning_replan_on_stall=2, enable_planning=True,
    stall_detector=..., pre_submit_guard=..., task_progress_tracker=..., run_logger=...)
```
- 显式 BrowserSession + BrowserProfile(headless=True)
- SERVER_BROWSER_ARGS 6 个 Chrome 参数
- MonitoredAgent 替代原生 Agent
- 多个监控和优化参数

### 根因定位
- **核心变更提交**: `f951791` (2026-03-24) — 为 Linux 服务器部署添加 BrowserSession(headless=True)
- **影响**: 本地开发也使用同一个 create_browser_session()，导致本地也 headless

### Reusable Assets
- `git diff v0.4.0 HEAD -- backend/core/agent_service.py` — 完整差异
- `git show v0.4.0:backend/core/agent_service.py` — v0.4.0 快照
- `backend/agent/dom_patch.py` — v0.8.1 的 click-to-edit 绕行方案

### Integration Points
- 对比结果写入 Phase 63 计划文件，供 Phase 64 报告引用
- 分析报告中的根因分析需要关联到 DIFF-01~04 需求项

</code_context>

<specifics>
## Specific Ideas

- 对比表应包含的配置项：Agent class、task、llm、browser_session、headless、Chrome args、viewport、max_actions_per_step、register_new_step_callback、extend_system_message、loop_detection_window、max_failures、planning_replan_on_stall、enable_planning、监控器参数
- headless 渲染差异需要研究：Chromium headless 模式对 CSS :hover/:focus 的处理、JavaScript 事件模拟的差异、Ant Design 表格组件在 headless 下的渲染行为
- 关联分析可以参考 browser-use 官方文档对 headless 模式的说明

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 63-代码对比分析*
*Context gathered: 2026-04-06*
