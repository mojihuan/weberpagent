---
phase: 86
slug: 登录机制研究
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-04-20
---

# Phase 86 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.2 + pytest-asyncio |
| **Config file** | pyproject.toml (tool.pytest.ini_options) |
| **Quick run command** | `.venv/bin/pytest backend/tests/unit/ -x -q` |
| **Full suite command** | `.venv/bin/pytest backend/tests/ -v` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `.venv/bin/pytest backend/tests/unit/ -x -q`
- **After every plan wave:** Run `.venv/bin/pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 86-01-01 | 01 | 1 | SC-3 | manual POC | `.venv/bin/python backend/tests/poc/poc_localstorage_inject.py` | ✅ W0 | ✅ green |
| 86-01-02 | 01 | 1 | SC-3 | manual POC | `.venv/bin/python backend/tests/poc/poc_form_login.py` | ✅ W0 | ✅ green |
| 86-02-01 | 02 | 2 | SC-1/SC-2/SC-4 | documentation | `grep "## " .planning/phases/86-登录机制研究/86-RESEARCH-REPORT.md \| wc -l` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `backend/tests/poc/poc_localstorage_inject.py` — POC script for 方案 C
- [x] `backend/tests/poc/poc_form_login.py` — POC script for 方案 A
- [x] `.venv` with browser-use, httpx, playwright installed — already exists

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| ERP SPA stays logged in after localStorage inject | SC-3 | Requires live ERP server access | Run POC script, verify no /login redirect |
| Form login triggers SPA redirect | SC-3 | Requires live ERP server access | Run POC script, verify SPA navigates to /index |
| Research report completeness | SC-1/SC-2/SC-4 | Subjective quality check | Review RESEARCH.md for all success criteria |

---

## Validation Sign-Off

- [x] All tasks have verification or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** complete
