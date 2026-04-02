import { useState } from 'react'
import { ChevronDown, ChevronRight, CheckCircle, XCircle, Clock, FileCode, ShieldCheck } from 'lucide-react'
import { ImageViewer, ReasoningText } from '../shared'
import type { ReportTimelineItem, ReportTimelineStep, ReportTimelinePrecondition, ReportTimelineAssertion } from '../../types'

interface TimelineItemCardProps {
  item: ReportTimelineItem
  defaultExpanded?: boolean
}

function formatDuration(ms: number | null | undefined): string {
  if (ms == null || ms === 0) return '-'
  if (ms < 1000) return `${ms}ms`
  return `${(ms / 1000).toFixed(1)}s`
}

function StatusIcon({ status, type }: { status: string; type: 'step' | 'precondition' | 'assertion' }) {
  const isSuccess = status === 'success' || status === 'pass'
  const colorMap = {
    step: { success: 'text-green-500', failed: 'text-red-500' },
    precondition: { success: 'text-amber-500', failed: 'text-red-500' },
    assertion: { success: 'text-purple-500', failed: 'text-red-500' },
  }
  const color = isSuccess ? colorMap[type].success : colorMap[type].failed
  return isSuccess
    ? <CheckCircle className={`w-5 h-5 ${color}`} />
    : <XCircle className={`w-5 h-5 ${color}`} />
}

