# Phase 6: Dashboard 仪表盘实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 Dashboard 仪表盘功能，展示统计概览、7 天趋势图、快速启动入口和最近执行记录。

**Architecture:** 采用四象限布局，顶部 4 个统计卡片，中部左侧趋势图 + 右侧快速启动，底部最近执行记录列表。复用现有 StatusBadge、useTasks Hook 和 Recharts 图表组件。

**Tech Stack:** React 18, TypeScript, Tailwind CSS, Recharts, React Router

---

## Task 1: 添加 Dashboard 类型定义

**Files:**
- Modify: `frontend/src/types/index.ts`

**Step 1: 添加 Dashboard 相关类型**

在 `frontend/src/types/index.ts` 文件末尾添加：

```typescript
// Dashboard 统计数据
export interface DashboardStats {
  totalTasks: number
  totalRuns: number
  successRate: number
  todayRuns: number
}

// 7 天趋势数据点
export interface TrendDataPoint {
  date: string
  runs: number
  successRate: number
}

// 最近执行记录
export interface RecentRun {
  id: string
  task_name: string
  status: 'success' | 'failed' | 'running'
  started_at: string
  duration_ms: number
}
```

**Step 2: 验证类型定义**

Run: `cd frontend && npm run build`
Expected: 编译成功，无类型错误

**Step 3: Commit**

```bash
git add frontend/src/types/index.ts
git commit -m "feat: 添加 Dashboard 类型定义"
```

---

## Task 2: 创建 Dashboard Mock 数据

**Files:**
- Create: `frontend/src/api/mock/dashboard.ts`
- Modify: `frontend/src/api/mock/index.ts`

**Step 1: 创建 Mock 数据文件**

创建 `frontend/src/api/mock/dashboard.ts`：

```typescript
import type { DashboardStats, TrendDataPoint, RecentRun } from '../../types'

export const mockDashboardStats: DashboardStats = {
  totalTasks: 12,
  totalRuns: 156,
  successRate: 87.5,
  todayRuns: 8,
}

export const mockTrendData: TrendDataPoint[] = [
  { date: '03-03', runs: 18, successRate: 83 },
  { date: '03-04', runs: 22, successRate: 86 },
  { date: '03-05', runs: 15, successRate: 80 },
  { date: '03-06', runs: 28, successRate: 92 },
  { date: '03-07', runs: 20, successRate: 85 },
  { date: '03-08', runs: 25, successRate: 88 },
  { date: '03-09', runs: 28, successRate: 90 },
]

export const mockRecentRuns: RecentRun[] = [
  {
    id: 'r_001',
    task_name: '用户登录测试',
    status: 'success',
    started_at: '2026-03-09T10:30:25Z',
    duration_ms: 12500,
  },
  {
    id: 'r_002',
    task_name: '表单提交测试',
    status: 'failed',
    started_at: '2026-03-09T09:15:00Z',
    duration_ms: 8300,
  },
  {
    id: 'r_003',
    task_name: '搜索功能测试',
    status: 'running',
    started_at: '2026-03-09T08:45:12Z',
    duration_ms: 0,
  },
  {
    id: 'r_004',
    task_name: '购物车流程测试',
    status: 'success',
    started_at: '2026-03-08T16:20:00Z',
    duration_ms: 45000,
  },
  {
    id: 'r_005',
    task_name: '订单查询测试',
    status: 'success',
    started_at: '2026-03-08T14:10:30Z',
    duration_ms: 9800,
  },
]
```

**Step 2: 导出 Mock 数据**

修改 `frontend/src/api/mock/index.ts`，添加导出：

```typescript
export * from './dashboard'
```

**Step 3: 验证 Mock 数据**

Run: `cd frontend && npm run build`
Expected: 编译成功

**Step 4: Commit**

```bash
git add frontend/src/api/mock/dashboard.ts frontend/src/api/mock/index.ts
git commit -m "feat: 添加 Dashboard Mock 数据"
```

---

## Task 3: 创建 StatCard 统计卡片组件

**Files:**
- Create: `frontend/src/components/Dashboard/StatCard.tsx`

**Step 1: 创建 StatCard 组件**

创建 `frontend/src/components/Dashboard/StatCard.tsx`：

