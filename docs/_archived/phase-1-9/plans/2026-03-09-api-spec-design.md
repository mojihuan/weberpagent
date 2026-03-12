# 后端 API 接口规范

> 基于前端页面逆向设计的 API 接口规范，供后端开发参考。

## 概述

- **Base URL**: `/api`
- **认证**: 无（POC 阶段）
- **数据格式**: JSON
- **日期格式**: ISO 8601（如 `2026-03-09T15:00:00Z`）

---

## 数据模型定义

### Task 任务

```typescript
interface Task {
  id: string
  name: string
  description: string
  target_url: string
  max_steps: number
  status: 'draft' | 'ready'
  created_at: string  // ISO 8601
  updated_at: string  // ISO 8601
}

interface CreateTaskDto {
  name: string
  description: string
  target_url: string
  max_steps: number
}

interface UpdateTaskDto {
  name?: string
  description?: string
  target_url?: string
  max_steps?: number
  status?: 'draft' | 'ready'
}
```

### Run 执行记录

```typescript
interface Run {
  id: string
  task_id: string
  status: 'running' | 'success' | 'failed' | 'stopped'
  started_at: string
  finished_at?: string
  steps: Step[]
}

interface Step {
  index: number
  action: string
  reasoning?: string
  screenshot: string  // 相对路径，如 /screenshots/step-1.png
  status: 'success' | 'failed'
  error?: string
  duration_ms: number
}
```

### Report 报告

```typescript
interface Report {
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
```

### Dashboard 仪表盘

```typescript
interface DashboardStats {
  totalTasks: number
  totalRuns: number
  successRate: number  // 0-100
  todayRuns: number
}

interface TrendDataPoint {
  date: string        // "MM-DD" 格式
  runs: number
  successRate: number // 0-100
}

interface RecentRun {
  id: string
  task_name: string
  status: 'success' | 'failed' | 'running'
  started_at: string
  duration_ms: number
}
```

### 通用响应格式

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: {
    code: string
    message: string
    details?: Record<string, unknown>
  }
}

interface PagedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}
```

---

## Tasks API

### 1. GET `/api/tasks` - 获取任务列表

**Query 参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | 否 | 筛选状态：`draft`、`ready`、`all`，默认 `all` |
| search | string | 否 | 搜索名称/描述 |

**响应：**

```json
{
  "success": true,
  "data": [
    {
      "id": "1",
      "name": "用户登录测试",
      "description": "使用测试账号登录系统",
      "target_url": "https://example.com/login",
      "max_steps": 10,
      "status": "ready",
      "created_at": "2026-03-08T10:00:00Z",
      "updated_at": "2026-03-08T14:30:00Z"
    }
  ]
}
```

---

### 2. POST `/api/tasks` - 创建任务

**请求体：**

```json
{
  "name": "用户登录测试",
  "description": "使用测试账号登录系统",
  "target_url": "https://example.com/login",
  "max_steps": 10
}
```

**响应：**

```json
{
  "success": true,
  "data": {
    "id": "100",
    "name": "用户登录测试",
    "description": "使用测试账号登录系统",
    "target_url": "https://example.com/login",
    "max_steps": 10,
    "status": "draft",
    "created_at": "2026-03-09T15:00:00Z",
    "updated_at": "2026-03-09T15:00:00Z"
  }
}
```

---

### 3. GET `/api/tasks/:id` - 获取任务详情

**响应：** 同上 Task 对象

---

### 4. PUT `/api/tasks/:id` - 更新任务

**请求体：** `UpdateTaskDto`（部分字段可选）

```json
{
  "name": "用户登录测试（修改版）",
  "status": "ready"
}
```

**响应：** 更新后的 Task 对象

---

### 5. DELETE `/api/tasks/:id` - 删除任务

**响应：**

```json
{
  "success": true
}
```

---

### 6. POST `/api/tasks/batch-delete` - 批量删除

**请求体：**

```json
{
  "ids": ["1", "2", "3"]
}
```

**响应：**

```json
{
  "success": true
}
```

---

### 7. PUT `/api/tasks/batch-status` - 批量更新状态

**请求体：**

```json
{
  "ids": ["1", "2"],
  "status": "ready"
}
```

**响应：**

```json
{
  "success": true
}
```

---

### 8. GET `/api/tasks/:id/runs` - 获取任务执行记录

**响应：**

```json
{
  "success": true,
  "data": [
    {
      "id": "r1",
      "task_id": "1",
      "status": "success",
      "started_at": "2026-03-08T14:30:00Z",
      "finished_at": "2026-03-08T14:30:45Z",
      "steps": []
    }
  ]
}
```

---

### 9. GET `/api/tasks/:id/stats` - 获取任务统计趋势

**Query 参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| days | number | 否 | 最近 N 天，默认 7 |

**响应：**

```json
{
  "success": true,
  "data": [
    { "date": "03/03", "runs": 3, "successRate": 67 },
    { "date": "03/04", "runs": 2, "successRate": 100 },
    { "date": "03/05", "runs": 4, "successRate": 75 }
  ]
}
```

---

## Runs API

### 1. POST `/api/runs` - 启动执行

**请求体：**

```json
{
  "task_id": "1"
}
```

**响应：**

```json
{
  "success": true,
  "data": {
    "run_id": "r_abc123",
    "status": "running"
  }
}
```

---

### 2. GET `/api/runs/:id` - 获取执行详情

**响应：**

```json
{
  "success": true,
  "data": {
    "id": "r1",
    "task_id": "1",
    "status": "success",
    "started_at": "2026-03-08T14:30:00Z",
    "finished_at": "2026-03-08T14:30:45Z",
    "steps": [
      {
        "index": 1,
        "action": "打开目标页面",
        "reasoning": "AI 分析：当前页面状态正常，准备执行下一步操作",
        "screenshot": "/screenshots/step-1.png",
        "status": "success",
        "duration_ms": 1500
      },
      {
        "index": 2,
        "action": "点击登录按钮",
        "reasoning": "检测到目标元素，正在进行交互",
        "screenshot": "/screenshots/step-2.png",
        "status": "failed",
        "error": "元素定位超时：未找到目标按钮",
        "duration_ms": 3000
      }
    ]
  }
}
```

---

### 3. POST `/api/runs/:id/stop` - 停止执行

**响应：**

```json
{
  "success": true,
  "data": {
    "run_id": "r1",
    "status": "stopped"
  }
}
```

---

### 4. GET `/api/runs/:id/stream` - SSE 实时流

**类型：** `text/event-stream`

**事件格式：**

```
event: started
data: {"run_id": "r1", "status": "running"}

