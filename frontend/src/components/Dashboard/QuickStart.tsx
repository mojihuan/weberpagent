import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import type { Task } from '../../types'
import { startRun } from '../../api/runs'

interface QuickStartProps {
  tasks: Task[]
  loading?: boolean
}

export function QuickStart({ tasks, loading }: QuickStartProps) {
  const navigate = useNavigate()
  const [selectedTaskId, setSelectedTaskId] = useState<string>('')
  const [starting, setStarting] = useState(false)

  const readyTasks = tasks.filter(t => t.status === 'ready')

  const handleStart = async () => {
    if (!selectedTaskId || starting) return

    setStarting(true)
    try {
      const { runId } = await startRun(selectedTaskId)
      navigate(`/runs/${runId}`)
    } catch (error) {
      console.error('Failed to start run:', error)
    } finally {
      setStarting(false)
    }
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h3 className="text-base font-medium text-gray-900 mb-4 flex items-center gap-2">
        <span>🚀</span>
        <span>快速启动</span>
      </h3>

      <div className="space-y-4">
        <select
          value={selectedTaskId}
          onChange={(e) => setSelectedTaskId(e.target.value)}
          disabled={loading || starting}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
        >
          <option value="">选择任务...</option>
          {readyTasks.map(task => (
            <option key={task.id} value={task.id}>
              {task.name}
            </option>
          ))}
        </select>

        <button
          onClick={handleStart}
          disabled={!selectedTaskId || starting}
          className="w-full px-4 py-2 bg-blue-500 text-white text-sm font-medium rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {starting ? '启动中...' : '启动执行'}
        </button>

        {readyTasks.length === 0 && !loading && (
          <p className="text-sm text-gray-500 text-center">
            暂无可执行的任务
          </p>
        )}
      </div>
    </div>
  )
}
