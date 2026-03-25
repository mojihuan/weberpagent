# Roadmap: aiDriveUITest

## Milestone: v0.6.1 表格输入框定位优化

**Goal:** 解决 Agent 无法正确定位表格单元格内输入框的问题，减少类似步骤的无效循环
**Created:** 2026-03-25
---

## Phases

- [x] **Phase 42: DOM 解析器增强** - 确保表格内输入框被正确识别为可交互元素 (completed 2026-03-25)
- [x] **Phase 43: 智能定位与降级** - 实现精确定位和自动降级策略 (completed 2026-03-25)
- [ ] **Phase 44: 日志与验证** - 增强日志输出,验证整体解决方案
---

## Phase Details
### Phase 42: DOM 解析器增强
**Goal:** 表格内的输入框被正确识别为可交互元素,Agent 点击 td 后能自动定位到内部 input 元素
**Depends on:** Phase 41 (v0.6.0 已完成)
**Requirements:** DOM-01
**Success Criteria** (what must be TRUE):
1. Agent 点击 td 元素后，焦点自动转移到内部输入框
2. TD 后处理在每次点击动作后执行
3. 诊断信息记录在 step_stats['td_post_process'] 字段
4. 现有非表格场景的 DOM 解析不受影响
**Plans:** 1/1 plans complete
Plans:
- [x] 42-01: TD 后处理实现 (DOM-01)
---
### Phase 43: 智能定位与降级
**Goal:** Agent 点击表格单元格时能正确定位到内部输入框,失败时自动降级到 JavaScript 方案
**Depends on:** Phase 42
**Requirements:** DOM-02, FALLBACK-01
**Success Criteria** (what must be TRUE):
1. Agent 点击 td 元素时,自动查找并聚焦到内部的 input/textarea/select
2. 当普通点击未能使输入框获得焦点时,自动使用 `page.evaluate()` 设置值
3. 降级策略的触发和执行被记录在执行日志中
4. 用户无需手动介入即可完成表格输入操作
**Plans:** 1/1 plans complete
Plans:
- [x] 43-01: JavaScript fallback for td input (DOM-02, FALLBACK-01)
---
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
**Plans:** 1/2 plans executed
Plans:
- [x] 44-01: Element diagnostics logging (LOG-03)
- [ ] 44-02: Validation and verification (LOG-03)
---
## Progress
**Execution Order:**
Phase 42 -> Phase 43 -> Phase 44
| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 42. DOM 解析器增强 | v0.6.1 | 1/1 | Complete    | 2026-03-25 |
| 43. 智能定位与降级 | v0.6.1 | 1/1 | Complete    | 2026-03-25 |
| 44. 日志与验证 | v0.6.1 | 1/2 | In Progress|  |
---
## Previous Milestone: v0.6.0 Agent 行为优化 (Complete)
### Phase 39: 循环干预优化
**Goal**: 更早检测并干预 Agent 的无效循环行为
**Depends on**: Phase 38
**Requirements**: LOOP-01
**Success Criteria** (what must be TRUE):
  1. Agent 在 stagnation 达到 5 时触发循环干预
  2. 干预后 Agent 能继续执行后续步骤
**Plans**: 2 plans
Plans:
- [x] 39-01: 实现更早的循环干预机制 (LOOP-01)
- [x] 39-02: 验证循环干预效果 (LOOP-01)
### Phase 40: 表格元素定位增强
**Goal**: Agent 能够定位并操作水平滚动表格内的输入字段
**Depends on**: Phase 39
**Requirements**: LOOP-02, LOOP-04
**Success Criteria** (what must be TRUE):
  1. Agent 能通过 scroll_table_and_input 工具定位水平滚动表格内的输入框
  2. 工具自动滚动表格使目标列可见
  3. Agent 根据工具返回的错误消息自行决定后续动作
**Plans**: 2 plans
Plans:
- [x] 40-01: 实现 scroll_table_and_input 工具 (LOOP-02, LOOP-04)
- [x] 40-02: 验证表格定位增强效果 (LOOP-02)
### Phase 41: 配置化与验证
**Goal**: 添加步骤执行统计功能并验证整体优化效果
**Depends on**: Phase 40
**Requirements**: LOG-02
**Success Criteria** (what must be TRUE):
  1. 报告中包含每步执行统计(时间、动作次数、页面变化)
  2. 销售出库用例能完整执行成功(包括步骤 11)
**Plans**: 1 plan
Plans:
- [x] 41-01: 添加步骤执行统计和最终验证 (LOG-02, - 标记 LOOP-03 为已满足
## v0.6.0 Progress (Complete)
**Execution Order:**
Phase 39 -> Phase 40 -> Phase 41
| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 39. 循环干预优化 | v0.6.0 | 2/2 | Complete   | 2026-03-24 |
| 40. 表格元素定位 | v0.6.0 | 2/2 | Complete    | 2026-03-24 |
| 41. 配置化与验证 | v0.6.0 | 1/1 | Complete   | 2026-03-25 |
---
## Coverage
| Requirement | Phase | Status |
|-------------|-------|--------|
| DOM-01 | Phase 42 | Complete |
| DOM-02 | Phase 43 | Complete |
| FALLBACK-01 | Phase 43 | Complete |
| LOG-03 | Phase 44 | Pending |
**Total v0.6.1:** 4/4 requirements mapped (100%)
---
*Roadmap updated: 2026-03-25 - Phase 44 plans created*
