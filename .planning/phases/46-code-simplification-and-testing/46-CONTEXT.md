# Phase 46: 代码简化与测试 - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

简化 `step_callback` 并删除废弃的 scroll_table 测试文件。此阶段专注于清理 Phase 45 遗留的测试文件，确保测试套件与简化后的代码一致。

</domain>

<decisions>
## Implementation Decisions

### 日志保留策略
- **D-01:** 保持 step_callback 当前详细日志级别
  - 保留 DOM 文件保存功能 (`dom_{run_id}_step{step}.txt`)
  - 保留元素树遍历日志（前 5 个元素详情）
  - 保留 URL、动作、推理等基础日志
  - 保留截图保存功能
  - **理由:** 详细日志对定位问题有帮助，不增加维护成本

### 测试更新策略
- **D-02:** 删除 scroll_table 相关测试文件，不添加新测试
  - 删除 `backend/tests/unit/test_scroll_table_tool.py`
  - 删除 `backend/tests/e2e/test_scroll_table_e2e.py`
  - 保留现有 `backend/tests/test_agent_service.py` 和 `backend/tests/unit/test_agent_service.py`
  - **理由:** 现有测试已覆盖 agent_service 基础功能，无需额外测试

### Claude's Discretion
- 无。所有决策已明确。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求文档
- `.planning/REQUIREMENTS.md` — v0.6.2 需求定义 (SIMPLIFY-01, SIMPLIFY-02, TEST-01)
- `.planning/ROADMAP.md` — Phase 46 成功标准

### 代码参考
- `backend/core/agent_service.py` — 当前 step_callback 实现
- `backend/tests/unit/test_scroll_table_tool.py` — 待删除的单元测试
- `backend/tests/e2e/test_scroll_table_e2e.py` — 待删除的 E2E 测试

</canonical_refs>

<code_context>
## Existing Code Insights

### 当前状态 (Phase 45 后)
- `agent_service.py` 已完成清理：
  - 无 `register_scroll_table_tool` 导入
  - Agent 创建时不传入 `tools` 参数
  - step_callback 保留基础日志和截图功能

### 待删除文件
- `backend/tests/unit/test_scroll_table_tool.py` (177 行)
  - 包含 `TestScrollTableInputParams`, `TestScrollTableAndInput`, `TestToolRegistration` 类
  - 引用已删除的 `backend.agent.tools.scroll_table_tool` 模块

- `backend/tests/e2e/test_scroll_table_e2e.py` (175 行)
  - 包含 E2E 测试文档和验证测试
  - 引用已删除的 `ScrollTableInputParams` 和 `scroll_table_and_input`

### 保留文件
- `backend/tests/test_agent_service.py` — AgentService 基础测试
- `backend/tests/unit/test_agent_service.py` — LLM temperature 配置测试

### Integration Points
- 删除测试文件后需运行完整测试套件验证无破坏性影响

</code_context>

<specifics>
## Specific Ideas

无特殊要求。按 REQUIREMENTS.md 执行删除操作即可。

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 46-code-simplification-and-testing*
*Context gathered: 2026-03-26*
