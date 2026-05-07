# Project Retrospective

## Milestone: v0.11.3 — 代码彻底的 Review

**Shipped:** 2026-05-04
**Phases:** 5 | **Plans:** 15

### What Was Built

- 后端核心逻辑审查: 31 文件 32 actionable findings，含 dual stall detection bug、assertion_service stub、架构耦合分析
- API 层与安全审查: 13 路由文件 78 findings，1 High (execute_run_code 路径验证缺失)，13 安全发现
- 前端审查: 87 文件 95 findings，含 SSE 交叉验证、JSON.parse 安全、React Query 未使用
- 代码质量审查: 81 new findings，5 系统性跨层模式 (CP-1~CP-5)，radon/ESLint 量化指标
- 测试规划: 277 findings 筛选为 67 可测试场景 (24 unit + 25 integration + 13 frontend + 5 E2E)，含实施路线图

### What Worked

- **Review-only 模式**: 不改代码让审查更客观，39 commits, 5672 行审查文档
- **跨 phase 关联发现系统性问题**: CP-1~CP-5 仅在 Phase 128 做 cross-phase correlation 时才被识别
- **量化工具比人工审查更可靠**: ruff/mypy/radon/ESLint 提供客观数据基线
- **4 phase sequential + 1 synthesis**: 125-128 按维度审查，129 综合规划，结构清晰

### What Was Inefficient

- Phase 127 和 126 实际上并行执行了（ROADMAP 标记 127 depends on 125，但实际审查不同代码区域）
- 15 个 plan 产出大量 FINDINGS.md 数据，Phase 129 汇总分析需要重新阅读大量前置数据

### Patterns Established

- **5 系统性模式框架**: CP-1~CP-5 作为跨层质量分析工具，未来审查可直接复用
- **严重程度驱动 ROI 排序**: Critical > High > Medium > Low，优先覆盖最高风险
- **安全发现双评估**: 单用户影响 + 公网影响，兼顾当前和未来

### Key Lessons

1. Review-only 模式有效——审查结果不受实现偏见影响，发现质量更高
2. 跨 phase 关联分析是识别系统性问题的关键——单 phase 只能看到局部
3. 量化工具 (radon/ESLint) 提供客观数据基线，人工审查补充上下文
4. 验证者纠正了审查者错误 (P1-01 ContextWrapper isinstance)——交叉验证重要

### Cost Observations

- Model mix: 100% opus
- Sessions: ~5 (125, 126+127 parallel, 128, 129)
- Notable: 3 天完成 5 个阶段 15 个计划，纯文档产出 (0 行代码修改)

## Milestone: v0.11.4 — 审查发现优化 — 系统性模式修复

**Shipped:** 2026-05-06
**Phases:** 5 | **Plans:** 10

### What Was Built

- 路径遍历防护: get_run_report + execute_run_code 端点添加 _validate_code_path 验证 (Phase 130)
- EventManager 内存泄漏修复: run 生命周期自动清理 + heartbeat task 取消 + StallDetector 1000 条上限 (Phase 131)
- SSE 异常保护: per-queue try/except 隔离 + event_generator disconnect 保护 + page.evaluate DOM 检测替换 stub (Phase 131)
- 阻塞操作异步迁移: save_screenshot asyncio.to_thread + subprocess.run → create_subprocess_exec (Phase 132)
- 前端健壮性: useRef + version counter O(1) 追加 + 7 处 JSON.parse try/catch + isConnected 修正 (Phase 133)
- 死代码清理: 85 行 response.py 删除 + PreSubmitGuard 精简 + scan_with_fallback 移除 + non_blocking_execute 统一 (Phase 134)
- React Query 迁移: 4 个 hooks 从手动 fetch 迁移到 useQuery，340→244 行 (Phase 134)

### What Worked

- **5 系统性模式框架驱动修复**: CP-1~CP-5 分类让修复有序，不遗漏
- **依赖链正确**: Phase 130→131→132/133→134，前端修复依赖后端 SSE 修复
- **TDD 在安全/内存修复中效果显著**: Phase 130-131 先写 failing test，确保修复正确
- **2 天完成 10 plans**: 平均每个 plan ~30 分钟，节奏极快

### What Was Inefficient

- Phase 133-02 STATE-02 最终确认为 no-op — 8 处 .push() 都是局部变量，investigation 花了时间但零代码改动
- Phase 132 两个 SUMMARY.md 缺少 one_liner — summary-extract 工具无法自动提取

