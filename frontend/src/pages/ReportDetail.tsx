import { useState, useEffect } from 'react'
import { useParams, Navigate } from 'react-router-dom'
import { Layers, CheckCircle, XCircle, Clock } from 'lucide-react'
import { ReportHeader, SummaryCard, TimelineItemCard } from '../components/Report'
import { StatusBadge, type Status } from '../components/shared/StatusBadge'
import { getReport, type ReportDetailResponse } from '../api/reports'

export function ReportDetail() {
  const { id } = useParams<{ id: string }>()
  const [data, setData] = useState<ReportDetailResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    if (!id) return

    setLoading(true)
    getReport(id)
      .then(setData)
      .catch(err => {
        setError(err instanceof Error ? err : new Error('Failed to fetch report'))
        console.error('Failed to fetch report:', err)
      })
      .finally(() => setLoading(false))
  }, [id])

  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`
    return `${Math.floor(ms / 60000)}m ${Math.floor((ms % 60000) / 1000)}s`
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  if (error || !data) {
    return <Navigate to="/reports" replace />
  }

  return (
    <div className="max-w-5xl mx-auto">
      {/* 头部 */}
      <ReportHeader taskName={data.task_name} status={data.status} />

      {/* 摘要卡片 */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <SummaryCard
          icon={<Layers className="w-5 h-5" />}
          label="总步骤"
          value={data.total_steps}
        />
        <SummaryCard
          icon={<CheckCircle className="w-5 h-5" />}
          label="成功数"
          value={data.success_steps}
          valueColor="text-green-600"
        />
        <SummaryCard
          icon={<XCircle className="w-5 h-5" />}
          label="失败数"
          value={data.failed_steps}
          valueColor={data.failed_steps > 0 ? 'text-red-600' : 'text-gray-900'}
        />
        <SummaryCard
          icon={<Clock className="w-5 h-5" />}
          label="总耗时"
          value={formatDuration(data.duration_ms)}
        />
      </div>

      {/* 执行状态 */}
      {data.execution_status && data.execution_status !== 'pending' && (
        <div className="flex items-center gap-2 mb-6 px-4 py-2 bg-gray-50 rounded-lg">
          <span className="text-sm text-gray-600">执行状态:</span>
          <StatusBadge status={data.execution_status as Status} />
        </div>
      )}

      {/* 统一时间线 */}
      <div className="space-y-3">
        <h2 className="text-lg font-medium text-gray-900 mb-3">执行步骤</h2>
        {(() => {
          const displayItems = data.timeline_items && data.timeline_items.length > 0
            ? data.timeline_items
            : data.steps.map((step, idx) => ({
                type: 'step' as const,
                id: `legacy-${idx}`,
                sequence_number: idx,
                step_index: step.index,
                action: step.action,
                reasoning: step.reasoning || null,
                screenshot_url: step.screenshot || null,
                status: step.status,
                error: step.error || null,
                duration_ms: step.duration_ms,
              }))

          return displayItems.map((item, index) => (
            <TimelineItemCard
              key={`${item.type}-${item.id}`}
              item={item}
              defaultExpanded={index === 0 || item.status === 'failed' || item.status === 'fail'}
            />
          ))
        })()}
      </div>
    </div>
  )
}
