// frontend/src/hooks/useRunStream.ts
import { useState, useEffect, useCallback, useRef } from 'react'
import type { Run } from '../types'
import { createMockRunStream, type RunEvent } from '../api/mock/runStream'

interface UseRunStreamOptions {
  runId: string
  autoConnect?: boolean
  useMock?: boolean
}

interface UseRunStreamReturn {
  run: Run | null
  isConnected: boolean
  error: Error | null
  connect: () => void
  disconnect: () => void
}

export function useRunStream(options: UseRunStreamOptions): UseRunStreamReturn {
  const { runId, autoConnect = true, useMock = true } = options

  const [run, setRun] = useState<Run | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const streamRef = useRef<ReturnType<typeof createMockRunStream> | null>(null)
  const isConnectedRef = useRef(false)

  const handleEvent = useCallback((event: RunEvent) => {
    switch (event.type) {
      case 'started':
        setRun({
          id: runId,
          task_id: '',
          status: 'running',
          started_at: new Date().toISOString(),
          steps: [],
        })
        setIsConnected(true)
        isConnectedRef.current = true
        break

      case 'step':
        setRun(prev => {
          if (!prev || !event.data.step) return prev
          return {
            ...prev,
            steps: [...prev.steps, event.data.step!],
          }
        })
        break

      case 'finished':
        setRun(prev => {
          if (!prev) return prev
          return {
            ...prev,
            status: event.data.status || 'success',
            finished_at: new Date().toISOString(),
          }
        })
        setIsConnected(false)
        isConnectedRef.current = false
        break

      case 'error':
        setError(new Error(event.data.error || 'Unknown error'))
        setIsConnected(false)
        isConnectedRef.current = false
        break
    }
  }, [runId])

  const connect = useCallback(() => {
    // 使用 ref 检查，避免循环依赖
    if (isConnectedRef.current) return

    setError(null)
    setIsConnected(true)
    isConnectedRef.current = true

    if (useMock) {
      streamRef.current = createMockRunStream({
        runId,
        onEvent: handleEvent,
      })
      streamRef.current.start()
    } else {
      // TODO: 实现真实 SSE 连接
      // const eventSource = new EventSource(`/api/runs/${runId}/stream`)
    }
  }, [runId, useMock, handleEvent])

  const disconnect = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.stop()
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
