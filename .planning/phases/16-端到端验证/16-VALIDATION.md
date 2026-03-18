---
phase: 16
slug: 端到端验证
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 16 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.0.0+ with pytest-asyncio 0.24.0+ |
| **Config file** | pyproject.toml [tool.pytest.ini_options] |
| **Quick run command** | `uv run pytest backend/tests/integration/test_e2e_precondition_integration.py -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/integration/test_e2e_precondition_integration.py -v`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 16-01-01 | 01 | 1 | VAL-01 | integration | `uv run pytest backend/tests/integration/test_e2e_precondition_integration.py::TestCompleteFlow -v` | ❌ W0 | ⬜ pending |
| 16-02-01 | 02 | 1 | VAL-02 | integration | `uv run pytest backend/tests/integration/test_e2e_precondition_integration.py::TestErrorScenarios -v` | ❌ W0 | ⬜ pending |
| 16-03-01 | 03 | 1 | VAL-02 | manual | N/A | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/integration/test_e2e_precondition_integration.py` — stubs for VAL-01, VAL-02
- [ ] `docs/manual-test-checklist.md` — manual test steps for real webseleniumerp verification

*Existing infrastructure (conftest.py, pytest.ini_options) covers all automated test requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Real webseleniumerp integration | VAL-01 | Requires external project setup outside CI | Follow manual test checklist with real WEBSERP_PATH |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
