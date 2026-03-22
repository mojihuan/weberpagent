# aiDriveUITest

## What This Is

AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例。基于 Browser-Use + 阿里云 Qwen 3.5 Plus 构建，实现「自然语言描述 → AI 决策 → Playwright 执行」的自动化测试流程。

**目标用户**: QA 测试人员
**核心场景**: 用中文描述测试步骤，AI 自动理解、执行并生成测试报告

## Core Value

**让 QA 用自然语言写测试用例，AI 自动执行并生成报告。**

这是产品的核心价值。如果这个流程跑不通，产品就没有意义。

## Current State: v0.4.1 断言系统调通 ✓ COMPLETE

**已交付版本:**
- v0.1 MVP (2026-03-14) - 基础功能
- v0.2 前置条件/接口断言/动态数据 (2026-03-17)
- v0.2.1 测试用例调通 (2026-03-18)
- v0.3 前置条件集成 (2026-03-18)
- v0.3.1 数据获取方法集成 (2026-03-19)
- v0.3.2 测试与Bug修复 (2026-03-20) - 稳定版本
- v0.4.0 断言系统集成 (2026-03-21) - ✓ SHIPPED
- v0.4.1 断言系统调通 (2026-03-22) - ✓ SHIPPED

**v0.4.1 断言系统调通 成果:**
- Phase 28: 后端字段发现 — 扫描 base_assertions_field.py，获取约 300 个可用字段
- Phase 29: 前端字段配置 UI — 字段选择器，支持三层参数配置
- Phase 30: 断言执行适配器 — execute_assertion_method() 接受三层参数
- Phase 31: E2E 测试 — 3 个 Playwright 测试验证端到端流程
- Phase 32: 三层参数缺口关闭 — execute_all_assertions() 正确传递三层参数

**三层参数架构现已完整:**
- api_params: API 查询参数 (i, j, k 等)
- field_params: 断言字段值 (saleTime, salesOrder 等)
- params: 向后兼容参数

## Previous Milestone: v0.4.1 断言系统调通 ✓ COMPLETE

**Goal:** 修正断言系统的参数结构，使其符合正确的三层设计，支持完整的断言字段配置。 — **ACHIEVED**

**v0.4.1 已完成功能:**
- ✓ 后端扫描 base_assertions_field.py 获取可用字段列表
- ✓ 前端 UI 支持三层参数配置 (api_params, field_params, params)
- ✓ 端到端验证断言执行流程正确
- ✓ execute_all_assertions() 正确传递三层参数到 execute_assertion_method()

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

### Active

(下一里程碑需求待规划)

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
- 5 unit tests with pre-existing isolation issues (test_external_bridge, test_browser_cleanup, test_precondition_service)
- Nyquist Wave 0 tasks pending (tests defined but not run)
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
| ExternalAssertionBridge 复用 Bridge 模式 | 与 ExternalPreconditionBridge 一致 | ✓ Good |
| execute_assertion_method() 异步执行 + 30s 超时 | 防止断言方法阻塞 | ✓ Good |
| AssertionError 解析提取字段级结果 | 精确错误定位 | ✓ Good |
| 断言结果存入 context 非 fail-fast | 收集所有结果后汇总 | ✓ Good |

---
*Last updated: 2026-03-22 after v0.4.1 milestone completion*
