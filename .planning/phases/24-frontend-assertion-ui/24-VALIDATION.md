---
phase: 24
slug: frontend-assertion-ui
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-20
---

# Phase 24 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Vitest (frontend) / pytest (backend) |
| **Config file** | `frontend/vitest.config.ts` / `backend/pytest.ini` |
| **Quick run command** | `cd frontend && npm run test -- --run` |
| **Full suite command** | `cd frontend && npm run test -- --run && cd .. && uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd frontend && npm run test -- --run`
- **After every plan wave:** Run full suite
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 24-01-01 | 01 | 1 | UI-01 | unit | `cd frontend && npm run test -- --run AssertionSelector.test.tsx` | ❌ W0 | ⬜ pending |
| 24-01-02 | 01 | 1 | UI-05 | unit | `cd frontend && npm run test -- --run AssertionSelector.test.tsx` | ❌ W0 | ⬜ pending |
| 24-02-01 | 02 | 1 | UI-02 | unit | `cd frontend && npm run test -- --run AssertionSelector.test.tsx` | ❌ W0 | ⬜ pending |
| 24-02-02 | 02 | 1 | UI-03 | unit | `cd frontend && npm run test -- --run AssertionSelector.test.tsx` | ❌ W0 | ⬜ pending |
| 24-02-03 | 02 | 1 | UI-04 | unit | `cd frontend && npm run test -- --run AssertionSelector.test.tsx` | ❌ W0 | ⬜ pending |
| 24-03-01 | 03 | 2 | UI-06 | integration | `cd frontend && npm run test -- --run TaskForm.test.tsx` | ❌ W0 | ⬜ pending |
| 24-03-02 | 03 | 2 | UI-06 | e2e | `npx playwright test --grep "assertion"` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `frontend/src/components/TaskModal/__tests__/AssertionSelector.test.tsx` — stubs for UI-01 to UI-05
- [ ] `frontend/src/components/TaskModal/__tests__/TaskForm.assertion.test.tsx` — stubs for UI-06
- [ ] `frontend/src/api/__tests__/externalAssertions.test.ts` — stubs for API client tests

*Backend: Existing infrastructure covers all phase requirements (pytest fixtures in place).*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Tab switching animation | UI-06 | Visual smoothness | Click between tabs, verify smooth transition |
| Collapsible group animation | UI-01 | Visual smoothness | Click group headers, verify expand/collapse |
| Search debounce feel | UI-05 | UX timing | Type in search, verify 300ms debounce feels right |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
