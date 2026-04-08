---
phase: 63
slug: 63-代码对比分析
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-06
---

# Phase 63 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest backend/tests/ -v -x -q 2>&1 \| tail -20` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/ -v -x -q 2>&1 | tail -20`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 63-01-01 | 01 | 1 | DIFF-01 | analysis | `grep -c "headless" .planning/phases/63-代码对比分析/63-PLAN.md` | ⬜ pending | ⬜ pending |
| 63-01-02 | 01 | 1 | DIFF-02 | analysis | `grep -c "Playwright" .planning/phases/63-代码对比分析/63-PLAN.md` | ⬜ pending | ⬜ pending |
| 63-02-01 | 02 | 1 | DIFF-03 | analysis | `grep -c "browser-use" .planning/phases/63-代码对比分析/63-PLAN.md` | ⬜ pending | ⬜ pending |
| 63-02-02 | 02 | 1 | DIFF-04 | analysis | `grep -c "agent_service" .planning/phases/63-代码对比分析/63-PLAN.md` | ⬜ pending | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements. This phase is primarily analytical/comparative — no new test infrastructure needed.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Verify comparison reports are accurate | DIFF-01~04 | Requires human review of git history interpretation | Read generated comparison docs and verify against actual git log |

---

## Validation Sign-Off

- [x] All tasks have automated verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
