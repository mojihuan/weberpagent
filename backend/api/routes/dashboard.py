"""仪表盘路由"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from backend.db import get_db
from backend.db.models import Task, Run


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
async def get_dashboard(db: AsyncSession = Depends(get_db)) -> dict:
    """获取仪表盘数据"""

    # 1. 统计数据
    total_tasks = (await db.execute(select(func.count(Task.id)))).scalar() or 0
    total_runs = (await db.execute(select(func.count(Run.id)))).scalar() or 0

    success_runs = (await db.execute(
        select(func.count(Run.id)).where(Run.status == "success")
    )).scalar() or 0
    success_rate = round((success_runs / total_runs * 100), 1) if total_runs > 0 else 0.0

    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_runs = (await db.execute(
        select(func.count(Run.id)).where(Run.created_at >= today_start)
    )).scalar() or 0

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
        )).scalar() or 0

        success_count = (await db.execute(
            select(func.count(Run.id)).where(
                Run.created_at >= date_start,
                Run.created_at < date_end,
                Run.status == "success"
            )
        )).scalar() or 0
        rate = round((success_count / runs_count * 100), 1) if runs_count > 0 else 0.0

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
