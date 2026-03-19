# Roadmap: aiDriveUITest

## Milestones

- [x] **v0.1 MVP** - Phases 1-4 (shipped 2026-03-14)
- [x] **v0.2 前置条件、接口断言、动态数据** - Phases 5-8 (shipped 2026-03-17)
- [x] **v0.2.1 测试用例调通** - Phases 9-10 (shipped 2026-03-18, Phases 11-12 deferred)
- [x] **v0.3 前置条件集成** - Phases 13-16 (shipped 2026-03-18)
- [ ] **v0.3.1 数据获取方法集成** - Phases 17-19 (in progress)
## Phases
<details>
<summary>v0.1 MVP (Phases 1-4) - SHIPPED 2026-03-14</summary>
- [x] Phase 1: Foundation Fixes (6/6 plans)
- [x] Phase 2: Data Layer Enhancement (4/4 plans)
- [x] Phase 3: Service Layer Restoration (6/6 plans)
- [x] Phase 4: Frontend + E2E Alignment (6/6 plans)
*Archived: .planning/milestones/v0.1-ROADMAP.md*
</details>
<details>
<summary>v0.2 前置条件、接口断言、动态数据 (Phases 5-8) - SHIPPED 2026-03-17</summary>
- [x] Phase 5: 前置条件系统 (4/4 plans) - completed 2026-03-16
- [x] Phase 6: 接口断言集成 (4/4 plans) - completed 2026-03-16
- [x] Phase 7: 动态数据支持 (4/4 plans) - completed 2026-03-17
- [x] Phase 8: 前端实时监控完善 (3/3 plans) - completed 2026-03-17
**Key accomplishments:**
1. 前置条件系统 - 支持 Python 代码格式，Jinja2 变量替换, SSE 实时监控
2. 接口断言集成 - ApiAssertionService 支持时间和数据断言,断言结果独立展示
3. 动态数据支持 - 随机数生成器、时间计算、跨步骤数据缓存
4. 前端实时监控完善 - SSE 事件处理器、报告数据完整性修复
*Archived: .planning/milestones/v0.2-ROADMAP.md*
</details>
<details>
<summary>v0.2.1 测试用例调通 (Phases 9-10) - SHIPPED 2026-03-18</summary>
- [x] Phase 9: 登录用例调通 (2/2 plans) - completed 2026-03-17
- [x] Phase 10: 销售出库用例调通 (4/4 plans) - completed 2026-03-18
- [ ] Phase 11: Bug 修复 - Deferred
- [ ] Phase 12: 文档指南 - Deferred
**Key accomplishments:**
1. 登录用例调通 - 端到端执行成功，报告正确展示
2. 销售出库用例 - 前置条件配置、动态数据生成、API 断言验证通过
*Note: Phases 11-12 推迟到后续版本*
</details>
<details>
<summary>v0.3 前置条件集成 (Phases 13-16) - SHIPPED 2026-03-18</summary>
- [x] Phase 13: 配置基础 (3/3 plans) - completed 2026-03-17
- [x] Phase 14: 后端桥接模块 (3/3 plans) - completed 2026-03-18
- [x] Phase 15: 前端集成 (3/3 plans) - completed 2026-03-18
- [x] Phase 16: 端到端验证 (3/3 plans) - completed 2026-03-18
**Key accomplishments:**
1. 配置基础 - WEBSERP_PATH 环境变量, 启动验证, 文档模板
2. 后端桥接模块 - ExternalPreconditionBridge, 操作码 API, PreconditionService 集成
3. 前端集成 - OperationCodeSelector 组件, 模块分组显示, 代码生成
4. 端到端验证 - E2E 测试, 错误场景测试, 手动测试检查清单
*Archived: .planning/milestones/v0.3-ROADMAP.md*
</details>
---

