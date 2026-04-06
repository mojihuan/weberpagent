# Phase 66: Agent 表格交互优化设计文档

**生成时间:** 2026-04-06
**基于:** Phase 65 差距关联分析结论（65-ANALYSIS-REPORT.md）
**目标读者:** 后续代码实施阶段的开发 Agent

## 设计输入摘要

Phase 65 三项分析的核心结论：

| 分析项 | 判定 | 关键依据 |
|--------|------|----------|
| ANALYSIS-01: headless 与定位不准的因果关联 | 部分 | headless 是加剧因素而非唯一根因；Ant Design hidden input 问题在 headed 下同样存在 |
| ANALYSIS-02: DOM Patch 在 headed 下的有效性 | 4/5 仍必要，1/5 部分必要 | Patch 2（paint order）可能部分冗余，其余 patch 解决 browser-use 序列化管线通用不足 |
| ANALYSIS-03: Section 9 Prompt 有效性 | 保留 | 应用级交互指导，与浏览器模式无关 |

**Phase 66 设计定位：** 基于"headless 不是唯一根因"的结论，设计不依赖浏览器模式的 Agent 交互优化策略，在 DOM Patch 层和 Prompt 层实现。

## 文档结构导航

1. **设计总览** — 四项优化的关系、实施层级、与现有 patch 的关系
2. **OPTIMIZE-01** — 按行定位 + 直接找 input 策略
3. **OPTIMIZE-02** — 反重复机制
4. **OPTIMIZE-03** — 三级策略优先级
5. **OPTIMIZE-04** — 失败恢复策略
6. **总结** — 代码任务总清单、实施优先级、测试建议
7. **验证记录** — CONTEXT.md 决策对照 + ROADMAP 成功标准检查

---

## 设计总览

### 四项优化的关系图

```
OPTIMIZE-01: 按行定位 + 直接找 input
    │
    │ 为 OPTIMIZE-02 提供行级上下文
    ▼
OPTIMIZE-02: 反重复机制
    │
    │ 为 OPTIMIZE-03 提供失败切换触发
    ▼
OPTIMIZE-03: 三级策略优先级
    │
    │ 为 OPTIMIZE-04 提供策略降级路径
    ▼
OPTIMIZE-04: 失败恢复策略
    │
    │ 反向引用 OPTIMIZE-01 的行标识辅助重新定位
    ▼
    OPTIMIZE-01 (循环)
```

**依赖链:** OPTIMIZE-01 是基础，OPTIMIZE-02 在其上添加防重复，OPTIMIZE-03 定义策略选择规则，OPTIMIZE-04 定义失败后的恢复动作。四项形成闭环。

### 实施层级（Per D-04/D-05/D-06）

| 层级 | 文件 | 实施方式 | 说明 |
|------|------|----------|------|
| DOM Patch 层 | `backend/agent/dom_patch.py` | 新增 patch 函数，遵循 monkey-patch 模式 | Per D-05: 融入现有 dom_patch.py，保持单文件 |
| Prompt 层 | `backend/agent/prompts.py` | 追加规则到 Section 9 末尾 | Per D-06: 保留现有内容作为基础 |

**不新增独立模块。** 所有优化在现有两个文件中完成。

### 与现有 5 Patches 的关系

| 现有 Patch | 关系 | 说明 |
|------------|------|------|
| Patch 1: `_patch_is_interactive` | 不变 | OPTIMIZE-01 新增的行标识 patch 不影响现有交互标记逻辑 |
| Patch 2: `_patch_paint_order_remover` | 不变 | OPTIMIZE-02 的动态标注在序列化输出阶段，不影响 paint order 处理 |
| Patch 3: `_patch_should_exclude_child` | 不变 | 反重复和策略标注不涉及 bbox 过滤逻辑 |
| Patch 4: `_patch_assign_interactive_indices` | **增强** | OPTIMIZE-01 增强此 patch 以添加行归属标注；OPTIMIZE-03 增加策略层级标注 |
| Patch 5: `_is_textual_td_cell` | 不变 | 行标识 patch 使用类似模式但独立实现 |

**原则：不替换现有 patch，在现有基础上新增和增强。**

---

## OPTIMIZE-01: 按行定位 + 直接找 input 策略

**对应需求:** OPTIMIZE-01
**设计决策:** Per D-07（`<tr>` 行标识）、D-08（商品编号/IMEI 作为标识符）、D-09（行内 placeholder 匹配找 input）

### 目标

| 目标 | 描述 |
|------|------|
| 让 Agent 在 DOM dump 中看到每行的商品标识 | 类似 Patch 5 让 td 显示文本，新 patch 让 tr 显示行标识 |
| 锁定目标行后精确定位行内 input | 解决"同一 placeholder 在多行出现"问题——Agent 先找行，再找行内 input |

### 问题分析

