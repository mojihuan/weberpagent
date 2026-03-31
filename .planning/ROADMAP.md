# Roadmap: aiDriveUITest

## Milestones

- ✅ **v0.6.3 Agent 可靠性优化** — Phases 48-51 (shipped 2026-03-28)
- ✅ **v0.6.2 回归原生 browser-use** — Phases 45-47 (shipped 2026-03-27)
- 🚧 **v0.7.0 更多操作边界测试** — Phases 52-56 (in progress)

## Phases

<details>
<summary>✅ v0.6.3 Agent 可靠性优化 (Phases 48-51) — SHIPPED 2026-03-28</summary>

- [x] Phase 48: 监控模块与 Agent 子类 (4/4 plans) — completed 2026-03-28
- [x] Phase 49: 提示词优化与参数调优 (2/2 plans) — completed 2026-03-28
- [x] Phase 50: AgentService 集成 (2/2 plans) — completed 2026-03-28
- [x] Phase 51: 端到端验证 (2/2 plans) — completed 2026-03-28

</details>

<details>
<summary>✅ v0.6.2 回归原生 browser-use (Phases 45-47) — SHIPPED 2026-03-27</summary>

- [x] Phase 45: 代码移除 (5/5 plans) — completed 2026-03-26
- [x] Phase 46: 代码简化与测试 (2/2 plans) — completed 2026-03-26
- [x] Phase 47: 验证 (0/1 plans) — completed 2026-03-26

</details>

### 🚧 v0.7.0 更多操作边界测试 (In Progress)

**Milestone Goal:** 扩展 AI Agent 操作能力边界，覆盖 ERP 测试中表格交互、文件导入、键盘操作和缓存断言等场景。

- [x] **Phase 52: Prompt 增强 — 键盘操作** — 扩展 ENHANCED_SYSTEM_MESSAGE 添加键盘操作指导，Agent 能执行 Control+a 全选覆盖、Enter 搜索触发、Escape 关闭弹窗 (gap closure in progress) (completed 2026-03-30)
- [x] **Phase 53: Prompt 增强 — 表格交互** — 扩展 ENHANCED_SYSTEM_MESSAGE 添加表格操作指导，Agent 能定位 checkbox、超链接、图标按钮 (completed 2026-03-31)
- [x] **Phase 54: 文件导入** — 验证并增强 Agent 文件上传能力，覆盖 Excel 和图片上传场景 (completed 2026-03-31)
- [ ] **Phase 55: 断言参数调优与缓存断言** — 修复断言参数传递问题，实现缓存查询和断言验证
- [x] **Phase 56: E2E 综合验证** — 用全部 11 个 ERP 测试用例端到端验证所有新操作能力 + 断言功能 (completed 2026-03-31)

## Phase Details

### Phase 52: Prompt 增强 — 键盘操作
**Goal**: Agent 能通过 Prompt 指导正确执行键盘操作（Enter 搜索触发、Escape 关闭弹窗、Control+a 全选覆盖）
**Depends on**: Phase 51 (v0.6.3 ENHANCED_SYSTEM_MESSAGE 基础)
**Requirements**: KB-01, KB-02, KB-03
**Success Criteria** (what must be TRUE):
  1. Agent 能在搜索框中使用 send_keys('Enter') 触发搜索（KB-02）
  2. Agent 能使用 send_keys('Escape') 关闭日期选择器等弹窗（KB-03）
  3. Agent 能使用 send_keys('Control+a') + input 覆盖输入框内容（KB-01）
  4. ENHANCED_SYSTEM_MESSAGE 中包含键盘操作的明确指导段落（第 6 段）
**Plans**: 3 plans

Plans:
- [x] 52-01-PLAN.md — TDD: 添加键盘操作测试 + ENHANCED_SYSTEM_MESSAGE 第 6 段
- [x] 52-02-PLAN.md — 采购单 ERP 场景验证（Enter/Escape/Control+a）
- [x] 52-03-PLAN.md — Gap closure: 强化 Escape/Control+a prompt 措辞 + 聚焦验证

