---
phase: 15
slug: 前端集成
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 15 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Manual testing (no frontend test infrastructure) |
| **Config file** | none — Deferred to future phase |
| **Quick run command** | `cd frontend && npm run build` (type check + build) |
| **Full suite command** | Manual: open UI, test flows |
| **Estimated runtime** | ~30 seconds (build) |

---

## Sampling Rate

- **After every task commit:** Run `cd frontend && npm run build`
- **After every plan wave:** Manual UI verification
- **Before `/gsd:verify-work`:** Build must pass, manual flows verified
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 15-01-01 | 01 | 1 | FRONT-01 | build | `npm run build` | ❌ W0 | ⬜ pending |
| 15-01-02 | 01 | 1 | FRONT-02 | manual | Modal shows grouped ops | N/A | ⬜ pending |
| 15-02-01 | 02 | 1 | FRONT-03 | build | `npm run build` | ❌ W0 | ⬜ pending |
| 15-02-02 | 02 | 1 | FRONT-03 | manual | Multi-select works | N/A | ⬜ pending |
| 15-03-01 | 03 | 1 | FRONT-04 | build | `npm run build` | ❌ W0 | ⬜ pending |
| 15-03-02 | 03 | 1 | FRONT-04 | manual | Code generates correctly | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] Existing infrastructure covers all phase requirements (manual testing)
- [x] TypeScript compiler available for type checking
- [x] Build command available for compilation verification

*No additional test infrastructure required for this phase.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Modal opens on button click | FRONT-01 | No E2E infrastructure | Click "选择操作码" button, verify modal appears |
| Operations grouped by module | FRONT-02 | Visual verification | Check groups: 配件管理、财务、运营、平台 |
| Multi-select functionality | FRONT-03 | Interaction test | Select FA1 and HC1, verify both checked |
| Search filters operations | FRONT-03 | Interaction test | Type "FA1", verify filtered list |
| Code appended to textarea | FRONT-04 | Integration test | Select ops, click confirm, check textarea has code |
| 503 error handling | FRONT-01 | Error state test | Set invalid WEBSERP_PATH, verify disabled button + tooltip |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: build verification after each task
- [x] Wave 0 covers all MISSING references (N/A - using manual testing)
- [x] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter (after verification)

**Approval:** pending