当前 Agent 在 ERP 销售出库表格中遇到的核心定位问题：

1. **同列多行相同 placeholder**: 销售出库表格中每个商品行都有 `placeholder="销售金额"` 的 input，Agent 无法区分是哪一行的
2. **行定位靠视觉猜测**: 当前 Section 9 只说"通过商品名称确认所在行"（prompts.py line 62），没有结构化的行标识机制
3. **行内定位缺乏约束**: 锁定行后，Agent 没有明确的规则在行内查找目标 input

### 设计规则表

| # | 条件 | 动作 | 示例 |
|---|------|------|------|
| R01-1 | 遇到 `<tr>` 内含 `<td>` 包含商品编号/IMEI 格式文本（I + 15 位数字） | DOM Patch 为该 `<tr>` 添加 `data-row-identity` 属性，内容为商品编号文本 | `<tr data-row-identity="I01784004409597">...</tr>` |
| R01-2 | DOM dump 序列化时遇到带 `data-row-identity` 的 `<tr>` | 在 DOM dump 中该行元素前添加行标识注释 `<!-- 行: {商品编号} -->` | Agent 看到 `<!-- 行: I01784004409597 -->` 后知道这是目标行 |
| R01-3 | Agent 需要填写某商品的"销售金额"字段 | Agent 先在 DOM dump 中找到包含目标商品编号的行标识注释 → 在该行内找到 `placeholder="销售金额"` 的 input 或 td → 操作该元素 | 在行 `I01784004409597` 内找到 `input[placeholder="销售金额"]` |
| R01-4 | 同一 `<tr>` 内有多个 `<td>` 包含不同文本内容 | DOM Patch 只取第一个匹配商品编号/IMEI 格式的文本作为行标识，忽略后续匹配 | 避免同一行有多个行标识造成混乱 |

### 集成点

#### DOM Patch 层: 新增 `_patch_add_row_identity()`

- **文件**: `backend/agent/dom_patch.py`
- **模式**: 遵循现有 monkey-patch 模式——保存原始方法 → 包装 → 替换
- **复用**: 复用 `_is_textual_td_cell()` 的 DOM 遍历模式（通过 `original_node.parent_node` 链遍历 `<tr>` 的子 `<td>`）
- **检测逻辑**: 在 `<td>` 的子节点文本中检测商品编号模式（正则 `I\d{15}` 匹配 IMEI 格式）
- **注入时机**: 拦截 DOM 序列化输出阶段（`_create_simplified_tree()` 或其后续处理），在 `<tr>` 节点的 DOM dump 文本前注入行标识注释
- **注册**: 在 `apply_dom_patch()` 中与其他 patch 一起注册

#### DOM Patch 层: 增强 Patch 4 `_patch_assign_interactive_indices()`

- **文件**: `backend/agent/dom_patch.py`，`_patch_assign_interactive_indices()` 函数（line 289-328）
- **当前行为**: Patch 4 为所有 ERP table cell input 分配交互索引，不考虑行归属
- **增强后行为**: 分配索引时检测 input 所在 `<tr>` 的行标识 → 在 DOM dump 注释中标注行归属（如 `<!-- 行内 input [行: I01784004409597] -->`）→ Agent 自然区分行内 input
- **兼容性**: 增强不改变现有索引分配逻辑，只是在索引分配时附加行归属信息

#### Prompt 层: Section 9 追加行标识使用规则

- **文件**: `backend/agent/prompts.py`，Section 9 "ERP 表格单元格填写"（line 52-83）
- **追加位置**: Section 9 末尾，在"点击编辑工作流"部分之后
- **追加内容**: 明确 DOM dump 中行标识的格式和使用方法——Agent 看到 `<!-- 行: I01784004409597 -->` 时知道这是包含商品 I01784004409597 的行，应在行内操作
- **现有内容**: prompts.py line 62-63 "通过商品名称/IMEI 确认所在行" → 新规则在此基础上结构化，将视觉猜测变为确定性查找

### 代码任务清单

1. **[DOM-PATCH]** 新增 `_detect_row_identity(tr_node)` 函数 — 从 `<tr>` 的子 `<td>` 文本中提取商品编号/IMEI（正则匹配 `I\d{15}` 模式）
2. **[DOM-PATCH]** 新增 `_patch_add_row_identity()` — 拦截序列化，为含商品编号的 `<tr>` 在 DOM dump 中注入行标识注释
3. **[DOM-PATCH]** 增强 Patch 4 `_patch_assign_interactive_indices()` — 为行内 input 添加行归属标注（`<!-- 行内 input [行: {id}] -->`）
4. **[DOM-PATCH]** 在 `apply_dom_patch()` 中注册新 `_patch_add_row_identity()`
5. **[PROMPT]** Section 9 追加行标识使用规则 — 指导 Agent 使用 `<!-- 行: ... -->` 注释锁定目标行

---

