---
phase: 14
slug: 后端桥接模块
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-17
---

# Phase 14 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | `backend/pyproject.toml` |
| **Quick run command** | `uv run pytest backend/tests/unit/test_external_bridge.py -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~5 seconds (unit) / ~30 seconds (full) |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_external_bridge.py -v`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 14-01-01 | 01 | 1 | BRIDGE-01 | unit | `uv run pytest backend/tests/unit/test_external_bridge.py::test_bridge_module_exists -v` | TDD-inline | pending |
| 14-01-02 | 01 | 1 | BRIDGE-01 | unit | `uv run pytest backend/tests/unit/test_external_bridge.py::test_bridge_singleton -v` | TDD-inline | pending |
| 14-02-01 | 02 | 2 | BRIDGE-02 | unit | `uv run pytest backend/tests/unit/test_external_bridge.py::test_parse_operations -v` | TDD-inline | pending |
| 14-02-02 | 02 | 2 | BRIDGE-02 | unit | `uv run pytest backend/tests/unit/test_external_bridge.py::test_caching -v` | TDD-inline | pending |
| 14-03-01 | 03 | 3 | BRIDGE-03 | integration | `uv run pytest backend/tests/api/test_external_operations.py::test_list_operations -v` | TDD-inline | pending |
| 14-03-02 | 03 | 3 | BRIDGE-03 | integration | `uv run pytest backend/tests/api/test_external_operations.py::test_503_when_unavailable -v` | TDD-inline | pending |
| 14-04-01 | 04 | 3 | BRIDGE-04 | unit | `uv run pytest backend/tests/unit/test_external_bridge.py::test_generate_code -v` | TDD-inline | pending |
| 14-04-02 | 04 | 3 | BRIDGE-04 | integration | `uv run pytest backend/tests/unit/test_precondition_service.py::test_execute_external_ops -v` | TDD-inline | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

**Note:** This phase uses TDD-inline approach where tests are created alongside implementation in each task. Wave 0 test stubs are NOT required because:

1. Each task with `tdd="true"` creates tests first (RED), then implements (GREEN)
2. The `<behavior>` block in each task explicitly lists test cases
3. Executors follow TDD discipline without pre-existing test stubs

Wave 0 is marked complete because the TDD approach ensures tests exist before implementation in each wave.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| External project integration | BRIDGE-02 | Requires real webseleniumerp project | 1. Configure WEBSERP_PATH in .env 2. Start server 3. GET /api/external-operations 4. Verify operation list |
| Code generation correctness | BRIDGE-04 | Requires real execution context | 1. Select operations via API 2. Execute generated code 3. Verify context['precondition_result'] |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (TDD-inline approach)
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