### Patterns Established

- **Ref + version counter 模式**: useRef 可变数组 + version 触发 useState，O(1) 追加替代 O(n^2) spread
- **asyncio.to_thread 迁移阻塞 I/O**: 零侵入，保持 sync API 不变
- **per-queue exception isolation**: SSE publish 每个 queue 独立 try/except，一个 bad queue 不影响其他
- **page.evaluate + JSON.stringify DOM 检测**: browser-use CDP 下唯一可靠的 DOM 查询方式

### Key Lessons

1. 系统性模式修复比零散修复高效——CP-1~CP-5 框架让修复有系统性覆盖
2. 前端 immutable 验证可能是 no-op——React .push() 在局部变量上是安全的，需要区分 state vs local
3. React Query 迁移 ROI 高——~28% 代码缩减，零消费者改动
4. TDD 在修复类任务中效率高——先写 failing test 锁定 bug，修复后立即验证

### Cost Observations

- Model mix: 100% opus
- Sessions: ~5 (130, 131, 132, 133, 134)
- Notable: 2 天完成 5 个阶段 10 个计划，38 文件修改 +3346/-547 行

## Cross-Milestone Trends

| Metric | v0.6.3 | v0.7.0 | v0.8.0 | v0.8.1 | v0.8.3 | v0.9.0 | v0.10.1 | v0.10.3 | v0.10.7 | v0.10.9 | v0.10.11 | v0.11.0 | v0.11.3 | v0.11.4 |
|--------|--------|--------|--------|--------|--------|--------|---------|---------|---------|---------|----------|---------|---------|---------|
| Phases | 4 | 5 | 5 | 1 | 2 | 4 | 4 | 3 | 3 | 3 | 4 | 5 | 5 | 5 |
| Plans | 10 | 10 | 6 | 1 | 2 | 8 | 6 | 4 | 6 | 6 | 8 | 11 | 15 | 10 |
| Duration (days) | 1 | 2 | 2 | 1 | <1 | 2 | 3 | 1 | 2 | 2 | <1 | 2 | 3 | 2 |
| Tech Debt Added | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bugs Found/Fixed | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 0 (review) | 5 (CP-1~5) |
| Code LOC Changed | ~800 | ~300 | ~600 | ~100 | 0 | ~9400 | ~3000 | ~380 | ~4000 | ~1500 | -2999 | -20094 | 0 | +3346/-547 |

## Milestone: v0.11.0 — 全面代码清理

**Shipped:** 2026-04-30
**Phases:** 5 | **Plans:** 11

### What Was Built

- 删除整个测试套件 (87 文件, ~20K 行) + pytest 配置 + 测试依赖清理
- 死代码清理: 3 个废弃模块 + 17 个未使用 import + pyflakes 零警告
- 13 处重复模式合并: BaseRepository + lazy-load 统一 + 503 guards + assertion checks
- 96 个公共函数完整类型标注 + py.typed + mypy 配置
- runs.py 拆分为 routes/pipeline, bridge 拆分为 loader/discovery/engine
- 8 个深层嵌套函数压平至 ≤4 层 + error_utils.py 统一异常处理
- 修复 silent_execute 异步安全问题

### What Worked

- **Delete-first 策略**: 先删测试 (Phase 120) 再清死代码 (Phase 121)，删完再优化 (122-124)
- **5 phase 线性流水线**: 每层职责明确，无回退修复
- **自动化验证**: pyflakes / mypy / FastAPI startup check 每个阶段验证
- **净减 20,094 行**: 143 文件修改，+4,292/-24,386，代码库从 ~30K 精简至 ~11.7K

### What Was Inefficient

- Phase 124 原定 2 plans 实际产生了 3 plans (124-03 fix commit) — silent_execute 异步问题发现较晚
- scan_with_fallback 在 D-09 中标记为 intentionally unused — 抽象过度，应更早识别

### Patterns Established

- **BaseRepository 基类模式**: _persist() 统一 ORM 写入 + 类型安全返回
- **_lazy_load 统一延迟加载**: globals() dict lookup 替代 4 处重复 lazy-load
- **error_utils 共享异常工具**: require_external_available / raise_not_found / _error_result
- **模块拆分 + re-export shim**: 向后兼容文件拆分

### Key Lessons

