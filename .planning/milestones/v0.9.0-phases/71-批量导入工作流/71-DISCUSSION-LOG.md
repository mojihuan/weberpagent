# Phase 71: 批量导入工作流 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-08
**Phase:** 71-批量导入工作流
**Areas discussed:** 上传交互体验, 预览展示设计, API 设计与流程, 前端状态管理

---

## 上传交互体验

| Option | Description | Selected |
|--------|-------------|----------|
| Modal 弹窗模式 | 点击「导入」按钮弹出 Modal，内含拖拽上传区 + 预览表格，确认后关闭 Modal 并刷新任务列表 | ✓ |
| 独立页面模式 | 点击「导入」按钮跳转到独立页面 | |
| 内嵌展开模式 | 在任务列表上方展开上传区 + 预览 | |

**User's choice:** Modal 弹窗模式
**Notes:** 与 TaskFormModal 同级交互模式，不离开当前页面

| Option | Description | Selected |
|--------|-------------|----------|
| 拖拽 + 点击双模式 | 拖入文件高亮提示，支持 .xlsx 格式校验 | ✓ |
| 仅点击选择 | 简洁但无拖拽体验 | |

**User's choice:** 拖拽 + 点击双模式

| Option | Description | Selected |
|--------|-------------|----------|
| 5MB 上限 | 足够 ~1000 行用例，符合 REQUIREMENTS | ✓ |
| 10MB 上限 | 更宽松但可能耗尽服务器内存 | |

**User's choice:** 5MB 上限

---

## 预览展示设计

| Option | Description | Selected |
|--------|-------------|----------|
| 完整表格预览 | 显示所有列，错误行红色背景 + 错误信息列 | ✓ |
| 精简列表预览 | 只显示名称 + 状态 + 错误 | |
| 卡片式预览 | 每任务一个卡片，视觉友好但占空间 | |

**User's choice:** 完整表格预览

| Option | Description | Selected |
|--------|-------------|----------|
| 摘要 + 错误行标红 | 表格顶部"有效 X 行，无效 Y 行"，错误行淡红背景 | ✓ |
| Tab 分组显示 | 有效行/无效行分 Tab 查看 | |

**User's choice:** 摘要 + 错误行标红

| Option | Description | Selected |
|--------|-------------|----------|
| Modal 内滚动 | 超过 Modal 高度时表头固定，内容区滚动 | ✓ |
| 分页加载 | 只显示前 N 行，需加载更多 | |

**User's choice:** Modal 内滚动

---

## API 设计与流程

| Option | Description | Selected |
|--------|-------------|----------|
| 两阶段重传模式 | preview 上传返回 JSON，confirm 重新上传文件创建。无服务器缓存 | ✓ |
| Token 缓存模式 | preview 返回 token，confirm 传 token。服务器缓存解析结果 | |

**User's choice:** 两阶段重传模式
**Notes:** 符合 STATE.md 已有决策"confirm 时重新解析而非缓存服务器状态"

| Option | Description | Selected |
|--------|-------------|----------|
| tasks.py 内新增 | 与 /tasks/template 保持一致 | ✓ |
| 独立路由文件 | 新建 routes/import.py | |

**User's choice:** tasks.py 内新增

| Option | Description | Selected |
|--------|-------------|----------|
| 单事务原子提交 | 任一失败全部回滚，符合 IMPT-03 | ✓ |
| 逐行独立创建 | 失败的跳过，成功的保留 | |

**User's choice:** 单事务原子提交

---

## 前端状态管理

| Option | Description | Selected |
|--------|-------------|----------|
| 独立 ImportModal 组件 | 与 TaskFormModal 同级，内部管理三步状态 | ✓ |
| 复用 TaskModal | 在现有 Modal 内新增 tab | |

**User's choice:** 独立 ImportModal 组件

| Option | Description | Selected |
|--------|-------------|----------|
| 分步 loading + toast 反馈 | 每步独立 loading，成功/失败 toast 通知 | ✓ |
| 进度条展示 | 更详细但复杂度高 | |

**User's choice:** 分步 loading + toast 反馈

| Option | Description | Selected |
|--------|-------------|----------|
| 关闭 Modal + 自动刷新 | 成功后关闭 Modal，刷新任务列表 | ✓ |
| 显示结果页后手动关闭 | Modal 显示"成功导入 X 个任务" | |

**User's choice:** 关闭 Modal + 自动刷新

| Option | Description | Selected |
|--------|-------------|----------|
| 原生 fetch + 复用配置 | 绕过 apiClient 的 Content-Type，复用 API_BASE | ✓ |
| 增强 apiClient 支持 FormData | 在 apiClient 中检测 FormData 自动去除 Content-Type | |

**User's choice:** 原生 fetch + 复用配置

---

## Claude's Discretion

- Modal 具体样式和布局
- 预览表格列宽分配
- 错误信息展示格式（列内 vs tooltip vs 行下方展开）
- Modal 尺寸
- 后端响应 JSON 结构
- ImportModal 内部子组件拆分

## Deferred Ideas

None — discussion stayed within phase scope
