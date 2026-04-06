---
phase: 65
slug: 差距关联分析
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-06
---

# Phase 65 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | 纯分析阶段 — 无代码修改，无需测试框架 |
| **Config file** | none — 分析报告阶段 |
| **Quick run command** | `grep -c "判定" .planning/phases/65-差距关联分析/65-ANALYSIS-REPORT.md` |
| **Full suite command** | 手动审查报告结构与判定完整性 |
| **Estimated runtime** | ~1 秒 |

---

## Sampling Rate

- **After every task commit:** 验证报告文件包含本任务对应的分析判定
- **After every plan wave:** 验证三项分析（ANALYSIS-01/02/03）均有明确判定
- **Before `/gsd:verify-work`:** 报告完整，三项判定均有因果判定和证据链
- **Max feedback latency:** 1 秒

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 65-01-01 | 01 | 1 | ANALYSIS-01 | 报告审查 | `grep "因果判定" 65-ANALYSIS-REPORT.md` | ⬜ pending | ⬜ pending |
| 65-01-02 | 01 | 1 | ANALYSIS-02 | 报告审查 | `grep "DOM Patch" 65-ANALYSIS-REPORT.md` | ⬜ pending | ⬜ pending |
| 65-01-03 | 01 | 1 | ANALYSIS-03 | 报告审查 | `grep "Section 9" 65-ANALYSIS-REPORT.md` | ⬜ pending | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] 无 — 纯分析阶段，无代码修改，无需测试基础设施

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 因果判定合理性 | ANALYSIS-01 | 需要技术判断，无法自动化 | 检查三层证据链（代码推理+已知行为+补丁效果）是否逻辑自洽 |
| DOM Patch 逐 patch 判定 | ANALYSIS-02 | 需要逐一验证5个patch的必要性评估 | 检查每个patch是否有明确判定（仍必要/冗余/部分必要/冲突） |
| Prompt 有效性评估 | ANALYSIS-03 | 需要判断click-to-edit指导的适用性 | 检查Section 9评估是否给出保留/调整/移除的明确建议 |

---

## Validation Sign-Off

- [ ] All tasks have verification criteria defined
- [ ] Sampling continuity: 报告文件包含所有三项分析的判定
- [ ] Wave 0 covers all MISSING references — 无需
- [ ] No watch-mode flags
- [ ] Feedback latency < 1s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
