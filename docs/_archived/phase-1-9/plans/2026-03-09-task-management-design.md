# Phase 3: 任务管理功能设计文档

> 创建日期：2026-03-09
> 状态：已确认

## 1. 概述

### 1.1 目标

实现前端任务管理功能，使用 Mock 数据开发，后续对接真实 API。

### 1.2 功能范围

- 任务列表页面（搜索、筛选、排序、分页、批量操作）
- 任务创建/编辑表单（模态弹窗）
- 任务详情页面（基本信息、执行历史、统计图表）

---

## 2. 架构设计

### 2.1 目录结构

```
frontend/src/
├── api/
│   ├── client.ts            # 已有 - 基础请求封装
│   ├── tasks.ts             # 新增 - 任务 API 接口
│   └── mock/
│       ├── index.ts         # Mock 开关控制
│       ├── tasks.ts         # 任务 Mock 数据
│       └── runs.ts          # 执行记录 Mock 数据
├── components/
│   ├── Layout.tsx           # 已有
│   ├── Sidebar.tsx          # 已有
│   ├── NavItem.tsx          # 已有
│   ├── Button.tsx           # 已有
│   ├── TaskList/            # 新增 - 任务列表组件
│   │   ├── index.ts
│   │   ├── TaskTable.tsx
│   │   ├── TaskFilters.tsx
│   │   ├── TaskRow.tsx
│   │   ├── BatchActions.tsx
│   │   └── TaskListHeader.tsx
│   ├── TaskModal/           # 新增 - 任务表单弹窗
│   │   ├── index.ts
│   │   ├── TaskFormModal.tsx
│   │   └── TaskForm.tsx
│   ├── TaskDetail/          # 新增 - 任务详情组件
│   │   ├── index.ts
│   │   ├── TaskHeader.tsx
│   │   ├── TaskInfo.tsx
│   │   ├── ConfigPanel.tsx
│   │   ├── RunHistory.tsx
│   │   ├── StatsChart.tsx
│   │   └── DeleteConfirm.tsx
│   └── shared/              # 新增 - 通用组件
│       ├── index.ts
│       ├── StatusBadge.tsx
│       ├── Pagination.tsx
│       ├── EmptyState.tsx
│       ├── ConfirmModal.tsx
│       └── LoadingSpinner.tsx
├── hooks/
│   └── useTasks.ts          # 新增 - 任务数据 Hook
├── pages/
│   ├── Tasks.tsx            # 修改 - 任务列表页
│   └── TaskDetail.tsx       # 修改 - 任务详情页
└── types/
    └── index.ts             # 已有 - 类型定义
```

### 2.2 组件架构

采用分层组件架构，职责清晰，便于维护和复用。

---

## 3. 模块详细设计

### 3.1 任务列表页面

#### 布局

```
┌─────────────────────────────────────────────────────────────┐
│  任务管理                              [+ 新建任务]          │  <- TaskListHeader
├─────────────────────────────────────────────────────────────┤
│  [🔍 搜索任务...]     [状态 ▼] [排序 ▼]                      │  <- TaskFilters
├─────────────────────────────────────────────────────────────┤
│  ☐ │ 名称          │ 目标URL      │ 状态   │ 步数 │ 操作    │
├─────────────────────────────────────────────────────────────┤
│  ☑ │ 用户登录测试   │ example.com  │ 🟢就绪 │ 10   │ ▶️ ✏️ 🗑️ │
│  ☐ │ 表单提交测试   │ example.com  │ ⚪草稿 │ 15   │ ▶️ ✏️ 🗑️ │
├─────────────────────────────────────────────────────────────┤
│  已选中 2 项  [批量删除] [批量设为就绪]                       │  <- BatchActions
├─────────────────────────────────────────────────────────────┤
│  共 25 条  < 1 2 3 ... 5 >                                  │  <- Pagination
└─────────────────────────────────────────────────────────────┘
```

#### 功能清单

- 搜索：按任务名称搜索
- 筛选：按状态筛选（全部/草稿/就绪）
- 排序：按更新时间/名称/创建时间
- 分页：前端分页，每页 10 条
- 批量操作：批量删除、批量设为就绪
- 快速操作：立即执行、编辑、删除

#### useTasks Hook

```typescript
export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState({
    search: '',
    status: 'all',
    sortBy: 'updated_at',
    sortOrder: 'desc'
  })
  const [selectedIds, setSelectedIds] = useState<string[]>([])
  const [page, setPage] = useState(1)
  const pageSize = 10

  return {
    tasks, loading, filters, selectedIds, page, pageSize,
    setFilters, setSelectedIds, setPage,
    fetchTasks, batchDelete, batchUpdateStatus,
  }
}
```

---

### 3.2 任务表单弹窗

#### 布局

```
┌─────────────────────────────────────────────────────────────┐
│  新建任务                                              [✕]  │
├─────────────────────────────────────────────────────────────┤
│  任务名称 *                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  任务描述                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  目标 URL *                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  最大步数（默认 20，范围 1-50）                             │
│  ┌──────────┐                                              │
│  │    20    │◀ ▶                                          │
│  └──────────┘                                              │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                              [取消]  [创建任务]             │
└─────────────────────────────────────────────────────────────┘
```

#### 表单字段

| 字段 | 类型 | 必填 | 验证规则 | 默认值 |
|------|------|------|----------|--------|
| name | text | ✅ | 1-50 字符 | - |
| description | textarea | ❌ | 最多 500 字符 | - |
| target_url | text | ✅ | 有效 URL 格式 | - |
| max_steps | number | ❌ | 1-50 | 20 |

