import { useQuery } from '@tanstack/react-query'
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
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['batch', batchId],
    queryFn: () => batchesApi.getStatus(batchId),
    refetchInterval: (query) => {
      const status = query.state.data?.status
      return status === 'completed' ? false : 2000
    },
    enabled: !!batchId,
  })

  return {
    batch: data ?? null,
    runs: data?.runs ?? [],
    loading: isLoading,
    error: error ? (error instanceof Error ? error.message : String(error)) : null,
    refetch,
  }
}
