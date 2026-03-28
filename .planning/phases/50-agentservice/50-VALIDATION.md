---
phase: 50
slug: agentservice
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-28
---

# Phase 50 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` (tool.pytest section) |
| **Quick run command** | `uv run pytest backend/tests/test_agent_params.py backend/tests/test_agent_service.py -x -q` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/test_agent_params.py backend/tests/test_agent_service.py -x -q`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 50-01-01 | 01 | 1 | INTEG-01 | unit | `uv run pytest backend/tests/test_agent_service.py -x -q` | ✅ | ⬜ pending |
| 50-01-02 | 01 | 1 | INTEG-02 | unit | `uv run pytest backend/tests/test_agent_service.py::test_monitored_agent_detectors_initialized -x -q` | ✅ | ⬜ pending |
| 50-01-03 | 01 | 1 | INTEG-05 | unit | `uv run pytest backend/tests/test_agent_params.py -x -q` | ✅ | ⬜ pending |
| 50-02-01 | 02 | 2 | INTEG-03 | unit | `uv run pytest backend/tests/test_agent_service.py -x -q -k "step_callback"` | ✅ | ⬜ pending |
| 50-02-02 | 02 | 2 | INTEG-04 | unit | `uv run pytest backend/tests/test_agent_service.py -x -q -k "monitor_log"` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/test_agent_service.py` — update mock target from Agent to MonitoredAgent
- [ ] `backend/tests/test_agent_params.py` — update mock target from Agent to MonitoredAgent

*Existing infrastructure covers all phase requirements — no new test files needed.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| None | - | - | All phase behaviors have automated verification |

All phase behaviors have automated verification.

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
