---
phase: 35
slug: 文档完善
status: draft
nyquist_compliant: false
wave_0_complete: true
created: 2026-03-23
---

# Phase 35 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | 文档验证（无代码测试框架） |
| **Config file** | none |
| **Quick run command** | `ls docs/断言系统使用指南.md && head -100 docs/断言系统使用指南.md` |
| **Full suite command** | `cat docs/断言系统使用指南.md` |
| **Estimated runtime** | ~1 秒 |

---

## Sampling Rate

- **After every task commit:** 确认文件存在且格式正确
- **After every plan wave:** 完整阅读文档内容验证
- **Before `/gsd:verify-work`:** 文档完整性检查
- **Max feedback latency:** 1 秒

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 35-01-01 | 01 | 1 | DOC-01 | file-check | `test -f docs/断言系统使用指南.md` | ❌ W0 | ⬜ pending |
| 35-01-02 | 01 | 1 | DOC-01 | content-check | `grep -q "三层参数" docs/断言系统使用指南.md` | ❌ W0 | ⬜ pending |
| 35-01-03 | 01 | 1 | DOC-02 | content-check | `grep -q "## FAQ" docs/断言系统使用指南.md` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements.*

此阶段为纯文档创建，无代码修改，无需安装测试框架。

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 文档可读性 | DOC-01 | 需人工判断 | 阅读 `docs/断言系统使用指南.md`，确认结构清晰 |
| 示例准确性 | DOC-01 | 需与代码对照 | 检查示例参数与 `external_precondition_bridge.py` 一致 |
| FAQ 实用性 | DOC-02 | 需用户反馈 | 检查问题覆盖常见错误场景 |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: 文档任务使用文件检查
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 1s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
