# Phase 4: 执行监控功能实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现执行监控页面，支持实时查看 AI Agent 的执行进度、步骤截图和推理日志。

**Architecture:** 左右分栏布局（截图预览 + 时间线/日志），使用 Mock SSE 模拟实时数据流，通过 useRunStream Hook 封装连接逻辑。

**Tech Stack:** React 19, TypeScript, Tailwind CSS v4, React Router, SSE (Mock)

---

## Task 1: 创建 Mock SSE 数据生成器

**Files:**
- Create: `frontend/src/api/mock/runStream.ts`

**Step 1: 创建 Mock SSE 生成器**

```typescript
// frontend/src/api/mock/runStream.ts
import type { Run, Step } from '../../types'

export type RunEventType = 'started' | 'step' | 'finished' | 'error'

export interface RunEvent {
  type: RunEventType
  data: {
    run_id: string
    status?: Run['status']
    step?: Step
    error?: string
  }
}

const ACTIONS = [
  '打开目标页面',
  '等待页面加载完成',
  '识别登录表单',
  '填写用户名',
  '填写密码',
  '点击登录按钮',
  '等待登录响应',
  '验证登录状态',
  '截图保存',
  '检查页面元素',
]

const REASONINGS = [
  'AI 分析：当前页面状态正常，准备执行下一步操作',
  '检测到目标元素，正在进行交互',
  '页面加载中，等待响应...',
  '元素定位成功，准备执行点击操作',
  '表单填写完成，准备提交',
  '验证操作结果，确认执行状态',
]

const SCREENSHOTS = [
  'https://picsum.photos/seed/step1/800/600',
  'https://picsum.photos/seed/step2/800/600',
  'https://picsum.photos/seed/step3/800/600',
  'https://picsum.photos/seed/step4/800/600',
  'https://picsum.photos/seed/step5/800/600',
  'https://picsum.photos/seed/step6/800/600',
  'https://picsum.photos/seed/step7/800/600',
  'https://picsum.photos/seed/step8/800/600',
  'https://picsum.photos/seed/step9/800/600',
  'https://picsum.photos/seed/step10/800/600',
]

export interface MockRunStreamOptions {
  runId: string
  onEvent: (event: RunEvent) => void
  stepCount?: number
  stepInterval?: number
  failureIndex?: number | null
}

export function createMockRunStream(options: MockRunStreamOptions): {
  start: () => void
  stop: () => void
} {
  const {
    runId,
    onEvent,
    stepCount = Math.floor(Math.random() * 6) + 5, // 5-10 步
    stepInterval = 2000,
    failureIndex = Math.random() > 0.8 ? Math.floor(Math.random() * (stepCount - 2)) + 1 : null, // 80% 成功率
  } = options

  let currentStep = 0
  let timeoutId: ReturnType<typeof setTimeout> | null = null
  let stopped = false

  const generateStep = (index: number): Step => {
    const isFailed = failureIndex !== null && index === failureIndex
    return {
      index: index + 1,
      action: ACTIONS[index % ACTIONS.length] || `执行操作 ${index + 1}`,
      reasoning: REASONINGS[index % REASONINGS.length],
      screenshot: SCREENSHOTS[index % SCREENSHOTS.length],
      status: isFailed ? 'failed' : 'success',
      error: isFailed ? '元素定位超时：未找到目标按钮' : undefined,
      duration_ms: Math.floor(Math.random() * 2000) + 500,
    }
  }

  const sendStep = () => {
    if (stopped) return

    if (currentStep === 0) {
      onEvent({
        type: 'started',
        data: { run_id: runId, status: 'running' },
      })
    }

    if (currentStep < stepCount) {
      const step = generateStep(currentStep)
      onEvent({
        type: 'step',
        data: { run_id: runId, step },
      })
      currentStep++
      timeoutId = setTimeout(sendStep, stepInterval)
    } else {
      const finalStatus = failureIndex !== null ? 'failed' : 'success'
      onEvent({
        type: 'finished',
        data: { run_id: runId, status: finalStatus },
      })
    }
  }

  return {
    start: () => {
      stopped = false
      currentStep = 0
      timeoutId = setTimeout(sendStep, 500)
    },
    stop: () => {
      stopped = true
      if (timeoutId) {
        clearTimeout(timeoutId)
        timeoutId = null
      }
      onEvent({
        type: 'finished',
        data: { run_id: runId, status: 'stopped' },
      })
    },
  }
}
```

**Step 2: 验证 Mock 数据生成器**

