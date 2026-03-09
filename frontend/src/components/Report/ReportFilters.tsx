import { Filter } from 'lucide-react'

export interface ReportFiltersState {
  status: 'all' | 'success' | 'failed'
  dateRange: 'all' | 'today' | '7days' | '30days'
}

interface ReportFiltersProps {
  filters: ReportFiltersState
  onFilterChange: (filters: ReportFiltersState) => void
}

export function ReportFilters({ filters, onFilterChange }: ReportFiltersProps) {
  const updateFilter = <K extends keyof ReportFiltersState>(
    key: K,
    value: ReportFiltersState[K]
  ) => {
    onFilterChange({
      ...filters,
      [key]: value,
    })
  }

  return (
    <div className="flex items-center gap-4 mb-4">
      <div className="flex items-center gap-2 text-gray-500">
        <Filter className="w-4 h-4" />
        <span className="text-sm">筛选</span>
      </div>

      <select
        value={filters.status}
        onChange={e => updateFilter('status', e.target.value as ReportFiltersState['status'])}
        className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="all">全部状态</option>
        <option value="success">成功</option>
        <option value="failed">失败</option>
      </select>

      <select
        value={filters.dateRange}
        onChange={e => updateFilter('dateRange', e.target.value as ReportFiltersState['dateRange'])}
        className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="all">全部时间</option>
        <option value="today">今天</option>
        <option value="7days">最近 7 天</option>
        <option value="30days">最近 30 天</option>
      </select>
    </div>
  )
}
