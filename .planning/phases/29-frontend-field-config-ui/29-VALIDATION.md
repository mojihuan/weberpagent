---
phase: 29
slug: frontend-field-config-ui
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-22
---

# Phase 29 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Manual UI verification (no frontend test framework) |
| **Config file** | none — Frontend tests not configured |
| **Quick run command** | `cd frontend && npm run build` (type check) |
| **Full suite command** | Manual browser testing |
| **Estimated runtime** | ~5 minutes per manual test |

---

## Sampling Rate

- **After every task commit:** Run `cd frontend && npm run build` (type check only)
- **After every plan wave:** Manual browser verification of UI changes
- **Before `/gsd:verify-work`:** Full manual UI walkthrough
- **Max feedback latency:** 5 minutes

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 29-01-01 | 01 | 1 | UI-01 | type | `npm run build` | ✅ | ⬜ pending |
| 29-01-02 | 01 | 1 | UI-02 | type | `npm run build` | ✅ | ⬜ pending |
| 29-01-03 | 01 | 1 | UI-03 | type | `npm run build` | ✅ | ⬜ pending |
| 29-01-04 | 01 | 1 | UI-04 | type | `npm run build` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] Existing infrastructure covers all phase requirements (type checking via `npm run build`)

*Note: Frontend unit test framework not configured. All UI behaviors verified manually.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Three-region layout | UI-01 | No test framework | 1. Open TaskModal, add assertion 2. Verify three distinct sections visible |
| Field search | UI-02 | No test framework | 1. Type in search box 2. Verify field list filters correctly |
| Grouped field display | UI-02 | No test framework | 1. Expand group 2. Verify fields shown with correct count |
| "now" button for time fields | UI-03 | No test framework | 1. Select time field 2. Click "now" button 3. Verify "now" string appears in input |
| Add/remove field configs | UI-04 | No test framework | 1. Add field config 2. Verify appears in list 3. Delete and verify removed |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies (type check only)
- [x] Sampling continuity: type check after every commit
- [x] Wave 0 covers all MISSING references (none needed)
- [x] No watch-mode flags
- [x] Feedback latency < 5 min
- [ ] `nyquist_compliant: true` set in frontmatter (pending execution)

**Approval:** pending
