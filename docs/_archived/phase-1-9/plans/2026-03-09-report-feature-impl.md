# 报告查看功能实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现前端报告列表页和报告详情页，支持状态筛选、日期筛选、分页、步骤展开查看。

**Architecture:** 报告列表页使用筛选 + 表格 + 分页布局；报告详情页使用上下布局（摘要卡片 + 可展开步骤列表）。复用现有组件 StatusBadge、Pagination、EmptyState、ImageViewer。

**Tech Stack:** React 18 + TypeScript + Tailwind CSS + React Router

---

## Task 1: 创建报告 Mock 数据

**Files:**
- Create: `frontend/src/api/mock/reports.ts`

**Step 1: 创建 reports.ts 文件**

```typescript
import type { Report, Run, Step } from '../../types'

// 基于 mockRuns 生成报告列表
function generateReportsFromRuns(): Report[] {
  const { mockRuns } = require('./runs')

  return mockRuns.map(run => ({
    id: `report-${run.id}`,
    run_id: run.id,
    task_name: `任务 ${run.task_id}`,
    status: run.status === 'success' ? 'success' : 'failed',
    total_steps: run.steps.length,
    success_steps: run.steps.filter(s => s.status === 'success').length,
    failed_steps: run.steps.filter(s => s.status === 'failed').length,
    duration_ms: run.steps.reduce((sum, s) => sum + s.duration_ms, 0),
    created_at: run.finished_at || run.started_at,
  }))
}

// 生成更多模拟报告数据
function generateMoreReports(): Report[] {
  const taskNames = [
    '登录流程测试',
    '表单提交测试',
    '搜索功能测试',
    '购物车测试',
    '用户注册测试',
  ]

  const reports: Report[] = []
  const now = new Date()

  for (let i = 10; i <= 30; i++) {
    const daysAgo = Math.floor(Math.random() * 30)
    const date = new Date(now)
    date.setDate(date.getDate() - daysAgo)

    const totalSteps = Math.floor(Math.random() * 15) + 3
    const failedSteps = Math.random() > 0.7 ? Math.floor(Math.random() * 3) : 0
    const successSteps = totalSteps - failedSteps

    reports.push({
      id: `report-r${i}`,
      run_id: `r${i}`,
      task_name: taskNames[Math.floor(Math.random() * taskNames.length)],
      status: failedSteps > 0 ? 'failed' : 'success',
      total_steps: totalSteps,
      success_steps: successSteps,
      failed_steps: failedSteps,
      duration_ms: Math.floor(Math.random() * 120000) + 10000,
      created_at: date.toISOString(),
    })
  }

  return reports
}

export const mockReports: Report[] = [
  ...generateReportsFromRuns(),
  ...generateMoreReports(),
]

// 获取报告列表（支持筛选和分页）
export function getReports(params: {
  status?: 'all' | 'success' | 'failed'
  dateRange?: 'all' | 'today' | '7days' | '30days'
  page?: number
  pageSize?: number
}): { reports: Report[]; total: number } {
  const { status = 'all', dateRange = 'all', page = 1, pageSize = 10 } = params

  let filtered = [...mockReports]

  // 状态筛选
  if (status !== 'all') {
    filtered = filtered.filter(r => r.status === status)
  }

  // 日期筛选
  if (dateRange !== 'all') {
    const now = new Date()
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())

    filtered = filtered.filter(r => {
      const reportDate = new Date(r.created_at)
      switch (dateRange) {
        case 'today':
          return reportDate >= today
        case '7days':
          const weekAgo = new Date(today)
          weekAgo.setDate(weekAgo.getDate() - 7)
          return reportDate >= weekAgo
        case '30days':
          const monthAgo = new Date(today)
          monthAgo.setDate(monthAgo.getDate() - 30)
          return reportDate >= monthAgo
        default:
          return true
      }
    })
  }

  // 按时间倒序
  filtered.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())

  const total = filtered.length
  const start = (page - 1) * pageSize
  const reports = filtered.slice(start, start + pageSize)

  return { reports, total }
}

// 获取单个报告详情（返回对应的 Run）
export function getReportDetail(reportId: string): { report: Report; run: Run } | null {
  const report = mockReports.find(r => r.id === reportId)
  if (!report) return null

  const { mockRuns } = require('./runs')
  const run = mockRuns.find((r: Run) => r.id === report.run_id)

  if (!run) {
    // 生成模拟的 Run 数据
    return {
      report,
      run: generateMockRun(report),
    }
  }

  return { report, run }
}

function generateMockRun(report: Report): Run {
  const actions = [
    '打开目标页面',
    '等待页面加载完成',
    '识别页面元素',
    '执行操作',
    '验证结果',
    '截图保存',
  ]

  const steps: Step[] = Array.from({ length: report.total_steps }, (_, i) => ({
    index: i + 1,
    action: actions[i % actions.length] || `执行操作 ${i + 1}`,
    reasoning: `AI 分析：当前步骤 ${i + 1}，准备执行 ${actions[i % actions.length] || '操作'}`,
    screenshot: `/screenshots/step-${i + 1}.png`,
    status: i < report.success_steps ? 'success' : 'failed',
    error: i >= report.success_steps ? '操作超时或元素未找到' : undefined,
    duration_ms: Math.floor(Math.random() * 3000) + 500,
  }))

  return {
    id: report.run_id,
    task_id: report.task_name,
    status: report.status,
    started_at: new Date(new Date(report.created_at).getTime() - report.duration_ms).toISOString(),
    finished_at: report.created_at,
    steps,
  }
}
```

