import { useState, useCallback } from 'react'
import { useQuery } from '@tanstack/react-query'
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
  const [filters, setFilters] = useState<ReportFiltersState>({
    status: 'all',
    dateRange: 'all',
  })
  const [page, setPage] = useState(1)
  const pageSize = 10

  // Reset page when filters change
  const [prevFilters, setPrevFilters] = useState(filters)
  if (prevFilters !== filters) {
    setPrevFilters(filters)
    setPage(1)
  }

  const queryParams: ReportsListParams = {
    status: filters.status === 'all' ? 'all' : filters.status,
    page,
    page_size: pageSize,
    ...(filters.dateRange === 'today' ? { date: 'today' } :
        filters.dateRange === '7days' ? { date: '7days' } :
        filters.dateRange === '30days' ? { date: '30days' } : {}),
  }

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['reports', { status: filters.status, dateRange: filters.dateRange, page, pageSize }],
    queryFn: () => listReports(queryParams),
  })

  const updateFilter = useCallback(<K extends keyof ReportFiltersState>(key: K, value: ReportFiltersState[K]) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }, [])

  return {
    reports: data?.reports ?? [],
    total: data?.total ?? 0,
    loading: isLoading,
    error: error instanceof Error ? error : error ? new Error(String(error)) : null,
    filters,
    page,
    pageSize,
    setPage,
    updateFilter,
    refresh: refetch,
  }
}