### Phase 53: Prompt 增强 — 表格交互
**Goal**: Agent 能准确定位并操作表格中的 checkbox、超链接和图标按钮
**Depends on**: Phase 52
**Requirements**: TBL-01, TBL-02, TBL-03, TBL-04
**Success Criteria** (what must be TRUE):
  1. Agent 能定位并点击表格行中的 checkbox 实现单行选择
  2. Agent 能定位并点击表头的全选 checkbox 实现批量全选
  3. Agent 能识别并点击表格中的超链接文本（如订单号、物品编号链接）
  4. Agent 能定位并点击表格行中的图标/操作按钮（编辑、删除、查看等）
  5. ENHANCED_SYSTEM_MESSAGE 中包含表格交互的明确指导段落
**Plans**: 2 plans

Plans:
- [x] 53-01-PLAN.md — TDD: 添加表格交互测试 + ENHANCED_SYSTEM_MESSAGE 第 7 段
- [x] 53-02-PLAN.md — 采购单列表 ERP 场景验证（checkbox 单选/全选、超链接、图标按钮）

### Phase 54: 文件导入
**Goal**: Agent 能触发文件上传对话框并成功上传 Excel 和图片文件完成数据导入
**Depends on**: Phase 53
**Requirements**: IMP-01, IMP-02
**Success Criteria** (what must be TRUE):
  1. Agent 能点击导入按钮触发文件上传对话框并上传 Excel 文件完成数据导入
  2. Agent 能点击上传按钮触发文件上传对话框并上传图片文件
  3. ENHANCED_SYSTEM_MESSAGE 中包含文件上传操作的指导段落
**Plans**: 2 plans

Plans:
- [x] 54-01-PLAN.md — TDD: 添加文件上传测试 + scan_test_files + ENHANCED_SYSTEM_MESSAGE 第 8 段
- [x] 54-02-PLAN.md — ERP 场景验证（采购单 Excel 导入 + 商品图片上传）

### Phase 55: 断言参数调优与缓存断言
**Goal**: 断言接口参数正确传递，且支持执行前查询缓存、执行后用缓存值断言的完整流程
**Depends on**: Phase 54
**Requirements**: AST-01, AST-02, CAC-01, CAC-02
**Success Criteria** (what must be TRUE):
  1. 断言调用能正确传递 headers 参数并完成接口验证
  2. inventory_list_data 的 i/j 参数组合正确传递并返回有效库存数据
  3. 执行用例步骤前能通过查询列表获取物品编号等数据并缓存到 context
  4. 执行完用例后能用缓存的值进行断言验证（无需硬编码唯一标识）
**Plans**: TBD

Plans:
- [ ] 55-01: 修复断言参数传递问题（headers、i/j 参数）
- [ ] 55-02: 实现缓存查询与断言验证流程

### Phase 56: E2E 综合验证
**Goal**: 用全部 11 个 ERP 测试用例（9 操作类 + 2 断言类）端到端验证 Phase 52-54 新增操作能力 + AST-01/02 断言功能协同工作
**Depends on**: Phase 55
**Requirements**: KB-01, KB-02, KB-03, TBL-01, TBL-02, TBL-03, TBL-04, IMP-01, IMP-02, AST-01, AST-02
**Success Criteria** (what must be TRUE):
  1. 键盘操作测试用例（Control+a 全选覆盖、Enter 搜索触发、ESC 关闭弹窗）全部执行通过
  2. 表格交互测试用例（checkbox、超链接、图标）全部执行通过
  3. 文件导入测试用例（Excel、图片上传）全部执行通过
  4. 断言验证测试用例（headers 参数、i/j 参数组合）全部执行通过
  5. 综合验证报告正确汇总全部 11 个场景结果
**Plans**: 2 plans

Plans:
- [x] 56-01-PLAN.md — 创建断言测试步骤文档 + 验证测试环境就绪
- [x] 56-02-PLAN.md — 执行全部 11 个 E2E 测试用例 + 生成综合验证报告

## Progress

**Execution Order:**
Phases execute in numeric order: 52 → 53 → 54 → 55 → 56

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 52. Prompt 增强 — 键盘操作 | v0.7.0 | 3/3 | Complete    | 2026-03-30 |
| 53. Prompt 增强 — 表格交互 | v0.7.0 | 3/3 | Complete | 2026-03-31 |
| 54. 文件导入 | v0.7.0 | 2/2 | Complete    | 2026-03-31 |
| 55. 断言参数调优与缓存断言 | v0.7.0 | 0/2 | Not started | - |
| 56. E2E 综合验证 | v0.7.0 | 2/2 | Complete    | 2026-03-31 |

---

*Roadmap updated: 2026-03-31 - Phase 56 planned: 2 plans (assertion doc + env prep, E2E execution + report)*
