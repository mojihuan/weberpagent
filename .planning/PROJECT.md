# aiDriveUITest

## What This Is

AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例。基于 Browser-Use + 阿里云 Qwen 3.5 Plus 构建，实现「自然语言描述 → AI 决策 → Playwright 执行」的自动化测试流程。

**目标用户**: QA 测试人员
**核心场景**: 用中文描述测试步骤，AI 自动理解、执行并生成测试报告

## Core Value

**让 QA 用自然语言写测试用例，AI 自动执行并生成报告。**

这是产品的核心价值。如果这个流程跑不通，产品就没有意义。

## Current State

**Shipped: v0.11.4 审查发现优化 — 系统性模式修复** (2026-05-05)

v0.11.4 全部 5 个 phase 完成。5 个系统性跨层模式 (CP-1~CP-5) 全部修复。

**Phase 134 complete** — 死代码清理: response.py 删除 (85行)、PreSubmitGuard 精简 (46→10行)、scan_with_fallback 删除、on_step 统一 non_blocking_execute；4 个前端 hooks 迁移到 React Query (~340→244行)。

**所有系统性模式已修复:**
- CP-1: ~~内存泄漏~~ — Phase 131 (后端) + Phase 133 (前端) 已修复
- CP-2: ~~错误处理缺口~~ — Phase 131 已修复
- CP-3: ~~未使用代码~~ — Phase 134 已修复 (React Query 迁移 + 死代码删除)
- CP-4: ~~阻塞操作~~ — Phase 132 已修复
- CP-5: ~~可变状态~~ — Phase 132/133 已修复

**Top 5 优先修复:**
1. event_manager 内存泄漏 (CP-1, High)
2. assertion_service.check_element_exists stub (High)
3. dual stall detection 正确性 bug (High)
4. execute_run_code 路径验证缺失 (High, SEC)
5. JSON.parse 无 try/catch (High, frontend)

## Current Milestone: v0.11.4 审查发现优化 — 系统性模式修复

**Goal:** 修复 v0.11.3 审查发现的 5 个系统性跨层模式 (CP-1~CP-5) 及 Top 5 High 优先问题，提升代码健壮性和安全性。

**Target features:**
- CP-1 内存泄漏修复 — event_manager._events 无界增长 + useRunStream 数组无清理
- CP-2 错误处理补全 — SSE event_generator 异常 + JSON.parse 无 try/catch 保护
- CP-3 未使用代码清理 — StructuredLogger 未启用 + React Query 未充分使用
- CP-4 阻塞操作迁移 — write_bytes 同步写文件 + subprocess.run 阻塞事件循环
- CP-5 可变状态解耦 — external assertion context 全局可变 + useState 直接修改
- Top 5 High 修复 — assertion_service stub、dual stall detection bug、execute_run_code 路径验证

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
- v0.11.0: 全面代码清理 (2026-04-30) — 删除测试 + 死代码 + 重复合并 + 类型标注 + 函数优化
- v0.11.3: 代码彻底的 Review (2026-05-04) — 全栈审查 277 findings + 67 测试场景规划

## Requirements

### Validated

**v0.11.3 代码彻底的 Review (2026-05-04):**
- ✓ CORR-01: 后端核心业务逻辑正确性审查 — Phase 125 (32 findings)
- ✓ CORR-02: API 路由层正确性审查 — Phase 126 (78 findings)
- ✓ CORR-03: 前端组件逻辑正确性审查 — Phase 127 (95 findings)
- ✓ SEC-01: 安全风险审查 — Phase 126 (13 安全 findings)
- ✓ PERF-01: 异步/并发性能审查 — Phase 128 (25 findings)
- ✓ PERF-02: 前端性能审查 — Phase 127 (15 findings)
- ✓ MAINT-01: DRY/SOLID 违反审查 — Phase 128 (32 findings)
- ✓ MAINT-02: 代码结构复杂度审查 — Phase 128 (22 findings)
- ✓ MAINT-03: 命名规范性审查 — Phase 128 (16 findings)
- ✓ ARCH-01: 模块耦合度审查 — Phase 125 (5 findings)
- ✓ ARCH-02: 抽象合理性审查 — Phase 125 (7 findings)
- ✓ ARCH-03: 横切关注点审查 — Phase 128 (23 findings)
- ✓ TEST-01: 关键测试缺失识别 — Phase 129 (52 scenarios)
- ✓ TEST-02: 边界/错误覆盖不足识别 — Phase 129 (35 scenarios)

