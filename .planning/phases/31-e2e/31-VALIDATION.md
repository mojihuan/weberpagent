---
phase: 31
slug: e2e
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-22
---

# Phase 31 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Playwright Test ^1.40.0 |
| **Config file** | e2e/playwright.config.ts |
| **Quick run command** | `cd e2e && npx playwright test assertion-flow.spec.ts -g "field_params\|now\|three-layer"` |
| **Full suite command** | `cd e2e && npx playwright test assertion-flow.spec.ts` |
| **Estimated runtime** | ~5-10 minutes (3 new tests × 5min timeout each) |

---

## Sampling Rate

- **After every task commit:** Run `cd e2e && npx playwright test assertion-flow.spec.ts -g "new test name"`
- **After every plan wave:** Run full assertion-flow.spec.ts suite
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 300 seconds (5 minutes per test)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 31-01-01 | 01 | 1 | E2E-01, E2E-02 | E2E | `cd e2e && npx playwright test assertion-flow.spec.ts -g "field_params configuration"` | Extend | pending |
| 31-01-02 | 01 | 1 | E2E-01, E2E-02 | E2E | `cd e2e && npx playwright test assertion-flow.spec.ts -g "now time conversion"` | Extend | pending |
| 31-01-03 | 01 | 1 | E2E-01, E2E-02 | E2E | `cd e2e && npx playwright test assertion-flow.spec.ts -g "three-layer params success"` | Extend | pending |

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements:
- [x] `e2e/tests/assertion-flow.spec.ts` — existing test patterns (5 tests)
- [x] `e2e/playwright.config.ts` — Playwright configuration with auto webServer
- [x] `e2e/package.json` — dependencies installed

*No Wave 0 work needed - extending existing test file.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| None | - | - | - |

*All phase behaviors have automated verification via E2E tests.*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 300s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