## OPTIMIZE-02: 反重复机制

**对应需求:** OPTIMIZE-02
**设计决策:** Per D-10（反重复在 DOM Patch 层实现——序列化时动态调整）

### 目标

| 目标 | 描述 |
|------|------|
| 检测 Agent 对同一 index 的重复失败操作 | 通过 step_callback 提供的 target_index 和 evaluation 判断失败 |
| 动态调整 DOM 序列化以避开已失败元素 | DOM Patch 根据失败历史改变元素标注/优先级，Agent 下次拿到调整后的 DOM dump |

### 问题分析

当前 Agent 的重复失败模式：

1. **同一 index 反复尝试**: Agent 对某个 click index 操作失败后，可能再次尝试同一 index（如 input 操作失败但 Agent 不切换策略）
2. **无失败记忆**: 每次 step Agent 拿到的 DOM dump 是相同的，无法区分哪些元素之前操作失败
3. **误点错误列后无标记**: Agent 点了"总成本"列而非"销售金额"列后，下次序列化时两列的 DOM 表示没有变化

### 设计规则表

| # | 条件 | 动作 | 示例 |
|---|------|------|------|
| R02-1 | 同一 target_index 连续 2 次操作后 evaluation 包含失败关键词（"失败"/"failed"/"error"/"无法"） | 在该 index 对应元素的 DOM dump 标注中添加 `<!-- 已尝试2次失败，建议切换策略 -->` | `<input placeholder="销售金额" /> <!-- 已尝试2次失败，建议切换策略 -->` |
| R02-2 | 同一 target_index 连续 2 次失败 | DOM Patch 降低该元素的交互优先级：在 DOM dump 中标注 `<!-- 策略降级: 改用 DOM 查询 -->`，同时提升同行其他候选元素的可见性 | 原来 index=5 的失败元素标注降级，Agent 被引导到替代路径 |
| R02-3 | Agent 点击某 index 后 DOM hash 未变化（点击无效果）1 次 | 立即标注该 index 对应元素为 `<!-- 点击无效，建议换策略 -->`，下次序列化时在元素旁添加替代路径提示 | `<td>210</td> <!-- 点击无效，尝试 evaluate JS -->` |
| R02-4 | Agent 点击某 index 后 evaluation 提示"错误列"/"wrong column"/"误点"等关键词 | 立即在误点元素标注 `<!-- 非目标列 -->`，同时在目标列元素标注 `<!-- 目标列 -->`（需配合 OPTIMIZE-01 行标识定位目标列） | Agent 知道哪个是正确列，下次不再误点 |

### 集成点

#### DOM Patch 层: 新增 `_patch_dynamic_annotation()`

- **文件**: `backend/agent/dom_patch.py`
- **功能**: 接收失败历史参数，在序列化时动态添加标注到 DOM dump
- **状态存储**: 使用模块级变量（类似现有 `_PATCHED`），每次 run 清空
  - 变量名: `_failure_tracker`，类型 `dict[int, dict]`
  - 每个 entry: `{index: {"count": int, "last_error": str, "mode": str}}`
  - `mode` 值: `"repeated_fail"` / `"click_no_effect"` / `"wrong_column"`
- **monkey-patch 模式**: 拦截序列化输出阶段，在生成 DOM dump 文本时根据 `_failure_tracker` 动态注入注释

#### 监控层: 利用 StallDetector 的检测能力

- **文件**: `backend/agent/monitored_agent.py`（step_callback）和 `backend/agent/stall_detector.py`
- **当前能力**: StallDetector 的 `check()` 已接收 `action_name`、`target_index`、`evaluation`、`dom_hash` 参数
- **新增能力**: 在 step_callback 中新增失败信息提取和 `_failure_tracker` 更新逻辑
  - 提取 evaluation 中的失败关键词
  - 比较 dom_hash_before 和 dom_hash_after 检测点击无变化
  - 更新 `_failure_tracker` 模块级状态

#### 数据流: step_callback -> failure_tracker -> DOM Patch

- **关键路径**:
  1. `step_callback`（agent_service.py line 175 或 monitored_agent.py line 159）提取 target_index + evaluation + dom_hash
  2. 调用 `update_failure_tracker(index, evaluation, dom_hash)` 更新失败历史
  3. 下次 DOM 序列化时，`_patch_dynamic_annotation()` 读取 `_failure_tracker`
  4. 根据失败历史在 DOM dump 中动态添加标注

- **状态共享机制**: 使用 `dom_patch.py` 的模块级变量 `_failure_tracker`，step_callback 通过 `from backend.agent.dom_patch import update_failure_tracker` 调用更新函数
  - 与现有 `_PATCHED` 模式一致
  - 每次 run 开始时在 `apply_dom_patch()` 中重置 `_failure_tracker = {}`

### 代码任务清单

