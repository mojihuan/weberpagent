---
phase: 28
slug: backend-field-discovery
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-21
---

# Phase 28 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest backend/tests/test_assertions_field_parser.py -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v --tb=short` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/test_assertions_field_parser.py -v`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 28-01-01 | 01 | 1 | FLD-01 | unit | `uv run pytest backend/tests/test_assertions_field_parser.py::test_parse_param_dict -v` | ❌ W0 | ⬜ pending |
| 28-01-02 | 01 | 1 | FLD-01 | unit | `uv run pytest backend/tests/test_assertions_field_parser.py::test_extract_field_tuples -v` | ❌ W0 | ⬜ pending |
| 28-01-03 | 01 | 1 | FLD-01 | unit | `uv run pytest backend/tests/test_assertions_field_parser.py::test_infer_field_group -v` | ❌ W0 | ⬜ pending |
| 28-01-04 | 01 | 1 | FLD-01 | unit | `uv run pytest backend/tests/test_assertions_field_parser.py::test_is_time_field -v` | ❌ W0 | ⬜ pending |
| 28-01-05 | 01 | 1 | FLD-01 | unit | `uv run pytest backend/tests/test_assertions_field_parser.py::test_generate_field_description -v` | ❌ W0 | ⬜ pending |
| 28-02-01 | 02 | 1 | FLD-02 | integration | `uv run pytest backend/tests/test_external_assertions_api.py::test_get_fields_endpoint -v` | ❌ W0 | ⬜ pending |
| 28-02-02 | 02 | 1 | FLD-02 | integration | `uv run pytest backend/tests/test_external_assertions_api.py::test_fields_response_structure -v` | ❌ W0 | ⬜ pending |
| 28-02-03 | 02 | 1 | FLD-03 | integration | `uv run pytest backend/tests/test_external_assertions_api.py::test_fields_grouped_response -v` | ❌ W0 | ⬜ pending |
| 28-02-04 | 02 | 1 | FLD-03 | integration | `uv run pytest backend/tests/test_external_assertions_api.py::test_fields_503_on_unavailable -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/test_assertions_field_parser.py` — unit tests for AST parser
- [ ] `backend/tests/test_external_assertions_api.py` — add fields endpoint tests (file exists, extend it)

*Existing infrastructure covers pytest framework.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| None | - | - | - |

*All phase behaviors have automated verification.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
