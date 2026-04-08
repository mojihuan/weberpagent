# Roadmap: aiDriveUITest

## Milestones

- 🚧 **v0.9.0 Excel 批量导入功能开发** — Phases 70-73 (in progress)
- ✅ **v0.8.4 基于 v0.8.3 的研究优化** — Phases 67-69 (shipped 2026-04-07)
- ✅ **v0.8.3 分析报告差距对表格填写影响** — Phases 65-66 (shipped 2026-04-06)
- ✅ **v0.8.2 浏览器模式差异调查** — Phases 63-64 (shipped 2026-04-06)
- ✅ **v0.8.1 修复销售出库表格填写问题** — Phase 62 (shipped 2026-04-06)
- ✅ **v0.8.0 报告完善与 UI 优化** — Phases 57-61 (shipped 2026-04-03)
- ✅ **v0.7.0 更多操作边界测试** — Phases 52-56 (shipped 2026-04-01)
- ✅ **v0.6.3 Agent 可靠性优化** — Phases 48-51 (shipped 2026-03-28)
- ✅ **v0.6.2 回归原生 browser-use** — Phases 45-47 (shipped 2026-03-27)

## Phases

### 🚧 v0.9.0 Excel 批量导入功能开发 (In Progress)

**Milestone Goal:** 实现 Excel 模版设计、解析器、上传 UI 和批量执行完整工作流

- [ ] **Phase 70: Excel 模版设计** — 模版生成 + 下载端点 + 列合约
- [ ] **Phase 71: Excel 导入 UI** — 文件上传 + 预览校验 + 批量创建
- [ ] **Phase 72: 批量执行** — 多任务并行执行框架
- [ ] **Phase 73: 前端集成** — 任务列表页下载模版按钮 + 导入入口

### ✅ v0.8.4 基于 v0.8.3 的研究优化 (Shipped 2026-04-07)

**Milestone Goal:** 实施 v0.8.3 设计文档中的 Agent 表格交互优化策略，实现行标识定位、反重复机制、三级策略优先级和失败恢复

- [ ] **Phase 67: 基础层** — 行标识检测、失败追踪状态、失败模式检测器
- [ ] **Phase 68: DOM Patch 增强** — 行标识注入、策略标注、失败动态标注
- [ ] **Phase 69: 服务集成与 Prompt 规则** — step_callback 集成、Section 9 规则追加

<details>
<summary>✅ v0.8.3 分析报告差距对表格填写影响 (Phases 65-66) — SHIPPED 2026-04-06</summary>

- [x] Phase 65: 差距关联分析 — 1/1 plans
- [x] Phase 66: 优化方案设计 — 1/1 plans

</details>

<details>
<summary>✅ v0.8.2 浏览器模式差异调查 (Phases 63-64) — SHIPPED 2026-04-06</summary>

- [x] Phase 63: 代码对比分析 — 识别 f951791 为根因 commit (2/2 plans)
- [x] Phase 64: 分析报告输出 — 完整技术报告 + 精简摘要 (1/1 plan)

</details>

<details>
<summary>✅ v0.8.1 修复销售出库表格填写问题 (Phase 62) — SHIPPED 2026-04-06</summary>

- [x] Phase 62: DOM Patch + Prompt 增强 — td cell 交互 + Section 9 click-to-edit 指导 (1/1 plan)

</details>

<details>
<summary>✅ v0.8.0 报告完善与 UI 优化 (Phases 57-61) — SHIPPED 2026-04-03</summary>

- [x] Phase 57: AI 推理格式优化 — Eval/Verdict/Memory/Goal 分行彩色 badge (1/1 plan)
- [x] Phase 58: 执行步骤展示 — StepTimeline 统一时间线 (1/1 plan)
- [x] Phase 59: 报告步骤展示 — 报告详情时间线 (2/2 plans)
- [x] Phase 60: 任务表单优化 — 删除 api_assertions (2/2 plans)
- [x] Phase 61: E2E 验证 — 6/6 检查 PASS (2/2 plans)

</details>

<details>
<summary>✅ v0.7.0 更多操作边界测试 (Phases 52-56) — SHIPPED 2026-04-01</summary>

- [x] Phase 52: Prompt 增强 — 键盘操作 (3/3 plans)
- [x] Phase 53: Prompt 增强 — 表格交互 (3/3 plans)
- [x] Phase 54: 文件导入 (2/2 plans)
- [x] Phase 55: 断言参数调优 (skipped)
- [x] Phase 56: E2E 综合验证 (2/2 plans)

</details>

<details>
<summary>✅ v0.6.3 Agent 可靠性优化 (Phases 48-51) — SHIPPED 2026-03-28</summary>

- [x] Phase 48: 监控模块与 Agent 子类 (4/4 plans)
- [x] Phase 49: 提示词优化与参数调优 (2/2 plans)
- [x] Phase 50: AgentService 集成 (2/2 plans)
- [x] Phase 51: 端到端验证 (2/2 plans)

</details>

<details>
<summary>✅ v0.6.2 回归原生 browser-use (Phases 45-47) — SHIPPED 2026-03-27</summary>

- [x] Phase 45: 代码移除 (5/5 plans)
- [x] Phase 46: 代码简化与测试 (2/2 plans)
- [x] Phase 47: 验证 (0/1 plans)

</details>

## Phase Details

