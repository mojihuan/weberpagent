# 删除前端 Mock 数据 - 实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 删除前端所有 mock 数据，将 Dashboard 和 Reports 模块接入真实后端 API

**Architecture:** Reports 作为独立实体存储，Run 完成时自动生成；Dashboard 实时聚合计算统计数据

**Tech Stack:** Python 3.11, FastAPI, SQLAlchemy, SQLite, React 18, TypeScript

---

## Phase 1: Reports 后端模块

### Task 1.1: 添加 Report 数据库模型

**Files:**
- Modify: `backend/db/models.py:67`

**Step 1: 添加 Report 模型**

在 `Step` 类之后添加：

```python
class Report(Base):
    """报告模型"""
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    run_id: Mapped[str] = mapped_column(String(8), ForeignKey("runs.id"), unique=True, nullable=False)
    task_id: Mapped[str] = mapped_column(String(8), ForeignKey("tasks.id"), nullable=False)
    task_name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # success, failed
    total_steps: Mapped[int] = mapped_column(Integer, default=0)
    success_steps: Mapped[int] = mapped_column(Integer, default=0)
    failed_steps: Mapped[int] = mapped_column(Integer, default=0)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # 关系
    run: Mapped["Run"] = relationship("Run", backref="report", uselist=False)
```

**Step 2: 验证模型加载**

Run: `python -c "from backend.db.models import Report; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add backend/db/models.py
git commit -m "feat(db): 添加 Report 模型"
```

---

### Task 1.2: 添加 Report Schemas

**Files:**
- Modify: `backend/db/schemas.py:110`

**Step 1: 添加 Report schemas**

在文件末尾添加：

```python
# === Report Schemas ===

class ReportResponse(BaseModel):
    """报告响应"""
    id: str
    run_id: str
    task_id: str
    task_name: str
    status: str
    total_steps: int
    success_steps: int
    failed_steps: int
    duration_ms: int
    created_at: datetime

    class Config:
        from_attributes = True


class ReportDetailResponse(ReportResponse):
    """报告详情响应（包含 steps）"""
    steps: List[StepResponse] = []


class ReportListParams(BaseModel):
    """报告列表查询参数"""
    status: Optional[str] = None  # success, failed, all
    date: Optional[str] = None    # today, 7days, 30days
    page: int = 1
    page_size: int = 10
```

**Step 2: 验证 schemas 加载**

Run: `python -c "from backend.db.schemas import ReportResponse; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add backend/db/schemas.py
git commit -m "feat(schemas): 添加 Report 相关 schemas"
```

---

### Task 1.3: 添加 ReportRepository

**Files:**
- Modify: `backend/db/repository.py:124`

**Step 1: 添加导入**

在文件顶部导入区添加：

```python
from sqlalchemy import func, and_
from datetime import timedelta
```

**Step 2: 添加 ReportRepository 类**

在文件末尾添加：

```python
class ReportRepository:
    """报告仓库"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        run_id: str,
        task_id: str,
        task_name: str,
        status: str,
        total_steps: int,
        success_steps: int,
        failed_steps: int,
        duration_ms: int,
    ) -> "Report":
        """创建报告"""
        from backend.db.models import Report
        report = Report(
            run_id=run_id,
            task_id=task_id,
            task_name=task_name,
            status=status,
            total_steps=total_steps,
            success_steps=success_steps,
            failed_steps=failed_steps,
            duration_ms=duration_ms,
        )
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def get(self, report_id: str) -> Optional["Report"]:
        from backend.db.models import Report
        return await self.session.get(Report, report_id)

    async def get_by_run_id(self, run_id: str) -> Optional["Report"]:
        """根据 run_id 获取报告"""
        from backend.db.models import Report
        stmt = select(Report).where(Report.run_id == run_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        status: Optional[str] = None,
        date: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[List["Report"], int]:
        """获取报告列表（支持筛选和分页）"""
        from backend.db.models import Report

        stmt = select(Report)

        # 状态筛选
        if status and status != "all":
            stmt = stmt.where(Report.status == status)

        # 日期筛选
        if date:
            now = datetime.now()
            if date == "today":
                start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif date == "7days":
                start = now - timedelta(days=7)
            elif date == "30days":
                start = now - timedelta(days=30)
            else:
                start = None
            if start:
                stmt = stmt.where(Report.created_at >= start)

        # 统计总数
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.session.execute(count_stmt)).scalar()

        # 分页
        stmt = stmt.order_by(Report.created_at.desc())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.session.execute(stmt)
        reports = list(result.scalars())

        return reports, total
```