event: step
data: {"run_id": "r1", "step": {"index": 1, "action": "打开目标页面", "reasoning": "...", "screenshot": "/screenshots/step-1.png", "status": "success", "duration_ms": 1500}}

event: finished
data: {"run_id": "r1", "status": "success"}

event: error
data: {"run_id": "r1", "error": "网络超时"}
```

**事件类型：**

| 事件 | 说明 | data 字段 |
|------|------|-----------|
| `started` | 执行开始 | `run_id`, `status` |
| `step` | 单步完成 | `run_id`, `step` |
| `finished` | 执行结束 | `run_id`, `status` |
| `error` | 发生错误 | `run_id`, `error` |

---

## Reports API

### 1. GET `/api/reports` - 获取报告列表

**Query 参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | 否 | 筛选状态：`success`、`failed`、`all`，默认 `all` |
| date | string | 否 | 时间范围：`today`、`7days`、`30days`，默认 all |
| page | number | 否 | 页码，默认 1 |
| pageSize | number | 否 | 每页条数，默认 10 |

**响应：**

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "report-r1",
        "run_id": "r1",
        "task_name": "用户登录测试",
        "status": "success",
        "total_steps": 8,
        "success_steps": 8,
        "failed_steps": 0,
        "duration_ms": 45000,
        "created_at": "2026-03-08T14:30:45Z"
      }
    ],
    "total": 28,
    "page": 1,
    "pageSize": 10
  }
}
```

---

### 2. GET `/api/reports/:id` - 获取报告详情

**响应：** 包含报告基本信息 + 对应的 Run 完整数据

```json
{
  "success": true,
  "data": {
    "report": {
      "id": "report-r1",
      "run_id": "r1",
      "task_name": "用户登录测试",
      "status": "success",
      "total_steps": 8,
      "success_steps": 8,
      "failed_steps": 0,
      "duration_ms": 45000,
      "created_at": "2026-03-08T14:30:45Z"
    },
    "run": {
      "id": "r1",
      "task_id": "1",
      "status": "success",
      "started_at": "2026-03-08T14:30:00Z",
      "finished_at": "2026-03-08T14:30:45Z",
      "steps": []
    }
  }
}
```

---

## Dashboard API

### 1. GET `/api/dashboard` - 获取仪表盘全部数据

**Query 参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| trendDays | number | 否 | 趋势天数，默认 7 |
| recentLimit | number | 否 | 最近执行条数，默认 5 |

**响应：**

```json
{
  "success": true,
  "data": {
    "stats": {
      "totalTasks": 12,
      "totalRuns": 156,
      "successRate": 87.5,
      "todayRuns": 8
    },
    "trend": [
      { "date": "03-03", "runs": 18, "successRate": 83 },
      { "date": "03-04", "runs": 22, "successRate": 86 },
      { "date": "03-05", "runs": 15, "successRate": 80 },
      { "date": "03-06", "runs": 28, "successRate": 92 },
      { "date": "03-07", "runs": 20, "successRate": 85 },
      { "date": "03-08", "runs": 25, "successRate": 88 },
      { "date": "03-09", "runs": 28, "successRate": 90 }
    ],
    "recentRuns": [
      {
        "id": "r_001",
        "task_name": "用户登录测试",
        "status": "success",
        "started_at": "2026-03-09T10:30:25Z",
        "duration_ms": 12500
      }
    ]
  }
}
```

