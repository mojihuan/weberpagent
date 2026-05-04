---
phase: 125
slug: backend-core-review
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-03
---

# Phase 125 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | ruff 0.15.12 + mypy 1.20.2 (review-only, no test execution) |
| **Config file** | pyproject.toml (ruff), mypy.ini |
| **Quick run command** | `ruff check backend/agent/ backend/core/ backend/api/routes/run_pipeline.py` |
| **Full suite command** | `ruff check backend/ && mypy backend/ --config mypy.ini` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `ruff check backend/agent/ backend/core/`
- **After every plan wave:** Run `ruff check backend/ && mypy backend/`
- **Before `/gsd:verify-work`:** No code changes expected (review-only phase)
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 125-01-01 | 01 | 1 | CORR-01 | manual | `ruff check` | N/A (review) | ⬜ pending |
| 125-02-01 | 02 | 2 | CORR-01 | manual | `ruff check` | N/A (review) | ⬜ pending |
| 125-03-01 | 03 | 3 | ARCH-01, ARCH-02 | manual | `ruff check` | N/A (review) | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] No test infrastructure needed — this is a review-only phase that outputs FINDINGS.md

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Code review correctness | CORR-01, ARCH-01, ARCH-02 | Human judgment required for logic review | Read source files, cross-reference with FINDINGS.md |
| Finding quality | CORR-01 | Subjective assessment of review depth | Verify FINDINGS.md covers all 4 success criteria |

---

## Validation Sign-Off

- [ ] All tasks have manual verify (review-only phase)
- [ ] Sampling continuity: ruff/mypy checks between tasks
- [ ] Wave 0: not applicable (no code changes)
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
