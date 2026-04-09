---
phase: 72
slug: 批量执行引擎
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-08
---

# Phase 72 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest + pytest-asyncio |
| **Config file** | none — existing infrastructure |
| **Quick run command** | `uv run pytest backend/tests/unit/test_batch*.py -v -x` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_batch*.py -v -x`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 72-01-01 | 01 | 1 | BATCH-01 | integration | `uv run pytest backend/tests/unit/test_batch_api.py::test_create_batch -x` | ❌ W0 | ⬜ pending |
| 72-01-02 | 01 | 1 | BATCH-01 | integration | `uv run pytest backend/tests/unit/test_batch_api.py::test_get_batch_status -x` | ❌ W0 | ⬜ pending |
| 72-01-03 | 01 | 1 | BATCH-01 | integration | `uv run pytest backend/tests/unit/test_batch_api.py::test_get_batch_runs -x` | ❌ W0 | ⬜ pending |
| 72-02-01 | 02 | 1 | BATCH-02 | unit | `uv run pytest backend/tests/unit/test_batch_execution.py::test_semaphore_limits_concurrency -x` | ❌ W0 | ⬜ pending |
| 72-02-02 | 02 | 1 | BATCH-02 | unit | `uv run pytest backend/tests/unit/test_batch_execution.py::test_error_isolation -x` | ❌ W0 | ⬜ pending |
| 72-02-03 | 02 | 1 | BATCH-02 | unit | `uv run pytest backend/tests/unit/test_batch_execution.py::test_batch_status_transitions -x` | ❌ W0 | ⬜ pending |
| 72-02-04 | 02 | 1 | BATCH-02 | unit | `uv run pytest backend/tests/unit/test_batch_execution.py::test_concurrency_cap -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_batch_api.py` — stubs for BATCH-01 API endpoint tests
- [ ] `backend/tests/unit/test_batch_execution.py` — stubs for BATCH-02 service tests (Semaphore, error isolation)
- [ ] BatchRepository unit tests can share existing `db_session` fixture from conftest.py

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Batch confirmation dialog renders concurrency slider | BATCH-01 | UI rendering requires visual inspection | Open Tasks page, select tasks, click "批量执行", verify slider appears with 1-4 range, default 2 |
| Multiple browser instances run in parallel | BATCH-02 | Requires real browser automation | Select 3+ tasks, set concurrency=2, start batch, verify only 2 browsers open simultaneously |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
