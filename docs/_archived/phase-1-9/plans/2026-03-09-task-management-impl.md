# Phase 3: 任务管理功能实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现前端任务管理功能（列表、表单、详情），使用 Mock 数据开发

**Architecture:** 分层组件架构，Mock 数据层独立，便于后续对接真实 API

**Tech Stack:** React 19 + TypeScript + Tailwind CSS v4 + @tanstack/react-query + Recharts + lucide-react

---

## Task 1: 安装依赖

**Files:**
- Modify: `frontend/package.json`

**Step 1: 安装 Recharts 图表库**

```bash
cd /Users/huhu/project/weberpagent/frontend && npm install recharts
```

**Step 2: 验证安装**

```bash
npm list recharts
```

Expected: `recharts@2.x.x`

---

## Task 2: 创建 Mock 数据层

**Files:**
- Create: `frontend/src/api/mock/index.ts`
- Create: `frontend/src/api/mock/tasks.ts`
- Create: `frontend/src/api/mock/runs.ts`

**Step 1: 创建 Mock 开关文件**

```typescript
// frontend/src/api/mock/index.ts
export const ENABLE_MOCK = true

export function delay(ms: number = 300) {
  return new Promise(resolve => setTimeout(resolve, ms))
}
```

**Step 2: 创建任务 Mock 数据**

```typescript
// frontend/src/api/mock/tasks.ts
import type { Task } from '../../types'

export const mockTasks: Task[] = [
  {
    id: '1',
    name: '用户登录测试',
    description: '使用测试账号登录系统，验证登录流程是否正常工作',
    target_url: 'https://example.com/login',
    max_steps: 10,
    status: 'ready',
    created_at: '2026-03-08T10:00:00Z',
    updated_at: '2026-03-08T14:30:00Z',
  },
  {
    id: '2',
    name: '表单提交测试',
    description: '填写并提交用户信息表单，验证数据提交功能',
    target_url: 'https://example.com/form',
    max_steps: 15,
    status: 'ready',
    created_at: '2026-03-07T09:00:00Z',
    updated_at: '2026-03-07T11:00:00Z',
  },
  {
    id: '3',
    name: '搜索功能测试',
    description: '测试搜索框的关键词搜索和结果展示',
    target_url: 'https://example.com/search',
    max_steps: 8,
    status: 'draft',
    created_at: '2026-03-06T14:00:00Z',
    updated_at: '2026-03-06T14:00:00Z',
  },
  {
    id: '4',
    name: '购物车流程测试',
    description: '添加商品到购物车，修改数量，结算流程',
    target_url: 'https://shop.example.com/cart',
    max_steps: 20,
    status: 'ready',
    created_at: '2026-03-05T08:00:00Z',
    updated_at: '2026-03-05T16:00:00Z',
  },
  {
    id: '5',
    name: '用户注册测试',
    description: '新用户注册流程，包括邮箱验证',
    target_url: 'https://example.com/register',
    max_steps: 12,
    status: 'draft',
    created_at: '2026-03-04T10:00:00Z',
    updated_at: '2026-03-04T10:00:00Z',
  },
  {
    id: '6',
    name: '订单查询测试',
    description: '查询历史订单列表和订单详情',
    target_url: 'https://example.com/orders',
    max_steps: 10,
    status: 'ready',
    created_at: '2026-03-03T09:00:00Z',
    updated_at: '2026-03-03T15:00:00Z',
  },
  {
    id: '7',
    name: '个人设置测试',
    description: '修改用户个人信息和偏好设置',
    target_url: 'https://example.com/settings',
    max_steps: 8,
    status: 'ready',
    created_at: '2026-03-02T11:00:00Z',
    updated_at: '2026-03-02T14:00:00Z',
  },
  {
    id: '8',
    name: '消息通知测试',
    description: '测试系统消息和通知的展示与交互',
    target_url: 'https://example.com/notifications',
    max_steps: 6,
    status: 'draft',
    created_at: '2026-03-01T10:00:00Z',
    updated_at: '2026-03-01T10:00:00Z',
  },
]

// 用于生成新 ID
let nextId = 100

export function generateTaskId(): string {
  return String(nextId++)
}
```

**Step 3: 创建执行记录 Mock 数据**

```typescript
// frontend/src/api/mock/runs.ts
import type { Run, Step } from '../../types'

// 生成模拟步骤
function generateSteps(count: number, hasError: boolean): Step[] {
  const actions = [
    '打开目标页面',
    '等待页面加载完成',
    '识别登录表单',
    '填写用户名',
    '填写密码',
    '点击登录按钮',
    '等待登录响应',
    '验证登录状态',
    '截图保存',
  ]

  return Array.from({ length: count }, (_, i) => {
    const isFailed = hasError && i === count - 2
    return {
      index: i + 1,
      action: actions[i % actions.length] || `执行操作 ${i + 1}`,
      reasoning: `AI 分析：当前页面状态正常，准备执行 ${actions[i % actions.length] || `操作 ${i + 1}`}`,
      screenshot: `/screenshots/step-${i + 1}.png`,
      status: isFailed ? 'failed' : 'success',
      error: isFailed ? '元素定位超时：未找到目标按钮' : undefined,
      duration_ms: Math.floor(Math.random() * 3000) + 500,
    }
  })
}

export const mockRuns: Run[] = [
  {
    id: 'r1',
    task_id: '1',
    status: 'success',
    started_at: '2026-03-08T14:30:00Z',
    finished_at: '2026-03-08T14:30:45Z',
    steps: generateSteps(8, false),
  },
  {
    id: 'r2',
    task_id: '1',
    status: 'failed',
    started_at: '2026-03-08T10:15:00Z',
    finished_at: '2026-03-08T10:15:32Z',
    steps: generateSteps(5, true),
  },
  {
    id: 'r3',
    task_id: '1',
    status: 'success',
    started_at: '2026-03-07T16:00:00Z',
    finished_at: '2026-03-07T16:01:15Z',
    steps: generateSteps(9, false),
  },
  {
    id: 'r4',
    task_id: '1',
    status: 'success',
    started_at: '2026-03-06T09:00:00Z',
    finished_at: '2026-03-06T09:00:38Z',
    steps: generateSteps(7, false),
  },
  {
    id: 'r5',
    task_id: '1',
    status: 'success',
    started_at: '2026-03-05T14:00:00Z',
    finished_at: '2026-03-05T14:00:52Z',
    steps: generateSteps(10, false),
  },
  {
    id: 'r6',
    task_id: '2',
    status: 'success',
    started_at: '2026-03-07T11:00:00Z',
    finished_at: '2026-03-07T11:01:20Z',
    steps: generateSteps(12, false),
  },
  {
    id: 'r7',
    task_id: '4',
    status: 'success',
    started_at: '2026-03-05T16:00:00Z',
    finished_at: '2026-03-05T16:02:30Z',
    steps: generateSteps(18, false),
  },
]

// 获取任务执行统计（用于图表）
export function getTaskStats(taskId: string) {
  const taskRuns = mockRuns.filter(r => r.task_id === taskId)
  const last7Days = ['03/03', '03/04', '03/05', '03/06', '03/07', '03/08', '03/09']

  return last7Days.map(date => {
    // 模拟每天的执行数据
    const runs = Math.floor(Math.random() * 5) + 1
    const successRate = Math.floor(Math.random() * 40) + 60
    return { date, runs, successRate }
  })
}
```

