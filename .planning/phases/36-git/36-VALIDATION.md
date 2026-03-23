---
phase: 36
slug: git
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-23
---

# Phase 36 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.0+ (via pyproject.toml) |
| **Config file** | pyproject.toml `[tool.pytest.ini_options]` |
| **Quick run command** | `uv run pytest backend/tests/ -x -q` |
| **Full suite command** | `uv run pytest backend/tests/ -v` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** 手动验证 `git remote -v` 和目录结构
- **After every plan wave:** 启动服务验证 API 可访问外部模块
- **Before `/gsd:verify-work`:** 服务启动正常，webseleniumerp 模块可导入
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 36-01-01 | 01 | 1 | GIT-01 | manual | `git remote -v` | N/A | ⬜ pending |
| 36-01-02 | 01 | 1 | GIT-01 | manual | `git push -u origin main --dry-run` | N/A | ⬜ pending |
| 36-02-01 | 02 | 1 | GIT-02 | manual | `ls -la webseleniumerp/common/` | N/A | ⬜ pending |
| 36-02-02 | 02 | 1 | GIT-02 | manual | `test ! -d webseleniumerp/.git` | N/A | ⬜ pending |
| 36-02-03 | 02 | 1 | GIT-02 | integration | `uv run pytest backend/tests/unit/test_external_bridge.py -v` | ✅ | ⬜ pending |
| 36-02-04 | 02 | 1 | GIT-02 | manual | `git check-ignore webseleniumerp/config/settings.py` | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `backend/tests/unit/test_external_bridge.py` — 已有集成测试
- [x] `backend/tests/conftest.py` — 共享 fixtures

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| git remote 显示新地址 | GIT-01 | Git 配置变更，无法自动化 | `git remote -v` 确认输出包含新仓库 URL |
| webseleniumerp 目录存在 | GIT-02 | 文件系统操作 | `ls webseleniumerp/` 确认目录存在 |
| 无嵌套 .git 目录 | GIT-02 | Git 仓库状态检查 | `test ! -d webseleniumerp/.git` |
| 敏感文件被忽略 | GIT-02 | 安全检查 | `git check-ignore webseleniumerp/config/settings.py` |
| 服务启动正常 | GIT-02 | 集成验证 | `uv run uvicorn backend.api.main:app --port 8080` |

---

## Validation Sign-Off

- [x] All tasks have verification steps (manual or automated)
- [x] Sampling continuity: 验证步骤覆盖所有关键变更
- [x] Wave 0 covers all MISSING references — N/A (现有测试覆盖)
- [x] No watch-mode flags
- [x] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
