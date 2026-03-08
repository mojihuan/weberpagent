import { Link } from 'react-router-dom'
import { Play, CheckCircle, XCircle, Clock, Loader2 } from 'lucide-react'

// 模拟数据（后续对接 API）
const mockRuns = [
  {
    id: 'run-001',
    task_name: '登录功能测试',
    status: 'success' as const,
    started_at: '2026-03-08 16:30:00',
    duration_ms: 45000,
    steps_count: 5,
  },
  {
    id: 'run-002',
    task_name: '表单提交测试',
    status: 'failed' as const,
    started_at: '2026-03-08 15:20:00',
    duration_ms: 30000,
    steps_count: 3,
  },
  {
    id: 'run-003',
    task_name: '搜索功能测试',
    status: 'running' as const,
    started_at: '2026-03-08 17:00:00',
    duration_ms: 0,
    steps_count: 2,
  },
]

const statusConfig = {
  running: { icon: Loader2, color: 'text-blue-500', bg: 'bg-blue-50', label: '执行中' },
  success: { icon: CheckCircle, color: 'text-green-500', bg: 'bg-green-50', label: '成功' },
  failed: { icon: XCircle, color: 'text-red-500', bg: 'bg-red-50', label: '失败' },
  stopped: { icon: Clock, color: 'text-gray-500', bg: 'bg-gray-50', label: '已停止' },
}

function formatDuration(ms: number): string {
  if (ms === 0) return '-'
  const seconds = Math.floor(ms / 1000)
  if (seconds < 60) return `${seconds}秒`
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}分${remainingSeconds}秒`
}

export function RunList() {
  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">执行监控</h1>
        <button className="flex items-center gap-2 px-4 h-9 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 transition-colors">
          <Play className="w-4 h-4" />
          新建执行
        </button>
      </div>

      {/* 执行历史列表 */}
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">任务名称</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">状态</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">开始时间</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">耗时</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">步骤数</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">操作</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {mockRuns.map((run) => {
              const config = statusConfig[run.status]
              const StatusIcon = config.icon
              return (
                <tr key={run.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-3 text-sm font-medium text-gray-900">
                    {run.task_name}
                  </td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-medium ${config.bg} ${config.color}`}>
                      <StatusIcon className={`w-3.5 h-3.5 ${run.status === 'running' ? 'animate-spin' : ''}`} />
                      {config.label}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">
                    {run.started_at}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">
                    {formatDuration(run.duration_ms)}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">
                    {run.steps_count}
                  </td>
                  <td className="px-4 py-3">
                    <Link
                      to={`/runs/${run.id}`}
                      className="text-sm text-blue-500 hover:text-blue-600 font-medium"
                    >
                      查看详情
                    </Link>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* 空状态 */}
      {mockRuns.length === 0 && (
        <div className="flex flex-col items-center justify-center py-16 text-gray-500">
          <Play className="w-12 h-12 mb-4 text-gray-300" />
          <p className="text-lg font-medium text-gray-900">暂无执行记录</p>
          <p className="text-sm mt-1">创建任务后可启动执行</p>
        </div>
      )}
    </div>
  )
}
