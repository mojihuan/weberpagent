---
phase: 23
slug: backend-assertion-discovery
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-20
---

# Phase 23 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (existing) |
| **Config file** | backend/tests/conftest.py |
| **Quick run command** | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py -x -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_external_assertion_bridge.py -x`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 23-01-01 | 01 | 1 | DISC-01 | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::test_load_assertion_classes -xvs` | ❌ W0 | ⬜ pending |
| 23-01-02 | 01 | 1 | DISC-01 | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::test_assertion_class_cache -xvs` | ❌ W0 | ⬜ pending |
| 23-02-01 | 02 | 1 | DISC-02 | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::test_get_assertion_methods_grouped -xvs` | ❌ W0 | ⬜ pending |
| 23-02-02 | 02 | 1 | DISC-03 | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::test_parse_data_options -xvs` | ❌ W0 | ⬜ pending |
| 23-02-03 | 02 | 1 | DISC-04 | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::test_parse_param_options -xvs` | ❌ W0 | ⬜ pending |
| 23-03-01 | 03 | 1 | DISC-05 | integration | `uv run pytest backend/tests/api/test_external_assertions_api.py::test_list_assertion_methods_success -xvs` | ❌ W0 | ⬜ pending |
| 23-03-02 | 03 | 1 | DISC-05 | integration | `uv run pytest backend/tests/api/test_external_assertions_api.py::test_list_assertion_methods_unavailable -xvs` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_external_assertion_bridge.py` — unit tests for assertion discovery functions
- [ ] `backend/tests/api/test_external_assertions_api.py` — integration tests for API endpoint
- [ ] Extend `reset_cache()` in bridge module to clear assertion caches

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Real webseleniumerp integration | DISC-01 | Requires external project setup | 1. Set WEBSERP_PATH in .env 2. Start server 3. Call GET /api/external-assertions/methods 4. Verify response contains PcAssert/MgAssert/McAssert classes |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
