import { FileQuestion } from 'lucide-react'

interface EmptyStateProps {
  message?: string
  action?: React.ReactNode
}

export function EmptyState({ message = '暂无数据', action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <FileQuestion className="w-12 h-12 text-gray-300 mb-4" />
      <p className="text-gray-500 mb-4">{message}</p>
      {action}
    </div>
  )
}
