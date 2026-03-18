# Milestones

## v0.3 前置条件集成 (Shipped: 2026-03-18)

**Phases completed:** 6 phases, 18 plans, 6 tasks

**Key accomplishments:**
- (none recorded)

---

## v0.3 前置条件集成 (Shipped: 2026-03-18)

**Phases completed:** 6 phases, 18 plans, 6 tasks

**Key accomplishments:**
- (none recorded)

---

## v0.3.1 - 前置条件数据传递（待规划）

**目标**: 扩展前置条件系统，支持从 FA1/HC1 等操作获取返回数据（如 IMEI）并传递给后续步骤。

**需求**:
- [ ] 执行 FA1/HC1 后获取返回数据
- [ ] 自动提取关键字段（如 IMEI）存入 context
- [ ] 在后续步骤中使用 `{{imei}}` 引用
- [ ] 支持调用 webseleniumerp 的 `inventory_list_data()` 等数据获取方法

**用例**:
```
前置条件: FA1（新增采购入库） → 获取 IMEI
步骤: 输入 {{imei}} 到表单
```

---

## v0.3 前置条件集成 (Shipped: 2026-03-18)

**Phases completed:** 4 phases (Phase 13-16), 12 plans

**Key accomplishments:**
1. 配置基础 - WEBSERP_PATH 环境变量, 启动验证, 文档模板
2. 后端桥接模块 - ExternalPreconditionBridge, 操作码 API, PreconditionService 集成
3. 前端集成 - OperationCodeSelector 组件, 模块分组显示, 代码生成
4. 端到端验证 - E2E 测试, 错误场景测试, 手动测试检查清单

---

## v0.2.1 测试用例调通 (Shipped: 2026-03-18)

**Phases completed:** 2 phases (Phase 9-10), 6 plans

**Key accomplishments:**
1. 登录用例调通 - 端到端执行成功，报告正确展示
2. 销售出库用例 - 前置条件配置、动态数据生成、API 断言验证通过

**Note:** Phase 11-12 (Bug 修复、文档指南) 推迟到后续版本

---

## v0.2 前置条件、接口断言、动态数据 (Shipped: 2026-03-17)

**Phases completed:** 4 phases (Phase 5-8), 15 plans

**Key accomplishments:**
1. 前置条件系统 - 支持 Python 代码格式，Jinja2 变量替换，SSE 实时监控
2. 接口断言集成 - ApiAssertionService 支持时间和数据断言，断言结果独立展示
3. 动态数据支持 - 随机数生成器、时间计算、跨步骤数据缓存
4. 前端实时监控完善 - SSE 事件处理器、报告数据完整性修复

**Tech Debt:**
- Nyquist Wave 0 tasks pending (tests defined but not run)
- Pre-existing TypeScript errors in ApiAssertionResults.tsx, RunList.tsx (not blocking)

---

## v0.1 MVP (Shipped: 2026-03-14)

**Phases completed:** 4 phases (Phase 1-4), 22 plans

**Key accomplishments:**
- Foundation fixes, data layer enhancement, service layer restoration, frontend + E2E alignment
