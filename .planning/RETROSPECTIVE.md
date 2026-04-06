# Project Retrospective

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

| Metric | v0.6.3 | v0.7.0 | v0.8.0 | v0.8.1 |
|--------|--------|--------|--------|--------|
| Phases | 4 | 5 | 5 | 1 |
| Plans | 10 | 10 | 6 | 1 |
| Duration (days) | 1 | 2 | 2 | 1 |
| Tech Debt Added | 0 | 1 (cache assert) | 0 | 0 |
| Bugs Found/Fixed | 0 | 0 | 0 | 2 (auto-fixed) |
