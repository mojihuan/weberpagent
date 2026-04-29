# aiDriveUITest

## What This Is

AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例。基于 Browser-Use + 阿里云 Qwen 3.5 Plus 构建，实现「自然语言描述 → AI 决策 → Playwright 执行」的自动化测试流程。

**目标用户**: QA 测试人员
**核心场景**: 用中文描述测试步骤，AI 自动理解、执行并生成测试报告

## Core Value

**让 QA 用自然语言写测试用例，AI 自动执行并生成报告。**

这是产品的核心价值。如果这个流程跑不通，产品就没有意义。

## Current State

**最新版本:** v0.10.11 移除自愈功能 (已归档)
**Server online**: 121.40.191.49
**当前状态:** 自愈功能完全移除，代码执行管道简化为一次性 pytest，928 测试通过

## Next Milestone

待规划。使用 `/gsd:new-milestone` 启动下一个里程碑。

## 已交付版本:

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
- v0.10.2: 测试验证与代码可用性修复 (2026-04-23)
- v0.10.3: DOM 深度修复 - 表格单元格选择精确性 (2026-04-23)
- v0.10.4: Playwright 代码验证与任务管理集成 (2026-04-24)
- v0.10.5: 生成测试代码修复与优化 (2026-04-24)
- v0.10.6: 生成测试代码稳定可用 (2026-04-25)
- v0.10.7: 生成测试代码行为优化 (2026-04-27)
- v0.10.8: 生成测试代码前置条件与断言步骤 (2026-04-27)
- v0.10.9: 逐步代码生成 (2026-04-29)
- v0.10.10: 表单填写优化 (2026-04-29)
- v0.10.11: 移除自愈功能 (2026-04-29)

## Requirements

### Active

(None — milestone v0.10.11 complete)

### Validated

**v0.10.11 移除自愈功能 (2026-04-29):**
- ✓ REMOVE-01~04: 删除 SelfHealingRunner/LLMHealer/ErrorClassifier/HealerError 四个自愈模块 — Phase 116
- ✓ SIMPLIFY-01~03: 简化 runs.py 执行管道 + 移除 append_step_async + 清理 code_generator — Phase 117
- ✓ DB-01~03: 清理 Run 模型/schema/repository healing 字段 — Phase 117
- ✓ API-01~02: 简化 API 端点 + 保留代码查看 — Phase 118
- ✓ FE-01~05: 移除前端 healing UI/类型/StatusBadge/CodeViewerModal — Phase 118
- ✓ TEST-01~03: 删除自愈测试 + 清理 mock + 全量回归 928 passed — Phase 119

**v0.10.10 表单填写优化 (2026-04-29):**
- ✓ FORM-01: 重构 _is_erp_table_cell_input 检测逻辑 — 检测 td 内所有可见 input，不依赖 placeholder 精确匹配 — Phase 114
- ✓ FORM-02: 修复 _is_textual_td_cell — td 内已有 ERP input 时不再将 td 标记为 interactive — Phase 114
- ✓ FORM-03: 增强 _patch_assign_interactive_indices — 列头注释语义化，支持任意 input — Phase 114
- ✓ FORM-04: 新增 DOM 诊断日志 — 运行开始时记录实际发现的 input placeholder 值 — Phase 114
- ✓ FORM-05: 更新 prompts.py Section 9 — 同时支持 click-to-edit 和始终可见 input 两种模式 — Phase 115
- ✓ FORM-06: E2E 验证 — 销售出库场景表单填写回归 — Phase 115
- ✓ FORM-01: 重构 _is_erp_table_cell_input 检测逻辑 — 检测 td 内所有可见 input，不依赖 placeholder 精确匹配 — Phase 114
- ✓ FORM-02: 修复 _is_textual_td_cell — td 内已有 ERP input 时不再将 td 标记为 interactive — Phase 114
- ✓ FORM-03: 增强 _patch_assign_interactive_indices — 列头注释语义化，支持任意 input — Phase 114
- ✓ FORM-04: 新增 DOM 诊断日志 — 运行开始时记录实际发现的 input placeholder 值 — Phase 114

