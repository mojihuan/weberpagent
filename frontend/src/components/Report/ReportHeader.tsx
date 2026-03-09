import { useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { StatusBadge } from '../shared'

interface ReportHeaderProps {
  taskName: string
  status: 'success' | 'failed'
}

export function ReportHeader({ taskName, status }: ReportHeaderProps) {
  const navigate = useNavigate()

  return (
    <div className="flex items-center gap-4 mb-6">
      {/* 返回按钮 */}
      <button
        onClick={() => navigate('/reports')}
        className="p-2 hover:bg-gray-100 rounded-lg transition"
      >
        <ArrowLeft className="w-5 h-5 text-gray-600" />
      </button>

      {/* 标题和状态 */}
      <div className="flex-1">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-semibold text-gray-900">{taskName}</h1>
          <StatusBadge status={status} />
        </div>
        <p className="text-gray-500 mt-1">执行报告详情</p>
      </div>
    </div>
  )
}
