"""报告管理路由"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db
from backend.db.repository import ReportRepository, StepRepository
from backend.db.schemas import ReportResponse, ReportDetailResponse, StepResponse


router = APIRouter(prefix="/reports", tags=["reports"])


def get_report_repo(db: AsyncSession = Depends(get_db)) -> ReportRepository:
    return ReportRepository(db)


def get_step_repo(db: AsyncSession = Depends(get_db)) -> StepRepository:
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
            screenshot_url=f"/api/run/{s.run_id}/screenshots/{s.step_index}" if s.screenshot_path else None,
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
