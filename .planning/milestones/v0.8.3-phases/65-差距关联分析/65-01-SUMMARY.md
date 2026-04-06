---
phase: 65-差距关联分析
plan: 01
status: complete
created: 2026-04-06
---

# Plan 65-01 Summary: 差距关联分析报告

## Objective
生成差距关联分析报告，回答三个核心问题：(1) headless 模式是否直接导致 Agent 表格定位不准；(2) 恢复 headed 后 5 个 DOM Patch 各自的有效性；(3) Section 9 click-to-edit 指导在 headed 模式下是否仍需保留。

## Result
完成。三项分析均使用三层证据链框架得出明确判定。

## Key Findings

### ANALYSIS-01: Headless 与表格定位不准的因果关联
- **判定: 部分**（置信度 MEDIUM-HIGH）
- Headless 是加剧因素而非唯一根因
- Index 偏移: headless 通过 paint order 差异加剧部分问题，但 ERP 嵌套结构和 hidden input 问题在 headed 下同样存在
- 元素不可见: 主要是 Ant Design click-to-edit 应用级行为（display:none），与浏览器模式无关

### ANALYSIS-02: DOM Patch 在 Headed 模式下的有效性
- Patch 1（is_interactive）: **仍必要**（HIGH）— browser-use 不识别 ERP CSS class
- Patch 2（paint_order_remover）: **部分必要**（MEDIUM）— headed 下 paint order 可能更准确
- Patch 3（should_exclude_child）: **仍必要**（HIGH）— bbox containment 几何关系不变
- Patch 4（assign_interactive_indices）: **仍必要**（HIGH）— display:none 不在 CDP layout tree
- Patch 5（textual_td_cell）: **仍必要**（HIGH）— click-to-edit 交互标记需求

### ANALYSIS-03: Section 9 Prompt 有效性
- **判定: 保留**（置信度 HIGH）
- Section 9 是应用级交互指导，与浏览器模式无关
- 所有核心内容（click-to-edit 工作流、定位策略、fallback）均需保留

## Key Files
- created: .planning/phases/65-差距关联分析/65-ANALYSIS-REPORT.md

## Issues
None — 纯分析任务，无代码修改。

## Self-Check: PASSED
- [x] All tasks executed (3/3)
- [x] Report file created and complete
- [x] Three analyses with clear verdicts
- [x] Three-layer evidence chain for each analysis
- [x] Summary verdict table with Phase 66 inputs
