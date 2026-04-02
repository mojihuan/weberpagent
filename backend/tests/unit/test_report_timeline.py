"""Tests for report_service.get_report_data() timeline_items field."""

import json
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.report_service import ReportService
from backend.db.models import Task, Run, Step, Assertion, AssertionResult
from backend.db.repository import (
    AssertionResultRepository,
    PreconditionResultRepository,
    ReportRepository,
    RunRepository,
    TaskRepository,
)


class TestReportTimeline:
    """Tests for timeline_items construction in report_service."""

    @pytest.fixture
    async def report_service(self, db_session: AsyncSession) -> ReportService:
        return ReportService(db_session)

    @pytest.fixture
    async def setup_data(self, db_session: AsyncSession):
        """Create task, run, step, assertion, assertion_result, report."""
        # Task
        task = Task(name="Timeline Test", description="Test")
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        # Assertion
        assertion = Assertion(
            task_id=task.id,
            name="Check URL",
            type="url_contains",
            expected="dashboard",
        )
        db_session.add(assertion)
        await db_session.commit()
        await db_session.refresh(assertion)

        # Run
        run = Run(task_id=task.id, status="success")
        db_session.add(run)
        await db_session.commit()
        await db_session.refresh(run)

        # Step with sequence_number=2
        step = Step(
            run_id=run.id,
            step_index=0,
            action="Click login",
            status="success",
            sequence_number=2,
        )
        db_session.add(step)

        # PreconditionResult with sequence_number=1
        precon_repo = PreconditionResultRepository(db_session)
        precon_result = await precon_repo.create(
            run_id=run.id,
            sequence_number=1,
            index=0,
            code="setup()",
            status="success",
            duration_ms=100,
        )

        # AssertionResult with sequence_number=3
        assertion_repo = AssertionResultRepository(db_session)
        assertion_result = await assertion_repo.create(
            run_id=run.id,
            assertion_id=assertion.id,
            status="pass",
            message="URL matches",
            actual_value="https://example.com/dashboard",
            sequence_number=3,
        )

        # Report
        report_repo = ReportRepository(db_session)
        await report_repo.create(
            run_id=run.id,
            task_id=task.id,
            task_name=task.name,
            status="success",
            total_steps=1,
            success_steps=1,
            failed_steps=0,
            duration_ms=1000,
        )

        return {
            "task": task,
            "run": run,
            "step": step,
            "precon_result": precon_result,
            "assertion_result": assertion_result,
        }

    async def test_timeline_items_contains_all_three_types(
        self,
        db_session: AsyncSession,
        report_service: ReportService,
        setup_data,
    ):
        """timeline_items contains all three types."""
        run_id = setup_data["run"].id

        data = await report_service.get_report_data(run_id)

        assert data is not None
        assert "timeline_items" in data
        assert len(data["timeline_items"]) == 3

        types = [item["type"] for item in data["timeline_items"]]
        assert "precondition" in types
        assert "step" in types
        assert "assertion" in types

    async def test_timeline_items_sorted_by_sequence_number(
        self,
        db_session: AsyncSession,
        report_service: ReportService,
    ):
        """timeline_items are sorted by sequence_number ascending."""
        # Insert in reverse order: assertion(seq=3), step(seq=1), precondition(seq=2)
        task = Task(name="Sort Test", description="Test")
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        assertion = Assertion(
            task_id=task.id, name="Check", type="text_exists", expected="hello"
        )
        db_session.add(assertion)
        await db_session.commit()
        await db_session.refresh(assertion)

        run = Run(task_id=task.id, status="success")
        db_session.add(run)
        await db_session.commit()
        await db_session.refresh(run)

        # Step seq=1
        db_session.add(Step(
            run_id=run.id, step_index=0, action="Navigate", status="success", sequence_number=1
        ))
        # Precondition seq=2
        precon_repo = PreconditionResultRepository(db_session)
        await precon_repo.create(
            run_id=run.id, sequence_number=2, index=0, code="auth()", status="success"
        )
        # Assertion seq=3
        assertion_repo = AssertionResultRepository(db_session)
        await assertion_repo.create(
            run_id=run.id, assertion_id=assertion.id, status="pass",
            message="ok", sequence_number=3,
        )

        report_repo = ReportRepository(db_session)
        await report_repo.create(
            run_id=run.id, task_id=task.id, task_name=task.name,
            status="success", total_steps=1, success_steps=1, failed_steps=0, duration_ms=1000,
        )

        data = await report_service.get_report_data(run.id)
        items = data["timeline_items"]
        seq_numbers = [item["sequence_number"] for item in items]
        assert seq_numbers == sorted(seq_numbers)
        assert seq_numbers == [1, 2, 3]

    async def test_old_report_without_sequence_number_returns_timeline_with_fallback(
        self,
        db_session: AsyncSession,
        report_service: ReportService,
    ):
        """Old reports without sequence_number still produce timeline using fallback."""
        task = Task(name="Old Report", description="Test")
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        run = Run(task_id=task.id, status="success")
        db_session.add(run)
        await db_session.commit()
        await db_session.refresh(run)

        # Step WITHOUT sequence_number (simulates old data)
        db_session.add(Step(
            run_id=run.id, step_index=0, action="Old action", status="success"
        ))
        await db_session.commit()

        report_repo = ReportRepository(db_session)
        await report_repo.create(
            run_id=run.id, task_id=task.id, task_name=task.name,
            status="success", total_steps=1, success_steps=1, failed_steps=0, duration_ms=500,
        )

        data = await report_service.get_report_data(run.id)
        assert data is not None
        assert "timeline_items" in data
        assert len(data["timeline_items"]) >= 1
        # Fallback: sequence_number should use step_index (0)
        assert data["timeline_items"][0]["sequence_number"] == 0
        assert data["timeline_items"][0]["type"] == "step"
