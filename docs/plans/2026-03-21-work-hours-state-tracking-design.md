# Work Hours Skill 状态追踪设计

## 背景

现有的 `work-hours` skill 从 git 提交生成工时记录，但没有追踪"上次处理到哪次提交"。这导致：
- 重复运行时可能重复记录工时
- 无法确定从哪里继续处理
- 用户需要手动记忆上次处理的位置

## 目标

为 skill 添加状态追踪功能，记录已处理的 commits，支持自动续接。

## 设计方案

### 1. 状态文件

位置：`_backup/archives/工时/.state.json`

格式：
```json
{
  "processed_commits": {
    "27e0c23": "2026-03-15.md",
    "7bdc080": "2026-03-15.md",
    "b3f3015": "2026-03-16.md"
  },
  "last_commit": "27e0c23",
  "last_date": "2026-03-15",
  "updated_at": "2026-03-21T10:30:00Z"
}
```

字段说明：
- `processed_commits`: commit hash → 工时文件的映射
- `last_commit`: 最后处理的 commit hash（短格式）
- `last_date`: 最后处理的工时文件日期
- `updated_at`: 状态文件最后更新时间

### 2. 工作流程

```
用户调用 /work-hours
        ↓
检查 .state.json 是否存在
        ↓
┌─ 不存在 → 提示用户指定开始日期，从头初始化
│
└─ 存在 → 读取 last_commit
        ↓
    获取该 commit 之后的所有新 commits
        ↓
    按现有逻辑生成工时文件
        ↓
    更新 .state.json（添加新 commits 到映射）
```

### 3. 命令参数

| 命令 | 行为 |
|------|------|
| `/work-hours` | 自动续接（从上次结束的地方继续） |
| `/work-hours --from 2026-03-01` | 强制从指定日期开始（重置状态） |
| `/work-hours --status` | 显示当前状态（最后处理的 commit、日期等） |

### 4. 智能推断逻辑

当存在状态文件时：
1. 读取 `last_commit`
2. 执行 `git log ${last_commit}..HEAD` 获取新 commits
3. 按日期分组，估算工时
4. 生成工时文件
5. 更新状态文件

当用户指定 `--from` 时：
1. 清空 `processed_commits`
2. 从指定日期开始重新处理
3. 重建状态文件

### 5. 状态显示示例

```
📊 工时记录状态：
  最后处理提交: 27e0c23 (2026-03-15)
  已处理 commits: 45 个
  生成工时文件: 12 个
  上次更新: 2026-03-21 10:30
```

## 实施范围

修改文件：`.claude/skills/work-hours.zip` 中的 `SKILL.md`

主要改动：
1. 添加状态文件格式说明
2. 更新工作流程
3. 添加命令参数说明
4. 添加状态显示逻辑

## 风险

- 状态文件可能被误删 → 建议用户定期备份 `_backup/archives/工时/` 目录
- commit hash 冲突（极低概率） → 使用短 hash 足够
