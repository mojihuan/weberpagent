---
phase: 52
slug: prompt
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-30
---

# Phase 52 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (existing) |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest backend/tests/unit/test_enhanced_prompt.py -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_enhanced_prompt.py -v`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 52-01-01 | 01 | 1 | KB-01, KB-02, KB-03 | unit | `uv run pytest backend/tests/unit/test_enhanced_prompt.py -v -k keyboard` | ❌ W0 | ⬜ pending |
| 52-02-01 | 02 | 2 | KB-01, KB-02, KB-03 | manual | ERP 场景手动验证 | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_enhanced_prompt.py` — stubs for keyboard operation keywords (send_keys, Enter, Escape, Control+a)

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Agent 在 ERP 采购单场景中执行 send_keys('Enter') | KB-02 | 需要 ERP 运行环境 + LLM 调用 | 通过前端创建测试用例，执行并观察 Agent 是否按 Enter 触发搜索 |
| Agent 执行 send_keys('Escape') 关闭日期选择器 | KB-03 | 需要 ERP 运行环境 + LLM 调用 | 通过前端创建测试用例，执行并观察 Agent 是否按 ESC 关闭弹窗 |
| Agent 执行 send_keys('Control+a') + 覆盖输入 | KB-01 | 需要 ERP 运行环境 + LLM 调用 | 通过前端创建测试用例，执行并观察 Agent 是否全选后覆盖输入 |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
