# 删除前端 Mock 数据 - 设计文档

## 概述

删除前端所有 mock 数据，将 Dashboard 和 Reports 模块接入真实后端 API。

## 当前状态

| 模块 | Mock 文件 | 后端 API 状态 | 前端使用方式 |
|------|----------|-------------|-------------|
| Tasks | `mock/tasks.ts` | ✅ 已有 `/api/tasks` | `api/tasks.ts` 有 mock 分支 |
| Runs | `mock/runs.ts` | ✅ 已有 `/api/runs` | `api/runs.ts` 已用真实 API |
| Dashboard | `mock/dashboard.ts` | ❌ 缺失 | `useDashboard.ts` 有 mock 分支 |
| Reports | `mock/reports.ts` | ❌ 缺失 | `useReports.ts` 直接用 mock |

## 设计决策

1. **Dashboard 数据来源**：实时计算（从数据库聚合）
2. **Reports 设计**：独立实体（独立 reports 表）
3. **Report 生成时机**：Run 完成时在 `runs.py` 中直接创建
4. **实施策略**：分层渐进（按模块逐步实施验证）

---

## Phase 1: Reports 模块

### 1.1 数据库表结构

```sql
CREATE TABLE reports (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL UNIQUE,
    task_id TEXT NOT NULL,
    task_name TEXT NOT NULL,
    status TEXT NOT NULL,         -- success / failed
    total_steps INTEGER DEFAULT 0,
    success_steps INTEGER DEFAULT 0,
    failed_steps INTEGER DEFAULT 0,
    duration_ms INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,

    FOREIGN KEY (run_id) REFERENCES runs(id)
);
```

### 1.2 后端文件

| 文件 | 操作 |
|------|------|
| `backend/db/models.py` | 添加 Report 模型 |
| `backend/db/schemas.py` | 添加 ReportCreate, ReportResponse |
| `backend/db/repository.py` | 添加 ReportRepository |
| `backend/api/routes/reports.py` | 新增 |

### 1.3 API 端点

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/reports` | 列表（支持 status/date 分筛，分页） |
| GET | `/api/reports/{id}` | 详情（包含对应 run 的 steps） |

### 1.4 Run 完成时生成 Report

在 `runs.py` 的 `run_agent_background` 函数中，finished 事件发送后调用 `ReportRepository.create()`。

---

## Phase 2: Dashboard 模块

### 2.1 API 端点

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/dashboard` | 返回仪表盘所有数据 |

### 2.2 响应结构

```typescript
interface DashboardResponse {
  stats: {
    totalTasks: number
    totalRuns: number
    successRate: number
    todayRuns: number
  }
  trendData: Array<{
    date: string      // "03-07" 格式
    runs: number
    successRate: number
  }>
  recentRuns: Array<{
    id: string
    task_name: string
    status: string
    started_at: string
    duration_ms: number
  }>
}
```

### 2.3 后端文件

| 文件 | 操作 |
|------|------|
| `backend/api/routes/dashboard.py` | 新增 |

### 2.4 实时聚合逻辑

- `totalTasks` → `SELECT COUNT(*) FROM tasks`
- `totalRuns` → `SELECT COUNT(*) FROM runs`
- `successRate` → `SELECT COUNT(*) FROM runs WHERE status='success' / total`
- `todayRuns` → `SELECT COUNT(*) FROM runs WHERE date(started_at) = today`
- `trendData` → 按 `date(started_at)` 分组，统计最近 7 天
- `recentRuns` → `SELECT ... FROM runs ORDER BY started_at DESC LIMIT 5`

---

## Phase 3: 前端改造

### 3.1 修改文件

| 文件 | 改动 |
|------|------|
| `api/tasks.ts` | 删除 mock 分支，简化为纯 API 调用 |
| `hooks/useDashboard.ts` | 删除 mock 分支，调用 `/api/dashboard` |
| `hooks/useReports.ts` | 改为调用真实 API |
| `api/mock/runStream.ts` | 检查是否仍在使用 |

### 3.2 新增文件

| 文件 | 说明 |
|------|------|
| `api/reports.ts` | Reports API 调用 |
| `api/dashboard.ts` | Dashboard API 调用 |

### 3.3 后端需补充的查询参数

- `/api/tasks`: `?status=`, `?search=`
- `/api/reports`: `?status=`, `?date=`, `?page=`, `?page_size=`

---

## Phase 4: 清理

### 4.1 删除文件

```
frontend/src/api/mock/
├── index.ts
├── tasks.ts
├── runs.ts
├── dashboard.ts
├── reports.ts
└── runStream.ts
```

### 4.2 验证清单

- [ ] `npm run build` 无错误
- [ ] Dashboard 页面正常加载
- [ ] Reports 页面正常加载（含分页、筛选）
- [ ] Tasks 页面正常 CRUD
- [ ] Runs 页面正常执行和监控

---

## 文件变更总结

| Phase | 新增 | 修改 | 删除 |
|-------|------|------|------|
| 1 | +4 | 1 | 0 |
| 2 | +1 | 0 | 0 |
| 3 | +2 | 4 | 0 |
| 4 | 0 | 0 | -6 |
