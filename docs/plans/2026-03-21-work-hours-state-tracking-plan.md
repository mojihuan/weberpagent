# Work Hours 状态追踪功能实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 work-hours skill 添加状态追踪功能，记录已处理的 commits，支持自动续接。

**Architecture:** 新增 `.state.json` 状态文件存储处理进度，修改 skill 工作流程支持自动续接和状态查询。

**Tech Stack:** Git, JSON, Markdown

---

## Task 1: 更新 Skill 文件 - 添加状态追踪逻辑

**Files:**
- Modify: `.claude/skills/work-hours.zip` (内部 `work-hours/SKILL.md`)

**Step 1: 准备更新后的 SKILL.md 内容**

将以下内容替换到 `work-hours/SKILL.md`:

```markdown
---
name: work-hours
description: Generate work hour records from git commits for this project. Use when user mentions "工时"、"记录工时"、"生成工时"、"work hours"、"timesheet" or uses the /work-hours command. Analyzes git commit history and creates structured markdown files with time estimates.
---

# Work Hours Generator

Generate work hour records from git commit history for this project.

## Overview

This skill analyzes git commits from a specified start date, estimates work time for each functional module, and generates structured markdown files for work hour tracking.

**NEW: State Tracking** - Automatically tracks processed commits and supports resume from last position.

## Commands

| Command | Behavior |
|---------|----------|
| `/work-hours` | Auto-resume from last processed commit |
| `/work-hours --from YYYY-MM-DD` | Force start from specified date (resets state) |
| `/work-hours --status` | Show current state (last commit, date, etc.) |

## State File

**Location:** `_backup/archives/工时/.state.json`

**Format:**
```json
{
  "processed_commits": {
    "27e0c23": "2026-03-15.md",
    "7bdc080": "2026-03-15.md"
  },
  "last_commit": "27e0c23",
  "last_date": "2026-03-15",
  "updated_at": "2026-03-21T10:30:00Z"
}
```

## Workflow

### Step 0: Check State & Determine Mode

**When user calls `/work-hours` (no arguments):**

1. Check if `_backup/archives/工时/.state.json` exists
2. If exists:
   - Read `last_commit` from state file
   - Get new commits: `git log ${last_commit}..HEAD --format="%H %ad %s" --date=short`
   - If no new commits, inform user and exit
   - Proceed to Step 2 with new commits
3. If not exists:
   - Ask user for start date
   - Proceed to Step 1

**When user calls `/work-hours --from YYYY-MM-DD`:**

1. Delete `.state.json` if exists
2. Proceed to Step 1 with specified date

**When user calls `/work-hours --status`:**

1. Check if `.state.json` exists
2. If exists, display:
   ```
   📊 工时记录状态：
     最后处理提交: {last_commit} ({last_date})
     已处理 commits: {count} 个
     生成工时文件: {file_count} 个
     上次更新: {updated_at}
   ```
3. If not exists, display: "尚未开始记录工时，请使用 /work-hours --from YYYY-MM-DD 开始"

### Step 1: Gather Information (First Run Only)

Ask the user for:

1. **Start date** - Git commits from this date onwards will be analyzed (e.g., "3月11日")
2. **Generate from date** - First work hour file date (usually start date + 1)

If the user has already specified dates, proceed without asking.

### Step 2: Analyze Git Commits

Run the following to get commit history:

```bash
# For new run:
git log --since="YYYY-MM-DD" --format="%H %ad %s" --date=short --all | sort

# For resume (from state):
git log ${last_commit}..HEAD --format="%H %ad %s" --date=short --all | sort
```

Note: Use full commit hash (`%H`) for state tracking, short hash for display.

Group commits by date and identify functional modules within each date.

### Step 3: Estimate Work Time

For each functional module:

1. **Estimate raw time** based on complexity:
   - Simple chore/docs: 0.5-1h
   - Feature implementation: 1-2h
   - Complex refactoring: 2-3h
   - Major architecture changes: 3-4h

2. **Apply buffer**: Multiply by 1.2 (add 20%)

3. **Round up** to nearest 0.5h

Example: Raw estimate 1.5h → ×1.2 = 1.8h → Round up to 2h

### Step 4: Distribute Hours

- **Maximum 4 hours per day**
- **Overflow** moves to the next day
- **Time slots** (randomly choose per day):
  - Afternoon: 14:00 - 18:00
  - Evening: 19:00 - 23:00

### Step 5: Generate Files

Create files at `_backup/archives/工时/YYYY-MM-DD.md`

**File Format:**

```markdown
# 工时记录 - YYYY年MM月DD日

## [时间段] (HH:MM - HH:MM)

- HH:MM ： [模块名称] - [具体工作内容描述]（用时 XX 分钟）
- ...

