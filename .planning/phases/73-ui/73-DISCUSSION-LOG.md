# Phase 73: 批量进度 UI - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-09
**Phase:** 73-ui
**Areas discussed:** 页面形式与入口, 进度列表布局, 状态展示与交互

---

## 页面形式与入口

### 页面形式
| Option | Description | Selected |
|--------|-------------|----------|
| 独立页面 | 跳转到 /batches/:id 独立页面，专注展示进度 | ✓ |
| Tasks 页内嵌 | Tasks 页面内嵌进度面板，无需跳转 | |
| 全屏弹窗 | 全屏 Modal 覆盖当前页面 | |

**User's choice:** 独立页面
**Notes:** 专注展示进度，不干扰任务列表

### 跳转时机
| Option | Description | Selected |
|--------|-------------|----------|
| 创建批次后立即跳转 | 用户点击「开始执行」后立即跳转 | ✓ |
| 等待所有 run 创建完 | 确保进度页不会出现空状态 | |

**User's choice:** 创建批次后立即跳转

---

## 进度列表布局

### 列表布局
| Option | Description | Selected |
|--------|-------------|----------|
| 简约列表行 | 每行一个任务，类似 TaskTable 的简约行 | |
| 卡片布局 | 每个任务一个卡片，显示更多信息 | ✓ |
| 表格布局 | 类似表格的布局，有列头 | |

**User's choice:** 卡片布局

### 信息展示（多选）
| Option | Selected |
|--------|----------|
| 任务名称 | ✓ |
| 状态标签 | ✓ |
| 耗时 | ✓ |
| 整体进度统计 | ✓ |

**User's choice:** 全选

---

## 状态展示与交互

### 跳转交互
| Option | Description | Selected |
|--------|-------------|----------|
| 点击卡片跳转 | 点击卡片任意位置直接跳转到 /runs/:id | ✓ |
| 单独跳转按钮 | 卡片右侧有独立的「查看详情」按钮 | |

**User's choice:** 点击卡片跳转

### 完成提示
| Option | Description | Selected |
|--------|-------------|----------|
| Toast 通知 + 摘要 | 全部完成时 toast + 摘要（成功/失败数） | ✓ |
| 结果汇总弹窗 | 全部完成时弹出结果汇总弹窗 | |
| 无提示 | 无额外提示 | |

**User's choice:** Toast 通知 + 摘要

---

## Claude's Discretion

- 卡片的具体 UI 样式和间距
- 状态标签的动画效果
- 整体进度统计的展示形式（纯文字 vs 带进度条）
- 卡片排列方式（单列 vs 响应式多列）
- 加载态和空状态的处理

## Deferred Ideas

- 侧边栏添加「批量进度」导航入口 — 可在 v2 添加，当前通过跳转进入即可
