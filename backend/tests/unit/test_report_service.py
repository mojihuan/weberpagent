"""Tests for ReportService."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.report_service import ReportService
from backend.db.repository import (
    RunRepository,
    TaskRepository,
    StepRepository,
    ReportRepository,
    AssertionResultRepository,
)
from backend.db.schemas import TaskCreate
from backend.db.models import Assertion


class TestReportService:
    """Tests for ReportService class."""

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
    async def assertion_result_repo(self, db_session: AsyncSession) -> AssertionResultRepository:
        return AssertionResultRepository(db_session)

    @pytest.fixture
    async def report_service(self, db_session: AsyncSession) -> ReportService:
        return ReportService(db_session)

    @pytest.fixture
    async def setup_completed_run(
        self,
        db_session: AsyncSession,
        task_repo: TaskRepository,
        run_repo: RunRepository,
        step_repo: StepRepository,
    ):
        """Create a completed run with steps for testing."""
        task = await task_repo.create(TaskCreate(name="Test Task", description="Test Description"))
        run = await run_repo.create(task_id=task.id)

        # Add steps
        await run_repo.add_step(
            run.id,
            {"step_index": 0, "action": "Click button", "status": "success"},
        )
        await run_repo.add_step(
            run.id,
            {"step_index": 1, "action": "Type text", "status": "success"},
        )
        await run_repo.add_step(
            run.id,
            {"step_index": 2, "action": "Submit form", "status": "failed", "error": "Timeout"},
        )

        # Update run status to completed
        run.status = "success"
        run.started_at = datetime.now() - timedelta(seconds=10)
        run.finished_at = datetime.now()
        await db_session.commit()
        await db_session.refresh(run)

        return {"task": task, "run": run}

    async def test_init_accepts_async_session(self, db_session: AsyncSession):
        """ReportService.__init__ accepts AsyncSession."""
        service = ReportService(db_session)
        assert service.session == db_session
        assert service.run_repo is not None
        assert service.step_repo is not None
        assert service.report_repo is not None
        assert service.assertion_result_repo is not None

    async def test_generate_report_creates_report_with_correct_statistics(
        self,
        db_session: AsyncSession,
        report_service: ReportService,
        setup_completed_run,
    ):
        """generate_report() creates Report with correct statistics."""
        run_id = setup_completed_run["run"].id
        task = setup_completed_run["task"]

        report = await report_service.generate_report(run_id)

        assert report is not None
        assert report.id is not None
        assert report.run_id == run_id
        assert report.task_id == task.id
        assert report.task_name == task.name
        assert report.total_steps == 3
        assert report.success_steps == 2
        assert report.failed_steps == 1
        assert report.duration_ms > 0

    async def test_generate_report_includes_step_details(
        self,
        db_session: AsyncSession,
        report_service: ReportService,
        setup_completed_run,
    ):
        """generate_report() includes all step details via get_report_data()."""
        run_id = setup_completed_run["run"].id

        # First generate the report
        await report_service.generate_report(run_id)

        # Then get full data
        data = await report_service.get_report_data(run_id)

        assert data is not None
        assert "report" in data
        assert "steps" in data
        assert len(data["steps"]) == 3
        assert data["steps"][0].action == "Click button"
        assert data["steps"][1].action == "Type text"
        assert data["steps"][2].action == "Submit form"

    async def test_generate_report_includes_assertion_results(
        self,
        db_session: AsyncSession,
        report_service: ReportService,
        assertion_result_repo: AssertionResultRepository,
        setup_completed_run,
    ):
        """generate_report() includes assertion results from AssertionResultRepository."""
        run_id = setup_completed_run["run"].id
        task = setup_completed_run["task"]

        # Create an assertion
        assertion = Assertion(
            task_id=task.id,
            name="Check URL",
            type="url_contains",
            expected="dashboard",
        )
        db_session.add(assertion)
        await db_session.commit()
        await db_session.refresh(assertion)

        # Create assertion results
        await assertion_result_repo.create(
            run_id=run_id,
            assertion_id=assertion.id,
            status="pass",
            message="URL contains expected value",
            actual_value="https://example.com/dashboard",
        )

        # Generate report and get data
        await report_service.generate_report(run_id)
        data = await report_service.get_report_data(run_id)

        assert data is not None
        assert "assertion_results" in data
        assert len(data["assertion_results"]) == 1
        assert data["assertion_results"][0].status == "pass"

    async def test_calculate_pass_rate_returns_correct_format(self):
        """calculate_pass_rate() returns correct percentage format '75% (3/4)'."""

        # Create mock assertion results
        class MockAssertionResult:
            def __init__(self, status: str):
                self.status = status

        # Test 75% pass rate
        results = [
            MockAssertionResult("pass"),
            MockAssertionResult("pass"),
            MockAssertionResult("pass"),
            MockAssertionResult("fail"),
        ]
        rate = ReportService.calculate_pass_rate(results)
        assert rate == "75% (3/4)"

        # Test 100% pass rate
        all_passed = [MockAssertionResult("pass"), MockAssertionResult("pass")]
        rate = ReportService.calculate_pass_rate(all_passed)
        assert rate == "100% (2/2)"

        # Test 0% pass rate
        all_failed = [MockAssertionResult("fail"), MockAssertionResult("fail")]
        rate = ReportService.calculate_pass_rate(all_failed)
        assert rate == "0% (0/2)"

        # Test empty list
        rate = ReportService.calculate_pass_rate([])
        assert rate == "N/A (0/0)"

    async def test_generate_report_returns_none_for_nonexistent_run(
        self,
        report_service: ReportService,
    ):
        """generate_report() returns None for non-existent run_id."""
        report = await report_service.generate_report("nonexistent")
        assert report is None

    async def test_get_report_data_returns_none_if_no_report(
        self,
        report_service: ReportService,
    ):
        """get_report_data() returns None if report doesn't exist."""
        data = await report_service.get_report_data("nonexistent")
        assert data is None