1. 全面代码清理的 ROI 很高——净减 67% 代码量，可维护性显著提升
2. 类型标注发现隐性 bug (silent_execute 异步不安全) ——投资类型系统值得
3. 函数拆分的边界选择很重要——职责单一但不过度碎片化
4. 统计工具 (pyflakes/mypy) 比人工审查更可靠

### Cost Observations

- Model mix: 100% opus
- Sessions: ~5 (120, 121, 122, 123, 124)
- Notable: 2 天完成 5 个阶段 11 个计划，净删除 20,094 行

## Cross-Milestone Trends

| Metric | v0.6.3 | v0.7.0 | v0.8.0 | v0.8.1 | v0.9.0 | v0.10.1 | v0.10.3 | v0.10.7 | v0.10.9 | v0.10.11 | v0.11.0 |
|--------|--------|--------|--------|--------|--------|---------|---------|---------|---------|----------|---------|
| Phases | 4 | 5 | 5 | 1 | 4 | 4 | 3 | 3 | 3 | 4 | 5 |
| Plans | 10 | 10 | 6 | 1 | 8 | 6 | 4 | 6 | 6 | 8 | 11 |
| Duration (days) | 1 | 2 | 2 | 1 | 2 | 3 | 1 | 2 | 2 | <1 | 2 |
| Tech Debt Added | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bugs Found/Fixed | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 1 | 0 | 1 | 1 |
| Code LOC Changed | ~800 | ~300 | ~600 | ~100 | ~9400 | ~3000 | ~380 | ~4000 | ~1500 | -2999 | -20094 |

## Milestone: v0.10.11 — 移除自愈功能

**Shipped:** 2026-04-29
**Phases:** 4 | **Plans:** 8

### What Was Built

- 删除 SelfHealingRunner/LLMHealer/ErrorClassifier/HealerError 四个自愈模块
- 执行管道简化: subprocess.run 一次性 pytest 替代重试循环
- 数据层清理: Run model/schema/repository 移除所有 healing 字段
- 前端 healing UI 清除: StatusBadge/CodeViewerModal/ReportDetail 零 healing 残留
- 测试清理: 删除 6 测试文件、清理 7 文件，928 测试通过

### What Worked

- **Delete-first cleanup-second 策略**: Phase 116 先删文件，116-02 再清引用，减少跨文件依赖风险
- **4 phase 线性清理**: 116→117→118→119 每层只关注自己范围，无跨层修复
- **同日完成**: 4 个 phase 8 个 plan 在一天内完成（~4 小时），节奏极快

### What Was Inefficient

- Phase 117 重命名 _healer→_logger 时遗漏测试断言，Phase 119 才发现修复
- action_translator.py 仍生成 _healer/HealerError fallback 代码（未清理，因为生成代码的消费者）

### Patterns Established

- **模块删除模式**: 删文件 → 清 import → 清用法 → 清数据层 → 清 UI → 清测试
- **ORM 字段保留 SQLite 列**: 不做 ALTER TABLE，ORM 停止读写即可
- **run.status 单一状态源**: 替代 healing 多状态轮询

### Key Lessons

1. 大规模模块删除（-2999 行）比添加代码更需要系统化计划——逐层清理避免遗漏
2. 重命名变量时必须同步更新测试断言——否则回归测试会在后续 phase 才暴露
3. 简化管道比优化管道更高效——subprocess.run 一次性执行比重试循环可靠得多

### Cost Observations

- Model mix: 100% opus
- Sessions: 4 (116, 117, 118, 119)
- Notable: 1 天完成 4 个阶段 8 个计划，净删除 2999 行代码

## Cross-Milestone Trends

| Metric | v0.6.3 | v0.7.0 | v0.8.0 | v0.8.1 | v0.8.3 | v0.9.0 | v0.10.1 | v0.10.3 | v0.10.7 | v0.10.9 | v0.10.11 |
|--------|--------|--------|--------|--------|--------|--------|---------|---------|---------|---------|----------|
| Phases | 4 | 5 | 5 | 1 | 2 | 4 | 4 | 3 | 3 | 3 | 4 |
| Plans | 10 | 10 | 6 | 1 | 2 | 8 | 6 | 4 | 6 | 6 | 8 |
| Duration (days) | 1 | 2 | 2 | 1 | <1 | 2 | 3 | 1 | 2 | 2 | <1 |
| Tech Debt Added | 0 | 1 (cache assert) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bugs Found/Fixed | 0 | 0 | 0 | 2 (auto-fixed) | 0 | 0 | 0 | 1 (fix commit) | 1 (call count) | 0 | 1 (_healer assert) |
| Code LOC Changed | ~800 | ~300 | ~600 | ~100 | 0 | ~9400 | ~3000 | ~380 | ~4000 | ~1500 | -2999 |

