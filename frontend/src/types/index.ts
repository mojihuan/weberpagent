// Task 任务
export interface Task {
  id: string
  name: string
  description: string
  target_url: string
  max_steps: number
  status: 'draft' | 'ready'
  created_at: string
  updated_at: string
}

// CreateTaskDto 创建任务请求
export interface CreateTaskDto {
  name: string
  description: string
  target_url: string
  max_steps: number
}

// UpdateTaskDto 更新任务请求
export interface UpdateTaskDto {
  name?: string
  description?: string
  target_url?: string
  max_steps?: number
  status?: 'draft' | 'ready'
}

// Run 执行记录
export interface Run {
  id: string
  task_id: string
  status: 'running' | 'success' | 'failed' | 'stopped'
  started_at: string
  finished_at?: string
  steps: Step[]
}

// Step 单步执行
export interface Step {
  index: number
  action: string
  reasoning?: string
  screenshot: string
  status: 'success' | 'failed'
  error?: string
  duration_ms: number
}

// Report 报告
export interface Report {
  id: string
  run_id: string
  task_name: string
  status: 'success' | 'failed'
  total_steps: number
  success_steps: number
  failed_steps: number
  duration_ms: number
  created_at: string
}

// Dashboard 统计数据
export interface DashboardStats {
  totalTasks: number
  totalRuns: number
  successRate: number
  todayRuns: number
}

// 7 天趋势数据点
export interface TrendDataPoint {
  date: string
  runs: number
  successRate: number
}

// 最近执行记录
export interface RecentRun {
  id: string
  task_name: string
  status: 'success' | 'failed' | 'running'
  started_at: string
  duration_ms: number
}
