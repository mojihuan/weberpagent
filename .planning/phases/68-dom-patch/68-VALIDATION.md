---
phase: 68
slug: dom-patch
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-07
---

# Phase 68 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.0+ |
| **Config file** | pyproject.toml `[tool.pytest.ini_options]` |
| **Quick run command** | `uv run pytest backend/tests/unit/test_dom_patch_phase68.py -v -x` |
| **Full suite command** | `uv run pytest backend/tests/unit/ -v` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_dom_patch_phase68.py -v -x`
- **After every plan wave:** Run `uv run pytest backend/tests/unit/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 68-01-01 | 01 | 1 | STRAT-01, STRAT-03 | unit | `uv run pytest backend/tests/unit/test_dom_patch_phase68.py::TestStrategyDetermination -v` | ❌ W0 | ⬜ pending |
| 68-01-02 | 01 | 1 | ROW-03 | unit | `uv run pytest backend/tests/unit/test_dom_patch_phase68.py::TestRowBelongingAnnotation -v` | ❌ W0 | ⬜ pending |
| 68-02-01 | 02 | 1 | ROW-02 | unit | `uv run pytest backend/tests/unit/test_dom_patch_phase68.py::TestRowIdentityComment -v` | ❌ W0 | ⬜ pending |
| 68-03-01 | 03 | 2 | STRAT-02, ANTI-02 | unit | `uv run pytest backend/tests/unit/test_dom_patch_phase68.py::TestFailureAnnotation -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_dom_patch_phase68.py` — stubs for ROW-02, ROW-03, STRAT-01, STRAT-02, STRAT-03, ANTI-02
- [ ] Test mock for `serialize_tree` output — mock original static method and verify annotation injection

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| None | - | - | All phase behaviors have automated verification |

*If none: "All phase behaviors have automated verification."*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
