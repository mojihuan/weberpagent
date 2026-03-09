import { Trash2, CheckCircle } from 'lucide-react'

interface BatchActionsProps {
  selectedCount: number
  onBatchDelete: () => void
  onBatchSetReady: () => void
}

export function BatchActions({ selectedCount, onBatchDelete, onBatchSetReady }: BatchActionsProps) {
  if (selectedCount === 0) return null

  return (
    <div className="flex items-center gap-4 px-4 py-2 bg-blue-50 border-y border-blue-100">
      <span className="text-sm text-blue-700">已选中 {selectedCount} 项</span>
      <div className="flex items-center gap-2">
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
