# aiDriveUITest

## What This Is

AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例。基于 Browser-Use + 阿里云 Qwen 3.5 Plus 构建，实现「自然语言描述 → AI 决策 → Playwright 执行」的自动化测试流程。

**目标用户**: QA 测试人员
**核心场景**: 用中文描述测试步骤，AI 自动理解、执行并生成测试报告

## Core Value

**让 QA 用自然语言写测试用例，AI 自动执行并生成报告。**

这是产品的核心价值。如果这个流程跑不通，产品就没有意义。

## Current Milestone: v0.7.0 更多操作边界测试

**Goal:** 扩展 AI Agent 的操作能力边界，支持表格复杂交互、文件导入、键盘操作和缓存断言等 ERP 测试中常见但尚未覆盖的操作场景。

**Target features:**
- 表格单选/全选 — 表格中的 checkbox 单行选择和全选操作
- 表格超链接/图标点击 — 表格中可点击的链接和图标操作
- 导入 Excel/图片 — 文件上传（Excel 导入、图片上传）
- 断言参数调优 — headers、i、j 参数组合的断言验证
- 键盘操作 — 粘贴(Ctrl+V)、回车(Enter)、ESC 等键盘快捷键
- 缓存断言 — 执行前查询获取物品编号并缓存，执行后用缓存值断言

## Current State

**最新版本:** v0.6.3 Agent 可靠性优化 ✓ SHIPPED (2026-03-28)

通过中间层监控 + Prompt 优化解决 Agent 循环重试、字段误填、步骤遗漏等核心问题。

**Server online**: 121.40.191.49

**已交付版本:**
- v0.1 ~ v0.5.0: 基础功能 → 断言系统 → 云端部署
- v0.6.2: 回归原生 browser-use (2026-03-27)
- v0.6.3: Agent 可靠性优化 (2026-03-28)

## Requirements

### Validated

**v0.6.3 Agent 可靠性优化 (2026-03-28):**
- ✓ StallDetector — 连续失败检测 + DOM 指纹停滞检测 — Phase 48
- ✓ PreSubmitGuard — 正则提取期望值 + 提交拦截 — Phase 48
- ✓ TaskProgressTracker — 4 种步骤格式解析 + 进度预警 — Phase 48
- ✓ MonitoredAgent — _pending_interventions 桥 + _execute_actions 拦截 — Phase 48
- ✓ ENHANCED_SYSTEM_MESSAGE — 5 段式 ERP 指导 + browser-use 参数调优 — Phase 49
- ✓ AgentService 集成 — MonitoredAgent 替换 + step_callback 检测器调用 — Phase 50
- ✓ E2E 验证 — 60/60 测试通过，94% 覆盖率，ERP 测试无循环违规 — Phase 51

<details>
<summary>v0.6.2 及更早版本的已验证需求</summary>

v0.6.2 回归原生 browser-use (2026-03-27):
- ✓ 移除 scroll_table 工具、TD 后处理、JS fallback、元素诊断、循环干预
- ✓ step_callback 简化为基本日志功能

v0.5.0 项目云端部署 (2026-03-24):
- ✓ Git 仓库迁移、阿里云部署、FastAPI + Gunicorn + Nginx

v0.1-v0.4.2 核心功能:
- ✓ 任务管理、AI 执行、实时监控、测试报告
- ✓ 前置条件系统、接口断言、动态数据获取
- ✓ 断言系统、数据获取方法集成
- ✓ 三层参数架构 (api_params, field_params, params)

</details>

### Active

**v0.7.0 更多操作边界测试:**
- TBL-01: 表格 checkbox 单选操作
- TBL-02: 表格 checkbox 全选操作
- TBL-03: 表格超链接点击
- TBL-04: 表格图标按钮点击
- IMP-01: 导入 Excel 文件上传
- IMP-02: 导入图片文件上传
- AST-01: 断言 headers 参数验证
- AST-02: 断言 i、j 参数组合验证
- KB-01: 键盘粘贴操作 (Ctrl+V)
- KB-02: 键盘回车操作 (Enter)
- KB-03: 键盘 ESC 操作
- CAC-01: 执行前查询缓存物品编号
- CAC-02: 执行后用缓存值断言

### Backlog

- PreSubmitGuard DOM 值提取 — 当前 actual_values=None，需实现 DOM 值读取才能主动拦截
- 5 个预先存在的测试隔离问题 (test_external_bridge, test_browser_cleanup 等)

### Out of Scope

- 用户认证/权限管理 — 单用户本地使用
- 多语言支持 — 只支持中文
- 高可用/负载均衡 — 单服务器足够

## Context

**技术背景:**
- 后端 FastAPI + Python
- 前端 React + Vite + Tailwind
- 数据库 SQLite (aiosqlite)

**技术栈:**
| 层级 | 技术 |
|------|------|
| 前端 | React 18, TypeScript, Vite, Tailwind CSS |
| 后端 | Python 3.11, FastAPI, Pydantic, SQLAlchemy |
| AI | Browser-Use, 阿里云 Qwen 3.5 Plus |
| 浏览器 | Playwright (Chromium) |
| 通信 | REST API + SSE |
| 存储 | SQLite |

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 中间层 + Prompt 优化，不侵入 browser-use 源码 | 升级安全，不 fork | ✓ Good |
| _pending_interventions 桥接模式 | step_callback 存储，_prepare_context 注入 | ✓ Good |
| 停滞阈值 2 次失败即切换 | 比 browser-use 默认更激进 | ✓ Good |
| frozen=True dataclass for StallResult/GuardResult | 不可变性保证 | ✓ Good |
| DOM 指纹用 (element_count, url, dom_hash[:12]) | 避免完整 DOM 文本哈希 | ✓ Good |
| ENHANCED_SYSTEM_MESSAGE 中文优先 | Qwen 中文理解更强 | ✓ Good |
| Agent 参数硬编码在 agent_service.py | 简化配置，避免过度设计 | ✓ Good |
| 检测器实例每次 run 创建新的 | 避免跨 run 状态残留 | ✓ Good |
| run_logger.log() 使用 detail= 而非 message= | 避免位置/关键字参数冲突 | ✓ Good |
| 前置条件使用 Python 代码格式 | 灵活性高，可直接调用 API | ✓ Good |
| exec() + asyncio.wait_for() 执行代码 | 30 秒超时保护 | ✓ Good |
| 断言结果存入 context 非 fail-fast | 收集所有结果后汇总 | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

---
*Last updated: 2026-03-30 after v0.7.0 milestone start*
