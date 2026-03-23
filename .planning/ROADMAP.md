# Roadmap: aiDriveUITest

## Milestones

- 🔄 **v0.4.2 人工验证断言系统** — Phases 33-35 (in progress)
- ✅ **v0.4.1 断言系统调通** — Phases 28-32 (shipped 2026-03-22) — [Full Details](milestones/v0.4.1-ROADMAP.md)
- ✅ **v0.4.0 断言系统集成** — Phases 23-27 (shipped 2026-03-21)
- ✅ **v0.3.2 测试与Bug修复** — Phases 20-22 (shipped 2026-03-20)
- ✅ **v0.3.1 数据获取方法集成** — Phases 17-19 (shipped 2026-03-19)
- ✅ **v0.3 前置条件集成** — Phases 13-16 (shipped 2026-03-18)
- ✅ **v0.2.1 测试用例调通** — Phases 9-10 (shipped 2026-03-18)
- ✅ **v0.2 前置条件/接口断言** — Phases 5-8 (shipped 2026-03-17)
- ✅ **v0.1 MVP** — Phases 1-4 (shipped 2026-03-14)

## Current Status

**Current:** v0.4.2 人工验证断言系统 (Phase 35)

**Goal:** 验证断言系统能够正确执行真实业务断言（销售出库用例）

**Scope:**
- 仅断言验证（前置条件/步骤假设已能执行）
- 人工执行 + AI 辅助诊断修复

## v0.4.2 Phase Overview

| # | Phase | Goal | Requirements | Status |
|---|-------|------|--------------|--------|
| 33 | 人工验证断言执行 | 验证断言流程 | Complete    | 2026-03-23 |
| 34 | Bug 修复 | 修复发现的问题 | N/A - 已在 Phase 33 中修复 | ⊘ Skipped |
| 35 | 文档完善 | 记录使用方式 | Complete    | 2026-03-23 |

### Phase 33: 人工验证断言执行

**Goal:** 人工执行销售出库测试用例，验证断言系统能正确执行 `sell_sale_item_list_assert`

**Success Criteria:**
1. 用户能在前端配置断言参数（salesOrder、articlesStateStr、saleTime）
2. 执行测试后断言被调用，返回成功或失败结果
3. 断言结果显示在测试报告中
4. `saleTime='now'` 显示为实际时间而非字符串 "now"

**Plans:** 1/1 plans complete

Plans:
- [x] 33-01-PLAN.md — Manual verification of assertion execution flow (5 checkpoint steps)

### Phase 34: Bug 修复

**Goal:** 修复验证过程中发现的影响断言执行的问题

**Success Criteria:**
1. 所有发现的 bug 已记录
2. 关键 bug 已修复并验证

### Phase 35: 文档完善

**Goal:** 记录断言系统的使用方式和常见问题

**Success Criteria:**
1. 断言系统使用文档已创建
2. 常见问题已记录

**Plans:** 1/1 plans complete

Plans:
- [ ] 35-01-PLAN.md — 创建断言系统使用指南文档（工作流程、三层参数详解、FAQ）

---

*Roadmap updated: 2026-03-23 for v0.4.2*
