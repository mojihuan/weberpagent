import { useNavigate } from 'react-router-dom'
import type { Run } from '../../types'
import { StatusBadge, LoadingSpinner, EmptyState } from '../shared'

interface RunHistoryProps {
  runs: Run[]
  loading: boolean
}

function formatDuration(ms: number): string {
  const seconds = Math.floor(ms / 1000)
  if (seconds < 60) return `${seconds}s`
  const minutes = Math.floor(seconds / 60)
  const remainSeconds = seconds % 60
  return `${minutes}m ${remainSeconds}s`
}

function formatDateTime(dateStr: string): string {
  return new Date(dateStr).toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function RunHistory({ runs, loading }: RunHistoryProps) {
  const navigate = useNavigate()

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <LoadingSpinner />
      </div>
    )
  }

  if (runs.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h3 className="text-base font-medium text-gray-900 mb-4">执行历史</h3>
        <EmptyState message="暂无执行记录" />
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h3 className="text-base font-medium text-gray-900 mb-4">执行历史</h3>
      <div className="space-y-2">
        {runs.map(run => (
          <div
            key={run.id}
            onClick={() => navigate(`/runs/${run.id}`)}
            className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
          >
            <div className="flex items-center gap-3">
              <StatusBadge status={run.status} />
              <span className="text-gray-900">{formatDateTime(run.started_at)}</span>
            </div>
            <div className="flex items-center gap-4 text-sm text-gray-500">
              <span>耗时 {formatDuration(run.steps.reduce((sum, s) => sum + s.duration_ms, 0))}</span>
              <span>步数 {run.steps.filter(s => s.status === 'success').length}/{run.steps.length}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
