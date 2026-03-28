# Phase 51: 端到端验证 - Context

**Gathered:** 2026-03-28
**Status:** Ready for planning

<domain>
## Phase Boundary

运行 ERP 销售出库测试，验证 Phase 48-50 的监控模块（StallDetector、PreSubmitGuard、TaskProgressTracker）、提示词优化（ENHANCED_SYSTEM_MESSAGE）和 AgentService 集成的实际效果。确认单元测试通过且覆盖率达标。

**不包含：**
- 新增功能或模块
- 修改现有代码
- 新增检测器或监控能力

</domain>

<decisions>
## Implementation Decisions

### 单元测试验证范围
- **D-01:** 运行全量测试（包括已有测试），确保回归安全。不只跑 Phase 48-50 新增测试
- **D-02:** 覆盖率只统计 Phase 48-50 新增的 6 个模块（monitored_agent、stall_detector、pre_submit_guard、task_progress_tracker、enhanced_prompt、agent_params），目标 >= 80%

### E2E 测试执行方式
- **D-03:** 通过平台 UI 手动执行。创建/执行任务，观察运行过程和日志输出，人工判断是否通过。与真实用户使用场景一致
- **D-04:** 复用原测试用例。使用 outputs/7fcea593 记录中的同一个销售出库测试用例，直接对比改善效果

### 验证成功标准（来自 REQUIREMENTS.md）
- **D-05:** VAL-02 — Agent 不再对同一元素重复失败超过 2 次（StallDetector 效果）
- **D-06:** VAL-03 — per-run 日志中出现 category="monitor" 条目（检测器接入效果）
- **D-07:** VAL-04 — 提交前有 PreSubmitGuard 拦截记录（校验效果）

### Claude's Discretion
- 全量测试运行的具体命令和参数
- 覆盖率报告的生成方式
- E2E 验证结果的人工判读标准细化
- 验证不通过时的回退策略建议

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求与路线图
- `.planning/REQUIREMENTS.md` — v0.6.3 完整需求定义（VAL-01~04）
- `.planning/ROADMAP.md` — Phase 51 成功标准和计划结构

### 设计文档
- `docs/plans/2026-03-27-agent-reliability-design.md` — 5 个问题分析（验证这些问题的解决效果）
- `docs/plans/2026-03-27-agent-reliability-impl.md` — 完整实施方案（验证实现完整性）

### 代码参考（验证目标模块）
- `backend/agent/monitored_agent.py` — MonitoredAgent 子类
- `backend/agent/stall_detector.py` — StallDetector
- `backend/agent/pre_submit_guard.py` — PreSubmitGuard
- `backend/agent/task_progress_tracker.py` — TaskProgressTracker
- `backend/agent/prompts.py` — ENHANCED_SYSTEM_MESSAGE
- `backend/core/agent_service.py` — AgentService（MonitoredAgent 替换 + step_callback 检测器调用）
- `backend/utils/run_logger.py` — RunLogger 结构化日志

### 测试文件（验证目标）
- `backend/tests/unit/test_stall_detector.py`
- `backend/tests/unit/test_pre_submit_guard.py`
- `backend/tests/unit/test_task_progress_tracker.py`
- `backend/tests/unit/test_monitored_agent.py`
- `backend/tests/unit/test_enhanced_prompt.py`
- `backend/tests/unit/test_agent_params.py`
- `backend/tests/unit/test_agent_service.py` — Phase 50 集成测试

### 先前阶段上下文
- `.planning/phases/48-agent/48-CONTEXT.md` — Phase 48 监控模块设计决策
- `.planning/phases/49-prompt-optimization/49-CONTEXT.md` — Phase 49 参数调优决策
- `.planning/phases/50-agentservice/50-CONTEXT.md` — Phase 50 集成决策

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- 全量测试已有 28+ 个测试文件（`backend/tests/unit/` 和 `backend/tests/`），可直接运行 `uv run pytest backend/tests/ -v`
- 覆盖率工具已配置：`uv run pytest backend/tests/ --cov=backend --cov-report=term-missing`
- 平台 UI 已部署在 121.40.191.49，可直接创建测试任务执行

### Established Patterns
- 测试运行命令：`uv run pytest backend/tests/ -v`
- 覆盖率命令：`uv run pytest backend/tests/ --cov=backend --cov-report=term-missing`
- 已知有 5 个预存隔离问题的测试（test_external_bridge, test_browser_cleanup, test_precondition_service）
- per-run 日志存储在 `outputs/` 目录下

### Integration Points
- 平台前端 → API → AgentService.run_with_streaming() → MonitoredAgent → 检测器
- run_logger 输出到 per-run 日志文件，可通过日志查看 monitor 类别条目
- outputs/ 目录存储每次运行的完整日志和截图

</code_context>

<specifics>
## Specific Ideas

- 对比 outputs/7fcea593（原运行记录）和新运行结果，确认改善效果
- 原记录暴露的 5 个问题：表格 click-to-edit 不可见、循环重试（12步）、值误填、步骤遗漏、提交未校验
- 验证重点：循环重试不超过 2 次、monitor 日志出现、PreSubmitGuard 拦截记录

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 51-e2e-verification*
*Context gathered: 2026-03-28*
