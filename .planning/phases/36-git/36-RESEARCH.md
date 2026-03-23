# Phase 36: Git 仓库迁移 - Research

**Researched:** 2026-03-23
**Domain:** Git 仓库迁移、外部模块集成
**Confidence:** HIGH

## Summary

本阶段研究将 weberpagent 项目从当前的 GitHub 仓库迁移到用户自己的 Git 仓库，并将外部的 webseleniumerp 项目作为子目录集成到项目中。

**核心发现:**
1. **当前配置**: weberpagent 的 git remote 指向 `https://github.com/mojihuan/weberpagent.git`
2. **外部依赖**: webseleniumerp 位于 `/Users/huhu/project/webseleniumerp`，通过 `WEBSERP_PATH` 环境变量引用
3. **引用方式**: 项目通过 `sys.path` 动态导入 webseleniumerp 的模块，不是 Python 包依赖
4. **敏感文件**: webseleniumerp 的 `config/settings.py` 在 `.gitignore` 中，包含敏感配置

**Primary recommendation:** 使用 `git remote set-url` 替换远程仓库地址，将 webseleniumerp 复制到项目根目录，并更新 `WEBSERP_PATH` 配置为相对路径。

---

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| GIT-01 | 将 weberpagent 项目 git remote 替换为用户自己的仓库 | 使用 `git remote set-url origin <new-url>` 命令，验证 `git remote -v` |
| GIT-02 | 将 webseleniumerp 复制到项目中，作为一个项目上传 | 复制目录、处理 `.gitignore`、更新 `WEBSERP_PATH` 配置 |

</phase_requirements>

---

## Standard Stack

### Core Commands

| 命令 | 用途 | 说明 |
|------|------|------|
| `git remote set-url origin <url>` | 替换远程仓库地址 | 保留本地 git 历史 |
| `git remote -v` | 验证远程仓库配置 | 确认迁移成功 |
| `cp -r` | 复制 webseleniumerp 目录 | 保留文件结构 |

### Supporting

| 工具 | 用途 | 何时使用 |
|------|------|----------|
| `rsync -av --exclude='.git'` | 复制时排除 git 历史 | 如需清除 webseleniumerp 的 git 历史 |
| `git subtree` | 将外部项目作为子目录合并 | 进阶方案，保留外部项目更新能力 |

### Alternatives Considered

| 标准方案 | 替代方案 | 权衡 |
|----------|----------|------|
| `git remote set-url` | 删除 `.git` 重新初始化 | 重新初始化会丢失历史，不推荐 |
| 直接复制目录 | `git submodule` | submodule 增加复杂度，用户需要单独管理 |
| 直接复制目录 | `git subtree` | subtree 更复杂，适合需要同步上游更新的场景 |

---

## Architecture Patterns

### 当前项目结构

```
/Users/huhu/project/
├── weberpagent/           # 主项目 (git remote: github.com/mojihuan/weberpagent.git)
│   ├── backend/
│   ├── frontend/
│   ├── .env               # WEBSERP_PATH=/Users/huhu/project/webseleniumerp
│   └── pyproject.toml
│
└── webseleniumerp/        # 外部依赖项目 (git remote: gitee.com/ouyangjuns/webseleniumerp.git)
    ├── common/            # 核心模块 (base_prerequisites.py, base_params.py, etc.)
    ├── config/
    │   └── settings.py    # 敏感配置 (在 .gitignore 中)
    └── pages/
```

### 迁移后目标结构

```
weberpagent/               # 主项目 (git remote: 用户的新仓库)
├── backend/
├── frontend/
├── webseleniumerp/        # 集成的外部模块
│   ├── common/
│   ├── config/
│   └── pages/
├── .env                   # WEBSERP_PATH=./webseleniumerp (相对路径)
└── pyproject.toml
```

### Pattern 1: Git Remote 替换

**What:** 使用 `git remote set-url` 命令替换远程仓库地址

**When to use:** 当需要将现有项目迁移到新仓库，同时保留完整 git 历史时

**Example:**
```bash
# 查看当前 remote
git remote -v
# origin  https://github.com/mojihuan/weberpagent.git (fetch)
# origin  https://github.com/mojihuan/weberpagent.git (push)

# 替换为用户的新仓库
git remote set-url origin https://github.com/username/new-repo.git
# 或使用 SSH
git remote set-url origin git@github.com:username/new-repo.git

# 验证
git remote -v
# origin  https://github.com/username/new-repo.git (fetch)
# origin  https://github.com/username/new-repo.git (push)

# 推送到新仓库
git push -u origin main
```

### Pattern 2: 外部模块集成

**What:** 将外部项目复制到主项目目录中，作为子目录管理

**When to use:** 当外部项目是硬编码依赖，无法通过 pip 安装时

