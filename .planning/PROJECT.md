# aiDriveUITest

## What This Is

AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例。基于 Browser-Use + 阿里云 Qwen 3.5 Plus 构建，实现「自然语言描述 → AI 决策 → Playwright 执行」的自动化测试流程。

**目标用户**: QA 测试人员
**核心场景**: 用中文描述测试步骤，AI 自动理解、执行并生成测试报告

## Core Value

**让 QA 用自然语言写测试用例，AI 自动执行并生成报告。**

这是产品的核心价值。如果这个流程跑不通，产品就没有意义。

## Current State

**最新版本:** v0.10.1 代码登录及 Agent 复用登录的浏览器状态 (shipped 2026-04-21)
**Server online**: 121.40.191.49
**当前进度:** 里程碑归档完成，准备下一里程碑

## Current Milestone: Planning Next

**Goal:** 待定

**已交付版本:**
- v0.1 ~ v0.5.0: 基础功能 → 断言系统 → 云端部署
- v0.6.2: 回归原生 browser-use (2026-03-27)
- v0.6.3: Agent 可靠性优化 (2026-03-28)
- v0.7.0: 更多操作边界测试 (2026-04-01)
- v0.8.0: 报告完善与 UI 优化 (2026-04-03)
- v0.8.1 ~ v0.8.4: 表格填写优化与调查 (2026-04-06 ~ 2026-04-07)
- v0.9.0: Excel 批量导入功能开发 (2026-04-09)
- v0.9.1: ERP 全面集成重构 (2026-04-12)
- v0.9.2: Cookie 预注入免登录 (2026-04-17)
- v0.10.0: Agent 执行速度优化 (2026-04-18)
- v0.10.1: 代码登录及 Agent 复用登录的浏览器状态 (2026-04-21)

## Requirements

### Validated

**v0.8.1 修复销售出库表格填写问题 (2026-04-06):**
- ✓ DOM-PATCH-01: td cell 文本内容检测 + ERP 表格 input 可见性 patch — Phase 62
- ✓ PROMPT-01: Section 9 click-to-edit 工作流指导 + 字段混淆警告 — Phase 62
- ✓ E2E-01: 销售出库场景 E2E 验证 (26步完成，销售金额=150) — Phase 62

**v0.8.0 报告完善与 UI 优化 (2026-04-03):**
- ✓ FMT-01/02/03: AI 推理格式 Eval/Verdict/Memory/Goal 分行彩色 badge 展示 — Phase 57
- ✓ EXEC-01/02/03: 执行监控 StepTimeline 统一时间线，前置条件/断言步骤交错排列 — Phase 58
- ✓ RPT-01/02/03: 报告详情统一时间线，PreconditionResult + global sequence_number — Phase 59
- ✓ FORM-01/02: 任务表单移除 api_assertions tab，业务断言直接展示 — Phase 60
- ✓ E2E 验证: 6/6 检查 PASS — Phase 61

**v0.7.0 更多操作边界测试 (2026-04-01):**
- ✓ KB-01/02/03: 键盘操作 (Enter/Escape/Control+a) — Phase 52/56
- ✓ TBL-01/02/03/04: 表格交互 (checkbox/超链接/图标) — Phase 53/56
- ✓ IMP-01/02: 文件导入 (Excel/图片) — Phase 54/56
- ✓ AST-01/02: 断言参数验证 (headers/i/j) — Phase 56
- ⏭ CAC-01/02: 缓存断言 — Deferred，推迟到有实际需求时实现

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

### Validated (v0.8.2)

- ✓ DIFF-01: 对比 v0.4.0 和当前版本 browser-use 初始化代码差异 — Phase 63
- ✓ DIFF-02: 对比 Playwright 配置（headless/headed 设置）— Phase 63
- ✓ DIFF-03: 分析 browser-use 版本变化和 API 差异 — Phase 63
- ✓ DIFF-04: 分析 agent_service.py 中 Agent/Browser 配置演变 — Phase 63
- ✓ RPT-01: 输出分析报告（完整技术版 + 精简摘要版）— Phase 64

### Validated (v0.9.1)

- ✓ CACHE-01: CacheService.cache() + cached() 基本存取 — Phase 74
- ✓ CACHE-02: cached() 返回深拷贝，外部修改不影响缓存 — Phase 74
- ✓ CACHE-03: ContextWrapper.cache()/cached() 委托到 CacheService — Phase 74
- ✓ ACCT-01: AccountService.resolve("main") 返回不可变 AccountInfo — Phase 75
- ✓ ACCT-02: resolve() 未知角色抛出 ValueError 列出所有可用角色 — Phase 75
- ✓ ACCT-03: get_login_url() 从 settings.erp_base_url 组合 URL — Phase 75

