import { useQuery } from '@tanstack/react-query'
import { getDashboard, type DashboardData } from '../api/dashboard'

const DEFAULT_DATA: DashboardData = {
  stats: { totalTasks: 0, totalRuns: 0, successRate: 0, todayRuns: 0 },
  trendData: [],
  recentRuns: [],
}

export function useDashboard() {
  const { data = DEFAULT_DATA, isLoading, error, refetch } = useQuery({
    queryKey: ['dashboard'],
    queryFn: getDashboard,
  })

  return {
    ...data,
    loading: isLoading,
    error: error instanceof Error ? error : error ? new Error(String(error)) : null,
    refetch,
  }
}
