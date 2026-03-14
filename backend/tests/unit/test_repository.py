"""Tests for RunRepository.get_steps() method."""

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.main import app
from backend.db.repository import RunRepository, TaskRepository
from backend.db.schemas import TaskCreate


class TestRunRepositoryGetSteps:
    """Tests for RunRepository.get_steps() method."""

    @pytest.fixture
    async def task_repo(self, db_session: AsyncSession) -> TaskRepository:
        return TaskRepository(db_session)

    @pytest.fixture
    async def run_repo(self, db_session: AsyncSession) -> RunRepository:
        return RunRepository(db_session)

    async def test_get_steps_returns_steps_for_run(
        self, db_session: AsyncSession, task_repo: TaskRepository, run_repo: RunRepository
    ):
        """get_steps(run_id) returns list of Step objects for that run."""
        # Create task and run
        task = await task_repo.create(TaskCreate(name="Test Task", description="Test"))
        run = await run_repo.create(task_id=task.id)

        # Add steps
        await run_repo.add_step(run.id, {"step_index": 0, "action": "Click button", "status": "success"})
        await run_repo.add_step(run.id, {"step_index": 1, "action": "Type text", "status": "success"})

        # Get steps
        steps = await run_repo.get_steps(run.id)

        assert len(steps) == 2
        assert steps[0].action == "Click button"
        assert steps[1].action == "Type text"

    async def test_get_steps_ordered_by_step_index(
        self, db_session: AsyncSession, task_repo: TaskRepository, run_repo: RunRepository
    ):
        """Steps are ordered by step_index ascending."""
        # Create task and run
        task = await task_repo.create(TaskCreate(name="Test Task", description="Test"))
        run = await run_repo.create(task_id=task.id)

        # Add steps in reverse order
        await run_repo.add_step(run.id, {"step_index": 2, "action": "Third step", "status": "success"})
        await run_repo.add_step(run.id, {"step_index": 0, "action": "First step", "status": "success"})
        await run_repo.add_step(run.id, {"step_index": 1, "action": "Second step", "status": "success"})

        # Get steps - should be ordered by step_index
        steps = await run_repo.get_steps(run.id)

        assert len(steps) == 3
        assert steps[0].step_index == 0
        assert steps[1].step_index == 1
        assert steps[2].step_index == 2
        assert steps[0].action == "First step"
        assert steps[1].action == "Second step"
        assert steps[2].action == "Third step"

    async def test_get_steps_empty_for_nonexistent_run(
        self, db_session: AsyncSession, run_repo: RunRepository
    ):
        """Empty list returned for non-existent run_id."""
        steps = await run_repo.get_steps("nonexistent")
        assert steps == []

    async def test_get_steps_only_returns_steps_for_specified_run(
        self, db_session: AsyncSession, task_repo: TaskRepository, run_repo: RunRepository
    ):
        """Only steps for the specified run_id are returned."""
        # Create task and two runs
        task = await task_repo.create(TaskCreate(name="Test Task", description="Test"))
        run1 = await run_repo.create(task_id=task.id)
        run2 = await run_repo.create(task_id=task.id)

        # Add steps to both runs
        await run_repo.add_step(run1.id, {"step_index": 0, "action": "Run1 Step", "status": "success"})
        await run_repo.add_step(run2.id, {"step_index": 0, "action": "Run2 Step", "status": "success"})

        # Get steps for run1
        steps = await run_repo.get_steps(run1.id)

        assert len(steps) == 1
        assert steps[0].action == "Run1 Step"
        assert steps[0].run_id == run1.id