在浏览器控制台测试：
```javascript
import { createMockRunStream } from './api/mock/runStream'

const stream = createMockRunStream({
  runId: 'test-run',
  onEvent: (event) => console.log('Event:', event),
})
stream.start()
// 应该看到 started -> step(多个) -> finished 事件
```

**Step 3: 提交**

```bash
git add frontend/src/api/mock/runStream.ts
git commit -m "feat: 添加 Mock SSE 数据生成器

- 支持 started/step/finished 事件类型
- 可配置步骤数量、间隔、失败位置
- 80% 成功率模拟真实场景"
```

---

## Task 2: 创建 useRunStream Hook

**Files:**
- Create: `frontend/src/hooks/useRunStream.ts`

**Step 1: 创建 SSE Hook**

```typescript
// frontend/src/hooks/useRunStream.ts
import { useState, useEffect, useCallback, useRef } from 'react'
import type { Run, Step } from '../types'
import { createMockRunStream, type RunEvent } from '../api/mock/runStream'

interface UseRunStreamOptions {
  runId: string
  autoConnect?: boolean
  useMock?: boolean
}

interface UseRunStreamReturn {
  run: Run | null
  isConnected: boolean
  error: Error | null
  connect: () => void
  disconnect: () => void
}

export function useRunStream(options: UseRunStreamOptions): UseRunStreamReturn {
  const { runId, autoConnect = true, useMock = true } = options

  const [run, setRun] = useState<Run | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const streamRef = useRef<ReturnType<typeof createMockRunStream> | null>(null)

  const handleEvent = useCallback((event: RunEvent) => {
    switch (event.type) {
      case 'started':
        setRun({
          id: runId,
          task_id: '',
          status: 'running',
          started_at: new Date().toISOString(),
          steps: [],
        })
        break

      case 'step':
        setRun(prev => {
          if (!prev || !event.data.step) return prev
          return {
            ...prev,
            steps: [...prev.steps, event.data.step!],
          }
        })
        break

      case 'finished':
        setRun(prev => {
          if (!prev) return prev
          return {
            ...prev,
            status: event.data.status || 'success',
            finished_at: new Date().toISOString(),
          }
        })
        setIsConnected(false)
        break

      case 'error':
        setError(new Error(event.data.error || 'Unknown error'))
        setIsConnected(false)
        break
    }
  }, [runId])

  const connect = useCallback(() => {
    if (isConnected) return

    setError(null)
    setIsConnected(true)

    if (useMock) {
      streamRef.current = createMockRunStream({
        runId,
        onEvent: handleEvent,
      })
      streamRef.current.start()
    } else {
      // TODO: 实现真实 SSE 连接
      // const eventSource = new EventSource(`/api/runs/${runId}/stream`)
    }
  }, [runId, isConnected, useMock, handleEvent])

  const disconnect = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.stop()
      streamRef.current = null
    }
    setIsConnected(false)
  }, [])

  useEffect(() => {
    if (autoConnect) {
      connect()
    }
    return () => {
      disconnect()
    }
  }, [autoConnect, connect, disconnect])

  return {
    run,
    isConnected,
    error,
    connect,
    disconnect,
  }
}
```

**Step 2: 验证 Hook**

在 RunMonitor 页面临时测试：
```typescript
// 临时添加到 RunMonitor.tsx
const { run, isConnected } = useRunStream({ runId: id || 'test' })
console.log('Run state:', run, 'Connected:', isConnected)
```

**Step 3: 提交**

```bash
git add frontend/src/hooks/useRunStream.ts
git commit -m "feat: 添加 useRunStream Hook

- 封装 SSE 连接逻辑
- 支持 Mock 和真实连接切换
- 自动管理连接生命周期"
```

---

## Task 3: 创建 RunHeader 组件

**Files:**
- Create: `frontend/src/components/RunMonitor/RunHeader.tsx`
- Create: `frontend/src/components/RunMonitor/index.ts`

**Step 1: 创建 RunHeader 组件**

