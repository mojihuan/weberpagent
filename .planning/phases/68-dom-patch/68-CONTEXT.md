# Phase 68: DOM Patch 增强 — 行标识注入与策略标注 - Context

**Gathered:** 2026-04-07
**Status:** Ready for planning

<domain>
## Phase Boundary

DOM dump 序列化输出增强：注入行标识注释、策略层级标注、失败动态标注，让 Agent 能锁定目标行、选择正确交互策略、避免重复失败操作。

**三个 Plan 范围：**
- 68-01: Patch 4 增强 — 在 index 分配阶段添加行归属和策略判定
- 68-02: Patch 6 — 行标识注释注入（`<!-- 行: {id} -->`）
- 68-03: Patch 7 — 失败动态标注注入（基于 _failure_tracker）

**不包含：**
- step_callback 集成调用（Phase 69）
- Section 9 Prompt 规则追加（Phase 69）
- backend_node_id 稳定性验证（Phase 69）
- 恢复 headed 模式
- 移除现有 DOM Patch 或 Section 9 内容

</domain>

<decisions>
## Implementation Decisions

### 序列化注入架构
- **D-01:** 两阶段注入：(1) 树构建阶段在 Patch 4 wrapper 中为 input 元素设置内部属性（行归属、策略层级），(2) 新增 Patch 包裹序列化输出方法，在生成 DOM dump 文本时注入 HTML 注释
  - **Why:** 职责分离 — Patch 4 负责判定逻辑，Patch 6/7 负责文本注入。避免单一 wrapper 过度膨胀
  - **How to apply:** Patch 4 wrapper 扩展为设置 `node._row_identity` 和 `node._strategy_level` 等临时属性；Patch 6 包裹序列化方法注入行标识注释；Patch 7 包裹序列化方法注入失败标注

### 标注格式
- **D-02:** 统一使用 HTML 注释格式，Agent 可直接在 DOM dump 文本中识别
  - 行标识注释：`<!-- 行: I01784004409597 -->`（在含商品编号的 `<tr>` 上方）
  - 行归属+策略：`<!-- 行内 input [行: I01784004409597] [策略: 2-需先 click] -->`（只在已失败元素上显示）
  - 失败标注：`<!-- 已尝试 2 次 [模式: click_no_effect]，建议切换策略 -->`（只在已失败元素上显示）
  - **Why:** 注释格式不干扰 DOM 结构，Agent 自然语言理解可识别
  - **How to apply:** 序列化包裹方法扫描已标注属性的节点，在对应位置插入注释文本

### 策略层级命名
- **D-03:** 描述性命名：
  - 策略1-原生 input：可见 input 元素，直接 input 操作
  - 策略2-需先 click：hidden input（Ant Design click-to-edit），先 click td 再 input
  - 策略3-evaluate JS：兜底策略，evaluate JS 直接操作 DOM
  - **Why:** 描述性命名让 Agent 看注释即懂操作方式，无需额外规则解释
  - **How to apply:** Patch 4 判定逻辑使用数字 1/2/3 内部标识，序列化时映射为描述性文字

### 标注显示策略
- **D-04:** 策略标注和失败标注只在已失败元素上显示（_failure_tracker 中有记录的元素）。未失败元素不显示任何策略/失败信息。行标识注释（`<!-- 行: {id} -->`）对所有含商品编号的行都显示（非失败驱动）
  - **Why:** Phase 66 决策 — 避免未失败元素显示策略标注导致 Agent 偏向 evaluate JS
  - **How to apply:** Patch 7 注入失败标注时先检查 _failure_tracker 是否有该 backend_node_id 的记录

### backend_node_id 稳定性
- **D-05:** Phase 68 假设 backend_node_id 跨 step 稳定，不做复合键回退实现。稳定性验证留给 Phase 69 集成阶段。若 Phase 69 发现不稳定，再切换为复合键 `(tag_name, placeholder, row_identity)`
  - **Why:** STATE.md blocker 标记的风险。Phase 67 已用 mock 假设稳定，Phase 68 继续此假设，避免过早优化
  - **How to apply:** planner 使用 backend_node_id 关联 _failure_tracker；若集成测试发现问题，在 Phase 69 适配

