import { useState, useCallback, useEffect, useMemo } from 'react'
import type { Task } from '../types'
import { tasksApi } from '../api/tasks'

export interface Filters {
  search: string
  status: 'all' | 'draft' | 'ready'
  sortBy: 'updated_at' | 'name' | 'created_at'
  sortOrder: 'asc' | 'desc'
}

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState<Filters>({
    search: '',
    status: 'all',
    sortBy: 'updated_at',
    sortOrder: 'desc',
  })
  const [selectedIds, setSelectedIds] = useState<string[]>([])
  const [page, setPage] = useState(1)
  const pageSize = 10

  const fetchTasks = useCallback(async () => {
    setLoading(true)
    try {
      const data = await tasksApi.list({
        status: filters.status,
        search: filters.search,
      })
      setTasks(data)
    } catch (error) {
      console.error('Failed to fetch tasks:', error)
    } finally {
      setLoading(false)
    }
  }, [filters.status, filters.search])

  useEffect(() => {
    fetchTasks()
  }, [fetchTasks])

  const filteredTasks = useMemo(() => {
    let result = [...tasks]

    result.sort((a, b) => {
      let aVal: string | number = ''
      let bVal: string | number = ''

      switch (filters.sortBy) {
        case 'name':
          aVal = a.name
          bVal = b.name
          break
        case 'created_at':
          aVal = new Date(a.created_at).getTime()
          bVal = new Date(b.created_at).getTime()
          break
        case 'updated_at':
        default:
          aVal = new Date(a.updated_at).getTime()
          bVal = new Date(b.updated_at).getTime()
      }

      if (typeof aVal === 'string') {
        return filters.sortOrder === 'asc'
          ? aVal.localeCompare(bVal as string)
          : (bVal as string).localeCompare(aVal)
      }
      return filters.sortOrder === 'asc' ? aVal - (bVal as number) : (bVal as number) - aVal
    })

    return result
  }, [tasks, filters.sortBy, filters.sortOrder])

  const paginatedTasks = useMemo(() => {
    const start = (page - 1) * pageSize
    return filteredTasks.slice(start, start + pageSize)
  }, [filteredTasks, page, pageSize])

  const toggleSelectAll = useCallback(() => {
    if (selectedIds.length === paginatedTasks.length) {
      setSelectedIds([])
    } else {
      setSelectedIds(paginatedTasks.map(t => t.id))
    }
  }, [selectedIds.length, paginatedTasks])

  const toggleSelect = useCallback((id: string) => {
    setSelectedIds(prev =>
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    )
  }, [])

  const batchDelete = useCallback(async () => {
    if (selectedIds.length === 0) return
    await tasksApi.batchDelete(selectedIds)
    setSelectedIds([])
    await fetchTasks()
  }, [selectedIds, fetchTasks])

  const batchUpdateStatus = useCallback(async (status: 'draft' | 'ready') => {
    if (selectedIds.length === 0) return
    await tasksApi.batchUpdateStatus(selectedIds, status)
    setSelectedIds([])
    await fetchTasks()
  }, [selectedIds, fetchTasks])

  const updateFilter = useCallback(<K extends keyof Filters>(key: K, value: Filters[K]) => {
    setFilters(prev => ({ ...prev, [key]: value }))
    setPage(1)
  }, [])

  return {
    tasks: paginatedTasks,
    allTasks: tasks,
    filteredTasks,
    total: filteredTasks.length,
    loading,
    filters,
    selectedIds,
    page,
    pageSize,
    setPage,
    setFilters,
    updateFilter,
    setSelectedIds,
    toggleSelectAll,
    toggleSelect,
    fetchTasks,
    batchDelete,
    batchUpdateStatus,
  }
}