**v0.11.0 全面代码清理 (2026-04-30):**
- ✓ TEST-01~04: 删除整个测试套件 (87 文件, ~20K 行) + pytest 配置 + 测试依赖 — Phase 120
- ✓ DEAD-01~04: 清理 3 个废弃模块 + 17 个未使用 import + 零未调用函数 — Phase 121
- ✓ DUP-01~03: 合并 13 处重复模式 (BaseRepository, lazy-load, 503 guards, assertion checks) — Phase 122
- ✓ NAME-01/02/03: snake_case 命名零违规，文件命名规范 — Phase 123
- ✓ TYPE-01/02/03: 96 个公共函数完整类型标注 + py.typed + mypy 配置 — Phase 123
- ✓ FUNC-01~04: 拆分过长函数 + 重组模块 (runs.py/bridge 拆分) + 嵌套压平 + error_utils — Phase 124

**v0.10.11 移除自愈功能 (2026-04-29):**
- ✓ REMOVE-01~04: 删除 SelfHealingRunner/LLMHealer/ErrorClassifier/HealerError 四个自愈模块 — Phase 116
- ✓ SIMPLIFY-01~03: 简化 runs.py 执行管道 + 移除 append_step_async + 清理 code_generator — Phase 117
- ✓ DB-01~03: 清理 Run 模型/schema/repository healing 字段 — Phase 117
- ✓ API-01~02: 简化 API 端点 + 保留代码查看 — Phase 118
- ✓ FE-01~05: 移除前端 healing UI/类型/StatusBadge/CodeViewerModal — Phase 118
- ✓ TEST-01~03: 删除自愈测试 + 清理 mock + 全量回归 928 passed — Phase 119

**v0.10.10 表单填写优化 (2026-04-29):**
- ✓ FORM-01: 重构 _is_erp_table_cell_input 检测逻辑 — Phase 114
- ✓ FORM-02: 修复 _is_textual_td_cell — Phase 114
- ✓ FORM-03: 增强 _patch_assign_interactive_indices — Phase 114
- ✓ FORM-04: 新增 DOM 诊断日志 — Phase 114
- ✓ FORM-05: 更新 prompts.py Section 9 — Phase 115
- ✓ FORM-06: E2E 验证 — Phase 115

<details>
<summary>v0.10.9 及更早版本的已验证需求</summary>

**v0.10.9 逐步代码生成 (2026-04-29):**
- ✓ CODEGEN-01: StepCodeBuffer.append_step() 同步翻译 — Phase 111
- ✓ CODEGEN-02: append_step_async() 弱步骤检测 + LLMHealer 修复 — Phase 111
- ✓ CODEGEN-03: _derive_wait() 智能等待推导 — Phase 111
- ✓ CODEGEN-04: buffer.assemble() 组装完整测试文件 — Phase 111
- ✓ INTEG-01~03: step_callback 集成 + 删除废弃方法 — Phase 112
- ✓ VAL-01~03: 单元测试 + 集成测试 + 全量回归 316 passed — Phase 111-113

**v0.10.8 生成测试代码前置条件与断言步骤 (2026-04-27):**
- ✓ PREC-01~03: 前置条件 page.goto() + wait_for_load_state() — Phase 108
- ✓ ASRT-01~03: 4 种断言类型 → Playwright expect() — Phase 109
- ✓ E2E-01: 完整生成代码验证 — Phase 110

**v0.10.7 生成测试代码行为优化 (2026-04-27):**
- ✓ TRANSLATE-01/02: 未知操作参数摘要 + 10 核心操作翻译回归 — Phase 105
- ✓ INDENT-01/02/03: 缩进后处理 + ast.parse 验证 — Phase 105
- ✓ LOCATOR-01~04: exact/XPath/PUA 过滤定位器优化 — Phase 106
- ✓ HEAL-01~04: 内容匹配修复 + DOM 精准映射 — Phase 107
- ✓ E2E-01/02: E2E healing pipeline + 全量回归 — Phase 107

