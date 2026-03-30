# Phase 53: Prompt 增强 — 表格交互 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-30
**Phase:** 53-prompt
**Areas discussed:** 表格元素定位策略, ERP 验证场景选择, 否定指令与边界

---

## 表格元素定位策略 — Checkbox 定位

| Option | Description | Selected |
|--------|-------------|----------|
| DOM 位置描述 | 表头 `<thead>` checkbox = 全选，`<tbody>` 行 checkbox = 单选。Agent 通过 DOM 层级区分 | ✓ |
| 文本关联描述 | checkbox 旁边有"全选"文本则全选，否则点击行 checkbox | |
| Claude's Discretion | 让 Claude 根据实际 ERP 表格结构决定 | |

**User's choice:** DOM 位置描述
**Notes:** 与 Phase 52 的 DOM 描述模式一致，Agent 对 DOM 层级有较好的识别能力

## 表格元素定位策略 — 超链接定位

| Option | Description | Selected |
|--------|-------------|----------|
| 文本定位 + 直接点击 | 表格中 `<a>` 超链接用可见文本直接 click，简洁直接 | ✓ |
| find_elements 查找后点击 | 先 find_elements('a') 查找，再用文本匹配，更精确但步骤更多 | |
| Claude's Discretion | 让 Claude 根据实际 ERP 决定 | |

**User's choice:** 文本定位 + 直接点击
**Notes:** Agent 对可见文本 click 已有成熟的操作能力

## 表格元素定位策略 — 图标按钮定位

| Option | Description | Selected |
|--------|-------------|----------|
| title/aria-label 定位 | 操作按钮通过 title 或 aria-label 属性定位，包含功能描述文本 | ✓ |
| 可点击元素查找 | find_elements 查找行内可点击元素，再根据位置选择 | |
| Claude's Discretion | 让 Claude 根据实际 ERP 图标结构决定 | |

**User's choice:** title/aria-label 定位
**Notes:** ERP 系统通常为图标按钮提供 title 或 aria-label 属性

## ERP 验证场景选择

| Option | Description | Selected |
|--------|-------------|----------|
| 采购单列表 | 采购单列表有 checkbox、订单号链接、操作按钮，与 Phase 52 场景一致 | ✓ |
| 销售出库列表 | 可能包含更多表格交互场景 | |
| 物品管理列表 | 物品编号是链接，有编辑/删除按钮 | |
| 多页面组合 | 多个页面分别验证不同场景 | |

**User's choice:** 采购单列表一站式验证
**Notes:** 采购单列表一站式覆盖 TBL-01~04 全部 4 个需求

## 否定指令与边界

| Option | Description | Selected |
|--------|-------------|----------|
| 加入否定指令 | Phase 52 否定指令成功模式，防止表格操作常见错误 | ✓ |
| 仅正面指导 | 不加否定指令，只用正面指导，保持 prompt 精简 | |
| Claude's Discretion | 根据实际测试中观察到的 Agent 错误决定 | |

**User's choice:** 加入否定指令
**Notes:** 延续 Phase 52 否定指令模式，具体措辞由 Claude 决定

## Claude's Discretion

- ENHANCED_SYSTEM_MESSAGE 表格交互段落的具体措辞
- 否定指令的具体内容和措辞
- 测试用例的具体关键词列表
- 验证步骤的具体 ERP 操作流程

## Deferred Ideas

None — discussion stayed within phase scope.
