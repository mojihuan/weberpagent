# Phase 4: 执行监控功能设计文档

> 创建日期: 2026-03-09

## 1. 概述

实现执行监控页面，支持实时查看 AI Agent 的执行进度、步骤截图和推理日志。

### 1.1 功能范围

- 执行启动入口（任务列表 + 任务详情页）
- SSE 实时进度接收
- 步骤进度时间线
- 截图实时预览（历史查看、全屏放大、下载）
- AI 推理日志展示

### 1.2 开发策略

- 前端独立开发，使用 Mock 数据模拟 SSE
- 后续对接真实 API 时只需替换数据源

---

## 2. 架构设计

### 2.1 模块结构

```
执行监控模块
├── 入口层
│   ├── TaskList → 执行按钮 → 跳转到 /runs/:id
│   └── TaskDetail → 执行按钮 → 跳转到 /runs/:id
│
├── 页面层
│   └── RunMonitor.tsx
│
├── 组件层
│   ├── RunHeader         # 状态概览（任务名、状态、进度）
│   ├── ScreenshotPanel   # 截图预览（左栏）
│   ├── StepTimeline      # 垂直时间线（右栏上）
│   └── ReasoningLog      # AI 日志（右栏下）
│
├── 数据层
│   ├── useRunStream.ts   # SSE 连接 Hook
│   └── mock/runStream.ts # Mock SSE 数据生成器
│
└── 工具层
    └── ImageViewer.tsx   # 全屏图片查看器
```

### 2.2 页面布局（左右分栏）

```
┌─────────────────────────────────────────────────────────┐
│  RunHeader: 任务名称 | 状态徽章 | 进度条 | 操作按钮      │
├────────────────────────────┬────────────────────────────┤
│                            │  StepTimeline              │
│    ScreenshotPanel         │  ├─ Step 1 ✓              │
│    (截图预览)               │  ├─ Step 2 ✓              │
│    - 当前/历史截图切换      │  ├─ Step 3 ● (当前)       │
│    - 点击放大              │  └─ Step 4 (等待中)        │
│    - 下载按钮              │                            │
│                            ├────────────────────────────┤
│                            │  ReasoningLog              │
│                            │  [Action] 点击登录按钮      │
│                            │  [Reasoning] 检测到登录表单 │
│                            │  ...                       │
└────────────────────────────┴────────────────────────────┘
```

---

## 3. 组件设计

### 3.1 RunHeader

**职责**: 展示执行状态概览

**Props**:
```typescript
interface RunHeaderProps {
  taskName: string
  status: Run['status']
  currentStep: number
  totalSteps: number
  onStop: () => void
}
```

**UI 元素**:
- 任务名称（左上）
- 状态徽章（running/success/failed/stopped）
- 进度条（显示 x/y 步骤）
- 停止按钮（仅 running 状态显示）

### 3.2 ScreenshotPanel

**职责**: 展示步骤截图

**Props**:
```typescript
interface ScreenshotPanelProps {
  currentStep: Step | null
  allSteps: Step[]
  onStepSelect: (index: number) => void
}
```

**UI 元素**:
- 主截图区域（居中显示）
- 左右箭头（切换历史步骤）
- 步骤指示器（如 3/10）
- 放大按钮
- 下载按钮

### 3.3 StepTimeline

**职责**: 垂直时间线展示步骤进度

**Props**:
```typescript
interface StepTimelineProps {
  steps: Step[]
  currentStepIndex: number
  onStepClick: (index: number) => void
}
```

**UI 元素**:
- 垂直时间线
- 每个步骤节点：
  - 状态图标（✓ 成功 / ✗ 失败 / ● 运行中 / ○ 等待）
  - 步骤编号
  - 动作描述
  - 耗时

### 3.4 ReasoningLog

**职责**: 展示 AI 推理日志

**Props**:
```typescript
interface ReasoningLogProps {
  steps: Step[]
  autoScroll?: boolean
}
```

**UI 元素**:
- 滚动容器
- 每个步骤的日志块：
  - Action 标签（蓝色）+ 内容
  - Reasoning 标签（灰色）+ 内容（如有）
- 自动滚动到最新

### 3.5 ImageViewer

**职责**: 全屏查看截图

**Props**:
```typescript
interface ImageViewerProps {
  src: string
  isOpen: boolean
  onClose: () => void
  onDownload?: () => void
}
```

**UI 元素**:
- 全屏 Modal
- 图片居中显示
- 关闭按钮
- 下载按钮

---

## 4. 数据流设计

### 4.1 SSE 事件格式

```typescript
// SSE 事件类型
type RunEventType =
  | 'started'   // 执行开始
  | 'step'      // 步骤更新
  | 'finished'  // 执行完成
  | 'error'     // 错误

// SSE 事件数据
interface RunEvent {
  type: RunEventType
  data: {
    run_id: string
    status?: Run['status']
    step?: Step
    error?: string
  }
}
```

### 4.2 useRunStream Hook

```typescript
interface UseRunStreamOptions {
  runId: string
  autoConnect?: boolean
}

interface UseRunStreamReturn {
  run: Run | null
  isConnected: boolean
  error: Error | null
  connect: () => void
  disconnect: () => void
}

function useRunStream(options: UseRunStreamOptions): UseRunStreamReturn
```

### 4.3 Mock 数据生成器

模拟真实 SSE 行为：
- 随机生成 5-10 个步骤
- 每步骤间隔 1-3 秒
- 80% 步骤成功，20% 失败
- 最后一步决定整体状态

---

## 5. 入口集成

### 5.1 任务列表页

在 `TaskTable` 组件的每行添加"执行"按钮：
- 点击后调用 `POST /api/runs`（Mock）
- 获取 run_id 后跳转到 `/runs/:id`

### 5.2 任务详情页

在 `TaskHeader` 组件添加"开始执行"按钮：
- 行为同上

---

## 6. 文件结构

```
frontend/src/
├── pages/
│   └── RunMonitor.tsx          # 执行监控页面
│
├── components/
│   ├── RunMonitor/
│   │   ├── RunHeader.tsx       # 状态概览
│   │   ├── ScreenshotPanel.tsx # 截图预览
│   │   ├── StepTimeline.tsx    # 步骤时间线
│   │   ├── ReasoningLog.tsx    # AI 日志
│   │   └── index.ts
│   └── shared/
│       └── ImageViewer.tsx     # 全屏图片查看器
│
├── hooks/
│   └── useRunStream.ts         # SSE 连接 Hook
│
└── api/
    └── mock/
        └── runStream.ts        # Mock SSE 生成器
```

---

## 7. 实现优先级

1. **P0 - 核心功能**
   - useRunStream Hook + Mock 数据
   - RunMonitor 页面骨架
   - StepTimeline 组件
   - ScreenshotPanel 组件

2. **P1 - 完善功能**
   - RunHeader 组件
   - ReasoningLog 组件
   - 入口集成（任务列表/详情页）

3. **P2 - 增强体验**
   - ImageViewer 全屏查看
   - 下载功能
   - 错误处理优化
