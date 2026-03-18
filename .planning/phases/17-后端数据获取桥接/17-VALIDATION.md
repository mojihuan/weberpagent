---
phase: "17"
slug: 后端数据获取桥接
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 17 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.0.0+ |
| **Config file** | pyproject.toml `[tool.pytest.ini_options]` |
| **Quick run command** | `uv run pytest backend/tests/unit/test_external_bridge.py -x -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_external_bridge.py -x -v`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 17-01-01 | 01 | 1 | DATA-01 | unit | `uv run pytest backend/tests/unit/test_external_bridge.py::TestDataMethodsDiscovery -x` | ❌ W0 | ⬜ pending |
| 17-01-02 | 01 | 1 | DATA-01 | unit | `uv run pytest backend/tests/unit/test_external_bridge.py::TestDataMethodsDiscovery::test_extract_parameter_info -x` | ❌ W0 | ⬜ pending |
| 17-02-01 | 02 | 1 | DATA-02 | api | `uv run pytest backend/tests/api/test_external_data_methods.py::TestListDataMethods -x` | ❌ W0 | ⬜ pending |
| 17-03-01 | 03 | 1 | DATA-03 | api | `uv run pytest backend/tests/api/test_external_data_methods.py::TestExecuteDataMethod -x` | ❌ W0 | ⬜ pending |
| 17-03-02 | 03 | 1 | DATA-03 | api | `uv run pytest backend/tests/api/test_external_data_methods.py::TestExecuteDataMethod::test_timeout_protection -x` | ❌ W0 | ⬜ pending |
| 17-03-03 | 03 | 1 | DATA-03 | api | `uv run pytest backend/tests/api/test_external_data_methods.py::TestExecuteDataMethod::test_parameter_error -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_external_bridge.py` — 添加 `TestDataMethodsDiscovery` 测试类
- [ ] `backend/tests/api/test_external_data_methods.py` — 新建 API 集成测试文件
- [ ] `backend/tests/conftest.py` — 添加 `mock_base_params` fixture 模拟外部模块
- [ ] 无需新框架 — pytest 已配置完成

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 真实 ERP 环境集成 | DATA-03 | 需要 webseleniumerp 环境 | 1. 配置 WEBSERP_PATH 2. 调用 /execute 端点 3. 验证返回真实数据 |
| 大数据集性能 | DATA-03 | 需要真实数据量 | 调用分页参数 (i=0, j=1000) 验证响应时间 < 30s |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
