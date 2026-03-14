---
phase: 4
slug: frontend-e2e-alignment
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-14
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Vitest (unit) + Playwright (E2E) |
| **Config file** | e2e/playwright.config.ts (to create in Wave 0) |
| **Quick run command** | `npx playwright test --project=chromium --reporter=list` |
| **Full suite command** | `npx playwright test` |
| **Estimated runtime** | ~60 seconds |

---

## Sampling Rate

- **After every task commit:** Run affected component's E2E test
- **After every plan wave:** Run full E2E suite
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | UI-01 | manual | Type comparison | N/A | ⬜ pending |
| 04-01-02 | 01 | 1 | UI-06 | manual | Verify VITE_API_BASE usage | Yes | ⬜ pending |
| 04-02-01 | 02 | 1 | UI-02 | E2E | `npx playwright test -g "task list"` | ❌ W0 | ⬜ pending |
| 04-03-01 | 03 | 1 | UI-03 | E2E | `npx playwright test -g "monitor"` | ❌ W0 | ⬜ pending |
| 04-03-02 | 03 | 1 | UI-04 | E2E | `npx playwright test -g "screenshot"` | ❌ W0 | ⬜ pending |
| 04-04-01 | 04 | 2 | UI-05 | E2E | `npx playwright test -g "report"` | ❌ W0 | ⬜ pending |
| 04-05-01 | 05 | 2 | E2E-01 | E2E | `npx playwright test -g "create task"` | ❌ W0 | ⬜ pending |
| 04-05-02 | 05 | 2 | E2E-02 | E2E | `npx playwright test -g "execute"` | ❌ W0 | ⬜ pending |
| 04-05-03 | 05 | 2 | E2E-03 | E2E | `npx playwright test -g "screenshot"` | ❌ W0 | ⬜ pending |
| 04-05-04 | 05 | 2 | E2E-04 | E2E | `npx playwright test -g "report"` | ❌ W0 | ⬜ pending |
| 04-05-05 | 05 | 2 | E2E-05 | E2E | `npx playwright test smoke.spec.ts` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `e2e/playwright.config.ts` — Playwright configuration
- [ ] `e2e/tests/smoke.spec.ts` — Complete flow smoke test stubs
- [ ] `e2e/tests/task-flow.spec.ts` — Task CRUD test stubs
- [ ] Playwright install: `npx playwright install chromium`
- [ ] Frontend: `npm install sonner` for toast notifications

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| TypeScript type alignment | UI-01 | Type comparison, not runtime behavior | Compare frontend/src/types/index.ts with backend/api/schemas/index.py field by field |
| API URL environment variable | UI-06 | Build-time configuration | Verify VITE_API_BASE_URL is used in frontend/src/api/client.ts |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
