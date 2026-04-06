# Project Retrospective

## Milestone: v0.8.3 — 分析报告差距对表格填写影响

**Shipped:** 2026-04-06
**Phases:** 2 | **Plans:** 2

### What Was Built

- 差距关联分析: headless 是加剧因素而非唯一根因，DOM Patch 4/5 仍必要
- 优化方案设计: 540 行设计文档，4 项策略（行定位/反重复/策略优先级/失败恢复），16 项代码任务

### What Worked

- **纯分析里程碑模式**: 不写代码，聚焦分析和设计，减少上下文切换
- **三层证据链框架**: 每项分析结论有明确判定（是/否/部分）+ 证据链，避免模糊描述
- **设计文档结构化**: 16 项代码任务标注依赖关系和优先级，可直接实施

### What Was Inefficient

- Phase 65 缺少 SUMMARY.md（验证时发现）
- ANALYSIS-01~03 在 REQUIREMENTS.md 中标记为 Pending（实际上已完成）

### Patterns Established

- **DOM dump 注释注入**: 通过 `<!-- -->` 注释向 Agent 传递结构化信息，不修改 Agent 决策逻辑
- **跨步骤状态共享**: 模块级变量在 step_callback 和 DOM Patch 间共享
- **策略自动降级**: 三级策略逐级降级，通过注释标注实现

### Key Lessons

1. 纯分析设计里程碑可以快速完成（1 天），为后续实施节省上下文
2. 设计文档的"可直接转化为代码任务"标准很重要——避免后续实施时的二次理解
3. 因果分析需要区分"根因"和"加剧因素"，避免过度简化

### Cost Observations

- Model mix: 100% opus
- Sessions: 2 (分析 + 设计)
- Notable: 极轻量里程碑，无代码修改，纯文档输出

## Milestone: v0.8.1 — 修复销售出库表格填写问题

**Shipped:** 2026-04-06
**Phases:** 1 | **Plans:** 1

### What Was Built

- DOM Patch 扩展到 5 个补丁，支持 ERP click-to-edit 表格的 td 单元格交互标记
- Section 9 提示词添加 ERP 销售出库 click-to-edit 工作流指导（点击 td → 等待 input → 输入值）
- E2E 验证: 销售出库 26 步完成，销售金额 150 成功填写

### What Worked

- **快速定位根因**: 通过 E2E 测试快速发现 Ant Design click-to-edit 表格不会预渲染 input 元素
- **Pivot 决策果断**: 从 input placeholder 检测快速转向 td 文本内容检测，仅用一次 commit 修复
- **DOM Patch 模式成熟**: 在已有 Phase 53 的 monkey-patch 基础上扩展，模式清晰可复用

### What Was Inefficient

- 初始方案基于错误假设（input placeholder 存在于 DOM 中），需要一次修复 commit
- Phase 60-task-form-optimize 空目录残留（init 标记为 pending 但实际无工作）

### Patterns Established

- **click-to-edit td 检测模式**: `_is_textual_td_cell()` 检测 td 内文本内容，标记为 interactive
- **Prompt Section 模式**: 每个 ERP 场景一个 Section，包含工作流 + 负面示例

### Key Lessons

1. Ant Design click-to-edit 表格不会预渲染 input，必须先 click td 触发编辑模式
2. DOM Patch 目标应基于实际 DOM 结构验证，而非假设
3. 简单的里程碑（1 phase）可以在 30 分钟内完成

### Cost Observations

- Model mix: 100% opus
- Sessions: 2 (plan + execute)
- Notable: 极小的里程碑，单阶段单计划，效率高

## Cross-Milestone Trends

| Metric | v0.6.3 | v0.7.0 | v0.8.0 | v0.8.1 | v0.8.3 |
|--------|--------|--------|--------|--------|--------|
| Phases | 4 | 5 | 5 | 1 | 2 |
| Plans | 10 | 10 | 6 | 1 | 2 |
| Duration (days) | 1 | 2 | 2 | 1 | <1 |
| Tech Debt Added | 0 | 1 (cache assert) | 0 | 0 | 0 |
| Bugs Found/Fixed | 0 | 0 | 0 | 2 (auto-fixed) | 0 |
| Code LOC Changed | ~800 | ~300 | ~600 | ~100 | 0 |
