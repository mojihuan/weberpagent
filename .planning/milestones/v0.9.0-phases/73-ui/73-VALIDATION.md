---
phase: 73
slug: ui
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-09
---

# Phase 73 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | No frontend test framework; TypeScript build check + pytest (backend) |
| **Config file** | `frontend/tsconfig.json` / `backend/pyproject.toml` |
| **Quick run command** | `cd frontend && npm run build` |
| **Full suite command** | `cd backend && uv run pytest backend/tests/ -v && cd ../frontend && npm run build` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd frontend && npm run build`
- **After every plan wave:** Run full suite (backend tests + frontend build)
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 73-01-01 | 01 | 1 | BATCH-03 | unit | `cd backend && uv run pytest backend/tests/ -v -k batch` | ✅ | ⬜ pending |
| 73-02-01 | 02 | 1 | BATCH-03 | build | `cd frontend && npm run build` | ✅ | ⬜ pending |
| 73-02-02 | 02 | 1 | BATCH-03 | build | `cd frontend && npm run build` | ✅ | ⬜ pending |
| 73-02-03 | 02 | 1 | BATCH-03 | build | `cd frontend && npm run build` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Backend: `test_batch_api.py` extended with timing field assertions
- [ ] Frontend: TypeScript compilation passes with new types

*Existing infrastructure covers core phase requirements. No new test framework installation needed.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Batch progress page displays task status cards | BATCH-03 | No frontend E2E framework | Navigate to Tasks, select tasks, batch execute, verify progress page shows cards with correct statuses |
| Polling updates statuses in real-time | BATCH-03 | Timing-dependent behavior | Watch status transitions from pending → running → completed/failed at 2s intervals |
| Click task card navigates to RunMonitor | BATCH-03 | Navigation test requires browser | Click a task card and verify navigation to `/runs/:id` |
| Toast notification on batch completion | BATCH-03 | Toast is transient UI element | Wait for all tasks to complete and verify toast appears with summary |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
