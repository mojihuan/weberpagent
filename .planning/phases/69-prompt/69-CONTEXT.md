# Phase 69: 服务集成与 Prompt 规则 - Context

**Gathered:** 2026-04-07
**Status:** Ready for planning

<domain>
## Phase Boundary

将 Phase 67/68 已实现但未启用的检测器和追踪器连接到实际运行流程，并在 Section 9 追加操作规则让 Agent 理解行标识、反重复、策略优先级和失败恢复。

**两个 Plan 范围：**
- 69-01: step_callback 集成与状态重置 — 在 agent_service.py 的 inline step_callback 中调用 detect_failure_mode() 和 update_failure_tracker()
- 69-02: Section 9 Prompt 规则追加 — 追加行标识/反重复/策略优先级/失败恢复四组规则

**不包含：**
- 修改现有 Section 9 内容
- 修改 monitored_agent.py 的死代码
- 恢复 headed 模式
- 移除现有 DOM Patch 或 Section 9 内容
- E2E 测试（v0.8.4 后续里程碑）

</domain>

<decisions>
## Implementation Decisions

### step_callback 集成
- **D-01:** 调用顺序：先 `detect_failure_mode()` 检测失败，如果有失败结果（`failure_mode is not None`）则调用 `update_failure_tracker()` 写入 tracker
  - **Why:** 逻辑清晰：检测→写入→下游 dom_patch 读取。避免无谓写入
  - **How to apply:** step_callback 中 stall_detector.check() 之后再调 detect_failure_mode()，条件判断后才 update

- **D-02:** dom_hash_before/after 通过闭包变量存储。step_callback 用 `_prev_dom_hash` 闭包变量存上一步 dom_hash，调用后更新为当前 dom_hash
  - **Why:** 简单直接，参考 stall_detector._history 的模式，无需修改 StallDetector 内部
  - **How to apply:** 在 step_callback 闭包外层初始化 `_prev_dom_hash = None`，每步末尾 `_prev_dom_hash = dom_hash`

- **D-03:** 仅在失败时调用 detect_failure_mode()。条件：evaluation 包含失败关键词（'失败'/'wrong'/'error'/'无法'/'不成功'/'未'）
  - **Why:** 避免成功 step 的无谓计算，减少 detect_failure_mode() 调用频率
  - **How to apply:** 在 stall_detector.check() 之前检查 evaluation 是否包含失败关键词

- **D-04:** 只修改 agent_service.py 的 inline step_callback，不碰 monitored_agent.py 的死代码
  - **Why:** monitored_agent.py 的 create_step_callback 当前未使用，减少变更范围
  - **How to apply:** 所有集成工作集中在 agent_service.py 的 run_with_streaming() 内

### Section 9 Prompt 规则
- **D-05:** 简洁操作指令风格，每组规则 2-4 行，"看到 X → 做 Y" 格式，不加解释性文字。与现有 Section 9 风格一致
  - **Why:** Prompt 空间有限，Agent 对简洁操作指令理解更好
  - **How to apply:** 每组规则以标题行开头，紧跟操作指令列表

- **D-06:** 规则追加顺序：行标识 → 反重复 → 策略优先级 → 失败恢复（定位→操作→异常的逻辑链）
  - **Why:** Agent 先学会定位（行标识），再学会操作（策略），最后处理异常（失败恢复）
  - **How to apply:** 按此顺序在 Section 9 末尾追加四个子节

- **D-07:** 只追加新规则，不修改现有 Section 9 内容
  - **Why:** 现有内容已验证有效，修改可能引入回归
  - **How to apply:** 在现有 Section 9 末尾（line 83 之后）追加新规则

### 集成测试
- **D-08:** Mock 单元测试为主，mock step_callback 的输入，验证调用链路和数据正确性
  - **Why:** 快速可重复，覆盖核心集成逻辑。E2E 测试留给后续里程碑
  - **How to apply:** 测试 detect_failure_mode() 被正确调用、update_failure_tracker() 正确写入、_failure_tracker 数据正确

