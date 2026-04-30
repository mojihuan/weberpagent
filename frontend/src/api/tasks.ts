import type { Task, CreateTaskDto, UpdateTaskDto, Run } from '../types'
import { apiClient } from './client'

// === Import types ===

export interface ImportPreviewRow {
  row_number: number
  data: Record<string, unknown>
  errors: string[]
  valid: boolean
}

export interface ImportPreviewResponse {
  rows: ImportPreviewRow[]
  total_rows: number
  valid_count: number
  error_count: number
  has_errors: boolean
}

export interface ImportConfirmResponse {
  status: string
  created_count: number
}

// Use raw fetch for FormData upload -- bypass apiClient which sets Content-Type: application/json
const IMPORT_API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:11002/api'

export async function importPreview(file: File): Promise<ImportPreviewResponse> {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`${IMPORT_API_BASE}/tasks/import/preview`, {
    method: 'POST',
    body: formData,
    // Do NOT set Content-Type -- browser auto-sets multipart/form-data with boundary
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '上传失败' }))
    throw new Error(error.detail || `上传失败: ${response.status}`)
  }
  return response.json()
}

export async function importConfirm(file: File): Promise<ImportConfirmResponse> {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`${IMPORT_API_BASE}/tasks/import/confirm`, {
    method: 'POST',
    body: formData,
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '导入失败' }))
    throw new Error(error.detail || `导入失败: ${response.status}`)
  }
  return response.json()
}

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
