# Work Hours Skill 智能状态追踪设计

## 问题

现有 `work-hours` skill 的状态追踪存在 bug：
- 状态文件记录的 `last_date` 是 git commit 的提交日期
- 工时文件可能顺延到更晚的日期（每天4小时上限）
- 导致下次运行时从旧日期重新生成，覆盖已有文件

**实际案例**：
- commit 日期：2026-03-15
- 工时文件生成到：2026-03-22
- 状态文件 `last_date`：2026-03-15
- 下次运行从 2026-03-16 重新开始 ❌

## 目标

实现智能状态追踪，确保从正确位置续接。

## 设计方案

### 1. 状态文件新增字段

```json
{
  "last_commit": "03c9df2",
  "last_date": "2026-03-15",
  "last_generated_date": "2026-03-22",
  "processed_count": 231,
  "updated_at": "2026-03-21T10:30:00Z"
}
```

新增：
- `last_generated_date`: 工时文件实际生成到的日期

### 2. 启动时智能检测逻辑

```
用户调用 /work-hours
        ↓
读取 .state.json（如果存在）
        ↓
扫描 _backup/archives/工时/*.md 文件
        ↓
计算起始日期 = max(
    state.last_generated_date,
    最新工时文件的日期
) + 1 天
        ↓
如果 起始日期 > 今天 → 提示"无新工时需要生成"
否则 → 从起始日期开始生成
```

### 3. 场景验证

**场景 A：状态文件过时（当前问题）**
```
state.last_generated_date = "2026-03-15"
实际文件最新日期 = "2026-03-22"

→ 起始日期 = max(03-15, 03-22) + 1 = 03-23 ✓
```

**场景 B：文件被误删**
```
state.last_generated_date = "2026-03-22"
实际文件最新日期 = "2026-03-20"

→ 起始日期 = max(03-22, 03-20) + 1 = 03-23 ✓
```

**场景 C：首次运行**
```
state 不存在，文件不存在

→ 提示用户指定开始日期
```

### 4. 修改范围

修改 `.claude/skills/work-hours.zip` 中的 `SKILL.md`：

1. **Step 0**：添加智能检测逻辑
2. **状态文件格式**：增加 `last_generated_date` 字段说明
3. **Step 6**：生成后更新 `last_generated_date`

## 实施范围

- 单个文件：`work-hours/SKILL.md`
- 无需代码修改（skill 本身是指导文档）
