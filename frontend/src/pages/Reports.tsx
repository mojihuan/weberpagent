import { useState } from 'react'
import { ReportFilters, ReportTable, type ReportFiltersState } from '../components/Report'
import { Pagination, EmptyState } from '../components/shared'
import { getReports } from '../api/mock/reports'

export function Reports() {
  const [filters, setFilters] = useState<ReportFiltersState>({
    status: 'all',
    dateRange: 'all',
  })
  const [page, setPage] = useState(1)
  const pageSize = 10

  // 获取报告数据
  const { reports, total } = getReports({
    status: filters.status === 'all' ? undefined : filters.status,
    date: filters.dateRange === 'all' ? undefined :
      filters.dateRange === 'today' ? 'today' :
      filters.dateRange === '7days' ? '7days' : '30days',
    page,
    pageSize,
  })

  const hasFilters = filters.status !== 'all' || filters.dateRange !== 'all'

  // 筛选变化时重置页码
  const handleFilterChange = (newFilters: ReportFiltersState) => {
    setFilters(newFilters)
    setPage(1)
  }

  return (
    <div>
      {/* 页面标题 */}
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">报告查看</h1>
        <p className="mt-1 text-gray-500">查看测试执行报告</p>
      </div>

      {/* 筛选栏 */}
      <ReportFilters
        filters={filters}
        onFilterChange={handleFilterChange}
      />

      {/* 表格 */}
      {reports.length === 0 ? (
        <div className="bg-white rounded-xl border border-gray-200 p-8">
          <EmptyState
            message={hasFilters ? '没有找到匹配的报告' : '暂无执行报告'}
          />
        </div>
      ) : (
        <ReportTable reports={reports} />
      )}

      {/* 分页 */}
      {total > pageSize && (
        <Pagination
          total={total}
          page={page}
          pageSize={pageSize}
          onChange={setPage}
        />
      )}
    </div>
  )
}
