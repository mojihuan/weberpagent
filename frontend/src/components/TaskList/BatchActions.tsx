import { Trash2, CheckCircle, Play } from 'lucide-react'

interface BatchActionsProps {
  selectedCount: number
  onBatchDelete: () => void
  onBatchSetReady: () => void
  onBatchExecute: () => void
  batchExecuting?: boolean
}

export function BatchActions({
  selectedCount,
  onBatchDelete,
  onBatchSetReady,
  onBatchExecute,
  batchExecuting = false,
}: BatchActionsProps) {
  if (selectedCount === 0) return null

  return (
    <div className="flex items-center gap-4 px-4 py-2 bg-blue-50 border-y border-blue-100">
      <span className="text-sm text-blue-700">已选中 {selectedCount} 项</span>
      <div className="flex items-center gap-2">
        <button
          onClick={onBatchExecute}
          disabled={batchExecuting}
          className="flex items-center gap-1 px-3 py-1.5 text-sm text-green-700 hover:bg-green-50 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Play className="w-4 h-4" />
          {batchExecuting ? '启动中...' : '批量执行'}
        </button>
        <button
          onClick={onBatchSetReady}
          className="flex items-center gap-1 px-3 py-1.5 text-sm text-blue-700 hover:bg-blue-100 rounded-lg transition-colors"
        >
          <CheckCircle className="w-4 h-4" />
          设为就绪
        </button>
        <button
          onClick={onBatchDelete}
          className="flex items-center gap-1 px-3 py-1.5 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
        >
          <Trash2 className="w-4 h-4" />
          批量删除
        </button>
      </div>
    </div>
  )
}
