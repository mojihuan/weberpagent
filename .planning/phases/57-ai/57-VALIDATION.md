---
phase: 57
slug: ai
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-02
---

# Phase 57 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | No frontend test framework (manual browser verification) |
| **Config file** | None |
| **Quick run command** | `cd frontend && npm run build` |
| **Full suite command** | `cd frontend && npm run build` + manual browser check |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd frontend && npm run build`
- **After every plan wave:** Visual verification in browser
- **Before `/gsd:verify-work`:** Build passes + both components verified visually
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 57-01-01 | 01 | 1 | FMT-01 | unit | Manual browser | N/A | ⬜ pending |
| 57-01-02 | 01 | 1 | FMT-02 | visual | Manual browser | N/A | ⬜ pending |
| 57-01-03 | 01 | 1 | FMT-03 | visual | Manual browser | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

No frontend test framework exists. For this phase (pure visual formatting), manual browser verification is sufficient.

- [x] `cd frontend && npm run build` — TypeScript compilation check
- [ ] Manual browser verification with existing task data containing reasoning text

*Existing infrastructure covers build verification. Visual checks are manual.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Reasoning text parsed into labeled badges | FMT-01 | No test framework | Open execution monitor, verify Eval/Verdict/Memory/Goal each on own line with colored badges |
| StepItem shows formatted reasoning | FMT-02 | Visual formatting | Open report detail page, verify reasoning badges in step items |
| ReasoningLog shows formatted reasoning | FMT-03 | Visual formatting | Open execution monitor, verify reasoning badges in log |
| Edge case: empty reasoning | FMT-01 | Visual edge case | Verify "暂无推理记录" shown for null/empty reasoning |
| Edge case: no standard labels | FMT-01 | Visual edge case | Verify plain text display for reasoning without Eval/Verdict/Memory/Goal |

---

## Validation Sign-Off

- [x] All tasks have verification approach (manual browser + build check)
- [x] Sampling continuity: build check after every task commit
- [x] Wave 0 covers build infrastructure
- [x] No watch-mode flags
- [x] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