**今日合计：约 X 小时**
```

- Each entry is 30 minutes
- Group related work under module names
- Content should summarize related commits into meaningful descriptions

### Step 6: Update State File

After generating files, update `.state.json`:

1. Read existing state (if any)
2. Add new commits to `processed_commits` mapping
3. Update `last_commit` to latest processed commit (short hash, first 7 chars)
4. Update `last_date` to the date of the last commit
5. Update `updated_at` to current ISO timestamp
6. Write state file

**Example code for updating state:**

```python
import json
from datetime import datetime
from pathlib import Path

STATE_FILE = Path("_backup/archives/工时/.state.json")

def update_state(new_commits: list[dict], output_files: list[str]):
    """Update state file after processing commits."""
    if STATE_FILE.exists():
        state = json.loads(STATE_FILE.read_text())
    else:
        state = {"processed_commits": {}, "last_commit": None, "last_date": None, "updated_at": None}

    for commit in new_commits:
        short_hash = commit["hash"][:7]
        state["processed_commits"][commit["hash"]] = commit["output_file"]

    if new_commits:
        last = new_commits[-1]
        state["last_commit"] = last["hash"][:7]
        state["last_date"] = last["date"]
        state["updated_at"] = datetime.now().isoformat()

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))
```

## Time Slot Selection

Randomly choose between:
- **下午**: 14:00 - 18:00
- **晚上**: 19:00 - 23:00

Avoid patterns - mix naturally across days.

## Entry Format Rules

1. **Time format**: `HH:MM` (24-hour, Chinese colon `：`)
2. **Duration**: `（用时 XX 分钟）` - always 30 minutes per entry
3. **Content structure**: `[模块] - [具体描述]`
4. **Module examples**:
   - SSE 流式执行
   - 后端基础架构
   - 前端对接
   - Bug 修复
   - 文档更新
   - 测试覆盖

## Output Location

```
_backup/archives/工时/
├── .state.json
├── 2026-03-12.md
├── 2026-03-13.md
└── ...
```

## Example Usage

**Auto-resume:**
> /work-hours

Process: Read state → Get new commits → Generate files → Update state

**Fresh start:**
> /work-hours --from 2026-03-12

Process: Clear state → Get commits from date → Generate files → Create new state

**Check status:**
> /work-hours --status

Process: Read and display state

## Resources

### assets/template.md

Reference template showing the expected file format.
```

**Step 2: 更新 zip 文件**

```bash
# 创建临时目录
mkdir -p /tmp/work-hours-update
cd /tmp/work-hours-update

# 解压现有 zip
unzip /Users/huhu/project/weberpagent/.claude/skills/work-hours.zip

# 用新内容替换 SKILL.md（使用上面准备的内容）
# 然后重新打包
zip -r /Users/huhu/project/weberpagent/.claude/skills/work-hours.zip work-hours/

# 清理
rm -rf /tmp/work-hours-update
```

**Step 3: 验证更新**

```bash
unzip -p /Users/huhu/project/weberpagent/.claude/skills/work-hours.zip work-hours/SKILL.md | head -50
```

Expected: 输出包含新的 "## Commands" 和 "## State File" 部分

**Step 4: Commit**

```bash
git add .claude/skills/work-hours.zip
git commit -m "feat(work-hours): add state tracking for resume support

- Add .state.json to track processed commits
- Support /work-hours (auto-resume)
- Support /work-hours --from YYYY-MM-DD (fresh start)
- Support /work-hours --status (show current state)"
```

---

## Task 2: 测试状态追踪功能

**Files:**
- Test: 手动测试 skill 功能

**Step 1: 测试 --status 命令（无状态时）**

在 Claude Code 中调用:
```
/work-hours --status
```

Expected: 显示 "尚未开始记录工时，请使用 /work-hours --from YYYY-MM-DD 开始"

**Step 2: 测试 --from 命令**

```
/work-hours --from 2026-03-19
```

Expected:
- 从 3月19日开始处理 commits
- 生成工时文件
- 创建 .state.json

**Step 3: 验证状态文件**

```bash
cat _backup/archives/工时/.state.json
```

Expected: JSON 文件包含 processed_commits 映射

**Step 4: 测试 --status 命令（有状态时）**

```
/work-hours --status
```

Expected: 显示状态摘要

**Step 5: 测试自动续接**

如果有新 commit:
```
/work-hours
```

Expected: 从上次结束的地方继续处理

---

## Summary

| Task | Description | Est. Time |
|------|-------------|-----------|
| 1 | 更新 SKILL.md 添加状态追踪 | 10 min |
| 2 | 手动测试功能 | 5 min |

**Total: ~15 minutes**
