# Phase 52: Prompt 增强 — 键盘操作 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-30
**Phase:** 52-prompt
**Areas discussed:** 键盘指导策略、粘贴场景细节、验证场景选择、Enter 使用范围、ESC 范围

---

## Prompt 格式

| Option | Description | Selected |
|--------|-------------|----------|
| 场景-动作对 | 每条规则以"场景 → 动作"描述，如"搜索框输入后 → send_keys('Enter')" | ✓ |
| 编号规则列表 | 逐条列出键盘操作规则 | |
| 混合格式 | 场景描述 + 代码示例混合 | |

**User's choice:** 场景-动作对
**Notes:** 与 Phase 49 精简指令风格一致，Qwen 对这种格式遵守度高

---

## 粘贴策略

| Option | Description | Selected |
|--------|-------------|----------|
| 先 input 全选再覆盖 | send_keys('Control+a') + type 新值，不依赖剪贴板 | ✓ |
| 直接 send_keys 粘贴 | send_keys('Control+v') 粘贴，需先复制内容到剪贴板 | |
| 两种都指导 | 同时说明两种方式，Agent 自行选择 | |

**User's choice:** 先 input 全选再覆盖
**Notes:** 剪贴板内容不确定，直接粘贴策略不可靠

---

## 验证场景

| Option | Description | Selected |
|--------|-------------|----------|
| 采购单场景 | IMEI/物品编号输入 Enter + 日期选择器 ESC，最典型 ERP 场景 | ✓ |
| 保卖/销售场景 | 物品编号输入 + 销售出库搜索，更贴近业务 | |
| 通用测试页面 | 设计通用测试页面覆盖三种操作 | |

**User's choice:** 采购单场景
**Notes:** 采购单同时覆盖 Enter（物品编号搜索）和 ESC（日期弹窗关闭）两种键盘操作

---

## Enter 使用范围

| Option | Description | Selected |
|--------|-------------|----------|
| 搜索触发式 | 仅搜索框输入后按 Enter 触发搜索 | ✓ |
| 搜索 + 表单提交 | 同时覆盖搜索和表单提交场景 | |
| 仅搜索场景 | 只搜索，表单提交用点击按钮 | |

**User's choice:** 搜索触发式
**Notes:** 表单提交通过点击按钮完成，Enter 仅用于搜索触发

---

## ESC 范围

| Option | Description | Selected |
|--------|-------------|----------|
| 仅关闭弹窗 | 日期选择器、下拉弹窗遮挡时 ESC 关闭 | ✓ |
| 关闭弹窗 + 取消操作 | 同时指导 ESC 取消编辑等操作 | |
| 关闭弹窗 + 恢复手段 | 增加 ESC 作为页面卡住时的恢复手段 | |

**User's choice:** 仅关闭弹窗
**Notes:** 保持简洁，ESC 仅用于关闭遮挡元素

---

## Claude's Discretion

- ENHANCED_SYSTEM_MESSAGE 键盘操作段落的具体措辞
- 测试用例的具体关键词列表
- 验证步骤的具体 ERP 操作流程

## Deferred Ideas

None — discussion stayed within phase scope.