## Milestone: v0.10.9 — 逐步代码生成

**Shipped:** 2026-04-29
**Phases:** 3 | **Plans:** 6

### What Was Built

- StepCodeBuffer 数据结构: append_step 同步翻译 + _derive_wait 3 层等待策略 + assemble() 组装完整测试文件
- append_step_async 弱步骤检测: elem=None 或 <=1 locator 时读取 DOM 快照，调用 LLMHealer 自愈
- runs.py step_callback 逐步即时翻译: 替代事后一次性 generate_and_save，每步累积翻译结果
- code_generator.py 废弃方法清理: 删除 generate_and_save + _heal_weak_steps，12 个任务精简
- 全量回归 316 tests passed + 5 个 E2E 集成测试验证 StepCodeBuffer 完整生命周期

### What Worked

- **Phase 111 StepCodeBuffer 核心实现**: 先建数据结构后集成，解耦清晰
- **Phase 112 集成**: action_dict guarded with 'in locals()' 避免条件块内变量未定义问题
- **Phase 113 回归**: Pydantic ConfigDict 迁移 + docstring 清理 + E2E 一气呵成

### What Was Inefficient

- ROADMAP.md Phase 113 进度表标记 1/2 但实际 2/2 已完成（checkbox 未更新）
- 4 个 debug session 文件残留未清理

### Patterns Established

- **StepCodeBuffer 逐步翻译模式**: 每步即时翻译 + 累积 + 最终组装，替代事后批量翻译
- **弱步骤异步自愈**: 非阻塞 append_step_async，失败静默降级
- **closure-captured buffer**: step_callback 通过闭包捕获 buffer 实例

### Key Lessons

1. StepCodeBuffer 的 _derive_wait 三策略（navigate→networkidle, duration>800ms→实际耗时, click→300ms）覆盖主要等待场景
2. Path import 冲突需要用 PathLib 别名在 try block 内导入
3. 全量回归测试是代码清理的安全网——删除废弃方法前先补集成测试

### Cost Observations

- Model mix: 100% opus
- Sessions: ~3 (111, 112, 113)
- Notable: 2 天完成 3 个阶段 6 个计划，含全量回归验证

## Cross-Milestone Trends

| Metric | v0.6.3 | v0.7.0 | v0.8.0 | v0.8.1 | v0.8.3 | v0.9.0 | v0.10.1 | v0.10.3 | v0.10.7 | v0.10.9 |
|--------|--------|--------|--------|--------|--------|--------|---------|---------|---------|---------|
| Phases | 4 | 5 | 5 | 1 | 2 | 4 | 4 | 3 | 3 | 3 |
| Plans | 10 | 10 | 6 | 1 | 2 | 8 | 6 | 4 | 6 | 6 |
| Duration (days) | 1 | 2 | 2 | 1 | <1 | 2 | 3 | 1 | 2 | 2 |
| Tech Debt Added | 0 | 1 (cache assert) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bugs Found/Fixed | 0 | 0 | 0 | 2 (auto-fixed) | 0 | 0 | 0 | 1 (fix commit) | 1 (call count) | 0 |
| Code LOC Changed | ~800 | ~300 | ~600 | ~100 | 0 | ~9400 | ~3000 | ~380 | ~4000 | ~1500 |

## Milestone: v0.10.3 — DOM 深度修复 - 表格单元格选择精确性

**Shipped:** 2026-04-23
**Phases:** 3 | **Plans:** 4

### What Was Built

- _td_child_depth helper: 保护 td 内部 div/span 不被 bbox 过滤扁平化（最多 2 层）
- Patch 8 列标题注入: `_get_column_header` 通过 thead th 位置映射，注入 `<!-- 列: {header} -->` 注释
- Section 9 全面重写: 四段式交叉定位（定位/操作/验证/异常处理），替代 placeholder 匹配
- E2E 验证: Agent 正确选择销售金额列而非利润列

### What Worked

- **根因精准定位**: 从 E2E 失败日志直接定位到 `_apply_bounding_box_filtering` 扁平化 td 内部结构
- **三层修复策略**: DOM Patch (可见性) + 列注释 (上下文) + Prompt (指导)，每层独立可测试
- **TDD 节奏稳定**: 先写 failing test → implement → pass，4 个 plan 全部按此流程