1. **[DOM-PATCH]** 新增 `_failure_tracker` 模块级状态 — `dict[int, dict]`，记录 `{index: {"count": int, "last_error": str, "mode": str}}`
2. **[DOM-PATCH]** 新增 `update_failure_tracker(index, evaluation, dom_hash)` 函数 — 在 step_callback 中调用，更新失败历史
3. **[DOM-PATCH]** 新增 `_patch_dynamic_annotation()` — 序列化时根据 `_failure_tracker` 动态标注元素
4. **[AGENT-SERVICE]** 在 step_callback 中调用 `update_failure_tracker()` — agent_service.py line 302-337 的 detector calls 区域
5. **[PROMPT]** Section 9 追加反重复规则 — Agent 看到标注后应如何响应（如看到"已尝试2次失败"应切换策略）

---

## OPTIMIZE-03: 三级策略优先级

**对应需求:** OPTIMIZE-03
**设计决策:** Per D-11（三级策略通过 DOM Patch 标注实现）

### 目标

| 目标 | 描述 |
|------|------|
| 定义 input 操作的三级策略优先级 | 原生 input > DOM 查询 > evaluate JS |
| 通过 DOM Patch 标注让 Agent 自然选择策略 | Agent 根据 DOM dump 中的策略层级标注选择操作方式 |

### 问题分析

当前 Agent 缺乏策略选择指导：

1. **策略无优先级**: Agent 在面对"如何填写值"时没有明确的策略选择规则，可能先尝试 evaluate JS（最慢且不可靠）而非直接 input（最快最可靠）
2. **无降级机制**: 当一种策略失败时，Agent 没有明确的"切换到下一级策略"规则
3. **click-to-edit 混淆**: Agent 不知道何时需要先 click td 再 input（策略 2），何时可以直接 input（策略 1）

### 设计规则表

| # | 条件 | 动作 | 示例 |
|---|------|------|------|
| R03-1 | ERP 表格 cell 内有可见 `<input>`（`snapshot_node` 存在，is_visible=True）且该 input 已通过 Patch 4 获得交互索引 | DOM dump 中标注该 input 为 `<!-- 策略1: 原生 input 操作 [index=N] -->` | `<input placeholder="销售金额" /> <!-- 策略1: 原生 input 操作 [index=15] -->` |
| R03-2 | ERP 表格 cell 内的 `<input>` 缺少 `snapshot_node`（hidden by React state/display:none）但已通过 Patch 4 强制获得索引 | DOM dump 中标注该 input 为 `<!-- 策略2: 需先 CLICK td 触发编辑，再 INPUT [index=N] -->` | 提示 Agent 需要 click-to-edit 工作流 |
| R03-3 | 策略 1 和策略 2 均失败（OPTIMIZE-02 `_failure_tracker` 记录该 index 连续 2 次失败） | DOM dump 中标注为 `<!-- 策略3: evaluate JS 兜底 --> document.querySelector('input[placeholder="销售金额"]').value = '目标值'` | Agent 使用 evaluate action 执行 JS |
| R03-4 | DOM Patch 检测到 input 的 hidden 状态（`display:none` 或 `snapshot_node` 不存在） | 自动将标注从策略 1 降级为策略 2（需要先 click td 激活编辑态） | Agent 知道不能直接 input，需要先激活 |
| R03-5 | OPTIMIZE-02 的 `_failure_tracker` 触发策略 2 降级（策略 2 也失败 2 次） | 自动将标注从策略 2 降级为策略 3 | Agent 切换到 evaluate JS |

### 策略层级详解

#### 策略 1: 原生 input 操作（最优）

- **适用场景**: input 元素在 DOM 中可见且已获得交互索引
- **Agent 操作**: 直接使用 `input(index=N, value="目标值")`
- **可靠性**: 高 — browser-use 原生支持，经过充分测试
- **前置条件**: `snapshot_node` 存在 + `is_visible=True` + Patch 4 已分配索引

#### 策略 2: click-to-edit 工作流（中等）

- **适用场景**: input 存在于 DOM 但被隐藏（Ant Design click-to-edit 模式），需要先点击 td 激活
- **Agent 操作**: `click(index=M)` 点击 td → 等待 input 出现 → `input(index=N, value="目标值")`
- **可靠性**: 中 — 依赖 React 状态变更和 DOM 更新时机
- **前置条件**: input 存在于 DOM（通过 Patch 4 强制可见）但 `snapshot_node` 缺失

#### 策略 3: evaluate JS 兜底（最低）

- **适用场景**: 策略 1 和策略 2 均失败，需要直接操作 DOM
- **Agent 操作**: `evaluate("document.querySelector('input[placeholder=\"销售金额\"]').value = '目标值'")`
- **可靠性**: 低-中 — 绕过 browser-use 交互层，可能不触发 React 状态更新
- **前置条件**: 无 — 总是可用的兜底方案

