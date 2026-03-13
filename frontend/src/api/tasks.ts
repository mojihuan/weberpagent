import type { Task, CreateTaskDto, UpdateTaskDto, Run } from '../types'
import { apiClient } from './client'

export const tasksApi = {
  async list(params?: { status?: string; search?: string }): Promise<Task[]> {
    const searchParams = new URLSearchParams()
    if (params?.status && params.status !== 'all') {
      searchParams.set('status', params.status)
    }
    if (params?.search) {
      searchParams.set('search', params.search)
    }
    const query = searchParams.toString()
    return apiClient<Task[]>(`/tasks${query ? `?${query}` : ''}`)
  },

  async get(id: string): Promise<Task | null> {
    return apiClient<Task>(`/tasks/${id}`)
  },

  async create(data: CreateTaskDto): Promise<Task> {
    return apiClient<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  async update(id: string, data: UpdateTaskDto): Promise<Task> {
    return apiClient<Task>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  },

  async delete(id: string): Promise<void> {
    return apiClient<void>(`/tasks/${id}`, { method: 'DELETE' })
  },

  async batchDelete(ids: string[]): Promise<void> {
    await Promise.all(ids.map(id => apiClient<void>(`/tasks/${id}`, { method: 'DELETE' })))
  },

  async batchUpdateStatus(ids: string[], status: 'draft' | 'ready'): Promise<void> {
    await Promise.all(ids.map(id =>
      apiClient<void>(`/tasks/${id}`, {
        method: 'PUT',
        body: JSON.stringify({ status }),
      })
    ))
  },

  async getRuns(taskId: string): Promise<Run[]> {
    return apiClient<Run[]>(`/tasks/${taskId}/runs`)
  },

  async getStats(taskId: string) {
    return apiClient<{ date: string; runs: number; successRate: number }[]>(`/tasks/${taskId}/stats`)
  },
}