### Phase 70: Excel 模版设计 — 模版生成与列合约
**Goal**: 创建标准化的 .xlsx 模版生成器、共享列合约 (TEMPLATE_COLUMNS) 和模版下载 API 端点
**Depends on**: Nothing (first phase of v0.9.0)
**Requirements**: TMPL-01, TMPL-02
**Success Criteria** (what must be TRUE):
  1. GET /tasks/template returns a valid .xlsx file with content-disposition header
  2. Template contains styled headers with 6 columns matching TEMPLATE_COLUMNS
  3. Template has DataValidation on max_steps column (1-100)
  4. Template has freeze panes, README sheet, and 2 example rows
**Plans**: 2 plans

Plans:
- [x] 70-01: Excel 模版生成器 + 列合约 + 单元测试 + 下载端点
- [ ] 70-02: Excel 解析器 + 错误收集

### Phase 67: 基础层 — 行标识检测与失败追踪状态
**Goal**: DOM Patch 能从 ERP 表格行中检测行标识，失败追踪状态在每次 run 正确初始化和重置，失败模式检测器能识别三种 ERP 表格交互失败
**Depends on**: Nothing (first phase of v0.8.4)
**Requirements**: ROW-01, ANTI-01, RECOV-01
**Success Criteria** (what must be TRUE):
  1. 给定包含 `<tr>` 子 `<td>` 文本为 "I352017041234567" 的 DOM 节点，`_detect_row_identity()` 返回提取的行标识字符串
  2. `_failure_tracker` 以 `backend_node_id` 为键存储 `{count, last_error, mode}`，`update_failure_tracker()` 能写入新记录和累加失败次数，`reset_failure_tracker()` 清空所有记录
  3. `reset_failure_tracker()` 作为独立函数在每次 run 开始时被调用，不受 `_PATCHED` 幂等保护影响
  4. StallDetector 新增 `detect_failure_mode()` 返回 `FailureDetectionResult`，能识别三种模式：点击无 DOM 变化（dom_hash 比对）、误点错误列（evaluation 关键词匹配）、编辑态未激活（input 操作失败）
**Plans**: 2 plans

Plans:
- [x] 67-01: 行标识检测与失败追踪状态
- [x] 67-02: 失败模式检测器

### Phase 68: DOM Patch 增强 — 行标识注入与策略标注
**Goal**: DOM dump 序列化输出包含行标识注释和策略层级标注，Agent 可据此锁定目标行并选择正确的交互策略，失败元素动态标注防止重复尝试
**Depends on**: Phase 67
**Requirements**: ROW-02, ROW-03, STRAT-01, STRAT-02, STRAT-03, ANTI-02
**Success Criteria** (what must be TRUE):
  1. DOM dump 序列化输出中，含商品编号的行上方出现 `<!-- 行: {id} -->` 注释，Agent 可据此锁定目标行
  2. 行内 input 元素带有行归属标注，Agent 可区分不同行的相同 placeholder input（如两行都有"请输入数量"）
  3. 可见 input 标注为策略 1，hidden input 标注为策略 2，同一元素策略 1 失败 2 次后标注降级为策略 2，策略 2 失败 2 次后降级为策略 3
  4. 策略标注和失败标注只出现在已失败元素上，未失败元素不显示任何策略/失败信息，避免 evaluate JS 偏差
  5. 所有对 `_assign_interactive_indices` 的增强合并到 Patch 4 的单一 wrapper 中，不产生多层 wrapping 链
**Plans**: 2 plans

Plans:
- [x] 68-01: Patch 4 增强 — sidecar 字典 + 行归属与策略判定 (ROW-03, STRAT-01, STRAT-03)
- [x] 68-02: 合并 Patch 6+7 — 行标识注释 + 失败动态标注注入 (ROW-02, STRAT-02, ANTI-02)

### Phase 69: 服务集成与 Prompt 规则
**Goal**: step_callback 将失败检测结果写入 _failure_tracker，Section 9 包含行标识、反重复、策略优先级和失败恢复的完整操作规则
**Depends on**: Phase 68
**Requirements**: ANTI-03, RECOV-02, RECOV-03, PROMPT-01, PROMPT-02, PROMPT-03
**Success Criteria** (what must be TRUE):
  1. step_callback 在 detector calls 区域调用 `update_failure_tracker()` 和 `detect_failure_mode()`，将 evaluation 失败关键词和 dom_hash 变化检测结果写入 tracker
  2. Section 9 包含行标识使用规则，指导 Agent 看到行标识注释后锁定目标行并在行内操作
  3. Section 9 包含反重复规则，指导 Agent 看到失败标注后切换策略，不在同一元素重复尝试
  4. Section 9 包含策略优先级规则，指导 Agent 遇到策略标注时优先使用策略 1，失败后按标注降级
  5. Section 9 包含 ERP 表格三种失败模式的检测-标注-切换操作恢复流程
**Plans**: 2 plans

Plans:
- [x] 69-01: step_callback 集成与状态重置
- [x] 69-02: Section 9 Prompt 规则追加

## Progress

**Execution Order:**
Phases execute in numeric order: 70 -> 71 -> 72 -> 73

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 70. Excel 模版设计 | v0.9.0 | 1/2 | In Progress | |
| 67. 基础层 | v0.8.4 | 2/2 | Complete    | 2026-04-07 |
| 68. DOM Patch 增强 | v0.8.4 | 2/2 | Complete    | 2026-04-07 |
| 69. 服务集成与 Prompt 规则 | v0.8.4 | 2/2 | Complete    | 2026-04-07 |

---
*Roadmap updated: 2026-04-07 — Phase 68 plan finalized*
