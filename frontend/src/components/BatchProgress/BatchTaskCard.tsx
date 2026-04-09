import { useNavigate } from 'react-router-dom'
import { StatusBadge } from '../shared/StatusBadge'
import type { BatchRunSummary } from '../../types'

interface BatchTaskCardProps {
  run: BatchRunSummary
}

function formatDuration(startTime: string, endTime?: string | null): string {
  const start = new Date(startTime).getTime()
  const end = endTime ? new Date(endTime).getTime() : Date.now()
  const seconds = Math.floor((end - start) / 1000)
  if (seconds < 60) return `${seconds}s`
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}m ${remainingSeconds}s`
}

function getBorderClass(status: string): string {
  switch (status) {
    case 'running':
      return 'border-l-4 border-l-blue-400'
    case 'success':
    case 'completed':
      return 'border-l-4 border-l-green-400'
    case 'failed':
      return 'border-l-4 border-l-red-400'
    case 'pending':
    default:
      return 'border-l-4 border-l-gray-300'
  }
}

function ElapsedTime({ run }: { run: BatchRunSummary }) {
  if (run.status === 'pending' || !run.started_at) {
    return null
  }

  if (run.status === 'running') {
    return (
      <span className="text-xs text-gray-400 mt-2">
        已用时 {formatDuration(run.started_at)}
      </span>
    )
  }

  if (run.finished_at) {
    return (
      <span className="text-xs text-gray-400 mt-2">
        耗时 {formatDuration(run.started_at, run.finished_at)}
      </span>
    )
  }

  return null
}

export function BatchTaskCard({ run }: BatchTaskCardProps) {
  const navigate = useNavigate()

  const handleClick = () => {
    navigate(`/runs/${run.id}`)
  }

  const isRunning = run.status === 'running'

  return (
    <div
      className={`p-4 bg-white border border-gray-200 rounded-xl hover:border-blue-300 hover:shadow-sm transition-all cursor-pointer ${getBorderClass(run.status)}`}
      onClick={handleClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          handleClick()
        }
      }}
    >
      <p className="text-sm text-gray-900 truncate" title={run.task_name ?? undefined}>
        {run.task_name ?? '未命名任务'}
      </p>
      <div className={`mt-2 ${isRunning ? 'animate-pulse' : ''}`}>
        <StatusBadge status={run.status as Parameters<typeof StatusBadge>[0]['status']} />
      </div>
      <ElapsedTime run={run} />
    </div>
  )
}
