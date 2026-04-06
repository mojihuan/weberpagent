# Requirements: aiDriveUITest v0.8.2

**Defined:** 2026-04-06
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v0.8.2 Requirements

### Code Investigation

- [x] **DIFF-01**: 对比 v0.4.0 和当前版本的 browser-use 初始化代码（Agent 构造参数、Browser 配置）
- [x] **DIFF-02**: 对比 Playwright 配置差异（headless/headed 设置、浏览器启动参数）
- [ ] **DIFF-03**: 分析 browser-use 版本升级变化（v0.4.0 时的版本 vs 当前版本 API 差异）
- [ ] **DIFF-04**: 分析 agent_service.py 中 Agent/Browser 配置的完整演变历史

### Analysis Report

- [ ] **RPT-01**: 输出结构化分析报告，包含：差异列表、根因分析、与表格输入框定位问题的关联性评估

## Future Requirements

(None — this is an investigation-only milestone)

## Out of Scope

| Feature | Reason |
|---------|--------|
| 修复浏览器模式问题 | 只做分析，修复留给后续 milestone |
| 恢复 headed 模式 | 调查阶段不做代码修改 |
| E2E 验证 | 调查性质，无需测试验证 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DIFF-01 | Phase 63 | Complete |
| DIFF-02 | Phase 63 | Complete |
| DIFF-03 | Phase 63 | Pending |
| DIFF-04 | Phase 63 | Pending |
| RPT-01 | Phase 64 | Pending |

**Coverage:**
- v0.8.2 requirements: 5 total
- Mapped to phases: 5
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-06*
*Last updated: 2026-04-06 after roadmap creation*
