# Roadmap: aiDriveUITest

## Milestones

- [x] **v0.1 MVP** - Phases 1-4 (shipped 2026-03-14)
- [x] **v0.2 前置条件、接口断言、动态数据** - Phases 5-8 (shipped 2026-03-17)
- [x] **v0.2.1 测试用例调通** - Phases 9-10 (shipped 2026-03-18, Phases 11-12 deferred)
- [x] **v0.3 前置条件集成** - Phases 13-16 (shipped 2026-03-18)
- [x] **v0.3.1 数据获取方法集成** - Phases 17-19 (shipped 2026-03-19)
- [ ] **v0.3.2 测试与Bug修复** - Phases 20-22 (in progress)

## Phases

<details>
<summary>v0.1 MVP (Phases 1-4) - SHIPPED 2026-03-14</summary>
- [x] Phase 1: Foundation Fixes (6/6 plans)
- [x] Phase 2: Data Layer Enhancement (4/4 plans)
- [x] Phase 3: Service Layer Restoration (6/6 plans)
- [x] Phase 4: Frontend + E2E Alignment (6/4 plans)
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

<details>
<summary>v0.3.1 数据获取方法集成 (Phases 17-19) - SHIPPED 2026-03-19</summary>
- [x] Phase 17: 后端数据获取桥接 (3/3 plans) - completed 2026-03-18
- [x] Phase 18: 前端数据选择器 (5/5 plans) - completed 2026-03-19
- [x] Phase 19: 集成与变量传递 (3/3 plans) - completed 2026-03-19
**Key accomplishments:**
1. 后端数据获取桥接 - 扫描 base_params.py，提供数据获取方法列表和执行 API
2. 前端数据选择器 - DataMethodSelector 4 步向导组件，支持参数配置和字段提取
3. 集成与变量传递 - context.get_data() 代码生成，API 断言变量替换
*Archived: .planning/milestones/v0.3.1-ROADMAP.md*
</details>

---

## v0.3.2 测试与Bug修复 (Phases 20-22)

**Milestone Goal:** 验证 v0.3.1 数据获取方法集成的端到端可行性，发现并修复潜在 bug

- [x] **Phase 20: E2E Testing + Manual Verification** - 端到端测试与手动验证 (completed 2026-03-19)
- [x] **Phase 21: Unit Test Coverage** - 单元测试覆盖 (completed 2026-03-19)
- [ ] **Phase 22: Bug Fix Sprint** - Bug 修复冲刺

---

## Phase Details

### Phase 20: E2E Testing + Manual Verification
**Goal:** 验证数据获取方法集成的端到端流程可用
**Depends on:** Phase 19 (v0.3.1 集成与变量传递完成)
**Requirements:** E2E-01, E2E-02, E2E-03, E2E-04, MANUAL-01, MANUAL-02, MANUAL-03
**Success Criteria** (what must be TRUE):
  1. 用户可通过 DataMethodSelector 选择并配置数据获取方法
  2. 执行数据获取方法后返回预期数据并显示在前端
  3. 测试步骤中的 `{{变量名}}` 被正确替换为实际值
  4. 完整测试用例（前置条件 -> 数据获取 -> 变量替换 -> AI 执行）端到端成功
  5. 真实 ERP 环境下完整流程手动验证通过
**Plans:** 6/6 plans complete

Plans:
- [x] 20-01: E2E 测试 - DataMethodSelector 选择与配置 (Wave 1) - completed 2026-03-19
- [x] 20-02: E2E 测试 - 数据获取执行与返回 (Wave 1) - completed 2026-03-19
- [ ] 20-03: E2E 测试 - 变量替换集成 (Wave 2)
- [ ] 20-04: E2E 测试 - 完整用例执行流程 (Wave 3)
- [ ] 20-05: 手动验证 - 创建检查清单 (Wave 4)
- [ ] 20-06: 手动验证 - 执行与确认 (Wave 5, checkpoint)

### Phase 21: Unit Test Coverage
**Goal:** 核心数据获取逻辑有充分的单元测试覆盖
**Depends on:** Phase 20
**Requirements:** UNIT-01, UNIT-02, UNIT-03
**Success Criteria** (what must be TRUE):
  1. ContextWrapper.get_data() 方法有完整单元测试（正常/异常路径）
  2. 数据获取 API 端点有完整单元测试（请求/响应/错误处理）
  3. 变量替换逻辑有完整单元测试（各种替换场景）
  4. 新增代码单元测试覆盖率达到 80%+
**Plans:** 3/3 plans complete

Plans:
- [x] 21-01: ContextWrapper.get_data() 与 execute_data_method_sync 单元测试 (Wave 1)
- [x] 21-02: 变量替换边界场景单元测试 (Wave 1)
- [x] 21-03: 数据获取 API 端点边界场景单元测试 (Wave 2)

### Phase 22: Bug Fix Sprint
**Goal:** 测试阶段发现的所有 bug 已修复并通过回归测试
**Depends on:** Phase 21
**Requirements:** BUG-01, BUG-02, BUG-03
**Success Criteria** (what must be TRUE):
  1. 所有阻断性 bug（阻塞核心流程）已修复 - 16 个失败测试 + 18 个归档文件
  2. 所有功能性 bug（影响用户体验）已修复 - 9 个 UI/交互 bug
  3. 修复后的代码通过回归测试，无新增失败用例
**Plans:** 6 plans

Plans:
- [ ] 22-01: 修复失败测试 - 测试隔离与 mock 签名更新 (Wave 1) - BUG-01
- [ ] 22-02: 归档遗留测试文件 - 移动 18 个导入已删除模块的测试 (Wave 1) - BUG-01
- [ ] 22-03: 修复 DataMethodSelector UI bug - 分组/计数/类型提示/校验/引号/Escape (Wave 2) - BUG-02
- [ ] 22-04: 修复代码生成 bug - 添加 import 语句 (Wave 2) - BUG-02
- [ ] 22-05: 修复报告页 bug - 添加前置条件执行信息 (Wave 3) - BUG-02
- [ ] 22-06: 回归测试验证 - 全量测试 + 手动验证 (Wave 4, checkpoint) - BUG-03

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
| 19. 集成与变量传递 | v0.3.1 | 3/3 | Complete | 2026-03-19 |
| 20. E2E Testing + Manual Verification | v0.3.2 | 6/6 | Complete | 2026-03-19 |
| 21. Unit Test Coverage | v0.3.2 | 3/3 | Complete | 2026-03-19 |
| 22. Bug Fix Sprint | v0.3.2 | 0/6 | Planning | - |

---
*Roadmap created: 2026-03-14*
*Last updated: 2026-03-19 - Phase 22 plans created*
