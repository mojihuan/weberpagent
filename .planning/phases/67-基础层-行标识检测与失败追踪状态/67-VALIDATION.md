---
phase: 67
slug: 基础层-行标识检测与失败追踪状态
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-07
---

# Phase 67 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest backend/tests/test_dom_patch_phase67.py backend/tests/test_stall_detector_phase67.py -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/test_dom_patch_phase67.py backend/tests/test_stall_detector_phase67.py -v`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 67-01-01 | 01 | 1 | ROW-01 | unit | `uv run pytest backend/tests/test_dom_patch_phase67.py::test_detect_row_identity -v` | ❌ W0 | ⬜ pending |
| 67-01-02 | 01 | 1 | ANTI-01 | unit | `uv run pytest backend/tests/test_dom_patch_phase67.py::test_failure_tracker -v` | ❌ W0 | ⬜ pending |
| 67-02-01 | 02 | 1 | RECOV-01 | unit | `uv run pytest backend/tests/test_stall_detector_phase67.py::test_detect_failure_mode -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/test_dom_patch_phase67.py` — stubs for ROW-01, ANTI-01
- [ ] `backend/tests/test_stall_detector_phase67.py` — stubs for RECOV-01
- [ ] No framework install needed — pytest already configured

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| None | — | — | All phase behaviors have automated verification. |

All phase behaviors have automated verification.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
