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
