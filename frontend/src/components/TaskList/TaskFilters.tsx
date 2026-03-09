import { Search } from 'lucide-react'
import type { Filters } from '../../hooks/useTasks'

interface TaskFiltersProps {
  filters: Filters
  onFilterChange: <K extends keyof Filters>(key: K, value: Filters[K]) => void
}

export function TaskFilters({ filters, onFilterChange }: TaskFiltersProps) {
  return (
    <div className="flex items-center gap-4 mb-4">
      <div className="relative flex-1 max-w-sm">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          placeholder="搜索任务名称..."
          value={filters.search}
          onChange={e => onFilterChange('search', e.target.value)}
          className="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <select
        value={filters.status}
        onChange={e => onFilterChange('status', e.target.value as Filters['status'])}
        className="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="all">全部状态</option>
        <option value="draft">草稿</option>
        <option value="ready">就绪</option>
      </select>

      <div className="flex items-center gap-2">
        <select
          value={filters.sortBy}
          onChange={e => onFilterChange('sortBy', e.target.value as Filters['sortBy'])}
          className="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="updated_at">按更新时间</option>
          <option value="created_at">按创建时间</option>
          <option value="name">按名称</option>
        </select>
        <button
          onClick={() => onFilterChange('sortOrder', filters.sortOrder === 'asc' ? 'desc' : 'asc')}
          className="px-3 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50"
        >
          {filters.sortOrder === 'asc' ? '↑ 升序' : '↓ 降序'}
        </button>
      </div>
    </div>
  )
}
