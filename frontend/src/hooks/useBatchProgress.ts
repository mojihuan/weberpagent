import { useState, useEffect, useRef, useCallback } from 'react'
import { batchesApi } from '../api/batches'
import type { Batch, BatchRunSummary } from '../types'

interface BatchProgressState {
  batch: Batch | null
  runs: BatchRunSummary[]
  loading: boolean
  error: string | null
  refetch: () => void
}

export function useBatchProgress(batchId: string): BatchProgressState {
  const [batch, setBatch] = useState<Batch | null>(null)
  const [runs, setRuns] = useState<BatchRunSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const completedRef = useRef(false)
  const [refetchCounter, setRefetchCounter] = useState(0)

  const refetch = useCallback(() => {
    setRefetchCounter(prev => prev + 1)
  }, [])

  useEffect(() => {
    let intervalId: ReturnType<typeof setInterval> | null = null

    const fetchData = async () => {
      try {
        const data = await batchesApi.getStatus(batchId)
        setBatch(data)
        setRuns(data.runs ?? [])
        setError(null)

        if (loading) {
          setLoading(false)
        }

        if (data.status === 'completed' && !completedRef.current) {
          completedRef.current = true
          if (intervalId) {
            clearInterval(intervalId)
            intervalId = null
          }
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : '加载批次进度失败'
        setError(message)
        if (loading) {
          setLoading(false)
        }
      }
    }

    fetchData()
    if (!completedRef.current) {
      intervalId = setInterval(fetchData, 2000)
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId)
      }
    }
  }, [batchId, refetchCounter]) // eslint-disable-line react-hooks/exhaustive-deps

  return { batch, runs, loading, error, refetch }
}
