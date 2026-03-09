import { useState } from 'react'
import { X } from 'lucide-react'
import type { Task, CreateTaskDto } from '../../types'
import { TaskForm } from './TaskForm'

interface TaskFormModalProps {
  open: boolean
  onClose: () => void
  mode: 'create' | 'edit'
  task?: Task
  onSubmit: (data: CreateTaskDto) => Promise<void>
}

export function TaskFormModal({ open, onClose, mode, task, onSubmit }: TaskFormModalProps) {
  const [loading, setLoading] = useState(false)

  if (!open) return null

  const handleSubmit = async (data: CreateTaskDto) => {
    setLoading(true)
    try {
      await onSubmit(data)
      onClose()
    } catch (error) {
      console.error('Failed to submit:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/50" onClick={onClose} />
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-lg mx-4 max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">
            {mode === 'create' ? '新建任务' : '编辑任务'}
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="p-6">
          <TaskForm
            initialData={task}
            mode={mode}
            onSubmit={handleSubmit}
            onCancel={onClose}
            loading={loading}
          />
        </div>
      </div>
    </div>
  )
}
