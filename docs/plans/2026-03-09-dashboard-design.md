# Phase 6: Dashboard 仪表盘设计

> 创建日期: 2026-03-09

## 1. 概述

为 AI + Playwright UI 自动化测试系统实现仪表盘功能，展示系统运行概览和快速操作入口。

## 2. 布局方案

采用 **四象限布局**：

```
┌─────────────────────────────────────────────────────────────┐
│  [统计卡片1]    [统计卡片2]    [统计卡片3]    [统计卡片4]     │
├─────────────────────────────────────┬───────────────────────┤
│                                     │                       │
│       7 天趋势图（双 Y 轴）          │    快速启动区域        │
│       占 2/3 宽度                   │    - 任务下拉选择      │
│                                     │    - 启动按钮         │
│                                     │                       │
├─────────────────────────────────────┴───────────────────────┤
│                      最近执行记录列表（5条）                  │
└─────────────────────────────────────────────────────────────┘
```

## 3. 数据结构

```typescript
// Dashboard 统计数据
interface DashboardStats {
  totalTasks: number        // 总任务数
  totalRuns: number         // 总执行次数
  successRate: number       // 成功率 (0-100)
  todayRuns: number         // 今日执行次数
}

// 7 天趋势数据点
interface TrendDataPoint {
  date: string              // 日期 "MM-DD"
  runs: number              // 执行次数
  successRate: number       // 成功率 (0-100)
}

// 最近执行记录
interface RecentRun {
  id: string
  task_name: string
  status: 'success' | 'failed' | 'running'
  started_at: string
  duration_ms: number
}
```

## 4. 组件设计

### 4.1 组件结构

```
Dashboard/
├── StatCard.tsx          # 统计卡片组件
├── TrendChart.tsx        # 7 天趋势图（双 Y 轴）
├── QuickStart.tsx        # 快速启动区域
├── RecentRuns.tsx        # 最近执行记录列表
└── index.ts              # 导出
```

### 4.2 StatCard 统计卡片

- 4 个卡片：总任务数、总执行次数、成功率、今日执行
- 使用浅灰背景 (#F9FAFB)，圆角 8px
- 图标 + 标题 + 数值的简洁布局
- 成功率卡片底部显示微小的变化趋势（如 "↑ 5% 较上周"）

### 4.3 TrendChart 趋势图

使用 **Recharts** 的 `ComposedChart` 实现：
- X 轴：日期（最近 7 天）
- 左 Y 轴：执行次数（柱状图，蓝色）
- 右 Y 轴：成功率（折线图，绿色）
- 鼠标悬停显示 Tooltip

### 4.4 QuickStart 快速启动

```
┌─────────────────────┐
│ 🚀 快速启动          │
│                     │
│ [选择任务 ▼]        │
│                     │
│ [    启动执行    ]  │
└─────────────────────┘
```

- 任务下拉选择器（只显示 status='ready' 的任务）
- 启动按钮使用主色调（蓝色）
- 点击后调用 `/api/runs` POST 接口，然后跳转到执行监控页

### 4.5 RecentRuns 最近执行记录

```
┌─────────────────────────────────────────────────────────────┐
│ 📋 最近执行记录                                    查看全部 → │
├─────────────────────────────────────────────────────────────┤
│ 任务名称          状态      执行时间        耗时             │
├─────────────────────────────────────────────────────────────┤
│ 登录测试          ✓ 成功    10:30:25       12.5s            │
│ 表单提交          ✗ 失败    09:15:00       8.3s             │
│ 搜索功能          ● 运行中  08:45:12       -                │
│ ...                                                         │
└─────────────────────────────────────────────────────────────┘
```

- 5 条记录，按时间倒序
- 状态使用 StatusBadge 组件（复用现有）
- 点击行跳转到 `/reports/:id`
- 右上角"查看全部"链接跳转到 `/reports`

## 5. Mock 数据

创建 `frontend/src/api/mock/dashboard.ts`：

```typescript
export const mockDashboardStats: DashboardStats
export const mockTrendData: TrendDataPoint[]
export const mockRecentRuns: RecentRun[]
```

## 6. 交互行为

| 操作 | 行为 |
|------|------|
| 点击快速启动按钮 | POST /api/runs → 跳转到 /runs/:id |
| 点击最近执行记录行 | 跳转到 /reports/:id |
| 点击"查看全部" | 跳转到 /reports |

## 7. 依赖

| 依赖 | 用途 |
|------|------|
| Recharts | 趋势图绑制 |
| useTasks Hook | 获取任务列表（快速启动下拉） |
| StatusBadge | 状态显示（复用现有组件） |
