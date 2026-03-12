# 报告查看功能设计文档

> 创建日期: 2026-03-09
> 阶段: Phase 5 - 报告查看功能

## 1. 概述

实现前端报告查看功能，包括报告列表页和报告详情页，使用 Mock 数据。

## 2. 页面设计

### 2.1 报告列表页 (`/reports`)

**布局**: 页面标题 + 筛选栏 + 表格 + 分页

**功能**:
- 状态筛选（全部/成功/失败）
- 日期范围筛选（今天、最近7天、最近30天）
- 表格列：任务名称、状态、步骤数、耗时、执行时间、操作
- 分页（每页 10 条）

**组件**:
- `ReportFilters.tsx` — 筛选栏
- `ReportTable.tsx` — 表格
- 复用: `StatusBadge`, `Pagination`, `EmptyState`

### 2.2 报告详情页 (`/reports/:id`)

**路由**: `/reports/:id`

**布局**:
```
┌─────────────────────────────────────────┐
│  Header: 任务名 + 状态 + 返回按钮         │
├─────────────────────────────────────────┤
│  摘要卡片（4个）                          │
│  总步骤 | 成功数 | 失败数 | 总耗时         │
├─────────────────────────────────────────┤
│  步骤列表（可展开）                       │
│  ▼ 步骤 1 - 打开页面    ✓  1.2s         │
│    ┌─────────────┬─────────────────┐    │
│    │   截图预览   │   AI 推理过程   │    │
│    │  (可点击放大) │                 │    │
│    └─────────────┴─────────────────┘    │
│  ▶ 步骤 2 - 填写表单    ✓  2.3s         │
└─────────────────────────────────────────┘
```

**组件**:
- `ReportHeader.tsx` — 顶部导航
- `SummaryCard.tsx` — 摘要卡片
- `StepItem.tsx` — 可展开的步骤项
- 复用: `StatusBadge`, `ImageViewer`

## 3. 数据结构

### Report 类型（已存在）
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

### 报告详情（复用 Run 类型）
报告详情直接使用 `Run` 类型，包含完整的 `Step[]` 信息。

## 4. 文件结构

```
frontend/src/
├── pages/
│   ├── Reports.tsx          # 报告列表页（重构）
│   └── ReportDetail.tsx     # 报告详情页（新增）
├── components/
│   └── Report/
│       ├── ReportFilters.tsx  # 筛选栏
│       ├── ReportTable.tsx    # 表格
│       ├── ReportHeader.tsx   # 详情页头部
│       ├── SummaryCard.tsx    # 摘要卡片
│       └── StepItem.tsx       # 可展开步骤项
├── api/mock/
│   └── reports.ts             # 报告 Mock 数据（新增）
└── types/
    └── index.ts               # 类型定义（已有）
```

## 5. 路由配置

```typescript
// App.tsx 添加路由
<Route path="/reports" element={<Reports />} />
<Route path="/reports/:id" element={<ReportDetail />} />
```

## 6. 依赖组件

复用现有组件:
- `StatusBadge` — 状态标签
- `Pagination` — 分页
- `EmptyState` — 空状态
- `ImageViewer` — 图片查看器

## 7. 实现顺序

1. 创建 Mock 数据 (`reports.ts`)
2. 实现报告列表页组件
3. 实现报告详情页组件
4. 配置路由
5. 测试验证