---

### 2. GET `/api/dashboard/stats` - 获取统计卡片数据

**响应：**

```json
{
  "success": true,
  "data": {
    "totalTasks": 12,
    "totalRuns": 156,
    "successRate": 87.5,
    "todayRuns": 8
  }
}
```

---

### 3. GET `/api/dashboard/trend` - 获取趋势图数据

**Query 参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| days | number | 否 | 天数，默认 7 |

**响应：**

```json
{
  "success": true,
  "data": [
    { "date": "03-03", "runs": 18, "successRate": 83 },
    { "date": "03-04", "runs": 22, "successRate": 86 }
  ]
}
```

---

### 4. GET `/api/dashboard/recent-runs` - 获取最近执行记录

**Query 参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| limit | number | 否 | 条数，默认 5 |

**响应：**

```json
{
  "success": true,
  "data": [
    {
      "id": "r_001",
      "task_name": "用户登录测试",
      "status": "success",
      "started_at": "2026-03-09T10:30:25Z",
      "duration_ms": 12500
    }
  ]
}
```

---

## 错误码规范

### HTTP 状态码

| 状态码 | 说明 | 使用场景 |
|--------|------|----------|
| 200 | 成功 | 请求正常处理 |
| 400 | 请求参数错误 | 缺少必填字段、格式错误 |
| 404 | 资源不存在 | 任务/执行/报告不存在 |
| 500 | 服务器内部错误 | 未知异常 |

### 错误响应格式

```json
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "任务不存在",
    "details": {}
  }
}
```

### 业务错误码

| 错误码 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| **Tasks 相关** |||
| `TASK_NOT_FOUND` | 404 | 任务不存在 |
| `TASK_NAME_REQUIRED` | 400 | 任务名称不能为空 |
| `TASK_URL_INVALID` | 400 | 目标 URL 格式错误 |
| `TASK_HAS_RUNNING_RUN` | 400 | 任务正在执行中，无法删除 |
| **Runs 相关** |||
| `RUN_NOT_FOUND` | 404 | 执行记录不存在 |
| `RUN_ALREADY_RUNNING` | 400 | 该任务已有执行中的记录 |
| `RUN_NOT_RUNNING` | 400 | 执行已结束，无法停止 |
| `TASK_NOT_READY` | 400 | 任务状态为 draft，无法执行 |
| **Reports 相关** |||
| `REPORT_NOT_FOUND` | 404 | 报告不存在 |
| **通用错误** |||
| `INVALID_PARAMS` | 400 | 请求参数错误 |
| `INTERNAL_ERROR` | 500 | 服务器内部错误 |

---

## 截图存储说明

- `screenshot` 字段返回**相对路径**，如 `/screenshots/step-1.png`
- 前端需配置 `IMAGE_BASE_URL` 进行拼接
- 示例：`http://localhost:8000` + `/screenshots/step-1.png`

---

## 接口清单汇总

| 资源 | 方法 | 路径 | 说明 |
|------|------|------|------|
| Tasks | GET | `/api/tasks` | 获取任务列表 |
| Tasks | POST | `/api/tasks` | 创建任务 |
| Tasks | GET | `/api/tasks/:id` | 获取任务详情 |
| Tasks | PUT | `/api/tasks/:id` | 更新任务 |
| Tasks | DELETE | `/api/tasks/:id` | 删除任务 |
| Tasks | POST | `/api/tasks/batch-delete` | 批量删除 |
| Tasks | PUT | `/api/tasks/batch-status` | 批量更新状态 |
| Tasks | GET | `/api/tasks/:id/runs` | 获取任务执行记录 |
| Tasks | GET | `/api/tasks/:id/stats` | 获取任务统计趋势 |
| Runs | POST | `/api/runs` | 启动执行 |
| Runs | GET | `/api/runs/:id` | 获取执行详情 |
| Runs | POST | `/api/runs/:id/stop` | 停止执行 |
| Runs | GET | `/api/runs/:id/stream` | SSE 实时流 |
| Reports | GET | `/api/reports` | 获取报告列表 |
| Reports | GET | `/api/reports/:id` | 获取报告详情 |
| Dashboard | GET | `/api/dashboard` | 获取仪表盘全部数据 |
| Dashboard | GET | `/api/dashboard/stats` | 获取统计卡片 |
| Dashboard | GET | `/api/dashboard/trend` | 获取趋势图 |
| Dashboard | GET | `/api/dashboard/recent-runs` | 获取最近执行 |

**总计：19 个接口**
