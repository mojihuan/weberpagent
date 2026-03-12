# CLAUDE.md 更新实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 更新 CLAUDE.md 区分前后端任务，添加阶段完成规则，创建进度追踪文件

**Architecture:** 纯文档更新，无代码改动。重构 CLAUDE.md 的 Implementation Phases 章节，新增阶段完成规则章节，创建独立的 docs/progress.md 进度追踪文件

**Tech Stack:** Markdown

---

### Task 1: 创建进度追踪文件

**Files:**
- Create: `docs/progress.md`

**Step 1: 创建 docs/progress.md 文件**

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

**Step 2: 验证文件创建成功**

Run: `cat docs/progress.md`
Expected: 显示上述内容

**Step 3: 提交**

```bash
git add docs/progress.md
git commit -m "docs: 创建项目进度追踪文件"
```

---

### Task 2: 更新 CLAUDE.md - 重构 Implementation Phases 章节

**Files:**
- Modify: `CLAUDE.md:168-174`

**Step 1: 找到并替换 Implementation Phases 章节**

将现有的：

```markdown
## Implementation Phases

1. **Phase 1**: Environment setup (1-2 days)
2. **Phase 2**: LLM adaptation (2-3 days)
3. **Phase 3**: Agent customization (2-3 days)
4. **Phase 4**: Scenario validation (2-3 days)
5. **Phase 5**: Summary and review (1 day)
```

替换为：

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

详细任务清单请参考：
- 后端：`docs/1_后端主计划.md`
- 前端：`docs/2_前端主计划.md`
```

**Step 2: 验证修改正确**

Run: `grep -A 20 "## Implementation Phases" CLAUDE.md`
Expected: 显示新的章节结构

---

### Task 3: 更新 CLAUDE.md - 新增阶段完成规则章节

**Files:**
- Modify: `CLAUDE.md` (在工时记录规则章节之前)

**Step 1: 在工时记录规则章节之前添加新章节**

在 `## 工时记录规则` 之前插入：

```markdown
## 阶段完成规则

当后端或前端的某个阶段完成时，必须执行以下操作：

### 1. 更新进度文件

更新 `docs/progress.md`，记录：
- 完成日期
- 阶段编号
- 更新内容摘要

**格式示例**：
```markdown
### Phase 2: 模型适配 ✅
- **完成日期**: 2026-03-10
- **更新内容**: 实现统一 LLM 接口、适配通义千问、验证图像理解能力
```

### 2. 同步更新主计划文档

- 后端完成：更新 `docs/1_后端主计划.md` 中的任务勾选状态
- 前端完成：更新 `docs/2_前端主计划.md` 中的任务勾选状态

### 3. 提交记录

使用格式：`docs: 记录 Phase X 完成 - [阶段名称]`

---

```

**Step 2: 验证修改正确**

Run: `grep -A 25 "## 阶段完成规则" CLAUDE.md`
Expected: 显示完整的规则章节

---

### Task 4: 最终验证与提交

**Files:**
- `CLAUDE.md`

**Step 1: 查看完整的 CLAUDE.md 确认修改**

Run: `cat CLAUDE.md`
Expected: 文件结构正确，无语法错误

**Step 2: 提交所有修改**

```bash
git add CLAUDE.md
git commit -m "$(cat <<'EOF'
docs: 重构 CLAUDE.md 区分前后端阶段，添加阶段完成规则

- 将 Implementation Phases 拆分为 Backend Phases 和 Frontend Phases
- 新增"阶段完成规则"章节，说明完成后需更新 docs/progress.md
- 在后端 Phase 1 标记 ✅ 表示已完成
EOF
)"
```

**Step 3: 推送到远程**

```bash
git push origin main
```

---

## 完成检查清单

- [ ] `docs/progress.md` 文件已创建
- [ ] CLAUDE.md 的 Implementation Phases 已拆分为前后端
- [ ] CLAUDE.md 已添加阶段完成规则章节
- [ ] 所有改动已提交
