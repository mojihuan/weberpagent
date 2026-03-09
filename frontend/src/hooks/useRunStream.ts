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
        break

      case 'error':
        setError(new Error(event.data.error || 'Unknown error'))
        setIsConnected(false)
        break
    }
  }, [runId])

  const connect = useCallback(() => {
    if (isConnected) return

    setError(null)
    setIsConnected(true)

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
  }, [runId, isConnected, useMock, handleEvent])

  const disconnect = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.stop()
      streamRef.current = null
    }
    setIsConnected(false)
  }, [])

  useEffect(() => {
    if (autoConnect) {
      connect()
    }
    return () => {
      disconnect()
    }
  }, [autoConnect, connect, disconnect])

  return {
    run,
    isConnected,
    error,
    connect,
    disconnect,
  }
}
