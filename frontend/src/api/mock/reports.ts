import type { Report, Run, Step } from '../../types'
import { mockRuns } from './runs'

/**
 * 基于 mockRuns 生成报告列表
 */
function generateReportsFromRuns(): Report[] {
  return mockRuns.map(run => ({
    id: `report-${run.id}`,
    run_id: run.id,
    task_name: getTaskName(run.task_id),
    status: run.status === 'running' ? 'success' : (run.status as 'success' | 'failed'),
    total_steps: run.steps.length,
    success_steps: run.steps.filter(s => s.status === 'success').length,
    failed_steps: run.steps.filter(s => s.status === 'failed').length,
    duration_ms: calculateDuration(run),
    created_at: run.finished_at || run.started_at,
  }))
}

/**
 * 生成额外的模拟报告数据（21条）
 */
function generateMoreReports(): Report[] {
  const taskNames = [
    '用户登录验证',
    '商品搜索测试',
    '表单提交验证',
    '购物流程测试',
    '用户注册流程',
    '订单查询测试',
    '支付流程验证',
    '数据导出测试',
  ]

  const reports: Report[] = []

  // 生成过去30天的报告
  const now = new Date('2026-03-09T12:00:00Z')

  for (let i = 0; i < 21; i++) {
    const daysAgo = Math.floor(Math.random() * 30) + 1
    const createdDate = new Date(now)
    createdDate.setDate(createdDate.getDate() - daysAgo)
    createdDate.setHours(Math.floor(Math.random() * 10) + 8)
    createdDate.setMinutes(Math.floor(Math.random() * 60))

    const totalSteps = Math.floor(Math.random() * 15) + 5
    const isSuccess = Math.random() > 0.25 // 75% 成功率
    const failedSteps = isSuccess ? 0 : Math.floor(Math.random() * 3) + 1
    const successSteps = isSuccess ? totalSteps : totalSteps - failedSteps
    const durationMs = (totalSteps * (Math.floor(Math.random() * 3000) + 2000))

    reports.push({
      id: `report-extra-${i + 1}`,
      run_id: `run-extra-${i + 1}`,
      task_name: taskNames[Math.floor(Math.random() * taskNames.length)],
      status: isSuccess ? 'success' : 'failed',
      total_steps: totalSteps,
      success_steps: successSteps,
      failed_steps: failedSteps,
      duration_ms: durationMs,
      created_at: createdDate.toISOString(),
    })
  }

  return reports
}

/**
 * 获取任务名称
 */
function getTaskName(taskId: string): string {
  const taskNames: Record<string, string> = {
    '1': '用户登录验证',
    '2': '商品搜索测试',
    '3': '表单提交验证',
    '4': '购物流程测试',
  }
  return taskNames[taskId] || `任务 ${taskId}`
}

/**
 * 计算执行时长
 */
function calculateDuration(run: Run): number {
  if (!run.finished_at) return 0
  const start = new Date(run.started_at).getTime()
  const end = new Date(run.finished_at).getTime()
  return end - start
}

/**
 * 合并报告数据
 */
export const mockReports: Report[] = [
  ...generateReportsFromRuns(),
  ...generateMoreReports(),
].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())

/**
 * 获取报告列表（支持筛选和分页）
 */
export interface GetReportsParams {
  status?: 'success' | 'failed' | 'all'
  date?: 'today' | '7days' | '30days'
  page?: number
  pageSize?: number
}

export function getReports(params: GetReportsParams = {}): {
  reports: Report[]
  total: number
  page: number
  pageSize: number
} {
  const {
    status = 'all',
    date,
    page = 1,
    pageSize = 10,
  } = params

  let filtered = [...mockReports]

  // 状态筛选
  if (status !== 'all') {
    filtered = filtered.filter(r => r.status === status)
  }

  // 日期筛选
  if (date) {
    const now = new Date('2026-03-09T23:59:59Z')
    let startDate: Date

    switch (date) {
      case 'today':
        startDate = new Date('2026-03-09T00:00:00Z')
        break
      case '7days':
        startDate = new Date(now)
        startDate.setDate(startDate.getDate() - 7)
        break
      case '30days':
        startDate = new Date(now)
        startDate.setDate(startDate.getDate() - 30)
        break
    }

    filtered = filtered.filter(r => {
      const reportDate = new Date(r.created_at)
      return reportDate >= startDate! && reportDate <= now
    })
  }

  // 分页
  const total = filtered.length
  const start = (page - 1) * pageSize
  const end = start + pageSize
  const paginated = filtered.slice(start, end)

  return {
    reports: paginated,
    total,
    page,
    pageSize,
  }
}

/**
 * 为没有对应 Run 的报告生成模拟 Run 数据
 */
function generateMockRun(report: Report): Run {
  const steps: Step[] = Array.from({ length: report.total_steps }, (_, i) => ({
    index: i + 1,
    action: `执行操作 ${i + 1}`,
    reasoning: `AI 分析：当前步骤 ${i + 1}，准备执行操作`,
    screenshot: `/screenshots/step-${i + 1}.png`,
    status: i < report.success_steps ? 'success' : 'failed',
    error: i >= report.success_steps ? '操作执行失败' : undefined,
    duration_ms: Math.floor(Math.random() * 3000) + 500,
  }))

  const startDate = new Date(report.created_at)
  const endDate = new Date(startDate.getTime() + report.duration_ms)

  return {
    id: report.run_id,
    task_id: 'unknown',
    status: report.status,
    started_at: startDate.toISOString(),
    finished_at: endDate.toISOString(),
    steps,
  }
}

/**
 * 获取报告详情（包含对应的 Run 数据）
 */
export function getReportDetail(reportId: string): {
  report: Report | null
  run: Run | null
} {
  const report = mockReports.find(r => r.id === reportId)

  if (!report) {
    return { report: null, run: null }
  }

  // 查找对应的 Run
  let run = mockRuns.find(r => r.id === report.run_id)

  // 如果没有找到对应的 Run，生成一个模拟的
  if (!run) {
    run = generateMockRun(report)
  }

  return { report, run }
}
