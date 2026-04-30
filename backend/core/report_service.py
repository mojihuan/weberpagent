"""Report generation service."""

import json
import logging
from typing import Any, Optional

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


def _build_step_timeline_item(s: Any, run_id: str) -> dict:
    """Build a timeline item dict from a step object."""
    return {
        "type": "step", "id": s.id,
        "sequence_number": s.sequence_number if s.sequence_number is not None else s.step_index,
        "step_index": s.step_index, "action": s.action, "reasoning": s.reasoning,
        "screenshot_url": f"/api/runs/{run_id}/screenshots/{s.step_index}" if s.screenshot_path else None,
        "status": s.status, "error": s.error, "duration_ms": s.duration_ms,
    }


def _build_precondition_timeline_item(pr: Any) -> dict:
    """Build a timeline item dict from a precondition result."""
    return {
        "type": "precondition", "id": pr.id, "sequence_number": pr.sequence_number,
        "index": pr.index, "code": pr.code, "status": pr.status,
        "error": pr.error, "duration_ms": pr.duration_ms,
        "variables": json.loads(pr.variables) if pr.variables else None,
    }


def _build_assertion_timeline_item(ar: Any) -> dict:
    """Build a timeline item dict from an assertion result."""
    return {
        "type": "assertion", "id": ar.id,
        "sequence_number": ar.sequence_number if ar.sequence_number is not None else 0,
        "assertion_id": ar.assertion_id,
        "assertion_name": ar.assertion.name if ar.assertion else None,
        "status": ar.status, "message": ar.message, "actual_value": ar.actual_value,
        "field_results": None, "duration_ms": None,
    }


def _build_external_assertion_timeline_items(raw_results: str, run_id: str) -> list[dict]:
    """Parse external assertion results JSON and build timeline items."""
    try:
        ext_results = json.loads(raw_results)
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"Failed to parse external_assertion_results for run {run_id}: {e}")
        return []

    items = []
    for ext in ext_results:
        seq = ext.get("sequence_number", 0)
        items.append({
            "type": "assertion", "id": f"ext-{seq}", "sequence_number": seq,
            "assertion_id": f"ext-{seq}",
            "assertion_name": ext.get("assertion_name", "External Assertion"),
            "status": ext.get("status", "unknown"), "message": ext.get("message"),
            "actual_value": None, "field_results": ext.get("field_results"),
            "duration_ms": int(ext.get("duration", 0) * 1000) if ext.get("duration") else None,
        })
    return items


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
        """Get full report data including steps and assertions."""
        report = await self.report_repo.get_by_run_id(run_id)
        if not report:
            return None

        steps = await self.run_repo.get_steps(run_id)
        assertion_results = await self.assertion_result_repo.list_by_run(run_id)
        pass_rate = self.calculate_pass_rate(assertion_results)
        precondition_results = await self.precondition_result_repo.list_by_run(run_id)

        timeline_items: list[dict] = []
        for s in steps:
            timeline_items.append(_build_step_timeline_item(s, run_id))
        for pr in precondition_results:
            timeline_items.append(_build_precondition_timeline_item(pr))
        for ar in assertion_results:
            timeline_items.append(_build_assertion_timeline_item(ar))

        run_data = await self.run_repo.get(run_id)
        if run_data and run_data.external_assertion_results:
            timeline_items.extend(_build_external_assertion_timeline_items(run_data.external_assertion_results, run_id))

        timeline_items.sort(key=lambda x: x["sequence_number"])

        return {
            "report": report, "steps": steps, "assertion_results": assertion_results,
            "ui_assertion_results": assertion_results, "pass_rate": pass_rate,
            "precondition_results": None, "timeline_items": timeline_items,
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
