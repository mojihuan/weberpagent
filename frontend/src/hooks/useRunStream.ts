// frontend/src/hooks/useRunStream.ts
import { useState, useEffect, useCallback, useRef } from 'react'
import type { Run, Step, SSEPreconditionEvent, SSEAssertionEvent } from '../types'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:11002/api'

interface UseRunStreamOptions {
  runId: string
  autoConnect?: boolean
  useMock?: boolean // 保留参数以保持向后兼容，但不再使用
}

interface UseRunStreamReturn {
  run: Run | null
  isConnected: boolean
  error: Error | null
  connect: () => void
  disconnect: () => void
}

export function useRunStream(options: UseRunStreamOptions): UseRunStreamReturn {
  const { runId, autoConnect = true } = options

  const [run, setRun] = useState<Run | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const streamRef = useRef<EventSource | null>(null)
  const isConnectedRef = useRef(false)

  const connect = useCallback(() => {
    // 使用 ref 检查，避免循环依赖
    if (isConnectedRef.current) return

    setError(null)
    setIsConnected(true)
    isConnectedRef.current = true

    // 真实 SSE 连接 - 使用 EventSource (GET 请求)
    const eventSource = new EventSource(`${API_BASE}/runs/${runId}/stream`)
    streamRef.current = eventSource

    eventSource.addEventListener('started', (e: MessageEvent) => {
      const data = JSON.parse(e.data)
      setRun(prev => ({
        id: runId,
        task_id: data.task_id || prev?.task_id || '',
        status: 'running',
        started_at: new Date().toISOString(),
        steps: prev?.steps || [],
        preconditions: prev?.preconditions || [],
        timeline: prev?.timeline || [],
      }))
      setIsConnected(true)
      isConnectedRef.current = true
    })

    eventSource.addEventListener('step', (e: MessageEvent) => {
      const stepData = JSON.parse(e.data)
      setRun(prev => {
        if (!prev) return prev
        // 拼接完整的截图 URL
        const screenshotUrl = stepData.screenshot_url
          ? `${API_BASE}${stepData.screenshot_url}`
          : ''
        const newStep: Step = {
          index: stepData.index,
          action: stepData.action,
          reasoning: stepData.reasoning,
          screenshot: screenshotUrl,
          status: stepData.status,
          duration_ms: stepData.duration_ms || 0,
        }
        return {
          ...prev,
          steps: [...prev.steps, newStep],
          timeline: [...prev.timeline, { type: 'step' as const, data: newStep }],
        }
      })
    })

    eventSource.addEventListener('precondition', (e: MessageEvent) => {
      const data: SSEPreconditionEvent = JSON.parse(e.data)
      setRun(prev => {
        if (!prev) {
          return {
            id: runId,
            task_id: '',
            status: 'running',
            started_at: new Date().toISOString(),
            steps: [],
            preconditions: [data],
            timeline: [{ type: 'precondition' as const, data }],
          }
        }
        const existingIdx = prev.timeline.findIndex(
          item => item.type === 'precondition' && item.data.index === data.index
        )
        const newTimeline = existingIdx >= 0
          ? prev.timeline.map((item, i) => i === existingIdx ? { type: 'precondition' as const, data } : item)
          : [...prev.timeline, { type: 'precondition' as const, data }]
        const newPreconditions = existingIdx >= 0
          ? prev.preconditions?.map((p) => p.index === data.index ? data : p) ?? [data]
          : [...(prev.preconditions || []), data]
        return { ...prev, preconditions: newPreconditions, timeline: newTimeline }
      })
    })

    eventSource.addEventListener('external_assertions', (e: MessageEvent) => {
      const data = JSON.parse(e.data)
      setRun(prev => {
        if (!prev) return prev
        return {
          ...prev,
          assertion_summary: {
            total: data.total ?? 0,
            passed: data.passed ?? 0,
            failed: data.failed ?? 0,
            errors: data.errors ?? 0,
          },
        }
      })
    })

    eventSource.addEventListener('assertion', (e: MessageEvent) => {
      const data: SSEAssertionEvent = JSON.parse(e.data)
      setRun(prev => {
        if (!prev) {
          return {
            id: runId,
            task_id: '',
            status: 'running',
            started_at: new Date().toISOString(),
            steps: [],
            preconditions: [],
            timeline: [{ type: 'assertion' as const, data }],
          }
        }
        return {
          ...prev,
          timeline: [...prev.timeline, { type: 'assertion' as const, data }],
        }
      })
    })

    eventSource.addEventListener('finished', (e: MessageEvent) => {
      const parsed = JSON.parse(e.data)
      setRun(prev => {
        if (!prev) return prev
        return {
          ...prev,
          status: parsed.status,
          finished_at: new Date().toISOString(),
        }
      })
      setIsConnected(false)
      isConnectedRef.current = false
      eventSource.close()
    })

    eventSource.addEventListener('error', (e: MessageEvent) => {
      if (e.data) {
        const parsed = JSON.parse(e.data)
        setError(new Error(parsed.error || 'Unknown error'))
      }
      // Update run status to failed on error
      setRun(prev => {
        if (!prev) return prev
        return {
          ...prev,
          status: 'failed',
          finished_at: new Date().toISOString(),
        }
      })
      setIsConnected(false)
      isConnectedRef.current = false
      eventSource.close()
    })

    eventSource.onerror = () => {
      // 连接错误，可能是网络问题或执行已结束
      if (eventSource.readyState === EventSource.CLOSED) {
        setIsConnected(false)
        isConnectedRef.current = false
      }
    }
  }, [runId])

  const disconnect = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.close()
      streamRef.current = null
    }
    setIsConnected(false)
    isConnectedRef.current = false
  }, [])

  useEffect(() => {
    if (autoConnect) {
      connect()
    }
    return () => {
      disconnect()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [autoConnect, runId]) // 只在 autoConnect 和 runId 变化时重新连接

  return {
    run,
    isConnected,
    error,
    connect,
    disconnect,
  }
}