**Step 4: 验证文件创建**

```bash
ls -la /Users/huhu/project/weberpagent/frontend/src/api/mock/
```

Expected: 3 files listed

---

## Task 3: 创建 API 接口层

**Files:**
- Create: `frontend/src/api/tasks.ts`

**Step 1: 创建任务 API 接口**

```typescript
// frontend/src/api/tasks.ts
import type { Task, CreateTaskDto, UpdateTaskDto, Run } from '../types'
import { apiClient } from './client'
import { ENABLE_MOCK, delay } from './mock/index'
import { mockTasks, mockRuns, generateTaskId, getTaskStats } from './mock'

const USE_MOCK = ENABLE_MOCK

export const tasksApi = {
  // 获取任务列表
  async list(params?: { status?: string; search?: string }): Promise<Task[]> {
    if (USE_MOCK) {
      await delay(200)
      let result = [...mockTasks]

      if (params?.status && params.status !== 'all') {
        result = result.filter(t => t.status === params.status)
      }

      if (params?.search) {
        const search = params.search.toLowerCase()
        result = result.filter(t =>
          t.name.toLowerCase().includes(search) ||
          t.description.toLowerCase().includes(search)
        )
      }

      return result
    }
    return apiClient<Task[]>('/tasks')
  },

  // 获取单个任务
  async get(id: string): Promise<Task | null> {
    if (USE_MOCK) {
      await delay(100)
      return mockTasks.find(t => t.id === id) || null
    }
    return apiClient<Task>(`/tasks/${id}`)
  },

  // 创建任务
  async create(data: CreateTaskDto): Promise<Task> {
    if (USE_MOCK) {
      await delay(300)
      const now = new Date().toISOString()
      const task: Task = {
        id: generateTaskId(),
        ...data,
        status: 'draft',
        created_at: now,
        updated_at: now,
      }
      mockTasks.unshift(task)
      return task
    }
    return apiClient<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  // 更新任务
  async update(id: string, data: UpdateTaskDto): Promise<Task> {
    if (USE_MOCK) {
      await delay(200)
      const index = mockTasks.findIndex(t => t.id === id)
      if (index === -1) throw new Error('Task not found')

      mockTasks[index] = {
        ...mockTasks[index],
        ...data,
        updated_at: new Date().toISOString(),
      }
      return mockTasks[index]
    }
    return apiClient<Task>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  },

  // 删除任务
  async delete(id: string): Promise<void> {
    if (USE_MOCK) {
      await delay(200)
      const index = mockTasks.findIndex(t => t.id === id)
      if (index !== -1) {
        mockTasks.splice(index, 1)
      }
      return
    }
    return apiClient<void>(`/tasks/${id}`, { method: 'DELETE' })
  },

  // 批量删除
  async batchDelete(ids: string[]): Promise<void> {
    if (USE_MOCK) {
      await delay(300)
      ids.forEach(id => {
        const index = mockTasks.findIndex(t => t.id === id)
        if (index !== -1) mockTasks.splice(index, 1)
      })
      return
    }
    // 真实 API 需要后端支持批量删除
    await Promise.all(ids.map(id => apiClient<void>(`/tasks/${id}`, { method: 'DELETE' })))
  },

  // 批量更新状态
  async batchUpdateStatus(ids: string[], status: 'draft' | 'ready'): Promise<void> {
    if (USE_MOCK) {
      await delay(300)
      const now = new Date().toISOString()
      ids.forEach(id => {
        const task = mockTasks.find(t => t.id === id)
        if (task) {
          task.status = status
          task.updated_at = now
        }
      })
      return
    }
    // 真实 API 需要后端支持批量更新
    await Promise.all(ids.map(id =>
      apiClient<void>(`/tasks/${id}`, {
        method: 'PUT',
        body: JSON.stringify({ status }),
      })
    ))
  },

  // 获取任务的执行历史
  async getRuns(taskId: string): Promise<Run[]> {
    if (USE_MOCK) {
      await delay(150)
      return mockRuns.filter(r => r.task_id === taskId)
    }
    return apiClient<Run[]>(`/tasks/${taskId}/runs`)
  },

  // 获取任务统计（用于图表）
  async getStats(taskId: string) {
    if (USE_MOCK) {
      await delay(100)
      return getTaskStats(taskId)
    }
    return apiClient<{ date: string; runs: number; successRate: number }[]>(`/tasks/${taskId}/stats`)
  },
}
```

**Step 2: 验证编译**

```bash
cd /Users/huhu/project/weberpagent/frontend && npx tsc --noEmit
```

Expected: No errors

---

## Task 4: 创建共享组件

**Files:**
- Create: `frontend/src/components/shared/index.ts`
- Create: `frontend/src/components/shared/StatusBadge.tsx`
- Create: `frontend/src/components/shared/Pagination.tsx`
- Create: `frontend/src/components/shared/EmptyState.tsx`
- Create: `frontend/src/components/shared/ConfirmModal.tsx`
- Create: `frontend/src/components/shared/LoadingSpinner.tsx`

**Step 1: 创建 StatusBadge 组件**

```typescript
// frontend/src/components/shared/StatusBadge.tsx
const statusConfig = {
  draft: { label: '草稿', className: 'bg-gray-100 text-gray-600' },
  ready: { label: '就绪', className: 'bg-green-100 text-green-700' },
  running: { label: '执行中', className: 'bg-blue-100 text-blue-700' },
  success: { label: '成功', className: 'bg-green-100 text-green-700' },
  failed: { label: '失败', className: 'bg-red-100 text-red-700' },
  stopped: { label: '已停止', className: 'bg-yellow-100 text-yellow-700' },
} as const

type Status = keyof typeof statusConfig

interface StatusBadgeProps {
  status: Status
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status]

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${config.className}`}>
      {config.label}
    </span>
  )
}
```

**Step 2: 创建 Pagination 组件**

```typescript
// frontend/src/components/shared/Pagination.tsx
import { ChevronLeft, ChevronRight } from 'lucide-react'

interface PaginationProps {
  total: number
  page: number
  pageSize: number
  onChange: (page: number) => void
}