function StepExpandedContent({ step }: { step: ReportTimelineStep }) {
  const [viewerOpen, setViewerOpen] = useState(false)
  const API_BASE = import.meta.env.VITE_API_BASE?.replace('/api', '') || 'http://localhost:8080'

  let screenshotUrl = step.screenshot_url || ''
  if (screenshotUrl && !screenshotUrl.startsWith('http')) {
    if (screenshotUrl.startsWith('/api/')) {
      screenshotUrl = `${API_BASE}${screenshotUrl}`
    } else {
      screenshotUrl = `${API_BASE}/api${screenshotUrl}`
    }
  }

  return (
    <div className="border-t border-gray-200 p-4 bg-gray-50">
      {step.error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600 font-medium">错误信息</p>
          <p className="text-sm text-red-500 mt-1">{step.error}</p>
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-sm font-medium text-gray-700 mb-2">截图</p>
          {screenshotUrl ? (
            <div className="relative cursor-pointer group" onClick={() => setViewerOpen(true)}>
              <img
                src={screenshotUrl}
                alt={`步骤 ${step.step_index} 截图`}
                className="w-full h-48 object-cover rounded-lg border border-gray-200 bg-white"
              />
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition rounded-lg flex items-center justify-center">
                <span className="text-white opacity-0 group-hover:opacity-100 text-sm font-medium">
                  点击查看大图
                </span>
              </div>
            </div>
          ) : (
            <div className="w-full h-48 bg-gray-100 rounded-lg border border-gray-200 flex items-center justify-center text-gray-400 text-sm">
              无截图
            </div>
          )}
        </div>
        <div>
          <p className="text-sm font-medium text-gray-700 mb-2">AI 推理过程</p>
          <div className="h-48 overflow-y-auto p-3 bg-white rounded-lg border border-gray-200">
            {step.reasoning ? (
              <ReasoningText text={step.reasoning} />
            ) : (
              <p className="text-sm text-gray-400 italic">暂无推理记录</p>
            )}
          </div>
        </div>
      </div>

      {screenshotUrl && (
        <ImageViewer
          src={screenshotUrl}
          isOpen={viewerOpen}
          onClose={() => setViewerOpen(false)}
        />
      )}
    </div>
  )
}

function PreconditionExpandedContent({ item }: { item: ReportTimelinePrecondition }) {
  return (
    <div className="border-t border-gray-200 p-4 bg-amber-50">
      {item.error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600 font-medium">错误信息</p>
          <p className="text-sm text-red-500 mt-1">{item.error}</p>
        </div>
      )}
      <div className="mb-3">
        <p className="text-sm font-medium text-gray-700 mb-2">完整代码:</p>
        <pre className="p-2 bg-gray-100 rounded text-xs font-mono whitespace-pre-wrap overflow-auto">{item.code}</pre>
      </div>
      {item.variables && Object.keys(item.variables).length > 0 && (
        <div>
          <p className="text-sm font-medium text-gray-700 mb-2">变量输出:</p>
          <div className="bg-gray-50 rounded p-2 font-mono text-sm">
            {Object.entries(item.variables).map(([key, value]) => (
              <div key={key} className="flex gap-2">
                <span className="text-blue-600">{key}</span>
                <span className="text-gray-400">=</span>
                <span className="text-green-600">
                  {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function AssertionExpandedContent({ item }: { item: ReportTimelineAssertion }) {
  return (
    <div className="border-t border-gray-200 p-4 bg-purple-50">
      {item.message && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600 font-medium">错误信息</p>
          <p className="text-sm text-red-500 mt-1">{item.message}</p>
        </div>
      )}
      {item.field_results && item.field_results.length > 0 && (
        <div>
          <p className="text-sm font-medium text-gray-700 mb-2">字段结果:</p>
          <div className="space-y-1">
            {item.field_results.map((field, idx) => (
              <p key={idx} className={`text-xs font-mono ${field.passed ? 'text-green-600' : 'text-red-600'}`}>
                {field.passed ? '[PASS]' : '[FAIL]'} {field.field_name}: {field.message}
              </p>
            ))}
          </div>
        </div>
      )}
      {(!item.field_results || item.field_results.length === 0) && item.message && (
        <div>
          <p className="text-sm font-medium text-gray-700 mb-2">结果信息:</p>
          <p className="text-sm text-gray-600">{item.message}</p>
          {item.actual_value && (
            <p className="text-sm text-gray-500 mt-1">实际值: {item.actual_value}</p>
          )}
        </div>
      )}
    </div>
  )
}

export function TimelineItemCard({ item, defaultExpanded = false }: TimelineItemCardProps) {
  const [expanded, setExpanded] = useState(defaultExpanded)

  const renderHeader = () => {
    switch (item.type) {
      case 'step': {
        const s = item as ReportTimelineStep
        return (
          <>
            <StatusIcon status={s.status} type="step" />
            <div className="flex-1 text-left">
              <span className="font-medium text-gray-900">步骤 {s.step_index}</span>
              <span className="text-gray-400 mx-2">-</span>
              <span className="text-gray-700">{s.action}</span>
            </div>
          </>
        )
      }
      case 'precondition': {
        const p = item as ReportTimelinePrecondition
        const codeTruncated = p.code.length > 80 ? p.code.slice(0, 80) + '...' : p.code
        return (
          <>
            <StatusIcon status={p.status} type="precondition" />
            <FileCode className="w-4 h-4 text-amber-500" />
            <div className="flex-1 text-left">
              <span className="font-medium text-amber-700">前置条件 {p.index + 1}</span>
              <span className="text-gray-400 mx-2">-</span>
              <span className="text-gray-700 font-mono truncate">{codeTruncated}</span>
            </div>
          </>
        )
      }
      case 'assertion': {
        const a = item as ReportTimelineAssertion
        return (
          <>
            <StatusIcon status={a.status} type="assertion" />
            <ShieldCheck className="w-4 h-4 text-purple-500" />
            <div className="flex-1 text-left">
              <span className="font-medium text-purple-700">
                断言 {a.assertion_name || a.assertion_id}
              </span>
              <span className="text-gray-400 mx-2">-</span>
              <span className="text-gray-700">{a.status === 'pass' ? '通过' : '失败'}</span>
            </div>
          </>
        )
      }
    }
  }

  const renderExpandedContent = () => {
    switch (item.type) {
      case 'step':
        return <StepExpandedContent step={item as ReportTimelineStep} />
      case 'precondition':
        return <PreconditionExpandedContent item={item as ReportTimelinePrecondition} />
      case 'assertion':
        return <AssertionExpandedContent item={item as ReportTimelineAssertion} />
    }
  }

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition"
      >
        {expanded ? (
          <ChevronDown className="w-5 h-5 text-gray-400" />
        ) : (
          <ChevronRight className="w-5 h-5 text-gray-400" />
        )}
        {renderHeader()}
        <div className="flex items-center gap-1 text-sm text-gray-500">
          <Clock className="w-4 h-4" />
          <span>{formatDuration(item.duration_ms)}</span>
        </div>
      </button>
      {expanded && renderExpandedContent()}
    </div>
  )
}
