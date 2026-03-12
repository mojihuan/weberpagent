# 前端基础框架实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 搭建 Vite + React + TypeScript 前端项目，实现基础布局和路由配置

**Architecture:** 使用 Vite 标准模板创建项目，Tailwind CSS v4 处理样式，React Router v6 管理路由，React Query 管理 API 状态。布局采用左侧固定侧边栏 + 右侧主内容区的经典 Dashboard 布局。

**Tech Stack:** Vite 5, React 18, TypeScript, Tailwind CSS v4, React Router v6, React Query, Lucide React

---

## Task 1: 初始化 Vite 项目

**Files:**
- Create: `frontend/` 目录及所有初始化文件

**Step 1: 创建 Vite 项目**

```bash
cd /Users/huhu/myGithub/jianzhi_ui_test
npm create vite@latest frontend -- --template react-ts
```

Expected: 项目创建成功，输出 "Scaffolding project in...frontend"

**Step 2: 验证项目结构**

```bash
ls -la frontend/
```

Expected: 看到 `package.json`, `src/`, `index.html` 等文件

**Step 3: 安装基础依赖**

```bash
cd frontend && npm install
```

Expected: 依赖安装成功

**Step 4: 验证开发服务器**

```bash
cd frontend && npm run dev
```

Expected: 服务器启动在 http://localhost:5173，显示 Vite 默认页面

**Step 5: 停止服务器并提交**

```bash
git add frontend/
git commit -m "feat: 初始化 Vite + React + TypeScript 项目"
```

---

## Task 2: 安装核心依赖

**Files:**
- Modify: `frontend/package.json`

**Step 1: 安装 Tailwind CSS v4**

```bash
cd frontend
npm install tailwindcss @tailwindcss/vite
```

Expected: package.json 中添加 tailwindcss 依赖

**Step 2: 安装 React Router v6**

```bash
npm install react-router-dom
```

Expected: package.json 中添加 react-router-dom 依赖

**Step 3: 安装 React Query**

```bash
npm install @tanstack/react-query
```

Expected: package.json 中添加 @tanstack/react-query 依赖

**Step 4: 安装 Lucide React 图标库**

```bash
npm install lucide-react
```

Expected: package.json 中添加 lucide-react 依赖

**Step 5: 提交依赖变更**

```bash
git add frontend/package.json frontend/package-lock.json
git commit -m "feat: 添加 Tailwind v4、React Router、React Query、Lucide 依赖"
```

---

## Task 3: 配置 Tailwind CSS v4

**Files:**
- Modify: `frontend/vite.config.ts`
- Modify: `frontend/src/index.css`
- Modify: `frontend/src/main.tsx`

**Step 1: 配置 Vite 插件**

修改 `frontend/vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

**Step 2: 更新 CSS 入口文件**

替换 `frontend/src/index.css` 内容为:

```css
@import "tailwindcss";
```

**Step 3: 验证 Tailwind 配置**

在 `frontend/src/App.tsx` 临时添加测试类:

```tsx
function App() {
  return (
    <div className="p-4 bg-blue-500 text-white">
      Tailwind 测试
    </div>
  )
}

export default App
```

**Step 4: 启动服务器验证**

```bash
cd frontend && npm run dev
```

Expected: 页面显示蓝色背景的 "Tailwind 测试" 文字

**Step 5: 恢复 App.tsx 并提交**

恢复 `frontend/src/App.tsx` 为原始内容，然后:

```bash
git add frontend/vite.config.ts frontend/src/index.css
git commit -m "feat: 配置 Tailwind CSS v4"
```

---

## Task 4: 创建类型定义

**Files:**
- Create: `frontend/src/types/index.ts`

**Step 1: 创建类型文件**

创建 `frontend/src/types/index.ts`:

```typescript
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
```

**Step 2: 提交类型定义**

```bash
git add frontend/src/types/
git commit -m "feat: 添加 Task、Run、Step、Report 类型定义"
```

---

## Task 5: 创建 API 客户端

**Files:**
- Create: `frontend/src/api/client.ts`

**Step 1: 创建 API 客户端**

创建 `frontend/src/api/client.ts`:

```typescript
const API_BASE = 'http://localhost:8000/api'

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = 'ApiError'
  }
}

