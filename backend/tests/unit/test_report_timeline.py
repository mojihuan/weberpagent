"""Tests for report_service.get_report_data() timeline_items field."""

import json
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.report_service import ReportService
from backend.db.repository import (
    AssertionResultRepository,
    PreconditionResultRepository,
    ReportRepository,
    RunRepository,
    StepRepository,
    TaskRepository,
)
from backend.db.schemas import TaskCreate
from backend.db.models import Assertion


class TestReportTimeline:
    """Tests for timeline_items construction in report_service."""

    @pytest.fixture
    async def task_repo(self, db_session: AsyncSession) -> TaskRepository:
        return TaskRepository(db_session)

    @pytest.fixture
    async def run_repo(self, db_session: AsyncSession) -> RunRepository:
        return RunRepository(db_session)

    @pytest.fixture
    async def step_repo(self, db_session: AsyncSession) -> StepRepository:
        return StepRepository(db_session)

    @pytest.fixture
    async def report_repo(self, db_session: AsyncSession) -> ReportRepository:
        return ReportRepository(db_session)

    @pytest.fixture
    async def assertion_result_repo(
        self, db_session: AsyncSession
    ) -> AssertionResultRepository:
        return AssertionResultRepository(db_session)

    @pytest.fixture
    async def precondition_result_repo(
        self, db_session: AsyncSession
    ) -> PreconditionResultRepository:
        return PreconditionResultRepository(db_session)

    @pytest.fixture
    async def report_service(self, db_session: AsyncSession) -> ReportService:
        return ReportService(db_session)

    @pytest.fixture
    async def setup_run(
        self,
        db_session: AsyncSession,
        task_repo: TaskRepository,
        run_repo: RunRepository,
    ):
        """Create a task and run for testing."""
        task = await task_repo.create(TaskCreate(name="Test Task", description="Test"))
        run = await run_repo.create(task_id=task.id)
        return {"task": task, "run": run}

    async def test_timeline_items_contains_all_three_types(
        self,
        db_session: AsyncSession,
        report_service: ReportService,
        report_repo: ReportRepository,
        assertion_result_repo: AssertionResultRepository,
        precondition_result_repo: PreconditionResultRepository,
        setup_run,
    ):
        """timeline_items contains all three step types."""
        run_id = setup_run["run"].id
        task = setup_run["task"]

        # Create a precondition result (seq=1)
        await precondition_result_repo.create(
            run_id=run_id,
            sequence_number=1,
            index=0,
            code="base_url = 'http://example.com'",
            status="success",
            duration_ms=100,
        )

        # Create a step (seq=2)
        await db_session.execute(
            __import__("sqlalchemy").text(
                "INSERT INTO steps (id, run_id, step_index, action, status, sequence_number) "
                "VALUES ('step-1', :run_id, 1, 'Click login', 'success', 2)"
            ),
            {"run_id": run_id},
        )
        await db_session.commit()

        # Create an assertion (seq=3)
        assertion = Assertion(
            task_id=task.id, name="Check URL", type="url_contains", expected="dashboard"
        )
        db_session.add(assertion)
        await db_session.commit()
        await db_session.refresh(assertion)

        await assertion_result_repo.create(
            run_id=run_id,
            assertion_id=assertion.id,
            status="pass",
            message="URL matches",
            actual_value="https://example.com/dashboard",
            sequence_number=3,
        )

        # Generate report
        await report_repo.create(
            run_id=run_id,
            task_id=task.id,
            task_name=task.name,
            status="success",
            total_steps=1,
            success_steps=1,
            failed_steps=0,
            duration_ms=1000,
        )

        data = await report_service.get_report_data(run_id)

        assert data is not None
        assert "timeline_items" in data
        assert len(data["timeline_items"]) == 3

        types = [item["type"] for item in data["timeline_items"]]
        assert types == ["precondition", "step", "assertion"]

    async def test_timeline_items_sorted_by_sequence_number(
        self,
        db_session: AsyncSession,
        report_service: ReportService,
        report_repo: ReportRepository,
        assertion_result_repo: AssertionResultRepository,
        precondition_result_repo: PreconditionResultRepository,
        setup_run,
    ):
        """timeline_items are sorted by sequence_number ascending."""
        run_id = setup_run["run"].id
        task = setup_run["task"]

        # Insert in reverse order: assertion (seq=3), step (seq=1), precondition (seq=2)
        assertion = Assertion(
            task_id=task.id,
            name="Check text",
            type="text_exists",
            expected="Hello",
        )
        db_session.add(assertion)
        await db_session.commit()
        await db_session.refresh(assertion)

        await assertion_result_repo.create(
            run_id=run_id,
            assertion_id=assertion.id,
            status="pass",
            message="Text found",
            sequence_number=3,
        )

        await db_session.execute(
            __import__("sqlalchemy").text(
                "INSERT INTO steps (id, run_id, step_index, action, status, sequence_number) "
                "VALUES ('step-2', :run_id, 2, 'Navigate', 'success', 1)"
            ),
            {"run_id": run_id},
        )
        await db_session.commit()

        await precondition_result_repo.create(
            run_id=run_id,
            sequence_number=2,
            index=0,
            code="setup()",
            status="success",
        )

        await report_repo.create(
            run_id=run_id,
            task_id=task.id,
            task_name=task.name,
            status="success",
            total_steps=1,
            success_steps=1,
            failed_steps=0,
            duration_ms=1000,
        )

        data = await report_service.get_report_data(run_id)

        items = data["timeline_items"]
        seq_numbers = [item["sequence_number"] for item in items]
        assert seq_numbers == sorted(seq_numbers)
        assert seq_numbers == [1, 2, 3]

    async def test_old_report_without_sequence_number_returns_timeline_with_fallback(
        self,
        db_session: AsyncSession,
        report_service: ReportService,
        report_repo: ReportRepository,
        setup_run,
    ):
        """Old reports without sequence_number still produce timeline using fallback."""
        run_id = setup_run["run"].id
        task = setup_run["task"]

        # Create a step WITHOUT sequence_number (simulates old data)
        await db_session.execute(
            __import__("sqlalchemy").text(
                "INSERT INTO steps (id, run_id, step_index, action, status) "
                "VALUES ('step-old', :run_id, 0, 'Old action', 'success')"
            ),
            {"run_id": run_id},
        )
        await db_session.commit()

        await report_repo.create(
            run_id=run_id,
            task_id=task.id,
            task_name=task.name,
            status="success",
            total_steps=1,
            success_steps=1,
            failed_steps=0,
            duration_ms=500,
        )

        data = await report_service.get_report_data(run_id)

        assert data is not None
        assert "timeline_items" in data
        assert len(data["timeline_items"]) >= 1
        # Fallback: sequence_number should use step_index (0)
        assert data["timeline_items"][0]["sequence_number"] == 0
        assert data["timeline_items"][0]["type"] == "step"
