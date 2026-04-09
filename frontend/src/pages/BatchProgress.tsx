import { useParams } from 'react-router-dom'
import { useRef, useEffect } from 'react'
import { toast } from 'sonner'
import { useBatchProgress } from '../hooks/useBatchProgress'
import { BatchSummary, BatchTaskCard } from '../components/BatchProgress'
import { LoadingSpinner } from '../components/shared'
import type { BatchRunSummary } from '../types'

function countByStatus(runs: BatchRunSummary[], status: string): number {
  return runs.filter(r => r.status === status).length
}

export function BatchProgress() {
  const { id: batchId } = useParams<{ id: string }>()
  const { batch, runs, loading, error, refetch } = useBatchProgress(batchId!)

  const toastShownRef = useRef(false)
  const prevBatchStatusRef = useRef<string | null>(null)

  useEffect(() => {
    if (!batch) return

    const prevStatus = prevBatchStatusRef.current
    prevBatchStatusRef.current = batch.status

    if (batch.status === 'completed' && prevStatus !== 'completed' && !toastShownRef.current) {
      toastShownRef.current = true
      const successCount = countByStatus(runs, 'success')
      const failedCount = countByStatus(runs, 'failed')
      const message = `批量执行完成：${successCount} 成功，${failedCount} 失败`

      if (failedCount > 0) {
        toast.warning(message)
      } else {
        toast.success(message)
      }
    }
  }, [batch, runs])

  if (loading && runs.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (error && !batch) {
    return (
      <div className="flex flex-col items-center justify-center h-64">
        <p className="text-red-500 mb-4">加载批次进度失败，请刷新页面重试</p>
        <button
          onClick={refetch}
          className="px-4 py-2 text-sm text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors"
        >
          刷新重试
        </button>
      </div>
    )
  }

  const completed = runs.filter(r => r.status === 'success' || r.status === 'failed' || r.status === 'completed').length
  const total = runs.length
  const successCount = countByStatus(runs, 'success') + countByStatus(runs, 'completed')
  const failedCount = countByStatus(runs, 'failed')
  const isCompleted = batch?.status === 'completed'

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">
        批量执行进度
      </h1>

      <div className="mb-6">
        <BatchSummary
          completed={completed}
          total={total}
          successCount={successCount}
          failedCount={failedCount}
          isCompleted={isCompleted}
        />
      </div>

      {runs.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12">
          <LoadingSpinner size="md" />
          <p className="text-gray-500 mt-4">正在加载任务列表...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {runs.map(run => (
            <BatchTaskCard key={run.id} run={run} />
          ))}
        </div>
      )}
    </div>
  )
}
