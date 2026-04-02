---
phase: 59
slug: report-steps
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-02
---

# Phase 59 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (backend) + vitest (frontend) |
| **Config file** | pytest.ini / frontend/vitest.config.ts |
| **Quick run command** | `uv run pytest backend/tests/ -v -x -q` |
| **Full suite command** | `uv run pytest backend/tests/ -v && cd frontend && npm run build` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/ -v -x -q`
- **After every plan wave:** Run full suite (pytest + frontend build)
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 59-01-01 | 01 | 1 | RPT-01 | unit | `uv run pytest backend/tests/test_precondition_result.py -v` | ❌ W0 | ⬜ pending |
| 59-01-02 | 01 | 1 | RPT-01,RPT-03 | unit | `uv run pytest backend/tests/test_report_timeline.py -v` | ❌ W0 | ⬜ pending |
| 59-01-03 | 01 | 1 | RPT-02,RPT-03 | integration | `uv run pytest backend/tests/test_report_api.py -v` | ❌ W0 | ⬜ pending |
| 59-01-04 | 01 | 2 | RPT-01,RPT-02 | unit | `cd frontend && npm run build` | ✅ | ⬜ pending |
| 59-01-05 | 01 | 2 | RPT-03 | unit | `cd frontend && npm run build` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/test_precondition_result.py` — stubs for RPT-01
- [ ] `backend/tests/test_report_timeline.py` — stubs for RPT-01, RPT-03
- [ ] `backend/tests/test_report_api.py` — stubs for RPT-02, RPT-03

*Frontend: Existing vitest infrastructure covers frontend build verification.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Visual layout of 3 step types in report | RPT-01,RPT-02 | Color/icon/rendering | Open report detail, verify 3 card types with distinct styles |
| Timeline interleaving order | RPT-03 | Requires real execution data | Run a task with preconditions+assertions, verify order in report |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
