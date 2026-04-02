"""Report generation service."""

import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.repository import (
    RunRepository,
    StepRepository,
    ReportRepository,
    AssertionResultRepository,
    PreconditionResultRepository,
)
from backend.db.models import Report

logger = logging.getLogger(__name__)


class ReportService:
    """Report generation service.

    Generates comprehensive test reports including:
    - Basic statistics (status, step counts, duration)
    - Step details (actions, screenshots, errors)
    - Assertion results (pass/fail, messages)
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.run_repo = RunRepository(session)
        self.step_repo = StepRepository(session)
        self.report_repo = ReportRepository(session)
        self.assertion_result_repo = AssertionResultRepository(session)
        self.precondition_result_repo = PreconditionResultRepository(session)

    async def generate_report(self, run_id: str) -> Optional[Report]:
        """Generate a comprehensive test report for a run.

        Args:
            run_id: The run ID to generate report for

        Returns:
            Created Report object, or None if run not found
        """
        # Get run info
        run = await self.run_repo.get(run_id)
        if not run:
            logger.warning(f"Run {run_id} not found for report generation")
            return None

        # Get task info
        task = run.task if run.task else None
        task_name = task.name if task else "Unknown"

        # Get steps
        steps = await self.run_repo.get_steps(run_id)
        total_steps = len(steps)
        success_steps = sum(1 for s in steps if s.status == "success")
        failed_steps = sum(1 for s in steps if s.status == "failed")

        # Calculate duration
        duration_ms = 0
        if run.started_at and run.finished_at:
            duration_ms = int((run.finished_at - run.started_at).total_seconds() * 1000)

        # Determine overall status
        # Check assertion results for final status
        assertion_results = await self.assertion_result_repo.list_by_run(run_id)
        all_assertions_passed = (
            all(ar.status == "pass" for ar in assertion_results)
            if assertion_results
            else True
        )

        final_status = "success" if run.status == "success" and all_assertions_passed else "failed"

        # Create report
        report = await self.report_repo.create(
            run_id=run_id,
            task_id=run.task_id,
            task_name=task_name,
            status=final_status,
            total_steps=total_steps,
            success_steps=success_steps,
            failed_steps=failed_steps,
            duration_ms=duration_ms,
        )

        logger.info(f"Generated report {report.id} for run {run_id}")
        return report

    async def get_report_data(self, run_id: str) -> Optional[dict]:
        """Get full report data including steps and assertions.

        This method returns a dict with all report details for API response.

        Args:
            run_id: The run ID

        Returns:
            Dict with report data, or None if not found
        """
        report = await self.report_repo.get_by_run_id(run_id)
        if not report:
            return None

        # Get steps
        steps = await self.run_repo.get_steps(run_id)

        # Get assertion results
        assertion_results = await self.assertion_result_repo.list_by_run(run_id)

        # Separate UI assertions from API assertions
        ui_assertion_results = [
            ar for ar in assertion_results
            if not ar.assertion_id.startswith("api_")
        ]
        api_assertion_results = [
            ar for ar in assertion_results
            if ar.assertion_id.startswith("api_")
        ]

        # Calculate pass rate
        pass_rate = self.calculate_pass_rate(assertion_results)
        api_pass_rate = self.calculate_pass_rate(api_assertion_results) if api_assertion_results else "N/A"

        # Phase 59: Build timeline_items
        precondition_results = await self.precondition_result_repo.list_by_run(run_id)

        timeline_items: list[dict] = []

        # Add UI steps
        for s in steps:
            timeline_items.append({
                "type": "step",
                "id": s.id,
                "sequence_number": s.sequence_number if s.sequence_number is not None else s.step_index,
                "step_index": s.step_index,
                "action": s.action,
                "reasoning": s.reasoning,
                "screenshot_url": f"/api/runs/{run_id}/screenshots/{s.step_index}" if s.screenshot_path else None,
                "status": s.status,
                "error": s.error,
                "duration_ms": s.duration_ms,
            })

        # Add precondition results
        for pr in precondition_results:
            timeline_items.append({
                "type": "precondition",
                "id": pr.id,
                "sequence_number": pr.sequence_number,
                "index": pr.index,
                "code": pr.code,
                "status": pr.status,
                "error": pr.error,
                "duration_ms": pr.duration_ms,
                "variables": pr.variables,  # JSON string, frontend deserializes
            })

        # Add UI assertion results
        for ar in ui_assertion_results:
            timeline_items.append({
                "type": "assertion",
                "id": ar.id,
                "sequence_number": ar.sequence_number if ar.sequence_number is not None else 0,
                "assertion_id": ar.assertion_id,
                "assertion_name": None,
                "status": ar.status,
                "message": ar.message,
                "actual_value": ar.actual_value,
                "field_results": None,
                "duration_ms": None,
            })

        # Add API assertion results (group field rows by assertion index)
        api_assertion_groups: dict[str, list] = {}
        for ar in api_assertion_results:
            parts = ar.assertion_id.split("_")
            group_key = f"{parts[0]}_{parts[1]}" if len(parts) >= 2 and parts[0] == "api" else ar.assertion_id
            if group_key not in api_assertion_groups:
                api_assertion_groups[group_key] = []
            api_assertion_groups[group_key].append(ar)

        for group_key, field_rows in api_assertion_groups.items():
            first = field_rows[0]
            seq_num = first.sequence_number if first.sequence_number is not None else 0
            field_results = [
                {
                    "field_name": row.assertion_id.split("_", 2)[-1] if "_" in row.assertion_id.split("_", 1)[-1] else row.assertion_id,
                    "expected": None,
                    "actual": row.actual_value,
                    "passed": row.status == "pass",
                    "message": row.message or "",
                    "assertion_type": "api",
                }
                for row in field_rows
            ]
            all_passed = all(row.status == "pass" for row in field_rows)
            timeline_items.append({
                "type": "assertion",
                "id": first.id,
                "sequence_number": seq_num,
                "assertion_id": first.assertion_id,
                "assertion_name": None,
                "status": "pass" if all_passed else "fail",
                "message": first.message,
                "actual_value": first.actual_value,
                "field_results": field_results,
                "duration_ms": None,
            })

        # Sort by sequence_number
        timeline_items.sort(key=lambda x: x["sequence_number"])

        return {
            "report": report,
            "steps": steps,
            "assertion_results": assertion_results,
            "ui_assertion_results": ui_assertion_results,
            "api_assertion_results": api_assertion_results,
            "pass_rate": pass_rate,
            "api_pass_rate": api_pass_rate,
            "precondition_results": None,  # legacy
            "timeline_items": timeline_items,
        }

    @staticmethod
    def calculate_pass_rate(assertion_results: list) -> str:
        """Calculate assertion pass rate as formatted string.

        Args:
            assertion_results: List of AssertionResult objects

        Returns:
            Formatted string like "75% (3/4)"
        """
        if not assertion_results:
            return "N/A (0/0)"

        total = len(assertion_results)
        passed = sum(1 for ar in assertion_results if ar.status == "pass")
        percentage = int((passed / total) * 100) if total > 0 else 0

        return f"{percentage}% ({passed}/{total})"
