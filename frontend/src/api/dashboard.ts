// frontend/src/api/dashboard.ts
import { apiClient } from './client'
import type { DashboardStats, TrendDataPoint, RecentRun } from '../types'

export interface DashboardData {
  stats: DashboardStats
  trendData: TrendDataPoint[]
  recentRuns: RecentRun[]
}

interface DashboardApiResponse {
  stats: {
    totalTasks: number
    totalRuns: number
    successRate: number
    todayRuns: number
  }
  trendData: Array<{
    date: string
    runs: number
    successRate: number
  }>
  recentRuns: Array<{
    id: string
    task_name: string
    status: string
    started_at: string
    duration_ms: number
  }>
}

export async function getDashboard(): Promise<DashboardData> {
  const response = await apiClient<DashboardApiResponse>('/dashboard')

  // 转换 status 为联合类型
  return {
    stats: response.stats,
    trendData: response.trendData,
    recentRuns: response.recentRuns.map(run => ({
      ...run,
      status: run.status as 'success' | 'failed' | 'running',
    })),
  }
}
