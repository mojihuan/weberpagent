# Roadmap: aiDriveUITest v0.2

## Overview

v0.2 聚焦于让产品真正可用于生产环境。通过集成前置条件系统、接口断言和动态数据支持，让 QA 能够用自然语言完成完整的测试流程。

## Phases

**Phase Numbering:**
- Phase 1-4: v0.1 已完成
- Phase 5-7: v0.2 新增

---

### Phase 5: 前置条件系统
**Goal**: 支持 API 方式执行前置条件，快速造数据
**Depends on**: Phase 4 (v0.1)
**Requirements**: PRE-01, PRE-02, PRE-03, PRE-04
**Success Criteria** (what must be TRUE):
  1. 用户可以在测试用例描述中定义前置条件步骤
  2. 前置条件通过 API 调用执行，不启动浏览器
  3. 支持调用现有项目的 API 封装方法
  4. 前置条件执行结果可以传递给后续测试步骤
**Plans**: 4 plans in 2 waves

Plans:
- [x] 05-01-PLAN.md - 前置条件语法设计（自然语言识别）
- [x] 05-02-PLAN.md - API 调用框架集成
- [x] 05-03-PLAN.md - 现有项目方法复用机制
- [x] 05-04-PLAN.md - 前置条件结果传递

### Phase 6: 接口断言集成
**Goal**: 支持通过 API 调用验证测试结果
**Depends on**: Phase 5
**Requirements**: API-01, API-02, API-03, API-04
**Success Criteria** (what must be TRUE):
  1. 用户可以在测试用例中定义 API 断言
  2. 时间断言支持 ±1 分钟范围验证
  3. 数据断言支持精确匹配和包含匹配
  4. 断言结果展示在测试报告中
**Plans**: 4 plans in 2 waves

Plans:
- [x] 06-01-PLAN.md - 断言语法设计（自然语言识别）
- [ ] 06-02-PLAN.md - BaseAssert 类移植
- [ ] 06-03-PLAN.md - 时间断言实现
- [ ] 06-04-PLAN.md - 断言结果报告集成

### Phase 7: 动态数据支持
**Goal**: 支持随机数生成、动态数据获取和数据缓存
**Depends on**: Phase 6
**Requirements**: DYN-01, DYN-02, DYN-03, DYN-04
**Success Criteria** (what must be TRUE):
  1. 支持生成 SF 物流单号、手机号等随机数据
  2. 支持从 API 接口获取数据并用于测试
  3. 支持跨步骤缓存数据供后续复用
  4. 支持时间计算（now ± N 分钟）
**Plans**: 4 plans in 2 waves

Plans:
- [ ] 07-01-PLAN.md - 随机数生成器移植（BaseRandomMixin 简化版）
- [ ] 07-02-PLAN.md - 时间计算工具
- [ ] 07-03-PLAN.md - PreconditionService 集成
- [ ] 07-04-PLAN.md - 端到端验证

---

## Progress

**Execution Order:**
Phases execute in numeric order: 5 -> 6 -> 7

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 5. 前置条件系统 | 4/4 | Complete | 2026-03-16 |
| 6. 接口断言集成 | 1/4 | In Progress | 06-01 |
| 7. 动态数据支持 | 0/4 | Planned | — |

---
*Roadmap created: 2026-03-16*
*Last updated: 2026-03-17 - Phase 7 plans created*
