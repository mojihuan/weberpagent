const statusConfig = {
  // Task/Run statuses
  draft: { label: '草稿', className: 'bg-gray-100 text-gray-600' },
  ready: { label: '就绪', className: 'bg-green-100 text-green-700' },
  pending: { label: '等待中', className: 'bg-yellow-100 text-yellow-700' },
  running: { label: '执行中', className: 'bg-blue-100 text-blue-700' },
  completed: { label: '已完成', className: 'bg-green-100 text-green-700' },
  failed: { label: '失败', className: 'bg-red-100 text-red-700' },
  stopped: { label: '已停止', className: 'bg-yellow-100 text-yellow-700' },
  // Assertion result statuses
  pass: { label: '通过', className: 'bg-green-100 text-green-700' },
  fail: { label: '未通过', className: 'bg-red-100 text-red-700' },
  // Legacy aliases (for backward compatibility)
  success: { label: '已完成', className: 'bg-green-100 text-green-700' },
} as const

type Status = keyof typeof statusConfig

interface StatusBadgeProps {
  status: Status
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status]

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${config.className}`}>
      {config.label}
    </span>
  )
}
