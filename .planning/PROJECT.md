# aiDriveUITest

## What This Is

AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例。基于 Browser-Use + 阿里云 Qwen 3.5 Plus 构建，实现「自然语言描述 → AI 决策 → Playwright 执行」的自动化测试流程。

**目标用户**: QA 测试人员
**核心场景**: 用中文描述测试步骤，AI 自动理解、执行并生成测试报告

## Core Value

**让 QA 用自然语言写测试用例，AI 自动执行并生成报告。**

这是产品的核心价值。如果这个流程跑不通，产品就没有意义。

## Requirements

### Validated

从现有代码推断的已实现功能：

- ✓ 任务管理 (创建/编辑/复制/删除测试任务) — existing
- ✓ AI 执行 (Browser-Use + Qwen 3.5 Plus 驱动) — existing
- ✓ 实时监控 (SSE 推送执行进度) — existing
- ✓ 测试报告 (截图、断言结果、耗时统计) — existing
- ✓ 断言系统 (URL 检查、文本存在、无错误等类型) — existing
- ✓ LLM 适配器 (OpenAI/Qwen/DeepSeek 多后端支持) — existing

### Active

v0.1 需要修复/完善的功能：

- [ ] 数据库结构优化 (当前结构差，需要重构)
- [ ] 前端数据显示修复 (当前数据显示有问题)
- [ ] 前后端完整打通 (确保完整流程可用)
- [ ] 代码结构整理 (当前项目结构混乱)

### Out of Scope

v0.1 明确排除的功能：

- 用户认证/权限管理 — v0.1 单用户，本地使用，不需要登录
- 任务调度 (定时执行/任务依赖) — 复杂度高，推迟到 v0.2
- 服务器部署 — v0.1 只需本地开发环境运行
- 多语言支持 — 只支持中文

## Context

**技术背景**:
- 项目已开发一段时间，技术栈选型已完成
- 后端 FastAPI + Python 基本可用
- 前端 React + Vite + Tailwind 已搭建
- 数据库使用 SQLite (aiosqlite)

**已知问题**:
- 数据库结构设计不合理，需要优化
- 前端数据显示存在问题
- 代码结构混乱，需要整理

**技术栈**:
| 层级 | 技术 |
|------|------|
| 前端 | React 18, TypeScript, Vite, Tailwind CSS |
| 后端 | Python 3.11, FastAPI, Pydantic, SQLAlchemy |
| AI | Browser-Use, 阿里云 Qwen 3.5 Plus |
| 浏览器 | Playwright (Chromium) |
| 通信 | REST API + SSE |
| 存储 | SQLite |

## Constraints

- **技术栈**: 已选型完成，不做更换
- **时间**: 1-2 周内完成 v0.1
- **部署**: 仅需本地开发环境
- **LLM**: 必须支持阿里云 DashScope (国内使用)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 先重构再修复 | 项目结构混乱，直接修 bug 会更混乱 | — Pending |
| 排除用户认证 | v0.1 单用户本地使用，降低复杂度 | — Pending |
| 排除任务调度 | 非核心功能，推迟到 v0.2 | — Pending |

---
*Last updated: 2026-03-14 after initialization*
