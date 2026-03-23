# aiDriveUITest

## What This Is

AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例。基于 Browser-Use + 阿里云 Qwen 3.5 Plus 构建，实现「自然语言描述 → AI 决策 → Playwright 执行」的自动化测试流程。

**目标用户**: QA 测试人员
**核心场景**: 用中文描述测试步骤，AI 自动理解、执行并生成测试报告

## Core Value

**让 QA 用自然语言写测试用例，AI 自动执行并生成报告。**

这是产品的核心价值。如果这个流程跑不通，产品就没有意义。

## Current Milestone: v0.5.0 项目云端部署

**Goal:** 将 aiDriveUITest 项目部署到国产云端服务器，并完成 Git 仓库迁移

**Target features:**
- Git 仓库迁移 (当前项目 + webseleniumerp 外置项目)
- 云服务器选型调研 (预算100元/月以下)
- 云端部署执行 (后端 + 前端 + 数据库)

**Key constraints:**
- 预算: 100元/月以下
- 需要运行浏览器 (Playwright Chromium)
- 需要持久化存储 (SQLite)
- LLM 调用需要稳定网络

## Current Status

**最新版本:** v0.4.2 人工验证断言系统 ✓ SHIPPED (2026-03-23)

断言系统已完成人工验证，`sell_sale_item_list_assert` 能正确执行并返回结果。修复了 5 个 bug，创建了完整的使用指南文档。

**已交付版本:**
- v0.1 MVP (2026-03-14) - 基础功能
- v0.2 前置条件/接口断言/动态数据 (2026-03-17)
- v0.2.1 测试用例调通 (2026-03-18)
- v0.3 前置条件集成 (2026-03-18)
- v0.3.1 数据获取方法集成 (2026-03-19)
- v0.3.2 测试与Bug修复 (2026-03-20) - 稳定版本
- v0.4.0 断言系统集成 (2026-03-21) - ✓ SHIPPED
- v0.4.1 断言系统调通 (2026-03-22) - ✓ SHIPPED
- v0.4.2 人工验证断言系统 (2026-03-23) - ✓ SHIPPED

**三层参数架构现已完整:**
- api_params: API 查询参数 (i, j, k 等)
- field_params: 断言字段值 (saleTime, salesOrder 等)
- params: 向后兼容参数

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

v0.4.0 断言系统集成 (2026-03-21):

- ✓ 断言方法发现 (PcAssert/MgAssert/McAssert) — DISC-01/02/03/04
- ✓ API 端点 GET /external-assertions/methods — DISC-05
- ✓ AssertionSelector 组件（分组、搜索、多选）— UI-01/05
- ✓ 参数配置 UI (headers/data/i/j/k) — UI-02/03/04
- ✓ TaskForm 集成断言配置 Tab — UI-06
- ✓ ExternalAssertionBridge 执行引擎 — EXEC-01/02
- ✓ resolve_headers() token 解析 — EXEC-03
- ✓ AssertionError 解析 + 字段级结果 — EXEC-04
- ✓ Context 存储断言结果 — EXEC-05
- ✓ 非 fail-fast 收集所有结果 — EXEC-06

v0.4.2 人工验证断言系统 (2026-03-23):

- ✓ 断言执行成功 — sell_sale_item_list_assert 正确执行 — ASSERT-01/02/03/04
- ✓ Bug 修复 — 修复 5 个 bug（字段命名、Headers解析、时间偏移、UI优化）— BUG-01/02
- ✓ 文档完善 — 创建《断言系统使用指南》(353行) — DOC-01/02

### Active

**v0.5.0 项目云端部署:**
- [ ] **GIT-01**: 将 weberpagent 项目 git 源迁移到用户自己的仓库
- [ ] **GIT-02**: 将 webseleniumerp 外置项目 git 源迁移到用户自己的仓库
- [ ] **CLOUD-01**: 调研国产云服务器性价比方案 (100元/月以下)
- [ ] **CLOUD-02**: 选择并购买云服务器
- [ ] **DEPLOY-01**: 部署后端服务 (FastAPI + uvicorn)
- [ ] **DEPLOY-02**: 部署前端服务 (React + Nginx)
- [ ] **DEPLOY-03**: 配置数据库持久化 (SQLite)
- [ ] **DEPLOY-04**: 配置浏览器环境 (Playwright Chromium)
- [ ] **DEPLOY-05**: 配置域名和 HTTPS (可选)

### Out of Scope

- 用户认证/权限管理 — 单用户本地使用
- 多语言支持 — 只支持中文
- 高可用/负载均衡 — 单服务器足够
- 自动扩缩容 — 预算有限，固定配置

## Context

**技术背景:**
- 后端 FastAPI + Python (~20,840 LOC)
- 前端 React + Vite + Tailwind (~345 LOC 组件)
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
- 5 unit tests with pre-existing isolation issues (test_external_bridge, test_browser_cleanup, test_precondition_service)
- Nyquist Wave 0 tasks pending (tests defined but not run)

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
| ExternalAssertionBridge 复用 Bridge 模式 | 与 ExternalPreconditionBridge 一致 | ✓ Good |
| execute_assertion_method() 异步执行 + 30s 超时 | 防止断言方法阻塞 | ✓ Good |
| AssertionError 解析提取字段级结果 | 精确错误定位 | ✓ Good |
| 断言结果存入 context 非 fail-fast | 收集所有结果后汇总 | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-23 - v0.5.0 milestone started*
