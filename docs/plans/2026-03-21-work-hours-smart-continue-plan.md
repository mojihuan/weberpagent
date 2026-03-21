# Work Hours 智能续接实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 修改 work-hours skill，实现自动检测续接点，无需手动指定日期

**Architecture:** 读取 .state.json 中的 last_commit，扫描工时文件夹找最新日期，获取新 commits，从断点续接生成

**Tech Stack:** Markdown skill 文档, Git, JSON 状态文件

---

## Task 1: 重写 SKILL.md 核心逻辑

**Files:**
- Modify: `.claude/skills/work-hours/SKILL.md`

**Step 1: 更新 description 触发词**

在 frontmatter 中更新 description，添加 "续接工时" 等关键词：

```markdown
---
name: work-hours
description: Generate work hour records from git commits. Supports smart continuation - auto-detects last processed commit and continues from there. Use when user mentions "工时"、"记录工时"、"生成工时"、"续接工时"、"work hours"、"timesheet" or uses the /work-hours command.
---
```

**Step 2: 替换 Workflow 部分**

将原有的 Step 1-5 替换为新的智能续接流程：

```markdown
## Workflow

### Phase 1: State Detection (Automatic)

**Step 1: Read state file**

Read `_backup/archives/工时/.state.json` to get:
- `last_commit`: Last processed commit hash
- `last_file_date`: Latest work hour file date

If `.state.json` doesn't exist, ask user for start date manually.

**Step 2: Scan work hour folder**

```bash
ls _backup/archives/工时/*.md | sort | tail -1
```

Find the latest file date (format: `YYYY-MM-DD.md`).

**Step 3: Get new commits**

```bash
git log <last_commit>..HEAD --format="%H %ad %s" --date=short --all | sort
```

Count new commits and identify their date range.

### Phase 2: Preview & Confirm

**Step 4: Display status preview**

Show a status table:

```
📋 工时续接状态
┌────────────────────┬─────────────────────────┐
│ 上次处理commit     │ <short_hash> (<date>)   │
│ 工时文件已到       │ YYYY-MM-DD              │
│ 发现新commits      │ N 个                    │
│ 续接起点           │ YYYY-MM-DD              │
└────────────────────┴─────────────────────────┘

确认继续？ [Y/n]
```

If user declines, exit without changes.

### Phase 3: Generate Work Hours

**Step 5: Analyze and group commits**

Group new commits by functional module:
- SSE 流式执行
- 后端基础架构
- 前端对接
- Bug 修复
- 文档更新
- 测试覆盖
- 断言系统
- E2E测试

**Step 6: Estimate work time**

For each functional module:

1. **Estimate raw time** based on complexity:
   - Simple chore/docs: 0.5-1h
   - Feature implementation: 1-2h
   - Complex refactoring: 2-3h
   - Major architecture changes: 3-4h

2. **Apply buffer**: Multiply by 1.2 (add 20%)

3. **Round up** to nearest 0.5h

Example: Raw estimate 1.5h → ×1.2 = 1.8h → Round up to 2h

**Step 7: Distribute hours**

- **Maximum 4 hours per day**
- **Overflow** moves to the next day
- **Start date**: `last_file_date + 1 day`
- **Time slots** (randomly choose per day):
  - Afternoon: 14:00 - 18:00
  - Evening: 19:00 - 23:00

**Step 8: Generate files**

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

### Phase 4: Update State

**Step 9: Update .state.json**

After successful generation, update the state file:

```json
{
  "last_commit": "<newest_processed_commit_hash>",
  "last_file_date": "<newest_generated_file_date>",
  "generated_files": ["<list of all generated files>"],
  "updated_at": "<ISO timestamp>"
}
```

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No new commits | Display "✅ 无新工作需要记录" and exit |
| .state.json missing | Ask user for start date manually (first-time setup) |
| User cancels | Exit without modifying any files |
| Work hour folder empty | Start from `last_commit` date + 1 |

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
   - 断言系统
   - E2E测试

## Output Location

```
_backup/archives/工时/
├── .state.json
├── 2026-03-12.md
├── 2026-03-13.md
└── ...
```

## Example Usage

**User request:**
> 记录工时

**Process:**
1. Read .state.json → last_commit: a7b4b8d
2. Scan folder → latest file: 2026-03-22
3. Get new commits → 32 commits found
4. Show preview → start from 2026-03-23
5. User confirms → generate files
6. Update .state.json with new state
```

**Step 3: Commit changes**

```bash
git add .claude/skills/work-hours/SKILL.md
git commit -m "$(cat <<'EOF'
feat(work-hours): add smart continuation support

- Auto-detect last processed commit from .state.json
- Scan work hour folder for latest file date
- Preview status before generation
- Continue from breakpoint automatically
- No manual date input required

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: 手动测试验证

**Files:**
- Test: `_backup/archives/工时/` folder

**Step 1: 验证当前状态**

```bash
cat _backup/archives/工时/.state.json
ls _backup/archives/工时/*.md | tail -5
```

Expected: See current state and recent files

**Step 2: 验证新 commits 存在**

```bash
git log a7b4b8d..HEAD --oneline | head -10
```

Expected: See commits from 3/20-3/21

**Step 3: 运行 skill 并验证**

Run the skill and verify:
- Status preview shows correct info
- Confirmation prompt appears
- Files are generated correctly
- .state.json is updated

---

## Success Criteria

1. ✅ Running skill shows automatic status detection
2. ✅ Preview displays: last commit, file date, new commits count, start date
3. ✅ User confirmation required before generation
4. ✅ Generated files reflect actual new git commits
5. ✅ .state.json updated with new last_commit and last_file_date
