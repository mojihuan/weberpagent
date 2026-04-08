import { apiClient } from './client'
import type { Batch, BatchCreateResponse, BatchRunSummary } from '../types'

export const batchesApi = {
  async create(taskIds: string[], concurrency: number = 2): Promise<BatchCreateResponse> {
    return apiClient<BatchCreateResponse>('/batches', {
      method: 'POST',
      body: JSON.stringify({ task_ids: taskIds, concurrency }),
    })
  },

  async getStatus(batchId: string): Promise<Batch> {
    return apiClient<Batch>(`/batches/${batchId}`)
  },

  async getRuns(batchId: string): Promise<BatchRunSummary[]> {
    return apiClient<BatchRunSummary[]>(`/batches/${batchId}/runs`)
  },
}