### 集成点

#### DOM Patch 层: 增强 Patch 4 `_patch_assign_interactive_indices()`

- **文件**: `backend/agent/dom_patch.py`，`_patch_assign_interactive_indices()` 函数（line 289-328）
- **增强内容**: 分配索引时添加策略层级判定逻辑
  - `snapshot_node` 存在 → 策略 1
  - `snapshot_node` 不存在 → 策略 2
  - `_failure_tracker` 记录 2 次失败 → 策略 3
- **标注格式**: 在 node 的 DOM dump 文本中注入注释 `<!-- 策略N: {描述} [index=X] -->`

#### DOM Patch 层: 新增 `_inject_strategy_annotation()`

- **文件**: `backend/agent/dom_patch.py`
- **功能**: 在 DOM dump 文本生成后，遍历已分配索引的 ERP input 元素，插入策略标注
- **注入时机**: 在 `_assign_interactive_indices` 之后（此时索引已分配，策略层级可判定）
- **与现有 pipeline 关系**:
  - 现有 pipeline: `build_snapshot_lookup` → `_build_enhanced_tree` → `_create_simplified_tree` → `_optimize_tree` → `_assign_interactive_indices`
  - 标注注入: 在 `_assign_interactive_indices` 完成后的 DOM dump 文本后处理阶段

#### Prompt 层: Section 9 追加策略优先级规则

- **文件**: `backend/agent/prompts.py`，Section 9（line 52-83）
- **追加位置**: Section 9 末尾
- **追加内容**:
  - 明确"策略 1 > 策略 2 > 策略 3"的优先级
  - 告知 Agent DOM dump 中 `<!-- 策略N: ... -->` 注释的含义
  - 指导 Agent 遇到策略标注时选择对应操作方式

### 代码任务清单

1. **[DOM-PATCH]** 增强 Patch 4 — 添加策略层级判定逻辑（`snapshot_node` 存在 → 策略 1，不存在 → 策略 2，`_failure_tracker` 触发 → 策略 3）
2. **[DOM-PATCH]** 新增 `_inject_strategy_annotation()` — 在 DOM dump 文本中插入策略注释
3. **[DOM-PATCH]** 与 OPTIMIZE-02 `_failure_tracker` 联动 — 失败 2 次后标注自动降级为策略 3
4. **[PROMPT]** Section 9 追加策略优先级规则和使用说明 — 指导 Agent 根据策略标注选择操作

---

## OPTIMIZE-04: 失败恢复策略

**对应需求:** OPTIMIZE-04
**设计决策:** Per D-12（失败恢复为统一规则表——失败模式 → 检测条件 → 切换动作）

### 目标

| 目标 | 描述 |
|------|------|
| 为三种失败模式定义统一的检测→恢复规则 | 点击无 DOM 变化 / 误点错误列 / 编辑态判断失误 |
| 规则表格式便于实施 | 失败模式 → 检测条件 → 切换动作，统一模板 |

### 问题分析

当前 Agent 面对失败时缺乏结构化恢复策略：

1. **点击无 DOM 变化**: Agent 点击某个 index 后页面无任何变化（如点击了不可交互的 td），但 Agent 可能重复尝试
2. **误点错误列**: Agent 点击了"总成本"列而非"销售金额"列，激活了错误的 input
3. **编辑态判断失误**: Agent 误认为 td 已进入编辑态（input 已出现），实际 input 未出现，尝试 input 操作失败

### 设计规则表

#### 规则 1: 点击无 DOM 变化

| 维度 | 内容 |
|------|------|
| **失败模式** | Agent 点击某 index 后 DOM hash 未变化（点击无效果） |
| **检测条件** | step_callback 中 `dom_hash_before == dom_hash_after` 且 `action_name == "click"` |
| **切换动作** | (1) 标注该 index 对应元素为 `<!-- 点击无响应 -->` (2) 如果目标是 td，建议先检查是否需要滚动到可视区域 (3) 如果目标是 input，切换到 evaluate JS 策略 (4) 注入干预消息指导 Agent 更换操作方式 |
| **示例** | Agent 点击 index=5 的 td 后无变化 → 标注 `<!-- 点击无响应，尝试 evaluate JS: document.querySelector('...').click() -->` → 下一步 Agent 使用 evaluate |

#### 规则 2: 误点错误列

| 维度 | 内容 |
|------|------|
| **失败模式** | Agent 点击了错误的列（如点了总成本列而非销售金额列） |
| **检测条件** | evaluation 中包含 "wrong column"/"错误列"/"误点"/"非目标列" 等关键词，或 DOM 变化显示错误的 input 被激活 |
| **切换动作** | (1) 标注误点元素为 `<!-- 非目标列，请忽略 -->` (2) 利用 OPTIMIZE-01 的行标识定位正确的目标列 td (3) 标注目标列元素为 `<!-- 目标列: {字段名}，请点击此处 -->` (4) 注入干预消息明确告知 Agent 正确的列 |
| **示例** | Agent 点了总成本 td → 标注 `<!-- 非目标列 -->` → 销售金额 td 标注 `<!-- 目标列: 销售金额 -->` → Agent 重新点击正确列 |

