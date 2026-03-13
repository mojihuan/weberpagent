import { useState, useEffect } from 'react'
import { getDashboard, type DashboardData } from '../api/dashboard'

export function useDashboard() {
  const [data, setData] = useState<DashboardData>({
    stats: { totalTasks: 0, totalRuns: 0, successRate: 0, todayRuns: 0 },
    trendData: [],
    recentRuns: [],
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    async function fetchDashboard() {
      setLoading(true)
      setError(null)
      try {
        const result = await getDashboard()
        setData(result)
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to fetch dashboard'))
        console.error('Failed to fetch dashboard data:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchDashboard()
  }, [])

  return {
    ...data,
    loading,
    error,
    refetch: () => {
      setLoading(true)
      getDashboard()
        .then(setData)
        .catch(err => setError(err instanceof Error ? err : new Error('Failed to fetch dashboard')))
        .finally(() => setLoading(false))
    },
  }
}
