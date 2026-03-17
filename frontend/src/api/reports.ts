// frontend/src/api/reports.ts
import { apiClient } from './client'
import type { Report, Step, AssertionResult } from '../types'

interface StepApiResponse {
  id: string
  run_id: string
  step_index: number
  action: string
  reasoning: string
  screenshot_url: string | null
  status: string
  error: string | null
  duration_ms: number
  created_at: string
}

interface ReportApiResponse {
  id: string
  run_id: string
  task_id: string
  task_name: string
  status: string
  total_steps: number
  success_steps: number
  failed_steps: number
  duration_ms: number
  created_at: string
}

interface AssertionResultApiResponse {
  id: string
  run_id: string
  assertion_id: string
  status: string
  message: string | null
  actual_value: string | null
  created_at: string
}

interface ReportDetailApiResponse extends ReportApiResponse {
  steps: StepApiResponse[]
  assertion_results: AssertionResultApiResponse[]
  ui_assertion_results?: AssertionResultApiResponse[]
  api_assertion_results?: AssertionResultApiResponse[]
  pass_rate?: string
  api_pass_rate?: string
}

interface ReportsListApiResponse {
  reports: ReportApiResponse[]
  total: number
  page: number
  page_size: number
}

export interface ReportsListParams {
  status?: string
  date?: string
  page?: number
  page_size?: number
}

// 转换 API 响应为前端类型
function transformReport(report: ReportApiResponse): Report {
  return {
    ...report,
    status: report.status as 'success' | 'failed',
  }
}

const API_BASE_FOR_IMAGES = import.meta.env.VITE_API_BASE?.replace('/api', '') || 'http://localhost:8080'

function transformStep(step: StepApiResponse): Step {
  // Build complete screenshot URL
  // Backend returns: /api/runs/{run_id}/screenshots/{step}
  // We need: http://localhost:8080/api/runs/{run_id}/screenshots/{step}
  let screenshotUrl = step.screenshot_url || ''
  if (screenshotUrl && !screenshotUrl.startsWith('http')) {
    // If it's a relative URL starting with /api, use API_BASE_FOR_IMAGES
    if (screenshotUrl.startsWith('/api/')) {
      screenshotUrl = `${API_BASE_FOR_IMAGES}${screenshotUrl}`
    } else {
      // Otherwise prepend the full API base
      screenshotUrl = `${API_BASE_FOR_IMAGES}/api${screenshotUrl}`
    }
  }

  return {
    index: step.step_index,
    action: step.action,
    reasoning: step.reasoning,
    screenshot: screenshotUrl,
    status: step.status as 'success' | 'failed',
    error: step.error || undefined,
    duration_ms: step.duration_ms,
  }
}

function transformAssertionResult(result: AssertionResultApiResponse): AssertionResult {
  return {
    id: result.id,
    run_id: result.run_id,
    assertion_id: result.assertion_id,
    status: result.status as 'pass' | 'fail',
    message: result.message,
    actual_value: result.actual_value,
    created_at: result.created_at,
  }
}

export interface ReportDetailResponse extends Report {
  steps: Step[]
  assertion_results?: AssertionResult[]
  ui_assertion_results?: AssertionResult[]
  api_assertion_results?: AssertionResult[]
  pass_rate?: string
  api_pass_rate?: string
}

export async function listReports(params?: ReportsListParams): Promise<{ reports: Report[]; total: number; page: number; page_size: number }> {
  const searchParams = new URLSearchParams()
  if (params?.status) searchParams.set('status', params.status)
  if (params?.date) searchParams.set('date', params.date)
  if (params?.page) searchParams.set('page', params.page.toString())
  if (params?.page_size) searchParams.set('page_size', params.page_size.toString())

  const query = searchParams.toString()
  const response = await apiClient<ReportsListApiResponse>(`/reports${query ? `?${query}` : ''}`)

  return {
    reports: response.reports.map(transformReport),
    total: response.total,
    page: response.page,
    page_size: response.page_size,
  }
}

export async function getReport(reportId: string): Promise<ReportDetailResponse> {
  const response = await apiClient<ReportDetailApiResponse>(`/reports/${reportId}`)

  return {
    ...transformReport(response),
    steps: response.steps.map(transformStep),
    assertion_results: (response.assertion_results || []).map(transformAssertionResult),
    ui_assertion_results: (response.ui_assertion_results || []).map(transformAssertionResult),
    api_assertion_results: (response.api_assertion_results || []).map(transformAssertionResult),
    pass_rate: response.pass_rate,
    api_pass_rate: response.api_pass_rate,
  }
}