**Step 3: 验证 repository 加载**

Run: `python -c "from backend.db.repository import ReportRepository; print('OK')"`
Expected: `OK`

**Step 4: Commit**

```bash
git add backend/db/repository.py
git commit -m "feat(repo): 添加 ReportRepository"
```

---

### Task 1.4: 创建 Reports API 路由

**Files:**
- Create: `backend/api/routes/reports.py`

**Step 1: 创建 reports.py**

```python
"""报告管理路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db
from backend.db.repository import ReportRepository, StepRepository
from backend.db.schemas import ReportResponse, ReportDetailResponse, StepResponse


router = APIRouter(prefix="/reports", tags=["reports"])


def get_report_repo(db: AsyncSession = Depends(get_db)) -> ReportRepository:
    return ReportRepository(db)


def get_step_repo(db: AsyncSession = Depends(get_step_repo)) -> StepRepository:
    return StepRepository(db)


@router.get("", response_model=dict)
async def list_reports(
    status: str = Query(default="all"),
    date: str = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    report_repo: ReportRepository = Depends(get_report_repo),
):
    """获取报告列表"""
    reports, total = await report_repo.list(
        status=status,
        date=date,
        page=page,
        page_size=page_size,
    )
    return {
        "reports": [ReportResponse.model_validate(r) for r in reports],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{report_id}", response_model=ReportDetailResponse)
async def get_report(
    report_id: str,
    report_repo: ReportRepository = Depends(get_report_repo),
    step_repo: StepRepository = Depends(get_step_repo),
):
    """获取报告详情"""
    report = await report_repo.get(report_id)
    if not report:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Report not found")

    # 获取关联的 steps
    steps = await step_repo.list_by_run(report.run_id)
    step_responses = [
        StepResponse(
            id=s.id,
            run_id=s.run_id,
            step_index=s.step_index,
            action=s.action,
            reasoning=s.reasoning,
            screenshot_url=f"/api/runs/{s.run_id}/screenshots/{s.step_index}" if s.screenshot_path else None,
            status=s.status,
            error=s.error,
            duration_ms=s.duration_ms,
            created_at=s.created_at,
        )
        for s in steps
    ]

    return ReportDetailResponse(
        id=report.id,
        run_id=report.run_id,
        task_id=report.task_id,
        task_name=report.task_name,
        status=report.status,
        total_steps=report.total_steps,
        success_steps=report.success_steps,
        failed_steps=report.failed_steps,
        duration_ms=report.duration_ms,
        created_at=report.created_at,
        steps=step_responses,
    )
```

**Step 2: 修复 StepRepository 依赖**

修复 `get_step_repo` 函数定义：

```python
def get_step_repo(db: AsyncSession = Depends(get_db)) -> StepRepository:
    return StepRepository(db)
```

**Step 3: 注册路由到 main.py**

修改 `backend/api/main.py`，在导入区添加：

```python
from backend.api.routes import tasks, runs, reports
```

在路由注册区添加：

```python
app.include_router(reports.router, prefix="/api")
```

**Step 4: 验证 API 加载**

Run: `python -c "from backend.api.main import app; print('OK')"`
Expected: `OK`

**Step 5: Commit**

