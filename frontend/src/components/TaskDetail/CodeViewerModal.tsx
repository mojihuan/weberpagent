import { useState, useEffect, useCallback } from 'react'
import { X, Play } from 'lucide-react'
import { toast } from 'sonner'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import type { Task } from '../../types'
import { getRunCode, executeRunCode, getRun } from '../../api/runs'
import { LoadingSpinner } from '../shared/LoadingSpinner'
import { CodeExecutionStatus, type ExecutionState } from './CodeExecutionStatus'

interface CodeViewerModalProps {
  task: Task
  onClose: () => void
}

export function CodeViewerModal({ task, onClose }: CodeViewerModalProps) {
  const [code, setCode] = useState<string | null>(null)
  const [codeLoading, setCodeLoading] = useState(true)
  const [codeError, setCodeError] = useState(false)
  const [execState, setExecState] = useState<ExecutionState>('idle')
  const [execError, setExecError] = useState<string | null>(null)

  // Load code on mount
  useEffect(() => {
    if (!task.latest_run_id) {
      setCodeLoading(false)
      return
    }

    let cancelled = false
    getRunCode(task.latest_run_id)
      .then((text) => {
        if (!cancelled) {
          setCode(text)
          setCodeLoading(false)
        }
      })
      .catch(() => {
        if (!cancelled) {
          setCodeError(true)
          setCodeLoading(false)
        }
      })
    return () => { cancelled = true }
  }, [task.latest_run_id])

  // Per D-05: poll GET /runs/{run_id} every 2 seconds after POST /execute-code returns 202
  useEffect(() => {
    if (execState !== 'waiting' && execState !== 'running') return
    if (!task.latest_run_id) return

    const poll = setInterval(async () => {
      try {
        const run = await getRun(task.latest_run_id!)
        if (run.status === 'success') {
          setExecState('success')
        } else if (run.status === 'failed') {
          setExecState('failed')
          setExecError('执行失败')
        }
      } catch {
        // Non-fatal polling error: continue polling
      }
    }, 2000)

    return () => clearInterval(poll)
  }, [execState, task.latest_run_id])

  const handleExecute = useCallback(async () => {
    if (!task.latest_run_id) return
    if (execState === 'waiting' || execState === 'running') return

    setExecState('waiting')
    setExecError(null)

    try {
      await executeRunCode(task.latest_run_id)
      setExecState('running')
    } catch (error: unknown) {
      const apiError = error as { status?: number; message?: string }
      // Per D-06: 409 conflict shows toast
      if (apiError?.status === 409) {
        toast.error('已有代码执行正在进行中，请稍后重试')
        setExecState('idle')
      } else {
        setExecState('failed')
        setExecError(apiError?.message || '执行请求失败')
      }
    }
  }, [task.latest_run_id, execState])

  const isExecInProgress = execState === 'waiting' || execState === 'running'

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/50" onClick={onClose} />
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-4xl mx-4 max-h-[80vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">任务代码</h3>
            <p className="text-sm text-gray-500 mt-0.5">{task.name}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Code area */}
        <div className="flex-1 overflow-auto px-6 py-4">
          {codeLoading && (
            <div className="flex items-center justify-center py-12">
              <LoadingSpinner size="lg" className="text-gray-400" />
            </div>
          )}
          {codeError && (
            <div className="text-center py-12">
              <p className="text-gray-500 mb-3">代码加载失败，请重试</p>
              <button
                onClick={() => window.location.reload()}
                className="text-blue-500 hover:text-blue-600 text-sm"
              >
                重试
              </button>
            </div>
          )}
          {code !== null && !codeLoading && (
            <div className="rounded-lg overflow-x-auto" style={{ background: '#1a1a2e' }}>
              <SyntaxHighlighter
                language="python"
                style={oneDark}
                showLineNumbers={true}
                customStyle={{ margin: 0, background: '#1a1a2e' }}
              >
                {code}
              </SyntaxHighlighter>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-6 py-4 border-t border-gray-200">
          <div>
            <CodeExecutionStatus state={execState} error={execError} />
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-lg text-sm text-gray-700 hover:bg-gray-100"
            >
              关闭
            </button>
            {code !== null && (
              <button
                onClick={handleExecute}
                disabled={isExecInProgress}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-sm ${
                  isExecInProgress
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-blue-500 hover:bg-blue-600 text-white'
                }`}
              >
                <Play className="w-4 h-4" />
                运行代码
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
