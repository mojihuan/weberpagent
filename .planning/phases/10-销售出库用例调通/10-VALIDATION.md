---
phase: 10
slug: 销售出库用例调通
status: ready
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-17
---

# Phase 10 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `backend/pyproject.toml` |
| **Quick run command** | `uv run pytest backend/tests/unit/ -v -x` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/ -v -x`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 10-01-01 | 01 | 1 | SALE-01 | manual | E2E: 前端创建任务 | N/A | ⬜ pending |
| 10-01-02 | 01 | 1 | SALE-06 | manual | E2E: 前置条件执行和变量传递 | N/A | ⬜ pending |
| 10-02-01 | 02 | 1 | SALE-03 | manual | E2E: 随机数生成器验证 | N/A | ⬜ pending |
| 10-02-02 | 02 | 1 | SALE-02 | manual | E2E: Jinja2 变量替换验证 | N/A | ⬜ pending |
| 10-03-01 | 03 | 1 | SALE-04 | manual | E2E: API 断言配置 | N/A | ⬜ pending |
| 10-03-02 | 03 | 1 | SALE-07 | manual | E2E: API 断言结果展示 | N/A | ⬜ pending |
| 10-04-01 | 04 | 2 | SALE-05 | manual | E2E: 完整用例执行 | N/A | ⬜ pending |
| 10-04-02 | 04 | 2 | SALE-05 | manual | E2E: 报告完整性验证 | N/A | ⬜ pending |
| 10-04-03 | 04 | 2 | BUGS | manual | E2E: Bug 记录 | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `backend/tests/unit/test_precondition_service.py` — 单元测试已存在
- [x] `backend/tests/unit/test_api_assertion_service.py` — 单元测试已存在
- [x] `backend/tests/integration/` — 集成测试基础设施已存在

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

This phase is primarily manual E2E verification because it requires:
1. **Live ERP environment** — Cannot be mocked realistically
2. **External ERP API module** — User-specific implementation
3. **AI-driven browser automation** — Non-deterministic by nature

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 前端任务创建 | SALE-01 | 需要 ERP 环境 | 打开前端 → 新建任务 → 填写销售出库信息 |
| 前置条件执行 | SALE-06 | 需要 ERP API | 配置 `context['order_no'] = sf_waybill()` → 执行 → 验证变量传递 |
| 动态数据替换 | SALE-02, SALE-03 | 需要 Jinja2 | 步骤使用 `{{order_no}}` → 执行 → 验证替换结果 |
| API 断言执行 | SALE-04 | 需要 ERP API | 配置断言 → 执行 → 验证结果展示 |
| 端到端执行 | SALE-05, SALE-07 | 需要完整环境 | 完整执行销售出库用例 → 验证所有步骤和断言 |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: Wave 0 unit tests provide baseline coverage
- [x] Wave 0 covers all MISSING references (no MISSING references)
- [x] No watch-mode flags
- [x] Feedback latency < 30s (unit tests)
- [x] `nyquist_compliant: true` set in frontmatter
- [x] Manual E2E tasks properly documented with acceptance_criteria

**Approval:** ready for execution

---

## Notes

This phase validates the v0.2 features (preconditions, dynamic data, API assertions) work together in a realistic sales outbound test scenario. All tasks are manual checkpoints because:

1. The execution requires a live ERP system with real data
2. The AI-driven browser automation is non-deterministic
3. The external ERP API module is user-specific

Unit tests in `backend/tests/unit/` provide baseline coverage for the underlying services (PreconditionService, ApiAssertionService, random_generators).