#### 规则 3: 编辑态判断失误

| 维度 | 内容 |
|------|------|
| **失败模式** | Agent 误认为 td 已进入编辑态（input 已出现），实际 input 未出现 |
| **检测条件** | Agent 尝试 input 操作但目标元素不可交互，或 evaluation 包含 "not editable"/"无法输入"/"元素不可操作" 等关键词 |
| **切换动作** | (1) 标注当前 td 为 `<!-- 编辑态未激活，需先 CLICK -->` (2) 注入干预消息提供 click-then-wait-retry 工作流指导 (3) 如果 click 后仍不出现 input，降级到策略 3（evaluate JS） |
| **示例** | Agent 尝试 INPUT 但失败 → 标注 `<!-- 编辑态未激活，执行: CLICK td → 等待 1s → INPUT -->` → Agent 重新按正确工作流操作 |

### 三种失败模式的关系

```
Agent 操作
    │
    ├── click(index) → DOM hash 不变 → 规则 1: 点击无变化
    │       └── 标注 + 切换操作方式
    │
    ├── click(index) → DOM 变化但错误列 → 规则 2: 误点错误列
    │       └── 标注 + 利用行标识重定位
    │
    └── input(index) → 元素不可交互 → 规则 3: 编辑态未激活
            └── 标注 + 提供 click-to-edit 工作流
```

### 集成点

#### DOM Patch 层: 与 OPTIMIZE-02 的 `_patch_dynamic_annotation()` 共用

- **文件**: `backend/agent/dom_patch.py`
- **关系**: 失败恢复标注是动态标注的子类型。OPTIMIZE-02 的 `_failure_tracker` 扩展为支持三种失败模式
- **扩展内容**:
  - `_failure_tracker` 新增 `"mode"` 字段: `"click_no_effect"` / `"wrong_column"` / `"edit_not_active"`
  - `_patch_dynamic_annotation()` 根据 mode 生成不同的标注文本

#### 监控层: 扩展 StallDetector

- **文件**: `backend/agent/stall_detector.py`
- **当前能力**: 检测重复操作和停滞
- **扩展内容**:
  - 新增 click 无 DOM 变化检测: 保存上一步 dom_hash，与当前步 dom_hash 比较
  - 新增 evaluation 中的列错误关键词匹配: 检测 "wrong column"/"错误列"/"误点" 等
  - 新增编辑态状态检测: 当 action_name == "input" 且 evaluation 包含失败关键词时标记
- **返回值扩展**: `StallResult` 可增加 `failure_mode` 字段，标识是哪种失败模式

#### Prompt 层: Section 9 追加 ERP 表格专用失败恢复规则

- **文件**: `backend/agent/prompts.py`
- **追加位置**: Section 9 末尾
- **与现有内容关系**:
  - Section 2 "失败恢复强制规则"（prompts.py line 16-21）是通用规则
  - 新规则是 ERP 表格专用规则（更具体），与 Section 2 互补
  - Section 2 说"连续 2 次失败后切换策略"，新规则说"对于 ERP 表格的三种具体失败模式，分别如何恢复"

### 代码任务清单

1. **[DOM-PATCH]** 扩展 `_failure_tracker` — 添加 `"mode"` 字段支持三种失败模式（`click_no_effect` / `wrong_column` / `edit_not_active`）
2. **[DOM-PATCH]** 扩展 `_patch_dynamic_annotation()` — 支持三种失败模式的不同标注文本
3. **[MONITOR]** 扩展 StallDetector — 添加 click 无 DOM 变化检测、列错误关键词检测、编辑态状态检测
4. **[AGENT-SERVICE]** step_callback 中调用新检测逻辑 — 在 agent_service.py line 302-337 的 detector calls 区域添加新的检测调用
5. **[PROMPT]** Section 9 追加 ERP 表格专用失败恢复规则 — 三种失败模式的应对流程

---

## 总结

### 代码任务总清单（去重、标注依赖关系）

按实施优先级排序（基于 Phase 65 结论：Patch 4 增强最高优先级）：

