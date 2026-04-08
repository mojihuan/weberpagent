import { useState } from 'react'
import { X } from 'lucide-react'

interface BatchExecuteDialogProps {
  open: boolean
  taskCount: number
  onConfirm: (concurrency: number) => void
  onCancel: () => void
  loading?: boolean
}

export function BatchExecuteDialog({
  open,
  taskCount,
  onConfirm,
  onCancel,
  loading = false,
}: BatchExecuteDialogProps) {
  const [concurrency, setConcurrency] = useState(2)

  if (!open) return null

  const handleBackdropClick = () => {
    if (!loading) {
      onCancel()
    }
  }

  const handleConfirm = () => {
    onConfirm(concurrency)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/50" onClick={handleBackdropClick} />
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-md mx-4 p-6">
        <button
          onClick={onCancel}
          disabled={loading}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          <X className="w-5 h-5" />
        </button>

        <h3 className="text-lg font-semibold text-gray-900 mb-2">批量执行确认</h3>

        <p className="text-gray-500 mb-6">
          已选择 {taskCount} 个任务进行批量执行
        </p>

        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            并发数
          </label>
          <div className="flex items-center gap-3">
            <input
              type="range"
              min={1}
              max={4}
              step={1}
              value={concurrency}
              onChange={(e) => setConcurrency(Number(e.target.value))}
              disabled={loading}
              className="w-full accent-blue-500"
            />
            <span className="text-lg font-semibold text-blue-600 min-w-[1.5rem] text-center">
              {concurrency}
            </span>
          </div>
          <div className="flex justify-between mt-1">
            <span className="text-xs text-gray-400">1</span>
            <span className="text-xs text-gray-400">4</span>
          </div>
        </div>

        <p className="text-sm text-gray-500 mb-6">
          每个任务将独立执行，单个任务失败不影响其他任务继续运行。
        </p>

        <div className="flex justify-end gap-3">
          <button
            onClick={onCancel}
            disabled={loading}
            className="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 disabled:opacity-50"
          >
            取消
          </button>
          <button
            onClick={handleConfirm}
            disabled={loading}
            className="px-4 py-2 rounded-lg bg-blue-500 hover:bg-blue-600 text-white font-medium disabled:opacity-50"
          >
            {loading ? '启动中...' : '开始执行'}
          </button>
        </div>
      </div>
    </div>
  )
}