**v0.10.9 逐步代码生成 (2026-04-29):**
- ✓ CODEGEN-01: StepCodeBuffer.append_step() 同步翻译，复用 ActionTranslator — Phase 111
- ✓ CODEGEN-02: append_step_async() 弱步骤检测 + LLMHealer 修复 — Phase 111
- ✓ CODEGEN-03: _derive_wait() 智能等待推导 (navigate/duration/click) — Phase 111
- ✓ CODEGEN-04: buffer.assemble() 组装完整测试文件 — Phase 111
- ✓ INTEG-01: runs.py step_callback 每步即时翻译 — Phase 112
- ✓ INTEG-02: buffer.assemble() + 文件写入替代 generate_and_save — Phase 112
- ✓ INTEG-03: code_generator.py 删除废弃方法 — Phase 112
- ✓ VAL-01: StepCodeBuffer 单元测试覆盖 — Phase 111
- ✓ VAL-02: 集成测试验证 step_callback 上下文 — Phase 112
- ✓ VAL-03: 全量回归 316 passed — Phase 113

**v0.10.8 生成测试代码前置条件与断言步骤 (2026-04-27):**
- ✓ PREC-01: generate() 接受 precondition_config，注入 page.goto() + wait_for_load_state() — Phase 108
- ✓ PREC-02: runs.py 传递 effective_target_url 给代码生成器 — Phase 108
- ✓ PREC-03: SelfHealingRunner storage_state + page.goto() 组合验证 — Phase 108
- ✓ ASRT-01: 4 种断言类型映射为 Playwright expect() 语句 — Phase 109
- ✓ ASRT-02: runs.py 传递任务断言给代码生成器 — Phase 109
- ✓ ASRT-03: 断言翻译单元测试 — Phase 109
- ✓ E2E-01: 完整生成代码包含前置条件+操作+断言，语法验证通过 — Phase 110

**v0.10.7 生成测试代码行为优化 (2026-04-27):**
- ✓ TRANSLATE-01: 未知操作显示参数摘要 f"参数={params}" — Phase 105
- ✓ TRANSLATE-02: 10 核心操作翻译质量回归守护 — Phase 105
- ✓ INDENT-01: _build_body 缩进后处理确保 4 空格函数体 — Phase 105
- ✓ INDENT-02: 多行 try-except 嵌套缩进正确对齐 — Phase 105
- ✓ INDENT-03: generate() 输出 ast.parse 验证 — Phase 105
- ✓ LOCATOR-01: get_by_text exact 仅对 ≤4 字符使用 — Phase 106
- ✓ LOCATOR-02: 相对 XPath 优先级 — Phase 106
- ✓ LOCATOR-03: _strip_pua_chars() 过滤 icon font 私有区 — Phase 106
- ✓ LOCATOR-04: 定位器链优先级完整 — Phase 106
- ✓ HEAL-01: _apply_fix 内容匹配多行替换 — Phase 107
- ✓ HEAL-02: DOM 快照精准映射（代码定位器提取）— Phase 107
- ✓ HEAL-03: 结构化 JSON LLM prompt + 20 行上下文 — Phase 107
- ✓ HEAL-04: ast.parse rollback 安全验证 — Phase 107
- ✓ E2E-01: E2E healing pipeline 测试通过 — Phase 107
- ✓ E2E-02: 全量回归测试通过 — Phase 107

**v0.10.6 生成测试代码稳定可用 (2026-04-25):**
- ~~EXEC-01~~: ✓ 修复 pytest 调用参数 `--headed=false` 为正确的 headless 配置 — Phase 102
- ~~EXEC-02~~: ✓ 修复代码生成器输出非 Python 文本 — Phase 102
- ~~EXEC-03~~: ✓ 隔离输出目录，避免 conftest.py 触发 WatchFiles 热重载 — Phase 102
- ~~HEAL-01~~: ✓ 纯函数错误分类器 — 区分环境错误(跳过LLM)与代码错误(继续修复) — Phase 103
- ~~E2E-01~~: ✓ E2E 测试验证代码执行管道 + error_category 全链路传播 — Phase 104

**v0.10.5 生成测试代码修复与优化 (2026-04-24):**
- ~~KEY-01~~: ✓ _CORE_TYPES 键名重命名 click_element→click, input_text→input — Phase 99
- ~~KEY-02~~: ✓ translate/translate_with_llm dispatch + LocatorChainBuilder 对齐 — Phase 99
- ~~KEY-03~~: ✓ _heal_weak_steps 类型检查修复，LLM healing 实际触发 — Phase 99
- ~~KEY-04~~: ✓ 所有测试文件更新，758 tests passed，旧键名零残留 — Phase 99
- ~~CODE-01~~: ✓ 修复 action_translator 键名不匹配 — click/input 映射到正确的 Playwright 代码 — Phase 100
- ~~CODE-02~~: ✓ 补充缺失 action 类型翻译 — wait/done/write_file/switch/extract/search 等非核心操作 — Phase 100
- ~~CODE-03~~: ✓ 测试用例使用真实 model_actions() 键名验证 — Phase 101
- ~~CODE-04~~: ✓ 端到端验证 — AI 执行后生成代码可被 pytest 运行 — Phase 101

