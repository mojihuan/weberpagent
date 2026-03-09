import { CheckCircle, XCircle, Loader2, Circle } from 'lucide-react'
import type { Step } from '../../types'

interface StepTimelineProps {
  steps: Step[]
  currentStepIndex: number
  onStepClick: (index: number) => void
}

export function StepTimeline({ steps, currentStepIndex, onStepClick }: StepTimelineProps) {
  const getStepStatus = (index: number): 'success' | 'failed' | 'running' | 'pending' => {
    if (index < currentStepIndex) {
      return steps[index]?.status || 'success'
    }
    if (index === currentStepIndex) {
      return 'running'
    }
    return 'pending'
  }

  const getStepIcon = (status: 'success' | 'failed' | 'running' | 'pending') => {
    switch (status) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />
      case 'running':
        return <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
      case 'pending':
        return <Circle className="w-5 h-5 text-gray-300" />
    }
  }

  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`
    return `${(ms / 1000).toFixed(1)}s`
  }

  if (steps.length === 0) {
    return (
      <div className="flex flex-col h-full overflow-hidden">
        <div className="px-4 py-3 border-b border-gray-200">
          <h3 className="font-medium text-gray-900">执行步骤</h3>
        </div>
        <div className="flex-1 flex items-center justify-center text-gray-400">
          等待执行开始...
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-200">
        <h3 className="font-medium text-gray-900">执行步骤</h3>
      </div>
      <div className="flex-1 overflow-y-auto p-4">
        <div className="relative">
          {steps.map((step, index) => {
            const status = getStepStatus(index)
            const isClickable = index <= currentStepIndex
            const isLast = index === steps.length - 1

            return (
              <div
                key={index}
                onClick={() => isClickable && onStepClick(index)}
                className={`relative flex gap-3 pb-4 ${
                  isClickable ? 'cursor-pointer hover:bg-gray-50 -mx-2 px-2 rounded' : ''
                }`}
              >
                {/* 连接线 */}
                {!isLast && (
                  <div className="absolute left-[10px] top-[22px] w-0.5 h-full bg-gray-200" />
                )}

                {/* 状态图标 */}
                <div className="relative z-10 bg-white">{getStepIcon(status)}</div>

                {/* 内容 */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-sm font-medium text-gray-900">
                      步骤 {step.index}
                    </span>
                    {step.duration_ms > 0 && (
                      <span className="text-xs text-gray-500">
                        {formatDuration(step.duration_ms)}
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-600 truncate">{step.action}</p>
                  {step.error && (
                    <p className="text-xs text-red-500 mt-1 truncate">{step.error}</p>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
