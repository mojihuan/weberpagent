# Phase 66: 优化方案设计 - Context

**Gathered:** 2026-04-06
**Status:** Ready for planning

<domain>
## Phase Boundary

基于 Phase 65 分析结论，设计四项可执行的 Agent 表格交互优化策略：
1. OPTIMIZE-01: 按行定位 + 直接找 input
2. OPTIMIZE-02: 反重复机制（同 index 失败 2 次自动切换）
3. OPTIMIZE-03: 策略优先级（原生 input → DOM 查询 → evaluate JS）
4. OPTIMIZE-04: 失败恢复策略（无变化/误列/编辑态误判）

**不包含：**
- 任何代码实现（本 milestone 只做设计文档）
- 恢复 headed 模式的实施
- 断言系统修改
- 移除现有 DOM Patch 或 Section 9 内容

**关键输入（Phase 65 结论）：**
- ANALYSIS-01: headless 是加剧因素（非唯一根因）
- ANALYSIS-02: 5 个 DOM Patch 中 4 个仍必要 (HIGH)，Patch 2 部分必要 (MEDIUM)
- ANALYSIS-03: Section 9 全部保留 (HIGH)
- Patch 4（强制 ERP input 获得索引）是最高价值 patch

</domain>

<decisions>
## Implementation Decisions

### 设计文档格式与位置
- **D-01:** 规则表 + 任务清单格式 — 每项优化用统一模板：目标 → 设计规则表（条件/动作/示例）→ 与现有代码集成点 → 转化为代码任务的清单
- **D-02:** 存放在 `.planning/phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md`
- **D-03:** 单文件统一设计 — 四项优化用相同模板，便于交叉引用（如 OPTIMIZE-03 策略优先级引用 OPTIMIZE-01 行定位结果）

### 优化方案实施层级
- **D-04:** 主要在 DOM Patch + Prompt 两层实现，不新增独立模块
- **D-05:** DOM Patch 层优化融入现有 `dom_patch.py`（新增 patch 函数），保持单文件
- **D-06:** Prompt 层追加新规则到现有 Section 9，保留现有内容作为基础

### 按行定位策略（OPTIMIZE-01）
- **D-07:** DOM Patch 层为 `<tr>` 添加行标识 — 类似 Patch 5 给 td 添加文本的方式，让 Agent 在 DOM dump 中看到每个 `<tr>` 的商品标识
- **D-08:** 行标识符使用商品编号/IMEI 文本 — ERP 销售出库表格每行有唯一编号（如 I01784004409597），出现在特定 `<td>` 中
- **D-09:** 锁定行后通过行内 placeholder 匹配找目标 input — 在指定行内查找包含目标 placeholder 的 `<input>`，解决"同一 placeholder 在多行出现"问题

### 反重复机制（OPTIMIZE-02）
- **D-10:** 反重复检测在 DOM Patch 层实现 — 序列化时动态调整，如果上次操作某 index 失败，下次序列化时改变该元素的优先级/可见性/标注。Agent 每次拿到的 DOM dump 根据失败历史动态调整

### 策略优先级（OPTIMIZE-03）
- **D-11:** 三级策略优先级在 DOM Patch 层通过标注策略层级实现 — 优化后的 Patch 4 优先分配行内 input 索引（原生操作级），失败后 Patch 动态标注 DOM 查询路径，再失败则标注 evaluate JS 路径。Agent 通过 DOM dump 中的标注自然选择策略

### 失败恢复策略（OPTIMIZE-04）
- **D-12:** 失败恢复设计为统一规则表 — 失败模式 → 检测条件 → 切换动作。三种失败模式（点击无 DOM 变化、误点错误列、编辑态判断失误）各一行规则

