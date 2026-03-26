# Roadmap: aiDriveUITest

## Milestone: v0.6.2 回归原生 browser-use

**Goal:** 移除所有自定义的 browser-use 扩展方法，完全依赖 browser-use 原生能力执行测试
**Created:** 2026-03-26
---

## Phases

- [x] **Phase 45: 代码移除** - 移除所有自定义 browser-use 扩展方法 (completed 2026-03-26)
- [ ] **Phase 46: 代码简化与测试** - 简化 step_callback 并更新测试
- [ ] **Phase 47: 验证** - 验证基础功能正常运行
---

## Phase Details
### Phase 45: 代码移除
**Goal:** 所有自定义扩展方法从代码库中完全移除，不再有 scroll_table_and_input 工具、TD 后处理、JavaScript fallback、元素诊断日志和循环干预逻辑
**Depends on:** Phase 44 (v0.6.1 已完成)
**Requirements:** CLEANUP-01, CLEANUP-02, CLEANUP-03, CLEANUP-04, CLEANUP-05
**Success Criteria** (what must be TRUE):
1. `backend/agent/tools/` 目录及 scroll_table_tool.py 文件不存在
2. `_post_process_td_click` 方法已从 agent_service.py 中删除
3. `_fallback_input` 方法已从 agent_service.py 中删除
4. `_collect_element_diagnostics` 方法已从 agent_service.py 中删除
5. `LoopInterventionTracker` 类及相关变量已从 agent_service.py 中删除
**Plans:** 5/5 plans complete

Plans:
- [x] 45-01: Delete tools directory (CLEANUP-01) - Wave 2
- [x] 45-02: Remove TD post-processing (CLEANUP-02) - Wave 1
- [x] 45-03: Remove fallback and diagnostics (CLEANUP-03, CLEANUP-04) - Wave 1
- [x] 45-04: Remove LoopInterventionTracker (CLEANUP-05) - Wave 1
- [x] 45-05: Remove test classes for deleted methods - Wave 3

### Phase 46: 代码简化与测试
**Goal:** step_callback 仅保留基础日志功能，所有相关测试已更新并通过
**Depends on:** Phase 45
**Requirements:** SIMPLIFY-01, SIMPLIFY-02, TEST-01
**Success Criteria** (what must be TRUE):
1. step_callback 仅记录 URL、DOM、动作、推理和截图，无自定义扩展调用
2. Agent 创建时不传入 tools 参数，无 register_scroll_table_tool 导入
3. test_scroll_table_tool.py 测试文件已删除
4. test_agent_service.py 中依赖自定义方法的测试已更新或删除
5. 所有剩余单元测试通过
**Plans:** TBD

### Phase 47: 验证
**Goal:** Agent 能正常启动、执行测试并生成报告，基础功能完全正常
**Depends on:** Phase 46
**Requirements:** VALIDATE-01
**Success Criteria** (what must be TRUE):
1. Agent 能正常启动并连接到目标页面
2. step_callback 正常记录执行日志
3. 截图正常保存到指定目录
4. 测试报告正常生成
**Plans:** TBD

## Progress
**Execution Order:**
Phase 45 -> Phase 46 -> Phase 47
| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 45. 代码移除 | v0.6.2 | 5/5 | Complete   | 2026-03-26 |
| 46. 代码简化与测试 | v0.6.2 | 0/0 | Not started | - |
| 47. 验证 | v0.6.2 | 0/0 | Not started | - |
---

## Previous Milestone: v0.6.1 表格输入框定位优化 (Complete)
### Phase 42: DOM 解析器增强
**Goal:** 表格内的输入框被正确识别为可交互元素,Agent 点击 td 后能自动定位到内部 input 元素
**Depends on:** Phase 41 (v0.6.0 已完成)
**Requirements:** DOM-01
**Success Criteria** (what must be TRUE):
  1. Agent 点击 td 元素后，焦点自动转移到内部输入框
  2. TD 后处理在每次点击动作后执行
  3. 诊断信息记录在 step_stats['td_post_process'] 字段
  4. 现有非表格场景的 DOM 解析不受影响
**Plans:** 1 plan
Plans:
- [x] 42-01: TD 后处理实现 (DOM-01)
### Phase 43: 智能定位与降级
**Goal:** Agent 点击表格单元格时能正确定位到内部输入框,失败时自动降级到 JavaScript 方案
**Depends on:** Phase 42
**Requirements:** DOM-02, FALLBACK-01
**Success Criteria** (what must be TRUE):
  1. Agent 点击 td 元素时,自动查找并聚焦到内部的 input/textarea/select
  2. 当普通点击未能使输入框获得焦点时,自动使用 `page.evaluate()` 设置值
  3. 降级策略的触发和执行被记录在执行日志中
  4. 用户无需手动介入即可完成表格输入操作
**Plans:** 1 plan
Plans:
- [x] 43-01: JavaScript fallback for td input (DOM-02, FALLBACK-01)
### Phase 44: 日志与验证
**Goal:** 开发者能通过日志快速定位元素定位失败原因,整体解决方案得到验证
**Depends on:** Phase 42
**Requirements:** LOG-03
**Success Criteria** (what must be TRUE):
  1. 日志记录 `is_interactive=False` 的元素信息(标签、索引、父元素链)
  2. 日志记录 `ignored_by_paint_order=True` 的父元素链
  3. 日志记录降级策略的触发原因和执行结果
  4. Agent 能在 3 步以内成功定位并输入表格单元格内的输入框
  5. Stagnation 不再因输入框定位问题超过 5
**Plans:** 2 plans
Plans:
- [x] 44-01: Element diagnostics logging (LOG-03)
- [ ] 44-02: Validation and verification (LOG-03)
## v0.6.1 Progress (Complete)
**Execution Order:**
Phase 42 -> Phase 43 -> Phase 44
| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 42. DOM 解析器增强 | v0.6.1 | 1/1 | Complete    | 2026-03-25 |
| 43. 智能定位与降级 | v0.6.1 | 1/1 | Complete   | 2026-03-25 |
| 44. 日志与验证 | v0.6.1 | 1/2 | In Progress | - |
---

## Coverage
| Requirement | Phase | Status |
|-------------|-------|--------|
| CLEANUP-01 | Phase 45 | Pending |
| CLEANUP-02 | Phase 45 | Pending |
| CLEANUP-03 | Phase 45 | Pending |
| CLEANUP-04 | Phase 45 | Pending |
| CLEANUP-05 | Phase 45 | Pending |
| SIMPLIFY-01 | Phase 46 | Pending |
| SIMPLIFY-02 | Phase 46 | Pending |
| TEST-01 | Phase 46 | Pending |
| VALIDATE-01 | Phase 47 | Pending |
**Total v0.6.2:** 9/9 requirements mapped (100%)
---
*Roadmap updated: 2026-03-26 - Phase 45 plans created with corrected wave structure*