export async function apiClient<T>(
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
    throw new ApiError(response.status, `API Error: ${response.status}`)
  }

  return response.json()
}
```

**Step 2: 提交 API 客户端**

```bash
git add frontend/src/api/
git commit -m "feat: 添加 API 客户端基础封装"
```

---

## Task 6: 创建 Button 组件

**Files:**
- Create: `frontend/src/components/Button.tsx`

**Step 1: 创建 Button 组件**

创建 `frontend/src/components/Button.tsx`:

```tsx
import { ButtonHTMLAttributes, ReactNode } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary'
  children: ReactNode
}

export function Button({ variant = 'primary', children, className = '', ...props }: ButtonProps) {
  const baseStyles = 'px-4 h-9 rounded-lg font-medium text-sm transition-colors'

  const variantStyles = {
    primary: 'bg-blue-500 text-white hover:bg-blue-600',
    secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
  }

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}
```

**Step 2: 提交 Button 组件**

```bash
git add frontend/src/components/Button.tsx
git commit -m "feat: 添加 Button 组件（primary/secondary 变体）"
```

---

## Task 7: 创建 NavItem 组件

**Files:**
- Create: `frontend/src/components/NavItem.tsx`

**Step 1: 创建 NavItem 组件**

创建 `frontend/src/components/NavItem.tsx`:

```tsx
import { NavLink } from 'react-router-dom'
import { LucideIcon } from 'lucide-react'

interface NavItemProps {
  icon: LucideIcon
  label: string
  to: string
}

export function NavItem({ icon: Icon, label, to }: NavItemProps) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `flex items-center gap-3 h-10 px-3 rounded-lg text-sm font-medium transition-colors ${
          isActive
            ? 'bg-blue-500 text-white'
            : 'text-gray-600 hover:bg-gray-100'
        }`
      }
    >
      <Icon className="w-5 h-5" />
      <span>{label}</span>
    </NavLink>
  )
}
```

**Step 2: 提交 NavItem 组件**

```bash
git add frontend/src/components/NavItem.tsx
git commit -m "feat: 添加 NavItem 导航项组件"
```

---

## Task 8: 创建 Sidebar 组件

**Files:**
- Create: `frontend/src/components/Sidebar.tsx`

**Step 1: 创建 Sidebar 组件**

创建 `frontend/src/components/Sidebar.tsx`:

```tsx
import { LayoutDashboard, ListTodo, Play, FileText } from 'lucide-react'
import { NavItem } from './NavItem'

export function Sidebar() {
  return (
    <aside className="w-60 bg-gray-50 p-4 flex flex-col h-screen">
      {/* Logo */}
      <div className="flex items-center gap-3 h-10">
        <div className="w-8 h-8 bg-blue-500 rounded-lg" />
        <span className="text-lg font-semibold text-gray-900">UI Test</span>
      </div>

      {/* Navigation */}
      <nav className="mt-4 space-y-1">
        <NavItem icon={LayoutDashboard} label="仪表盘" to="/" />
        <NavItem icon={ListTodo} label="任务管理" to="/tasks" />
        <NavItem icon={Play} label="执行监控" to="/runs" />
        <NavItem icon={FileText} label="报告查看" to="/reports" />
      </nav>
    </aside>
  )
}
```

**Step 2: 提交 Sidebar 组件**

```bash
git add frontend/src/components/Sidebar.tsx
git commit -m "feat: 添加 Sidebar 侧边栏组件"
```

---

## Task 9: 创建 Layout 组件

**Files:**
- Create: `frontend/src/components/Layout.tsx`

**Step 1: 创建 Layout 组件**

创建 `frontend/src/components/Layout.tsx`:

```tsx
import { ReactNode } from 'react'
import { Sidebar } from './Sidebar'