```typescript
// frontend/src/components/RunMonitor/RunHeader.tsx
import { Square } from 'lucide-react'
import type { Run } from '../../types'
import { Button } from '../Button'
import { StatusBadge } from '../shared'

interface RunHeaderProps {
  taskName: string
  status: Run['status']
  currentStep: number
  totalSteps: number
  onStop: () => void
}

export function RunHeader({
  taskName,
  status,
  currentStep,
  totalSteps,
  onStop,
}: RunHeaderProps) {
  const progress = totalSteps > 0 ? (currentStep / totalSteps) * 100 : 0
  const isRunning = status === 'running'

  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <h1 className="text-xl font-semibold text-gray-900">{taskName}</h1>
          <StatusBadge status={status} />
        </div>
        {isRunning && (
          <Button variant="secondary" onClick={onStop} className="text-red-600 hover:bg-red-50">
            <Square className="w-4 h-4 mr-1" />
            停止执行
          </Button>
        )}
      </div>

      <div className="flex items-center gap-3">
        <div className="flex-1 bg-gray-200 rounded-full h-2 overflow-hidden">
          <div
            className="h-full bg-blue-500 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
        <span className="text-sm text-gray-500 min-w-[60px] text-right">
          {currentStep} / {totalSteps} 步
        </span>
      </div>
    </div>
  )
}
```

**Step 2: 创建 index.ts 导出**

```typescript
// frontend/src/components/RunMonitor/index.ts
export { RunHeader } from './RunHeader'
```

**Step 3: 验证组件**

```bash
# 启动开发服务器
cd frontend && npm run dev
# 访问 http://localhost:5173/runs/test
# 检查 Header 是否正确显示
```

**Step 4: 提交**

```bash
git add frontend/src/components/RunMonitor/
git commit -m "feat: 添加 RunHeader 组件

- 显示任务名称和状态徽章
- 进度条展示执行进度
- 运行中显示停止按钮"
```

---

## Task 4: 创建 StepTimeline 组件

**Files:**
- Create: `frontend/src/components/RunMonitor/StepTimeline.tsx`
- Modify: `frontend/src/components/RunMonitor/index.ts`

**Step 1: 创建 StepTimeline 组件**