```bash
git add backend/api/routes/reports.py backend/api/main.py
git commit -m "feat(api): 添加 Reports API 路由"
```

---

### Task 1.5: 在 Run 完成时生成 Report

**Files:**
- Modify: `backend/api/routes/runs.py:119-130`

**Step 1: 添加导入**

在 `runs.py` 文件顶部添加：

```python
from backend.db.repository import TaskRepository, RunRepository, StepRepository, ReportRepository
```

**Step 2: 修改 run_agent_background 函数**

在发送 `finished` 事件后（约第 129 行），添加生成报告的逻辑：

```python
            # 生成报告
            try:
                # 统计步骤数据
                steps = await run_repo.session.execute(
                    select(Step).where(Step.run_id == run_id)
                )
                steps_list = list(steps.scalars())
                total_steps = len(steps_list)
                success_steps = sum(1 for s in steps_list if s.status == "success")
                failed_steps = total_steps - success_steps

                # 计算时长
                run = await run_repo.get(run_id)
                duration_ms = 0
                if run.started_at and run.finished_at:
                    duration_ms = int((run.finished_at - run.started_at).total_seconds() * 1000)

                # 创建报告
                report_repo = ReportRepository(run_repo.session)
                await report_repo.create(
                    run_id=run_id,
                    task_id=run.task_id,
                    task_name=task_name,
                    status=final_status,
                    total_steps=total_steps,
                    success_steps=success_steps,
                    failed_steps=failed_steps,
                    duration_ms=duration_ms,
                )
                logger.info(f"[{run_id}] 已生成报告")
            except Exception as e:
                logger.error(f"[{run_id}] 生成报告失败: {e}")
```

**Step 3: 添加必要的导入**

在 `runs.py` 顶部添加：

```python
from sqlalchemy import select
from backend.db.models import Step
```

**Step 4: Commit**

```bash
git add backend/api/routes/runs.py
git commit -m "feat(runs): Run 完成时自动生成 Report"
```

---

### Task 1.6: 重建数据库（应用新表）

**Step 1: 备份现有数据（可选）**

```bash
cp backend/data/database.db backend/data/database.db.bak
```

**Step 2: 删除旧数据库并重建**

```bash
rm backend/data/database.db
python -c "
from backend.db.database import engine, Base
from backend.db.models import Task, Run, Step, Report
import asyncio

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Database initialized')

asyncio.run(init_db())
"
```

Expected: `Database initialized`

**Step 3: 验证表结构**

Run: `sqlite3 backend/data/database.db ".tables"`
Expected: `reports  runs  steps  tasks`

---

## Phase 2: Dashboard 后端模块

### Task 2.1: 创建 Dashboard API 路由

**Files:**
- Create: `backend/api/routes/dashboard.py`

**Step 1: 创建 dashboard.py**

