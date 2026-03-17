# Requirements: aiDriveUITest v0.2.1

**Defined:** 2026-03-17
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v0.2.1 Requirements

本里程碑目标是调通核心测试用例的端到端执行。

### 登录用例

- [ ] **LOGN-01**: 用户可以在前端创建登录测试任务（4 步骤）
- [ ] **LOGN-02**: 登录用例可以端到端执行成功
- [ ] **LOGN-03**: 执行结果在报告中正确展示

### 销售出库用例

- [ ] **SALE-01**: 用户可以在前端配置前置条件 `self.pre.operations(data=['FA1', 'HC1'])`
- [x] **SALE-02**: 用户可以在步骤中使用动态数据方法 `self.copy()` 和 `self.affix()`
- [x] **SALE-03**: 用户可以在步骤中使用随机数方法 `self.sf`
- [ ] **SALE-04**: 用户可以配置 API 断言验证销售单号、状态、时间
- [ ] **SALE-05**: 销售出库用例可以端到端执行成功
- [ ] **SALE-06**: 前置条件执行结果正确传递到测试步骤
- [ ] **SALE-07**: API 断言结果在报告中正确展示

### Bug 修复

- [ ] **BUGS-01**: 调通过程中发现的执行引擎 Bug 已修复
- [ ] **BUGS-02**: 调通过程中发现的前端 Bug 已修复

### 文档指南

- [ ] **DOCS-01**: 提供登录用例的前端填写指南
- [ ] **DOCS-02**: 提供销售出库用例的前端填写指南（含前置条件、动态数据、断言配置）

## v0.3 Requirements (Deferred)

推迟到后续版本：

### 批量执行

- **BATCH-01**: Excel 导入测试用例
- **BATCH-02**: 批量运行测试用例
- **BATCH-03**: 批量执行结果汇总

## Out of Scope

| Feature | Reason |
|---------|--------|
| 用户认证/权限管理 | 单用户本地使用 |
| 服务器部署 | 只需本地开发环境运行 |
| 多语言支持 | 只支持中文 |
| 批量执行 | 推迟到 v0.3 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| LOGN-01 | Phase 9 | Pending |
| LOGN-02 | Phase 9 | Pending |
| LOGN-03 | Phase 9 | Pending |
| SALE-01 | Phase 10 | Pending |
| SALE-02 | Phase 10 | Complete |
| SALE-03 | Phase 10 | Complete |
| SALE-04 | Phase 10 | Pending |
| SALE-05 | Phase 10 | Pending |
| SALE-06 | Phase 10 | Pending |
| SALE-07 | Phase 10 | Pending |
| BUGS-01 | Phase 11 | Pending |
| BUGS-02 | Phase 11 | Pending |
| DOCS-01 | Phase 12 | Pending |
| DOCS-02 | Phase 12 | Pending |

**Coverage:**
- v0.2.1 requirements: 14 total
- Mapped to phases: 14
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-17*
*Last updated: 2026-03-17 after roadmap creation*
