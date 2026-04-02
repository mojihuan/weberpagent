"""报告管理路由"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db
from backend.db.repository import ReportRepository
from backend.db.schemas import ReportResponse, ReportDetailResponse, StepResponse, AssertionResultResponse
from backend.core.report_service import ReportService


router = APIRouter(prefix="/reports", tags=["reports"])


def get_report_repo(db: AsyncSession = Depends(get_db)) -> ReportRepository:
    return ReportRepository(db)


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
    db: AsyncSession = Depends(get_db),
):
    """获取报告详情

    支持通过 report_id 或 run_id 查询报告。
    优先使用 report_id，如果未找到则尝试使用 run_id。
    """
    report_repo = ReportRepository(db)
    report = await report_repo.get(report_id)

    # If not found by report_id, try by run_id
    if not report:
        report = await report_repo.get_by_run_id(report_id)

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Use ReportService for complete data
    report_service = ReportService(db)
    data = await report_service.get_report_data(report.run_id)

    if not data:
        raise HTTPException(status_code=404, detail="Report data not found")

    # Transform steps
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
        for s in data["steps"]
    ]

    # Transform assertion results
    def transform_assertion_results(results):
        return [
            AssertionResultResponse(
                id=ar.id,
                run_id=ar.run_id,
                assertion_id=ar.assertion_id,
                status=ar.status,
                message=ar.message,
                actual_value=ar.actual_value,
                created_at=ar.created_at,
            )
            for ar in results
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
        assertion_results=transform_assertion_results(data["assertion_results"]),
        ui_assertion_results=transform_assertion_results(data["ui_assertion_results"]),
        pass_rate=data["pass_rate"],
        precondition_results=data.get("precondition_results"),
        timeline_items=data.get("timeline_items"),
    )
