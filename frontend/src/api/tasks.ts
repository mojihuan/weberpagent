import type { Task, CreateTaskDto, UpdateTaskDto, Run } from '../types'
import { apiClient } from './client'
import { ENABLE_MOCK, delay } from './mock/index'
import { mockTasks, generateTaskId } from './mock/tasks'
import { mockRuns, getTaskStats } from './mock/runs'

const USE_MOCK = ENABLE_MOCK

export const tasksApi = {
  async list(params?: { status?: string; search?: string }): Promise<Task[]> {
    if (USE_MOCK) {
      await delay(200)
      let result = [...mockTasks]

      if (params?.status && params.status !== 'all') {
        result = result.filter(t => t.status === params.status)
      }

      if (params?.search) {
        const search = params.search.toLowerCase()
        result = result.filter(t =>
          t.name.toLowerCase().includes(search) ||
          t.description.toLowerCase().includes(search)
        )
      }

      return result
    }
    return apiClient<Task[]>('/tasks')
  },

  async get(id: string): Promise<Task | null> {
    if (USE_MOCK) {
      await delay(100)
      return mockTasks.find(t => t.id === id) || null
    }
    return apiClient<Task>(`/tasks/${id}`)
  },

  async create(data: CreateTaskDto): Promise<Task> {
    if (USE_MOCK) {
      await delay(300)
      const now = new Date().toISOString()
      const task: Task = {
        id: generateTaskId(),
        ...data,
        status: 'draft',
        created_at: now,
        updated_at: now,
      }
      mockTasks.unshift(task)
      return task
    }
    return apiClient<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  async update(id: string, data: UpdateTaskDto): Promise<Task> {
    if (USE_MOCK) {
      await delay(200)
      const index = mockTasks.findIndex(t => t.id === id)
      if (index === -1) throw new Error('Task not found')

      mockTasks[index] = {
        ...mockTasks[index],
        ...data,
        updated_at: new Date().toISOString(),
      }
      return mockTasks[index]
    }
    return apiClient<Task>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  },

  async delete(id: string): Promise<void> {
    if (USE_MOCK) {
      await delay(200)
      const index = mockTasks.findIndex(t => t.id === id)
      if (index !== -1) {
        mockTasks.splice(index, 1)
      }
      return
    }
    return apiClient<void>(`/tasks/${id}`, { method: 'DELETE' })
  },

  async batchDelete(ids: string[]): Promise<void> {
    if (USE_MOCK) {
      await delay(300)
      ids.forEach(id => {
        const index = mockTasks.findIndex(t => t.id === id)
        if (index !== -1) mockTasks.splice(index, 1)
      })
      return
    }
    await Promise.all(ids.map(id => apiClient<void>(`/tasks/${id}`, { method: 'DELETE' })))
  },

  async batchUpdateStatus(ids: string[], status: 'draft' | 'ready'): Promise<void> {
    if (USE_MOCK) {
      await delay(300)
      const now = new Date().toISOString()
      ids.forEach(id => {
        const task = mockTasks.find(t => t.id === id)
        if (task) {
          task.status = status
          task.updated_at = now
        }
      })
      return
    }
    await Promise.all(ids.map(id =>
      apiClient<void>(`/tasks/${id}`, {
        method: 'PUT',
        body: JSON.stringify({ status }),
      })
    ))
  },

  async getRuns(taskId: string): Promise<Run[]> {
    if (USE_MOCK) {
      await delay(150)
      return mockRuns.filter(r => r.task_id === taskId)
    }
    return apiClient<Run[]>(`/tasks/${taskId}/runs`)
  },

  async getStats(taskId: string) {
    if (USE_MOCK) {
      await delay(100)
      return getTaskStats(taskId)
    }
    return apiClient<{ date: string; runs: number; successRate: number }[]>(`/tasks/${taskId}/stats`)
  },
}
