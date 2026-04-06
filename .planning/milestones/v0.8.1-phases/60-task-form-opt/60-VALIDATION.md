---
phase: 60
slug: task-form-opt
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-02
---

# Phase 60 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | vitest (frontend) + pytest (backend) |
| **Config file** | frontend/vite.config.ts / backend/pyproject.toml |
| **Quick run command** | `cd frontend && npx vitest run --reporter=verbose 2>&1 | tail -20` |
| **Full suite command** | `cd frontend && npm run build 2>&1 && npx vitest run` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd frontend && npx vitest run --reporter=verbose 2>&1 | tail -20`
- **After every plan wave:** Run `cd frontend && npm run build 2>&1 && npx vitest run`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 60-01-01 | 01 | 1 | FORM-01 | build | `cd frontend && npm run build` | W0 | ⬜ pending |
| 60-01-02 | 01 | 1 | FORM-01 | unit | `cd frontend && npx vitest run` | W0 | ⬜ pending |
| 60-01-03 | 01 | 1 | FORM-02 | unit | `cd backend && uv run pytest -v` | W0 | ⬜ pending |
| 60-01-04 | 01 | 1 | FORM-02 | build | `cd frontend && npm run build` | W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Verify existing test infrastructure runs clean before modifications

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Tab switcher not visible in TaskForm | FORM-01 | Visual UI check | Open task modal, verify no tab switcher between assertions |
| Business assertion section always visible | FORM-01 | Visual UI check | Open task modal, verify AssertionSelector is visible by default |
| No api_assertions textarea | FORM-02 | Visual UI check | Verify no free-text code input for API assertions |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