```python
"""仪表盘路由"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from backend.db import get_db
from backend.db.models import Task, Run, Step


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    """获取仪表盘数据"""

    # 1. 统计数据
    total_tasks = (await db.execute(select(func.count(Task.id)))).scalar()
    total_runs = (await db.execute(select(func.count(Run.id)))).scalar()

    success_runs = (await db.execute(
        select(func.count(Run.id)).where(Run.status == "success")
    )).scalar()
    success_rate = round((success_runs / total_runs * 100), 1) if total_runs > 0 else 0

    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_runs = (await db.execute(
        select(func.count(Run.id)).where(Run.created_at >= today_start)
    )).scalar()

    stats = {
        "totalTasks": total_tasks,
        "totalRuns": total_runs,
        "successRate": success_rate,
        "todayRuns": today_runs,
    }

    # 2. 趋势数据（最近 7 天）
    trend_data = []
    for i in range(6, -1, -1):
        date = datetime.now() - timedelta(days=i)
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date_start + timedelta(days=1)

        runs_count = (await db.execute(
            select(func.count(Run.id)).where(
                Run.created_at >= date_start,
                Run.created_at < date_end
            )
        )).scalar()

        success_count = (await db.execute(
            select(func.count(Run.id)).where(
                Run.created_at >= date_start,
                Run.created_at < date_end,
                Run.status == "success"
            )
        )).scalar()

        rate = round((success_count / runs_count * 100), 1) if runs_count > 0 else 0
        trend_data.append({
            "date": date.strftime("%m-%d"),
            "runs": runs_count,
            "successRate": rate,
        })

    # 3. 最近执行（5 条）
    recent_runs_result = await db.execute(
        select(Run, Task.name.label("task_name"))
        .join(Task, Run.task_id == Task.id)
        .order_by(Run.created_at.desc())
        .limit(5)
    )

    recent_runs = []
    for row in recent_runs_result:
        run = row[0]
        task_name = row[1]
        duration_ms = 0
        if run.started_at and run.finished_at:
            duration_ms = int((run.finished_at - run.started_at).total_seconds() * 1000)
        recent_runs.append({
            "id": run.id,
            "task_name": task_name,
            "status": run.status,
            "started_at": run.started_at.isoformat() if run.started_at else run.created_at.isoformat(),
            "duration_ms": duration_ms,
        })

    return {
        "stats": stats,
        "trendData": trend_data,
        "recentRuns": recent_runs,
    }
```

**Step 2: 注册路由到 main.py**

修改 `backend/api/main.py`：

```python
from backend.api.routes import tasks, runs, reports, dashboard
```

```python
app.include_router(dashboard.router, prefix="/api")
```

**Step 3: 验证 API 加载**

Run: `python -c "from backend.api.main import app; print('OK')"`
Expected: `OK`

**Step 4: Commit**

```bash
git add backend/api/routes/dashboard.py backend/api/main.py
git commit -m "feat(api): 添加 Dashboard API 路由"
```

---

## Phase 3: 前端改造

### Task 3.1: 创建 Dashboard API 客户端

**Files:**
- Create: `frontend/src/api/dashboard.ts`

**Step 1: 创建 dashboard.ts**

```typescript
import { apiClient } from './client'
import type { DashboardStats, TrendDataPoint, RecentRun } from '../types'

export interface DashboardResponse {
  stats: DashboardStats
  trendData: TrendDataPoint[]
  recentRuns: RecentRun[]
}

export async function getDashboard(): Promise<DashboardResponse> {
  return apiClient<DashboardResponse>('/dashboard')
}
```

**Step 2: Commit**

```bash
git add frontend/src/api/dashboard.ts
git commit -m "feat(frontend): 添加 Dashboard API 客户端"
```

---

### Task 3.2: 创建 Reports API 客户端

**Files:**
- Create: `frontend/src/api/reports.ts`

**Step 1: 创建 reports.ts**

```typescript
import { apiClient } from './client'
import type { Report, Run, Step } from '../types'

interface ReportListResponse {
  reports: Report[]
  total: number
  page: number
  page_size: number
}

interface ReportDetail extends Report {
  steps: Step[]
}

export interface ReportsParams {
  status?: 'success' | 'failed' | 'all'
  date?: 'today' | '7days' | '30days'
  page?: number
  pageSize?: number
}

export async function getReports(params: ReportsParams = {}): Promise<ReportListResponse> {
  const query = new URLSearchParams()
  if (params.status) query.set('status', params.status)
  if (params.date) query.set('date', params.date)
  if (params.page) query.set('page', String(params.page))
  if (params.pageSize) query.set('page_size', String(params.pageSize))
  return apiClient<ReportListResponse>(`/reports?${query}`)
}

export async function getReport(reportId: string): Promise<ReportDetail> {
  return apiClient<ReportDetail>(`/reports/${reportId}`)
}
```

**Step 2: Commit**

```bash
git add frontend/src/api/reports.ts
git commit -m "feat(frontend): 添加 Reports API 客户端"
```