export function Pagination({ total, page, pageSize, onChange }: PaginationProps) {
  const totalPages = Math.ceil(total / pageSize)

  if (totalPages <= 1) return null

  const pages = Array.from({ length: totalPages }, (_, i) => i + 1)

  return (
    <div className="flex items-center justify-between px-4 py-3 border-t border-gray-100">
      <div className="text-sm text-gray-500">
        共 {total} 条
      </div>
      <div className="flex items-center gap-1">
        <button
          onClick={() => onChange(page - 1)}
          disabled={page === 1}
          className="p-1 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>
        {pages.map(p => (
          <button
            key={p}
            onClick={() => onChange(p)}
            className={`w-8 h-8 rounded text-sm ${
              p === page
                ? 'bg-blue-500 text-white'
                : 'hover:bg-gray-100 text-gray-700'
            }`}
          >
            {p}
          </button>
        ))}
        <button
          onClick={() => onChange(page + 1)}
          disabled={page === totalPages}
          className="p-1 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  )
}
```

**Step 3: 创建 EmptyState 组件**

```typescript
// frontend/src/components/shared/EmptyState.tsx
import { FileQuestion } from 'lucide-react'

interface EmptyStateProps {
  message?: string
  action?: React.ReactNode
}

export function EmptyState({ message = '暂无数据', action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <FileQuestion className="w-12 h-12 text-gray-300 mb-4" />
      <p className="text-gray-500 mb-4">{message}</p>
      {action}
    </div>
  )
}
```

**Step 4: 创建 ConfirmModal 组件**

```typescript
// frontend/src/components/shared/ConfirmModal.tsx
import { X } from 'lucide-react'

interface ConfirmModalProps {
  open: boolean
  title: string
  message: string
  confirmText?: string
  cancelText?: string
  variant?: 'danger' | 'warning'
  onConfirm: () => void
  onCancel: () => void
  loading?: boolean
}

export function ConfirmModal({
  open,
  title,
  message,
  confirmText = '确认',
  cancelText = '取消',
  variant = 'warning',
  onConfirm,
  onCancel,
  loading = false,
}: ConfirmModalProps) {
  if (!open) return null

  const confirmBtnClass = variant === 'danger'
    ? 'bg-red-500 hover:bg-red-600 text-white'
    : 'bg-blue-500 hover:bg-blue-600 text-white'

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/50" onClick={onCancel} />
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-md mx-4 p-6">
        <button
          onClick={onCancel}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          <X className="w-5 h-5" />
        </button>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
        <p className="text-gray-500 mb-6">{message}</p>
        <div className="flex justify-end gap-3">
          <button
            onClick={onCancel}
            disabled={loading}
            className="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 disabled:opacity-50"
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            disabled={loading}
            className={`px-4 py-2 rounded-lg font-medium disabled:opacity-50 ${confirmBtnClass}`}
          >
            {loading ? '处理中...' : confirmText}
          </button>
        </div>
      </div>
    </div>
  )
}
```

**Step 5: 创建 LoadingSpinner 组件**

```typescript
// frontend/src/components/shared/LoadingSpinner.tsx
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function LoadingSpinner({ size = 'md', className = '' }: LoadingSpinnerProps) {
  const sizeMap = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
  }

  return (
    <div className={`animate-spin ${sizeMap[size]} ${className}`}>
      <svg fill="none" viewBox="0 0 24 24">
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
        />
      </svg>
    </div>
  )
}
```

**Step 6: 创建导出文件**

```typescript
// frontend/src/components/shared/index.ts
export { StatusBadge } from './StatusBadge'
export { Pagination } from './Pagination'
export { EmptyState } from './EmptyState'
export { ConfirmModal } from './ConfirmModal'
export { LoadingSpinner } from './LoadingSpinner'
```

**Step 7: 验证编译**

```bash
cd /Users/huhu/project/weberpagent/frontend && npx tsc --noEmit
```

Expected: No errors

---

## Task 5: 创建 useTasks Hook

**Files:**
- Create: `frontend/src/hooks/useTasks.ts`

**Step 1: 创建 useTasks Hook**

```typescript
// frontend/src/hooks/useTasks.ts
import { useState, useCallback, useEffect, useMemo } from 'react'
import type { Task } from '../types'
import { tasksApi } from '../api/tasks'

interface Filters {
  search: string
  status: 'all' | 'draft' | 'ready'
  sortBy: 'updated_at' | 'name' | 'created_at'
  sortOrder: 'asc' | 'desc'
}

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState<Filters>({
    search: '',
    status: 'all',
    sortBy: 'updated_at',
    sortOrder: 'desc',
  })
  const [selectedIds, setSelectedIds] = useState<string[]>([])
  const [page, setPage] = useState(1)
  const pageSize = 10

  // 获取任务列表
  const fetchTasks = useCallback(async () => {
    setLoading(true)
    try {
      const data = await tasksApi.list({
        status: filters.status,
        search: filters.search,
      })
      setTasks(data)
    } catch (error) {
      console.error('Failed to fetch tasks:', error)
    } finally {
      setLoading(false)
    }
  }, [filters.status, filters.search])

  // 初始加载
  useEffect(() => {
    fetchTasks()
  }, [fetchTasks])

  // 筛选后的任务
  const filteredTasks = useMemo(() => {
    let result = [...tasks]

    // 排序
    result.sort((a, b) => {
      let aVal: string | number = ''
      let bVal: string | number = ''

      switch (filters.sortBy) {
        case 'name':
          aVal = a.name
          bVal = b.name
          break
        case 'created_at':
          aVal = new Date(a.created_at).getTime()
          bVal = new Date(b.created_at).getTime()
          break
        case 'updated_at':
        default:
          aVal = new Date(a.updated_at).getTime()
          bVal = new Date(b.updated_at).getTime()
      }

      if (typeof aVal === 'string') {
        return filters.sortOrder === 'asc'
          ? aVal.localeCompare(bVal as string)
          : (bVal as string).localeCompare(aVal)
      }
      return filters.sortOrder === 'asc' ? aVal - (bVal as number) : (bVal as number) - aVal
    })

    return result
  }, [tasks, filters.sortBy, filters.sortOrder])

  // 分页后的任务
  const paginatedTasks = useMemo(() => {
    const start = (page - 1) * pageSize
    return filteredTasks.slice(start, start + pageSize)
  }, [filteredTasks, page, pageSize])

  // 全选/取消全选
  const toggleSelectAll = useCallback(() => {
    if (selectedIds.length === paginatedTasks.length) {
      setSelectedIds([])
    } else {
      setSelectedIds(paginatedTasks.map(t => t.id))
    }
  }, [selectedIds.length, paginatedTasks])

  // 切换单个选中
  const toggleSelect = useCallback((id: string) => {
    setSelectedIds(prev =>
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    )
  }, [])

  // 批量删除
  const batchDelete = useCallback(async () => {
    if (selectedIds.length === 0) return
    await tasksApi.batchDelete(selectedIds)
    setSelectedIds([])
    await fetchTasks()
  }, [selectedIds, fetchTasks])

  // 批量更新状态
  const batchUpdateStatus = useCallback(async (status: 'draft' | 'ready') => {
    if (selectedIds.length === 0) return
    await tasksApi.batchUpdateStatus(selectedIds, status)
    setSelectedIds([])
    await fetchTasks()
  }, [selectedIds, fetchTasks])

  // 更新筛选条件
  const updateFilter = useCallback(<K extends keyof Filters>(key: K, value: Filters[K]) => {
    setFilters(prev => ({ ...prev, [key]: value }))
    setPage(1) // 重置页码
  }, [])

  return {
    tasks: paginatedTasks,
    allTasks: tasks,
    filteredTasks,
    total: filteredTasks.length,
    loading,
    filters,
    selectedIds,
    page,
    pageSize,
    setPage,
    setFilters,
    updateFilter,
    setSelectedIds,
    toggleSelectAll,
    toggleSelect,
    fetchTasks,
    batchDelete,
    batchUpdateStatus,
  }
}
```

**Step 2: 验证编译**

```bash
cd /Users/huhu/project/weberpagent/frontend && npx tsc --noEmit
```

Expected: No errors

---

## Task 6: 创建任务列表组件

**Files:**
- Create: `frontend/src/components/TaskList/index.ts`
- Create: `frontend/src/components/TaskList/TaskListHeader.tsx`
- Create: `frontend/src/components/TaskList/TaskFilters.tsx`
- Create: `frontend/src/components/TaskList/TaskTable.tsx`
- Create: `frontend/src/components/TaskList/TaskRow.tsx`
- Create: `frontend/src/components/TaskList/BatchActions.tsx`

**Step 1: 创建 TaskListHeader**

```typescript
// frontend/src/components/TaskList/TaskListHeader.tsx
import { Plus } from 'lucide-react'
import { Button } from '../Button'

