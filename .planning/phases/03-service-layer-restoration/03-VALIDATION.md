---
phase: "03"
slug: service-layer-restoration
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-14
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.0.0+ with pytest-asyncio 0.24.0+ |
| **Config file** | pyproject.toml (asyncio_mode = "auto") |
| **Quick run command** | `uv run pytest backend/tests/unit/ -x` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/ -x`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | SVC-01 | unit | `uv run pytest backend/tests/unit/test_assertion_service.py -x` | ❌ W0 | ⬜ pending |
| 03-01-02 | 01 | 1 | SVC-01 | unit | `uv run pytest backend/tests/unit/test_assertion_result_repo.py -x` | ❌ W0 | ⬜ pending |
| 03-02-01 | 02 | 1 | SVC-02 | unit | `uv run pytest backend/tests/unit/test_report_service.py -x` | ❌ W0 | ⬜ pending |
| 03-03-01 | 03 | 1 | SVC-03 | unit | `uv run pytest backend/tests/unit/test_agent_service.py::test_llm_temperature -x` | ✅ partial | ⬜ pending |
| 03-04-01 | 04 | 1 | SVC-04 | unit | `uv run pytest backend/tests/unit/test_event_manager.py::test_heartbeat -x` | ❌ W0 | ⬜ pending |
| 03-05-01 | 05 | 2 | SVC-05 | integration | `uv run pytest backend/tests/integration/test_runs_background.py -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_assertion_service.py` — stubs for SVC-01 (AssertionService with ORM)
- [ ] `backend/tests/unit/test_assertion_result_repo.py` — stubs for AssertionResultRepository
- [ ] `backend/tests/unit/test_report_service.py` — stubs for SVC-02 (ReportService)
- [ ] `backend/tests/unit/test_event_manager.py::test_heartbeat` — stubs for SVC-04 (heartbeat)
- [ ] `backend/tests/unit/test_llm_retry.py` — stubs for LLM retry logic
- [ ] `backend/tests/integration/test_runs_background.py` — stubs for SVC-05 (background task status)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| SSE heartbeat visible in browser DevTools | SVC-04 | Requires browser client to observe network traffic | 1. Open browser DevTools Network tab 2. Filter for EventSource 3. Verify `:heartbeat` comments appear every 20s |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