---

### Task 3.3: 改造 useDashboard hook

**Files:**
- Modify: `frontend/src/hooks/useDashboard.ts`

**Step 1: 简化 useDashboard.ts**

替换整个文件内容：

```typescript
import { useState, useEffect } from 'react'
import type { DashboardStats, TrendDataPoint, RecentRun } from '../types'
import { getDashboard } from '../api/dashboard'

interface DashboardData {
  stats: DashboardStats
  trendData: TrendDataPoint[]
  recentRuns: RecentRun[]
}

export function useDashboard() {
  const [data, setData] = useState<DashboardData>({
    stats: { totalTasks: 0, totalRuns: 0, successRate: 0, todayRuns: 0 },
    trendData: [],
    recentRuns: [],
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchDashboard() {
      setLoading(true)
      setError(null)
      try {
        const result = await getDashboard()
        setData(result)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch dashboard')
      } finally {
        setLoading(false)
      }
    }

    fetchDashboard()
  }, [])

  return {
    ...data,
    loading,
    error,
  }
}
```

**Step 2: Commit**

```bash
git add frontend/src/hooks/useDashboard.ts
git commit -m "refactor(hooks): useDashboard 使用真实 API"
```

---

### Task 3.4: 改造 useReports hook

**Files:**
- Modify: `frontend/src/hooks/useReports.ts`

**Step 1: 简化 useReports.ts**

替换整个文件内容：

```typescript
import { useState, useEffect, useCallback } from 'react'
import { getReports } from '../api/reports'
import type { Report } from '../types'
import type { ReportFiltersState } from '../components/Report'

interface UseReportsReturn {
  reports: Report[]
  total: number
  loading: boolean
  error: string | null
  filters: ReportFiltersState
  page: number
  pageSize: number
  setPage: (page: number) => void
  updateFilter: <K extends keyof ReportFiltersState>(
    key: K,
    value: ReportFiltersState[K]
  ) => void
  refresh: () => void
}

export function useReports(): UseReportsReturn {
  const [reports, setReports] = useState<Report[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filters, setFilters] = useState<ReportFiltersState>({
    status: 'all',
    dateRange: 'all',
  })
  const [page, setPage] = useState(1)
  const pageSize = 10

  const fetchReports = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await getReports({
        status: filters.status,
        date: filters.dateRange === 'all' ? undefined : filters.dateRange,
        page,
        pageSize,
      })
      setReports(result.reports)
      setTotal(result.total)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch reports')
    } finally {
      setLoading(false)
    }
  }, [filters, page])

  useEffect(() => {
    fetchReports()
  }, [fetchReports])

  useEffect(() => {
    setPage(1)
  }, [filters])

  const updateFilter = <K extends keyof ReportFiltersState>(
    key: K,
    value: ReportFiltersState[K]
  ) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }

  return {
    reports,
    total,
    loading,
    error,
    filters,
    page,
    pageSize,
    setPage,
    updateFilter,
    refresh: fetchReports,
  }
}
```

**Step 2: Commit**

```bash
git add frontend/src/hooks/useReports.ts
git commit -m "refactor(hooks): useReports 使用真实 API"
```

---

### Task 3.5: 简化 tasks.ts（移除 mock 分支）

**Files:**
- Modify: `frontend/src/api/tasks.ts`

**Step 1: 简化 tasks.ts**

替换整个文件内容：

