import { useNavigate } from 'react-router-dom'
import { Eye, Clock, CheckCircle, XCircle } from 'lucide-react'
import { StatusBadge } from '../shared'
import type { Report } from '../../types'

interface ReportTableProps {
  reports: Report[]
}

export function ReportTable({ reports }: ReportTableProps) {
  const navigate = useNavigate()

  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`
    return `${Math.floor(ms / 60000)}m ${Math.floor((ms % 60000) / 1000)}s`
  }

  const formatDate = (dateStr: string): string => {
    const date = new Date(dateStr)
    return date.toLocaleString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const handleView = (reportId: string) => {
    navigate(`/reports/${reportId}`)
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-50 border-b border-gray-200">
          <tr>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">任务名称</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">状态</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">步骤</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">耗时</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">执行时间</th>
            <th className="px-4 py-3 text-right text-sm font-medium text-gray-500">操作</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {reports.map(report => (
            <tr key={report.id} className="hover:bg-gray-50">
              <td className="px-4 py-3">
                <span className="font-medium text-gray-900">{report.task_name}</span>
              </td>
              <td className="px-4 py-3">
                <StatusBadge status={report.status} />
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center gap-1 text-sm text-gray-600">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>{report.success_steps}</span>
                  {report.failed_steps > 0 && (
                    <>
                      <XCircle className="w-4 h-4 text-red-500 ml-2" />
                      <span>{report.failed_steps}</span>
                    </>
                  )}
                  <span className="text-gray-400 ml-1">/ {report.total_steps}</span>
                </div>
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center gap-1 text-sm text-gray-600">
                  <Clock className="w-4 h-4" />
                  <span>{formatDuration(report.duration_ms)}</span>
                </div>
              </td>
              <td className="px-4 py-3 text-sm text-gray-500">
                {formatDate(report.created_at)}
              </td>
              <td className="px-4 py-3 text-right">
                <button
                  onClick={() => handleView(report.id)}
                  className="inline-flex items-center gap-1 px-3 py-1 text-sm text-blue-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition"
                >
                  <Eye className="w-4 h-4" />
                  查看
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
