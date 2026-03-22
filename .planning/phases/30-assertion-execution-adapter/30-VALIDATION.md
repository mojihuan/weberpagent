---
phase: 30
slug: assertion-execution-adapter
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-22
---

# Phase 30 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_external_assertion_bridge.py -v`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 30-01-01 | 01 | 1 | EXEC-01 | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::TestExecuteAssertionMethod::test_three_layer_params -v` | ❌ W0 | ⬜ pending |
| 30-01-02 | 01 | 1 | EXEC-02 | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::TestConvertNowValues -v` | ❌ W0 | ⬜ pending |
| 30-02-01 | 02 | 1 | EXEC-03 | unit | `uv run pytest backend/tests/core/test_external_precondition_bridge_assertion.py::TestParseAssertionError::test_returns_name_not_field -v` | ✅ | ⬜ pending |
| 30-03-01 | 03 | 1 | EXEC-04 | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::TestBackwardCompatibility -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `backend/tests/unit/test_external_assertion_bridge.py` — 新增 TestConvertNowValues 测试类
- [x] `backend/tests/unit/test_external_assertion_bridge.py` — 扩展 TestExecuteAssertionMethod 三层参数测试
- [x] `backend/tests/unit/test_external_assertion_bridge.py` — 新增 TestBackwardCompatibility 测试类
- [x] `backend/tests/core/test_external_precondition_bridge_assertion.py` — 修改 TestParseAssertionError 验证 name 字段

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| None | - | - | All phase behaviors have automated verification. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