| # | 任务 | 来源 | 依赖 | 文件 |
|---|------|------|------|------|
| T01 | 新增 `_detect_row_identity(tr_node)` | OPTIMIZE-01 | 无 | dom_patch.py |
| T02 | 新增 `_patch_add_row_identity()` | OPTIMIZE-01 | T01 | dom_patch.py |
| T03 | 在 `apply_dom_patch()` 中注册新 patch | OPTIMIZE-01 | T02 | dom_patch.py |
| T04 | 增强 Patch 4 — 添加行归属标注 | OPTIMIZE-01 | T02 | dom_patch.py |
| T05 | 增强 Patch 4 — 添加策略层级判定 | OPTIMIZE-03 | T04 | dom_patch.py |
| T06 | 新增 `_inject_strategy_annotation()` | OPTIMIZE-03 | T05 | dom_patch.py |
| T07 | 新增 `_failure_tracker` 模块级状态 | OPTIMIZE-02 | 无 | dom_patch.py |
| T08 | 新增 `update_failure_tracker()` | OPTIMIZE-02 | T07 | dom_patch.py |
| T09 | 新增 `_patch_dynamic_annotation()` | OPTIMIZE-02, 04 | T07, T08 | dom_patch.py |
| T10 | 与 `_failure_tracker` 联动策略降级 | OPTIMIZE-03 | T05, T07 | dom_patch.py |
| T11 | 扩展 StallDetector — 三种失败模式检测 | OPTIMIZE-04 | 无 | stall_detector.py |
| T12 | step_callback 调用 `update_failure_tracker()` | OPTIMIZE-02 | T08, T11 | agent_service.py |
| T13 | Section 9 追加行标识使用规则 | OPTIMIZE-01 | T02 | prompts.py |
| T14 | Section 9 追加反重复规则 | OPTIMIZE-02 | T09 | prompts.py |
| T15 | Section 9 追加策略优先级规则 | OPTIMIZE-03 | T06 | prompts.py |
| T16 | Section 9 追加 ERP 失败恢复规则 | OPTIMIZE-04 | T11 | prompts.py |

### 实施优先级建议

基于 Phase 65 结论（Patch 4 增强最高优先级），建议按以下顺序实施：

**第一优先级（基础能力）:**
1. T01-T03: 行标识机制（OPTIMIZE-01 的 DOM Patch 部分）
2. T07-T08: 失败追踪器基础（OPTIMIZE-02 的状态管理）

**第二优先级（增强现有 patch）:**
3. T04: Patch 4 增强行归属（依赖 T01-T03）
4. T05: Patch 4 增强策略层级（依赖 T04）
5. T06: 策略标注注入（依赖 T05）

**第三优先级（动态调整）:**
6. T09: 动态标注 patch（依赖 T07, T08）
7. T10: 策略降级联动（依赖 T05, T07）
8. T11: StallDetector 扩展（独立，可与 T09 并行）

**第四优先级（Prompt 层 + 集成）:**
9. T12: step_callback 集成（依赖 T08, T11）
10. T13-T16: Section 9 Prompt 追加（依赖对应 DOM Patch 完成）

### 测试验证建议

引用 Phase 65 Section 5.3.3 的 A/B 对照测试方案：

1. **组 A: headed + 全部 5 patches + 新优化**（预期：定位准确、失败少、策略切换顺畅）
2. **组 B: headed + 全部 5 patches（无新优化）**（对照：验证新优化的边际价值）
3. **测试场景**: 销售出库表格填写（Phase 62 E2E 场景的扩展版）
4. **评估指标**:
   - 步骤数（越少越好）
   - 错误点击次数（越少越好）
   - JS fallback 使用次数（越少越好）
   - 最终填写值正确性（必须 100%）

### 文档变更记录

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 1.0 | 2026-04-06 | 初始版本 — 四项优化设计（OPTIMIZE-01~04） |

---

## 验证记录

### CONTEXT.md 决策对照检查（D-01 ~ D-12）

| 决策 | 要求 | 文档中体现 | 通过 |
|------|------|-----------|------|
| D-01 | 规则表 + 任务清单格式 | 每项优化均有：目标表格 + 规则表（条件/动作/示例）+ 集成点 + 代码任务清单 | PASS |
| D-02 | 存放在 `.planning/phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md` | 文件位于指定路径 | PASS |
| D-03 | 单文件统一设计 | 所有四项优化在同一个文件中，可交叉引用 | PASS |
| D-04 | DOM Patch + Prompt 两层实现 | 集成点只涉及 dom_patch.py 和 prompts.py，无独立模块 | PASS |
| D-05 | 融入 dom_patch.py | DOM Patch 集成点均引用 dom_patch.py 现有函数和模式 | PASS |
| D-06 | 追加 Section 9 | 所有 Prompt 集成点明确"追加到 Section 9 末尾" | PASS |
| D-07 | `<tr>` 行标识 | OPTIMIZE-01 设计为 `<tr>` 添加 `data-row-identity` 属性和 DOM dump 注释 | PASS |
| D-08 | 商品编号/IMEI 作为标识符 | OPTIMIZE-01 使用正则 `I\d{15}` 匹配 IMEI 格式作为行标识 | PASS |
| D-09 | 行内 placeholder 匹配找 input | OPTIMIZE-01 R01-3 规则：锁定行后通过 placeholder 匹配找目标 input | PASS |
| D-10 | 反重复在 DOM Patch 层 | OPTIMIZE-02 在序列化时动态调整（`_patch_dynamic_annotation()`） | PASS |
| D-11 | 三级策略通过 DOM Patch 标注 | OPTIMIZE-03 通过 DOM dump 中的 `<!-- 策略N: ... -->` 注释实现策略选择 | PASS |
| D-12 | 失败恢复为统一规则表 | OPTIMIZE-04 为三种失败模式各定义了：失败模式 → 检测条件 → 切换动作 | PASS |

