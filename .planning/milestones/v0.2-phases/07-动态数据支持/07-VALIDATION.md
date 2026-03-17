---
phase: 07
slug: dynamic-data-support
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-17
---

# Phase 7 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest backend/tests/unit/test_dynamic_data.py -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v --tb=short` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_dynamic_data.py -v`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 07-01-01 | 01 | 1 | DYN-01 | unit | `uv run pytest backend/tests/unit/test_random_generators.py -v` | ❌ W0 | ⬜ pending |
| 07-01-02 | 01 | 1 | DYN-01 | unit | `uv run pytest backend/tests/unit/test_random_generators.py -v` | ❌ W0 | ⬜ pending |
| 07-02-01 | 02 | 1 | DYN-04 | unit | `uv run pytest backend/tests/unit/test_time_utils.py -v` | ❌ W0 | ⬜ pending |
| 07-02-02 | 02 | 1 | DYN-04 | unit | `uv run pytest backend/tests/unit/test_time_utils.py -v` | ❌ W0 | ⬜ pending |
| 07-03-01 | 03 | 2 | DYN-01, DYN-04 | integration | `uv run pytest backend/tests/integration/test_precondition_dynamic_data.py -v` | ❌ W0 | ⬜ pending |
| 07-03-02 | 03 | 2 | DYN-03 | integration | `uv run pytest backend/tests/integration/test_context_passing.py -v` | ❌ W0 | ⬜ pending |
| 07-04-01 | 04 | 2 | DYN-01, DYN-02, DYN-03, DYN-04 | e2e | `uv run pytest backend/tests/e2e/test_dynamic_data_flow.py -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_random_generators.py` — 随机数生成器测试
- [ ] `backend/tests/unit/test_time_utils.py` — 时间计算工具测试
- [ ] `backend/tests/integration/test_precondition_dynamic_data.py` — 前置条件集成测试
- [ ] `backend/tests/integration/test_context_passing.py` — context 传递测试
- [ ] `backend/tests/e2e/test_dynamic_data_flow.py` — E2E 流程测试

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| None | - | - | All phase behaviors have automated verification |

*All phase behaviors have automated verification.*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