**Step 2: 验证文件创建成功**

Run: `ls frontend/src/api/mock/reports.ts`
Expected: 文件存在

**Step 3: Commit**

```bash
git add frontend/src/api/mock/reports.ts
git commit -m "feat: 添加报告 Mock 数据模块"
```

---

## Task 2: 创建报告筛选组件

**Files:**
- Create: `frontend/src/components/Report/ReportFilters.tsx`
- Create: `frontend/src/components/Report/index.ts`

**Step 1: 创建 ReportFilters.tsx**

```typescript
import { Filter } from 'lucide-react'

export interface ReportFiltersState {
  status: 'all' | 'success' | 'failed'
  dateRange: 'all' | 'today' | '7days' | '30days'
}

interface ReportFiltersProps {
  filters: ReportFiltersState
  onFilterChange: (filters: ReportFiltersState) => void
}

export function ReportFilters({ filters, onFilterChange }: ReportFiltersProps) {
  const updateFilter = <K extends keyof ReportFiltersState>(
    key: K,
    value: ReportFiltersState[K]
  ) => {
    onFilterChange({ ...filters, [key]: value })
  }

  return (
    <div className="flex items-center gap-4 mb-4">
      <div className="flex items-center gap-2 text-gray-500">
        <Filter className="w-4 h-4" />
        <span className="text-sm">筛选:</span>
      </div>

      {/* 状态筛选 */}
      <select
        value={filters.status}
        onChange={e => updateFilter('status', e.target.value as ReportFiltersState['status'])}
        className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="all">全部状态</option>
        <option value="success">成功</option>
        <option value="failed">失败</option>
      </select>

      {/* 日期筛选 */}
      <select
        value={filters.dateRange}
        onChange={e => updateFilter('dateRange', e.target.value as ReportFiltersState['dateRange'])}
        className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="all">全部时间</option>
        <option value="today">今天</option>
        <option value="7days">最近 7 天</option>
        <option value="30days">最近 30 天</option>
      </select>
    </div>
  )
}
```

**Step 2: 创建 index.ts 导出文件**

```typescript
export { ReportFilters, type ReportFiltersState } from './ReportFilters'
```

**Step 3: Commit**

```bash
git add frontend/src/components/Report/
git commit -m "feat: 添加报告筛选组件"
```

---

## Task 3: 创建报告表格组件

**Files:**
- Create: `frontend/src/components/Report/ReportTable.tsx`
- Modify: `frontend/src/components/Report/index.ts`

**Step 1: 创建 ReportTable.tsx**

