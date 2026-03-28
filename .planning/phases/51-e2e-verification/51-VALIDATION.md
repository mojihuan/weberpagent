---
phase: 51
slug: e2e-verification
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-28
---

# Phase 51 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | pyproject.toml (tool.pytest) |
| **Quick run command** | `uv run pytest backend/tests/unit/test_stall_detector.py backend/tests/unit/test_pre_submit_guard.py backend/tests/unit/test_task_progress_tracker.py backend/tests/unit/test_monitored_agent.py backend/tests/unit/test_enhanced_prompt.py backend/tests/unit/test_agent_params.py backend/tests/unit/test_agent_service.py -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v --tb=short` |
| **Coverage command** | `uv run pytest backend/tests/unit/test_stall_detector.py backend/tests/unit/test_pre_submit_guard.py backend/tests/unit/test_task_progress_tracker.py backend/tests/unit/test_monitored_agent.py backend/tests/unit/test_enhanced_prompt.py backend/tests/unit/test_agent_params.py backend/tests/unit/test_agent_service.py --cov=backend/agent/monitored_agent --cov=backend/agent/stall_detector --cov=backend/agent/pre_submit_guard --cov=backend/agent/task_progress_tracker --cov=backend/agent/prompts --cov=backend/core/agent_service --cov-report=term-missing` |
| **Estimated runtime** | ~15 seconds (unit) / ~30 seconds (full) |

---

## Sampling Rate

- **After every task commit:** Run quick run command (7 target test files)
- **After every plan wave:** Run full suite command
- **Before `/gsd:verify-work`:** Full suite + coverage report must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 51-01-01 | 01 | 1 | VAL-01 | unit | `uv run pytest backend/tests/ -v --tb=short` | ✅ | ⬜ pending |
| 51-01-02 | 01 | 1 | VAL-01 | coverage | `uv run pytest ... --cov=... --cov-report=term-missing` | ✅ | ⬜ pending |
| 51-02-01 | 02 | 2 | VAL-02 | manual | E2E ERP test execution | N/A | ⬜ pending |
| 51-02-02 | 02 | 2 | VAL-03 | manual | per-run log inspection | N/A | ⬜ pending |
| 51-02-03 | 02 | 2 | VAL-04 | manual | PreSubmitGuard log inspection | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements. 60 unit tests already exist across 7 test files. No new test stubs needed.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| ERP 销售出库 Agent 不重复失败超过 2 次 | VAL-02 | 需要真实 ERP 环境和浏览器交互 | 通过平台 UI 创建销售出库测试任务，执行后观察 Agent 行为和 per-run 日志 |
| per-run 日志包含 category="monitor" 条目 | VAL-03 | 需要完整运行管道触发日志写入 | 执行测试后检查 outputs/ 目录下 JSONL 日志文件 |
| PreSubmitGuard 拦截记录存在 | VAL-04 | 需要真实表单提交场景 | 检查 per-run 日志中 PreSubmitGuard.check() 调用记录 |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (none needed)
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
