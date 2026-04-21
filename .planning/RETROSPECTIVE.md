# Project Retrospective

## Milestone: v0.10.1 — 代码登录及 Agent 复用登录的浏览器状态

**Shipped:** 2026-04-21
**Phases:** 4 | **Plans:** 6

### What Was Built

- 登录机制研究: POC 确认 localStorage 注入不可行，编程式表单登录 (dispatchEvent) 可行
- Vue SPA 编程式登录修复: dispatchEvent(MouseEvent) 替代 btn.click() + 完整表单事件序列
- 认证代码清理: 删除死代码（auth_session_factory, POC scripts），storage_state 内联到 self_healing_runner
- 测试覆盖: 5 个新单元测试 + 27 个测试全通过

### What Worked

- **POC 验证驱动研究**: Phase 86 用最小 POC 验证两个方案，快速排除不可行的 localStorage 注入
- **单行修复核心问题**: Phase 87 的关键修复只有一行 (btn.click() → dispatchEvent)，问题定位精准
- **先清理后测试**: Phase 88 清理死代码后 Phase 89 补测试，测试基于最终代码结构

### What Was Inefficient

- Phase 87 ROADMAP 标记为 "Not started" 但实际已完成（进度表未更新）
- REQUIREMENTS.md 仍指向 v0.9.2，v0.10.1 未更新需求文档

### Patterns Established

- **POC-first 研究**: 先用最小代码验证可行性，再进入实施
- **dispatchEvent 替代 click**: Vue/React SPA 需要构造正确的 MouseEvent 而非 .click()

### Key Lessons

1. Vue SPA 的登录按钮不能直接 .click()，需要 dispatchEvent(new MouseEvent('click', {bubbles: true}))
2. Vuex/Pinia store 在 SPA 初始化时读取 localStorage，后续直接修改 localStorage 不会触发 store 更新
3. browser-use 的 page.evaluate 返回复杂 JS 对象时需要 JSON.stringify 序列化

### Cost Observations

- Model mix: 100% opus
- Sessions: ~4 (86, 87, 88, 89)
- Notable: 3 天完成 4 个阶段 6 个计划，包含研究和清理

## Milestone: v0.9.0 — Excel 批量导入功能开发

**Shipped:** 2026-04-09
**Phases:** 4 | **Plans:** 8

### What Was Built

- Excel 模版系统: TEMPLATE_COLUMNS 合约 + generate_template() + DataValidation
- ExcelParser: collect-all 错误策略 + 类型强制转换 + round-trip 验证
- 两阶段导入工作流: preview → confirm 原子批量创建，ImportModal 三步状态机
- 批量执行引擎: BatchExecutionService + Semaphore 并发控制 (default 2, cap 4)
- 批量进度 UI: 2s 轮询 + 任务卡片 + elapsed time + 点击导航

### What Worked

- **两阶段导入设计**: preview + confirm 模式让 QA 在确认前预览，避免脏数据进入
- **Semaphore 并发控制**: 简单有效的并发限制，默认 2 个浏览器实例
- **轮询替代 SSE**: 避免了 multiplexer 架构改造，2s 轮询足够满足需求
- **TEMPLATE_COLUMNS 合约**: 模版生成器和解析器共享列定义，减少不一致

### What Was Inefficient

- Phase 70-02 PLAN 标记未勾选但实际已完成（ROADMAP.md checkbox 不一致）
- 批量执行后需手动跳转到进度页面（可在后续版本自动跳转）

### Patterns Established

- **collect-all error strategy**: 解析时不提前终止，收集所有错误一次性展示给用户
- **stateless confirm**: confirm 端点重新解析文件而非缓存服务器状态
- **fire-and-forget execution**: asyncio.create_task 启动批量执行，立即返回状态

### Key Lessons

1. Excel 导入的关键难点在数据校验（类型、格式、必填），collect-all 策略显著提升用户体验
2. 并发控制需要考虑服务器资源限制，Semaphore 上限应基于实际硬件容量
3. 两阶段操作（preview + confirm）是批量操作的最佳实践

### Cost Observations

- Model mix: 100% opus
- Sessions: ~4 (70, 71, 72, 73)
- Notable: 2 天完成 4 个阶段 8 个计划，节奏稳定

## Milestone: v0.8.3 — 分析报告差距对表格填写影响