**v0.10.4 Playwright 代码验证与任务管理集成 (2026-04-24):**
- ✓ CODE-01: GET /runs/{run_id}/code 返回已生成的 Playwright 代码文件内容 — Phase 97
- ✓ CODE-02: POST /execute-code 触发 pytest 执行，复用 SelfHealingRunner — Phase 97
- ✓ CODE-03: healing_status/healing_error 反映执行结果 — Phase 97
- ✓ STATUS-01: Task.status 扩展为 draft/ready/success，执行成功自动标记 — Phase 97
- ✓ UI-01: 任务列表"代码"列，蓝色/灰色 Code2 图标 — Phase 98
- ✓ UI-02: CodeViewerModal 语法高亮只读显示 Python 代码 — Phase 98
- ✓ UI-03: "运行代码"按钮 + 执行状态轮询 + 错误展示 — Phase 98

**v0.10.3 DOM 深度修复 - 表格单元格选择精确性 (2026-04-23):**
- ✓ DEPTH-01: td 内部子元素 bbox 保护 — 防止 `<div>/<span>` 被 `excluded_by_parent` 扁平化 — Phase 94
- ✓ DEPTH-02: td 内部 input 可见性保证 — 确保编辑态 input 出现在 DOM dump — Phase 94
- ✓ DEPTH-03: 列标题映射注入 — `<!-- 列: 销售金额 -->` 注释 — Phase 94
- ✓ DEPTH-04: Prompt 更新 — Section 9 利用列标题和深度结构 — Phase 95
- ✓ DEPTH-05: E2E 验证 — 销售出库场景正确列选择 — Phase 96

**v0.10.2 测试验证与代码可用性修复 (2026-04-23):**
- ✓ CLEAN-01/02: 删除 37 过时测试文件 + autouse cache reset fixtures — Phase 90
- ✓ TEST-01~05: 全量测试套件 876 passed, 0 failed, 0 errors — Phase 91
- ✓ DATA-01/02: Docstring 方法映射 + ImportApi 别名修补，上游混淆名变化不再破坏前置条件 — Phase 92
- ✓ E2E-01/02/03: 自然语言→AI 执行→报告全链路验证通过 + 3 个 E2E 回归测试 — Phase 93

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
- ✓ TEST-03: 顶层 conftest.py db_session + autouse reset_cache — Phase 91
- ✓ TEST-04: 外部断言桥接测试 resolve_headers mock 对齐 — Phase 91
- ✓ TEST-05: 全量测试套件 876 passed, 0 failed, 0 errors — Phase 91

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
- 4/81 assertion api_attrs 无法匹配 (bidding/fulfillment 模块类数多于 _module_map 条目) — 未来优化

### Out of Scope

- 用户认证/权限管理 — 单用户本地使用
- 多语言支持 — 只支持中文
- 高可用/负载均衡 — 单服务器足够

## Context

**技术背景:**
- 后端 FastAPI + Python
- 前端 React + Vite + Tailwind
- 数据库 SQLite (aiosqlite)