#### Props

```typescript
interface TaskFormModalProps {
  open: boolean
  onClose: () => void
  mode: 'create' | 'edit'
  task?: Task
  onSuccess: (task: Task) => void
}
```

---

### 3.3 任务详情页面

#### 布局

```
┌─────────────────────────────────────────────────────────────┐
│  ← 返回列表                                                  │
├─────────────────────────────────────────────────────────────┤
│  用户登录测试                               [▶ 立即执行]    │
│  使用测试账号登录系统，验证登录流程            [✏️ 编辑]     │
│                                              [🗑️ 删除]     │
├─────────────────────────────────────────────────────────────┤
│  基本信息                                              🟢就绪│
│  ┌─────────────────────────────────────────────────────┐   │
│  │  目标 URL    https://example.com/login              │   │
│  │  最大步数    10                                     │   │
│  │  创建时间    2026-03-08 10:00                       │   │
│  │  更新时间    2026-03-08 14:30                       │   │
│  └─────────────────────────────────────────────────────┘   │
│  ▶ 配置详情（可折叠）                                       │
├─────────────────────────────────────────────────────────────┤
│  执行统计                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │     📈 最近 7 天执行趋势（双 Y 轴折线图）             │   │
│  │      ── 执行次数  ── 成功率%                         │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  执行历史                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🟢 成功  2026-03-08 14:30  耗时 12.5s  步数 8/10   │   │
│  │  🔴 失败  2026-03-08 10:15  耗时 8.2s   步数 5/10   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

#### 组件拆分

| 组件 | 功能 |
|------|------|
| TaskHeader | 任务名称、描述、操作按钮 |
| TaskInfo | 基本信息卡片 |
| ConfigPanel | 配置详情（可折叠） |
| StatsChart | 统计图表（Recharts） |
| RunHistory | 执行历史列表 |

#### 操作按钮行为

| 按钮 | 行为 |
|------|------|
| 立即执行 | 调用 API → 跳转执行监控页 |
| 编辑 | 打开编辑弹窗 |
| 删除 | 确认弹窗 → 删除 → 返回列表 |

---

### 3.4 统计图表

使用 **Recharts** 实现双 Y 轴折线图：

- 左 Y 轴：执行次数
- 右 Y 轴：成功率（0-100%）
- X 轴：最近 7 天日期

```typescript
const chartData = [
  { date: '03/03', runs: 3, successRate: 100 },
  { date: '03/04', runs: 5, successRate: 80 },
  // ...
]
```

---

### 3.5 Mock 数据层

```typescript
// api/mock/index.ts
const ENABLE_MOCK = true

// api/mock/tasks.ts
export const mockTasks: Task[] = [
  {
    id: '1',
    name: '用户登录测试',
    description: '使用测试账号登录系统，验证登录流程',
    target_url: 'https://example.com/login',
    max_steps: 10,
    status: 'ready',
    created_at: '2026-03-08T10:00:00Z',
    updated_at: '2026-03-08T10:00:00Z'
  },
  // ... 更多测试数据
]

// api/mock/runs.ts
export const mockRuns: Run[] = [
  // 执行历史数据
]
```

---

### 3.6 共享组件

```
components/shared/
├── StatusBadge.tsx      # 状态标签
├── Pagination.tsx       # 分页
├── EmptyState.tsx       # 空状态
├── ConfirmModal.tsx     # 确认弹窗
└── LoadingSpinner.tsx   # 加载动画
```

**状态颜色映射**：

```typescript
const statusConfig = {
  draft: { label: '草稿', color: 'gray' },
  ready: { label: '就绪', color: 'green' },
  running: { label: '执行中', color: 'blue' },
  success: { label: '成功', color: 'green' },
  failed: { label: '失败', color: 'red' },
  stopped: { label: '已停止', color: 'yellow' }
}
```

---

## 4. 依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| recharts | ^2.12.0 | 统计图表 |

---

## 5. 实现计划

```
Phase 3 实现顺序
────────────────────────────────────────────────────
1. 基础层（约 1-2 小时）
   ├── 1.1 Mock 数据层
   ├── 1.2 API 接口层
   ├── 1.3 useTasks Hook
   └── 1.4 共享组件

2. 任务列表页（约 2-3 小时）
   ├── 2.1 TaskListHeader
   ├── 2.2 TaskFilters
   ├── 2.3 TaskTable + TaskRow
   ├── 2.4 BatchActions
   └── 2.5 分页逻辑

3. 任务表单弹窗（约 1-2 小时）
   ├── 3.1 TaskForm 表单
   └── 3.2 TaskFormModal 弹窗

4. 任务详情页（约 2-3 小时）
   ├── 4.1 TaskHeader
   ├── 4.2 TaskInfo
   ├── 4.3 ConfigPanel
   ├── 4.4 RunHistory
   └── 4.5 StatsChart

5. 集成测试（约 0.5 小时）
   └── 5.1 页面间跳转 + 交互验证
────────────────────────────────────────────────────
预估总工时：6-10 小时
```

---

## 6. 验收标准

- [ ] 任务列表页可正常显示、搜索、筛选、排序、分页
- [ ] 可创建、编辑、删除任务
- [ ] 任务详情页显示完整信息
- [ ] 统计图表正确展示
- [ ] 执行历史可点击跳转
- [ ] Mock 数据可切换到真实 API