**Shipped:** 2026-04-06
**Phases:** 2 | **Plans:** 2

### What Was Built

- 差距关联分析: headless 是加剧因素而非唯一根因，DOM Patch 4/5 仍必要
- 优化方案设计: 540 行设计文档，4 项策略（行定位/反重复/策略优先级/失败恢复），16 项代码任务

### What Worked

- **纯分析里程碑模式**: 不写代码，聚焦分析和设计，减少上下文切换
- **三层证据链框架**: 每项分析结论有明确判定（是/否/部分）+ 证据链，避免模糊描述
- **设计文档结构化**: 16 项代码任务标注依赖关系和优先级，可直接实施

### What Was Inefficient

- Phase 65 缺少 SUMMARY.md（验证时发现）
- ANALYSIS-01~03 在 REQUIREMENTS.md 中标记为 Pending（实际上已完成）

### Patterns Established

- **DOM dump 注释注入**: 通过 `<!-- -->` 注释向 Agent 传递结构化信息，不修改 Agent 决策逻辑
- **跨步骤状态共享**: 模块级变量在 step_callback 和 DOM Patch 间共享
- **策略自动降级**: 三级策略逐级降级，通过注释标注实现

### Key Lessons

1. 纯分析设计里程碑可以快速完成（1 天），为后续实施节省上下文
2. 设计文档的"可直接转化为代码任务"标准很重要——避免后续实施时的二次理解
3. 因果分析需要区分"根因"和"加剧因素"，避免过度简化

### Cost Observations

- Model mix: 100% opus
- Sessions: 2 (分析 + 设计)
- Notable: 极轻量里程碑，无代码修改，纯文档输出

## Milestone: v0.8.1 — 修复销售出库表格填写问题

**Shipped:** 2026-04-06
**Phases:** 1 | **Plans:** 1

### What Was Built

- DOM Patch 扩展到 5 个补丁，支持 ERP click-to-edit 表格的 td 单元格交互标记
- Section 9 提示词添加 ERP 销售出库 click-to-edit 工作流指导（点击 td → 等待 input → 输入值）
- E2E 验证: 销售出库 26 步完成，销售金额 150 成功填写

### What Worked

- **快速定位根因**: 通过 E2E 测试快速发现 Ant Design click-to-edit 表格不会预渲染 input 元素
- **Pivot 决策果断**: 从 input placeholder 检测快速转向 td 文本内容检测，仅用一次 commit 修复
- **DOM Patch 模式成熟**: 在已有 Phase 53 的 monkey-patch 基础上扩展，模式清晰可复用

### What Was Inefficient

- 初始方案基于错误假设（input placeholder 存在于 DOM 中），需要一次修复 commit
- Phase 60-task-form-optimize 空目录残留（init 标记为 pending 但实际无工作）

### Patterns Established

- **click-to-edit td 检测模式**: `_is_textual_td_cell()` 检测 td 内文本内容，标记为 interactive
- **Prompt Section 模式**: 每个 ERP 场景一个 Section，包含工作流 + 负面示例

### Key Lessons

1. Ant Design click-to-edit 表格不会预渲染 input，必须先 click td 触发编辑模式
2. DOM Patch 目标应基于实际 DOM 结构验证，而非假设
3. 简单的里程碑（1 phase）可以在 30 分钟内完成

### Cost Observations

- Model mix: 100% opus
- Sessions: 2 (plan + execute)
- Notable: 极小的里程碑，单阶段单计划，效率高

## Cross-Milestone Trends

| Metric | v0.6.3 | v0.7.0 | v0.8.0 | v0.8.1 | v0.8.3 | v0.9.0 | v0.10.1 |
|--------|--------|--------|--------|--------|--------|--------|---------|
| Phases | 4 | 5 | 5 | 1 | 2 | 4 | 4 |
| Plans | 10 | 10 | 6 | 1 | 2 | 8 | 6 |
| Duration (days) | 1 | 2 | 2 | 1 | <1 | 2 | 3 |
| Tech Debt Added | 0 | 1 (cache assert) | 0 | 0 | 0 | 0 | 0 |
| Bugs Found/Fixed | 0 | 0 | 0 | 2 (auto-fixed) | 0 | 0 | 0 |
| Code LOC Changed | ~800 | ~300 | ~600 | ~100 | 0 | ~9400 | ~3000 |