## v0.3.1 数据获取方法集成 (Phases 17-19)
- [x] **Phase 17: 后端数据获取桥接** - 扫描 base_params.py 并提供数据获取 API (completed 2026-03-18)
- [x] **Phase 18: 前端数据选择器** - DataMethodSelector 组件及参数配置 UI (completed 2026-03-19)
- [ ] **Phase 19: 集成与变量传递** - 前置条件代码生成与 Jinja2 变量替换
---

## Phase Details
### Phase 17: 后端数据获取桥接
**Goal:** 用户可以通过 API 获取 webseleniumerp 中所有 xxx_data() 查询方法的列表和执行结果
**Depends on:** Phase 16 (v0.3 前置条件集成完成)
**Requirements:** DATA-01, DATA-02, DATA-03
**Success Criteria** (what must be TRUE):
  1. 用户调用 API 可获取所有 xxx_data() 方法的列表（按模块分组，包含方法描述）
  2. API 返回每个方法的参数签名信息（参数名、类型）
  3. 用户调用执行 API 可获取指定方法的 JSON 数据结果
  4. 当 WEBSERP_PATH 未配置时，API 返回清晰的错误提示
**Plans:** 3/3 plans complete
Plans:
- [x] 17-01-PLAN.md - Extend bridge module for data method discovery (DATA-01)
- [x] 17-02-PLAN.md - Create data method list API endpoint (DATA-02)
- [x] 17-03-PLAN.md - Create data method execution API endpoint (DATA-03)
### Phase 18: 前端数据选择器
**Goal:** 用户可以在前端选择数据获取方法、配置参数、设置字段提取路径和变量名
**Depends on:** Phase 17 (后端数据获取 API 就绪)
**Requirements:** UI-01, UI-02, UI-03, UI-04
**Success Criteria** (what must be TRUE):
  1. 用户可从按模块分组的下拉列表中选择数据获取方法
  2. 用户可填写方法参数（如 i=2, j=13）
  3. 用户可配置字段提取路径（如 [0].imei）
  4. 用户可设置生成的变量名
  5. 系统自动生成可预览的 Python 代码片段
**Plans:** 5/5 plans complete
Plans:
- [x] 18-01-PLAN.md - API client, types, and DataMethodSelector skeleton (UI-01) - completed 2026-03-18
- [x] 18-02-PLAN.md - Method selection and parameter configuration steps (UI-01, UI-02)
- [x] 18-03-PLAN.md - Data preview, field extraction, and variable naming steps (UI-03, UI-04) - completed 2026-03-18
- [x] 18-04-PLAN.md - TaskForm integration with "获取数据" button (UI-01, UI-02, UI-03, UI-04)
- [x] 18-05-PLAN.md - Variable naming and code preview step (UI-04) - completed 2026-03-19
### Phase 19: 集成与变量传递
**Goal:** 用户配置的数据获取代码可注入前置条件块，获取的数据可在测试步骤中通过 {{变量名}} 引用
**Depends on:** Phase 18 (前端 UI 就绪)
**Requirements:** INT-01, INT-02, INT-03
**Success Criteria** (what must be TRUE):
  1. 用户点击确认后，生成的代码自动插入前置条件文本框
  2. 执行测试时，数据获取结果存入 context 变量
  3. 测试步骤中使用 {{变量名}} 可正确替换为实际获取的数据
  4. 数据获取失败时，测试终止并显示清晰的错误信息
**Plans:** 1/3 plans complete
Plans:
- [x] 19-01-PLAN.md - Update frontend code generation to include className (INT-01) - completed 2026-03-19
- [ ] 19-02-PLAN.md - Implement ContextWrapper with get_data() method (INT-02)
- [ ] 19-03-PLAN.md - Verify API assertion variable substitution (INT-03)
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
| 17. 后端数据获取桥接 | v0.3.1 | 3/3 | Complete | 2026-03-18 |
| 18. 前端数据选择器 | v0.3.1 | 5/5 | Complete | 2026-03-19 |
| 19. 集成与变量传递 | v0.3.1 | 1/3 | In progress | 2026-03-19 |
---
*Roadmap created: 2026-03-14*
*Last updated: 2026-03-19 - Phase 19 plan 01 complete*
