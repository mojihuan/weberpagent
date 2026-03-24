# Roadmap: aiDriveUITest

## Milestones

- **v0.4.2 人工验证断言系统** - Phases 33-35 (shipped 2026-03-23)
- **v0.5.0 项目云端部署** - Phases 36-38 (shipped 2026-03-24)
- **v0.6.0 Agent 行为优化** - Phases 39-41 (current)

## Phases

<details>
<summary>v0.5.0 项目云端部署 (Phases 36-38) - SHIPPED 2026-03-24</summary>

### Phase 36: Git 仓库迁移
**Goal**: 项目代码迁移到用户自己的仓库，便于云端部署
**Plans**: 2 plans

Plans:
- [x] 36-01-PLAN.md - Git remote 替换
- [x] 36-02-PLAN.md - webseleniumerp 子目录管理

### Phase 37: 云服务器选型
**Goal**: 选择并购买符合预算要求的云服务器
**Plans**: 2 plans

Plans:
- [x] 37-01-PLAN.md - 云服务器调研报告
- [x] 37-02-PLAN.md - 购买并验证 SSH 登录

### Phase 38: 部署执行
**Goal**: 将项目完整部署到云端服务器
**Plans**: 1 plan

Plans:
- [x] 38-01: 部署验证与归档

</details>

---

## v0.6.0 Agent 行为优化 (Current)

**Milestone Goal:** 优化 Agent 在复杂场景下的执行效率，减少无效循环，提高任务成功率

**Context:** 从执行日志发现 agent 在步骤 11（输入销售金额）陷入 stagnation=27 的循环，浪费了大量步骤。browser-use 已有循环检测机制但只提醒不干预。

### Phase 39: 循环干预优化 (基础)
**Goal**: 实现更早的循环干预和增强日志
**Depends on**: Nothing
**Requirements**: LOOP-01, LOG-01
**Success Criteria** (what must be TRUE):
  1. stagnation 达到 5 时自动尝试跳过当前困难步骤
  2. 循环检测触发时输出详细诊断信息（stagnation 值、最近动作、页面变化）
  3. 用户可在报告中看到循环干预记录
**Plans**: 2 plans

Plans:
- [x] 39-01: 实现自定义 hook 监控 stagnation 并触发跳过逻辑 (LOOP-01)
- [x] 39-02: 增强循环日志输出，包含完整诊断信息 (LOG-01)

### Phase 40: 表格元素定位增强
**Goal**: 解决水平滚动表格内输入字段定位问题
**Depends on**: Phase 39
**Requirements**: LOOP-02, LOOP-04
**Success Criteria** (what must be TRUE):
  1. 销售出库场景中能成功输入销售金额
  2. 水平滚动表格内的输入字段能被正确定位和操作
  3. 无法完成的步骤被跳过后，后续步骤能继续执行
**Plans**: 2 plans

Plans:
- [x] 40-01: 创建自定义工具 `scroll_table_and_input` (LOOP-02)
- [ ] 40-02: 实现智能跳过与继续逻辑 (LOOP-04)

### Phase 41: 配置化与验证
**Goal**: 允许用户自定义参数，并验证整体优化效果
**Depends on**: Phase 40
**Requirements**: LOOP-03, LOG-02
**Success Criteria** (what must be TRUE):
  1. 用户可在 TaskConfig 中配置 max_stagnation 等参数
  2. 报告中包含每步执行统计（时间、动作次数、页面变化）
  3. 销售出库用例能完整执行成功（包括步骤 11）
**Plans**: 2 plans

Plans:
- [ ] 41-01: 扩展 AgentSettings 配置项 (LOOP-03)
- [ ] 41-02: 添加步骤执行统计和最终验证 (LOG-02)

## Progress

**Execution Order:**
Phase 39 → Phase 40 → Phase 41

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 39. 循环干预优化 | v0.6.0 | 2/2 | Complete   | 2026-03-24 |
| 40. 表格元素定位 | v0.6.0 | 1/2 | In Progress|  |
| 41. 配置化与验证 | v0.6.0 | 0/2 | Pending | - |

---

## Previous Milestones (Archived)

<details>
<summary>v0.4.2 人工验证断言系统 (Phases 33-35) - SHIPPED 2026-03-23</summary>

### Phase 33: Bug 修复
**Goal**: 修复断言执行中发现的问题
**Plans**: 2 plans

Plans:
- [x] 33-01: 修复字段命名和 Headers 解析问题
- [x] 33-02: 修复时间偏移和 UI 优化

### Phase 34: 断言执行验证
**Goal**: 验证断言系统端到端可用
**Plans**: 1 plan

Plans:
- [x] 34-01: 执行 sell_sale_item_list_assert 验证

### Phase 35: 文档完善
**Goal**: 创建断言系统使用指南
**Plans**: 1 plan

Plans:
- [x] 35-01: 编写断言系统使用指南

</details>

---

*Roadmap updated: 2026-03-24 - v0.6.0 milestone started*
