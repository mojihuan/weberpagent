# aiDriveUITest

## What This Is

AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例。基于 Browser-Use + 阿里云 Qwen 3.5 Plus 构建，实现「自然语言描述 → AI 决策 → Playwright 执行」的自动化测试流程。

**目标用户**: QA 测试人员
**核心场景**: 用中文描述测试步骤，AI 自动理解、执行并生成测试报告

## Core Value

**让 QA 用自然语言写测试用例，AI 自动执行并生成报告。**

这是产品的核心价值。如果这个流程跑不通，产品就没有意义。

## Current State: v0.3.1 已交付

**已交付版本:**
- v0.1 MVP (2026-03-14) - 基础功能
- v0.2 前置条件/接口断言/动态数据 (2026-03-17)
- v0.2.1 测试用例调通 (2026-03-18)
- v0.3 前置条件集成 (2026-03-18)
- v0.3.1 数据获取方法集成 (2026-03-19)

**v0.3.1 关键成果:**
1. 后端数据获取桥接 - 扫描 base_params.py，提供方法列表和执行 API
2. 前端 DataMethodSelector - 4 步向导：方法选择 → 参数配置 → 数据预览 → 变量命名
3. ContextWrapper 集成 - 支持同步数据方法调用和变量存储
4. 变量传递 - 测试步骤中支持 `{{变量名}}` 语法

## Next Milestone: TBD

规划下一版本需求...

## Requirements

### Validated

v0.1-v0.3 已交付功能：

- ✓ 任务管理 (创建/编辑/复制/删除测试任务) — v0.1
- ✓ AI 执行 (Browser-Use + Qwen 3.5 Plus 驱动) — v0.1
- ✓ 实时监控 (SSE 推送执行进度) — v0.1
- ✓ 测试报告 (截图、断言结果、耗时统计) — v0.1
- ✓ 页面断言系统 (URL 检查、文本存在、无错误等类型) — v0.1
- ✓ LLM 适配器 (OpenAI/Qwen/DeepSeek 多后端支持) — v0.1
- ✓ 前置条件系统 (Python 代码格式，Jinja2 变量替换) — v0.2
- ✓ 接口断言集成 (ApiAssertionService，时间/数据断言) — v0.2
- ✓ 随机数生成器 (SF物流单号、手机号、IMEI、序列号) — v0.2
- ✓ 动态数据获取 (外部模块加载) — v0.2
- ✓ 登录用例调通 (端到端执行成功) — v0.2.1
- ✓ 销售出库用例调通 (前置条件/动态数据/API断言验证) — v0.2.1
- ✓ 外部前置条件集成 (WEBSERP_PATH, OperationCodeSelector) — v0.3

v0.3.1 数据获取方法集成 (2026-03-19):

- ✓ 扫描 base_params.py 获取 xxx_data() 查询方法 — DATA-01
- ✓ 前端表单列出数据获取方法（按模块分组）— UI-01
- ✓ 参数配置 UI（支持 i/j/k 等筛选参数）— UI-02
- ✓ 字段提取路径配置（如 `[0].imei`）— UI-03
- ✓ 生成变量名并在测试步骤中使用 `{{变量名}}` — INT-01/02/03

### Active

待规划下一版本需求...

### Out of Scope

- 用户认证/权限管理 — 单用户本地使用
- 服务器部署 — 只需本地开发环境运行
- 多语言支持 — 只支持中文

## Context

**技术背景:**
- 后端 FastAPI + Python (~13,700 LOC)
- 前端 React + Vite + Tailwind (~4,300 LOC)
- 数据库使用 SQLite (aiosqlite)

**技术栈:**
| 层级 | 技术 |
|------|------|
| 前端 | React 18, TypeScript, Vite, Tailwind CSS |
| 后端 | Python 3.11, FastAPI, Pydantic, SQLAlchemy |
| AI | Browser-Use, 阿里云 Qwen 3.5 Plus |
| 浏览器 | Playwright (Chromium) |
| 通信 | REST API + SSE |
| 存储 | SQLite |

**Known Tech Debt:**
- Nyquist Wave 0 tasks pending (tests defined but not run)
- Pre-existing TypeScript errors in ApiAssertionResults.tsx, RunList.tsx (not blocking)
- Phase 11-12 (Bug 修复、文档指南) 推迟到后续版本

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
| 外部模块路径通过 WEBSERP_PATH 配置 | 复用现有 webseleniumerp 项目 | ✓ Good |
| 前置条件失败时立即终止整个测试 | Fail-fast 模式 | ✓ Good |
| ApiAssertionService 收集所有结果 (非终止) | 允许部分失败 | ✓ Good |
| ExternalPreconditionBridge 隔离外部项目导入 | 解耦依赖，支持缓存 | ✓ Good |
| OperationCodeSelector 模块分组显示 | 按业务模块组织，便于查找 | ✓ Good |
| DataMethodSelector 4 步向导模式 | 分步引导用户完成数据配置 | ✓ Good |
| ContextWrapper 提供类字典接口 | 向后兼容，支持 context['var'] 语法 | ✓ Good |
| context.get_data() 同步调用模式 | 使用 nest_asyncio 处理嵌套事件循环 | ✓ Good |
| 代码生成格式: context.get_data('ClassName', 'method', params) | 匹配后端签名，包含类名 | ✓ Good |

---
*Last updated: 2026-03-19 after v0.3.1 milestone completion*
