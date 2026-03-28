# aiDriveUITest

## What This Is

AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例。基于 Browser-Use + 阿里云 Qwen 3.5 Plus 构建，实现「自然语言描述 → AI 决策 → Playwright 执行」的自动化测试流程。

**目标用户**: QA 测试人员
**核心场景**: 用中文描述测试步骤，AI 自动理解、执行并生成测试报告

## Core Value

**让 QA 用自然语言写测试用例，AI 自动执行并生成报告。**

这是产品的核心价值。如果这个流程跑不通，产品就没有意义。

## Current Milestone: v0.6.3 Agent 可靠性优化

**Goal:** 通过中间层监控和 Prompt 优化解决 Agent 循环重试、字段误填、步骤遗漏、提交未校验等核心问题，提升测试执行成功率。

**Target features:**
- **StallDetector（停滞检测器）** — 检测 Agent 对同一元素的重复失败操作，2 次即干预
- **PreSubmitGuard（提交前校验器）** — 提交前校验关键字段值，阻止错误提交
- **TaskProgressTracker（任务进度追踪器）** — 追踪任务完成进度，步数紧张时发出警告
- **ENHANCED_SYSTEM_MESSAGE（增强系统提示词）** — click-to-edit 模式指导、失败恢复规则
- **AgentService 集成** — 将以上模块集成到 step_callback，通过 `_message_manager._add_context_message()` 注入干预消息

**Key context:**
- v0.6.2 已回归原生 browser-use，移除了所有自定义扩展
- 运行记录 `outputs/7fcea593` 暴露了 5 个核心问题：表格 click-to-edit 不可见、循环重试、值误填、步骤遗漏、提交未校验
- 计划依赖 browser-use 0.12.x 的 `_message_manager._add_context_message()` API，需验证可行性
- 核心风险：消息注入机制可能不可行，需退而求其次

**Key constraints:**
- 不侵入 browser-use 源码，升级安全
- 保持 Qwen 3.5 Plus 作为 LLM，通过工程手段弥补指令遵守能力不足

## Current Status

**最新版本:** v0.5.0 项目云端部署 ✓ SHIPPED (2026-03-24)

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
- v0.5.0 项目云端部署 (2026-03-24) - ✓ SHIPPED

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

(None - all Phase 48 requirements validated)

### Validated

**Phase 48 Agent 可靠性优化 (2026-03-28):**
- [x] **MON-01**: StallDetector 检测 2 次连续同目标失败 → 干预
- [x] **MON-02**: StallDetector 检测 3 次连续相同 DOM 指纹 → 干预
- [x] **MON-03**: StallDetector 成功步骤重置失败计数器
- [x] **MON-04**: PreSubmitGuard 从任务描述提取期望值（金额、付款状态）
- [x] **MON-05**: PreSubmitGuard 字段不匹配时拦截提交
- [x] **MON-06**: PreSubmitGuard 无期望值时不拦截
- [x] **MON-07**: TaskProgressTracker 解析 4 种步骤格式
- [x] **MON-08**: TaskProgressTracker 步数不足时预警
- [x] **SUB-01**: MonitoredAgent._prepare_context() 注入干预消息
- [x] **SUB-02**: step_callback 存储到 _pending_interventions
- [x] **SUB-03**: _execute_actions() 拦截提交点击

**Phase 46 代码简化与测试 (2026-03-26):**
- [x] **TEST-01**: 删除过时 scroll_table 测试文件 - 移除 352 行测试代码
- [x] **SIMPLIFY-01**: step_callback 已简化 - 只包含基本日志功能
- [x] **SIMPLIFY-02**: Agent 无自定义工具 - 无 tools= 参数

**Phase 45 代码清理 (2026-03-26):**
- [x] **CLEANUP-01**: 移除 scroll_table_and_input 工具 - 删除 backend/agent/tools/ 目录
- [x] **CLEANUP-02**: 移除 TD 后处理逻辑 - 删除 `_post_process_td_click` 方法及相关调用
- [x] **CLEANUP-03**: 移除 JavaScript fallback - 删除 `_fallback_input` 方法及相关调用
- [x] **CLEANUP-04**: 移除元素诊断日志 - 删除 `_collect_element_diagnostics` 方法及相关调用
- [x] **CLEANUP-05**: 移除循环干预逻辑 - 删除 `LoopInterventionTracker` 类及相关调用

### Validated (Previous Milestones)

**v0.5.0 项目云端部署 (Shipped: 2026-03-24):**
- [x] **GIT-01**: Git 仓库迁移完成
- [x] **CLOUD-01/02**: 阿里云轻量 2核4G (约16.6元/月)
- [x] **DEPLOY-01-04**: FastAPI + Gunicorn + Nginx + SQLite WAL 部署完成
- [x] **DEPLOY-05**: HTTPS 跳过（无域名）

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
*Last updated: 2026-03-28 - Phase 48 complete: 3 detectors + MonitoredAgent integration (40 tests, 10/10 must-haves)*
