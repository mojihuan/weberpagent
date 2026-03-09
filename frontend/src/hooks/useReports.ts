import { useState, useEffect, useCallback } from 'react'
import { getReports } from '../api/mock/reports'
import type { Report } from '../types'
import type { ReportFiltersState } from '../components/Report'

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

    // 映射筛选状态
    const statusParam = filters.status === 'all' ? 'all' : filters.status
    const dateParam = filters.dateRange === 'all' ? undefined :
      filters.dateRange === 'today' ? 'today' :
      filters.dateRange === '7days' ? '7days' : '30days'

    const result = getReports({
      status: statusParam,
      date: dateParam,
      page,
      pageSize,
    })

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