```typescript
interface StatCardProps {
  title: string
  value: string | number
  icon: React.ReactNode
  trend?: string
  trendUp?: boolean
}

export function StatCard({ title, value, icon, trend, trendUp }: StatCardProps) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <div className="flex items-center gap-3 mb-3">
        <span className="text-2xl">{icon}</span>
        <span className="text-sm font-medium text-gray-500">{title}</span>
      </div>
      <div className="text-3xl font-semibold text-gray-900">{value}</div>
      {trend && (
        <div className={`mt-2 text-sm ${trendUp ? 'text-green-600' : 'text-red-600'}`}>
          {trendUp ? '↑' : '↓'} {trend}
        </div>
      )}
    </div>
  )
}
```

**Step 2: 验证组件**

Run: `cd frontend && npm run build`
Expected: 编译成功

**Step 3: Commit**

```bash
git add frontend/src/components/Dashboard/StatCard.tsx
git commit -m "feat: 添加 StatCard 统计卡片组件"
```

---

## Task 4: 创建 TrendChart 趋势图组件

**Files:**
- Create: `frontend/src/components/Dashboard/TrendChart.tsx`

**Step 1: 创建 TrendChart 组件**

创建 `frontend/src/components/Dashboard/TrendChart.tsx`：

```typescript
import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'
import type { TrendDataPoint } from '../../types'

interface TrendChartProps {
  data: TrendDataPoint[]
  loading?: boolean
}

export function TrendChart({ data, loading }: TrendChartProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-5 h-80 flex items-center justify-center">
        <span className="text-gray-400">加载中...</span>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 h-80">
      <h3 className="text-base font-medium text-gray-900 mb-4">7 天执行趋势</h3>
      <div className="h-60">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="date" stroke="#9ca3af" fontSize={12} />
            <YAxis
              yAxisId="left"
              stroke="#9ca3af"
              fontSize={12}
              allowDecimals={false}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              stroke="#9ca3af"
              fontSize={12}
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fff',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
              }}
              formatter={(value: number, name: string) => {
                if (name === 'successRate') return [`${value}%`, '成功率']
                return [value, '执行次数']
              }}
            />
            <Legend
              formatter={(value) => (value === 'runs' ? '执行次数' : '成功率')}
            />
            <Bar
              yAxisId="left"
              dataKey="runs"
              name="runs"
              fill="#3b82f6"
              radius={[4, 4, 0, 0]}
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="successRate"
              name="successRate"
              stroke="#22c55e"
              strokeWidth={2}
              dot={{ fill: '#22c55e', strokeWidth: 2 }}
              activeDot={{ r: 6 }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
```

**Step 2: 验证组件**

Run: `cd frontend && npm run build`
Expected: 编译成功

**Step 3: Commit**

```bash
git add frontend/src/components/Dashboard/TrendChart.tsx
git commit -m "feat: 添加 TrendChart 趋势图组件"
```

---

## Task 5: 创建 QuickStart 快速启动组件

**Files:**
- Create: `frontend/src/components/Dashboard/QuickStart.tsx`

**Step 1: 创建 QuickStart 组件**

创建 `frontend/src/components/Dashboard/QuickStart.tsx`：

```typescript
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import type { Task } from '../../types'
import { startRun } from '../../api/runs'

interface QuickStartProps {
  tasks: Task[]
  loading?: boolean
}

export function QuickStart({ tasks, loading }: QuickStartProps) {
  const navigate = useNavigate()
  const [selectedTaskId, setSelectedTaskId] = useState<string>('')
  const [starting, setStarting] = useState(false)

  const readyTasks = tasks.filter(t => t.status === 'ready')

  const handleStart = async () => {
    if (!selectedTaskId || starting) return

    setStarting(true)
    try {
      const { runId } = await startRun(selectedTaskId)
      navigate(`/runs/${runId}`)
    } catch (error) {
      console.error('Failed to start run:', error)
    } finally {
      setStarting(false)
    }
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h3 className="text-base font-medium text-gray-900 mb-4 flex items-center gap-2">
        <span>🚀</span>
        <span>快速启动</span>
      </h3>

      <div className="space-y-4">
        <select
          value={selectedTaskId}
          onChange={(e) => setSelectedTaskId(e.target.value)}
          disabled={loading || starting}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
        >
          <option value="">选择任务...</option>
          {readyTasks.map(task => (
            <option key={task.id} value={task.id}>
              {task.name}
            </option>
          ))}
        </select>

        <button
          onClick={handleStart}
          disabled={!selectedTaskId || starting}
          className="w-full px-4 py-2 bg-blue-500 text-white text-sm font-medium rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {starting ? '启动中...' : '启动执行'}
        </button>

        {readyTasks.length === 0 && !loading && (
          <p className="text-sm text-gray-500 text-center">
            暂无可执行的任务
          </p>
        )}
      </div>
    </div>
  )
}
```