interface TaskListHeaderProps {
  onCreateClick: () => void
}

export function TaskListHeader({ onCreateClick }: TaskListHeaderProps) {
  return (
    <div className="flex items-center justify-between mb-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">任务管理</h1>
        <p className="text-gray-500 mt-1">创建和管理 UI 自动化测试任务</p>
      </div>
      <Button onClick={onCreateClick}>
        <Plus className="w-4 h-4 mr-1" />
        新建任务
      </Button>
    </div>
  )
}
```

**Step 2: 创建 TaskFilters**

```typescript
// frontend/src/components/TaskList/TaskFilters.tsx
import { Search, ChevronDown } from 'lucide-react'
import type { Filters } from '../../hooks/useTasks'

interface TaskFiltersProps {
  filters: Filters
  onFilterChange: <K extends keyof Filters>(key: K, value: Filters[K]) => void
}

export function TaskFilters({ filters, onFilterChange }: TaskFiltersProps) {
  return (
    <div className="flex items-center gap-4 mb-4">
      {/* 搜索框 */}
      <div className="relative flex-1 max-w-sm">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          placeholder="搜索任务名称..."
          value={filters.search}
          onChange={e => onFilterChange('search', e.target.value)}
          className="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      {/* 状态筛选 */}
      <select
        value={filters.status}
        onChange={e => onFilterChange('status', e.target.value as Filters['status'])}
        className="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="all">全部状态</option>
        <option value="draft">草稿</option>
        <option value="ready">就绪</option>
      </select>

      {/* 排序 */}
      <div className="flex items-center gap-2">
        <select
          value={filters.sortBy}
          onChange={e => onFilterChange('sortBy', e.target.value as Filters['sortBy'])}
          className="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="updated_at">按更新时间</option>
          <option value="created_at">按创建时间</option>
          <option value="name">按名称</option>
        </select>
        <button
          onClick={() => onFilterChange('sortOrder', filters.sortOrder === 'asc' ? 'desc' : 'asc')}
          className="px-3 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50"
        >
          {filters.sortOrder === 'asc' ? '↑ 升序' : '↓ 降序'}
        </button>
      </div>
    </div>
  )
}
```

**Step 3: 创建 TaskRow**

```typescript
// frontend/src/components/TaskList/TaskRow.tsx
import { Play, Pencil, Trash2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import type { Task } from '../../types'
import { StatusBadge } from '../shared'

interface TaskRowProps {
  task: Task
  selected: boolean
  onSelect: () => void
  onEdit: () => void
  onDelete: () => void
}

export function TaskRow({ task, selected, onSelect, onEdit, onDelete }: TaskRowProps) {
  const navigate = useNavigate()

  const handleExecute = (e: React.MouseEvent) => {
    e.stopPropagation()
    // TODO: 调用执行 API
    console.log('Execute task:', task.id)
  }

  const handleEdit = (e: React.MouseEvent) => {
    e.stopPropagation()
    onEdit()
  }

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation()
    onDelete()
  }

  const handleRowClick = () => {
    navigate(`/tasks/${task.id}`)
  }

  // 提取域名
  const domain = (() => {
    try {
      return new URL(task.target_url).hostname
    } catch {
      return task.target_url
    }
  })()

  return (
    <tr
      onClick={handleRowClick}
      className="border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition-colors"
    >
      <td className="px-4 py-3" onClick={e => e.stopPropagation()}>
        <input
          type="checkbox"
          checked={selected}
          onChange={onSelect}
          className="w-4 h-4 rounded border-gray-300 text-blue-500 focus:ring-blue-500"
        />
      </td>
      <td className="px-4 py-3">
        <div className="font-medium text-gray-900">{task.name}</div>
        <div className="text-sm text-gray-500 truncate max-w-xs">{task.description}</div>
      </td>
      <td className="px-4 py-3 text-gray-500 text-sm">{domain}</td>
      <td className="px-4 py-3">
        <StatusBadge status={task.status} />
      </td>
      <td className="px-4 py-3 text-gray-500 text-sm">{task.max_steps}</td>
      <td className="px-4 py-3">
        <div className="flex items-center gap-1">
          <button
            onClick={handleExecute}
            className="p-1.5 rounded hover:bg-gray-100 text-gray-500 hover:text-blue-500"
            title="立即执行"
          >
            <Play className="w-4 h-4" />
          </button>
          <button
            onClick={handleEdit}
            className="p-1.5 rounded hover:bg-gray-100 text-gray-500 hover:text-gray-700"
            title="编辑"
          >
            <Pencil className="w-4 h-4" />
          </button>
          <button
            onClick={handleDelete}
            className="p-1.5 rounded hover:bg-gray-100 text-gray-500 hover:text-red-500"
            title="删除"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </td>
    </tr>
  )
}
```

**Step 4: 创建 TaskTable**

```typescript
// frontend/src/components/TaskList/TaskTable.tsx
import type { Task } from '../../types'
import { TaskRow } from './TaskRow'

interface TaskTableProps {
  tasks: Task[]
  selectedIds: string[]
  onSelectAll: () => void
  onToggleSelect: (id: string) => void
  onEdit: (task: Task) => void
  onDelete: (task: Task) => void
}

