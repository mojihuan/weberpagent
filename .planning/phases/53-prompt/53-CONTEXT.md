# Phase 53: Prompt 增强 — 表格交互 - Context

**Gathered:** 2026-03-30
**Status:** Ready for planning

<domain>
## Phase Boundary

扩展 ENHANCED_SYSTEM_MESSAGE 添加表格交互指导段落（第 7 段），让 Agent 能准确定位并操作表格中的 checkbox（单选/全选）、超链接文本和图标/操作按钮。

**不包含：**
- 代码层面修改 browser-use 源码
- 修改 Agent 参数配置（已在 Phase 49 调优）
- 键盘操作（Phase 52 已完成）
- 文件导入（Phase 54）
- 断言与缓存（Phase 55）
- E2E 综合验证（Phase 56）

</domain>

<decisions>
## Implementation Decisions

### Prompt 内容格式
- **D-01:** 作为 ENHANCED_SYSTEM_MESSAGE 的第 7 段落添加，保留现有 6 段不变（Phase 52 D-02 模式）
- **D-02:** 场景-动作对格式，与 Phase 52 键盘操作段落风格一致（Phase 52 D-01）
- **D-03:** 中文撰写，精简指令式风格，增量控制在 10 行以内（Phase 49 D-01、Phase 52 D-04）

### Checkbox 定位策略
- **D-04:** DOM 位置描述方式区分。表头 `<thead>` 中的 checkbox = 全选，`<tbody>` 行中的 checkbox = 单行选择。Agent 通过 DOM 层级位置判断 checkbox 用途

### 超链接定位策略
- **D-05:** 文本定位 + 直接点击。表格中的 `<a>` 超链接（如订单号、物品编号）用可见文本直接 click 定位。无需 find_elements 预查找

### 图标按钮定位策略
- **D-06:** title/aria-label 属性定位。表格行末尾的操作按钮（编辑、删除、查看等）通过 title 或 aria-label 属性定位。这些属性通常包含按钮的功能描述文本

### 否定指令
- **D-07:** 加入否定指令防止表格操作常见错误（延续 Phase 52 否定指令模式）。具体措辞由 Claude 决定

### 验证场景
- **D-08:** 使用采购单列表一站式验证，覆盖 TBL-01~04 全部 4 个需求。采购单列表同时包含 checkbox、超链接和图标按钮
- **D-09:** Plan 53-01 为 prompt 修改 + 测试，Plan 53-02 为采购单列表 ERP 场景验证（Phase 52 D-11 两 plan 模式）

### 测试策略
- **D-10:** 结构 + 关键词检查。测试 ENHANCED_SYSTEM_MESSAGE 包含表格交互关键词（checkbox、thead、tbody、a、aria-label、title），不检查具体措辞（Phase 49 D-09 模式）

### Claude's Discretion
- ENHANCED_SYSTEM_MESSAGE 表格交互段落的具体措辞
- 否定指令的具体内容和措辞
- 测试用例的具体关键词列表
- 验证步骤的具体 ERP 操作流程

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求与路线图
- `.planning/REQUIREMENTS.md` — TBL-01、TBL-02、TBL-03、TBL-04 表格交互需求定义
- `.planning/ROADMAP.md` — Phase 53 成功标准和计划结构

### 代码参考
- `backend/agent/prompts.py` — 现有 ENHANCED_SYSTEM_MESSAGE（6 段），将添加第 7 段
- `backend/core/agent_service.py` — Agent 创建处，extend_system_message 注入点
- `backend/tests/unit/test_enhanced_prompt.py` — 现有 prompt 测试，需扩展表格交互测试

### 先前阶段上下文
- `.planning/phases/52-prompt/52-CONTEXT.md` — Phase 52 键盘操作 Prompt 决策（场景-动作对格式、否定指令模式、两 plan 结构）
- `.planning/phases/49-prompt-optimization/49-CONTEXT.md` — Phase 49 Prompt 优化决策（精简指令式风格、中文撰写、段落结构）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/agent/prompts.py` ENHANCED_SYSTEM_MESSAGE：现有 6 段 prompt 结构（39 行），可直接追加第 7 段
- `backend/tests/unit/test_enhanced_prompt.py`：现有测试模式（关键词检查 + 行数限制），可扩展表格交互测试

### Established Patterns
- Agent 构造在 agent_service.py 中注入 extend_system_message（Phase 49 D-07）
- 新段落追加模式：保留现有段落，追加新段（Phase 52 D-02）
- 场景-动作对格式："场景 → 动作"（Phase 52 D-01）
- 否定指令有效阻止 Agent 错误行为（Phase 52 D-08 实际验证）
- Qwen 3.5 Plus 对精短指令遵守度更高（Phase 49 D-01）

### Integration Points
- `prompts.py` — 追加表格交互段落到 ENHANCED_SYSTEM_MESSAGE
- `test_enhanced_prompt.py` — 添加表格交互关键词断言
- Plan 53-02 通过前端触发采购单列表 ERP 测试验证

</code_context>

<specifics>
## Specific Ideas

- 表格交互场景示例：
  - "表头全选 → click thead 中的 checkbox"
  - "选择某行 → click tbody 行中对应 checkbox"
  - "点击订单号链接 → click 文本匹配的 <a> 元素"
  - "点击编辑按钮 → click title/aria-label='编辑' 的元素"
- 采购单列表验证场景：采购单页面包含 checkbox 全选/单选、订单号超链接、操作图标按钮
- 否定指令参考 Phase 52 模式：明确告知 Agent "不要..." 防止常见错误

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 53-prompt*
*Context gathered: 2026-03-30*
