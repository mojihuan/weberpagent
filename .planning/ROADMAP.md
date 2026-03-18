# Roadmap: aiDriveUITest

## Milestones

- ✅ **v0.1 MVP** — Phases 1-4 (shipped 2026-03-14)
- ✅ **v0.2 前置条件、接口断言、动态数据** — Phases 5-8 (shipped 2026-03-17)
- ⏸️ **v0.2.1 测试用例调通** — Phases 9-12 (partially complete, blocked by erp_api module)
- 🚧 **v0.3 前置条件集成** — Phases 13+ (current)

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
    [x] Phase 8: 前端实时监控完善 (3/3 plans) — completed 2026-03-17
**Key accomplishments:**
1. 前置条件系统 - 支持 Python 代码格式，Jinja2 变量替换, SSE 实时监控
2. 接口断言集成 - ApiAssertionService 支持时间和数据断言,断言结果独立展示
3. 动态数据支持 - 随机数生成器、 时间计算、跨步骤数据缓存
4. 前端实时监控完善 - SSE 事件处理器、报告数据完整性修复
*Archived: .planning/milestones/v0.2-ROADMAP.md*
</details>
### ⏸️ v0.2.1 测试用例调通 (Partially Complete - Blocked)
**Milestone Goal:** 调通核心测试用例的端到端执行流程
**Status:** Phase 10 blocked by erp_api module - missing required functions
- [x] **Phase 9: 登录用例调通** - Complete
- [ ] **Phase 10: 销售出库用例调通** - 2/4 plans complete (blocked)
- [ ] **Phase 11: Bug 修复** - Deferred
- [ ] **Phase 12: 文档指南** - Deferred
## Phase Details
### Phase 9: 登录用例调通
**Goal**: 登录测试用例可以从前端创建到执行成功，报告正确展示
**Depends on**: Phase 8 (前端实时监控完善)
**Requirements**: LOGN-01, LOGN-02, LOGN-03
**Success Criteria** (what must be TRUE):
  1. QA 可以在前端创建一个 4 步骤的登录测试任务
  2. 登录用例执行后所有步骤显示成功状态
  3. 测试报告中正确显示每个步骤的执行结果和截图
**Plans**: 2 plans
Plans:
- [x] 09-01: 创建并执行登录测试用例
- [x] 09-02: 验证报告展示正确性
### Phase 10: 销售出库用例调通
**Goal**: 销售出库测试用例（含前置条件、动态数据、API断言）端到端执行成功
**Depends on**: Phase 9 (登录用例调通，确保基础流程稳定)
**Requirements**: SALE-01, SALE-02, SALE-03, SALE-04, SALE-05, SALE-06, SALE-07
**Success Criteria** (what must be TRUE):
  1. QA 可以在前端配置前置条件 `self.pre.operations(data=['FA1', 'HC1'])`
  2. QA 可以在步骤中使用 `self.copy()` 和 `self.affix()` 引用动态数据
  3. QA 可以在步骤中使用 `self.sf` 生成随机数
  4. QA 可以配置 API 断言验证销售单号、状态、时间
  5. 前置条件执行结果正确传递到测试步骤中
  6. API 断言结果在报告中正确展示（通过/失败状态）
**Plans**: 4 plans
Plans:
- [x] 10-01: 配置前置条件并验证数据传递
- [x] 10-02: 配置动态数据方法并验证
- [x] 10-03: 配置 API 断言并验证报告展示
- [ ] 10-04: 完整执行销售出库用例
### Phase 11: Bug 修复
**Goal**: 调通过程中发现的执行引擎和前端 Bug 已修复
**Depends on**: Phase 10 (完成调试，收集 Bug 清单)
**Requirements**: BUGS-01, BUGS-02
**Success Criteria** (what must be TRUE):
  1. 调通过程中发现的执行引擎 Bug 全部修复，不再阻塞测试执行
  2. 调通过程中发现的前端 Bug 全部修复，UI 操作流畅无阻塞
**Plans**: 2 plans
Plans:
- [ ] 11-01: 修复执行引擎 Bug
- [ ] 11-02: 修复前端 Bug
### Phase 12: 文档指南
**Goal**: QA 有清晰的前端填写指南，可以独立创建测试用例
**Depends on**: Phase 11 (所有 Bug 已修复，功能稳定)
**Requirements**: DOCS-01, DOCS-02
**Success Criteria** (what must be TRUE):
  1. QA 可以按照登录用例指南独立创建并执行登录测试
  2. QA 可以按照销售出库用例指南独立配置前置条件、动态数据和断言
