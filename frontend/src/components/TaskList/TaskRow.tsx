import { useState } from 'react'
import { Play, Pencil, Trash2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import type { Task } from '../../types'
import { StatusBadge } from '../shared'
import { startRun } from '../../api/runs'

interface TaskRowProps {
  task: Task
  selected: boolean
  onSelect: () => void
  onEdit: () => void
  onDelete: () => void
}

export function TaskRow({ task, selected, onSelect, onEdit, onDelete }: TaskRowProps) {
  const navigate = useNavigate()
  const [isStarting, setIsStarting] = useState(false)

  const handleExecute = async (e: React.MouseEvent) => {
    e.stopPropagation()
    if (isStarting) return

    setIsStarting(true)
    try {
      const { runId } = await startRun(task.id)
      navigate(`/runs/${runId}`)
    } catch (error) {
      console.error('Failed to start run:', error)
    } finally {
      setIsStarting(false)
    }
  }

  const handleEdit = (e: React.MouseEvent) => {
    e.stopPropagation()
    onEdit()
  }

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation()
    onDelete()
  }

  const handleRowClick = () => {
    navigate(`/tasks/${task.id}`)
  }

  const domain = (() => {
    try {
      return new URL(task.target_url).hostname
    } catch {
      return task.target_url
    }
  })()

  return (
    <tr
      onClick={handleRowClick}
      className="border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition-colors"
    >
      <td className="px-4 py-3" onClick={e => e.stopPropagation()}>
        <input
          type="checkbox"
          checked={selected}
          onChange={onSelect}
          className="w-4 h-4 rounded border-gray-300 text-blue-500 focus:ring-blue-500"
        />
      </td>
      <td className="px-4 py-3">
        <div className="font-medium text-gray-900">{task.name}</div>
        <div className="text-sm text-gray-500 truncate max-w-xs">{task.description}</div>
      </td>
      <td className="px-4 py-3 text-gray-500 text-sm">{domain}</td>
      <td className="px-4 py-3">
        <StatusBadge status={task.status} />
      </td>
      <td className="px-4 py-3 text-gray-500 text-sm">{task.max_steps}</td>
      <td className="px-4 py-3">
        <div className="flex items-center gap-1">
          <button
            onClick={handleExecute}
            disabled={isStarting}
            className={`p-1.5 rounded hover:bg-gray-100 ${
              isStarting
                ? 'text-gray-300 cursor-wait'
                : 'text-gray-500 hover:text-green-500'
            }`}
            title="立即执行"
          >
            <Play className="w-4 h-4" />
          </button>
          <button
            onClick={handleEdit}
            className="p-1.5 rounded hover:bg-gray-100 text-gray-500 hover:text-gray-700"
            title="编辑"
          >
            <Pencil className="w-4 h-4" />
          </button>
          <button
            onClick={handleDelete}
            className="p-1.5 rounded hover:bg-gray-100 text-gray-500 hover:text-red-500"
            title="删除"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </td>
    </tr>
  )
}
