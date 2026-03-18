// Task 任务
export interface Task {
  id: string
  name: string
  description: string
  target_url: string
  max_steps: number
  preconditions?: string[]
  api_assertions?: string[]
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
  preconditions?: string[]
  api_assertions?: string[]
}

// UpdateTaskDto 更新任务请求
export interface UpdateTaskDto {
  name?: string
  description?: string
  target_url?: string
  max_steps?: number
  status?: 'draft' | 'ready'
  preconditions?: string[]
  api_assertions?: string[]
}

// RunStatus 执行状态
export type RunStatus = 'pending' | 'running' | 'success' | 'failed'

// Run 执行记录
export interface Run {
  id: string
  task_id: string
  status: RunStatus
  started_at: string
  finished_at?: string
  steps: Step[]
  preconditions?: SSEPreconditionEvent[]
  api_assertions?: SSEApiAssertionEvent[]
}

// Assertion 断言定义
export interface Assertion {
  id: string
  task_id: string
  name: string
  type: 'url_contains' | 'text_exists' | 'no_errors'
  expected: string
  created_at: string
}

// AssertionResult 断言执行结果
export interface AssertionResult {
  id: string
  run_id: string
  assertion_id: string
  assertion_name?: string
  status: 'pass' | 'fail'
  message: string | null
  actual_value: string | null
  created_at: string
}

// ApiAssertionFieldResult 接口断言字段结果
export interface ApiAssertionFieldResult {
  field_name: string
  expected: any
  actual: any
  passed: boolean
  message: string
  assertion_type: string
}

// SSEApiAssertionEvent SSE 接口断言事件
export interface SSEApiAssertionEvent {
  index: number
  code: string
  status: 'running' | 'success' | 'failed'
  error?: string
  duration_ms: number
  field_results?: ApiAssertionFieldResult[]
}

// SSEPreconditionEvent SSE 前置条件事件
export interface SSEPreconditionEvent {
  index: number
  code: string
  status: 'running' | 'success' | 'failed'
  error?: string
  duration_ms?: number
  variables?: Record<string, any>
}

// SSE Event Types
export interface SSEStartedEvent {
  run_id: string
  task_name: string
}

export interface SSEStepEvent {
  index: number
  action: string
  reasoning: string | null
  screenshot_url: string | null
  status: string
  duration_ms: number | null
}

export interface SSEFinishedEvent {
  status: string
  total_steps: number
  duration_ms: number
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

// ReportDetailResponse 报告详情（包含步骤和断言结果）
export interface ReportDetailResponse extends Report {
  steps: Step[]
  assertion_results?: AssertionResult[]
  ui_assertion_results?: AssertionResult[]
  api_assertion_results?: AssertionResult[]
  pass_rate?: string
  api_pass_rate?: string
}

// External Operations - External precondition operations from webseleniumerp
export interface OperationItem {
  code: string
  description: string
}

export interface ModuleGroup {
  name: string
  operations: OperationItem[]
}

export interface OperationsResponse {
  available: boolean
  modules: ModuleGroup[]
  total: number
  error?: string
}

export interface GenerateRequest {
  operation_codes: string[]
}

export interface GenerateResponse {
  code: string
}

// External Data Methods - Data query methods from webseleniumerp

export interface DataMethodParameter {
  name: string
  type: string
  required: boolean
  default: string | null
}

export interface DataMethodInfo {
  name: string
  description: string
  parameters: DataMethodParameter[]
}

export interface DataMethodClass {
  name: string
  methods: DataMethodInfo[]
}

export interface DataMethodsResponse {
  available: boolean
  classes: DataMethodClass[]
  total: number
  error?: string
}

export interface ExecuteDataMethodRequest {
  class_name: string
  method_name: string
  params: Record<string, any>
}

export interface ExecuteDataMethodResponse {
  success: boolean
  data?: Array<Record<string, any>>
  error?: string
  error_type?: string
}

// Data extraction configuration for frontend UI
export interface FieldExtraction {
  path: string           // e.g., "[0].imei"
  variableName: string   // e.g., "imei"
}

export interface DataMethodConfig {
  className: string
  methodName: string
  parameters: Record<string, any>
  extractions: FieldExtraction[]
}
