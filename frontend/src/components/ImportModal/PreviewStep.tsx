import { CheckCircle, AlertCircle } from 'lucide-react'
import { Button } from '../Button'
import { LoadingSpinner } from '../shared/LoadingSpinner'
import type { ImportPreviewResponse } from '../../api/tasks'

interface PreviewStepProps {
  data: ImportPreviewResponse
  file: File
  onConfirm: () => void
  onBack: () => void
  confirming: boolean
}

const PREVIEW_COLUMNS = [
  { key: 'name', label: '任务名称', width: 'w-40' },
  { key: 'login_role', label: '登录角色', width: 'w-20' },
  { key: 'description', label: '任务描述', width: '' },
  { key: 'target_url', label: '目标URL', width: 'w-40' },
  { key: 'max_steps', label: '最大步数', width: 'w-20' },
  { key: 'preconditions', label: '前置条件', width: 'w-32' },
  { key: 'assertions', label: '断言', width: 'w-32' },
] as const

function formatCellValue(value: unknown): string {
  if (value === null || value === undefined) return ''
  if (Array.isArray(value)) return JSON.stringify(value)
  if (typeof value === 'object') return JSON.stringify(value)
  return String(value)
}

export function PreviewStep({ data, file: _file, onConfirm, onBack, confirming }: PreviewStepProps) {
  return (
    <div className="flex flex-col">
      <div className="flex items-center justify-between mb-4 px-1">
        <span className="text-sm text-gray-600">
          共 {data.total_rows} 行数据，有效{' '}
          <span className="text-green-600">{data.valid_count}</span> 行，无效{' '}
          <span className="text-red-600">{data.error_count}</span> 行
        </span>
      </div>

      <div className="overflow-y-auto max-h-[50vh] border border-gray-200 rounded-lg">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 sticky top-0 z-10">
              <th className="px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider w-12">
                #
              </th>
              {PREVIEW_COLUMNS.map((col) => (
                <th
                  key={col.key}
                  className={`px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider ${col.width}`}
                >
                  {col.label}
                </th>
              ))}
              <th className="px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider w-24">
                状态
              </th>
            </tr>
          </thead>
          <tbody>
            {data.rows.map((row) => (
              <tr key={row.row_number} className={row.valid ? 'bg-white' : 'bg-red-50'}>
                <td className="px-3 py-2 text-gray-700">{row.row_number}</td>
                {PREVIEW_COLUMNS.map((col) => (
                  <td key={col.key} className="px-3 py-2 text-gray-700 max-w-[200px] truncate">
                    {formatCellValue(row.data[col.key])}
                  </td>
                ))}
                <td className="px-3 py-2">
                  {row.valid ? (
                    <CheckCircle className="w-4 h-4 text-green-500" />
                  ) : (
                    <div className="flex items-start gap-1">
                      <AlertCircle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
                      <span className="text-red-600 text-xs">
                        {row.errors.join('; ')}
                      </span>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-gray-100 mt-4">
        <Button variant="secondary" onClick={onBack}>
          重新选择
        </Button>
        <Button
          variant="primary"
          onClick={onConfirm}
          disabled={data.has_errors || confirming}
        >
          {confirming ? (
            <span className="flex items-center gap-2">
              <LoadingSpinner size="sm" />
              导入中...
            </span>
          ) : (
            '确认导入'
          )}
        </Button>
      </div>
    </div>
  )
}
