---
phase: 44
slug: logging-and-verification
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-25
---

# Phase 44 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | `pyproject.toml` (existing) |
| **Quick run command** | `uv run pytest backend/tests/unit/test_agent_service.py -v -k "diagnostic" --tb=short` |
| **Full suite command** | `uv run pytest backend/tests/ -v --tb=short` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_agent_service.py -v -k "diagnostic" --tb=short`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v --tb=short`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 44-01-01 | 01 | 1 | LOG-03 | unit | `uv run pytest backend/tests/unit/test_agent_service.py::TestElementDiagnostics -v --tb=short` | ✅ | ⬜ pending |
| 44-01-02 | 01 | 1 | LOG-03 | unit | `uv run pytest backend/tests/unit/test_agent_service.py::TestElementDiagnostics -v --tb=short` | ✅ | ⬜ pending |
| 44-01-03 | 01 | 1 | LOG-03 | integration | `uv run pytest backend/tests/unit/test_agent_service.py -v --tb=short` | ✅ | ⬜ pending |
| 44-02-01 | 02 | 2 | LOG-03 | unit | `uv run pytest backend/tests/unit/test_agent_service.py::TestElementDiagnostics::test_element_diagnostics_integration_with_fallback -v --tb=short` | ✅ | ⬜ pending |
| 44-02-02 | 02 | 2 | LOG-03 | manual | Manual: Run sales outbound use case, inspect step_stats | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements:
- ✅ `backend/tests/unit/test_agent_service.py` — existing test file
- ✅ `backend/tests/conftest.py` — shared fixtures exist
- ✅ pytest framework installed via pyproject.toml

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Agent 3-step table input | SC4 | Requires real browser + ERP system | 1. Start backend service 2. Run sales outbound use case 3. Check step 11 logs for 3-step completion |
| Stagnation ≤ 5 | SC5 | Requires real browser + ERP system | 1. Run sales outbound use case 2. Check step_stats['stagnation'] value |
| element_diagnostics content | LOG-03 | Requires real DOM elements | 1. Run use case 2. Inspect step_stats['element_diagnostics'] in logs |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
