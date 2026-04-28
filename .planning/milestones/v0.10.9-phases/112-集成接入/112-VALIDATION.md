---
phase: 112
slug: 112-集成接入
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-28
---

# Phase 112 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest >=8.0.0 + pytest-asyncio >=0.24.0 |
| **Config file** | pyproject.toml [tool.pytest.ini_options], asyncio_mode = "auto" |
| **Quick run command** | `uv run pytest backend/tests/unit/test_step_code_buffer.py backend/tests/unit/test_code_generator.py -v -x` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_step_code_buffer.py backend/tests/unit/test_code_generator.py -v -x`
- **After every plan wave:** Run `uv run pytest backend/tests/unit/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 112-01-01 | 01 | 1 | INTEG-01 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py -k "integration" -x` | Wave 0 | ⬜ pending |
| 112-01-02 | 01 | 1 | INTEG-01 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py -k "on_step_action_dict" -x` | Wave 0 | ⬜ pending |
| 112-02-01 | 02 | 1 | INTEG-02 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py -k "assemble_write" -x` | Wave 0 | ⬜ pending |
| 112-02-02 | 02 | 1 | INTEG-03 | unit | `uv run pytest backend/tests/unit/test_code_generator.py -x` | Update existing | ⬜ pending |
| 112-03-01 | 03 | 2 | VAL-02 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::TestIntegration -x` | Wave 0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_step_code_buffer.py` — add TestIntegration class with VAL-02 tests
- [ ] `backend/tests/unit/test_code_generator.py` — remove test_healing_failure_preserves_original and test_generate_and_save_validates_before_write (methods being deleted per D-03)

*Existing infrastructure covers pytest and pytest-asyncio.*

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
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
