# aiDriveUITest

## What This Is

AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例。基于 Browser-Use + 阿里云 Qwen 3.5 Plus 构建，实现「自然语言描述 → AI 决策 → Playwright 执行」的自动化测试流程。

**目标用户**: QA 测试人员
**核心场景**: 用中文描述测试步骤，AI 自动理解、执行并生成测试报告

## Core Value

**让 QA 用自然语言写测试用例，AI 自动执行并生成报告。**

这是产品的核心价值。如果这个流程跑不通，产品就没有意义。

## Current Milestone: v0.3 规划中

**Goal:** 待定

## Requirements

### Validated

v0.1 已交付功能：

- ✓ 任务管理 (创建/编辑/复制/删除测试任务) — v0.1
- ✓ AI 执行 (Browser-Use + Qwen 3.5 Plus 驱动) — v0.1
- ✓ 实时监控 (SSE 推送执行进度) — v0.1
- ✓ 测试报告 (截图、断言结果、耗时统计) — v0.1
- ✓ 页面断言系统 (URL 检查、文本存在、无错误等类型) — v0.1
- ✓ LLM 适配器 (OpenAI/Qwen/DeepSeek 多后端支持) — v0.1
- ✓ 数据库结构优化 — v0.1
- ✓ 前后端完整打通 — v0.1

v0.2 已交付功能：

- ✓ 前置条件系统 (Python 代码格式，exec() 执行，Jinja2 变量替换) — v0.2
- ✓ 接口断言集成 (ApiAssertionService，时间/数据断言，独立报告展示) — v0.2
- ✓ 随机数生成器 (SF物流单号、手机号、IMEI、序列号) — v0.2
- ✓ 动态数据获取 (外部模块加载，ERP_API_MODULE_PATH 配置) — v0.2
- ✓ 数据缓存复用 (PreconditionService.context 持久化) — v0.2
- ✓ 时间计算 (time_now 偏移计算) — v0.2
- ✓ 前端实时监控 (precondition/api_assertion SSE 事件处理) — v0.2

### Active

v0.3 需求待定义：

- [ ] 批量执行 (Excel 导入)
- [ ] 批量运行测试用例
- [ ] 批量执行结果汇总

### Out of Scope

v0.3 明确排除的功能：

- 用户认证/权限管理 — 单用户本地使用
- 服务器部署 — 只需本地开发环境运行
- 多语言支持 — 只支持中文

## Context

**技术背景**:
- v0.2 已完成，前置条件、接口断言、动态数据支持全部实现
- 后端 FastAPI + Python (~13,702 LOC)
- 前端 React + Vite + Tailwind (~4,303 LOC)
- 数据库使用 SQLite (aiosqlite)

**技术栈**:
| 层级 | 技术 |
|------|------|
| 前端 | React 18, TypeScript, Vite, Tailwind CSS |
| 后端 | Python 3.11, FastAPI, Pydantic, SQLAlchemy |
| AI | Browser-Use, 阿里云 Qwen 3.5 Plus |
| 浏览器 | Playwright (Chromium) |
| 通信 | REST API + SSE |
| 存储 | SQLite |

**Known Tech Debt**:
- Nyquist Wave 0 tasks pending (tests defined but not run)
- Pre-existing TypeScript errors in ApiAssertionResults.tsx, RunList.tsx (not blocking)

## Constraints

- **技术栈**: 已选型完成，不做更换
- **部署**: 仅需本地开发环境
- **LLM**: 必须支持阿里云 DashScope (国内使用)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 前置条件使用 Python 代码格式 | 灵活性高，可直接调用 API | ✓ Good |
| 使用 exec() + asyncio.wait_for() 执行代码 | 30 秒超时保护 | ✓ Good |
| 使用 Jinja2 进行 {{变量名}} 替换 | 标准模板引擎，StrictUndefined 防止静默失败 | ✓ Good |
| 外部模块路径通过 ERP_API_MODULE_PATH 配置 | 复用现有项目 API 封装 | ✓ Good |
| 前置条件失败时立即终止整个测试 | Fail-fast 模式 | ✓ Good |
| Store preconditions as JSON string in Text column | 灵活性高 | ✓ Good |
| ApiAssertionService 收集所有结果 (非终止) | 允许部分失败 | ✓ Good |
| TIME_TOLERANCE_SECONDS=60, DECIMAL_TOLERANCE=0.01 | 合理默认值 | ✓ Good |
| 报告中分离 UI/API 断言结果 | 清晰可见 | ✓ Good |

---
*Last updated: 2026-03-17 after v0.2 milestone*
