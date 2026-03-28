# Phase 49: 提示词优化与参数调优 - Context

**Gathered:** 2026-03-28
**Status:** Ready for planning

<domain>
## Phase Boundary

创建 ENHANCED_SYSTEM_MESSAGE（合并替换现有 CHINESE_ENHANCEMENT），通过 extend_system_message 注入 agent_service.py，调优 browser-use 内置参数（loop_detection_window、max_failures、planning_replan_on_stall）。

**不包含：**
- MonitoredAgent 集成到 AgentService（Phase 50）
- step_callback 接入检测器（Phase 50）
- 端到端验证（Phase 51）

</domain>

<decisions>
## Implementation Decisions

### Prompt 内容
- **D-01:** 精简指令式风格。每条规则一句话，总长度控制在 60 行以内。Qwen 3.5 Plus 对简短指令遵守更好
- **D-02:** 合并替换现有 CHINESE_ENHANCEMENT。将原有有价值的表单字段映射和选择器策略融入 ENHANCED_SYSTEM_MESSAGE，删除 CHINESE_ENHANCEMENT
- **D-03:** 中文撰写。与 ERP 系统语言和 Phase 48 干预消息一致
- **D-04:** 内容边界：PRM-01~04 四部分 + 原有 CHINESE_ENHANCEMENT 有价值内容 + 允许 Claude 根据 ERP 场景补充相关指导（弹窗处理、列表选择器等）
- **D-05:** 4 部分 prompt 结构：
  1. 表格 click-to-edit 模式说明（PRM-01）
  2. 失败恢复强制规则 — 2 次失败后禁止重试，强制替代策略（PRM-02）
  3. 字段填写后验证指导（PRM-03）
  4. 提交前校验规则（PRM-04）

### 参数配置
- **D-06:** 参数硬编码在 agent_service.py 的 Agent() 构造调用中。Phase 50 集成 MonitoredAgent 时保留这些参数
- **D-07:** Phase 49 就修改 agent_service.py 注入 extend_system_message 和调优参数，不等到 Phase 50
- **D-08:** 参数值：`loop_detection_window=10`、`max_failures=4`、`planning_replan_on_stall=2`、`enable_planning=True`

### 测试策略
- **D-09:** 结构 + 参数检查。测试 ENHANCED_SYSTEM_MESSAGE 包含关键词（click-to-edit、失败、验证、提交），不检查具体措辞。测试 Agent 构造传入正确参数值
- **D-10:** 新建独立测试文件 `test_enhanced_prompt.py` 和 `test_agent_params.py`，不修改现有测试

### Claude's Discretion
- ENHANCED_SYSTEM_MESSAGE 各部分的具体措辞和措辞细节
- ERP 场景补充内容的具体范围
- 从 CHINESE_ENHANCEMENT 中保留哪些有价值内容的取舍
- 测试用例的具体关键词列表

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求与路线图
- `.planning/REQUIREMENTS.md` — v0.6.3 完整需求定义（PRM-01~05, TUNE-01~04）
- `.planning/ROADMAP.md` — Phase 49 成功标准和计划结构

### 设计文档
- `docs/plans/2026-03-27-agent-reliability-design.md` — 5 个问题分析、4 部分 prompt 框架设计（Part 1-4）、模块 4 Prompt 优化部分

### 代码参考
- `backend/agent/prompts.py` — 现有 CHINESE_ENHANCEMENT（将被替换）
- `backend/core/agent_service.py` — Agent 创建处（:296），需注入 extend_system_message 和调优参数
- `backend/agent/monitored_agent.py` — Phase 48 创建的 MonitoredAgent 子类（Phase 50 集成参考）

### browser-use 内部 API（只读参考）
- `.venv/lib/python3.11/site-packages/browser_use/agent/service.py` — Agent 构造函数参数：extend_system_message、max_failures、enable_planning、planning_replan_on_stall、loop_detection_window

### 先前阶段上下文
- `.planning/phases/48-agent/48-CONTEXT.md` — Phase 48 监控模块设计决策（消息格式、容错处理等）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/agent/prompts.py` CHINESE_ENHANCEMENT：表单字段映射（用户名/密码/登录等）、选择器策略（text > role > CSS）、错误处理策略可融入新 prompt
- `backend/agent/browser_agent.py`：有 extend_system_message=CHINESE_ENHANCEMENT 使用示例（已废弃但可参考）
- `backend/agent/proxy_agent.py`：同样有 extend_system_message 使用参考

### Established Patterns
- Agent 构造在 `agent_service.py:296`，当前无 extend_system_message
- 参数全部用 browser-use 默认值：max_failures=5, planning_replan_on_stall=3, loop_detection_window=20
- 测试文件命名：`test_*.py`，放在 `backend/tests/unit/` 或 `backend/tests/`

### Integration Points
- `agent_service.py:296` Agent() 构造 — Phase 49 注入参数
- `prompts.py` — Phase 49 修改/新增 ENHANCED_SYSTEM_MESSAGE
- Phase 50 将 `Agent()` 替换为 `MonitoredAgent()`，保留 extend_system_message 和参数

</code_context>

<specifics>
## Specific Ideas

- ERP 表格 click-to-edit 特征：Ant Design 表格的 `<td>` 在 DOM 快照中为空，需要先 click 触发编辑模式
- 失败恢复示例：同一元素 2 次失败后，用 `evaluate` 执行 JS、`find_elements` 精确查找、或跳过
- 原有 CHINESE_ENHANCEMENT 中有价值的内容：中文表单字段映射、选择器策略优先级
- 干预消息格式参考 Phase 48：`【类型标签】问题描述 + 建议动作`

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 49-prompt-optimization*
*Context gathered: 2026-03-28*
