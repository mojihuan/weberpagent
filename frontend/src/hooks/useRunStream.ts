// frontend/src/hooks/useRunStream.ts
import { useState, useEffect, useCallback, useRef } from 'react'
import type { Run, Step } from '../types'
import { createMockRunStream, type RunEvent } from '../api/mock/runStream'

const API_BASE = 'http://localhost:8080/api'

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

  const streamRef = useRef<ReturnType<typeof createMockRunStream> | EventSource | null>(null)
  const isConnectedRef = useRef(false)

  const handleMockEvent = useCallback((event: RunEvent) => {
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
      // Mock 模式
      streamRef.current = createMockRunStream({
        runId,
        onEvent: handleMockEvent,
      })
      streamRef.current.start()
    } else {
      // 真实 SSE 连接
      const eventSource = new EventSource(`${API_BASE}/runs/${runId}/execute`, {
        withCredentials: true,
      })

      eventSource.addEventListener('started', (e) => {
        try {
          const data = JSON.parse(e.data)
          setRun({
            id: runId,
            task_id: data.run_id || '',
            status: 'running',
            started_at: new Date().toISOString(),
            steps: [],
          })
          setIsConnected(true)
          isConnectedRef.current = true
        } catch (err) {
          console.error('Failed to parse started event:', err)
        }
      })

      eventSource.addEventListener('step', (e) => {
        try {
          const stepData = JSON.parse(e.data)
          setRun(prev => {
            if (!prev) return prev
            const newStep: Step = {
              index: stepData.index,
              action: stepData.action,
              reasoning: stepData.reasoning,
              screenshot: stepData.screenshot_url || '',
              status: stepData.status,
              duration_ms: stepData.duration_ms || 0,
            }
            return {
              ...prev,
              steps: [...prev.steps, newStep],
            }
          })
        } catch (err) {
            console.error('Failed to parse step event:', err)
          }
        }
      })

      eventSource.addEventListener('finished', (e) => {
        try {
          const data = JSON.parse(e.data)
          setRun(prev => {
            if (!prev) return prev
            return {
              ...prev,
              status: data.status,
              finished_at: new Date().toISOString(),
            }
          })
          setIsConnected(false)
          isConnectedRef.current = false
          eventSource.close()
        } catch (err) {
          console.error('Failed to parse finished event:', err)
        }
      })

      eventSource.addEventListener('error', (e) => {
        try {
          const data = JSON.parse(e.data)
          setError(new Error(data.error || 'Unknown error'))
        } catch {
          setError(new Error('SSE connection error'))
        }
        setIsConnected(false)
        isConnectedRef.current = false
        eventSource.close()
      })

      eventSource.onerror = () => {
        setError(new Error('SSE connection error'))
        setIsConnected(false)
        isConnectedRef.current = false
        eventSource.close()
      }

      streamRef.current = eventSource
    }
  }, [runId, useMock, handleMockEvent])

  const disconnect = useCallback(() => {
    if (streamRef.current) {
      if ('stop' in streamRef.current) {
        // Mock stream
        streamRef.current.stop()
      } else {
        // EventSource
        streamRef.current.close()
      }
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
