# Work Hours 智能状态追踪 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 修复 work-hours skill 状态追踪 bug，添加智能检测逻辑确保从正确位置续接。

**Architecture:** 在状态文件增加 `last_generated_date` 字段，启动时同时检测状态文件和已有工时文件，取较晚日期作为起始点。

**Tech Stack:** Markdown skill 文件，无代码修改

---

## Task 1: 更新状态文件格式说明

**Files:**
- Modify: `.claude/skills/work-hours.zip` → `work-hours/SKILL.md` (State File 部分)

**Step 1: 提取并编辑 SKILL.md**

```bash
cd /Users/huhu/project/weberpagent
unzip -o .claude/skills/work-hours.zip -d /tmp/work-hours-skill/
```

**Step 2: 更新状态文件格式**

在 `## State File` 部分的 JSON 示例中，添加 `last_generated_date` 字段：

```json
{
  "processed_commits": {
    "27e0c23": "2026-03-15.md",
    "7bdc080": "2026-03-15.md"
  },
  "last_commit": "27e0c23",
  "last_date": "2026-03-15",
  "last_generated_date": "2026-03-22",
  "updated_at": "2026-03-21T10:30:00Z"
}
```

添加字段说明：
- `last_generated_date`: 工时文件实际生成到的日期（可能晚于 commit 日期，因为每天4小时上限会顺延）

**Step 3: 更新状态文件位置说明**

确保说明状态文件位置：`_backup/archives/工时/.state.json`

---

## Task 2: 更新 Step 0 智能检测逻辑

**Files:**
- Modify: `/tmp/work-hours-skill/work-hours/SKILL.md` (Step 0 部分)

**Step 1: 重写 Step 0 的 "When user calls /work-hours (no arguments)" 部分**

替换为：

```markdown
**When user calls `/work-hours` (no arguments):**

1. 检查状态文件和已有工时文件
2. 智能计算起始日期：
   ```bash
   # 扫描已有工时文件
   ls _backup/archives/工时/*.md | sort | tail -1
   ```
3. 起始日期 = max(
     state.last_generated_date (如果存在),
     最新工时文件日期 (如果存在)
   ) + 1 天
4. 如果起始日期 > 今天：
   - 显示"✅ 工时已是最新，无需生成"
   - 退出
5. 如果状态和文件都不存在：
   - 提示用户使用 `/work-hours --from YYYY-MM-DD` 开始
   - 退出
6. 获取新 commits：
   ```bash
   git log ${last_commit}..HEAD --format="%H %ad %s" --date=short
   ```
7. 如果没有新 commits：
   - 显示"✅ 没有新的提交，无需生成工时"
   - 退出
8. 继续执行 Step 2
```

**Step 2: 添加检测已有文件的代码示例**

```markdown
**检测已有工时文件的 Python 示例：**

```python
from pathlib import Path
import re

def get_latest_generated_date(hours_dir: Path) -> str | None:
    """获取最新工时文件的日期"""
    pattern = re.compile(r"(\d{4}-\d{2}-\d{2})\.md$")
    dates = []
    for f in hours_dir.glob("*.md"):
        match = pattern.search(f.name)
        if match:
            dates.append(match.group(1))
    return max(dates) if dates else None

def calculate_start_date(state: dict, hours_dir: Path) -> str:
    """计算起始日期，取状态和实际文件的较晚者"""
    state_date = state.get("last_generated_date")
    file_date = get_latest_generated_date(hours_dir)

    dates = [d for d in [state_date, file_date] if d]
    if not dates:
        return None  # 需要用户指定

    from datetime import datetime, timedelta
    latest = max(dates)
    next_day = datetime.strptime(latest, "%Y-%m-%d") + timedelta(days=1)
    return next_day.strftime("%Y-%m-%d")
```
```

---

## Task 3: 更新 Step 6 状态更新逻辑

**Files:**
- Modify: `/tmp/work-hours-skill/work-hours/SKILL.md` (Step 6 部分)

**Step 1: 更新 Step 6 的状态更新说明**

修改 Step 6 开头为：

```markdown
### Step 6: Update State File

After generating files, update `.state.json`:

1. Read existing state (if any)
2. Add new commits to `processed_commits` mapping
3. Update `last_commit` to latest processed commit (short hash, first 7 chars)
4. Update `last_date` to the date of the last commit
5. **Update `last_generated_date` to the date of the LAST GENERATED FILE** (not commit date!)
6. Update `updated_at` to current ISO timestamp
7. Write state file
```

**Step 2: 更新 Python 示例代码**

修改 `update_state` 函数：

```python
import json
from datetime import datetime
from pathlib import Path

STATE_FILE = Path("_backup/archives/工时/.state.json")

def update_state(new_commits: list[dict], last_generated_date: str):
    """Update state file after processing commits.

    Args:
        new_commits: List of processed commits with hash, date, output_file
        last_generated_date: Date of the LAST GENERATED work hours file
    """
    if STATE_FILE.exists():
        state = json.loads(STATE_FILE.read_text())
    else:
        state = {
            "processed_commits": {},
            "last_commit": None,
            "last_date": None,
            "last_generated_date": None,
            "updated_at": None
        }

    for commit in new_commits:
        state["processed_commits"][commit["hash"]] = commit["output_file"]

    if new_commits:
        last = new_commits[-1]
        state["last_commit"] = last["hash"][:7]
        state["last_date"] = last["date"]

    # 关键：记录工时文件实际生成到的日期
    state["last_generated_date"] = last_generated_date
    state["updated_at"] = datetime.now().isoformat()

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))
```

---

## Task 4: 打包并验证

**Files:**
- Modify: `.claude/skills/work-hours.zip`

**Step 1: 重新打包 skill**

```bash
cd /tmp/work-hours-skill
zip -r /Users/huhu/project/weberpagent/.claude/skills/work-hours.zip work-hours/
```

**Step 2: 验证打包成功**

```bash
unzip -l /Users/huhu/project/weberpagent/.claude/skills/work-hours.zip
```

Expected: 列出 `work-hours/SKILL.md` 和 `work-hours/assets/template.md`

**Step 3: 清理临时文件**

```bash
rm -rf /tmp/work-hours-skill
```

---

## Task 5: 提交变更

**Step 1: 提交 skill 更新**

```bash
cd /Users/huhu/project/weberpagent
git add .claude/skills/work-hours.zip
git commit -m "fix(work-hours): add smart state tracking with last_generated_date"
```

**Step 2: 清理旧设计文档（可选）**

如果有重复的设计文档，可以删除旧的：
```bash
git rm docs/plans/2026-03-21-work-hours-state-tracking-design.md
git rm docs/plans/2026-03-21-work-hours-state-tracking-plan.md
git commit -m "chore: remove outdated work-hours design docs"
```

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | 更新状态文件格式 | SKILL.md (State File 部分) |
| 2 | 添加智能检测逻辑 | SKILL.md (Step 0 部分) |
| 3 | 更新状态更新逻辑 | SKILL.md (Step 6 部分) |
| 4 | 打包并验证 | work-hours.zip |
| 5 | 提交变更 | git |

**Total estimated time:** 15-20 minutes
