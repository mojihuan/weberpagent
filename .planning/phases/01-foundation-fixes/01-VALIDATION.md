---
phase: 1
slug: foundation-fixes
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-03-14
revised: 2026-03-14
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x (backend), vitest (frontend) |
| **Config file** | `pyproject.toml` (pytest), `frontend/vitest.config.ts` |
| **Quick run command** | `uv run pytest backend/tests/unit/ -v -x` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/ -v -x`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 01-00-01 | 00 | 0 | - | scaffold | `test -f backend/tests/unit/__init__.py` | Created by 01-00 | pending |
| 01-00-02 | 00 | 0 | - | scaffold | `test -f backend/tests/integration/__init__.py` | Created by 01-00 | pending |
| 01-00-03 | 00 | 0 | - | scaffold | `uv run pytest --collect-only -q` | Created by 01-00 | pending |
| 01-01-01 | 01 | 1 | FND-01 | unit | `uv run pytest backend/tests/unit/test_settings.py -v` | Created by 01-00 | pending |
| 01-01-02 | 01 | 1 | FND-01 | unit | `uv run pytest backend/tests/unit/test_settings.py -v` | Created by 01-00 | pending |
| 01-02-01 | 02 | 1 | FND-02 | unit | `uv run pytest backend/tests/unit/test_response_format.py -v` | Created by 01-00 | pending |
| 01-02-02 | 02 | 1 | FND-02 | integration | `uv run pytest backend/tests/integration/test_api_responses.py -v` | Created by 01-00 | pending |
| 01-03-01 | 03 | 1 | FND-03 | unit | `uv run pytest backend/tests/unit/test_database_async.py -v` | Created by 01-00 | pending |
| 01-03-02 | 03 | 1 | FND-03 | integration | `uv run pytest backend/tests/integration/test_database_concurrent.py -v` | Created by 01-00 | pending |
| 01-04-01 | 04 | 2 | FND-04 | unit | `uv run pytest backend/tests/unit/test_llm_config.py -v` | Created by 01-00 | pending |
| 01-04-02 | 04 | 2 | FND-04 | integration | `uv run pytest backend/tests/integration/test_agent_service.py -v` | Created by 01-00 | pending |
| 01-05-01 | 05 | 2 | FND-05 | unit | `uv run pytest backend/tests/unit/test_browser_cleanup.py -v` | Created by 01-00 | pending |

*Status: pending | green | red | flaky*

---

## Wave 0 Requirements

**Status: PLANNED** (Plan 01-00 creates all stubs)

| File | Purpose | Created By |
|------|---------|------------|
| `backend/tests/unit/__init__.py` | Unit test package | 01-00 Task 1 |
| `backend/tests/integration/__init__.py` | Integration test package | 01-00 Task 2 |
| `backend/tests/unit/test_settings.py` | Stubs for FND-01 | 01-00 Task 3 |
| `backend/tests/unit/test_response_format.py` | Stubs for FND-02 | 01-00 Task 3 |
| `backend/tests/unit/test_database_async.py` | Stubs for FND-03 | 01-00 Task 3 |
| `backend/tests/unit/test_llm_config.py` | Stubs for FND-04 | 01-00 Task 4 |
| `backend/tests/unit/test_browser_cleanup.py` | Stubs for FND-05 | 01-00 Task 4 |
| `backend/tests/integration/test_api_responses.py` | Stubs for FND-02 integration | 01-00 Task 5 |
| `backend/tests/integration/test_agent_service.py` | Stubs for FND-04 integration | 01-00 Task 5 |
| `backend/tests/integration/test_database_concurrent.py` | Stubs for FND-03 integration | 01-00 Task 5 |

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| LLM determinism across runs | FND-04 | Requires external API calls and timing | Run same test prompt 3x, compare outputs |
| Browser cleanup on crash | FND-05 | Requires process kill simulation | Kill process mid-execution, verify no orphan processes |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (Plan 01-00)
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending execution
