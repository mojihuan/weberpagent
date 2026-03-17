---
phase: 8
slug: 前端实时监控完善
status: draft
nyquist_compliant: false
wave_0_complete: true
created: 2026-03-17
---

# Phase 8 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Backend Framework** | pytest 7.x |
| **Frontend Framework** | Vitest (not configured - manual E2E) |
| **Config file** | pyproject.toml (backend), none (frontend) |
| **Quick run command** | `uv run pytest backend/tests/unit/ -v -x` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Frontend build** | `cd frontend && npm run build` |
| **Estimated runtime** | ~30 seconds (backend), ~60 seconds (frontend build) |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/ -v -x`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v && cd frontend && npm run build`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 08-01-01 | 01 | 1 | API-01 | unit | `uv run pytest backend/tests/unit/ -v -k test_report` | ✅ | ⬜ pending |
| 08-01-02 | 01 | 1 | API-01 | unit | `uv run pytest backend/tests/unit/ -v -k test_report` | ✅ | ⬜ pending |
| 08-02-01 | 02 | 1 | API-01 | build | `cd frontend && npm run build` | ✅ | ⬜ pending |
| 08-02-02 | 02 | 1 | API-01 | build | `cd frontend && npm run build` | ✅ | ⬜ pending |
| 08-02-03 | 02 | 1 | API-01 | build | `cd frontend && npm run build` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `backend/tests/unit/` — existing test infrastructure
- [x] `backend/tests/integration/` — integration test infrastructure
- [x] `frontend/` — existing TypeScript/React setup

*Existing infrastructure covers all phase requirements. Frontend lacks unit tests but build verification is sufficient for this gap closure.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| SSE event real-time display | API-04 | Requires live browser testing | 1. Create task with preconditions/api_assertions 2. Execute task 3. Verify events appear in RunMonitor |
| Report page API assertion display | API-04 | Requires E2E flow | 1. Execute task with api_assertions 2. Navigate to report page 3. Verify api_assertion_results and api_pass_rate displayed |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter (after approval)

**Approval:** pending
