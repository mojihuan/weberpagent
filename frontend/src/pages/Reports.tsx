import { useReports } from '../hooks/useReports'
import { ReportFilters, ReportTable, type ReportFiltersState } from '../components/Report'
import { Pagination, EmptyState } from '../components/shared'

export function Reports() {
  const {
    reports,
    total,
    loading,
    error,
    filters,
    page,
    pageSize,
    setPage,
    updateFilter,
    refresh,
  } = useReports()

  const hasFilters = filters.status !== 'all' || filters.dateRange !== 'all'

  // 筛选变化处理
  const handleFilterChange = (newFilters: ReportFiltersState) => {
    Object.entries(newFilters).forEach(([key, value]) => {
      updateFilter(key as keyof ReportFiltersState, value)
    })
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-red-700">
        加载失败: {error.message}
        <button onClick={refresh} className="ml-4 text-red-600 underline">
          重试
        </button>
      </div>
    )
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

      {/* 加载状态 */}
      {loading ? (
        <div className="bg-white rounded-xl border border-gray-200 p-8">
          <div className="flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
          </div>
        </div>
      ) : reports.length === 0 ? (
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