```typescript
import type { Task, CreateTaskDto, UpdateTaskDto, Run } from '../types'
import { apiClient } from './client'

export const tasksApi = {
  async list(params?: { status?: string; search?: string }): Promise<Task[]> {
    const query = new URLSearchParams()
    if (params?.status && params.status !== 'all') {
      query.set('status', params.status)
    }
    if (params?.search) {
      query.set('search', params.search)
    }
    const queryString = query.toString()
    return apiClient<Task[]>(queryString ? `/tasks?${queryString}` : '/tasks')
  },

  async get(id: string): Promise<Task | null> {
    return apiClient<Task>(`/tasks/${id}`)
  },

  async create(data: CreateTaskDto): Promise<Task> {
    return apiClient<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  async update(id: string, data: UpdateTaskDto): Promise<Task> {
    return apiClient<Task>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  },

  async delete(id: string): Promise<void> {
    return apiClient<void>(`/tasks/${id}`, { method: 'DELETE' })
  },

  async batchDelete(ids: string[]): Promise<void> {
    await Promise.all(ids.map(id => apiClient<void>(`/tasks/${id}`, { method: 'DELETE' })))
  },

  async batchUpdateStatus(ids: string[], status: 'draft' | 'ready'): Promise<void> {
    await Promise.all(ids.map(id =>
      apiClient<void>(`/tasks/${id}`, {
        method: 'PUT',
        body: JSON.stringify({ status }),
      })
    ))
  },

  async getRuns(taskId: string): Promise<Run[]> {
    return apiClient<Run[]>(`/tasks/${taskId}/runs`)
  },

  async getStats(taskId: string) {
    return apiClient<{ date: string; runs: number; successRate: number }[]>(`/tasks/${taskId}/stats`)
  },
}
```

**Step 2: Commit**

```bash
git add frontend/src/api/tasks.ts
git commit -m "refactor(api): 移除 tasks.ts mock 分支"
```

---

### Task 3.6: 后端补充 tasks 查询参数

**Files:**
- Modify: `backend/api/routes/tasks.py:18-22`

**Step 1: 添加查询参数支持**

修改 `list_tasks` 函数：

```python
@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    status: str = Query(default=None),
    search: str = Query(default=None),
    repo: TaskRepository = Depends(get_task_repo),
):
    return await repo.list(status=status, search=search)
```

**Step 2: 添加 Query 导入**

```python
from fastapi import APIRouter, Depends, HTTPException, Query
```

**Step 3: 修改 TaskRepository.list 方法**

修改 `backend/db/repository.py` 中的 `TaskRepository.list` 方法：

```python
async def list(self, status: Optional[str] = None, search: Optional[str] = None) -> List[Task]:
    stmt = select(Task)
    if status:
        stmt = stmt.where(Task.status == status)
    if search:
        search_pattern = f"%{search}%"
        stmt = stmt.where(
            (Task.name.ilike(search_pattern)) | (Task.description.ilike(search_pattern))
        )
    stmt = stmt.order_by(Task.created_at.desc())
    result = await self.session.execute(stmt)
    return list(result.scalars())
```

**Step 4: Commit**

```bash
git add backend/api/routes/tasks.py backend/db/repository.py
git commit -m "feat(api): tasks 支持 status 和 search 查询参数"
```

---

## Phase 4: 清理 Mock 文件

### Task 4.1: 删除 mock 目录

**Step 1: 删除整个 mock 目录**

```bash
rm -rf frontend/src/api/mock
```

**Step 2: 验证构建**

Run: `cd frontend && npm run build`
Expected: 无错误

**Step 3: Commit**

```bash
git add -A
git commit -m "chore: 删除前端 mock 数据"
```

---

### Task 4.2: 最终验证

**Step 1: 启动后端**

```bash
cd /Users/huhu/project/weberpagent
source .venv/bin/activate
uvicorn backend.api.main:app --reload --port 8080
```

**Step 2: 启动前端**

```bash
cd frontend && npm run dev
```

**Step 3: 验证功能**

- [ ] Dashboard 页面加载正常
- [ ] Reports 页面加载正常（含分页、筛选）
- [ ] Tasks 页面 CRUD 正常
- [ ] Runs 执行和监控正常

---

## 完成标记

```bash
git add docs/plans/2026-03-13-remove-mock-data-impl.md
git commit -m "docs: 添加删除 mock 数据实施计划"
```
