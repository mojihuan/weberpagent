"""Report generation service."""

import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.repository import (
    RunRepository,
    StepRepository,
    ReportRepository,
    AssertionResultRepository,
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

        return {
            "report": report,
            "steps": steps,
            "assertion_results": assertion_results,
            "ui_assertion_results": ui_assertion_results,
            "api_assertion_results": api_assertion_results,
            "pass_rate": pass_rate,
            "api_pass_rate": api_pass_rate,
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
