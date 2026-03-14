// frontend/src/api/runs.ts
import { apiClient } from './client'
import type { Run } from '../types'

// 创建执行记录
export async function createRun(taskId: string): Promise<Run> {
  return apiClient<Run>(`/runs?task_id=${taskId}`, {
    method: 'POST',
  })
}

// 获取执行详情
export async function getRun(runId: string): Promise<Run> {
  return apiClient<Run>(`/runs/${runId}`)
}

// 获取执行列表
export async function listRuns(taskId?: string): Promise<Run[]> {
  const url = taskId ? `/runs?task_id=${taskId}` : '/runs'
  return apiClient<Run[]>(url)
}

// 停止执行
export async function stopRun(runId: string): Promise<{ status: string }> {
  return apiClient<{ status: string }>(`/runs/${runId}/stop`, {
    method: 'POST',
  })
}

// 获取截图 URL
export function getScreenshotUrl(runId: string, stepIndex: number): string {
  const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080/api'
  return `${API_BASE}/runs/${runId}/screenshots/${stepIndex}`
}

// Mock: 启动执行 (保留向后兼容)
export async function startRun(_taskId: string): Promise<{ runId: string }> {
  const run = await createRun(_taskId)
  return { runId: run.id }
}
