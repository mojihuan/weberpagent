---
phase: 13
slug: 配置基础
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-17
---

# Phase 13 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` (existing) |
| **Quick run command** | `uv run pytest backend/tests/unit/test_config/ -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_config/ -v`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 13-01-01 | 01 | 1 | CONFIG-01 | unit | `uv run pytest backend/tests/unit/test_config/test_settings.py -v -k weberp_path` | ✅ | ⬜ pending |
| 13-01-02 | 01 | 1 | CONFIG-01 | unit | `uv run pytest backend/tests/unit/test_config/test_validators.py -v` | ❌ W0 | ⬜ pending |
| 13-02-01 | 02 | 1 | CONFIG-02 | unit | `uv run pytest backend/tests/unit/test_config/test_validators.py -v -k validate_weberp_path` | ❌ W0 | ⬜ pending |
| 13-03-01 | 03 | 1 | CONFIG-03 | manual | `grep -A 20 "webseleniumerp" README.md` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_config/test_validators.py` — stubs for CONFIG-01, CONFIG-02
- [ ] `backend/tests/unit/test_config/conftest.py` — shared fixtures (mock paths)
- [ ] Existing pytest infrastructure covers all phase requirements.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| README.md contains webseleniumerp configuration section | CONFIG-03 | Documentation verification | Run `grep -A 20 "webseleniumerp" README.md` and verify content |
| Error messages are clear and actionable | CONFIG-02 | UX verification | Temporarily set invalid WEBSERP_PATH and verify startup error output |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
