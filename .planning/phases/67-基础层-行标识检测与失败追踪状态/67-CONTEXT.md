# Phase 67: 基础层 — 行标识检测与失败追踪状态 - Context

**Gathered:** 2026-04-06
**Status:** Ready for planning

<domain>
## Phase Boundary

在 DOM Patch 和 StallDetector 中建立三项基础能力：
1. `_detect_row_identity()` — 从 ERP 表格行中检测行标识（IMEI/商品编号）
2. `_failure_tracker` 状态管理 — 失败追踪字典 + update/reset 函数
3. `detect_failure_mode()` — 失败模式检测器，识别三种 ERP 表格交互失败

**不包含：**
- 行标识注释注入（Phase 68 — DOM Patch 增强）
- 策略标注注入（Phase 68）
- step_callback 集成调用（Phase 69）
- Section 9 Prompt 规则追加（Phase 69）
- 恢复 headed 模式
- 移除现有 DOM Patch 或 Section 9 内容

</domain>

<decisions>
## Implementation Decisions

### _failure_tracker 键策略
- **D-01:** 以 `backend_node_id` 为键，与 browser-use `_selector_map` 一致。简单直接，不引入复合键复杂度。若 Phase 68/69 集成时发现跨 step 不稳定，再切换为复合键 `(tag_name, placeholder, row_identity)`
  - **Why:** STATE.md blocker 指出 backend_node_id 跨 step 稳定性未验证，但过早优化复合键会增加实现复杂度
  - **How to apply:** planner 使用 backend_node_id 为键；若集成测试发现问题，agent_service.py 中的调用点需适配复合键

### FailureDetectionResult 结构
- **D-02:** 新增 `FailureDetectionResult` frozen dataclass，与 `StallResult` 平级。字段：`failure_mode: str | None`（None 表示无失败）、`details: dict`（诊断信息，如匹配到的关键词、hash 比对结果）。遵循 Phase 48 frozen=True 不可变模式
  - **Why:** Phase 48 确立 frozen dataclass 为检测器返回值的标准模式
  - **How to apply:** detect_failure_mode() 返回此结构；details 字典内容因模式而异，下游 planner/executor 可灵活消费

### 检测集成方式
- **D-03:** `detect_failure_mode()` 作为 StallDetector 的独立方法，与 `check()` 平级。签名：`detect_failure_mode(action_name, target_index, evaluation, dom_hash_before, dom_hash_after) -> FailureDetectionResult`。`check()` 保持不变
  - **Why:** 职责分离——check() 检测停滞，detect_failure_mode() 检测失败模式。独立方法避免扩大 check() 的职责范围
  - **How to apply:** step_callback 每步调用完 check() 后再调用 detect_failure_mode()，传入前后两步的 hash

### 测试策略
- **D-04:** 纯单元测试（mock），与 Phase 48 策略一致。backend_node_id 在 mock 中假设为稳定。覆盖 >= 80%
  - **Why:** Phase 48 确立纯单元测试为检测器测试标准；backend_node_id 稳定性验证留给 Phase 68/69 集成阶段
  - **How to apply:** mock SimplifiedNode 和 AccessibilityNode 测试 _detect_row_identity；mock step 参数测试 detect_failure_mode；dict 操作测试 _failure_tracker

### Claude's Discretion
- `_detect_row_identity()` 的具体 DOM 遍历实现（复用 _is_textual_td_cell 模式或新写）
- `update_failure_tracker()` 的参数签名（是否包含 mode 参数或从 evaluation 推断）
- `FailureDetectionResult.details` 的具体字段名
- 单元测试的 mock 数据设计
- 失败模式关键词列表的具体内容

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase 66 设计文档（核心输入）
- `.planning/milestones/v0.8.3-phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md` — 四项优化完整设计，含 OPTIMIZE-01~04 规则表、代码任务清单 T01-T16
- `.planning/milestones/v0.8.3-phases/66-优化方案设计/66-CONTEXT.md` — Phase 66 设计决策 D-01~D12

### 源代码（直接修改文件）
- `backend/agent/dom_patch.py` — DOM Patch 5 patches 实现，新增 _detect_row_identity / _failure_tracker / update_failure_tracker / reset_failure_tracker 在此文件
- `backend/agent/stall_detector.py` — StallDetector 类，新增 detect_failure_mode() 和 FailureDetectionResult 在此文件

### 源代码（参考/调用方）
- `backend/agent/monitored_agent.py` — create_step_callback()，Phase 69 集成调用点参考
- `backend/core/agent_service.py` — apply_dom_patch() 调用入口（line 357），step_callback detector calls 区域（line 302-337）

### Phase 48 设计参考（模式参考）
- `.planning/phases/48-agent/48-CONTEXT.md` — StallDetector/PreSubmitGuard 设计决策，frozen dataclass 模式，纯单元测试策略

### 需求与路线图
- `.planning/REQUIREMENTS.md` — v0.8.4 需求 ROW-01, ANTI-01, RECOV-01
- `.planning/ROADMAP.md` — Phase 67 成功标准（4 条）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `dom_patch.py` monkey-patch 模式 — 新函数遵循：保存原始方法 → 包装 → 替换。`apply_dom_patch()` 是统一注册入口
- `_is_textual_td_cell()` — 已实现 td 文本检测逻辑（通过 original_node.get_all_children_text()），_detect_row_identity 可复用此 DOM 遍历模式
- `_is_inside_table_cell()` — 已实现 td/th 父级遍历（通过 parent_node 链），可用于行级遍历的参考
- `_ERP_TABLE_CELL_PLACEHOLDERS` — 已定义 ERP 字段 placeholder 列表（frozenset）
- `StallDetector` frozen dataclass 模式 — StallResult 使用 frozen=True，_StepRecord 为内部状态

### Established Patterns
- frozen=True dataclass 用于返回值（Phase 48 D-05）
- 模块级变量用于状态共享（`_PATCHED` 模式）— `_failure_tracker` 遵循此模式
- 检测器实例每次 run 创建新实例（Phase 48 D-04 / PROJECT.md）
- 日志使用 Python logging 模块，category="monitor" 用于检测器日志
- 文件命名：snake_case，类名 PascalCase

### Integration Points
- `apply_dom_patch()` — reset_failure_tracker() 在此函数中被调用（每次 run 开始时重置），但独立于 _PATCHED 幂等保护
- `stall_detector.py` — detect_failure_mode() 新增到 StallDetector 类中
- Phase 69 集成点：step_callback 将调用 update_failure_tracker() 和 detect_failure_mode()

</code_context>

<specifics>
## Specific Ideas

- _detect_row_identity 核心思路：遍历 tr 的子 td，对每个 td 的 get_all_children_text() 应用正则 `I\d{15}` 匹配，返回第一个匹配的字符串
- _failure_tracker 数据结构：`dict[str, dict]`，键为 backend_node_id（字符串），值为 `{"count": int, "last_error": str, "mode": str}`
- 三种失败模式检测逻辑：
  - click_no_effect: dom_hash_before == dom_hash_after 且 action_name == "click"
  - wrong_column: evaluation 包含 "wrong column"/"错误列"/"误点"/"非目标列" 关键词
  - edit_not_active: action_name == "input" 且 evaluation 包含 "not editable"/"无法输入"/"元素不可操作" 关键词

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---
*Phase: 67-基础层-行标识检测与失败追踪状态*
*Context gathered: 2026-04-06*
