---
phase: 70
slug: excel
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-08
---

# Phase 70 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (existing) |
| **Config file** | None (uses default pytest discovery) |
| **Quick run command** | `uv run pytest backend/tests/unit/test_excel_template.py backend/tests/unit/test_excel_parser.py -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_excel_template.py backend/tests/unit/test_excel_parser.py -v`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 70-01-01 | 01 | 1 | TMPL-01 | unit | `uv run pytest backend/tests/unit/test_excel_template.py::test_template_has_correct_headers -v` | ❌ W0 | ⬜ pending |
| 70-01-02 | 01 | 1 | TMPL-01 | unit | `uv run pytest backend/tests/unit/test_excel_template.py::test_template_has_example_data -v` | ❌ W0 | ⬜ pending |
| 70-01-03 | 01 | 1 | TMPL-01 | unit | `uv run pytest backend/tests/unit/test_excel_template.py::test_template_has_readme_sheet -v` | ❌ W0 | ⬜ pending |
| 70-01-04 | 01 | 1 | TMPL-02 | unit | `uv run pytest backend/tests/unit/test_excel_template.py::test_max_steps_validation -v` | ❌ W0 | ⬜ pending |
| 70-01-05 | 01 | 1 | TMPL-02 | unit | `uv run python -c "from backend.api.routes.tasks import router; routes = [r.path for r in router.routes]; assert '/template' in routes and routes.index('/template') < next((i for i, r in enumerate(routes) if r == '/{task_id}'), len(routes))"` | ❌ W0 | ⬜ pending |
| 70-02-01 | 02 | 2 | TMPL-01 | unit | `uv run pytest backend/tests/unit/test_excel_parser.py::test_parse_valid_rows -v` | ❌ W0 | ⬜ pending |
| 70-02-02 | 02 | 2 | TMPL-01 | unit | `uv run pytest backend/tests/unit/test_excel_parser.py::test_skip_empty_rows -v` | ❌ W0 | ⬜ pending |
| 70-02-03 | 02 | 2 | TMPL-01 | unit | `uv run pytest backend/tests/unit/test_excel_parser.py::test_merged_cell_detection -v` | ❌ W0 | ⬜ pending |
| 70-02-04 | 02 | 2 | TMPL-01 | unit | `uv run pytest backend/tests/unit/test_excel_parser.py::test_type_coercion -v` | ❌ W0 | ⬜ pending |
| 70-02-05 | 02 | 2 | TMPL-01 | unit | `uv run pytest backend/tests/unit/test_excel_parser.py::test_roundtrip -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_excel_template.py` — stubs for TMPL-01, TMPL-02
- [ ] `backend/tests/unit/test_excel_parser.py` — stubs for parser type coercion, error collection, merged cell detection, empty row skipping

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Downloaded .xlsx opens correctly in Excel/WPS | TMPL-01 | Requires GUI application to verify | 1. Call GET /tasks/template 2. Save response body 3. Open in Excel/WPS 4. Verify headers, example data, README sheet visible |
| Data validation dropdown appears in max_steps column | TMPL-02 | Requires GUI application to verify | 1. Open downloaded template 2. Click cell D2 3. Verify dropdown arrow appears 4. Enter 101 → verify error message shown |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
