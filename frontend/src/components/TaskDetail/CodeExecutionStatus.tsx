import { Loader2, CheckCircle2, XCircle } from 'lucide-react'

export type ExecutionState = 'idle' | 'waiting' | 'running' | 'success' | 'failed'

interface CodeExecutionStatusProps {
  state: ExecutionState
  error?: string | null
}

export function CodeExecutionStatus({ state, error }: CodeExecutionStatusProps) {
  if (state === 'idle') return null

  return (
    <div className="flex flex-col">
      {state === 'waiting' && (
        <div className="flex items-center gap-2 text-gray-500">
          <Loader2 className="w-4 h-4 animate-spin" />
          <span className="text-sm">等待执行...</span>
        </div>
      )}
      {state === 'running' && (
        <div className="flex items-center gap-2 text-blue-500">
          <Loader2 className="w-4 h-4 animate-spin" />
          <span className="text-sm">执行中...</span>
        </div>
      )}
      {state === 'success' && (
        <div className="flex items-center gap-2 text-green-600">
          <CheckCircle2 className="w-4 h-4" />
          <span className="text-sm font-medium">执行成功</span>
        </div>
      )}
      {state === 'failed' && (
        <div>
          <div className="flex items-center gap-2 text-red-600">
            <XCircle className="w-4 h-4" />
            <span className="text-sm font-medium">执行失败</span>
          </div>
          {error && (
            <div className="mt-2 max-h-24 overflow-auto bg-red-50 border border-red-200 rounded-lg p-3">
              <pre className="text-sm text-red-600 font-mono whitespace-pre-wrap">{error}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
