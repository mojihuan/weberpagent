---
phase: 111
slug: stepcodebuffer
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-04-28
---

# Phase 111 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (via uv) |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest backend/tests/unit/test_step_code_buffer.py -v` |
| **Full suite command** | `uv run pytest backend/tests/unit/test_step_code_buffer.py backend/tests/unit/test_dom_patch.py backend/tests/unit/test_code_api.py -v` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_step_code_buffer.py -v`
- **After every plan wave:** Run `uv run pytest backend/tests/unit/test_step_code_buffer.py backend/tests/unit/test_code_api.py -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 111-01-01 | 01 | 1 | CODEGEN-01 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_append_step_sync -v` | ❌ W0 | ⬜ pending |
| 111-01-02 | 01 | 1 | CODEGEN-02 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_derive_wait -v` | ❌ W0 | ⬜ pending |
| 111-02-01 | 02 | 1 | CODEGEN-03 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_append_step_async -v` | ❌ W0 | ⬜ pending |
| 111-03-01 | 03 | 2 | CODEGEN-04 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_assemble -v` | ❌ W0 | ⬜ pending |
| 111-04-01 | 04 | 2 | VAL-01 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_step_code_buffer.py` — stubs for CODEGEN-01~04, VAL-01
- [ ] `backend/tests/unit/conftest.py` — shared fixtures (likely exists)

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| (none) | — | — | — |

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
