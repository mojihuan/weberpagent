---
phase: 6
slug: 06-接口断言集成
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-16
---

# Phase 6 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | `backend/pyproject.toml` |
| **Quick run command** | `uv run pytest backend/tests/test_api_assertion_service.py -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v --tb=short` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/test_api_assertion_service.py -v`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v --tb=short`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 06-01-01 | 01 | 1 | API-01 | unit | `uv run pytest backend/tests/test_api_assertion_service.py::test_parse_assertion_code -v` | ❌ W0 | ⬜ pending |
| 06-01-02 | 01 | 1 | API-01 | unit | `uv run pytest backend/tests/test_api_assertion_service.py::test_variable_substitution -v` | ❌ W0 | ⬜ pending |
| 06-02-01 | 02 | 1 | API-02 | unit | `uv run pytest backend/tests/test_api_assertion_service.py::test_time_assertion_within_range -v` | ❌ W0 | ⬜ pending |
| 06-02-02 | 02 | 1 | API-02 | unit | `uv run pytest backend/tests/test_api_assertion_service.py::test_time_assertion_outside_range -v` | ❌ W0 | ⬜ pending |
| 06-03-01 | 03 | 1 | API-03 | unit | `uv run pytest backend/tests/test_api_assertion_service.py::test_exact_match -v` | ❌ W0 | ⬜ pending |
| 06-03-02 | 03 | 1 | API-03 | unit | `uv run pytest backend/tests/test_api_assertion_service.py::test_contains_match -v` | ❌ W0 | ⬜ pending |
| 06-03-03 | 03 | 1 | API-03 | unit | `uv run pytest backend/tests/test_api_assertion_service.py::test_decimal_approx -v` | ❌ W0 | ⬜ pending |
| 06-04-01 | 04 | 2 | API-04 | integration | `uv run pytest backend/tests/test_api_assertion_service.py::test_report_includes_assertion_results -v` | ❌ W0 | ⬜ pending |
| 06-04-02 | 04 | 2 | API-04 | e2e | `cd frontend && npm test -- --testPathPattern=ApiAssertionResults` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/test_api_assertion_service.py` — stubs for API-01, API-02, API-03, API-04
- [ ] `backend/tests/fixtures/api_assertion_fixtures.py` — shared test fixtures
- [ ] `frontend/src/components/ApiAssertionResults.test.tsx` — frontend component tests

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 接口断言代码高亮显示 | API-01 | Monaco Editor 集成验证 | 在任务编辑页查看接口断言输入区域是否正确高亮 |
| 断言结果在报告中展示 | API-04 | UI 视觉验证 | 运行测试后查看报告页面是否正确显示断言结果 |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
