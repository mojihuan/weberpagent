import { useState } from 'react'
import { ChevronDown, ChevronRight, CheckCircle, XCircle, Clock } from 'lucide-react'
import { ImageViewer } from '../shared'
import type { Step } from '../../types'

interface StepItemProps {
  step: Step
  defaultExpanded?: boolean
}

export function StepItem({ step, defaultExpanded = false }: StepItemProps) {
  const [expanded, setExpanded] = useState(defaultExpanded)
  const [viewerOpen, setViewerOpen] = useState(false)

  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`
    return `${(ms / 1000).toFixed(1)}s`
  }

  const isSuccess = step.status === 'success'

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      {/* 步骤头部 */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition"
      >
        {/* 展开图标 */}
        {expanded ? (
          <ChevronDown className="w-5 h-5 text-gray-400" />
        ) : (
          <ChevronRight className="w-5 h-5 text-gray-400" />
        )}

        {/* 状态图标 */}
        {isSuccess ? (
          <CheckCircle className="w-5 h-5 text-green-500" />
        ) : (
          <XCircle className="w-5 h-5 text-red-500" />
        )}

        {/* 步骤信息 */}
        <div className="flex-1 text-left">
          <span className="font-medium text-gray-900">步骤 {step.index}</span>
          <span className="text-gray-500 mx-2">-</span>
          <span className="text-gray-700">{step.action}</span>
        </div>

        {/* 耗时 */}
        <div className="flex items-center gap-1 text-sm text-gray-500">
          <Clock className="w-4 h-4" />
          <span>{formatDuration(step.duration_ms)}</span>
        </div>
      </button>

      {/* 展开内容 */}
      {expanded && (
        <div className="border-t border-gray-200 p-4 bg-gray-50">
          {/* 错误信息 */}
          {step.error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-600 font-medium">错误信息</p>
              <p className="text-sm text-red-500 mt-1">{step.error}</p>
            </div>
          )}

          {/* 截图和推理 */}
          <div className="grid grid-cols-2 gap-4">
            {/* 截图预览 */}
            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">截图</p>
              <div
                className="relative cursor-pointer group"
                onClick={() => setViewerOpen(true)}
              >
                <img
                  src={step.screenshot}
                  alt={`步骤 ${step.index} 截图`}
                  className="w-full h-48 object-cover rounded-lg border border-gray-200 bg-white"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition rounded-lg flex items-center justify-center">
                  <span className="text-white opacity-0 group-hover:opacity-100 text-sm font-medium">
                    点击查看大图
                  </span>
                </div>
              </div>
            </div>

            {/* AI 推理 */}
            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">AI 推理过程</p>
              <div className="h-48 overflow-y-auto p-3 bg-white rounded-lg border border-gray-200">
                {step.reasoning ? (
                  <p className="text-sm text-gray-600 whitespace-pre-wrap">{step.reasoning}</p>
                ) : (
                  <p className="text-sm text-gray-400 italic">暂无推理记录</p>
                )}
              </div>
            </div>
          </div>

          {/* 图片查看器 */}
          <ImageViewer
            src={step.screenshot}
            isOpen={viewerOpen}
            onClose={() => setViewerOpen(false)}
          />
        </div>
      )}
    </div>
  )
}