### Claude's Discretion
- 规则表中示例的具体文字表述
- 文档中的图表/流程图使用
- 与 Phase 65 结论的引用格式

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase 65 分析结果（核心输入）
- `.planning/phases/65-差距关联分析/65-ANALYSIS-REPORT.md` — 三项分析完整报告，含因果判定、逐 Patch 评估、Section 9 评估、Phase 66 输入建议
- `.planning/phases/65-差距关联分析/65-CONTEXT.md` — Phase 65 分析方法和格式决策

### Phase 63-64 分析结果
- `.planning/phases/63-代码对比分析/63-01-comparison-result.md` — v0.4.0 vs 当前版本配置对比 + DOM 渲染差异分析
- `.planning/phases/63-代码对比分析/63-02-evolution-result.md` — browser-use 版本对比 + Agent/Browser 配置演变
- `.planning/phases/64-分析报告输出/64-REPORT.md` — v0.8.2 完整技术分析报告
- `docs/browser-mode-analysis.md` — v0.8.2 精简摘要

### 源代码（设计集成点）
- `backend/agent/dom_patch.py` — DOM Patch 5 patches 实现，新优化将融入此文件
- `backend/agent/prompts.py` — ENHANCED_SYSTEM_MESSAGE Section 9（第 52-83 行），新规则将追加于此
- `backend/core/agent_service.py` — Agent/Browser 配置，apply_dom_patch() 调用入口
- `backend/agent/monitored_agent.py` — StallDetector/PreSubmitGuard，了解现有监控模式

### 需求与路线图
- `.planning/REQUIREMENTS.md` — v0.8.3 需求定义（OPTIMIZE-01~04）
- `.planning/ROADMAP.md` — Phase 66 成功标准

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `dom_patch.py` 的 monkey-patch 模式 — 新 patch 遵循相同模式：保存原始方法 → 包装 → 替换。`apply_dom_patch()` 是统一入口
- `_is_textual_td_cell()` — 已实现 td 文本检测逻辑，行标识 patch 可复用此模式的 DOM 遍历
- `_is_inside_table_cell()` — 已实现 td/th 父级遍历，可用于行定位的行级遍历
- `_ERP_TABLE_CELL_PLACEHOLDERS` — 已定义 ERP 字段 placeholder 列表，行内 input 匹配可直接使用
- `_ERP_CLICKABLE_CLASSES` — 已定义 ERP 可交互 CSS class，行标识可参考

### Established Patterns
- DOM Patch 是 monkey-patch（非侵入式），不修改 browser-use 源码
- Prompt 追加而非重写 — 保持 ENHANCED_SYSTEM_MESSAGE 结构稳定
- frozen=True dataclass 不可变模式
- 检测器实例每次 run 创建新实例（避免跨 run 状态残留）

### Integration Points
- `apply_dom_patch()` 在 `agent_service.py` 中调用 — 新 patch 需在此函数中注册
- Section 9 是 `ENHANCED_SYSTEM_MESSAGE` 的一部分 — 新规则追加在 Section 9 末尾
- DOM Patch 的序列化时动态调整需要在 `run_simple()`/`run_with_streaming()` 调用之间保持状态 — 可能需要通过 `step_callback` 传递失败信息

</code_context>

<specifics>
## Specific Ideas

- 按行定位的核心思路：Patch 5 让 `<td>` 显示文本内容 → 新 patch 让 `<tr>` 显示行标识（商品编号） → Agent 能看到"行 I01784004409597 包含 td 销售金额"
- 反重复的关键机制：DOM Patch 在序列化时根据失败历史动态调整，Agent 每次拿到不同的 DOM dump，自然避开之前失败的元素
- 三级策略的自然切换：DOM dump 中标注策略层级（"行内 input 可用" / "需要 DOM 查询" / "需要 JS fallback"），Agent 根据 dump 中的标注选择操作方式
- 设计文档格式参考：每项优化 = 目标表格 + 规则表（条件列/动作列/示例列）+ 与现有 patch 的集成点 + 代码任务清单

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 66-优化方案设计*
*Context gathered: 2026-04-06*