**Plans**: 2 plans
Plans:
- [ ] 12-01: 编写登录用例前端填写指南
- [ ] 12-02: 编写销售出库用例前端填写指南
### 🚧 v0.3 前置条件集成 (Current)
**Milestone Goal:** 将 webseleniumerp 项目的 base_prerequisites.py 集成到当前平台
**Status:** In Progress
- [x] **Phase 13: 配置基础** - 3/3 plans (Complete)
- [x] **Phase 14: 后端桥接模块** - 3/3 plans (completed 2026-03-18)
- [x] **Phase 15: 前端集成** - 3/3 plans (completed 2026-03-18)
- [ ] **Phase 16: 端到端验证** - 0/? plans
## Phase Details
### Phase 13: 配置基础
**Goal**: 配置 WEBSERP_PATH 环境变量，提供 webseleniumerp 配置文档
**Depends on**: None
**Requirements**: CONFIG-01, CONFIG-02, CONFIG-03
**Success Criteria** (what must be TRUE):
  1. 用户可以在 .env 中配置 WEBSERP_PATH 指向 webseleniumerp 项目路径
  2. 系统启动时验证 WEBSERP_PATH 路径有效性
  3. 提供 webseleniumerp 的 config/settings.py 模板文档
**Plans**: 3 plans
Plans:
- [x] 13-01: Add weberp_path field to Settings class
- [x] 13-02: Implement startup validation for WEBSERP_PATH
- [x] 13-03: Add webseleniumerp documentation to README.md
### Phase 14: 后端桥接模块
**Goal**: 创建 ExternalPreconditionBridge 模块，提供操作码 API
**Depends on**: Phase 13 (配置基础)
**Requirements**: BRIDGE-01, BRIDGE-02, BRIDGE-03, BRIDGE-04
**Success Criteria** (what must be TRUE):
  1. 创建 ExternalPreconditionBridge 模块，隔离外部项目导入
  2. 实现 get_available_operations() 返回操作码列表及描述
  3. 提供 `/api/external-operations` API 端点
  4. 实现操作码执行功能，与现有 PreconditionService 集成
**Plans**: 3 plans
Plans:
- [x] 14-01: Create ExternalPreconditionBridge module with source parsing
- [x] 14-02: Create /api/external-operations API endpoint
- [x] 14-03: Verify PreconditionService integration with bridge-generated code
### Phase 15: 前端集成
**Goal**: 在前置条件编辑器中添加操作码选择器
**Depends on**: Phase 14 (后端桥接模块)
**Requirements**: FRONT-01, FRONT-02, FRONT-03, FRONT-04
**Success Criteria** (what must be TRUE):
  1. 前置条件编辑器中添加操作码选择器组件
  2. 操作码按模块分组显示 (配件、财务、运营、平台等)
  3. 支持多选操作码
  4. 选中操作码后自动生成 Python 代码模板
**Plans**: 3 plans
Plans:
- [x] 15-01: Add external operation types and API module
- [x] 15-02: Create OperationCodeSelector modal component
- [x] 15-03: Integrate selector into TaskForm with error handling
### Phase 16: 端到端验证
**Goal**: 完整流程测试：选择操作码 → 执行前置条件 → 查看结果
**Depends on**: Phase 15 (前端集成)
**Requirements**: VAL-01, VAL-02
**Success Criteria** (what must be TRUE):
  1. 完整流程测试：选择操作码 → 执行前置条件 → 查看结果
  2. 错误处理：外部项目缺失、配置错误、执行失败
**Plans**: ? plans
## Progress
**Execution Order:**
Phases execute in numeric order: 13 → 14 → 15 → 16
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
| 10. 销售出库用例调通 | v0.2.1 | 2/4 | Blocked | - |
| 11. Bug 修复 | v0.2.1 | 0/2 | Deferred | - |
| 12. 文档指南 | v0.2.1 | 0/2 | Deferred | - |
| 13. 配置基础 | v0.3 | 3/3 | Complete | 2026-03-17 |
| 14. 后端桥接模块 | v0.3 | 3/3 | Complete | 2026-03-18 |
| 15. 前端集成 | v0.3 | 3/3 | Complete | 2026-03-18 |
| 16. 端到端验证 | v0.3 | 0/? | Not started | - |
---
*Roadmap created: 2026-03-14*
*Last updated: 2026-03-18 - Phase 15 complete*
