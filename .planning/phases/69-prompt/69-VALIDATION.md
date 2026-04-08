---
phase: 69
slug: prompt
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-07
---

# Phase 69 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest backend/tests/ -k "phase69 or failure_tracker or prompt_rule" -x -q` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/ -k "phase69 or failure_tracker or prompt_rule" -x -q`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 69-01-01 | 01 | 1 | ANTI-03 | unit | `uv run pytest backend/tests/ -k "test_step_callback_failure_tracker" -x` | ✅ | ⬜ pending |
| 69-01-02 | 01 | 1 | RECOV-02 | unit | `uv run pytest backend/tests/ -k "test_step_callback_detect_failure" -x` | ✅ | ⬜ pending |
| 69-01-03 | 01 | 1 | RECOV-03 | unit | `uv run pytest backend/tests/ -k "test_step_callback_state_reset" -x` | ✅ | ⬜ pending |
| 69-02-01 | 02 | 1 | PROMPT-01 | unit | `uv run pytest backend/tests/ -k "test_prompt_line_marker_rule" -x` | ✅ | ⬜ pending |
| 69-02-02 | 02 | 1 | PROMPT-02 | unit | `uv run pytest backend/tests/ -k "test_prompt_anti_repeat_rule" -x` | ✅ | ⬜ pending |
| 69-02-03 | 02 | 1 | PROMPT-03 | unit | `uv run pytest backend/tests/ -k "test_prompt_strategy_priority_rule" -x` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/test_step_callback_phase69.py` — stubs for ANTI-03, RECOV-02, RECOV-03
- [ ] `backend/tests/test_prompt_rules_phase69.py` — stubs for PROMPT-01, PROMPT-02, PROMPT-03

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Agent reads Section 9 rules and follows them during execution | PROMPT-01/02/03 | Requires live browser + LLM interaction | Run E2E test case with known failure scenario, verify agent switches strategy instead of repeating |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
