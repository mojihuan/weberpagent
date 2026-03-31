---
phase: 54
slug: import
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-31
---

# Phase 54 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest backend/tests/unit/test_enhanced_prompt.py -x -v` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest backend/tests/unit/test_enhanced_prompt.py -x -v`
- **After every plan wave:** Run `uv run pytest backend/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 54-01-01 | 01 | 1 | IMP-01 | unit | `uv run pytest backend/tests/unit/test_enhanced_prompt.py -x -k file_upload` | ❌ W0 | ⬜ pending |
| 54-01-02 | 01 | 1 | IMP-01 | unit | `uv run pytest backend/tests/unit/test_agent_service.py -x -k scan_test_files` | ❌ W0 | ⬜ pending |
| 54-01-03 | 01 | 1 | D-01/D-02 | unit | `uv run pytest backend/tests/unit/test_agent_service.py -x -k test_files` | ❌ W0 | ⬜ pending |
| 54-02-01 | 02 | 2 | IMP-01 | manual | ERP 采购单 Excel 导入验证 | N/A | ⬜ pending |
| 54-02-02 | 02 | 2 | IMP-02 | manual | ERP 商品图片上传验证 | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/unit/test_enhanced_prompt.py` — add `test_contains_file_upload_keywords` and `test_file_upload_section_line_count`
- [ ] `backend/tests/unit/test_agent_service.py` — add `test_scan_test_files`
- [ ] `data/test-files/` — test asset directory with Excel + image files

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Excel 导入采购单 | IMP-01 | 需要 ERP 运行环境 + 浏览器交互 | 在 ERP 采购单导入页面执行 upload_file，验证文件成功上传 |
| 商品图片上传 | IMP-02 | 需要 ERP 运行环境 + 浏览器交互 | 在 ERP 商品管理页面执行 upload_file 上传图片，验证成功 |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
