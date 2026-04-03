import { useState } from 'react'
import { CheckCircle, XCircle, Loader2, Circle, FileCode, ShieldCheck } from 'lucide-react'
import type { Step, SSEPreconditionEvent, SSEAssertionEvent, TimelineItem } from '../../types'

interface StepTimelineProps {
  items: TimelineItem[]
  currentStepIndex: number
  onItemClick: (item: TimelineItem, timelineIndex: number) => void
}

function getStatusIcon(
  status: 'success' | 'failed' | 'running' | 'pending',
  type: 'step' | 'precondition' | 'assertion'
) {
  const colorMap = {
    step: { success: 'text-green-500', running: 'text-blue-500', failed: 'text-red-500', pending: 'text-gray-300' },
    precondition: { success: 'text-amber-500', running: 'text-amber-500', failed: 'text-red-500', pending: 'text-gray-300' },
    assertion: { success: 'text-purple-500', running: 'text-purple-500', failed: 'text-red-500', pending: 'text-gray-300' },
  }

  const color = colorMap[type][status]

  switch (status) {
    case 'success':
      return <CheckCircle className={`w-5 h-5 ${color}`} />
    case 'failed':
      return <XCircle className={`w-5 h-5 ${color}`} />
    case 'running':
      return <Loader2 className={`w-5 h-5 ${color} animate-spin`} />
    case 'pending':
      return <Circle className={`w-5 h-5 ${color}`} />
  }
}

function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`
  return `${(ms / 1000).toFixed(1)}s`
}

function truncateCode(code: string, maxLen: number = 60): string {
  if (code.length <= maxLen) return code
  return code.slice(0, maxLen) + '...'
}

function StepTimeline({ items, currentStepIndex, onItemClick }: StepTimelineProps) {
  const [expanded, setExpanded] = useState<Set<number>>(new Set())

  const toggleExpand = (index: number) => {
    setExpanded(prev => {
      const next = new Set(prev)
      if (next.has(index)) {
        next.delete(index)
      } else {
        next.add(index)
      }
      return next
    })
  }

  const getItemStatus = (index: number): 'success' | 'failed' | 'running' | 'pending' => {
    const item = items[index]
    if (!item) return 'pending'
    if (item.type === 'step') {
      const actualStatus = item.data.status || 'success'
      if (index < currentStepIndex) return actualStatus
      if (index === currentStepIndex) {
        // Use actual status if terminal, otherwise running
        if (actualStatus === 'success' || actualStatus === 'failed') return actualStatus
        return 'running'
      }
      return 'pending'
    }
    if (item.type === 'assertion') {
      return item.data.status === 'pass' ? 'success' : 'failed'
    }
    // precondition items
    const actualStatus = item.data.status || 'pending'
    if (actualStatus === 'success' || actualStatus === 'failed') return actualStatus
    return actualStatus === 'running' ? 'running' : 'pending'
  }

  const renderStepItem = (data: Step) => {
    return (
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <span className="text-sm font-medium text-gray-900">
            步骤 {data.index}
          </span>
          {data.duration_ms > 0 && (
            <span className="text-xs text-gray-500">
              {formatDuration(data.duration_ms)}
            </span>
          )}
        </div>
        <p className="text-sm text-gray-600 truncate">{data.action}</p>
        {data.error && (
          <p className="text-xs text-red-500 mt-1 truncate">{data.error}</p>
        )}
      </div>
    )
  }

  const renderPreconditionItem = (data: SSEPreconditionEvent, timelineIndex: number) => {
    const isExpanded = expanded.has(timelineIndex)
    return (
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-1.5">
            <FileCode className="w-4 h-4 text-amber-500" />
            <span className="text-sm font-medium text-amber-700">
              前置条件 {data.index + 1}
            </span>
          </div>
          {data.duration_ms != null && data.duration_ms > 0 && (
            <span className="text-xs text-gray-500">
              {formatDuration(data.duration_ms)}
            </span>
          )}
        </div>
        <p className="text-sm text-gray-600 font-mono truncate">
          {truncateCode(data.code)}
        </p>
        {data.error && (
          <p className="text-xs text-red-500 mt-1 truncate">{data.error}</p>
        )}
        {isExpanded && (
          <div className="mt-2 p-3 bg-amber-50 rounded-lg text-sm space-y-2">
            <div>
              <span className="font-medium text-gray-700">完整代码:</span>
              <pre className="mt-1 text-xs text-gray-600 whitespace-pre-wrap font-mono">{data.code}</pre>
            </div>
            {data.variables && Object.keys(data.variables).length > 0 && (
              <div>
                <span className="font-medium text-gray-700">变量输出:</span>
                <pre className="mt-1 text-xs text-gray-600 whitespace-pre-wrap font-mono">
                  {JSON.stringify(data.variables, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}
      </div>
    )
  }

  const renderAssertionItem = (data: SSEAssertionEvent) => {
    return (
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-purple-500" />
            <span className="text-sm font-medium text-purple-700">
              断言: {data.assertion_name}
            </span>
          </div>
        </div>
        <p className="text-sm text-gray-600">
          {data.status === 'pass' ? '通过' : '失败'}
        </p>
        {data.message && (
          <p className={`text-xs mt-1 truncate ${data.status === 'pass' ? 'text-gray-500' : 'text-red-500'}`}>
            {data.message}
          </p>
        )}
      </div>
    )
  }

  const handleItemClick = (item: TimelineItem, timelineIndex: number) => {
    if (item.type === 'step') {
      onItemClick(item, timelineIndex)
    } else {
      toggleExpand(timelineIndex)
    }
  }

  const getItemType = (item: TimelineItem): 'step' | 'precondition' | 'assertion' => {
    return item.type
  }

  if (items.length === 0) {
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
          {items.map((item, index) => {
            const status = getItemStatus(index)
            const isLast = index === items.length - 1

            return (
              <div
                key={index}
                onClick={() => handleItemClick(item, index)}
                className="relative flex gap-3 pb-4 cursor-pointer hover:bg-gray-50 -mx-2 px-2 rounded"
              >
                {/* Connector line */}
                {!isLast && (
                  <div className="absolute left-[10px] top-[22px] w-0.5 h-full bg-gray-200" />
                )}

                {/* Status icon */}
                <div className="relative z-10 bg-white">{getStatusIcon(status, getItemType(item))}</div>

                {/* Content */}
                {item.type === 'step' && renderStepItem(item.data)}
                {item.type === 'precondition' && renderPreconditionItem(item.data, index)}
                {item.type === 'assertion' && renderAssertionItem(item.data)}
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export { StepTimeline }