export function TaskTable({
  tasks,
  selectedIds,
  onSelectAll,
  onToggleSelect,
  onEdit,
  onDelete,
}: TaskTableProps) {
  const allSelected = tasks.length > 0 && selectedIds.length === tasks.length
  const someSelected = selectedIds.length > 0 && selectedIds.length < tasks.length

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-50 border-b border-gray-200">
          <tr>
            <th className="px-4 py-3 text-left">
              <input
                type="checkbox"
                checked={allSelected}
                ref={el => {
                  if (el) el.indeterminate = someSelected
                }}
                onChange={onSelectAll}
                className="w-4 h-4 rounded border-gray-300 text-blue-500 focus:ring-blue-500"
              />
            </th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">名称</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">目标 URL</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">状态</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">步数</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">操作</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map(task => (
            <TaskRow
              key={task.id}
              task={task}
              selected={selectedIds.includes(task.id)}
              onSelect={() => onToggleSelect(task.id)}
              onEdit={() => onEdit(task)}
              onDelete={() => onDelete(task)}
            />
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

**Step 5: 创建 BatchActions**

```typescript
// frontend/src/components/TaskList/BatchActions.tsx
import { Trash2, CheckCircle } from 'lucide-react'

interface BatchActionsProps {
  selectedCount: number
  onBatchDelete: () => void
  onBatchSetReady: () => void
}

export function BatchActions({ selectedCount, onBatchDelete, onBatchSetReady }: BatchActionsProps) {
  if (selectedCount === 0) return null

  return (
    <div className="flex items-center gap-4 px-4 py-2 bg-blue-50 border-y border-blue-100">
      <span className="text-sm text-blue-700">已选中 {selectedCount} 项</span>
      <div className="flex items-center gap-2">
        <button
          onClick={onBatchSetReady}
          className="flex items-center gap-1 px-3 py-1.5 text-sm text-blue-700 hover:bg-blue-100 rounded-lg transition-colors"
        >
          <CheckCircle className="w-4 h-4" />
          设为就绪
        </button>
        <button
          onClick={onBatchDelete}
          className="flex items-center gap-1 px-3 py-1.5 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
        >
          <Trash2 className="w-4 h-4" />
          批量删除
        </button>
      </div>
    </div>
  )
}
```

**Step 6: 创建导出文件**

```typescript
// frontend/src/components/TaskList/index.ts
export { TaskListHeader } from './TaskListHeader'
export { TaskFilters } from './TaskFilters'
export { TaskTable } from './TaskTable'
export { TaskRow } from './TaskRow'
export { BatchActions } from './BatchActions'
```

**Step 7: 验证编译**

```bash
cd /Users/huhu/project/weberpagent/frontend && npx tsc --noEmit
```

Expected: No errors

---

## Task 7: 创建任务表单弹窗

**Files:**
- Create: `frontend/src/components/TaskModal/index.ts`
- Create: `frontend/src/components/TaskModal/TaskForm.tsx`
- Create: `frontend/src/components/TaskModal/TaskFormModal.tsx`

**Step 1: 创建 TaskForm**

```typescript
// frontend/src/components/TaskModal/TaskForm.tsx
import { useState, useEffect } from 'react'
import type { Task, CreateTaskDto } from '../../types'

interface TaskFormProps {
  initialData?: Task
  onSubmit: (data: CreateTaskDto) => void
  onCancel: () => void
  loading?: boolean
  mode: 'create' | 'edit'
}

interface FormData {
  name: string
  description: string
  target_url: string
  max_steps: number
}

interface FormErrors {
  name?: string
  target_url?: string
}

export function TaskForm({ initialData, onSubmit, onCancel, loading, mode }: TaskFormProps) {
  const [formData, setFormData] = useState<FormData>({
    name: initialData?.name || '',
    description: initialData?.description || '',
    target_url: initialData?.target_url || '',
    max_steps: initialData?.max_steps || 20,
  })
  const [errors, setErrors] = useState<FormErrors>({})

  useEffect(() => {
    if (initialData) {
      setFormData({
        name: initialData.name,
        description: initialData.description,
        target_url: initialData.target_url,
        max_steps: initialData.max_steps,
      })
    }
  }, [initialData])

  const validate = (): boolean => {
    const newErrors: FormErrors = {}

    if (!formData.name.trim()) {
      newErrors.name = '请输入任务名称'
    } else if (formData.name.length > 50) {
      newErrors.name = '任务名称不能超过 50 个字符'
    }

    if (!formData.target_url.trim()) {
      newErrors.target_url = '请输入目标 URL'
    } else {
      try {
        new URL(formData.target_url)
      } catch {
        newErrors.target_url = '请输入有效的 URL 格式'
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (validate()) {
      onSubmit(formData)
    }
  }

  const handleStepsChange = (delta: number) => {
    const newSteps = Math.max(1, Math.min(50, formData.max_steps + delta))
    setFormData(prev => ({ ...prev, max_steps: newSteps }))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* 任务名称 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          任务名称 <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          value={formData.name}
          onChange={e => setFormData(prev => ({ ...prev, name: e.target.value }))}
          placeholder="例如：用户登录测试"
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.name ? 'border-red-500' : 'border-gray-200'
          }`}
        />
        {errors.name && <p className="mt-1 text-sm text-red-500">{errors.name}</p>}
      </div>

      {/* 任务描述 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">任务描述</label>
        <textarea
          value={formData.description}
          onChange={e => setFormData(prev => ({ ...prev, description: e.target.value }))}
          placeholder="描述任务的目标和步骤..."
          rows={3}
          className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        />
      </div>

      {/* 目标 URL */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          目标 URL <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          value={formData.target_url}
          onChange={e => setFormData(prev => ({ ...prev, target_url: e.target.value }))}
          placeholder="https://example.com/login"
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.target_url ? 'border-red-500' : 'border-gray-200'
          }`}
        />
        {errors.target_url && <p className="mt-1 text-sm text-red-500">{errors.target_url}</p>}
      </div>

      {/* 最大步数 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          最大步数
        </label>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => handleStepsChange(-5)}
            className="w-8 h-8 flex items-center justify-center border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            -5
          </button>
          <button
            type="button"
            onClick={() => handleStepsChange(-1)}
            className="w-8 h-8 flex items-center justify-center border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            -1
          </button>
          <span className="w-16 text-center font-medium">{formData.max_steps}</span>
          <button
            type="button"
            onClick={() => handleStepsChange(1)}
            className="w-8 h-8 flex items-center justify-center border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            +1
          </button>
          <button
            type="button"
            onClick={() => handleStepsChange(5)}
            className="w-8 h-8 flex items-center justify-center border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            +5
          </button>
          <span className="text-sm text-gray-500 ml-2">范围 1-50</span>
        </div>
      </div>

      {/* 按钮组 */}
      <div className="flex justify-end gap-3 pt-4 border-t border-gray-100">
        <button
          type="button"
          onClick={onCancel}
          disabled={loading}
          className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg disabled:opacity-50"
        >
          取消
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 font-medium"
        >
          {loading ? '处理中...' : mode === 'create' ? '创建任务' : '保存修改'}
        </button>
      </div>
    </form>
  )
}
```