### Claude's Discretion
- 具体的失败关键词列表确定
- detect_failure_mode() 调用的 dom_hash 前后对比的具体边界条件处理（如 _prev_dom_hash 为 None 的第一步）
- Section 9 每组规则的具体措辞

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 设计文档
- `.planning/phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md` — Phase 66 优化方案设计，D-01~D12 决策、T01-T16 代码任务清单
- `.planning/phases/66-优化方案设计/66-CONTEXT.md` — Phase 66 设计决策完整记录
- `.planning/REQUIREMENTS.md` — v0.8.4 需求 ANTI-03, RECOV-02, RECOV-03, PROMPT-01, PROMPT-02, PROMPT-03
- `.planning/ROADMAP.md` — Phase 69 成功标准（5 条）

### 源代码（直接修改文件）
- `backend/core/agent_service.py` — step_callback 内联定义（lines 175-346），apply_dom_patch() 调用（line 357）
- `backend/agent/prompts.py` — ENHANCED_SYSTEM_MESSAGE，Section 9 当前内容（lines 52-83）

### 源代码（参考/调用方 — 不修改但需理解）
- `backend/agent/dom_patch.py` — update_failure_tracker() (lines 168-186), reset_failure_tracker() (lines 189-192), _failure_tracker (line 41)
- `backend/agent/stall_detector.py` — detect_failure_mode() (lines 162-221), FailureDetectionResult (lines 39-49), StallDetector.check() (lines 76-101)

### 前序 Phase 上下文
- `.planning/phases/67-基础层-行标识检测与失败追踪状态/67-CONTEXT.md` — 基础层设计决策
- `.planning/phases/68-dom-patch/68-CONTEXT.md` — DOM Patch 增强设计决策，标注格式、策略层级命名

### Phase 48 设计参考（模式参考）
- `.planning/phases/48-agent/48-CONTEXT.md` — StallDetector/PreSubmitGuard 设计决策，frozen dataclass 模式

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `StallDetector.detect_failure_mode()` — 已定义但从未调用，签名 `(action_name, target_index, evaluation, dom_hash_before, dom_hash_after) -> FailureDetectionResult`
- `dom_patch.update_failure_tracker()` — 已定义但从未调用，签名 `(backend_node_id, error, mode) -> None`
- `dom_patch.reset_failure_tracker()` — 已定义且每 run 通过 apply_dom_patch() 调用
- `_failure_tracker` — 模块级字典，dom_patch.py 内部读取用于策略降级和失败标注注入

### Established Patterns
- step_callback 是 agent_service.py 中的内联闭包，通过 `register_new_step_callback=step_callback` 注册
- 检测器在 step_callback 中调用，结果存入 `_pending_interventions` 列表
- 日志使用 Python logging 模块，category="monitor" 用于检测器日志
- frozen=True dataclass 用于返回值
- 模块级变量用于状态共享（`_PATCHED` / `_failure_tracker` 模式）

### Integration Points
- `agent_service.py` step_callback (lines 302-337) — 当前检测器调用区域，新增 detect_failure_mode + update_failure_tracker
- `agent_service.py` run_with_streaming() — dom_hash 计算在 line ~290，step_callback 定义在 line ~175
- `prompts.py` ENHANCED_SYSTEM_MESSAGE — Section 9 在 line 52-83，新规则追加到 line 83 之后
- `dom_patch.py` — _failure_tracker 被 Patch 4 wrapper 和 serialize_tree annotations 读取

### Critical Gap
- `update_failure_tracker()` 从未被调用 → Phase 68 的策略降级逻辑当前是 inert（空转）
- `detect_failure_mode()` 从未被调用 → 失败模式检测逻辑当前是 inert
- Phase 69 的核心价值：激活这两个函数，让整个检测→标注→降级链路真正工作

</code_context>

<specifics>
## Specific Ideas

- step_callback 中 detect_failure_mode() 需要闭包变量存储上一步 dom_hash（`_prev_dom_hash = None` 初始化）
- detect_failure_mode() 的 target_index 参数对应 action_params.get("index")，backend_node_id 需从 browser_state 的 selector_map 获取
- Section 9 新规则标题参考：9.1 行标识定位、9.2 反重复操作、9.3 策略优先级、9.4 失败恢复
- 失败关键词筛选条件：evaluation 中包含 '失败'/'wrong'/'error'/'无法'/'不成功'/'未'

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---
*Phase: 69-prompt*
*Context gathered: 2026-04-07*