**v0.10.6 生成测试代码稳定可用 (2026-04-25):**
- ✓ EXEC-01~03: pytest 参数修复 + 代码生成器修复 + 输出隔离 — Phase 102
- ✓ HEAL-01: 纯函数错误分类器 — Phase 103
- ✓ E2E-01: E2E 测试验证 — Phase 104

**v0.10.5 生成测试代码修复与优化 (2026-04-24):**
- ✓ KEY-01~04: 键名重命名 + dispatch 对齐 + 类型修复 + 测试更新 — Phase 99
- ✓ CODE-01~04: action_translator 键名修复 + 补充缺失翻译 + E2E — Phase 100-101

**v0.10.4 Playwright 代码验证与任务管理集成 (2026-04-24):**
- ✓ CODE-01~03: 代码查看 + 执行 + healing_status — Phase 97
- ✓ STATUS-01: Task.status 扩展 — Phase 97
- ✓ UI-01~03: 代码列 + CodeViewerModal + 运行按钮 — Phase 98

**v0.10.3 DOM 深度修复 (2026-04-23):**
- ✓ DEPTH-01~05: bbox 保护 + input 可见性 + 列标题映射 + Prompt 更新 + E2E — Phase 94-96

**v0.10.2 测试验证与代码可用性修复 (2026-04-23):**
- ✓ CLEAN-01/02: 删除 37 过时测试 + cache reset fixtures — Phase 90
- ✓ TEST-01~05: 876 passed — Phase 91
- ✓ DATA-01/02: Docstring 方法映射 + ImportApi 别名修补 — Phase 92
- ✓ E2E-01~03: 全链路验证 + 3 个 E2E 回归测试 — Phase 93

**v0.8.1 修复销售出库表格填写问题 (2026-04-06):**
- ✓ DOM-PATCH-01: td cell 文本内容检测 + ERP 表格 input 可见性 patch — Phase 62
- ✓ PROMPT-01: Section 9 click-to-edit 工作流指导 — Phase 62
- ✓ E2E-01: 销售出库场景 E2E 验证 — Phase 62

**v0.8.0 报告完善与 UI 优化 (2026-04-03):**
- ✓ FMT-01/02/03: AI 推理格式分行彩色 badge 展示 — Phase 57
- ✓ EXEC-01/02/03: StepTimeline 统一时间线 — Phase 58
- ✓ RPT-01/02/03: 报告详情统一时间线 — Phase 59
- ✓ FORM-01/02: 任务表单移除 api_assertions tab — Phase 60
- ✓ E2E 验证: 6/6 检查 PASS — Phase 61

**v0.7.0 更多操作边界测试 (2026-04-01):**
- ✓ KB-01/02/03: 键盘操作 — Phase 52/56
- ✓ TBL-01/02/03/04: 表格交互 — Phase 53/56
- ✓ IMP-01/02: 文件导入 — Phase 54/56
- ✓ AST-01/02: 断言参数验证 — Phase 56

**v0.6.3 Agent 可靠性优化 (2026-03-28):**
- ✓ StallDetector + PreSubmitGuard + TaskProgressTracker + MonitoredAgent — Phase 48
- ✓ ENHANCED_SYSTEM_MESSAGE 5 段式 ERP 指导 — Phase 49
- ✓ AgentService 集成 + E2E 60/60 测试通过 — Phase 50-51

**v0.6.2 回归原生 browser-use (2026-03-27):**
- ✓ 移除 scroll_table 工具、TD 后处理、JS fallback、元素诊断、循环干预

**v0.5.0 项目云端部署 (2026-03-24):**
- ✓ Git 仓库迁移、阿里云部署、FastAPI + Gunicorn + Nginx

**v0.1-v0.4.2 核心功能:**
- ✓ 任务管理、AI 执行、实时监控、测试报告
- ✓ 前置条件系统、接口断言、动态数据获取
- ✓ 断言系统、数据获取方法集成
- ✓ 三层参数架构 (api_params, field_params, params)

</details>

### Active

(None — all v0.11.4 requirements validated)

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

