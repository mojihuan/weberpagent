---
phase: 58
slug: exec-display
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-02
---

# Phase 58 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | vitest (unit) + Playwright (E2E) |
| **Config file** | frontend/vitest.config.ts |
| **Quick run command** | `cd frontend && npx vitest run --reporter=verbose 2>&1 | tail -20` |
| **Full suite command** | `cd frontend && npx vitest run 2>&1` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd frontend && npx vitest run --reporter=verbose 2>&1 | tail -20`
- **After every plan wave:** Run `cd frontend && npx vitest run 2>&1`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 58-01-01 | 01 | 1 | EXEC-01 | unit | `cd frontend && npx vitest run` | ⬜ W0 | ⬜ pending |
| 58-01-02 | 01 | 1 | EXEC-02 | unit | `cd frontend && npx vitest run` | ⬜ W0 | ⬜ pending |
| 58-01-03 | 01 | 1 | EXEC-03 | unit | `cd frontend && npx vitest run` | ⬜ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `frontend/src/types/__tests__/timeline.test.ts` — stubs for EXEC-01/02/03 type tests
- [ ] `frontend/src/hooks/__tests__/useRunStream.test.ts` — stubs for SSE event handling tests

*Existing vitest infrastructure covers framework needs. Only test file stubs required.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Timeline renders all 3 step types interleaved | EXEC-03 | Visual ordering verification requires browser | Run a test case with preconditions + assertions, verify StepTimeline shows all steps in execution order |
| Duplicate event handling (running → success) | EXEC-01 | SSE event sequence timing | Observe timeline doesn't show duplicate entries when precondition transitions from running to success |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