### Claude's Discretion
- Patch 4 wrapper 的具体扩展方式（如何设置 _row_identity 和 _strategy_level 属性）
- 序列化方法包裹的具体实现（哪个方法、注入位置）
- 策略判定的具体条件（snapshot_node 存在性检查的具体属性名）
- Patch 6 和 Patch 7 的注册顺序和依赖关系
- 单元测试的 mock 数据设计

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase 66 设计文档（核心输入）
- `.planning/milestones/v0.8.3-phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md` — 四项优化完整设计，含 OPTIMIZE-01~04 规则表、代码任务清单 T01-T16
- `.planning/milestones/v0.8.3-phases/66-优化方案设计/66-CONTEXT.md` — Phase 66 设计决策 D-01~D12

### 源代码（直接修改文件）
- `backend/agent/dom_patch.py` — DOM Patch 5 patches 实现 + Phase 67 新增的 _detect_row_identity / _failure_tracker / update_failure_tracker / reset_failure_tracker
- `backend/agent/stall_detector.py` — StallDetector + FailureDetectionResult（Phase 67 已实现）

### 源代码（参考/调用方）
- `backend/core/agent_service.py` — apply_dom_patch() 调用入口（line 357），step_callback detector calls 区域（line 302-337）

### 前序 Phase 上下文
- `.planning/phases/67-基础层-行标识检测与失败追踪状态/67-CONTEXT.md` — Phase 67 设计决策（_failure_tracker 键策略、FailureDetectionResult 结构、检测集成方式）

### 需求与路线图
- `.planning/REQUIREMENTS.md` — v0.8.4 需求 ROW-02, ROW-03, STRAT-01, STRAT-02, STRAT-03, ANTI-02
- `.planning/ROADMAP.md` — Phase 68 成功标准（5 条）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `_detect_row_identity(node)` — Phase 67 已实现，从 tr 的子 td 文本中提取 IMEI 格式行标识。68-02 直接调用
- `_failure_tracker: dict[str, dict]` — Phase 67 已实现，以 backend_node_id 为键。68-03 读取此状态
- `update_failure_tracker()` / `reset_failure_tracker()` — Phase 67 已实现。Phase 69 集成调用
- `_patch_assign_interactive_indices()` — 当前 Patch 4 wrapper，68-01 扩展此 wrapper
- `_is_textual_td_cell()` — DOM 遍历模式（original_node.get_all_children_text()）
- `_is_inside_table_cell()` — td/th 父级遍历（parent_node 链）
- `_is_erp_table_cell_input()` — ERP input 检测（placeholder 匹配）
- `_ERP_TABLE_CELL_PLACEHOLDERS` — ERP 字段 placeholder 列表

### Established Patterns
- monkey-patch 模式：保存原始方法 → 包装 → 替换（dom_patch.py 全文件遵循）
- 模块级变量用于状态共享（`_PATCHED` / `_failure_tracker` 模式）
- frozen=True dataclass 用于返回值（Phase 48/67）
- apply_dom_patch() 是统一注册入口，所有 patch 在此注册
- reset_failure_tracker() 独立于 _PATCHED 幂等保护（每次 run 都重置）

### Integration Points
- `apply_dom_patch()` — 注册新 Patch 6 和 Patch 7，且调用 reset_failure_tracker()
- `_patch_assign_interactive_indices()` — 68-01 扩展此 wrapper 添加行归属和策略判定
- Phase 69 集成点：step_callback 调用 update_failure_tracker() 和 detect_failure_mode()
- Phase 69 集成点：Section 9 追加注释使用说明

</code_context>

<specifics>
## Specific Ideas

- Patch 4 增强思路：在现有 `_is_erp_table_cell_input()` 检测后，增加行归属判定（调用 `_detect_row_identity()`）和策略层级判定（检查 snapshot_node 存在性）。将判定结果存储为节点的临时属性
- Patch 6 思路：新增 monkey-patch 包裹序列化输出方法，扫描 DOM 树中含行标识的 `<tr>` 节点，在其序列化文本前注入 `<!-- 行: {id} -->` 注释
- Patch 7 思路：新增 monkey-patch 包裹序列化输出方法，读取 `_failure_tracker`，为已失败元素的序列化文本注入策略降级和失败模式标注。只在 _failure_tracker 有记录的元素上注入
- 三个 patch 的注册顺序：Patch 6（行标识）先于 Patch 7（失败标注），因为失败标注可能需要引用行标识

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---
*Phase: 68-dom-patch*
*Context gathered: 2026-04-07*