**Step 2: 验证组件**

Run: `cd frontend && npm run build`
Expected: 编译成功

**Step 3: Commit**

```bash
git add frontend/src/components/Dashboard/QuickStart.tsx
git commit -m "feat: 添加 QuickStart 快速启动组件"
```

---

## Task 6: 创建 RecentRuns 最近执行记录组件

**Files:**
- Create: `frontend/src/components/Dashboard/RecentRuns.tsx`

**Step 1: 创建 RecentRuns 组件**

创建 `frontend/src/components/Dashboard/RecentRuns.tsx`：

```typescript
import { useNavigate } from 'react-router-dom'
import type { RecentRun } from '../../types'
import { StatusBadge } from '../shared/StatusBadge'

interface RecentRunsProps {
  runs: RecentRun[]
  loading?: boolean
}

function formatTime(isoString: string): string {
  const date = new Date(isoString)
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

function formatDuration(ms: number): string {
  if (ms === 0) return '-'
  if (ms < 1000) return `${ms}ms`
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`
  return `${Math.floor(ms / 60000)}m ${Math.floor((ms % 60000) / 1000)}s`
}

export function RecentRuns({ runs, loading }: RecentRunsProps) {
  const navigate = useNavigate()

  if (loading) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-medium text-gray-900 flex items-center gap-2">
            <span>📋</span>
            <span>最近执行记录</span>
          </h3>
        </div>
        <div className="text-center py-8 text-gray-400">加载中...</div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-medium text-gray-900 flex items-center gap-2">
          <span>📋</span>
          <span>最近执行记录</span>
        </h3>
        <button
          onClick={() => navigate('/reports')}
          className="text-sm text-blue-500 hover:text-blue-600 font-medium"
        >
          查看全部 →
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="text-left text-sm text-gray-500 border-b border-gray-200">
              <th className="pb-3 font-medium">任务名称</th>
              <th className="pb-3 font-medium">状态</th>
              <th className="pb-3 font-medium">执行时间</th>
              <th className="pb-3 font-medium text-right">耗时</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {runs.map(run => (
              <tr
                key={run.id}
                onClick={() => navigate(`/reports/${run.id}`)}
                className="cursor-pointer hover:bg-gray-50 transition-colors"
              >
                <td className="py-3 text-sm text-gray-900">{run.task_name}</td>
                <td className="py-3">
                  <StatusBadge status={run.status} />
                </td>
                <td className="py-3 text-sm text-gray-500">
                  {formatTime(run.started_at)}
                </td>
                <td className="py-3 text-sm text-gray-500 text-right">
                  {formatDuration(run.duration_ms)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {runs.length === 0 && (
          <div className="text-center py-8 text-gray-400">
            暂无执行记录
          </div>
        )}
      </div>
    </div>
  )
}
```

**Step 2: 验证组件**

Run: `cd frontend && npm run build`
Expected: 编译成功

**Step 3: Commit**

```bash
git add frontend/src/components/Dashboard/RecentRuns.tsx
git commit -m "feat: 添加 RecentRuns 最近执行记录组件"
```

---

## Task 7: 创建 Dashboard 组件导出文件

**Files:**
- Create: `frontend/src/components/Dashboard/index.ts`

**Step 1: 创建导出文件**

创建 `frontend/src/components/Dashboard/index.ts`：

```typescript
export { StatCard } from './StatCard'
export { TrendChart } from './TrendChart'
export { QuickStart } from './QuickStart'
export { RecentRuns } from './RecentRuns'
```

**Step 2: 验证导出**

Run: `cd frontend && npm run build`
Expected: 编译成功

**Step 3: Commit**

```bash
git add frontend/src/components/Dashboard/index.ts
git commit -m "feat: 添加 Dashboard 组件导出"
```

---

## Task 8: 创建 useDashboard Hook

**Files:**
- Create: `frontend/src/hooks/useDashboard.ts`

**Step 1: 创建 Hook**

创建 `frontend/src/hooks/useDashboard.ts`：

```typescript
import { useState, useEffect } from 'react'
import type { DashboardStats, TrendDataPoint, RecentRun } from '../types'
import { ENABLE_MOCK, delay } from '../api/mock'
import { mockDashboardStats, mockTrendData, mockRecentRuns } from '../api/mock/dashboard'

interface DashboardData {
  stats: DashboardStats
  trendData: TrendDataPoint[]
  recentRuns: RecentRun[]
}

export function useDashboard() {
  const [data, setData] = useState<DashboardData>({
    stats: { totalTasks: 0, totalRuns: 0, successRate: 0, todayRuns: 0 },
    trendData: [],
    recentRuns: [],
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchDashboard() {
      setLoading(true)
      try {
        if (ENABLE_MOCK) {
          await delay(300)
          setData({
            stats: mockDashboardStats,
            trendData: mockTrendData,
            recentRuns: mockRecentRuns,
          })
        } else {
          // TODO: 对接真实 API
          const response = await fetch('/api/dashboard')
          const result = await response.json()
          setData(result)
        }
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchDashboard()
  }, [])

  return {
    ...data,
    loading,
  }
}
```

**Step 2: 验证 Hook**

Run: `cd frontend && npm run build`
Expected: 编译成功

**Step 3: Commit**

```bash
git add frontend/src/hooks/useDashboard.ts
git commit -m "feat: 添加 useDashboard Hook"
```

---

## Task 9: 更新 Dashboard 页面

**Files:**
- Modify: `frontend/src/pages/Dashboard.tsx`

**Step 1: 重写 Dashboard 页面**

修改 `frontend/src/pages/Dashboard.tsx`：

```typescript
import { StatCard, TrendChart, QuickStart, RecentRuns } from '../components/Dashboard'
import { useDashboard } from '../hooks/useDashboard'
import { useTasks } from '../hooks/useTasks'

export function Dashboard() {
  const { stats, trendData, recentRuns, loading } = useDashboard()
  const { allTasks, loading: tasksLoading } = useTasks()

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">仪表盘</h1>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="总任务数"
          value={stats.totalTasks}
          icon="📊"
        />
        <StatCard
          title="总执行次数"
          value={stats.totalRuns}
          icon="🔄"
        />
        <StatCard
          title="成功率"
          value={`${stats.successRate}%`}
          icon="✅"
          trend="5% 较上周"
          trendUp={true}
        />
        <StatCard
          title="今日执行"
          value={stats.todayRuns}
          icon="📅"
        />
      </div>

      {/* 趋势图 + 快速启动 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <TrendChart data={trendData} loading={loading} />
        </div>
        <div className="lg:col-span-1">
          <QuickStart tasks={allTasks} loading={tasksLoading} />
        </div>
      </div>

      {/* 最近执行记录 */}
      <RecentRuns runs={recentRuns} loading={loading} />
    </div>
  )
}
```

**Step 2: 验证页面**

Run: `cd frontend && npm run build`
Expected: 编译成功

**Step 3: Commit**

```bash
git add frontend/src/pages/Dashboard.tsx
git commit -m "feat: 完成 Dashboard 仪表盘页面"
```

---

## Task 10: 验证并更新进度文档

**Files:**
- Modify: `docs/progress.md`
- Modify: `docs/2_前端主计划.md`

**Step 1: 启动开发服务器验证**

Run: `cd frontend && npm run dev`
Expected: 访问 http://localhost:5173 能看到完整的 Dashboard 页面

**Step 2: 更新进度文档**

在 `docs/progress.md` 的 Phase 6 部分更新：

```markdown
### Phase 6: 仪表盘功能 ✅
- **完成日期**: 2026-03-09
- **更新内容**:
  - 统计概览卡片（总任务数、总执行次数、成功率、今日执行）
  - 7 天趋势图（双 Y 轴：执行次数柱状图 + 成功率折线图）
  - 快速启动区域（任务下拉选择、一键启动）
  - 最近执行记录列表（5 条）
  - Dashboard Mock 数据模块
  - useDashboard Hook
```

**Step 3: 更新主计划文档**

在 `docs/2_前端主计划.md` 中勾选 Phase 6 的所有任务。

**Step 4: Commit**

```bash
git add docs/progress.md docs/2_前端主计划.md
git commit -m "docs: 记录 Phase 6 Dashboard 完成"
```

---

## 完成清单

- [ ] Task 1: 添加 Dashboard 类型定义
- [ ] Task 2: 创建 Dashboard Mock 数据
- [ ] Task 3: 创建 StatCard 统计卡片组件
- [ ] Task 4: 创建 TrendChart 趋势图组件
- [ ] Task 5: 创建 QuickStart 快速启动组件
- [ ] Task 6: 创建 RecentRuns 最近执行记录组件
- [ ] Task 7: 创建 Dashboard 组件导出文件
- [ ] Task 8: 创建 useDashboard Hook
- [ ] Task 9: 更新 Dashboard 页面
- [ ] Task 10: 验证并更新进度文档