```typescript
import { useNavigate } from 'react-router-dom'
import { Eye, Clock, CheckCircle, XCircle } from 'lucide-react'
import { StatusBadge } from '../shared'
import type { Report } from '../../types'

interface ReportTableProps {
  reports: Report[]
}

export function ReportTable({ reports }: ReportTableProps) {
  const navigate = useNavigate()

  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`
    return `${Math.floor(ms / 60000)}m ${Math.floor((ms % 60000) / 1000)}s`
  }

  const formatDate = (dateStr: string): string => {
    const date = new Date(dateStr)
    return date.toLocaleString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const handleView = (reportId: string) => {
    navigate(`/reports/${reportId}`)
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-50 border-b border-gray-200">
          <tr>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">任务名称</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">状态</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">步骤</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">耗时</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">执行时间</th>
            <th className="px-4 py-3 text-right text-sm font-medium text-gray-500">操作</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {reports.map(report => (
            <tr key={report.id} className="hover:bg-gray-50">
              <td className="px-4 py-3">
                <span className="font-medium text-gray-900">{report.task_name}</span>
              </td>
              <td className="px-4 py-3">
                <StatusBadge status={report.status} />
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center gap-1 text-sm text-gray-600">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>{report.success_steps}</span>
                  {report.failed_steps > 0 && (
                    <>
                      <XCircle className="w-4 h-4 text-red-500 ml-2" />
                      <span>{report.failed_steps}</span>
                    </>
                  )}
                  <span className="text-gray-400 ml-1">/ {report.total_steps}</span>
                </div>
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center gap-1 text-sm text-gray-600">
                  <Clock className="w-4 h-4" />
                  <span>{formatDuration(report.duration_ms)}</span>
                </div>
              </td>
              <td className="px-4 py-3 text-sm text-gray-500">
                {formatDate(report.created_at)}
              </td>
              <td className="px-4 py-3 text-right">
                <button
                  onClick={() => handleView(report.id)}
                  className="inline-flex items-center gap-1 px-3 py-1 text-sm text-blue-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition"
                >
                  <Eye className="w-4 h-4" />
                  查看
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

**Step 2: 更新 index.ts**

```typescript
export { ReportFilters, type ReportFiltersState } from './ReportFilters'
export { ReportTable } from './ReportTable'
```

**Step 3: Commit**

```bash
git add frontend/src/components/Report/
git commit -m "feat: 添加报告表格组件"
```

---

## Task 4: 创建报告列表页

**Files:**
- Modify: `frontend/src/pages/Reports.tsx`
- Create: `frontend/src/hooks/useReports.ts`

**Step 1: 创建 useReports Hook**

```typescript
import { useState, useEffect, useCallback } from 'react'
import { getReports, type ReportFiltersState } from '../components/Report'
import type { Report } from '../types'

interface UseReportsReturn {
  reports: Report[]
  total: number
  loading: boolean
  filters: ReportFiltersState
  page: number
  pageSize: number
  setPage: (page: number) => void
  updateFilter: <K extends keyof ReportFiltersState>(
    key: K,
    value: ReportFiltersState[K]
  ) => void
  refresh: () => void
}

export function useReports(): UseReportsReturn {
  const [reports, setReports] = useState<Report[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState<ReportFiltersState>({
    status: 'all',
    dateRange: 'all',
  })
  const [page, setPage] = useState(1)
  const pageSize = 10

  const fetchReports = useCallback(() => {
    setLoading(true)
    const result = getReports({ ...filters, page, pageSize })
    setReports(result.reports)
    setTotal(result.total)
    setLoading(false)
  }, [filters, page])

  useEffect(() => {
    fetchReports()
  }, [fetchReports])

  // 筛选变化时重置页码
  useEffect(() => {
    setPage(1)
  }, [filters])

  const updateFilter = <K extends keyof ReportFiltersState>(
    key: K,
    value: ReportFiltersState[K]
  ) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }

  return {
    reports,
    total,
    loading,
    filters,
    page,
    pageSize,
    setPage,
    updateFilter,
    refresh: fetchReports,
  }
}
```

**Step 2: 重构 Reports.tsx**

```typescript
import { ReportFilters, ReportTable } from '../components/Report'
import { Pagination, EmptyState, LoadingSpinner } from '../components/shared'
import { useReports } from '../hooks/useReports'

export function Reports() {
  const {
    reports,
    total,
    loading,
    filters,
    page,
    pageSize,
    setPage,
    updateFilter,
  } = useReports()

  if (loading && reports.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  const hasFilters = filters.status !== 'all' || filters.dateRange !== 'all'

  return (
    <div>
      {/* 页面标题 */}
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">报告查看</h1>
        <p className="mt-1 text-gray-500">查看测试执行报告</p>
      </div>

      {/* 筛选栏 */}
      <ReportFilters filters={filters} onFilterChange={updateFilter} />

      {/* 表格 */}
      {reports.length === 0 ? (
        <div className="bg-white rounded-xl border border-gray-200 p-8">
          <EmptyState
            message={hasFilters ? '没有找到匹配的报告' : '暂无执行报告'}
          />
        </div>
      ) : (
        <ReportTable reports={reports} />
      )}

      {/* 分页 */}
      <Pagination total={total} page={page} pageSize={pageSize} onChange={setPage} />
    </div>
  )
}
```

**Step 3: 验证编译**

Run: `cd frontend && npm run build`
Expected: 编译成功

**Step 4: Commit**

```bash
git add frontend/src/pages/Reports.tsx frontend/src/hooks/useReports.ts
git commit -m "feat: 实现报告列表页"
```

---

## Task 5: 创建摘要卡片组件

**Files:**
- Create: `frontend/src/components/Report/SummaryCard.tsx`
- Modify: `frontend/src/components/Report/index.ts`

**Step 1: 创建 SummaryCard.tsx**

```typescript
import type { ReactNode } from 'react'

interface SummaryCardProps {
  icon: ReactNode
  label: string
  value: string | number
  valueColor?: string
}

export function SummaryCard({ icon, label, value, valueColor = 'text-gray-900' }: SummaryCardProps) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4">
      <div className="flex items-center gap-3">
        <div className="p-2 bg-gray-100 rounded-lg text-gray-600">
          {icon}
        </div>
        <div>
          <p className="text-sm text-gray-500">{label}</p>
          <p className={`text-xl font-semibold ${valueColor}`}>{value}</p>
        </div>
      </div>
    </div>
  )
}
```

**Step 2: 更新 index.ts**

```typescript
export { ReportFilters, type ReportFiltersState } from './ReportFilters'
export { ReportTable } from './ReportTable'
export { SummaryCard } from './SummaryCard'
```

**Step 3: Commit**

```bash
git add frontend/src/components/Report/
git commit -m "feat: 添加摘要卡片组件"
```

---

## Task 6: 创建步骤展开组件

**Files:**
- Create: `frontend/src/components/Report/StepItem.tsx`
- Modify: `frontend/src/components/Report/index.ts`

**Step 1: 创建 StepItem.tsx**

```typescript
import { useState } from 'react'
import { ChevronDown, ChevronRight, CheckCircle, XCircle, Clock } from 'lucide-react'
import { ImageViewer } from '../shared'
import type { Step } from '../../types'

interface StepItemProps {
  step: Step
  defaultExpanded?: boolean
}

export function StepItem({ step, defaultExpanded = false }: StepItemProps) {
  const [expanded, setExpanded] = useState(defaultExpanded)
  const [viewerOpen, setViewerOpen] = useState(false)

  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`
    return `${(ms / 1000).toFixed(1)}s`
  }

  const isSuccess = step.status === 'success'

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      {/* 步骤头部 */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition"
      >
        {/* 展开图标 */}
        {expanded ? (
          <ChevronDown className="w-5 h-5 text-gray-400" />
        ) : (
          <ChevronRight className="w-5 h-5 text-gray-400" />
        )}

        {/* 状态图标 */}
        {isSuccess ? (
          <CheckCircle className="w-5 h-5 text-green-500" />
        ) : (
          <XCircle className="w-5 h-5 text-red-500" />
        )}

        {/* 步骤信息 */}
        <div className="flex-1 text-left">
          <span className="font-medium text-gray-900">步骤 {step.index}</span>
          <span className="text-gray-500 mx-2">-</span>
          <span className="text-gray-700">{step.action}</span>
        </div>

        {/* 耗时 */}
        <div className="flex items-center gap-1 text-sm text-gray-500">
          <Clock className="w-4 h-4" />
          <span>{formatDuration(step.duration_ms)}</span>
        </div>
      </button>

      {/* 展开内容 */}
      {expanded && (
        <div className="border-t border-gray-200 p-4 bg-gray-50">
          {/* 错误信息 */}
          {step.error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-600 font-medium">错误信息</p>
              <p className="text-sm text-red-500 mt-1">{step.error}</p>
            </div>
          )}

          {/* 截图和推理 */}
          <div className="grid grid-cols-2 gap-4">
            {/* 截图预览 */}
            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">截图</p>
              <div
                className="relative cursor-pointer group"
                onClick={() => setViewerOpen(true)}
              >
                <img
                  src={step.screenshot}
                  alt={`步骤 ${step.index} 截图`}
                  className="w-full h-48 object-cover rounded-lg border border-gray-200 bg-white"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition rounded-lg flex items-center justify-center">
                  <span className="text-white opacity-0 group-hover:opacity-100 text-sm font-medium">
                    点击查看大图
                  </span>
                </div>
              </div>
            </div>

            {/* AI 推理 */}
            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">AI 推理过程</p>
              <div className="h-48 overflow-y-auto p-3 bg-white rounded-lg border border-gray-200">
                {step.reasoning ? (
                  <p className="text-sm text-gray-600 whitespace-pre-wrap">{step.reasoning}</p>
                ) : (
                  <p className="text-sm text-gray-400 italic">暂无推理记录</p>
                )}
              </div>
            </div>
          </div>

          {/* 图片查看器 */}
          <ImageViewer
            src={step.screenshot}
            isOpen={viewerOpen}
            onClose={() => setViewerOpen(false)}
          />
        </div>
      )}
    </div>
  )
}
```

**Step 2: 更新 index.ts**

```typescript
export { ReportFilters, type ReportFiltersState } from './ReportFilters'
export { ReportTable } from './ReportTable'
export { SummaryCard } from './SummaryCard'
export { StepItem } from './StepItem'
```

**Step 3: Commit**

```bash
git add frontend/src/components/Report/
git commit -m "feat: 添加步骤展开组件"
```

---

## Task 7: 创建报告详情页头部组件

**Files:**
- Create: `frontend/src/components/Report/ReportHeader.tsx`
- Modify: `frontend/src/components/Report/index.ts`

**Step 1: 创建 ReportHeader.tsx**

```typescript
import { useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { StatusBadge } from '../shared'

interface ReportHeaderProps {
  taskName: string
  status: 'success' | 'failed'
}

export function ReportHeader({ taskName, status }: ReportHeaderProps) {
  const navigate = useNavigate()

  return (
    <div className="flex items-center gap-4 mb-6">
      {/* 返回按钮 */}
      <button
        onClick={() => navigate('/reports')}
        className="p-2 hover:bg-gray-100 rounded-lg transition"
      >
        <ArrowLeft className="w-5 h-5 text-gray-600" />
      </button>

      {/* 标题和状态 */}
      <div className="flex-1">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-semibold text-gray-900">{taskName}</h1>
          <StatusBadge status={status} />
        </div>
        <p className="text-gray-500 mt-1">执行报告详情</p>
      </div>
    </div>
  )
}
```

**Step 2: 更新 index.ts**

```typescript
export { ReportFilters, type ReportFiltersState } from './ReportFilters'
export { ReportTable } from './ReportTable'
export { SummaryCard } from './SummaryCard'
export { StepItem } from './StepItem'
export { ReportHeader } from './ReportHeader'
```

**Step 3: Commit**

```bash
git add frontend/src/components/Report/
git commit -m "feat: 添加报告详情页头部组件"
```

---

## Task 8: 创建报告详情页

**Files:**
- Create: `frontend/src/pages/ReportDetail.tsx`
- Modify: `frontend/src/api/mock/reports.ts`（添加导出）

**Step 1: 更新 reports.ts 导出 getReportDetail**

确保 `reports.ts` 中 `getReportDetail` 函数已导出（已在 Task 1 创建）。

**Step 2: 创建 ReportDetail.tsx**

```typescript
import { useParams, Navigate } from 'react-router-dom'
import { Layers, CheckCircle, XCircle, Clock } from 'lucide-react'
import { ReportHeader, SummaryCard, StepItem } from '../components/Report'
import { LoadingSpinner } from '../components/shared'
import { getReportDetail } from '../api/mock/reports'

export function ReportDetail() {
  const { id } = useParams<{ id: string }>()

  // 获取报告详情
  const data = id ? getReportDetail(id) : null

  if (!data) {
    return <Navigate to="/reports" replace />
  }

  const { report, run } = data

  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`
    return `${Math.floor(ms / 60000)}m ${Math.floor((ms % 60000) / 1000)}s`
  }

  return (
    <div className="max-w-5xl mx-auto">
      {/* 头部 */}
      <ReportHeader taskName={report.task_name} status={report.status} />

      {/* 摘要卡片 */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <SummaryCard
          icon={<Layers className="w-5 h-5" />}
          label="总步骤"
          value={report.total_steps}
        />
        <SummaryCard
          icon={<CheckCircle className="w-5 h-5" />}
          label="成功数"
          value={report.success_steps}
          valueColor="text-green-600"
        />
        <SummaryCard
          icon={<XCircle className="w-5 h-5" />}
          label="失败数"
          value={report.failed_steps}
          valueColor={report.failed_steps > 0 ? 'text-red-600' : 'text-gray-900'}
        />
        <SummaryCard
          icon={<Clock className="w-5 h-5" />}
          label="总耗时"
          value={formatDuration(report.duration_ms)}
        />
      </div>

      {/* 步骤列表 */}
      <div className="space-y-3">
        <h2 className="text-lg font-medium text-gray-900 mb-3">执行步骤</h2>
        {run.steps.map((step, index) => (
          <StepItem
            key={step.index}
            step={step}
            defaultExpanded={index === 0 || step.status === 'failed'}
          />
        ))}
      </div>
    </div>
  )
}
```

**Step 3: Commit**

```bash
git add frontend/src/pages/ReportDetail.tsx
git commit -m "feat: 创建报告详情页"
```

---

## Task 9: 配置路由

**Files:**
- Modify: `frontend/src/App.tsx`

**Step 1: 添加 ReportDetail 导入和路由**

```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { Tasks } from './pages/Tasks'
import { TaskDetail } from './pages/TaskDetail'
import { RunList } from './pages/RunList'
import { RunMonitor } from './pages/RunMonitor'
import { Reports } from './pages/Reports'
import { ReportDetail } from './pages/ReportDetail'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/tasks" element={<Tasks />} />
            <Route path="/tasks/:id" element={<TaskDetail />} />
            <Route path="/runs" element={<RunList />} />
            <Route path="/runs/:id" element={<RunMonitor />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/reports/:id" element={<ReportDetail />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
>
  )
}

export default App
```

**Step 2: 验证编译**

Run: `cd frontend && npm run build`
Expected: 编译成功

**Step 3: Commit**

```bash
git add frontend/src/App.tsx
git commit -m "feat: 添加报告详情页路由"
```

---

## Task 10: 修复 Mock 数据导入问题

**Files:**
- Modify: `frontend/src/api/mock/reports.ts`

**Step 1: 修复动态导入问题**

将 `require('./runs')` 改为静态导入：

```typescript
import type { Report, Run, Step } from '../../types'
import { mockRuns } from './runs'

// 基于 mockRuns 生成报告列表
function generateReportsFromRuns(): Report[] {
  return mockRuns.map(run => ({
    id: `report-${run.id}`,
    run_id: run.id,
    task_name: `任务 ${run.task_id}`,
    status: run.status === 'success' ? 'success' : 'failed',
    total_steps: run.steps.length,
    success_steps: run.steps.filter(s => s.status === 'success').length,
    failed_steps: run.steps.filter(s => s.status === 'failed').length,
    duration_ms: run.steps.reduce((sum, s) => sum + s.duration_ms, 0),
    created_at: run.finished_at || run.started_at,
  }))
}

// ... 其余代码保持不变，但删除 generateMockRun 中的 require

export function getReportDetail(reportId: string): { report: Report; run: Run } | null {
  const report = mockReports.find(r => r.id === reportId)
  if (!report) return null

  const run = mockRuns.find((r: Run) => r.id === report.run_id)

  if (!run) {
    return {
      report,
      run: generateMockRun(report),
    }
  }

  return { report, run }
}
```

**Step 2: 验证编译**

Run: `cd frontend && npm run build`
Expected: 编译成功，无 require 相关错误

**Step 3: Commit**

```bash
git add frontend/src/api/mock/reports.ts
git commit -m "fix: 修复 Mock 数据导入方式"
```

---

## Task 11: 验证和测试

**Step 1: 启动开发服务器**

Run: `cd frontend && npm run dev`

**Step 2: 手动测试**

1. 访问 `/reports` — 验证报告列表显示
2. 测试状态筛选 — 全部/成功/失败
3. 测试日期筛选 — 今天/最近7天/最近30天
4. 测试分页 — 点击页码切换
5. 点击「查看」进入报告详情页
6. 验证摘要卡片显示正确
7. 验证步骤列表展开/收起
8. 点击截图查看大图

**Step 3: 最终 Commit**

```bash
git add -A
git commit -m "feat: 完成 Phase 5 报告查看功能"
```

---

## 完成检查

- [ ] 报告列表页显示正常
- [ ] 状态筛选功能正常
- [ ] 日期筛选功能正常
- [ ] 分页功能正常
- [ ] 报告详情页显示正常
- [ ] 摘要卡片数据正确
- [ ] 步骤列表展开/收起正常
- [ ] 截图查看器正常工作
- [ ] 所有编译无错误