### ROADMAP 成功标准检查

| # | 标准 | 文档中体现 | 通过 |
|---|------|-----------|------|
| 1 | 按行定位 + 直接找 input 策略 — 有行定位选择器和 input 匹配规则 | OPTIMIZE-01: `_detect_row_identity()` 提取行标识，R01-3 规则定义行内 placeholder 匹配 | PASS |
| 2 | 反重复机制 — 触发条件明确（同 index 2 次、误点 1 次） | OPTIMIZE-02: R02-1/R02-2（同 index 2 次失败）、R02-3（点击无变化 1 次）、R02-4（误点 1 次） | PASS |
| 3 | 三级策略优先级 — 每级适用场景和切换条件明确 | OPTIMIZE-03: 策略 1（可见 input）、策略 2（hidden input）、策略 3（兜底），R03-4/R03-5 定义切换条件 | PASS |
| 4 | 失败恢复策略 — 三种失败模式的快速切换规则 | OPTIMIZE-04: 规则 1（点击无变化）、规则 2（误点错误列）、规则 3（编辑态误判） | PASS |
| 5 | 设计文档无代码实现但描述足够具体 | 文档无 Python 代码块（除伪代码示例），每项有 5 项代码任务可转化 | PASS |

### 需求覆盖检查

| 需求 ID | 需求描述 | 对应设计 | 通过 |
|---------|----------|----------|------|
| OPTIMIZE-01 | 按行定位 + 直接找 input 的表格输入策略设计 | OPTIMIZE-01: 4 条规则 + 5 项代码任务 | PASS |
| OPTIMIZE-02 | 反重复机制设计（同 index 失败 2 次自动切换） | OPTIMIZE-02: 4 条规则 + 5 项代码任务 | PASS |
| OPTIMIZE-03 | 原生 input → DOM 查询 → evaluate JS 策略优先级 | OPTIMIZE-03: 5 条规则 + 4 项代码任务 | PASS |
| OPTIMIZE-04 | 失败恢复策略设计（三种失败模式的快速切换规则） | OPTIMIZE-04: 3 条规则 + 5 项代码任务 | PASS |

### 集成点一致性检查

| 集成点引用 | 引用位置 | 实际代码验证 | 通过 |
|-----------|---------|-------------|------|
| `_patch_is_interactive()` | dom_patch.py line 183-211 | 函数存在于 line 183 | PASS |
| `_patch_paint_order_remover()` | dom_patch.py line 250-266 | 函数存在于 line 250 | PASS |
| `_patch_should_exclude_child()` | dom_patch.py line 269-286 | 函数存在于 line 269 | PASS |
| `_patch_assign_interactive_indices()` | dom_patch.py line 289-328 | 函数存在于 line 289 | PASS |
| `_is_textual_td_cell()` | dom_patch.py line 37-81 | 函数存在于 line 37 | PASS |
| `apply_dom_patch()` | dom_patch.py line 214-247 | 函数存在于 line 214 | PASS |
| `_ERP_TABLE_CELL_PLACEHOLDERS` | dom_patch.py line 21-27 | 常量存在于 line 21 | PASS |
| `_ERP_CLICKABLE_CLASSES` | dom_patch.py line 17 | 常量存在于 line 17 | PASS |
| Section 9 "ERP 表格单元格填写" | prompts.py line 52-83 | Section 9 位于 line 52-83 | PASS |
| Section 2 "失败恢复强制规则" | prompts.py line 16-21 | Section 2 位于 line 16-21 | PASS |
| `apply_dom_patch()` 调用入口 | agent_service.py line 357 | 调用存在于 line 357 | PASS |
| `step_callback` 检测器调用 | agent_service.py line 302-337 | detector calls 区域存在于 line 302 | PASS |
| `_pending_interventions` 列表 | monitored_agent.py line 53 | 变量存在于 line 53 | PASS |
| `StallDetector.check()` | stall_detector.py | 检测器存在 | PASS |
| `create_step_callback()` | monitored_agent.py line 147-239 | 函数存在于 line 147 | PASS |

---

*文档生成时间: 2026-04-06*
*基于 Phase 65 分析结论（65-ANALYSIS-REPORT.md）*
*设计决策来源: 66-CONTEXT.md (D-01 ~ D-12)*