**代码质量 (v0.11.3 后):**
- 测试套件已删除 — 项目无自测套件（v0.11.3 规划了 67 个重建场景）
- backend/ 约 11,705 行 Python 代码 (从 ~30K+ 精简)
- pyflakes 零警告
- 96 个公共函数完整类型标注
- 277 个可操作发现 (Critical: 0, High: 14+, Medium: 100+, Low: 160+)
- 5 系统性跨层模式 (CP-1~CP-5)
- radon 平均复杂度 A (3.31), 1 个 F 级函数

**技术栈:**
| 层级 | 技术 |
|------|------|
| 前端 | React 19.2, TypeScript 5.9, Vite 7.3, Tailwind CSS 4.2 |
| 后端 | Python 3.11, FastAPI, Pydantic, SQLAlchemy |
| AI | Browser-Use 0.12+, Qwen 3.5 Plus (阿里云 DashScope) |
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
| 前置条件使用 Python 代码格式 | 灵活性高，可直接调用 API | ✓ Good |
| exec() + asyncio.wait_for() 执行代码 | 30 秒超时保护 | ✓ Good |
| 断言结果存入 context 非 fail-fast | 收集所有结果后汇总 | ✓ Good |
| click-to-edit td 检测取代 input placeholder 检测 | Ant Design 表格不预渲染 input | ✓ Good |
| DOM Patch 5 patches 覆盖 ERP 特殊模式 | ERP 表格 click-to-edit + checkbox 等 | ✓ Good |
| openpyxl 唯一依赖，零新依赖 | 已安装 3.1.5，减少供应链风险 | ✓ Good |
| 导入两阶段模式 (preview + confirm) | confirm 重新解析而非缓存，无状态设计 | ✓ Good |
| 批量进度轮询 (2s) 而非 SSE | 避免 multiplexer 架构改造 | ✓ Good |
| Semaphore 默认并发 2，硬上限 4 | 基于部署服务器内存的安全边界 | ✓ Good |
| Vue SPA 需要 dispatchEvent(MouseEvent) 登录 | btn.click() 不触发 Vue 事件绑定 | ✓ Good |
| storage_state 构造内联到 self_healing_runner | 消费者唯一，保持模块解耦 | ✓ Good |
| browser-use page.evaluate 返回复杂对象为 string | 用 JSON.stringify + json.loads 序列化 | ✓ Good |
| Docstring first-line 作为稳定方法标识符 | webseleniumerp 混淆名变化不影响 docstring | ✓ Good |
| Runtime ImportApi._module_map alias patching | 不侵入上游代码，运行时修补 | ✓ Good |
| Delete-first cleanup-second (v0.11.0) | 删除文件后再清理引用，减少跨文件依赖风险 | ✓ Good |
| Mutable dict counters instead of nonlocal (v0.11.0) | 跨函数边界闭包提取更简洁 | ✓ Good |
| Thin re-export shims for backward-compatible file splits (v0.11.0) | 拆分模块时保持外部导入路径不变 | ✓ Good |
| error_utils.py selective application (v0.11.0) | 只在减少复杂度时替换 try-except | ✓ Good |
| Replace async-unsafe silent_execute with non_blocking_execute (v0.11.0) | 修复异步异常处理 | ✓ Good |
| SQLite 列保留不 ALTER TABLE (v0.10.11) | ORM 停止读写 healing 列，DB 列保持不动 | ✓ Good |
| run.status 单一执行状态源 (v0.10.11) | 替代 healing_status 多状态轮询 | ✓ Good |
| logger name "healer" 保留 (v0.10.11) | getLogger("healer") 不变，避免破坏已有测试文件 | ✓ Good |
| Review-only 模式 (v0.11.3) | 审查结果不受实现偏见影响，发现更客观 | ✓ Good |
| 严重程度驱动 ROI 排序 (v0.11.3) | Critical > High > Medium > Low，最高风险先覆盖 | ✓ Good |
| 后端测试优先于前端 (v0.11.3) | 后端无测试保护风险最高，前端有编译期保护 | ✓ Good |
| 安全发现双评估 (v0.11.3) | 当前单用户影响 + 公网部署影响，兼顾当前和未来 | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

---
*Last updated: 2026-05-05 — v0.11.4 milestone complete*