**代码质量:**
- 测试套件: 928 tests passed (Phase 119 regression gate)
- 自愈功能完全移除，-2999 行代码
- 执行管道简化为一次性 pytest (subprocess.run)

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
| Docstring first-line 作为稳定方法标识符 | webseleniumerp 混淆名变化不影响 docstring | ✓ Good |
| Runtime ImportApi._module_map alias patching | 不侵入上游代码，运行时修补 | ✓ Good |
| 三阶段 alias patching (remap + scan params + scan assertions) | 处理上游全量重新混淆 | ✓ Good |
| 前置条件变量序列化过滤非 JSON-safe 类型 | 防止 SSE/DB 序列化崩溃 | ✓ Good |
| td 内部子元素 bbox 保护（ant-table-cell-inner 等）| `_apply_bounding_box_filtering` 将 td 内 div/span 标记为 `excluded_by_parent` 导致扁平化 | ✓ Good |
| 列标题映射注入到 DOM dump | Agent 无法区分相邻同值 td 列 | ✓ Good |
| httpx AsyncClient + ASGITransport 进程内 E2E 测试 | 无需真实服务器，快速可靠 | ✓ Good |
| FastAPI dependency_overrides 替代 patch() 测试注入 | patch 不影响已解析的 Depends() | ✓ Good |
| asyncio.Semaphore(1) 代码执行并发保护 | 2GB 服务器内存安全边界 | ✓ Good |
| BackgroundTasks.add_task + 新 DB session | 请求 session 在响应后关闭 | ✓ Good |
| 路由层构造 computed fields dict | has_code/latest_run_id 非 ORM 字段 | ✓ Good |
| ErrorCategoryResult frozen dataclass | 项目不可变约定 | ✓ Good |
| Unknown exit codes 默认 CODE_RUNTIME | 不遗漏 LLM 修复机会 | ✓ Good |
| error_category default empty string | HealingResult 向后兼容 | ✓ Good |
| Patch account_service at source module | E2E test lazy import fix | ✓ Good |
| pytest-timeout dev dependency | SelfHealingRunner --timeout flag | ✓ Good |
| getRunCode 原始 fetch 替代 apiClient | apiClient 调 response.json() 对 PlainTextResponse 失败 | ✓ Good |
| StatusBadge context prop 实体感知标签 | Task='成功' vs Run='已完成'，保持向后兼容 | ✓ Good |
| react-syntax-highlighter Prism build 只读代码展示 | 40KB gzipped，零配置 | ✓ Good |
| Unknown action types show f-string params summary | QA 可检查原始参数 | ✓ Good |
| validate_syntax 防御性双重调用 | generate() + generate_and_save() 双重验证 | ✓ Good |
| Short text (≤4 chars) exact=True, long text fuzzy | 短文本精确匹配，长文本模糊匹配 | ✓ Good |
| 相对 XPath priority: data-testid > id > absolute fallback | 语义优先的定位器策略 | ✓ Good |
| PUA filtering at extract() entry (U+E000-U+F8FF) | 过滤 icon font 渲染字符 | ✓ Good |
| Content-matching _apply_fix replaces line-number fix | 启用多行修复 + ast.parse rollback | ✓ Good |
| Code locator extraction from failing line | 替代 error_output 正则猜测 | ✓ Good |
| Structured JSON LLM repair {target_snippet, replacement} | 明确修复结构 | ✓ Good |
| Mock LLMHealer at class level for E2E tests | patch at backend.core.self_healing_runner.LLMHealer | ✓ Good |
| StepRecord frozen dataclass | 不可变性保证，action/wait_before/step_index | ✓ Good |
| StepCodeBuffer keyword-only __init__ | *, base_dir, run_id, llm_config — 向后兼容 | ✓ Good |
| navigate wait_for_load_state 最高优先级 | 不管 duration 多少，navigate 后一定等 networkidle | ✓ Good |
| append_step_async 失败静默降级 | heal 失败/异常/缺 DOM 均不阻塞主流程 | ✓ Good |
| Path imported as PathLib in try block | 避免顶层 Path import 冲突 | ✓ Good |
| Structural input detection replaces placeholder matching | tag+type+visibility 检测，不依赖 placeholder 精确匹配 | ✓ Good |
| Five-segment prompt structure (定位/判断模式/操作/验证/异常处理) | 清晰的 Agent 决策流程 | ✓ Good |
| DOM element type (td vs input) determines mode judgment | 与 dom_patch.py 检测对齐 | ✓ Good |
| action_dict guarded with 'in locals()' | 变量在条件块内，需存在性检查 | ✓ Good |
| Delete-first cleanup-second (v0.10.11) | 删除文件后再清理引用，减少跨文件依赖风险 | ✓ Good |
| subprocess.run 替代 SelfHealingRunner (v0.10.11) | 一次性 pytest 执行，消除重试循环 | ✓ Good |
| SQLite 列保留不 ALTER TABLE (v0.10.11) | ORM 停止读写 healing 列，DB 列保持不动 | ✓ Good |
| run.status 单一执行状态源 (v0.10.11) | 替代 healing_status 多状态轮询 | ✓ Good |
| logger name "healer" 保留 (v0.10.11) | 生成代码中 getLogger("healer") 不变，避免破坏已有测试文件 | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

---
*Last updated: 2026-04-29 after v0.10.11 milestone*
