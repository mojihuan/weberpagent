import { useEffect, useRef } from 'react'
import type { Step } from '../../types'

interface ReasoningLogProps {
  steps: Step[]
  autoScroll?: boolean
}

export function ReasoningLog({ steps, autoScroll = true }: ReasoningLogProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (autoScroll && containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }, [steps, autoScroll])

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-200">
        <h3 className="font-medium text-gray-900">AI 推理日志</h3>
      </div>
      <div ref={containerRef} className="flex-1 overflow-y-auto p-4 space-y-4">
        {steps.length === 0 ? (
          <div className="text-gray-400 text-center py-8">
            <p>等待执行开始...</p>
          </div>
        ) : (
          steps.map((step, index) => (
            <div key={index} className="space-y-2">
              {/* Action 标签 */}
              <div className="flex items-start gap-2">
                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-700 shrink-0">
                  Action
                </span>
                <span className="text-sm text-gray-900">{step.action}</span>
              </div>

              {/* Reasoning 标签 */}
              {step.reasoning && (
                <div className="flex items-start gap-2">
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-600 shrink-0">
                    Reasoning
                  </span>
                  <span className="text-sm text-gray-600">{step.reasoning}</span>
                </div>
              )}

              {/* 错误信息 */}
              {step.error && (
                <div className="flex items-start gap-2">
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-700 shrink-0">
                    Error
                  </span>
                  <span className="text-sm text-red-600">{step.error}</span>
                </div>
              )}

              {index < steps.length - 1 && (
                <div className="border-b border-gray-100 my-2" />
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}
