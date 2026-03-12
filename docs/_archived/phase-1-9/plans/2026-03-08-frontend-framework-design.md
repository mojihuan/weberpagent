# 前端基础框架设计文档

> 创建日期：2026-03-08
> 阶段：Phase 2 - 前端基础框架搭建

## 1. 技术选型

| 项目 | 选择 | 理由 |
|------|------|------|
| 框架 | Vite + React 18 + TypeScript | 标准模板，开发体验好 |
| 样式 | Tailwind CSS v4 | 配置简洁，与设计稿风格一致 |
| 状态管理 | React Query + useState | 适合 API 驱动的 CRUD 场景 |
| HTTP 客户端 | 原生 fetch | 无额外依赖，React Query 已封装 |
| 路由 | React Router v6 | 标准方案 |

## 2. 项目结构

```
frontend/
├── index.html
├── package.json
├── vite.config.ts
├── src/
│   ├── main.tsx              # 入口，挂载 React Query
│   ├── App.tsx               # 路由配置
│   ├── index.css             # Tailwind v4 导入
│   ├── api/
│   │   └── client.ts         # fetch 封装 + API 函数
│   ├── components/
│   │   ├── Layout.tsx        # 布局容器
│   │   ├── Sidebar.tsx       # 侧边栏
│   │   ├── NavItem.tsx       # 导航项
│   │   └── Button.tsx        # 按钮组件
│   ├── pages/
│   │   ├── Dashboard.tsx     # 首页（占位）
│   │   ├── Tasks.tsx         # 任务列表（占位）
│   │   ├── TaskDetail.tsx    # 任务详情（占位）
│   │   ├── RunMonitor.tsx    # 执行监控（占位）
│   │   └── Reports.tsx       # 报告查看（占位）
│   └── types/
│       └── index.ts          # TypeScript 类型定义
```

## 3. 页面路由

| 路径 | 页面 | 说明 |
|------|------|------|
| `/` | Dashboard | 首页仪表盘 |
| `/tasks` | Tasks | 任务列表 |
| `/tasks/:id` | TaskDetail | 任务详情 |
| `/runs/:id` | RunMonitor | 执行监控 |
| `/reports` | Reports | 报告列表 |

## 4. 核心组件设计

### 4.1 Layout 组件

```tsx
// 布局结构
<div className="flex min-h-screen">
  <Sidebar />
  <main className="flex-1 bg-white">
    {children}
  </main>
</div>
```

### 4.2 Sidebar 组件

```tsx
// 侧边栏结构
<aside className="w-60 bg-gray-50 p-4">
  <Logo />
  <nav className="mt-4 space-y-1">
    <NavItem icon="layout-dashboard" label="仪表盘" to="/" />
    <NavItem icon="list-todo" label="任务管理" to="/tasks" />
    <NavItem icon="play" label="执行监控" to="/runs" />
    <NavItem icon="file-text" label="报告查看" to="/reports" />
  </nav>
</aside>
```

### 4.3 NavItem 组件

```tsx
interface NavItemProps {
  icon: string      // Lucide 图标名
  label: string     // 显示文字
  to: string        // 路由路径
  active?: boolean  // 是否选中
}
```

### 4.4 Button 组件

```tsx
interface ButtonProps {
  variant: 'primary' | 'secondary'
  children: React.ReactNode
  onClick?: () => void
}

// primary: 蓝色背景，白色文字
// secondary: 灰色背景，深色文字
```

## 5. 类型定义

```typescript
// Task 任务
interface Task {
  id: string
  name: string
  description: string
  target_url: string
  max_steps: number
  status: 'draft' | 'ready'
}

// Run 执行记录
interface Run {
  id: string
  task_id: string
  status: 'running' | 'success' | 'failed' | 'stopped'
  started_at: string
  finished_at?: string
  steps: Step[]
}

// Step 单步执行
interface Step {
  index: number
  action: string
  reasoning?: string
  screenshot: string
  status: 'success' | 'failed'
  error?: string
  duration_ms: number
}
```

## 6. API 客户端设计

```typescript
// src/api/client.ts
const API_BASE = 'http://localhost:8000/api'

async function apiClient<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  })

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`)
  }

  return response.json()
}

// API 函数（Phase 3 实现）
export const taskApi = {
  list: () => apiClient<Task[]>('/tasks'),
  get: (id: string) => apiClient<Task>(`/tasks/${id}`),
  create: (data: CreateTaskDto) => apiClient<Task>('/tasks', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: string, data: UpdateTaskDto) => apiClient<Task>(`/tasks/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: string) => apiClient<void>(`/tasks/${id}`, { method: 'DELETE' }),
}
```

## 7. Phase 2 实施步骤

1. **初始化项目** - `npm create vite@latest frontend -- --template react-ts`
2. **安装依赖** - Tailwind v4、React Router、React Query
3. **配置 Tailwind v4** - 使用 `@import "tailwindcss"` 语法
4. **实现布局组件** - Layout + Sidebar + NavItem + Button
5. **配置路由** - 5 个页面占位组件
6. **类型定义** - Task、Run、Step 接口

## 8. 设计决策记录

| 决策项 | 选择 | 理由 |
|--------|------|------|
| CSS 方案 | Tailwind v4 | 配置简洁，新项目推荐 |
| 状态管理 | React Query | 适合 API 驱动场景，自动缓存 |
| HTTP 客户端 | 原生 fetch | 无额外依赖，够用 |
| 图标 | Lucide React | 与设计稿图标一致 |
