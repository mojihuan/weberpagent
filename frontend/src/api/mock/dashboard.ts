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
