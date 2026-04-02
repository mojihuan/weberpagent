"""Tests for PreconditionResultRepository."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.repository import (
    PreconditionResultRepository,
    RunRepository,
    TaskRepository,
)
from backend.db.schemas import TaskCreate


class TestPreconditionResultRepository:
    """Tests for PreconditionResultRepository."""

    @pytest.fixture
    async def task_repo(self, db_session: AsyncSession) -> TaskRepository:
        return TaskRepository(db_session)

    @pytest.fixture
    async def run_repo(self, db_session: AsyncSession) -> RunRepository:
        return RunRepository(db_session)

    @pytest.fixture
    async def precondition_result_repo(
        self, db_session: AsyncSession
    ) -> PreconditionResultRepository:
        return PreconditionResultRepository(db_session)

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

    async def test_create_stores_precondition_result_with_all_fields(
        self,
        db_session: AsyncSession,
        precondition_result_repo: PreconditionResultRepository,
        setup_run,
    ):
        """create() stores PreconditionResult with all fields."""
        run_id = setup_run["run"].id

        result = await precondition_result_repo.create(
            run_id=run_id,
            sequence_number=1,
            index=0,
            code="response = requests.get(base_url)",
            status="success",
            duration_ms=150,
            variables='{"status_code": 200}',
        )

        assert result.id is not None
        assert result.run_id == run_id
        assert result.sequence_number == 1
        assert result.index == 0
        assert result.code == "response = requests.get(base_url)"
        assert result.status == "success"
        assert result.duration_ms == 150
        assert result.variables == '{"status_code": 200}'
        assert result.error is None
        assert result.created_at is not None

    async def test_create_with_error_fields(
        self,
        db_session: AsyncSession,
        precondition_result_repo: PreconditionResultRepository,
        setup_run,
    ):
        """create() stores PreconditionResult with error fields."""
        run_id = setup_run["run"].id

        result = await precondition_result_repo.create(
            run_id=run_id,
            sequence_number=2,
            index=1,
            code="response.raise_for_status()",
            status="failed",
            error="Connection refused",
            duration_ms=50,
        )

        assert result.status == "failed"
        assert result.error == "Connection refused"

    async def test_list_by_run_returns_rows_ordered_by_sequence_number(
        self,
        db_session: AsyncSession,
        precondition_result_repo: PreconditionResultRepository,
        setup_run,
    ):
        """list_by_run() returns results ordered by sequence_number."""
        run_id = setup_run["run"].id

        # Insert in reverse order
        r3 = await precondition_result_repo.create(
            run_id=run_id, sequence_number=3, index=2, code="c3", status="success"
        )
        r1 = await precondition_result_repo.create(
            run_id=run_id, sequence_number=1, index=0, code="c1", status="success"
        )
        r2 = await precondition_result_repo.create(
            run_id=run_id, sequence_number=2, index=1, code="c2", status="success"
        )

        results = await precondition_result_repo.list_by_run(run_id)

        assert len(results) == 3
        assert results[0].sequence_number == 1
        assert results[1].sequence_number == 2
        assert results[2].sequence_number == 3

    async def test_list_by_run_returns_empty_for_nonexistent_run(
        self,
        db_session: AsyncSession,
        precondition_result_repo: PreconditionResultRepository,
    ):
        """list_by_run() returns empty list for non-existent run_id."""
        results = await precondition_result_repo.list_by_run("nonexistent")
        assert results == []