### What Was Inefficient

- DashScope 账户欠费导致 E2E 不能随时重跑（需充值才能验证）
- Phase 96 利润列断言逻辑需要一次 fix commit（初始 blanket check 过于严格）

### Patterns Established

- **列注释注入模式**: 通过 DOM 注释向 Agent 传递列位置信息，不修改 Agent 决策逻辑
- **四段式 Prompt 结构**: 定位→操作→验证→异常恢复，适用于所有 ERP 表格操作场景
- **td-child depth 限制**: strict less-than 2 层保护，depth 2+ 回退原始逻辑

### Key Lessons

1. browser-use 的 `_apply_bounding_box_filtering` 会将 td 内的 div/span 标记为 `excluded_by_parent`，需要在 monkey-patch 层保护
2. 列标题注释比 placeholder 匹配更可靠——Ant Design 表格不预渲染 input
3. success-based 断言比 blanket 禁止检查更稳健——关注正确结果而非禁止错误模式

### Cost Observations

- Model mix: 100% opus
- Sessions: 1 (all 3 phases in single session)
- Notable: 1 天完成 3 个阶段 4 个计划，含 TDD + E2E 验证

## Milestone: v0.10.7 — 生成测试代码行为优化

**Shipped:** 2026-04-27
**Phases:** 3 | **Plans:** 6

### What Was Built

- ActionTranslator 未知操作参数摘要 + 10 核心类型回归守护
- _build_body 缩进后处理 + validate_syntax 双重防御集成
- LocatorChainBuilder: icon font PUA 过滤 + exact≤4 字符阈值 + 相对 XPath
- _apply_fix 内容匹配多行替换 + 代码定位器 DOM 精准映射
- 结构化 JSON LLM repair prompt {target_snippet, replacement} + 20 行上下文
- E2E healing pipeline 测试: Mock LLM 修复 + ast.parse rollback 安全拒绝

### What Worked

- **8 根因分析驱动**: 64 个文件分析 → 8 个系统性根因 → 精准修复，不做猜测性改动
- **TDD 节奏极快**: Phase 105-107 各 2-5 分钟完成，TDD RED/GREEN 流畅
- **LocatorChainBuilder 渐进优化**: Phase 106 Plan 01 加功能，Plan 02 验证无回归，分离关注点

### What Was Inefficient

- gsd-tools milestone complete 输出了所有 83 phases 的 accomplishments，需手动精简
- 跨阶段上下文累积导致 STATE.md 信息过载

### Patterns Established

- **内容匹配修复模式**: _apply_fix 用代码内容匹配替代行号定位，支持多行修复
- **代码定位器提取**: 从失败行代码中提取定位器，比正则匹配 error_output 更精准
- **结构化 LLM prompt**: JSON schema {target_snippet, replacement} 替代自由文本输出

### Key Lessons

1. 代码生成质量的提升需要全链路修复（翻译→缩进→定位器→自愈），单点修复不够
2. Mock LLM 在 E2E 测试中效果好——避免真实 LLM 调用的非确定性和成本
3. ast.parse rollback 是自愈修复的关键安全网——拒绝语法错误的修复结果

### Cost Observations

- Model mix: 100% opus
- Sessions: ~3 (105, 106, 107)
- Notable: 2 天完成 3 个阶段 6 个计划，含 TDD + E2E

## Cross-Milestone Trends

| Metric | v0.6.3 | v0.7.0 | v0.8.0 | v0.8.1 | v0.8.3 | v0.9.0 | v0.10.1 | v0.10.3 | v0.10.7 |
|--------|--------|--------|--------|--------|--------|--------|---------|---------|---------|
| Phases | 4 | 5 | 5 | 1 | 2 | 4 | 4 | 3 | 3 |
| Plans | 10 | 10 | 6 | 1 | 2 | 8 | 6 | 4 | 6 |
| Duration (days) | 1 | 2 | 2 | 1 | <1 | 2 | 3 | 1 | 2 |
| Tech Debt Added | 0 | 1 (cache assert) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bugs Found/Fixed | 0 | 0 | 0 | 2 (auto-fixed) | 0 | 0 | 0 | 1 (fix commit) | 1 (call count) |
| Code LOC Changed | ~800 | ~300 | ~600 | ~100 | 0 | ~9400 | ~3000 | ~380 | ~4000 |

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

## Milestone: v0.9.0 — Excel 批量导入功能开发