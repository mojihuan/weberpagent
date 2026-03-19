import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Play, CheckCircle, XCircle, Clock, Loader2 } from 'lucide-react'
import { listRuns } from '../api/runs'
import type { Run } from '../types'
import { LoadingSpinner } from '../components/shared'

const statusConfig = {
  pending: { icon: Clock, color: 'text-yellow-500', bg: 'bg-yellow-50', label: '等待中' },
  running: { icon: Loader2, color: 'text-blue-500', bg: 'bg-blue-50', label: '执行中' },
  success: { icon: CheckCircle, color: 'text-green-500', bg: 'bg-green-50', label: '成功' },
  failed: { icon: XCircle, color: 'text-red-500', bg: 'bg-red-50', label: '失败' },
  stopped: { icon: Clock, color: 'text-gray-500', bg: 'bg-gray-50', label: '已停止' },
}

function formatDuration(startedAt: string | null | undefined, finishedAt: string | null | undefined): string {
  if (!startedAt) return '-'
  const start = new Date(startedAt).getTime()
  const end = finishedAt ? new Date(finishedAt).getTime() : Date.now()
  const ms = end - start
  const seconds = Math.floor(ms / 1000)
  if (seconds < 60) return `${seconds}秒`
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}分${remainingSeconds}秒`
}

function formatDateTime(dateStr: string | null): string {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

interface RunWithDetails extends Run {
  task_name?: string
  steps_count?: number
}

export function RunList() {
  const [runs, setRuns] = useState<RunWithDetails[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchRuns = async () => {
      try {
        setLoading(true)
        const data = await listRuns()
        setRuns(data)
        setError(null)
      } catch (err) {
        console.error('Failed to fetch runs:', err)
        setError('加载执行记录失败')
      } finally {
        setLoading(false)
      }
    }
    fetchRuns()
  }, [])

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12 text-red-500">
        <p>{error}</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">执行监控</h1>
      </div>

      {/* 执行历史列表 */}
      {runs.length > 0 ? (
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
              {runs.map((run) => {
                const config = statusConfig[run.status as keyof typeof statusConfig] || statusConfig.pending
                const StatusIcon = config.icon
                return (
                  <tr key={run.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">
                      {run.task_name || '未知任务'}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-medium ${config.bg} ${config.color}`}>
                        <StatusIcon className={`w-3.5 h-3.5 ${run.status === 'running' ? 'animate-spin' : ''}`} />
                        {config.label}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-500">
                      {formatDateTime(run.started_at)}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-500">
                      {formatDuration(run.started_at, run.finished_at)}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-500">
                      {run.steps_count ?? 0}
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
      ) : (
        <div className="flex flex-col items-center justify-center py-16 text-gray-500 bg-white rounded-lg border border-gray-200">
          <Play className="w-12 h-12 mb-4 text-gray-300" />
          <p className="text-lg font-medium text-gray-900">暂无执行记录</p>
          <p className="text-sm mt-1">创建任务后可启动执行</p>
          <Link
            to="/tasks"
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600"
          >
            前往任务列表
          </Link>
        </div>
      )}
    </div>
  )
}
