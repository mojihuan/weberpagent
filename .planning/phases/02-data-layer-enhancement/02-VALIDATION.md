---
phase: 02
slug: data-layer-enhancement
status: ready
nyquist_compliant: true
wave_0_complete: false
created: 2026-03-14
---

# Phase 02 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.0+ with pytest-asyncio 0.24+ |
| **Config file** | pyproject.toml (tool.pytest.ini_options) |
| **Quick run command** | `uv run pytest backend/tests/unit/ -v -x` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/ -v -x`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 02-00-T1 | 00 | 0 | DATA-01,02,03 | unit | `uv run pytest backend/tests/unit/test_models.py --collect-only -q` | ❌ W0 | ⬜ pending |
| 02-00-T2 | 00 | 0 | DATA-05 | unit | `uv run pytest backend/tests/unit/test_repository.py --collect-only -q` | ❌ W0 | ⬜ pending |
| 02-00-T3 | 00 | 0 | fixtures | unit | `uv run python -c "from backend.tests.conftest import *"` | ❌ W0 | ⬜ pending |
| 02-01-T1 | 01 | 1 | DATA-01 | unit | `uv run pytest backend/tests/unit/test_models.py::test_assertion_model -v` | ❌ W0 | ⬜ pending |
| 02-01-T2 | 01 | 1 | DATA-02 | unit | `uv run pytest backend/tests/unit/test_models.py::test_assertion_result_model -v` | ❌ W0 | ⬜ pending |
| 02-01-T3 | 01 | 1 | DATA-03 | unit | `uv run pytest backend/tests/unit/test_models.py::test_assertion_relationships -v` | ❌ W0 | ⬜ pending |
| 02-02-T1 | 02 | 1 | DATA-05 | unit | `uv run pytest backend/tests/unit/test_repository.py::test_run_repository_get_steps -v` | ❌ W0 | ⬜ pending |
| 02-03-T1 | 03 | 2 | DATA-01,02 | unit | `uv run python -c "from backend.db.schemas import AssertionResponse, AssertionResultResponse"` | ✅ | ⬜ pending |
| 02-03-T2 | 03 | 2 | DATA-04 | integration | `uv run pytest backend/tests/integration/test_screenshot_storage.py -v` | ✅ verify | ⬜ pending |
| 02-03-T3 | 03 | 2 | all | unit | `uv run pytest backend/tests/unit/ backend/tests/integration/ -v --tb=short` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_models.py` — test stubs for DATA-01, DATA-02, DATA-03
- [ ] `backend/tests/unit/test_repository.py` — test stub for DATA-05
- [ ] `backend/tests/conftest.py` — fixtures for assertion test data

*DATA-04: Existing infrastructure covers requirement — screenshot storage already implemented.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| None | — | — | — |

*All phase behaviors have automated verification.*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 15s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** 2026-03-14
