---
phase: 48
slug: agent
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-27
---

# Phase 48 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | backend/tests/conftest.py |
| **Quick run command** | `uv run pytest backend/tests/unit/test_monitored_agent.py -x` |
| **Full suite command** | `uv run pytest backend/tests/unit/ -v` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_monitored_agent.py -x`
- **After every plan wave:** Run `uv run pytest backend/tests/unit/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 48-01-01 | 01 | 1 | MON-01 | unit | `uv run pytest backend/tests/unit/test_stall_detector.py::test_consecutive_failures -x` | Wave 0 | pending |
| 48-01-02 | 01 | 1 | MON-02 | unit | `uv run pytest backend/tests/unit/test_stall_detector.py::test_stagnant_dom -x` | Wave 0 | pending |
| 48-01-03 | 01 | 1 | MON-03 | unit | `uv run pytest backend/tests/unit/test_stall_detector.py::test_reset_on_success -x` | Wave 0 | pending |
| 48-02-01 | 02 | 1 | MON-04 | unit | `uv run pytest backend/tests/unit/test_pre_submit_guard.py::test_extract_values -x` | Wave 0 | pending |
| 48-02-02 | 02 | 1 | MON-05 | unit | `uv run pytest backend/tests/unit/test_pre_submit_guard.py::test_blocks_mismatch -x` | Wave 0 | pending |
| 48-02-03 | 02 | 1 | MON-06 | unit | `uv run pytest backend/tests/unit/test_pre_submit_guard.py::test_skips_no_expectations -x` | Wave 0 | pending |
| 48-03-01 | 03 | 1 | MON-07 | unit | `uv run pytest backend/tests/unit/test_task_progress_tracker.py::test_parse_steps -x` | Wave 0 | pending |
| 48-03-02 | 03 | 1 | MON-08 | unit | `uv run pytest backend/tests/unit/test_task_progress_tracker.py::test_urgent_warning -x` | Wave 0 | pending |
| 48-04-01 | 04 | 2 | SUB-01 | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_prepare_context_injects -x` | Wave 0 | pending |
| 48-04-02 | 04 | 2 | SUB-02 | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_step_callback_stores -x` | Wave 0 | pending |
| 48-04-03 | 04 | 2 | SUB-03 | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_execute_actions_blocks -x` | Wave 0 | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_stall_detector.py` — stubs for MON-01, MON-02, MON-03
- [ ] `backend/tests/unit/test_pre_submit_guard.py` — stubs for MON-04, MON-05, MON-06
- [ ] `backend/tests/unit/test_task_progress_tracker.py` — stubs for MON-07, MON-08
- [ ] `backend/tests/unit/test_monitored_agent.py` — stubs for SUB-01, SUB-02, SUB-03

*Existing pytest infrastructure already installed via uv.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| None | — | — | — |

*All phase behaviors have automated verification.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
