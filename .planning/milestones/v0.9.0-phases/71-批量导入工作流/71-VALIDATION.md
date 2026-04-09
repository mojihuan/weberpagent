---
phase: 71
slug: 批量导入工作流
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-04-08
---

# Phase 71 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (backend), tsc + vite build (frontend) |
| **Config file** | pyproject.toml, frontend/tsconfig.json |
| **Quick run command** | `uv run pytest backend/tests/ -k "import" -v --tb=short` |
| **Full suite command** | `uv run pytest backend/tests/ -v && cd frontend && npx tsc --noEmit && npm run build` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/ -k "import" -v --tb=short` (backend) or `cd frontend && npx tsc --noEmit` (frontend)
- **After every plan wave:** Run full suite command
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| TBD | 01 | 1 | IMPT-01 | unit | `uv run pytest backend/tests/unit/test_import_endpoints.py -v` | ❌ W0 | ⬜ pending |
| TBD | 01 | 1 | IMPT-03 | unit | `uv run pytest backend/tests/unit/test_import_endpoints.py -v` | ❌ W0 | ⬜ pending |
| TBD | 02 | 2 | IMPT-01, IMPT-02, IMPT-03 | static | `cd frontend && npx tsc --noEmit && npm run build` | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_import_endpoints.py` — stubs for IMPT-01, IMPT-02, IMPT-03 (all 9 test cases from Plan 01 Task 1)
- [ ] Existing infrastructure covers frontend static verification (TypeScript compiler + Vite build already configured).

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Drag-and-drop file upload UX | IMPT-01 | Browser interaction required | Manually drag .xlsx file onto drop zone, verify highlight |
| Error row red highlighting in preview | IMPT-01, IMPT-02 | Visual rendering | Upload file with errors, verify red rows in preview table |
| Confirm button disabled with invalid rows | IMPT-02 | Visual state | Upload file with errors, verify button is disabled |
| Summary bar shows correct counts | IMPT-02 | Visual rendering | Upload file with mixed valid/invalid rows, verify counts |
| Auto-close after successful import | IMPT-01 | Timed behavior | Complete import, verify Modal auto-closes after 1.5s |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