interface LayoutProps {
  children: ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="flex min-h-screen bg-white">
      <Sidebar />
      <main className="flex-1 p-6 overflow-auto">
        {children}
      </main>
    </div>
  )
}
```

**Step 2: 提交 Layout 组件**

```bash
git add frontend/src/components/Layout.tsx
git commit -m "feat: 添加 Layout 布局组件"
```

---

## Task 10: 创建页面占位组件

**Files:**
- Create: `frontend/src/pages/Dashboard.tsx`
- Create: `frontend/src/pages/Tasks.tsx`
- Create: `frontend/src/pages/TaskDetail.tsx`
- Create: `frontend/src/pages/RunMonitor.tsx`
- Create: `frontend/src/pages/Reports.tsx`

**Step 1: 创建 Dashboard 页面**

创建 `frontend/src/pages/Dashboard.tsx`:

```tsx
export function Dashboard() {
  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">仪表盘</h1>
      <p className="mt-2 text-gray-500">欢迎使用 AI + Playwright UI 自动化测试系统</p>
    </div>
  )
}
```

**Step 2: 创建 Tasks 页面**

创建 `frontend/src/pages/Tasks.tsx`:

```tsx
export function Tasks() {
  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">任务管理</h1>
      <p className="mt-2 text-gray-500">创建和管理测试任务</p>
    </div>
  )
}
```

**Step 3: 创建 TaskDetail 页面**

创建 `frontend/src/pages/TaskDetail.tsx`:

```tsx
import { useParams } from 'react-router-dom'

export function TaskDetail() {
  const { id } = useParams()

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">任务详情</h1>
      <p className="mt-2 text-gray-500">任务 ID: {id}</p>
    </div>
  )
}
```

**Step 4: 创建 RunMonitor 页面**

创建 `frontend/src/pages/RunMonitor.tsx`:

```tsx
import { useParams } from 'react-router-dom'

export function RunMonitor() {
  const { id } = useParams()

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">执行监控</h1>
      <p className="mt-2 text-gray-500">执行 ID: {id}</p>
    </div>
  )
}
```

**Step 5: 创建 Reports 页面**

创建 `frontend/src/pages/Reports.tsx`:

```tsx
export function Reports() {
  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">报告查看</h1>
      <p className="mt-2 text-gray-500">查看测试执行报告</p>
    </div>
  )
}
```

**Step 6: 提交页面组件**

```bash
git add frontend/src/pages/
git commit -m "feat: 添加 5 个页面占位组件"
```

---

## Task 11: 配置路由和入口

**Files:**
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/main.tsx`

**Step 1: 配置路由**

替换 `frontend/src/App.tsx`:

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { Tasks } from './pages/Tasks'
import { TaskDetail } from './pages/TaskDetail'
import { RunMonitor } from './pages/RunMonitor'
import { Reports } from './pages/Reports'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/tasks" element={<Tasks />} />
            <Route path="/tasks/:id" element={<TaskDetail />} />
            <Route path="/runs/:id" element={<RunMonitor />} />
            <Route path="/reports" element={<Reports />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
```

**Step 2: 清理 main.tsx**

确保 `frontend/src/main.tsx` 为:

```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

**Step 3: 删除无用文件**

```bash
rm frontend/src/App.css
```

**Step 4: 启动验证**

```bash
cd frontend && npm run dev
```

Expected:
- 访问 http://localhost:5173 显示仪表盘页面
- 侧边栏导航正常工作
- 点击导航项可以切换页面

**Step 5: 提交路由配置**

```bash
git add frontend/src/App.tsx frontend/src/main.tsx
git rm frontend/src/App.css
git commit -m "feat: 配置 React Router 路由和 React Query"
```

---

## Task 12: 最终验证和清理

**Step 1: 运行类型检查**

```bash
cd frontend && npm run build
```

Expected: 构建成功，无类型错误

**Step 2: 手动功能验证**

1. 启动开发服务器 `npm run dev`
2. 验证所有路由可访问
3. 验证侧边栏导航高亮正常
4. 验证样式符合设计稿

**Step 3: 更新进度文件**

更新 `docs/progress.md`:

```markdown
### Phase 2: 前端基础框架搭建 ✅
- **完成日期**: 2026-03-08
- **更新内容**:
  - Vite + React + TypeScript 项目初始化
  - Tailwind CSS v4 配置
  - Layout、Sidebar、NavItem、Button 组件
  - React Router 路由配置（5 个页面）
  - 类型定义（Task、Run、Step、Report）
```

**Step 4: 提交进度更新**

```bash
git add docs/progress.md
git commit -m "docs: 记录 Phase 2 完成 - 前端基础框架搭建"
```

---

## 完成检查清单

- [ ] Vite 项目正常运行
- [ ] Tailwind CSS v4 生效
- [ ] 侧边栏显示正确
- [ ] 导航项可点击并高亮
- [ ] 5 个页面路由正常
- [ ] 类型检查通过
- [ ] 构建成功
- [ ] 进度文件已更新