**Example:**
```bash
# 复制 webseleniumerp 到项目中 (排除 .git 目录)
rsync -av --exclude='.git' /Users/huhu/project/webseleniumerp/ ./webseleniumerp/

# 或者简单复制 (之后手动删除 .git)
cp -r /Users/huhu/project/webseleniumerp ./

# 更新 .env 配置
# WEBSERP_PATH=/Users/huhu/project/webseleniumerp
# 改为
# WEBSERP_PATH=./webseleniumerp
```

### Anti-Patterns to Avoid

- **直接复制 `.git` 目录**: 会导致嵌套 git 仓库，引起混淆
- **忽略 `.gitignore` 规则**: webseleniumerp 的 `config/settings.py` 包含敏感信息，必须保持被忽略
- **使用绝对路径**: 迁移后 `WEBSERP_PATH` 应使用相对路径，确保跨环境兼容

---

## Don't Hand-Roll

| 问题 | 不要构建 | 使用 | 原因 |
|------|----------|------|------|
| 替换 git remote | 手动编辑 `.git/config` | `git remote set-url` | 命令更安全，自动验证格式 |
| 复制目录 | 自定义脚本 | `cp -r` 或 `rsync` | 成熟工具，处理边界情况 |
| 忽略敏感文件 | 手动管理 | `.gitignore` | 标准机制，团队一致理解 |

**Key insight:** Git 仓库迁移是标准操作，使用内置命令比自定义脚本更可靠。

---

## Common Pitfalls

### Pitfall 1: 嵌套 Git 仓库

**What goes wrong:** 复制 webseleniumerp 时保留了 `.git` 目录，导致主项目无法正确追踪子目录文件

**Why it happens:** 直接使用 `cp -r` 会复制所有文件包括隐藏的 `.git` 目录

**How to avoid:**
```bash
# 方案 1: 使用 rsync 排除
rsync -av --exclude='.git' /path/to/webseleniumerp/ ./webseleniumerp/

# 方案 2: 复制后删除
cp -r /path/to/webseleniumerp ./
rm -rf ./webseleniumerp/.git
```

**Warning signs:** `git status` 显示 `webseleniumerp/` 为 untracked 但无法 add

### Pitfall 2: 敏感配置泄露

**What goes wrong:** `config/settings.py` (包含 ERP 密码等) 被提交到公开仓库

**Why it happens:** 复制目录时可能覆盖或忽略 `.gitignore` 规则

**How to avoid:**
1. 确保 webseleniumerp 的 `.gitignore` 包含 `config/settings.py`
2. 在主项目 `.gitignore` 中也添加 `webseleniumerp/config/settings.py`
3. 复制后检查: `git check-ignore webseleniumerp/config/settings.py`

**Warning signs:** `git status` 显示 settings.py 为待提交文件

### Pitfall 3: WEBSERP_PATH 路径问题

**What goes wrong:** 迁移后代码无法找到 webseleniumerp 模块

**Why it happens:** `.env` 中的 `WEBSERP_PATH` 仍指向原绝对路径

**How to avoid:**
1. 更新 `.env.example` 中的注释说明
2. 使用相对路径: `WEBSERP_PATH=./webseleniumerp`
3. 或使用相对于项目根目录的路径

**Warning signs:** API 返回 "WEBSERP_PATH does not exist" 错误

### Pitfall 4: 未推送到新仓库

**What goes wrong:** 本地 remote 已更新，但代码仍在旧仓库

**Why it happens:** 只执行了 `set-url`，没有推送

**How to avoid:**
```bash
# 完整流程
git remote set-url origin <new-url>
git push -u origin main  # 必须执行推送
```

**Warning signs:** 新仓库为空，或与本地不同步

---

## Code Examples

### 完整迁移脚本示例

```bash
#!/bin/bash
# migrate-repo.sh - Git 仓库迁移脚本

set -e

# 配置变量 (用户需要修改)
NEW_REPO_URL="${1:-git@github.com:username/weberpagent.git}"
WEBSERP_SOURCE="/Users/huhu/project/webseleniumerp"

echo "=== Git 仓库迁移 ==="
echo "目标仓库: $NEW_REPO_URL"
echo ""

# 1. 替换 git remote
echo "[1/4] 更新 git remote..."
git remote set-url origin "$NEW_REPO_URL"
git remote -v

# 2. 复制 webseleniumerp
echo "[2/4] 复制 webseleniumerp..."
if [ -d "webseleniumerp" ]; then
    echo "webseleniumerp 目录已存在，跳过复制"
else
    rsync -av --exclude='.git' "$WEBSERP_SOURCE/" ./webseleniumerp/
fi

# 3. 更新 .gitignore (确保敏感文件被忽略)
echo "[3/4] 更新 .gitignore..."
if ! grep -q "webseleniumerp/config/settings.py" .gitignore 2>/dev/null; then
    echo "" >> .gitignore
    echo "# webseleniumerp sensitive files" >> .gitignore
    echo "webseleniumerp/config/settings.py" >> .gitignore
fi

# 4. 提示用户更新 .env
echo "[4/4] 请手动更新 .env 文件:"
echo "  WEBSERP_PATH=./webseleniumerp"
echo ""
echo "=== 迁移完成 ==="
echo "下一步: git add . && git commit -m 'chore: migrate to new repo' && git push -u origin main"
```

