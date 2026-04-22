# Requirements: v0.10.2 测试验证与代码可用性修复

## Active

### 过时测试清理 (CLEAN) — 执行优先

- [x] **CLEAN-01**: 识别并删除不再需要的测试文件 — 无法修复或与当前架构不符的过时测试（先清理再修复，避免修复了后面会被删除的测试）
- [x] **CLEAN-02**: 清理测试隔离问题 — 修复跨测试状态泄漏、共享 fixture 问题

### 测试代码修复 (TEST)

- [x] **TEST-01**: 修复 Import Error 测试 — 引用已删除/重构模块的测试文件更新或删除
- [x] **TEST-02**: 修复外部断言桥接测试 — mock 目标路径与当前代码对齐 (test_external_assertion_bridge.py)
- [x] **TEST-03**: 修复 auth_service 测试 — 重构后测试 mock 路径更新 (test_auth_service.py)
- [x] **TEST-04**: 修复 precondition_service 测试 — mock 目标与当前 execute_data_method_sync 路径一致 (test_precondition_service.py)
- [x] **TEST-05**: 修复其他零散失败测试 — agent_service, self_healing_runner, llm_healer, browser_cleanup, repository 等

### DataMethodError 修复 (DATA)

- [x] **DATA-01**: 诊断 PcImport 混淆方法名失效根因 — webseleniumerp 上游更新后方法名变化导致前置条件执行失败
- [x] **DATA-02**: 实现方法名自动发现或动态映射 — 避免硬编码混淆方法名，降低上游更新影响

### 端到端可用性验证 (E2E)

- [x] **E2E-01**: 验证自然语言→AI 执行→报告全链路可用 — 在服务器上执行完整测试流程
- [x] **E2E-02**: 验证前置条件系统正常工作 — context.get_data() 调用链路修复后可用
- [x] **E2E-03**: 验证断言系统正常工作 — 业务断言执行链路完整

## Future Requirements (Deferred)

- PreSubmitGuard DOM 值提取 — actual_values=None，需实现 DOM 值读取
- 性能优化 — 测试运行速度、并发稳定性

## Out of Scope

- 新功能开发 — 本里程碑只做验证和修复
- 架构重构 — 不改变现有模块结构
- webseleniumerp 混淆策略修改 — 上游项目决定混淆方式，不在本项目中改变

## Traceability

| REQ-ID | Phase | Status |
|--------|-------|--------|
| CLEAN-01 | Phase 90 | Complete |
| CLEAN-02 | Phase 90 | Complete |
| TEST-01 | Phase 91 | Complete |
| TEST-02 | Phase 91 | Complete |
| TEST-03 | Phase 91 | Complete |
| TEST-04 | Phase 91 | Complete |
| TEST-05 | Phase 91 | Complete |
| DATA-01 | Phase 92 | Complete |
| DATA-02 | Phase 92 | Complete |
| E2E-01 | Phase 93 | Complete |
| E2E-02 | Phase 93 | Complete |
| E2E-03 | Phase 93 | Complete |

---
*Requirements defined: 2026-04-21 — v0.10.2 milestone*
