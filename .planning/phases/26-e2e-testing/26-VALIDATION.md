---
phase: 26
slug: e2e-testing
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-20
---

# Phase 26 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Playwright 1.51.1 |
| **Config file** | e2e/playwright.config.ts |
| **Quick run command** | `npm run test:e2e -- --grep "smoke"` |
| **Full suite command** | `npm run test:e2e` |
| **Estimated runtime** | ~180 seconds (AI execution) |

---

## Sampling Rate

- **After every task commit:** Run `npm run test:e2e -- --grep "smoke"`
- **After every plan wave:** Run `npm run test:e2e`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 180 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 26-01-01 | 01 | 1 | SC-1 | E2E | `npx playwright test assertion-flow.spec.ts -g "create"` | ❌ W0 | ⬜ pending |
| 26-01-02 | 01 | 1 | SC-2 | E2E | `npx playwright test assertion-flow.spec.ts -g "report"` | ❌ W0 | ⬜ pending |
| 26-02-01 | 02 | 1 | SC-3 | E2E | `npx playwright test assertion-flow.spec.ts -g "multiple"` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `e2e/tests/assertion-flow.spec.ts` — E2E tests for SC-1, SC-2, SC-3
- [ ] Manual verification checklist in VERIFICATION.md template
- [ ] No additional framework config needed — existing playwright.config.ts sufficient

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Complete sales outbound flow | SC-1, SC-2, SC-3 | E2E tests may pass with simplified scenarios; manual verification ensures real-world usability | Execute full flow: create task with assertions → run → verify report displays results correctly |
| Context variable access (SC-4) | SC-4 | Deferred to future phase — not in E2E scope | N/A |

*If none: "All phase behaviors have automated verification."*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 180s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
