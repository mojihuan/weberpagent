interface BatchSummaryProps {
  completed: number
  total: number
  successCount: number
  failedCount: number
  isCompleted: boolean
}

export function BatchSummary({ completed, total, successCount, failedCount, isCompleted }: BatchSummaryProps) {
  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0

  if (isCompleted) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-xl p-6">
        <div className="h-2 rounded-full bg-gray-100 mb-4">
          <div
            className="h-2 rounded-full bg-green-500 transition-all duration-500"
            style={{ width: '100%' }}
          />
        </div>
        <p className="text-lg font-semibold text-green-800">
          全部完成：{successCount} 成功，{failedCount} 失败
        </p>
      </div>
    )
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6">
      <div className="h-2 rounded-full bg-gray-100 mb-4">
        <div
          className="h-2 rounded-full bg-blue-500 transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <p className="text-sm text-gray-500">
        {completed} / {total} 已完成
      </p>
    </div>
  )
}