### 验证迁移成功

```bash
# 验证 git remote
git remote -v

# 验证 webseleniumerp 存在
ls -la webseleniumerp/common/base_prerequisites.py

# 验证敏感文件被忽略
git check-ignore webseleniumerp/config/settings.py && echo "OK: settings.py 被正确忽略"

# 验证没有嵌套 git
test ! -d webseleniumerp/.git && echo "OK: 没有嵌套 .git 目录"

# 启动服务验证引用正常
uv run uvicorn backend.api.main:app --reload --port 8080
```

---

## State of the Art

| 旧方法 | 当前方法 | 变化时间 | 影响 |
|--------|----------|----------|------|
| 手动编辑 `.git/config` | `git remote set-url` | Git 1.7+ | 更安全，有验证 |
| `git submodule` | 直接复制目录 | 项目特定 | 简化部署，但失去同步能力 |

**Deprecated/outdated:**
- `git remote rm` + `git remote add`: 现在直接用 `set-url` 更简洁

---

## Open Questions

1. **用户的新仓库地址是什么？**
   - What we know: 需要替换当前 `github.com/mojihuan/weberpagent.git`
   - What's unclear: 用户尚未提供新仓库 URL
   - Recommendation: 在执行阶段询问用户，或作为变量在脚本中处理

2. **是否需要保留 webseleniumerp 的 git 历史？**
   - What we know: 当前方案是复制文件，不保留历史
   - What's unclear: 用户是否有后续同步需求
   - Recommendation: 如需同步上游更新，考虑使用 `git subtree`

3. **webseleniumerp 的 config/settings.py 如何处理？**
   - What we know: 文件在 `.gitignore` 中，包含敏感配置
   - What's unclear: 用户是否有模板文件或创建指南
   - Recommendation: 复制 `.gitignore` 规则，提供创建指南

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 8.0+ (via pyproject.toml) |
| Config file | pyproject.toml `[tool.pytest.ini_options]` |
| Quick run command | `uv run pytest backend/tests/ -x -q` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| GIT-01 | git remote 显示新仓库地址 | manual | `git remote -v` | N/A |
| GIT-02 | webseleniumerp 目录存在 | manual | `ls webseleniumerp/` | N/A |
| GIT-02 | 代码可正常引用 webseleniumerp | integration | `uv run pytest backend/tests/unit/test_external_bridge.py -v` | Yes |

### Sampling Rate

- **Per task commit:** 无自动化测试 (git 配置变更)
- **Per wave merge:** 手动验证 `git remote -v` 和目录结构
- **Phase gate:** 启动服务验证 API 可访问外部模块

### Wave 0 Gaps

- [ ] 手动验证步骤清单 (非自动化测试)
- [ ] 用户需提供新仓库 URL

**注意:** 本阶段主要是 Git 配置和文件操作，不适合自动化测试。验证主要依赖手动检查和集成测试。

---

## Sources

### Primary (HIGH confidence)

- Git 官方文档 - `git remote` 命令
- 项目代码分析 - `backend/core/external_precondition_bridge.py` (引用方式)
- 项目配置文件 - `.env`, `pyproject.toml`, `.gitignore`

### Secondary (MEDIUM confidence)

- 项目状态文件 - `.planning/STATE.md`, `.planning/REQUIREMENTS.md`

### Tertiary (LOW confidence)

- 无

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Git 命令是标准工具，文档完善
- Architecture: HIGH - 已分析现有代码引用方式
- Pitfalls: HIGH - 常见 Git 迁移问题，有明确解决方案

**Research date:** 2026-03-23
**Valid until:** 30 days (Git 命令稳定)

---

## Appendix: Current Configuration Snapshot

### weberpagent Git 配置
```
origin  https://github.com/mojihuan/weberpagent.git (fetch)
origin  https://github.com/mojihuan/weberpagent.git (push)
Branch: main
```

### webseleniumerp Git 配置
```
origin  git@gitee.com:ouyangjuns/webseleniumerp.git (fetch)
origin  git@gitee.com:ouyangjuns/webseleniumerp.git (push)
Branch: master
Size: 907M
```

### 当前 WEBSERP_PATH 配置
```
WEBSERP_PATH=/Users/huhu/project/webseleniumerp
```

### 关键引用文件
- `backend/core/external_precondition_bridge.py` - 动态导入 webseleniumerp 模块
- `backend/config/settings.py` - 读取 WEBSERP_PATH 环境变量
- `backend/config/validators.py` - 验证 WEBSERP_PATH 路径有效性
