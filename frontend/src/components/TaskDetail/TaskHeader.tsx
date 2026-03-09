import { ArrowLeft, Play, Pencil, Trash2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import type { Task } from '../../types'
import { Button } from '../Button'
import { StatusBadge } from '../shared'

interface TaskHeaderProps {
  task: Task
  onEdit: () => void
  onDelete: () => void
  onExecute: () => void
}

export function TaskHeader({ task, onEdit, onDelete, onExecute }: TaskHeaderProps) {
  const navigate = useNavigate()

  return (
    <div className="mb-6">
      <button
        onClick={() => navigate('/tasks')}
        className="flex items-center gap-1 text-gray-500 hover:text-gray-700 mb-4"
      >
        <ArrowLeft className="w-4 h-4" />
        返回列表
      </button>

      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-2xl font-semibold text-gray-900">{task.name}</h1>
            <StatusBadge status={task.status} />
          </div>
          <p className="text-gray-500">{task.description}</p>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="secondary" onClick={onExecute}>
            <Play className="w-4 h-4 mr-1" />
            立即执行
          </Button>
          <Button variant="secondary" onClick={onEdit}>
            <Pencil className="w-4 h-4 mr-1" />
            编辑
          </Button>
          <Button variant="secondary" onClick={onDelete} className="text-red-600 hover:bg-red-50">
            <Trash2 className="w-4 h-4 mr-1" />
            删除
          </Button>
        </div>
      </div>
    </div>
  )
}
