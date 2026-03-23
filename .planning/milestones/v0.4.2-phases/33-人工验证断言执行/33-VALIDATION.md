---
phase: 33
slug: 人工验证断言执行
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-22
---

# Phase 33 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Manual UI Verification (Playwright for辅助截图) |
| **Config file** | N/A - Manual verification |
| **Quick run command** | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~15 minutes (manual) |

---

## Sampling Rate

- **After every verification step:** Document findings in VERIFICATION.md
- **Before marking complete:** All 4 Success Criteria must be verified
- **Max feedback latency:** Immediate (manual observation)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 33-01-01 | 01 | 1 | ASSERT-01 | manual | N/A | N/A | ⬜ pending |
| 33-01-02 | 01 | 1 | ASSERT-02 | manual | N/A | N/A | ⬜ pending |
| 33-01-03 | 01 | 1 | ASSERT-03 | manual | N/A | N/A | ⬜ pending |
| 33-01-04 | 01 | 1 | ASSERT-04 | manual | N/A | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] Existing infrastructure covers all phase requirements.
  - Backend: `uv run uvicorn backend.api.main:app --reload --port 8080`
  - Frontend: `cd frontend && npm run dev`
  - Unit tests: `backend/tests/unit/test_external_assertion_bridge.py`

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 前端断言参数配置 | ASSERT-01 | UI 交互验证 | 在 TaskModal 中配置断言参数，验证字段搜索、分组、值输入 |
| 断言执行结果 | ASSERT-02 | 端到端流程 | 执行测试后查看断言被调用，返回 success/passed/fields |
| 报告显示断言结果 | ASSERT-03 | UI 展示验证 | 在 ReportDetail 页面查看断言结果卡片 |
| "now" 时间转换 | ASSERT-04 | 运行时验证 | 验证 saleTime='now' 显示为实际时间字符串 |

---

## Validation Sign-Off

- [x] All tasks have manual verification steps defined
- [x] Sampling continuity: each step has documented verification
- [x] Wave 0 covers all dependencies (existing infrastructure)
- [x] No watch-mode flags needed
- [x] Feedback latency: immediate (manual)
- [ ] `nyquist_compliant: true` set in frontmatter (after verification complete)

**Approval:** pending
