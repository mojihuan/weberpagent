# 项目结构整理实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将项目根目录中非核心内容移入 backup 文件夹，清理项目结构。

**Architecture:** 使用 git mv 移动文件保留历史，然后 git rm --cached 停止跟踪 backup 文件夹，最后更新 .gitignore。

**Tech Stack:** Git, Bash

---

## Task 1: 创建 backup 目录结构

**Files:**
- Create: `backup/archives/`
- Create: `backup/runtime-data/`
- Create: `backup/temp/`

**Step 1: 创建目录结构**

```bash
mkdir -p backup/archives backup/runtime-data backup/temp
```

**Step 2: 验证目录创建成功**

Run: `ls -la backup/`
Expected: 看到 archives、runtime-data、temp 三个目录

---

## Task 2: 移动 archives 内容

**Files:**
- Move: `工时/` → `backup/archives/工时/`
- Move: `测试案例/` → `backup/archives/测试案例/`
- Move: `jianzhi_ui_test.egg-info/` → `backup/archives/jianzhi_ui_test.egg-info/`

**Step 1: 移动工时文件夹**

```bash
git mv 工时 backup/archives/工时
```

**Step 2: 移动测试案例文件夹**

```bash
git mv 测试案例 backup/archives/测试案例
```

**Step 3: 移动 egg-info 文件夹**

```bash
git mv jianzhi_ui_test.egg-info backup/archives/jianzhi_ui_test.egg-info
```

**Step 4: 验证移动成功**

Run: `ls backup/archives/`
Expected: 看到 工时、测试案例、jianzhi_ui_test.egg-info

---

## Task 3: 移动已归档代码

**Files:**
- Move: `backend/_archived/` → `backup/archives/backend_archived/`
- Move: `docs/_archived/` → `backup/archives/docs_archived/`

**Step 1: 移动 backend/_archived**

```bash
git mv backend/_archived backup/archives/backend_archived
```

**Step 2: 移动 docs/_archived**

```bash
git mv docs/_archived backup/archives/docs_archived
```

**Step 3: 验证移动成功**

Run: `ls backup/archives/`
Expected: 看到 backend_archived、docs_archived

---

## Task 4: 移动运行时数据

**Files:**
- Move: `outputs/` → `backup/runtime-data/outputs/`
- Move: `data/` → `backup/runtime-data/data/`

**Step 1: 移动 outputs 文件夹**

```bash
git mv outputs backup/runtime-data/outputs
```

**Step 2: 移动 data 文件夹**

```bash
git mv data backup/runtime-data/data
```

**Step 3: 验证移动成功**

Run: `ls backup/runtime-data/`
Expected: 看到 outputs、data

---

## Task 5: 移动临时文件

**Files:**
- Move: `debug_memoryview_error.py` → `backup/temp/`
- Move: `test_backend_env.py` → `backup/temp/`
- Move: `login.log` → `backup/temp/`
- Move: `.pytest_cache/` → `backup/temp/.pytest_cache/`

**Step 1: 移动调试文件**

```bash
git mv debug_memoryview_error.py backup/temp/
git mv test_backend_env.py backup/temp/
git mv login.log backup/temp/
```

**Step 2: 移动 pytest 缓存**

```bash
git mv .pytest_cache backup/temp/.pytest_cache
```

**Step 3: 验证移动成功**

Run: `ls backup/temp/`
Expected: 看到 debug_memoryview_error.py、test_backend_env.py、login.log、.pytest_cache

---

## Task 6: 停止跟踪 backup 文件夹

**Files:**
- Modify: `.gitignore`

**Step 1: 从 git 索引移除 backup 文件夹**

```bash
git rm --cached -r backup
```

**Step 2: 更新 .gitignore**

在 `.gitignore` 文件末尾添加：

```
# Backup folder
backup/
```

**Step 3: 验证 git 状态**

Run: `git status`
Expected: backup 文件夹不再被跟踪，.gitignore 显示为 modified

---

## Task 7: 提交更改

**Step 1: 添加 .gitignore 更改**

```bash
git add .gitignore
```

**Step 2: 提交所有更改**

```bash
git commit -m "chore: 整理项目结构，非核心内容移入 backup

- 移动工时、测试案例、egg-info 到 backup/archives/
- 移动 backend/_archived、docs/_archived 到 backup/archives/
- 移动 outputs、data 到 backup/runtime-data/
- 移动临时文件到 backup/temp/
- backup/ 已添加到 .gitignore

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Step 3: 验证提交成功**

Run: `git log -1 --oneline`
Expected: 看到新的提交记录

---

## Task 8: 验证最终结构

**Step 1: 验证根目录结构**

Run: `ls -la`
Expected: 只看到 backend、frontend、docs、.playwright-mcp、.claude、配置文件等

**Step 2: 验证 backup 结构**

Run: `tree backup -L 2` 或 `find backup -type d | head -20`
Expected: backup/archives、backup/runtime-data、backup/temp 结构正确

**Step 3: 验证 git 忽略生效**

Run: `git status --ignored | grep backup`
Expected: backup/ 显示在 ignored 列表中

---

## 完成检查

- [ ] 根目录整洁，只有核心代码和配置
- [ ] backup 文件夹结构正确（archives/runtime-data/temp）
- [ ] .gitignore 包含 backup/
- [ ] git status 显示 backup 被忽略
- [ ] 提交记录完整
