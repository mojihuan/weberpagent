// frontend/src/hooks/useRunStream.ts
import { useState, useEffect, useCallback, useRef, useMemo } from 'react'
import { toast } from 'sonner'
import type { Run, Step, SSEPreconditionEvent, SSEAssertionEvent, RunStatus } from '../types'

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

  // Ref-based mutable arrays for O(1) appends (replaces O(n^2) spread copies)
  const stepsRef = useRef<Step[]>([])
  const timelineRef = useRef<TimelineItem[]>([])
  const preconditionsRef = useRef<SSEPreconditionEvent[]>([])
  const versionRef = useRef(0)
  const [version, setVersion] = useState(0)

  // Base run data (scalar fields, no arrays)
  const [baseRun, setBaseRun] = useState<{
    id: string
    task_id: string
    status: RunStatus
    started_at: string
    finished_at?: string
    assertion_summary?: { total: number; passed: number; failed: number; errors: number }
  } | null>(null)

  // Connection state
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const streamRef = useRef<EventSource | null>(null)
  const isConnectedRef = useRef(false)

  // Version counter bumps trigger useMemo recomputation
  const bumpVersion = () => {
    versionRef.current += 1
    setVersion(versionRef.current)
  }

  // Compute run object from baseRun + refs, only recomputes when version or baseRun changes
  const run = useMemo<Run | null>(() => {
    if (!baseRun) return null
    return {
      ...baseRun,
      steps: stepsRef.current,
      preconditions: preconditionsRef.current,
      timeline: timelineRef.current,
    }
  }, [version, baseRun])

  const connect = useCallback(() => {
    // 使用 ref 检查，避免循环依赖
    if (isConnectedRef.current) return

    setError(null)
    // Do NOT set isConnected here -- wait for onopen

    // 真实 SSE 连接 - 使用 EventSource (GET 请求)
    const eventSource = new EventSource(`${API_BASE}/runs/${runId}/stream`)
    streamRef.current = eventSource

    eventSource.onopen = () => {
      setIsConnected(true)
      isConnectedRef.current = true
    }

    eventSource.addEventListener('started', (e: MessageEvent) => {
      let data: { task_id?: string }
      try {
        data = JSON.parse(e.data)
      } catch (err) {
        console.error('[useRunStream] Failed to parse "started" event data:', err, 'raw data:', e.data)
        toast.error('数据解析错误')
        return
      }
      stepsRef.current = []
      timelineRef.current = []
      preconditionsRef.current = []
      setBaseRun({
        id: runId,
        task_id: data.task_id || '',
        status: 'running' as RunStatus,
        started_at: new Date().toISOString(),
      })
      setIsConnected(true)
      isConnectedRef.current = true
    })

    eventSource.addEventListener('step', (e: MessageEvent) => {
      let stepData: { index: number; action: string; reasoning?: string; screenshot_url?: string; status: string; duration_ms?: number }
      try {
        stepData = JSON.parse(e.data)
      } catch (err) {
        console.error('[useRunStream] Failed to parse "step" event data:', err, 'raw data:', e.data)
        toast.error('数据解析错误')
        return
      }
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
      stepsRef.current.push(newStep)
      timelineRef.current.push({ type: 'step' as const, data: newStep })
      bumpVersion()
    })

    eventSource.addEventListener('precondition', (e: MessageEvent) => {
      let data: SSEPreconditionEvent
      try {
        data = JSON.parse(e.data) as SSEPreconditionEvent
      } catch (err) {
        console.error('[useRunStream] Failed to parse "precondition" event data:', err, 'raw data:', e.data)
        toast.error('数据解析错误')
        return
      }
      const existingIdx = timelineRef.current.findIndex(
        item => item.type === 'precondition' && item.data.index === data.index
      )
      if (existingIdx >= 0) {
        timelineRef.current[existingIdx] = { type: 'precondition' as const, data }
        const precondIdx = preconditionsRef.current.findIndex(p => p.index === data.index)
        if (precondIdx >= 0) {
          preconditionsRef.current[precondIdx] = data
        }
      } else {
        timelineRef.current.push({ type: 'precondition' as const, data })
        preconditionsRef.current.push(data)
      }
      if (!baseRun) {
        setBaseRun({
          id: runId,
          task_id: '',
          status: 'running' as RunStatus,
          started_at: new Date().toISOString(),
        })
      }
      bumpVersion()
    })

    eventSource.addEventListener('external_assertions', (e: MessageEvent) => {
      let data: { total?: number; passed?: number; failed?: number; errors?: number }
      try {
        data = JSON.parse(e.data)
      } catch (err) {
        console.error('[useRunStream] Failed to parse "external_assertions" event data:', err, 'raw data:', e.data)
        toast.error('数据解析错误')
        return
      }
      setBaseRun(prev => prev ? {
        ...prev,
        assertion_summary: {
          total: data.total ?? 0,
          passed: data.passed ?? 0,
          failed: data.failed ?? 0,
          errors: data.errors ?? 0,
        },
      } : prev)
    })

    eventSource.addEventListener('assertion', (e: MessageEvent) => {
      let data: SSEAssertionEvent
      try {
        data = JSON.parse(e.data) as SSEAssertionEvent
      } catch (err) {
        console.error('[useRunStream] Failed to parse "assertion" event data:', err, 'raw data:', e.data)
        toast.error('数据解析错误')
        return
      }
      timelineRef.current.push({ type: 'assertion' as const, data })
      if (!baseRun) {
        setBaseRun({
          id: runId,
          task_id: '',
          status: 'running' as RunStatus,
          started_at: new Date().toISOString(),
        })
      }
      bumpVersion()
    })

    eventSource.addEventListener('finished', (e: MessageEvent) => {
      let parsed: { status?: string }
      try {
        parsed = JSON.parse(e.data)
      } catch (err) {
        console.error('[useRunStream] Failed to parse "finished" event data:', err, 'raw data:', e.data)
        toast.error('数据解析错误')
        return
      }
      setBaseRun(prev => prev ? {
        ...prev,
        status: parsed.status as RunStatus,
        finished_at: new Date().toISOString(),
      } : prev)
      setIsConnected(false)
      isConnectedRef.current = false
      eventSource.close()
    })

    eventSource.addEventListener('error', (e: MessageEvent) => {
      if (e.data) {
        let parsed: { error?: string }
        try {
          parsed = JSON.parse(e.data)
        } catch (err) {
          console.error('[useRunStream] Failed to parse "error" event data:', err, 'raw data:', e.data)
          toast.error('数据解析错误')
          parsed = { error: 'Unknown error' }
        }
        setError(new Error(parsed.error || 'Unknown error'))
      }
      // Update run status to failed on error
      setBaseRun(prev => prev ? {
        ...prev,
        status: 'failed' as RunStatus,
        finished_at: new Date().toISOString(),
      } : prev)
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
    stepsRef.current = []
    timelineRef.current = []
    preconditionsRef.current = []
    versionRef.current = 0
    setBaseRun(null)
    setVersion(0)
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
