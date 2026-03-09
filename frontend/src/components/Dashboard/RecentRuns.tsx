import { useNavigate } from 'react-router-dom'
import type { RecentRun } from '../../types'
import { StatusBadge } from '../shared/StatusBadge'

interface RecentRunsProps {
  runs: RecentRun[]
  loading?: boolean
}

function formatTime(isoString: string): string {
  const date = new Date(isoString)
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

function formatDuration(ms: number): string {
  if (ms === 0) return '-'
  if (ms < 1000) return `${ms}ms`
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`
  return `${Math.floor(ms / 60000)}m ${Math.floor((ms % 60000) / 1000)}s`
}

export function RecentRuns({ runs, loading }: RecentRunsProps) {
  const navigate = useNavigate()

  if (loading) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-medium text-gray-900 flex items-center gap-2">
            <span>📋</span>
            <span>最近执行记录</span>
          </h3>
        </div>
        <div className="text-center py-8 text-gray-400">加载中...</div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-medium text-gray-900 flex items-center gap-2">
          <span>📋</span>
          <span>最近执行记录</span>
        </h3>
        <button
          onClick={() => navigate('/reports')}
          className="text-sm text-blue-500 hover:text-blue-600 font-medium"
        >
          查看全部 →
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="text-left text-sm text-gray-500 border-b border-gray-200">
              <th className="pb-3 font-medium">任务名称</th>
              <th className="pb-3 font-medium">状态</th>
              <th className="pb-3 font-medium">执行时间</th>
              <th className="pb-3 font-medium text-right">耗时</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {runs.map(run => (
              <tr
                key={run.id}
                onClick={() => navigate(`/reports/${run.id}`)}
                className="cursor-pointer hover:bg-gray-50 transition-colors"
              >
                <td className="py-3 text-sm text-gray-900">{run.task_name}</td>
                <td className="py-3">
                  <StatusBadge status={run.status} />
                </td>
                <td className="py-3 text-sm text-gray-500">
                  {formatTime(run.started_at)}
                </td>
                <td className="py-3 text-sm text-gray-500 text-right">
                  {formatDuration(run.duration_ms)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {runs.length === 0 && (
          <div className="text-center py-8 text-gray-400">
            暂无执行记录
          </div>
        )}
      </div>
    </div>
  )
}
