import { useState, useEffect, useCallback } from 'react'
import { listReports, type ReportsListParams } from '../api/reports'
import type { Report } from '../types'
import type { ReportFiltersState } from '../components/Report'

interface UseReportsReturn {
  reports: Report[]
  total: number
  loading: boolean
  error: Error | null
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
  const [error, setError] = useState<Error | null>(null)
  const [filters, setFilters] = useState<ReportFiltersState>({
    status: 'all',
    dateRange: 'all',
  })
  const [page, setPage] = useState(1)
  const pageSize = 10

  const fetchReports = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      // 映射筛选状态
      const params: ReportsListParams = {
        status: filters.status === 'all' ? 'all' : filters.status,
        page,
        page_size: pageSize,
      }

      if (filters.dateRange === 'today') {
        params.date = 'today'
      } else if (filters.dateRange === '7days') {
        params.date = '7days'
      } else if (filters.dateRange === '30days') {
        params.date = '30days'
      }

      const result = await listReports(params)
      setReports(result.reports)
      setTotal(result.total)
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch reports'))
      console.error('Failed to fetch reports:', err)
    } finally {
      setLoading(false)
    }
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
    error,
    filters,
    page,
    pageSize,
    setPage,
    updateFilter,
    refresh: fetchReports,
  }
}
