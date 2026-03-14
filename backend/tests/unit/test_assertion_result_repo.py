"""Tests for AssertionResultRepository."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.repository import AssertionResultRepository, RunRepository, TaskRepository
from backend.db.schemas import TaskCreate
from backend.db.models import Assertion, AssertionResult


class TestAssertionResultRepository:
    """Tests for AssertionResultRepository."""

    @pytest.fixture
    async def task_repo(self, db_session: AsyncSession) -> TaskRepository:
        return TaskRepository(db_session)

    @pytest.fixture
    async def run_repo(self, db_session: AsyncSession) -> RunRepository:
        return RunRepository(db_session)

    @pytest.fixture
    async def result_repo(self, db_session: AsyncSession) -> AssertionResultRepository:
        return AssertionResultRepository(db_session)

    @pytest.fixture
    async def setup_run(
        self, db_session: AsyncSession, task_repo: TaskRepository, run_repo: RunRepository
    ):
        """Create a task, assertion, and run for testing."""
        task = await task_repo.create(TaskCreate(name="Test Task", description="Test"))
        # Create an assertion directly in the session
        assertion = Assertion(
            task_id=task.id,
            name="Check URL",
            type="url_contains",
            expected="dashboard",
        )
        db_session.add(assertion)
        await db_session.commit()
        await db_session.refresh(assertion)
        run = await run_repo.create(task_id=task.id)
        return {"task": task, "assertion": assertion, "run": run}

    async def test_create_stores_assertion_result_with_all_fields(
        self,
        db_session: AsyncSession,
        result_repo: AssertionResultRepository,
        setup_run,
    ):
        """create() stores AssertionResult with all fields and returns ORM object."""
        run_id = setup_run["run"].id
        assertion_id = setup_run["assertion"].id

        result = await result_repo.create(
            run_id=run_id,
            assertion_id=assertion_id,
            status="pass",
            message="URL contains expected value",
            actual_value="https://example.com/dashboard",
        )

        assert result.id is not None
        assert result.run_id == run_id
        assert result.assertion_id == assertion_id
        assert result.status == "pass"
        assert result.message == "URL contains expected value"
        assert result.actual_value == "https://example.com/dashboard"
        assert result.created_at is not None

    async def test_create_with_minimal_fields(
        self,
        db_session: AsyncSession,
        result_repo: AssertionResultRepository,
        setup_run,
    ):
        """create() works with only required fields (status defaults handled)."""
        run_id = setup_run["run"].id
        assertion_id = setup_run["assertion"].id

        result = await result_repo.create(
            run_id=run_id,
            assertion_id=assertion_id,
            status="fail",
        )

        assert result.id is not None
        assert result.status == "fail"
        assert result.message is None
        assert result.actual_value is None

    async def test_list_by_run_returns_all_results_ordered_by_created_at(
        self,
        db_session: AsyncSession,
        result_repo: AssertionResultRepository,
        setup_run,
    ):
        """list_by_run() returns all AssertionResult objects for given run_id ordered by created_at."""
        run_id = setup_run["run"].id
        assertion_id = setup_run["assertion"].id

        # Create multiple results with small delays to ensure different created_at
        result1 = await result_repo.create(
            run_id=run_id,
            assertion_id=assertion_id,
            status="pass",
            message="First assertion passed",
        )

        result2 = await result_repo.create(
            run_id=run_id,
            assertion_id=assertion_id,
            status="fail",
            message="Second assertion failed",
        )

        result3 = await result_repo.create(
            run_id=run_id,
            assertion_id=assertion_id,
            status="pass",
            message="Third assertion passed",
        )

        # List results
        results = await result_repo.list_by_run(run_id)

        assert len(results) == 3
        # Results should be ordered by created_at ascending
        assert results[0].id == result1.id
        assert results[1].id == result2.id
        assert results[2].id == result3.id

    async def test_list_by_run_returns_empty_for_nonexistent_run(
        self,
        db_session: AsyncSession,
        result_repo: AssertionResultRepository,
    ):
        """list_by_run() returns empty list for non-existent run_id."""
        results = await result_repo.list_by_run("nonexistent")
        assert results == []

    async def test_list_by_run_only_returns_results_for_specified_run(
        self,
        db_session: AsyncSession,
        task_repo: TaskRepository,
        run_repo: RunRepository,
        result_repo: AssertionResultRepository,
    ):
        """list_by_run() only returns results for the specified run_id."""
        # Create two tasks and runs
        task1 = await task_repo.create(TaskCreate(name="Task 1", description="Test"))
        task2 = await task_repo.create(TaskCreate(name="Task 2", description="Test"))

        assertion1 = Assertion(
            task_id=task1.id,
            name="Assertion 1",
            type="url_contains",
            expected="dashboard",
        )
        db_session.add(assertion1)
        await db_session.commit()
        await db_session.refresh(assertion1)

        assertion2 = Assertion(
            task_id=task2.id,
            name="Assertion 2",
            type="text_exists",
            expected="Hello",
        )
        db_session.add(assertion2)
        await db_session.commit()
        await db_session.refresh(assertion2)

        run1 = await run_repo.create(task_id=task1.id)
        run2 = await run_repo.create(task_id=task2.id)

        # Create results for both runs
        await result_repo.create(
            run_id=run1.id,
            assertion_id=assertion1.id,
            status="pass",
            message="Run1 result",
        )
        await result_repo.create(
            run_id=run2.id,
            assertion_id=assertion2.id,
            status="fail",
            message="Run2 result",
        )

        # Get results for run1 only
        results = await result_repo.list_by_run(run1.id)

        assert len(results) == 1
        assert results[0].run_id == run1.id
        assert results[0].message == "Run1 result"
