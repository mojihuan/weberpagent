// Task 任务
export interface Task {
  id: string
  name: string
  description: string
  target_url: string
  max_steps: number
  preconditions?: string[]
  assertions?: AssertionConfig[]
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
  assertions?: AssertionConfig[]
}

// UpdateTaskDto 更新任务请求
export interface UpdateTaskDto {
  name?: string
  description?: string
  target_url?: string
  max_steps?: number
  status?: 'draft' | 'ready'
  preconditions?: string[]
  assertions?: AssertionConfig[]
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
  timeline: TimelineItem[]
  assertion_summary?: {
    total: number
    passed: number
    failed: number
    errors: number
  }
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

// SSEPreconditionEvent SSE 前置条件事件
export interface SSEPreconditionEvent {
  index: number
  code: string
  status: 'running' | 'success' | 'failed'
  error?: string
  duration_ms?: number
  variables?: Record<string, any>
}

// SSEAssertionEvent SSE 断言评估事件
export interface SSEAssertionEvent {
  assertion_id: string
  assertion_name: string
  assertion_type: string
  status: 'pass' | 'fail'
  message?: string
  actual_value?: string
  field_results?: Array<{
    name: string
    field_name?: string  // alias
    expected?: string
    actual?: string
    passed: boolean
    message?: string
    description?: string
    comparison_type?: string
  }>
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
  step_stats?: {
    action_count: number
    stagnation: number
    duration_ms: number
    element_count: number
  }
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
  step_stats?: {
    action_count: number
    stagnation: number
    duration_ms: number
    element_count: number
  }
}

// TimelineItem types for unified execution timeline
export interface TimelineItemStep {
  type: 'step'
  data: Step
}

export interface TimelineItemPrecondition {
  type: 'precondition'
  data: SSEPreconditionEvent
}

export interface TimelineItemAssertion {
  type: 'assertion'
  data: SSEAssertionEvent
}

export type TimelineItem =
  | TimelineItemStep
  | TimelineItemPrecondition
  | TimelineItemAssertion

// Report TimelineItem types for report detail page
export interface ReportTimelineStep {
  type: 'step'
  id: string
  sequence_number: number
  step_index: number
  action: string
  reasoning: string | null
  screenshot_url: string | null
  status: string
  error: string | null
  duration_ms: number | null
}

export interface ReportTimelinePrecondition {
  type: 'precondition'
  id: string
  sequence_number: number
  index: number
  code: string
  status: string
  error: string | null
  duration_ms: number | null
  variables: Record<string, unknown> | null
}

export interface ReportTimelineAssertionFieldResult {
  field_name: string
  expected: unknown
  actual: unknown
  passed: boolean
  message: string
  assertion_type: string
}

export interface ReportTimelineAssertion {
  type: 'assertion'
  id: string
  sequence_number: number
  assertion_id: string
  assertion_name: string | null
  status: string
  message: string | null
  actual_value: string | null
  field_results: ReportTimelineAssertionFieldResult[] | null
  duration_ms: number | null
}

export type ReportTimelineItem =
  | ReportTimelineStep
  | ReportTimelinePrecondition
  | ReportTimelineAssertion

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
  pass_rate?: string
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
  description?: string
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

// External Assertions - Business assertions from webseleniumerp base_assertions.py

export interface AssertionParameterOption {
  value: number
  label: string
}

export interface AssertionParameterInfo {
  name: string
  description: string
  options: AssertionParameterOption[]
}

export interface DataOption {
  value: string
  label: string
}

export interface HeadersOption {
  value: string
  label: string
}

export interface AssertionMethodInfo {
  name: string
  description: string
  data_options: DataOption[]
  parameters: AssertionParameterInfo[]
}

export interface AssertionClassGroup {
  name: string
  methods: AssertionMethodInfo[]
}

export interface AssertionMethodsResponse {
  available: boolean
  headers_options: HeadersOption[]
  classes: AssertionClassGroup[]
  total: number
  error?: string
}

// AssertionConfig - structured configuration for business assertions
// Per CONTEXT.md decision: stored as structured JSON, NOT Python code
export interface AssertionConfig {
  className: string      // e.g., "PcAssert"
  methodName: string     // e.g., "attachment_inventory_list_assert"
  headers: string        // e.g., "main" - identifier resolved at execution time
  data: string           // e.g., "main" - from method's data_options
  params: Record<string, number | string>  // i, j, k etc. filter parameters
  field_params?: Record<string, string>    // field validation parameters e.g., { saleTime: 'now', salesOrder: 'SA' }
}

// Assertion field types for field_params configuration

export interface AssertionFieldInfo {
  name: string
  path: string
  is_time_field: boolean
  description: string
}

export interface AssertionFieldGroup {
  name: string
  fields: AssertionFieldInfo[]
}

export interface AssertionFieldsResponse {
  available: boolean
  error?: string
  groups: AssertionFieldGroup[]
  total: number
}

// Batch 批量执行
export interface Batch {
  id: string
  concurrency: number
  status: 'pending' | 'running' | 'completed'
  created_at: string
  finished_at: string | null
}

export interface BatchCreateResponse {
  id: string
  concurrency: number
  status: string
  created_at: string
}

export interface BatchRunSummary {
  id: string
  task_id: string
  task_name: string | null
  status: string
  started_at: string | null
  finished_at: string | null
}
