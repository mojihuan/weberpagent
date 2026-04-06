# Phase 65: 差距关联分析 - Context

**Gathered:** 2026-04-06
**Status:** Ready for planning

<domain>
## Phase Boundary

确认 v0.8.2 报告中发现的 headless/headed 浏览器模式差异是否直接导致 Agent 在 ERP 表格填写时定位不准，并评估恢复 headed 模式后现有 DOM Patch + Prompt 策略的有效性。

**不包含：**
- 任何代码修改
- 恢复 headed 模式的实施
- 设计优化方案（属于 Phase 66）
- 实际运行测试对比

</domain>

<decisions>
## Implementation Decisions

### 验证方法
- **D-01:** 纯代码推理 — 基于 Phase 63 分析结果、browser-use 源码、Chromium 文档进行推理分析
  - 不需要实际运行环境
  - 依托 Phase 63 的代码对比和 DOM 渲染差异分析
  - 通过浏览器引擎源码和已知行为记录构建证据链

### 报告格式与位置
- **D-02:** 单文件存放在 `.planning/phases/65-差距关联分析/` 目录下
  - Phase 64 已产出完整技术报告 (.planning/) 和精简摘要 (docs/)
  - Phase 65 是中间分析产物，不需要单独的 docs/ 版本
  - Phase 66 可直接引用 Phase 65 分析结果

### DOM Patch 评估粒度
- **D-03:** 逐 patch 评估 — 5 个 patch 逐一分析在 headed 模式下的必要性
  - Patch 1: 交互标记 (_patch_is_interactive — hand/checkbox/td 文本)
  - Patch 2: paint order 移除 (_patch_paint_order_remover)
  - Patch 3: child 排除 (_patch_should_exclude_child)
  - Patch 4: input 索引 (_patch_assign_interactive_indices)
  - Patch 5: td 文本检测 (_is_textual_td_cell)
  - 每个patch 给出判定：仍必要 / 冗余 / 部分必要 / 冲突
  - 为 Phase 66 优化方案提供精确输入

### 结论判定标准
- **D-04:** 三层证据链判定法
  - 层 1: 代码推理（browser-use/Chromium 源码分析）
  - 层 2: 已知行为（Phase 62-64 观察记录）
  - 层 3: 补丁效果（DOM Patch 实际解决了问题）
  - 判定规则：三层一致 → "是"，两层一致 → "部分"，一层或以下 → "否"
  - 三项分析（ANALYSIS-01/02/03）均需给出明确判定，不是模糊描述

### Claude's Discretion
- 报告中文/英文表述的选择
- 证据链引用的具体格式
- DOM Patch 评估的论述深度

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase 63-64 分析结果（核心输入）
- `.planning/phases/63-代码对比分析/63-01-comparison-result.md` — v0.4.0 vs 当前版本配置对比 + DOM 渲染差异分析 + DOM Patch 评估
- `.planning/phases/63-代码对比分析/63-02-evolution-result.md` — browser-use 版本对比 + Agent/Browser 配置演变时间线
- `.planning/phases/64-分析报告输出/64-REPORT.md` — v0.8.2 完整技术分析报告
- `docs/browser-mode-analysis.md` — v0.8.2 精简摘要报告

### 源代码
- `backend/core/agent_service.py` — 当前 Agent/Browser 配置
- `backend/agent/dom_patch.py` — DOM Patch 5 patches 实现
- `backend/agent/prompts.py` — ENHANCED_SYSTEM_MESSAGE（含 Section 9）

### browser-use 内部
- `.venv/lib/python3.11/site-packages/browser_use/browser/profile.py` — headless 自动检测逻辑、CHROME_HEADLESS_ARGS
- `.venv/lib/python3.11/site-packages/browser_use/agent/service.py` — Agent 类

### 先前阶段上下文
- `.planning/phases/63-代码对比分析/63-CONTEXT.md` — Phase 63 对比范围和格式决策
- `.planning/phases/64-分析报告输出/64-CONTEXT.md` — Phase 64 报告格式和位置决策

### 需求与路线图
- `.planning/REQUIREMENTS.md` — v0.8.3 需求定义（ANALYSIS-01~03）
- `.planning/ROADMAP.md` — Phase 65 成功标准

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Phase 63 已完成完整的配置对比表（run_simple/run_with_streaming/Playwright 配置），可直接引用
- Phase 63 已完成 DOM Patch 5 patches 的初步评估（MEDIUM confidence）
- Phase 64 已完成根因分析确认（f951791 提交）
- Phase 62 已完成 E2E 验证（26 步成功，销售金额=150）

### Established Patterns
- 报告语言为中文（项目一贯风格）
- 分析报告使用 Markdown 格式
- 技术报告包含配置项表格、代码片段、置信度表

### Integration Points
- Phase 65 分析结论是 Phase 66 优化方案设计的直接输入
- Phase 66 需要基于 Phase 65 的逐 patch 判定设计优化策略
- REQUIREMENTS.md 中的 ANALYSIS-01/02/03 对应三项分析任务

</code_context>

<specifics>
## Specific Ideas

- 三项分析应使用统一的三层证据链框架：代码推理 + 已知行为 + 补丁效果
- ANALYSIS-01（因果关联）需回答：headless 下 DOM 序列化是否导致 index 偏移或元素不可见
- ANALYSIS-02（DOM Patch 有效性）需回答：每个 patch 在 headed 模式下仍必要还是冗余
- ANALYSIS-03（Prompt 有效性）需回答：Section 9 click-to-edit 指导在 headed 模式下是否仍需保留
- 报告应包含明确的判定表：分析项 | 判定 | 证据链 | 置信度

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 65-差距关联分析*
*Context gathered: 2026-04-06*