```typescript
// frontend/src/components/RunMonitor/StepTimeline.tsx
import { CheckCircle, XCircle, Loader2, Circle } from 'lucide-react'
import type { Step } from '../../types'

interface StepTimelineProps {
  steps: Step[]
  currentStepIndex: number
  onStepClick: (index: number) => void
}

export function StepTimeline({ steps, currentStepIndex, onStepClick }: StepTimelineProps) {
  const getStepStatus = (index: number): 'success' | 'failed' | 'running' | 'pending' => {
    if (index < currentStepIndex) {
      return steps[index]?.status || 'success'
    }
    if (index === currentStepIndex) {
      return 'running'
    }
    return 'pending'
  }

  const getStepIcon = (status: 'success' | 'failed' | 'running' | 'pending') => {
    switch (status) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />
      case 'running':
        return <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
      case 'pending':
        return <Circle className="w-5 h-5 text-gray-300" />
    }
  }

  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`
    return `${(ms / 1000).toFixed(1)}s`
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-200">
        <h3 className="font-medium text-gray-900">执行步骤</h3>
      </div>
      <div className="flex-1 overflow-y-auto p-4">
        <div className="relative">
          {steps.map((step, index) => {
            const status = getStepStatus(index)
            const isClickable = index <= currentStepIndex

            return (
              <div
                key={index}
                onClick={() => isClickable && onStepClick(index)}
                className={`flex gap-3 pb-4 ${
                  index < steps.length - 1
                    ? 'border-l-2 border-gray-200 ml-2.5 pl-4 -ml-0'
                    : 'ml-2.5 pl-4 -ml-0'
                } ${isClickable ? 'cursor-pointer hover:bg-gray-50 -mx-4 px-4 rounded' : ''}`}
              >
                <div className="absolute left-0">{getStepIcon(status)}</div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-sm font-medium text-gray-900">
                      步骤 {step.index}
                    </span>
                    {step.duration_ms > 0 && (
                      <span className="text-xs text-gray-500">
                        {formatDuration(step.duration_ms)}
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-600 truncate">{step.action}</p>
                  {step.error && (
                    <p className="text-xs text-red-500 mt-1 truncate">{step.error}</p>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
```

**Step 2: 更新 index.ts**

```typescript
// frontend/src/components/RunMonitor/index.ts
export { RunHeader } from './RunHeader'
export { StepTimeline } from './StepTimeline'
```

**Step 3: 验证组件**

检查时间线是否正确显示步骤状态和图标。

**Step 4: 提交**

```bash
git add frontend/src/components/RunMonitor/
git commit -m "feat: 添加 StepTimeline 组件

- 垂直时间线展示步骤进度
- 支持 4 种状态图标（成功/失败/运行/等待）
- 点击历史步骤可查看对应截图"
```

---

## Task 5: 创建 ScreenshotPanel 组件

**Files:**
- Create: `frontend/src/components/RunMonitor/ScreenshotPanel.tsx`
- Modify: `frontend/src/components/RunMonitor/index.ts`

**Step 1: 创建 ScreenshotPanel 组件**

```typescript
// frontend/src/components/RunMonitor/ScreenshotPanel.tsx
import { useState } from 'react'
import { ChevronLeft, ChevronRight, ZoomIn, Download } from 'lucide-react'
import type { Step } from '../../types'

interface ScreenshotPanelProps {
  steps: Step[]
  currentViewIndex: number
  onViewChange: (index: number) => void
  onZoom: () => void
}

export function ScreenshotPanel({
  steps,
  currentViewIndex,
  onViewChange,
  onZoom,
}: ScreenshotPanelProps) {
  const [imageLoaded, setImageLoaded] = useState(false)

  const currentStep = steps[currentViewIndex]
  const hasSteps = steps.length > 0
  const canGoPrev = currentViewIndex > 0
  const canGoNext = currentViewIndex < steps.length - 1

  const handlePrev = () => {
    if (canGoPrev) {
      setImageLoaded(false)
      onViewChange(currentViewIndex - 1)
    }
  }

  const handleNext = () => {
    if (canGoNext) {
      setImageLoaded(false)
      onViewChange(currentViewIndex + 1)
    }
  }

  const handleDownload = () => {
    if (!currentStep) return
    const link = document.createElement('a')
    link.href = currentStep.screenshot
    link.download = `step-${currentStep.index}.png`
    link.click()
  }

  return (
    <div className="flex flex-col h-full bg-gray-50">
      <div className="px-4 py-3 border-b border-gray-200 bg-white flex items-center justify-between">
        <h3 className="font-medium text-gray-900">截图预览</h3>
        {hasSteps && (
          <span className="text-sm text-gray-500">
            {currentViewIndex + 1} / {steps.length}
          </span>
        )}
      </div>

      <div className="flex-1 relative flex items-center justify-center p-4">
        {!hasSteps ? (
          <div className="text-gray-400 text-center">
            <p>等待执行开始...</p>
          </div>
        ) : (
          <>
            {!imageLoaded && (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
                <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
              </div>
            )}
            <img
              src={currentStep.screenshot}
              alt={`步骤 ${currentStep.index}`}
              className={`max-w-full max-h-full object-contain rounded-lg shadow-lg transition-opacity ${
                imageLoaded ? 'opacity-100' : 'opacity-0'
              }`}
              onLoad={() => setImageLoaded(true)}
            />

            {/* 左箭头 */}
            <button
              onClick={handlePrev}
              disabled={!canGoPrev}
              className={`absolute left-2 p-2 rounded-full bg-white shadow-md transition ${
                canGoPrev
                  ? 'hover:bg-gray-100 text-gray-700'
                  : 'opacity-50 cursor-not-allowed text-gray-400'
              }`}
            >
              <ChevronLeft className="w-5 h-5" />
            </button>

            {/* 右箭头 */}
            <button
              onClick={handleNext}
              disabled={!canGoNext}
              className={`absolute right-2 p-2 rounded-full bg-white shadow-md transition ${
                canGoNext
                  ? 'hover:bg-gray-100 text-gray-700'
                  : 'opacity-50 cursor-not-allowed text-gray-400'
              }`}
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </>
        )}
      </div>

      {/* 工具栏 */}
      {hasSteps && (
        <div className="px-4 py-2 border-t border-gray-200 bg-white flex items-center justify-center gap-2">
          <button
            onClick={onZoom}
            className="p-2 rounded hover:bg-gray-100 text-gray-600"
            title="放大查看"
          >
            <ZoomIn className="w-5 h-5" />
          </button>
          <button
            onClick={handleDownload}
            className="p-2 rounded hover:bg-gray-100 text-gray-600"
            title="下载截图"
          >
            <Download className="w-5 h-5" />
          </button>
        </div>
      )}
    </div>
  )
}
```

**Step 2: 更新 index.ts**

```typescript
// frontend/src/components/RunMonitor/index.ts
export { RunHeader } from './RunHeader'
export { StepTimeline } from './StepTimeline'
export { ScreenshotPanel } from './ScreenshotPanel'
```

**Step 3: 验证组件**

检查截图预览、左右切换、工具栏按钮是否正常工作。

**Step 4: 提交**

```bash
git add frontend/src/components/RunMonitor/
git commit -m "feat: 添加 ScreenshotPanel 组件

- 截图预览与加载状态
- 左右箭头切换历史步骤
- 放大和下载按钮"
```

---

## Task 6: 创建 ReasoningLog 组件

**Files:**
- Create: `frontend/src/components/RunMonitor/ReasoningLog.tsx`
- Modify: `frontend/src/components/RunMonitor/index.ts`

**Step 1: 创建 ReasoningLog 组件**

```typescript
// frontend/src/components/RunMonitor/ReasoningLog.tsx
import { useEffect, useRef } from 'react'
import type { Step } from '../../types'

interface ReasoningLogProps {
  steps: Step[]
  autoScroll?: boolean
}

export function ReasoningLog({ steps, autoScroll = true }: ReasoningLogProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (autoScroll && containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }, [steps, autoScroll])

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-200">
        <h3 className="font-medium text-gray-900">AI 推理日志</h3>
      </div>
      <div ref={containerRef} className="flex-1 overflow-y-auto p-4 space-y-4">
        {steps.length === 0 ? (
          <div className="text-gray-400 text-center py-8">
            <p>等待执行开始...</p>
          </div>
        ) : (
          steps.map((step, index) => (
            <div key={index} className="space-y-2">
              {/* Action 标签 */}
              <div className="flex items-start gap-2">
                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-700 shrink-0">
                  Action
                </span>
                <span className="text-sm text-gray-900">{step.action}</span>
              </div>

              {/* Reasoning 标签 */}
              {step.reasoning && (
                <div className="flex items-start gap-2">
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-600 shrink-0">
                    Reasoning
                  </span>
                  <span className="text-sm text-gray-600">{step.reasoning}</span>
                </div>
              )}

              {/* 错误信息 */}
              {step.error && (
                <div className="flex items-start gap-2">
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-700 shrink-0">
                    Error
                  </span>
                  <span className="text-sm text-red-600">{step.error}</span>
                </div>
              )}

              {index < steps.length - 1 && (
                <div className="border-b border-gray-100 my-2" />
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}
```

**Step 2: 更新 index.ts**

```typescript
// frontend/src/components/RunMonitor/index.ts
export { RunHeader } from './RunHeader'
export { StepTimeline } from './StepTimeline'
export { ScreenshotPanel } from './ScreenshotPanel'
export { ReasoningLog } from './ReasoningLog'
```

**Step 3: 验证组件**

检查日志是否正确显示 Action/Reasoning/Error 标签，自动滚动是否正常。

**Step 4: 提交**

```bash
git add frontend/src/components/RunMonitor/
git commit -m "feat: 添加 ReasoningLog 组件

- 分离展示 Action 和 Reasoning
- 不同颜色标签区分类型
- 自动滚动到最新内容"
```

---

## Task 7: 创建 ImageViewer 共享组件

**Files:**
- Create: `frontend/src/components/shared/ImageViewer.tsx`
- Modify: `frontend/src/components/shared/index.ts`

**Step 1: 创建 ImageViewer 组件**

```typescript
// frontend/src/components/shared/ImageViewer.tsx
import { useEffect } from 'react'
import { X, Download } from 'lucide-react'

interface ImageViewerProps {
  src: string
  isOpen: boolean
  onClose: () => void
  onDownload?: () => void
}

export function ImageViewer({ src, isOpen, onClose, onDownload }: ImageViewerProps) {
  // ESC 关闭
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isOpen, onClose])

  if (!isOpen) return null

  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = src
    link.download = src.split('/').pop() || 'screenshot.png'
    link.click()
    onDownload?.()
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
      onClick={onClose}
    >
      {/* 关闭按钮 */}
      <button
        onClick={onClose}
        className="absolute top-4 right-4 p-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition"
      >
        <X className="w-6 h-6" />
      </button>

      {/* 下载按钮 */}
      <button
        onClick={handleDownload}
        className="absolute top-4 right-14 p-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition"
      >
        <Download className="w-6 h-6" />
      </button>

      {/* 图片 */}
      <img
        src={src}
        alt="Screenshot"
        className="max-w-[90vw] max-h-[90vh] object-contain"
        onClick={e => e.stopPropagation()}
      />
    </div>
  )
}
```

**Step 2: 更新 shared/index.ts**

```typescript
// frontend/src/components/shared/index.ts
export { StatusBadge } from './StatusBadge'
export { Pagination } from './Pagination'
export { EmptyState } from './EmptyState'
export { ConfirmModal } from './ConfirmModal'
export { LoadingSpinner } from './LoadingSpinner'
export { ImageViewer } from './ImageViewer'
```

**Step 3: 验证组件**

点击放大按钮，检查全屏 Modal 是否正确显示，ESC 和点击背景是否可关闭。

**Step 4: 提交**

```bash
git add frontend/src/components/shared/
git commit -m "feat: 添加 ImageViewer 全屏图片查看器

- 全屏 Modal 展示截图
- 支持 ESC 关闭和点击背景关闭
- 内置下载功能"
```

---

## Task 8: 组装 RunMonitor 页面

**Files:**
- Modify: `frontend/src/pages/RunMonitor.tsx`

**Step 1: 实现完整页面**

```typescript
// frontend/src/pages/RunMonitor.tsx
import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { RunHeader, StepTimeline, ScreenshotPanel, ReasoningLog } from '../components/RunMonitor'
import { ImageViewer } from '../components/shared'
import { useRunStream } from '../hooks/useRunStream'
import { mockTasks } from '../api/mock/tasks'

export function RunMonitor() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const { run, isConnected, disconnect } = useRunStream({
    runId: id || '',
    autoConnect: true,
  })

  const [viewIndex, setViewIndex] = useState(0)
  const [viewerOpen, setViewerOpen] = useState(false)

  // 自动跟随最新步骤
  useEffect(() => {
    if (run?.steps.length) {
      setViewIndex(run.steps.length - 1)
    }
  }, [run?.steps.length])

  const handleStop = () => {
    disconnect()
  }

  const handleStepClick = (index: number) => {
    setViewIndex(index)
  }

  const handleViewChange = (index: number) => {
    setViewIndex(index)
  }

  const handleZoom = () => {
    setViewerOpen(true)
  }

  // 获取任务名称（从 Mock 数据）
  const taskName = run?.task_id
    ? mockTasks.find(t => t.id === run.task_id)?.name || '未知任务'
    : '执行监控'

  const currentStep = run?.steps[viewIndex]

  if (!run) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-500">正在连接...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <RunHeader
        taskName={taskName}
        status={run.status}
        currentStep={run.steps.length}
        totalSteps={run.steps.length > 0 ? run.steps.length : 10}
        onStop={handleStop}
      />

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left: Screenshot */}
        <div className="w-1/2 border-r border-gray-200">
          <ScreenshotPanel
            steps={run.steps}
            currentViewIndex={viewIndex}
            onViewChange={handleViewChange}
            onZoom={handleZoom}
          />
        </div>

        {/* Right: Timeline + Log */}
        <div className="w-1/2 flex flex-col">
          <div className="h-1/2 border-b border-gray-200">
            <StepTimeline
              steps={run.steps}
              currentStepIndex={run.steps.length - 1}
              onStepClick={handleStepClick}
            />
          </div>
          <div className="h-1/2">
            <ReasoningLog steps={run.steps} autoScroll />
          </div>
        </div>
      </div>

      {/* ImageViewer Modal */}
      {currentStep && (
        <ImageViewer
          src={currentStep.screenshot}
          isOpen={viewerOpen}
          onClose={() => setViewerOpen(false)}
        />
      )}
    </div>
  )
}
```

**Step 2: 验证页面**

1. 访问 `/runs/test`
2. 检查 Mock SSE 是否正常工作
3. 验证所有组件交互是否正常

**Step 3: 提交**

```bash
git add frontend/src/pages/RunMonitor.tsx
git commit -m "feat: 完成 RunMonitor 执行监控页面

- 左右分栏布局
- 集成 useRunStream Hook
- 自动跟随最新步骤
- 全屏查看截图"
```

---

## Task 9: 添加执行入口 - 任务列表页

**Files:**
- Modify: `frontend/src/components/TaskList/TaskRow.tsx`
- Create: `frontend/src/api/runs.ts`

**Step 1: 创建 runs API**

```typescript
// frontend/src/api/runs.ts
import { v4 as uuidv4 } from 'uuid'

// Mock: 启动执行
export async function startRun(taskId: string): Promise<{ runId: string }> {
  // 模拟 API 延迟
  await new Promise(resolve => setTimeout(resolve, 300))

  const runId = `r_${uuidv4().slice(0, 8)}`
  return { runId }
}
```

**Step 2: 修改 TaskRow 组件**

```typescript
// frontend/src/components/TaskList/TaskRow.tsx
import { Play, Pencil, Trash2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import type { Task } from '../../types'
import { StatusBadge } from '../shared'
import { startRun } from '../../api/runs'

interface TaskRowProps {
  task: Task
  selected: boolean
  onSelect: () => void
  onEdit: () => void
  onDelete: () => void
}

export function TaskRow({ task, selected, onSelect, onEdit, onDelete }: TaskRowProps) {
  const navigate = useNavigate()
  const [isStarting, setIsStarting] = useState(false)

  const handleExecute = async (e: React.MouseEvent) => {
    e.stopPropagation()
    if (isStarting) return

    setIsStarting(true)
    try {
      const { runId } = await startRun(task.id)
      navigate(`/runs/${runId}`)
    } catch (error) {
      console.error('Failed to start run:', error)
    } finally {
      setIsStarting(false)
    }
  }

  const handleEdit = (e: React.MouseEvent) => {
    e.stopPropagation()
    onEdit()
  }

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation()
    onDelete()
  }

  const handleRowClick = () => {
    navigate(`/tasks/${task.id}`)
  }

  const domain = (() => {
    try {
      return new URL(task.target_url).hostname
    } catch {
      return task.target_url
    }
  })()

  return (
    <tr
      onClick={handleRowClick}
      className="border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition-colors"
    >
      <td className="px-4 py-3" onClick={e => e.stopPropagation()}>
        <input
          type="checkbox"
          checked={selected}
          onChange={onSelect}
          className="w-4 h-4 rounded border-gray-300 text-blue-500 focus:ring-blue-500"
        />
      </td>
      <td className="px-4 py-3">
        <div className="font-medium text-gray-900">{task.name}</div>
        <div className="text-sm text-gray-500 truncate max-w-xs">{task.description}</div>
      </td>
      <td className="px-4 py-3 text-gray-500 text-sm">{domain}</td>
      <td className="px-4 py-3">
        <StatusBadge status={task.status} />
      </td>
      <td className="px-4 py-3 text-gray-500 text-sm">{task.max_steps}</td>
      <td className="px-4 py-3">
        <div className="flex items-center gap-1">
          <button
            onClick={handleExecute}
            disabled={isStarting}
            className={`p-1.5 rounded hover:bg-gray-100 ${
              isStarting
                ? 'text-gray-300 cursor-wait'
                : 'text-gray-500 hover:text-green-500'
            }`}
            title="立即执行"
          >
            <Play className="w-4 h-4" />
          </button>
          <button
            onClick={handleEdit}
            className="p-1.5 rounded hover:bg-gray-100 text-gray-500 hover:text-gray-700"
            title="编辑"
          >
            <Pencil className="w-4 h-4" />
          </button>
          <button
            onClick={handleDelete}
            className="p-1.5 rounded hover:bg-gray-100 text-gray-500 hover:text-red-500"
            title="删除"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </td>
    </tr>
  )
}
```

**Step 3: 安装 uuid 依赖**

```bash
cd frontend
npm install uuid
npm install -D @types/uuid
```

**Step 4: 验证入口**

1. 在任务列表页点击执行按钮
2. 应该跳转到 `/runs/:id` 页面

**Step 5: 提交**

```bash
git add frontend/src/components/TaskList/TaskRow.tsx frontend/src/api/runs.ts frontend/package.json
git commit -m "feat: 任务列表页添加执行入口

- 点击执行按钮启动 Run 并跳转到监控页
- 添加 loading 状态防止重复点击"
```

---

## Task 10: 添加执行入口 - 任务详情页

**Files:**
- Modify: `frontend/src/components/TaskDetail/TaskHeader.tsx`
- Modify: `frontend/src/pages/TaskDetail.tsx`

**Step 1: 修改 TaskHeader 组件**

```typescript
// frontend/src/components/TaskDetail/TaskHeader.tsx
import { ArrowLeft, Play, Pencil, Trash2, Loader2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import type { Task } from '../../types'
import { Button } from '../Button'
import { StatusBadge } from '../shared'

interface TaskHeaderProps {
  task: Task
  onEdit: () => void
  onDelete: () => void
  onExecute: () => void
  isExecuting?: boolean
}

export function TaskHeader({
  task,
  onEdit,
  onDelete,
  onExecute,
  isExecuting = false,
}: TaskHeaderProps) {
  const navigate = useNavigate()

  return (
    <div className="mb-6">
      <button
        onClick={() => navigate('/tasks')}
        className="flex items-center gap-1 text-gray-500 hover:text-gray-700 mb-4"
      >
        <ArrowLeft className="w-4 h-4" />
        返回列表
      </button>

      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-2xl font-semibold text-gray-900">{task.name}</h1>
            <StatusBadge status={task.status} />
          </div>
          <p className="text-gray-500">{task.description}</p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="primary"
            onClick={onExecute}
            disabled={isExecuting}
          >
            {isExecuting ? (
              <Loader2 className="w-4 h-4 mr-1 animate-spin" />
            ) : (
              <Play className="w-4 h-4 mr-1" />
            )}
            {isExecuting ? '启动中...' : '立即执行'}
          </Button>
          <Button variant="secondary" onClick={onEdit}>
            <Pencil className="w-4 h-4 mr-1" />
            编辑
          </Button>
          <Button
            variant="secondary"
            onClick={onDelete}
            className="text-red-600 hover:bg-red-50"
          >
            <Trash2 className="w-4 h-4 mr-1" />
            删除
          </Button>
        </div>
      </div>
    </div>
  )
}
```

**Step 2: 修改 TaskDetail 页面**

在 `TaskDetail.tsx` 中添加执行逻辑：

```typescript
// 添加 imports
import { startRun } from '../api/runs'

// 在组件内添加
const [isExecuting, setIsExecuting] = useState(false)

const handleExecute = async () => {
  if (isExecuting) return
  setIsExecuting(true)
  try {
    const { runId } = await startRun(task.id)
    navigate(`/runs/${runId}`)
  } catch (error) {
    console.error('Failed to start run:', error)
  } finally {
    setIsExecuting(false)
  }
}

// 更新 TaskHeader props
<TaskHeader
  task={task}
  onEdit={handleEdit}
  onDelete={() => setShowDeleteConfirm(true)}
  onExecute={handleExecute}
  isExecuting={isExecuting}
/>
```

**Step 3: 验证入口**

1. 在任务详情页点击"立即执行"按钮
2. 应该跳转到 `/runs/:id` 页面

**Step 4: 提交**

```bash
git add frontend/src/components/TaskDetail/TaskHeader.tsx frontend/src/pages/TaskDetail.tsx
git commit -m "feat: 任务详情页添加执行入口

- 立即执行按钮（主要按钮样式）
- 添加 loading 状态"
```

---

## Task 11: 更新进度文档

**Files:**
- Modify: `docs/progress.md`
- Modify: `docs/2_前端主计划.md`

**Step 1: 更新 progress.md**

```markdown
### Phase 4: 执行监控功能 ✅
- **完成日期**: 2026-03-09
- **更新内容**:
  - Mock SSE 数据生成器
  - useRunStream Hook
  - RunMonitor 页面（左右分栏布局）
  - RunHeader、StepTimeline、ScreenshotPanel、ReasoningLog 组件
  - ImageViewer 全屏图片查看器
  - 任务列表/详情页执行入口
```

**Step 2: 更新 2_前端主计划.md**

将 Phase 4 的任务勾选：
```markdown
### Phase 4: 执行监控功能（1 天）✅

- [x] 4.1 实现执行启动功能
- [x] 4.2 实现 SSE 实时进度接收
- [x] 4.3 实现步骤进度展示
- [x] 4.4 实现截图实时预览
```

**Step 3: 提交**

```bash
git add docs/progress.md docs/2_前端主计划.md
git commit -m "docs: 记录 Phase 4 执行监控功能完成"
```

---

## 任务依赖图

```
Task 1 (Mock SSE) ──┬──> Task 2 (useRunStream)
                    │
                    └──> Task 3-6 (组件) ──> Task 8 (页面组装)
                                              │
Task 7 (ImageViewer) ─────────────────────────┘
                                              │
Task 9 (列表入口) ─────────────────────────────┤
                                              │
Task 10 (详情入口) ────────────────────────────┘
                                              │
                                              v
                                        Task 11 (文档更新)
```

---

## 验证清单

完成所有任务后，验证以下功能：

- [ ] 访问 `/runs/:id` 页面正常加载
- [ ] Mock SSE 自动开始推送步骤
- [ ] 步骤时间线实时更新
- [ ] 截图预览正确显示
- [ ] 左右箭头切换历史步骤
- [ ] 点击时间线步骤切换截图
- [ ] 放大按钮打开全屏 Modal
- [ ] 下载按钮正常工作
- [ ] AI 日志自动滚动
- [ ] 停止按钮终止执行
- [ ] 任务列表执行按钮跳转到监控页
- [ ] 任务详情执行按钮跳转到监控页
