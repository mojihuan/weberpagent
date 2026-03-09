import { StatCard, TrendChart, QuickStart, RecentRuns } from '../components/Dashboard'
import { useDashboard } from '../hooks/useDashboard'
import { useTasks } from '../hooks/useTasks'

export function Dashboard() {
  const { stats, trendData, recentRuns, loading } = useDashboard()
  const { allTasks, loading: tasksLoading } = useTasks()

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">仪表盘</h1>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="总任务数"
          value={stats.totalTasks}
          icon="📊"
        />
        <StatCard
          title="总执行次数"
          value={stats.totalRuns}
          icon="🔄"
        />
        <StatCard
          title="成功率"
          value={`${stats.successRate}%`}
          icon="✅"
          trend="5% 较上周"
          trendUp={true}
        />
        <StatCard
          title="今日执行"
          value={stats.todayRuns}
          icon="📅"
        />
      </div>

      {/* 趋势图 + 快速启动 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <TrendChart data={trendData} loading={loading} />
        </div>
        <div className="lg:col-span-1">
          <QuickStart tasks={allTasks} loading={tasksLoading} />
        </div>
      </div>

      {/* 最近执行记录 */}
      <RecentRuns runs={recentRuns} loading={loading} />
    </div>
  )
}