**Step 2: 创建 TaskFormModal**

```typescript
// frontend/src/components/TaskModal/TaskFormModal.tsx
import { X } from 'lucide-react'
import type { Task, CreateTaskDto } from '../../types'
import { TaskForm } from './TaskForm'

interface TaskFormModalProps {
  open: boolean
  onClose: () => void
  mode: 'create' | 'edit'
  task?: Task
  onSubmit: (data: CreateTaskDto) => Promise<void>
}

export function TaskFormModal({ open, onClose, mode, task, onSubmit }: TaskFormModalProps) {
  const [loading, setLoading] = useState(false)

  if (!open) return null

  const handleSubmit = async (data: CreateTaskDto) => {
    setLoading(true)
    try {
      await onSubmit(data)
      onClose()
    } catch (error) {
      console.error('Failed to submit:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/50" onClick={onClose} />
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-lg mx-4 max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">
            {mode === 'create' ? '新建任务' : '编辑任务'}
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="p-6">
          <TaskForm
            initialData={task}
            mode={mode}
            onSubmit={handleSubmit}
            onCancel={onClose}
            loading={loading}
          />
        </div>
      </div>
    </div>
  )
}
```

**Step 3: 添加缺少的 import**

```typescript
// 修复 TaskFormModal.tsx 顶部
import { useState } from 'react'
import { X } from 'lucide-react'
import type { Task, CreateTaskDto } from '../../types'
import { TaskForm } from './TaskForm'
```

**Step 4: 创建导出文件**

```typescript
// frontend/src/components/TaskModal/index.ts
export { TaskForm } from './TaskForm'
export { TaskFormModal } from './TaskFormModal'
```

**Step 5: 验证编译**

```bash
cd /Users/huhu/project/weberpagent/frontend && npx tsc --noEmit
```

Expected: No errors

---

## Task 8: 创建任务详情组件

**Files:**
- Create: `frontend/src/components/TaskDetail/index.ts`
- Create: `frontend/src/components/TaskDetail/TaskHeader.tsx`
- Create: `frontend/src/components/TaskDetail/TaskInfo.tsx`
- Create: `frontend/src/components/TaskDetail/ConfigPanel.tsx`
- Create: `frontend/src/components/TaskDetail/RunHistory.tsx`
- Create: `frontend/src/components/TaskDetail/StatsChart.tsx`

**Step 1: 创建 TaskHeader**

```typescript
// frontend/src/components/TaskDetail/TaskHeader.tsx
import { ArrowLeft, Play, Pencil, Trash2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import type { Task } from '../../types'
import { Button } from '../Button'
import { StatusBadge } from '../shared'

interface TaskHeaderProps {
  task: Task
  onEdit: () => void
  onDelete: () => void
  onExecute: () => void
}

export function TaskHeader({ task, onEdit, onDelete, onExecute }: TaskHeaderProps) {
  const navigate = useNavigate()

  return (
    <div className="mb-6">
      <button
        onClick={() => navigate('/tasks')}
        className="flex items-center gap-1 text-gray-500 hover:text-gray-700 mb-4"
      >
        <ArrowLeft className="w-4 h-4" />
        返回列表
      </button>

      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-2xl font-semibold text-gray-900">{task.name}</h1>
            <StatusBadge status={task.status} />
          </div>
          <p className="text-gray-500">{task.description}</p>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="secondary" onClick={onExecute}>
            <Play className="w-4 h-4 mr-1" />
            立即执行
          </Button>
          <Button variant="secondary" onClick={onEdit}>
            <Pencil className="w-4 h-4 mr-1" />
            编辑
          </Button>
          <Button variant="secondary" onClick={onDelete} className="text-red-600 hover:bg-red-50">
            <Trash2 className="w-4 h-4 mr-1" />
            删除
          </Button>
        </div>
      </div>
    </div>
  )
}
```

**Step 2: 创建 TaskInfo**

```typescript
// frontend/src/components/TaskDetail/TaskInfo.tsx
import { Globe, Hash, Clock, Calendar } from 'lucide-react'
import type { Task } from '../../types'

interface TaskInfoProps {
  task: Task
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function TaskInfo({ task }: TaskInfoProps) {
  const infoItems = [
    { icon: Globe, label: '目标 URL', value: task.target_url },
    { icon: Hash, label: '最大步数', value: task.max_steps.toString() },
    { icon: Calendar, label: '创建时间', value: formatDate(task.created_at) },
    { icon: Clock, label: '更新时间', value: formatDate(task.updated_at) },
  ]

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 mb-4">
      <h3 className="text-base font-medium text-gray-900 mb-4">基本信息</h3>
      <div className="grid grid-cols-2 gap-4">
        {infoItems.map(({ icon: Icon, label, value }) => (
          <div key={label} className="flex items-start gap-3">
            <Icon className="w-4 h-4 text-gray-400 mt-0.5" />
            <div>
              <div className="text-sm text-gray-500">{label}</div>
              <div className="text-gray-900 break-all">{value}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

**Step 3: 创建 ConfigPanel**

```typescript
// frontend/src/components/TaskDetail/ConfigPanel.tsx
import { useState } from 'react'
import { ChevronRight, ChevronDown } from 'lucide-react'
import type { Task } from '../../types'

interface ConfigPanelProps {
  task: Task
}

