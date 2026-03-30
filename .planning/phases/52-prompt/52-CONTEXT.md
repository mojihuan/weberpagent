# Phase 52: Prompt 增强 — 键盘操作 - Context

**Gathered:** 2026-03-30
**Status:** Ready for planning

<domain>
## Phase Boundary

扩展 ENHANCED_SYSTEM_MESSAGE 添加键盘操作指导段落（第 6 段），让 Agent 能通过 Prompt 指导正确执行 Ctrl+V 粘贴、Enter 回车确认、ESC 关闭弹窗等键盘操作。

**不包含：**
- 代码层面修改 browser-use 源码
- 修改 Agent 参数配置（已在 Phase 49 调优）
- 表格交互（Phase 53）
- 文件导入（Phase 54）
- 断言与缓存（Phase 55）
- E2E 综合验证（Phase 56）

</domain>

<decisions>
## Implementation Decisions

### Prompt 内容格式
- **D-01:** 场景-动作对格式。每条规则以"场景 → 动作"形式描述，如"搜索框输入后 → send_keys('Enter')触发搜索"。符合 Phase 49 的精简指令式风格
- **D-02:** 作为 ENHANCED_SYSTEM_MESSAGE 的第 6 段落添加，保留现有 5 段不变
- **D-03:** 中文撰写，与现有 prompt 风格一致（Phase 49 D-03）
- **D-04:** 总长度增量控制在 10 行以内，避免 prompt 过长影响 Qwen 遵守率

### 粘贴操作策略
- **D-05:** 采用"先全选再覆盖"模式。用 send_keys('Control+a') 全选输入框内容，再用 input action 输入新值覆盖。不依赖系统剪贴板状态
- **D-06:** 不指导 Agent 使用 send_keys('Control+v') 粘贴操作。剪贴板内容不确定，粘贴策略不可靠

### Enter 回车使用
- **D-07:** 仅搜索触发式场景。当输入框是搜索框（如物品编号搜索框）时，输入完成后用 send_keys('Enter') 触发搜索。不用于表单提交

### ESC 关闭弹窗
- **D-08:** 仅关闭弹窗场景。当日期选择器、下拉弹窗等遮挡元素出现时，用 send_keys('Escape') 关闭。不扩展到取消操作等场景

### 验证场景
- **D-09:** 使用采购单场景验证。采购单的"输入 IMEI/物品编号"后回车触发搜索 + 日期选择器 ESC 关闭。这是最典型的 ERP 键盘操作场景

### 测试策略
- **D-10:** 结构 + 关键词检查。测试 ENHANCED_SYSTEM_MESSAGE 包含键盘操作关键词（send_keys、Enter、Escape、Control+a），不检查具体措辞
- **D-11:** Plan 52-01 为 prompt 修改，Plan 52-02 为 ERP 场景验证

### Claude's Discretion
- ENHANCED_SYSTEM_MESSAGE 键盘操作段落的具体措辞
- 测试用例的具体关键词列表
- 验证步骤的具体 ERP 操作流程

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求与路线图
- `.planning/REQUIREMENTS.md` — KB-01、KB-02、KB-03 键盘操作需求定义
- `.planning/ROADMAP.md` — Phase 52 成功标准和计划结构

### 代码参考
- `backend/agent/prompts.py` — 现有 ENHANCED_SYSTEM_MESSAGE（5 段），将添加第 6 段
- `backend/core/agent_service.py` — Agent 创建处，extend_system_message 注入点
- `backend/tests/unit/test_enhanced_prompt.py` — 现有 prompt 测试，需扩展

### browser-use 键盘操作 API（只读参考）
- `.venv/lib/python3.11/site-packages/browser_use/tools/views.py` — SendKeysAction 模型：keys 参数（如 "Escape"、"Enter"、"Control+a"）
- `.venv/lib/python3.11/site-packages/browser_use/browser/watchdogs/default_action_watchdog.py:1371-1480` — send_keys 事件处理器：支持键别名（ctrl→Control、esc→Escape、enter→Enter）、组合键解析（+分隔）、CDP keyDown/keyUp 派发

### 先前阶段上下文
- `.planning/phases/49-prompt-optimization/49-CONTEXT.md` — Phase 49 Prompt 优化决策（精简指令式风格、中文撰写、5 段结构）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/agent/prompts.py` ENHANCED_SYSTEM_MESSAGE：现有 5 段 prompt 结构可直接追加第 6 段
- `backend/tests/unit/test_enhanced_prompt.py`：现有测试模式（关键词检查 + 结构验证），可直接扩展键盘操作测试

### Established Patterns
- browser-use 的 send_keys 动作通过 CDP DispatchKeyEvent 实现，支持键别名和组合键
- 键别名映射：ctrl→Control、esc→Escape、enter→Enter
- 组合键格式：'+' 分隔，如 'Control+a'、'Control+v'
- Agent 构造在 agent_service.py 中注入 extend_system_message（Phase 49 D-07）

### Integration Points
- `prompts.py` — 追加键盘操作段落到 ENHANCED_SYSTEM_MESSAGE
- `test_enhanced_prompt.py` — 添加键盘操作关键词断言
- Plan 52-02 通过前端触发实际 ERP 测试验证

### 关键技术约束
- browser-use 的 SendKeysEvent 在 `.venv/.../browser/session.py` 中被注释掉（`# self.event_bus.on(SendKeysEvent, ...)`），需确认 send_keys 动作是否正常工作
- Qwen 3.5 Plus 对精短指令遵守度更高（Phase 49 D-01），键盘操作段落需简洁

</code_context>

<specifics>
## Specific Ideas

- 场景-动作对示例：
  - "搜索框输入后 → send_keys('Enter')触发搜索"
  - "日期选择器遮挡 → send_keys('Escape')关闭"
  - "需清空输入框 → send_keys('Control+a')全选后 input 新值"
- 采购单验证场景：物品编号输入框输入后按 Enter 触发搜索/确认 + 日期弹窗用 ESC 关闭
- 粘贴操作不使用 Ctrl+V（剪贴板内容不确定），改用全选+覆盖策略

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 52-prompt*
*Context gathered: 2026-03-30*