### Validated (v0.10.1)

- ✓ AUTH-01: Vue SPA 编程式登录修复 — dispatchEvent(MouseEvent) 替代 btn.click() — Phase 87
- ✓ AUTH-02: 代码登录失败时自动回退到文字登录模式，包含角色名和失败原因的 warning 日志 — Phase 87
- ✓ CLEAN-01: auth_service 职责单一 — 只负责 HTTP token 获取 — Phase 88
- ✓ CLEAN-02: storage_state 构造内联到 self_healing_runner — Phase 88
- ✓ TEST-01: _build_storage_state 和 _get_storage_state_for_role 单元测试 (5 tests) — Phase 89
- ✓ TEST-02: 27 单元测试全部通过，mock 路径更新完毕 — Phase 89

### Validated (v0.9.0)

- ✓ TMPL-01: Excel 模版生成 (styled headers, DataValidation, README sheet) — Phase 70
- ✓ TMPL-02: max_steps 列 1-100 下拉验证 — Phase 70
- ✓ IMPT-01: Excel 上传 + 行级验证 — Phase 71
- ✓ IMPT-02: 前端 ImportModal 三步状态机 (upload→preview→result) — Phase 71
- ✓ IMPT-03: 原子批量 Task 创建 + 回滚 — Phase 71
- ✓ BATCH-01: 批量执行 + Semaphore 并发控制 — Phase 72
- ✓ BATCH-02: Semaphore 默认 2，上限 4 — Phase 72
- ✓ BATCH-03: 批量进度 UI + 轮询 + 点击导航 — Phase 73

### Validated (v0.8.4 Phase 69)

- ✓ ANTI-03: step_callback 失败模式检测集成 — Phase 69
- ✓ RECOV-02: detect_failure_mode → update_failure_tracker 调用链 — Phase 69
- ✓ RECOV-03: Section 9 失败恢复规则（三种模式）— Phase 69
- ✓ PROMPT-01: Section 9 行标识定位规则 — Phase 69
- ✓ PROMPT-02: Section 9 反重复操作规则 — Phase 69
- ✓ PROMPT-03: Section 9 策略优先级规则 — Phase 69

### Validated (v0.8.3)

- ✓ ANALYSIS-01: headless/headed 差异与表格定位不准的因果关联 — 部分，headless 为加剧因素 — Phase 65
- ✓ ANALYSIS-02: headed 模式恢复后 DOM Patch (5 patches) 有效性评估 — 4/5 仍必要 — Phase 65
- ✓ ANALYSIS-03: headed 模式恢复后 Section 9 Prompt 有效性评估 — 确认保留 — Phase 65
- ✓ OPTIMIZE-01: 按行定位 + 直接找 input 的表格输入策略设计 — Phase 66
- ✓ OPTIMIZE-02: 反重复机制设计（同 index 失败 2 次自动切换）— Phase 66
- ✓ OPTIMIZE-03: 原生 input → DOM 查询 → evaluate JS 策略优先级 — Phase 66
- ✓ OPTIMIZE-04: 失败恢复策略设计（无变化/误列/编辑态误判）— Phase 66

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
| click-to-edit td 检测取代 input placeholder 检测 | Ant Design 表格不预渲染 input | ✓ Good |
| DOM Patch 5 patches 覆盖 ERP 特殊模式 | ERP 表格 click-to-edit + checkbox 等 | ✓ Good |
| openpyxl 唯一依赖，零新依赖 | 已安装 3.1.5，减少供应链风险 | ✓ Good |
| 导入两阶段模式 (preview + confirm) | confirm 重新解析而非缓存，无状态设计 | ✓ Good |
| 批量进度轮询 (2s) 而非 SSE | 避免 multiplexer 架构改造 | ✓ Good |
| Semaphore 默认并发 2，硬上限 4 | 基于部署服务器内存的安全边界 | ✓ Good |
| _active_batches 模块字典防 GC | asyncio.create_task 无引用会被回收 | ✓ Good |
| SQLite busy_timeout 30 秒 | 并发写入场景下避免 immediate lock | ⚠️ Revisit — 需实测高并发 |
| Vue SPA 需要 dispatchEvent(MouseEvent) 登录 | btn.click() 不触发 Vue 事件绑定 | ✓ Good |
| localStorage 注入不可行 | Vuex/Pinia store 初始化后才读 localStorage，router guard 检查 store | ✓ Good |
| storage_state 构造内联到 self_healing_runner | 消费者唯一，保持模块解耦 | ✓ Good |
| browser-use page.evaluate 返回复杂对象为 string | 用 JSON.stringify + json.loads 序列化 | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

---
*Last updated: 2026-04-21 after v0.10.1 milestone*
