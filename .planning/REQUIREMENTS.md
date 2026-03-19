# Requirements: aiDriveUITest v0.3.2

**Defined:** 2026-03-19
**Core Value:** 验证 v0.3.1 数据获取方法集成的端到端可行性，发现并修复潜在 bug

## v1 Requirements (v0.3.2)

测试与Bug修复需求，确保 v0.3.1 数据获取方法集成功能稳定可用。

### 端到端测试

- [ ] **E2E-01**: 用户可以通过 DataMethodSelector 选择数据获取方法
- [x] **E2E-02**: 数据获取方法执行后返回预期数据
- [ ] **E2E-03**: 变量名可在测试步骤中正确引用（`{{变量名}}` 替换）
- [ ] **E2E-04**: 完整测试用例执行流程（前置条件 → 数据获取 → 变量替换 → AI 执行）

### 单元测试

- [ ] **UNIT-01**: ContextWrapper.get_data() 单元测试覆盖
- [ ] **UNIT-02**: 数据获取 API 端点单元测试覆盖
- [ ] **UNIT-03**: 变量替换逻辑单元测试覆盖

### Bug 修复

- [ ] **BUG-01**: 发现的阻断性 bug 全部修复
- [ ] **BUG-02**: 发现的功能性 bug 全部修复
- [ ] **BUG-03**: Bug 修复后回归测试通过

### 手动验证

- [ ] **MANUAL-01**: DataMethodSelector UI 功能手动验证
- [ ] **MANUAL-02**: 真实 ERP 环境下端到端流程验证
- [ ] **MANUAL-03**: 测试报告正确展示数据获取结果

## v2 Requirements (Future)

推迟到后续版本的需求。

(none)

## Out of Scope

明确排除的功能和原因。

| Feature | Reason |
|---------|--------|
| 性能优化 | 本次专注功能正确性 |
| 新功能开发 | 先验证现有功能 |
| 低优先级 UI 问题 | 不影响核心流程 |

## Traceability

需求到阶段的映射。在 roadmap 创建时更新。

| Requirement | Phase | Status |
|-------------|-------|--------|
| E2E-01 | Phase 20 | Pending |
| E2E-02 | Phase 20 | Complete |
| E2E-03 | Phase 20 | Pending |
| E2E-04 | Phase 20 | Pending |
| UNIT-01 | Phase 21 | Pending |
| UNIT-02 | Phase 21 | Pending |
| UNIT-03 | Phase 21 | Pending |
| BUG-01 | Phase 22 | Pending |
| BUG-02 | Phase 22 | Pending |
| BUG-03 | Phase 22 | Pending |
| MANUAL-01 | Phase 20 | Pending |
| MANUAL-02 | Phase 20 | Pending |
| MANUAL-03 | Phase 20 | Pending |

**Coverage:**
- v1 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-19*
*Last updated: 2026-03-19 after initial definition*
