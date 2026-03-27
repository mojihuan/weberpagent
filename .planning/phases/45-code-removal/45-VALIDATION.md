---
phase: 45
slug: code-removal
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-26
---

# Phase 45 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest backend/tests/unit/test_agent_service.py -v -k "not scroll" --tb=short` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_agent_service.py -v -k "not scroll" --tb=short`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 45-01-01 | 01 | 1 | CLEANUP-01 | unit | `test ! -d backend/agent/tools` | ✅ | ⬜ pending |
| 45-02-01 | 02 | 1 | CLEANUP-02 | unit | `grep -c "_post_process_td_click" backend/core/agent_service.py` returns 0 | ✅ | ⬜ pending |
| 45-03-01 | 03 | 1 | CLEANUP-03 | unit | `grep -c "_fallback_input" backend/core/agent_service.py` returns 0 | ✅ | ⬜ pending |
| 45-04-01 | 04 | 1 | CLEANUP-04 | unit | `grep -c "_collect_element_diagnostics" backend/core/agent_service.py` returns 0 | ✅ | ⬜ pending |
| 45-05-01 | 05 | 1 | CLEANUP-05 | unit | `grep -c "LoopInterventionTracker" backend/core/agent_service.py` returns 0 | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `backend/tests/unit/test_agent_service.py` — existing test file
- [x] `backend/tests/conftest.py` — shared fixtures exist
- [x] pytest — framework installed

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| None | - | - | - |

*All phase behaviors have automated verification.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
