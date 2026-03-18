# Roadmap: aiDriveUITest

## Milestones

- ✅ **v0.1 MVP** — Phases 1-4 (shipped 2026-03-14)
- ✅ **v0.2 前置条件、接口断言、动态数据** — Phases 5-8 (shipped 2026-03-17)
- ✅ **v0.2.1 测试用例调通** — Phases 9-10 (shipped 2026-03-18, Phases 11-12 deferred)
- ✅ **v0.3 前置条件集成** — Phases 13-16 (shipped 2026-03-18)

## Phases

<details>
<summary>✅ v0.1 MVP (Phases 1-4) — SHIPPED 2026-03-14</summary>
- [x] Phase 1: Foundation Fixes (6/6 plans)
- [x] Phase 2: Data Layer Enhancement (4/4 plans)
- [x] Phase 3: Service Layer Restoration (6/6 plans)
- [x] Phase 4: Frontend + E2E Alignment (6/6 plans)
*Archived: .planning/milestones/v0.1-ROADMAP.md*
</details>

<details>
<summary>✅ v0.2 前置条件、接口断言、动态数据 (Phases 5-8) — SHIPPED 2026-03-17</summary>
- [x] Phase 5: 前置条件系统 (4/4 plans) — completed 2026-03-16
- [x] Phase 6: 接口断言集成 (4/4 plans) — completed 2026-03-16
- [x] Phase 7: 动态数据支持 (4/4 plans) — completed 2026-03-17
- [x] Phase 8: 前端实时监控完善 (3/3 plans) — completed 2026-03-17

**Key accomplishments:**
1. 前置条件系统 - 支持 Python 代码格式，Jinja2 变量替换, SSE 实时监控
2. 接口断言集成 - ApiAssertionService 支持时间和数据断言,断言结果独立展示
3. 动态数据支持 - 随机数生成器、时间计算、跨步骤数据缓存
4. 前端实时监控完善 - SSE 事件处理器、报告数据完整性修复
*Archived: .planning/milestones/v0.2-ROADMAP.md*
</details>

<details>
<summary>✅ v0.2.1 测试用例调通 (Phases 9-10) — SHIPPED 2026-03-18</summary>
- [x] Phase 9: 登录用例调通 (2/2 plans) — completed 2026-03-17
- [x] Phase 10: 销售出库用例调通 (4/4 plans) — completed 2026-03-18
- [ ] Phase 11: Bug 修复 — Deferred
- [ ] Phase 12: 文档指南 — Deferred

**Key accomplishments:**
1. 登录用例调通 - 端到端执行成功，报告正确展示
2. 销售出库用例 - 前置条件配置、动态数据生成、API 断言验证通过
*Note: Phases 11-12 推迟到后续版本*
</details>

<details>
<summary>✅ v0.3 前置条件集成 (Phases 13-16) — SHIPPED 2026-03-18</summary>
- [x] Phase 13: 配置基础 (3/3 plans) — completed 2026-03-17
- [x] Phase 14: 后端桥接模块 (3/3 plans) — completed 2026-03-18
- [x] Phase 15: 前端集成 (3/3 plans) — completed 2026-03-18
- [x] Phase 16: 端到端验证 (3/3 plans) — completed 2026-03-18

**Key accomplishments:**
1. 配置基础 - WEBSERP_PATH 环境变量, 启动验证, 文档模板
2. 后端桥接模块 - ExternalPreconditionBridge, 操作码 API, PreconditionService 集成
3. 前端集成 - OperationCodeSelector 组件, 模块分组显示, 代码生成
4. 端到端验证 - E2E 测试, 错误场景测试, 手动测试检查清单
*Archived: .planning/milestones/v0.3-ROADMAP.md*
</details>

---

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Foundation Fixes | v0.1 | 6/6 | Complete | 2026-03-14 |
| 2. Data Layer Enhancement | v0.1 | 4/4 | Complete | 2026-03-14 |
| 3. Service Layer Restoration | v0.1 | 6/6 | Complete | 2026-03-14 |
| 4. Frontend + E2E Alignment | v0.1 | 6/6 | Complete | 2026-03-14 |
| 5. 前置条件系统 | v0.2 | 4/4 | Complete | 2026-03-16 |
| 6. 接口断言集成 | v0.2 | 4/4 | Complete | 2026-03-16 |
| 7. 动态数据支持 | v0.2 | 4/4 | Complete | 2026-03-17 |
| 8. 前端实时监控完善 | v0.2 | 3/3 | Complete | 2026-03-17 |
| 9. 登录用例调通 | v0.2.1 | 2/2 | Complete | 2026-03-17 |
| 10. 销售出库用例调通 | v0.2.1 | 4/4 | Complete | 2026-03-18 |
| 11. Bug 修复 | v0.2.1 | 0/2 | Deferred | - |
| 12. 文档指南 | v0.2.1 | 0/2 | Deferred | - |
| 13. 配置基础 | v0.3 | 3/3 | Complete | 2026-03-17 |
| 14. 后端桥接模块 | v0.3 | 3/3 | Complete | 2026-03-18 |
| 15. 前端集成 | v0.3 | 3/3 | Complete | 2026-03-18 |
| 16. 端到端验证 | v0.3 | 3/3 | Complete | 2026-03-18 |

---
*Roadmap created: 2026-03-14*
*Last updated: 2026-03-18 - v0.3 milestone archived*
