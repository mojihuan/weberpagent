# Phase 72: 批量执行引擎 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-08
**Phase:** 72-批量执行引擎
**Areas discussed:** 触发方式, Batch 模型设计, 后端并发架构, 错误隔离, 确认弹窗 UI, API 路由, 状态流转

---

## 触发方式

| Option | Description | Selected |
|--------|-------------|----------|
| 直接启动 | 点击按钮后直接以默认并发数 2 启动所有勾选任务 | |
| 确认弹窗 + 并发数配置 | 弹出小弹窗让用户调整并发数（1-4），确认后启动 | ✓ |
| 直接启动 + 可选高级设置 | 默认直接启动，但提供一个「高级」链接展开并发数设置 | |

**User's choice:** 确认弹窗 + 并发数配置
**Notes:** 用户希望给高级用户控制力

---

## Batch 模型设计

| Option | Description | Selected |
|--------|-------------|----------|
| 有 Batch 模型 | 后端创建 Batch 表记录 batch_id、并发数、状态，关联多个 Run | ✓ |
| 无 Batch 模型 | 前端维护 run_id 列表，后端只提供批量查询多个 run 状态的 API | |

**User's choice:** 有 Batch 模型
**Notes:** 结构清晰，支持后续扩展（取消、重试等）

---

## 后端并发架构

| Option | Description | Selected |
|--------|-------------|----------|
| 复用 BackgroundTasks + Semaphore | 在路由层用 asyncio.gather + Semaphore 协调，复用现有函数 | |
| BatchExecutionService | 创建独立服务类封装 Semaphore、任务调度、错误隔离、进度更新 | ✓ |

**User's choice:** BatchExecutionService
**Notes:** 更结构化，便于测试和后续扩展

---

## 错误隔离策略

| Option | Description | Selected |
|--------|-------------|----------|
| 继续执行 | 某个任务失败后继续执行其他任务，全部完成后由成功/失败比例决定 | ✓ |
| 部分停止 | 某个任务失败后停止剩余等待中的任务，但已启动的任务继续完成 | |

**User's choice:** 继续执行
**Notes:** 符合 Success Criteria 第 4 条——单个任务执行失败不影响其他任务继续执行

---

## 确认弹窗 UI

| Option | Description | Selected |
|--------|-------------|----------|
| 简单摘要 | 弹窗显示已选任务数量 + 并发数滑块 + 确认/取消按钮 | ✓ |
| 任务清单 + 可取消勾选 | 弹窗列出所有勾选的任务名称，用户可取消勾选某些任务后再启动 | |

**User's choice:** 简单摘要
**Notes:** 保持简洁

---

## API 路由设计

| Option | Description | Selected |
|--------|-------------|----------|
| 独立 batches 路由 | POST /batches 创建批次，GET /batches/{id} 查进度 | ✓ |
| 挂在 runs 路由下 | POST /runs/batch 创建批次，GET /runs/batch/{id} 查进度 | |

**User's choice:** 独立 batches 路由
**Notes:** 职责分离清晰

---

## 状态流转设计

| Option | Description | Selected |
|--------|-------------|----------|
| 二级状态 | batch pending/running/completed + run pending/running/success/failed | ✓ |
| 仅 run 级状态 | 前端轮询检查是否所有 run 都不是 pending/running | |

**User's choice:** 二级状态
**Notes:** Batch 状态由子 Run 状态聚合

---

## Claude's Discretion

- Batch 模型具体字段类型和默认值
- 确认弹窗组件的具体 UI 样式和布局
- 并发数滑块的步长和默认值展示
- BatchExecutionService 的内部实现细节
- API 响应的具体 JSON 结构

## Deferred Ideas

- 批量取消操作 — v2 BATCH-05
- 批量重试失败任务 — v2 BATCH-06
- 批量执行汇总报告 — v2 BATCH-04
- 批量进度 UI 页面 — Phase 73
