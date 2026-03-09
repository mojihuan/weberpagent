import { useParams, Navigate } from 'react-router-dom'
import { Layers, CheckCircle, XCircle, Clock } from 'lucide-react'
import { ReportHeader, SummaryCard, StepItem } from '../components/Report'
import { getReportDetail } from '../api/mock/reports'

export function ReportDetail() {
  const { id } = useParams<{ id: string }>()

  // 获取报告详情
  const data = id ? getReportDetail(id) : null

  if (!data || !data.report || !data.run) {
    return <Navigate to="/reports" replace />
  }

  const { report, run } = data

  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`
    return `${Math.floor(ms / 60000)}m ${Math.floor((ms % 60000) / 1000)}s`
  }

  return (
    <div className="max-w-5xl mx-auto">
      {/* 头部 */}
      <ReportHeader taskName={report.task_name} status={report.status} />

      {/* 摘要卡片 */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <SummaryCard
          icon={<Layers className="w-5 h-5" />}
          label="总步骤"
          value={report.total_steps}
        />
        <SummaryCard
          icon={<CheckCircle className="w-5 h-5" />}
          label="成功数"
          value={report.success_steps}
          valueColor="text-green-600"
        />
        <SummaryCard
          icon={<XCircle className="w-5 h-5" />}
          label="失败数"
          value={report.failed_steps}
          valueColor={report.failed_steps > 0 ? 'text-red-600' : 'text-gray-900'}
        />
        <SummaryCard
          icon={<Clock className="w-5 h-5" />}
          label="总耗时"
          value={formatDuration(report.duration_ms)}
        />
      </div>

      {/* 步骤列表 */}
      <div className="space-y-3">
        <h2 className="text-lg font-medium text-gray-900 mb-3">执行步骤</h2>
        {run.steps.map((step, index) => (
          <StepItem
            key={step.index}
            step={step}
            defaultExpanded={index === 0 || step.status === 'failed'}
          />
        ))}
      </div>
    </div>
  )
}
