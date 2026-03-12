# CLAUDE.md 更新设计

## 目标

更新 CLAUDE.md 文件，实现：
1. 区分前后端任务部分
2. 添加阶段完成记录规则

## 设计决策

| 决策项 | 选择 | 理由 |
|--------|------|------|
| 进度记录位置 | 独立文件 `docs/progress.md` | CLAUDE.md 保持简洁，进度集中管理 |
| 文件组织方式 | 单文件，标题区分前后端 | 简单直接，便于整体查看 |

## 改动内容

### 1. CLAUDE.md 改动

#### 1.1 重构 "Implementation Phases" 章节

将现有的单一阶段列表拆分为：

```markdown
## Implementation Phases

### Backend Phases

1. **Phase 1**: Environment setup (1-2 days) ✅
2. **Phase 2**: LLM adaptation (2-3 days)
3. **Phase 3**: Agent customization (2-3 days)
4. **Phase 4**: Scenario validation (2-3 days)
5. **Phase 5**: Summary and review (1 day)

### Frontend Phases

1. **Phase 1**: FastAPI basic API (1 day)
2. **Phase 2**: Frontend framework setup (0.5 day)
3. **Phase 3**: Task management (1 day)
4. **Phase 4**: Execution monitoring (1 day)
5. **Phase 5**: Report viewing (0.5 day)
```

#### 1.2 新增 "阶段完成规则" 章节

```markdown
## 阶段完成规则

当后端或前端的某个阶段完成时，必须：

1. **更新进度文件** `docs/progress.md`
   - 记录完成日期
   - 记录阶段编号
   - 写明更新内容摘要

2. **格式示例**：
   ```markdown
   ### Phase 2: 模型适配 ✅
   - **完成日期**: 2026-03-10
   - **更新内容**: 实现统一 LLM 接口、适配通义千问、验证图像理解能力
   ```

3. **同步更新主计划文档**
   - 后端：更新 `docs/1_后端主计划.md` 中的任务勾选状态
   - 前端：更新 `docs/2_前端主计划.md` 中的任务勾选状态
```

### 2. 新建 `docs/progress.md`

```markdown
# 项目进度追踪

> 本文件记录前后端各阶段的完成情况

## 后端进度

### Phase 1: 环境搭建 ✅
- **完成日期**: 2026-03-08
- **更新内容**: 项目结构初始化、Browser-Use 安装、API Key 配置、Playwright 验证

### Phase 2: 模型适配
- *待完成*

### Phase 3: Agent 改造
- *待完成*

### Phase 4: 场景验证
- *待完成*

### Phase 5: 总结与复盘
- *待完成*

---

## 前端进度

### Phase 1: FastAPI 基础 API 搭建
- *待完成*

### Phase 2: 前端基础框架搭建
- *待完成*

### Phase 3: 任务管理功能
- *待完成*

### Phase 4: 执行监控功能
- *待完成*

### Phase 5: 报告查看功能
- *待完成*
```

## 文件变更清单

| 文件 | 操作 |
|------|------|
| `CLAUDE.md` | 修改：重构阶段章节，新增规则章节 |
| `docs/progress.md` | 新建：进度追踪文件 |
