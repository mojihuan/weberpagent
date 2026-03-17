---
phase: "05"
slug: 前置条件系统
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-16
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x + pytest-asyncio |
| **Config file** | backend/tests/conftest.py |
| **Quick run command** | `uv run pytest backend/tests/unit/ -v --tb=short` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/ -v --tb=short`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | PRE-01 | unit | `uv run pytest backend/tests/unit/test_models.py::test_task_preconditions -v` | ❌ W0 | ⬜ pending |
| 05-01-02 | 01 | 1 | PRE-01 | unit | `uv run pytest backend/tests/unit/test_schemas.py::test_precondition_schema -v` | ❌ W0 | ⬜ pending |
| 05-02-01 | 02 | 1 | PRE-02 | unit | `uv run pytest backend/tests/unit/test_precondition_service.py::test_execute_without_browser -v` | ❌ W0 | ⬜ pending |
| 05-02-02 | 02 | 1 | PRE-02 | unit | `uv run pytest backend/tests/unit/test_precondition_service.py::test_timeout_control -v` | ❌ W0 | ⬜ pending |
| 05-03-01 | 03 | 1 | PRE-03 | unit | `uv run pytest backend/tests/unit/test_precondition_service.py::test_load_external_module -v` | ❌ W0 | ⬜ pending |
| 05-04-01 | 04 | 2 | PRE-04 | unit | `uv run pytest backend/tests/unit/test_precondition_service.py::test_substitute_variables -v` | ❌ W0 | ⬜ pending |
| 05-04-02 | 04 | 2 | PRE-04 | integration | `uv run pytest backend/tests/integration/test_precondition_flow.py -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_precondition_service.py` — PreconditionService 单元测试桩
- [ ] `backend/tests/integration/test_precondition_flow.py` — 前置条件到 UI 测试的完整流程测试桩
- [ ] `backend/tests/unit/test_models.py::test_task_preconditions` — Task.preconditions 字段测试
- [ ] `backend/tests/unit/test_schemas.py::test_precondition_schema` — Precondition schema 测试

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 前端前置条件输入区域显示 | PRE-01 | UI 视觉验证 | 1. 创建新任务 2. 检查前置条件输入区域可见 3. 添加/删除前置条件验证交互 |
| 前置条件执行进度展示 | PRE-02 | SSE 实时更新验证 | 1. 执行带前置条件的任务 2. 观察执行监控页面 3. 确认前置条件进度实时更新 |
| 外部模块路径配置生效 | PRE-03 | 环境配置验证 | 1. 配置 ERP_API_MODULE_PATH 2. 执行引用外部 API 的前置条件 3. 确认模块加载成功 |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