export function ConfigPanel({ task }: ConfigPanelProps) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className="bg-white rounded-xl border border-gray-200 mb-4 overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-5 py-4 flex items-center gap-2 hover:bg-gray-50 transition-colors"
      >
        {expanded ? (
          <ChevronDown className="w-4 h-4 text-gray-400" />
        ) : (
          <ChevronRight className="w-4 h-4 text-gray-400" />
        )}
        <span className="font-medium text-gray-900">配置详情</span>
      </button>

      {expanded && (
        <div className="px-5 pb-4 border-t border-gray-100">
          <div className="pt-4 space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">任务 ID</span>
              <span className="text-gray-900 font-mono">{task.id}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">状态</span>
              <span className="text-gray-900">{task.status === 'ready' ? '就绪' : '草稿'}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">超时设置</span>
              <span className="text-gray-900">30 秒/步</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">重试次数</span>
              <span className="text-gray-900">3 次</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">截图保存</span>
              <span className="text-gray-900">开启</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
```

**Step 4: 创建 RunHistory**

```typescript
// frontend/src/components/TaskDetail/RunHistory.tsx
import { useNavigate } from 'react-router-dom'
import type { Run } from '../../types'
import { StatusBadge, LoadingSpinner, EmptyState } from '../shared'

interface RunHistoryProps {
  runs: Run[]
  loading: boolean
}

function formatDuration(ms: number): string {
  const seconds = Math.floor(ms / 1000)
  if (seconds < 60) return `${seconds}s`
  const minutes = Math.floor(seconds / 60)
  const remainSeconds = seconds % 60
  return `${minutes}m ${remainSeconds}s`
}

function formatDateTime(dateStr: string): string {
  return new Date(dateStr).toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function RunHistory({ runs, loading }: RunHistoryProps) {
  const navigate = useNavigate()

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <LoadingSpinner />
      </div>
    )
  }

  if (runs.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h3 className="text-base font-medium text-gray-900 mb-4">执行历史</h3>
        <EmptyState message="暂无执行记录" />
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h3 className="text-base font-medium text-gray-900 mb-4">执行历史</h3>
      <div className="space-y-2">
        {runs.map(run => (
          <div
            key={run.id}
            onClick={() => navigate(`/runs/${run.id}`)}
            className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
          >
            <div className="flex items-center gap-3">
              <StatusBadge status={run.status} />
              <span className="text-gray-900">{formatDateTime(run.started_at)}</span>
            </div>
            <div className="flex items-center gap-4 text-sm text-gray-500">
              <span>耗时 {formatDuration(run.steps.reduce((sum, s) => sum + s.duration_ms, 0))}</span>
              <span>步数 {run.steps.filter(s => s.status === 'success').length}/{run.steps.length}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

**Step 5: 创建 StatsChart**

```typescript
// frontend/src/components/TaskDetail/StatsChart.tsx
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'

interface StatsChartProps {
  data: { date: string; runs: number; successRate: number }[]
  loading: boolean
}

export function StatsChart({ data, loading }: StatsChartProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-5 mb-4 h-64 flex items-center justify-center">
        <span className="text-gray-400">加载中...</span>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 mb-4">
      <h3 className="text-base font-medium text-gray-900 mb-4">执行统计</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="date" stroke="#9ca3af" fontSize={12} />
            <YAxis
              yAxisId="left"
              stroke="#9ca3af"
              fontSize={12}
              label={{ value: '执行次数', angle: -90, position: 'insideLeft', fill: '#9ca3af' }}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              stroke="#9ca3af"
              fontSize={12}
              domain={[0, 100]}
              label={{ value: '成功率%', angle: 90, position: 'insideRight', fill: '#9ca3af' }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fff',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
              }}
            />
            <Legend />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="runs"
              name="执行次数"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={{ fill: '#3b82f6', strokeWidth: 2 }}
              activeDot={{ r: 6 }}
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="successRate"
              name="成功率%"
              stroke="#22c55e"
              strokeWidth={2}
              dot={{ fill: '#22c55e', strokeWidth: 2 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
```

**Step 6: 创建导出文件**

```typescript
// frontend/src/components/TaskDetail/index.ts
export { TaskHeader } from './TaskHeader'
export { TaskInfo } from './TaskInfo'
export { ConfigPanel } from './ConfigPanel'
export { RunHistory } from './RunHistory'
export { StatsChart } from './StatsChart'
```

**Step 7: 验证编译**

```bash
cd /Users/huhu/project/weberpagent/frontend && npx tsc --noEmit
```

Expected: No errors

---

## Task 9: 更新 Tasks 页面

**Files:**
- Modify: `frontend/src/pages/Tasks.tsx`

**Step 1: 更新 Tasks 页面**

```typescript
// frontend/src/pages/Tasks.tsx
import { useState } from 'react'
import { useTasks } from '../hooks/useTasks'
import {
  TaskListHeader,
  TaskFilters,
  TaskTable,
  BatchActions,
} from '../components/TaskList'
import { TaskFormModal } from '../components/TaskModal'
import { Pagination, EmptyState, LoadingSpinner, ConfirmModal } from '../components/shared'
import { tasksApi } from '../api/tasks'
import type { Task, CreateTaskDto } from '../types'

export function Tasks() {
  const {
    tasks,
    total,
    loading,
    filters,
    selectedIds,
    page,
    pageSize,
    setPage,
    updateFilter,
    toggleSelectAll,
    toggleSelect,
    fetchTasks,
    batchDelete,
    batchUpdateStatus,
  } = useTasks()

  // 弹窗状态
  const [modalOpen, setModalOpen] = useState(false)
  const [modalMode, setModalMode] = useState<'create' | 'edit'>('create')
  const [editingTask, setEditingTask] = useState<Task | undefined>()

  // 删除确认弹窗
  const [deleteConfirm, setDeleteConfirm] = useState<Task | null>(null)
  const [batchDeleteConfirm, setBatchDeleteConfirm] = useState(false)
  const [deleting, setDeleting] = useState(false)

  // 打开创建弹窗
  const handleCreate = () => {
    setModalMode('create')
    setEditingTask(undefined)
    setModalOpen(true)
  }

  // 打开编辑弹窗
  const handleEdit = (task: Task) => {
    setModalMode('edit')
    setEditingTask(task)
    setModalOpen(true)
  }

  // 提交表单
  const handleSubmit = async (data: CreateTaskDto) => {
    if (modalMode === 'create') {
      await tasksApi.create(data)
    } else if (editingTask) {
      await tasksApi.update(editingTask.id, data)
    }
    await fetchTasks()
  }

  // 删除任务
  const handleDelete = async () => {
    if (!deleteConfirm) return
    setDeleting(true)
    try {
      await tasksApi.delete(deleteConfirm.id)
      await fetchTasks()
    } finally {
      setDeleting(false)
      setDeleteConfirm(null)
    }
  }

  // 批量删除
  const handleBatchDelete = async () => {
    setDeleting(true)
    try {
      await batchDelete()
    } finally {
      setDeleting(false)
      setBatchDeleteConfirm(false)
    }
  }

  // 批量设为就绪
  const handleBatchSetReady = async () => {
    await batchUpdateStatus('ready')
  }

  if (loading && tasks.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <div>
      <TaskListHeader onCreateClick={handleCreate} />

      <TaskFilters filters={filters} onFilterChange={updateFilter} />

      <BatchActions
        selectedCount={selectedIds.length}
        onBatchDelete={() => setBatchDeleteConfirm(true)}
        onBatchSetReady={handleBatchSetReady}
      />

      {tasks.length === 0 ? (
        <div className="bg-white rounded-xl border border-gray-200 p-8">
          <EmptyState
            message={filters.search || filters.status !== 'all' ? '没有找到匹配的任务' : '暂无任务'}
            action={
              !filters.search && filters.status === 'all' && (
                <button onClick={handleCreate} className="text-blue-500 hover:text-blue-600">
                  创建第一个任务
                </button>
              )
            }
          />
        </div>
      ) : (
        <TaskTable
          tasks={tasks}
          selectedIds={selectedIds}
          onSelectAll={toggleSelectAll}
          onToggleSelect={toggleSelect}
          onEdit={handleEdit}
          onDelete={task => setDeleteConfirm(task)}
        />
      )}

      <Pagination total={total} page={page} pageSize={pageSize} onChange={setPage} />

      {/* 任务表单弹窗 */}
      <TaskFormModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        mode={modalMode}
        task={editingTask}
        onSubmit={handleSubmit}
      />

      {/* 删除确认弹窗 */}
      <ConfirmModal
        open={!!deleteConfirm}
        title="删除任务"
        message={`确定要删除任务「${deleteConfirm?.name}」吗？此操作无法撤销。`}
        confirmText="删除"
        variant="danger"
        onConfirm={handleDelete}
        onCancel={() => setDeleteConfirm(null)}
        loading={deleting}
      />

      {/* 批量删除确认弹窗 */}
      <ConfirmModal
        open={batchDeleteConfirm}
        title="批量删除"
        message={`确定要删除选中的 ${selectedIds.length} 个任务吗？此操作无法撤销。`}
        confirmText="删除"
        variant="danger"
        onConfirm={handleBatchDelete}
        onCancel={() => setBatchDeleteConfirm(false)}
        loading={deleting}
      />
    </div>
  )
}
```

**Step 2: 验证编译**

```bash
cd /Users/huhu/project/weberpagent/frontend && npx tsc --noEmit
```

Expected: No errors

---

## Task 10: 更新 TaskDetail 页面

**Files:**
- Modify: `frontend/src/pages/TaskDetail.tsx`

**Step 1: 更新 TaskDetail 页面**

```typescript
// frontend/src/pages/TaskDetail.tsx
import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { tasksApi } from '../api/tasks'
import type { Task, Run, CreateTaskDto } from '../types'
import {
  TaskHeader,
  TaskInfo,
  ConfigPanel,
  RunHistory,
  StatsChart,
} from '../components/TaskDetail'
import { TaskFormModal } from '../components/TaskModal'
import { ConfirmModal, LoadingSpinner } from '../components/shared'

export function TaskDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const [task, setTask] = useState<Task | null>(null)
  const [runs, setRuns] = useState<Run[]>([])
  const [stats, setStats] = useState<{ date: string; runs: number; successRate: number }[]>([])
  const [loading, setLoading] = useState(true)
  const [runsLoading, setRunsLoading] = useState(true)
  const [statsLoading, setStatsLoading] = useState(true)

  // 弹窗状态
  const [editModalOpen, setEditModalOpen] = useState(false)
  const [deleteConfirm, setDeleteConfirm] = useState(false)
  const [deleting, setDeleting] = useState(false)

  // 加载任务详情
  useEffect(() => {
    if (!id) return

    const loadTask = async () => {
      setLoading(true)
      try {
        const data = await tasksApi.get(id)
        setTask(data)
      } catch (error) {
        console.error('Failed to load task:', error)
      } finally {
        setLoading(false)
      }
    }

    loadTask()
  }, [id])

  // 加载执行历史
  useEffect(() => {
    if (!id) return

    const loadRuns = async () => {
      setRunsLoading(true)
      try {
        const data = await tasksApi.getRuns(id)
        setRuns(data)
      } catch (error) {
        console.error('Failed to load runs:', error)
      } finally {
        setRunsLoading(false)
      }
    }

    loadRuns()
  }, [id])

  // 加载统计数据
  useEffect(() => {
    if (!id) return

    const loadStats = async () => {
      setStatsLoading(true)
      try {
        const data = await tasksApi.getStats(id)
        setStats(data)
      } catch (error) {
        console.error('Failed to load stats:', error)
      } finally {
        setStatsLoading(false)
      }
    }

    loadStats()
  }, [id])

  // 执行任务
  const handleExecute = () => {
    // TODO: 调用执行 API，然后跳转到执行监控页
    console.log('Execute task:', id)
    // navigate(`/runs/${runId}`)
  }

  // 更新任务
  const handleUpdate = async (data: CreateTaskDto) => {
    if (!id) return
    const updated = await tasksApi.update(id, data)
    setTask(updated)
  }

  // 删除任务
  const handleDelete = async () => {
    if (!id) return
    setDeleting(true)
    try {
      await tasksApi.delete(id)
      navigate('/tasks')
    } finally {
      setDeleting(false)
      setDeleteConfirm(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!task) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">任务不存在</p>
        <button
          onClick={() => navigate('/tasks')}
          className="mt-4 text-blue-500 hover:text-blue-600"
        >
          返回列表
        </button>
      </div>
    )
  }

  return (
    <div>
      <TaskHeader
        task={task}
        onEdit={() => setEditModalOpen(true)}
        onDelete={() => setDeleteConfirm(true)}
        onExecute={handleExecute}
      />

      <TaskInfo task={task} />
      <ConfigPanel task={task} />
      <StatsChart data={stats} loading={statsLoading} />
      <RunHistory runs={runs} loading={runsLoading} />

      {/* 编辑弹窗 */}
      <TaskFormModal
        open={editModalOpen}
        onClose={() => setEditModalOpen(false)}
        mode="edit"
        task={task}
        onSubmit={handleUpdate}
      />

      {/* 删除确认弹窗 */}
      <ConfirmModal
        open={deleteConfirm}
        title="删除任务"
        message={`确定要删除任务「${task.name}」吗？此操作无法撤销。`}
        confirmText="删除"
        variant="danger"
        onConfirm={handleDelete}
        onCancel={() => setDeleteConfirm(false)}
        loading={deleting}
      />
    </div>
  )
}
```

**Step 2: 验证编译**

```bash
cd /Users/huhu/project/weberpagent/frontend && npx tsc --noEmit
```

Expected: No errors

---

## Task 11: 运行并验证

**Step 1: 启动开发服务器**

```bash
cd /Users/huhu/project/weberpagent/frontend && npm run dev
```

**Step 2: 手动验证功能**

1. 访问 http://localhost:5173/tasks
2. 验证任务列表显示
3. 验证搜索、筛选、排序功能
4. 验证新建任务弹窗
5. 验证编辑任务
6. 验证删除任务
7. 验证批量操作
8. 点击任务进入详情页
9. 验证任务详情显示
10. 验证统计图表
11. 验证执行历史列表

**Step 3: 提交代码**

```bash
cd /Users/huhu/project/weberpagent
git add frontend/
git commit -m "$(cat <<'EOF'
feat: 实现 Phase 3 任务管理功能

- 任务列表页：搜索、筛选、排序、分页、批量操作
- 任务表单：模态弹窗、创建/编辑复用
- 任务详情：基本信息、配置详情、执行历史、统计图表
- Mock 数据层，便于后续对接真实 API
- 共享组件：StatusBadge、Pagination、EmptyState、ConfirmModal

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## 验收清单

- [ ] 任务列表页正常显示
- [ ] 搜索功能正常
- [ ] 状态筛选正常
- [ ] 排序功能正常
- [ ] 分页功能正常
- [ ] 新建任务功能正常
- [ ] 编辑任务功能正常
- [ ] 删除任务功能正常
- [ ] 批量删除功能正常
- [ ] 批量设为就绪功能正常
- [ ] 任务详情页正常显示
- [ ] 统计图表正常显示
- [ ] 执行历史列表正常显示
- [ ] 点击执行历史可跳转
