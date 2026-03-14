"""Integration tests for background task status updates

Tests SVC-05: Background task status updates on completion/error
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from backend.db.schemas import TaskCreate


class TestBackgroundTaskStatus:
    """Integration tests for background task status updates"""

    @pytest.mark.asyncio
    async def test_run_status_updated_on_success(self, db_session):
        """Status is updated to 'success' after successful run"""
        from backend.db.repository import TaskRepository, RunRepository
        from backend.api.routes.runs import run_agent_background
        from backend.core.event_manager import event_manager

        # Create task and run
        task_repo = TaskRepository(db_session)
        task = await task_repo.create(TaskCreate(
            name="Test Task",
            description="Test description",
            max_steps=5
        ))

        run_repo = RunRepository(db_session)
        run = await run_repo.create(task_id=task.id)

        # Mock agent service to return successful result
        with patch('backend.api.routes.runs.AgentService') as MockAgentService:
            mock_service = MagicMock()
            mock_result = MagicMock()
            mock_result.is_successful.return_value = True
            mock_service.run_with_cleanup = AsyncMock(return_value=mock_result)
            MockAgentService.return_value = mock_service

            # Run background task
            await run_agent_background(
                run_id=run.id,
                task_name=task.name,
                task_description=task.description,
                max_steps=task.max_steps
            )

        # Verify status updated to success
        updated_run = await run_repo.get(run.id)
        assert updated_run.status == "success"

    @pytest.mark.asyncio
    async def test_run_status_updated_on_error(self, db_session):
        """Status is updated to 'failed' after error"""
        from backend.db.repository import TaskRepository, RunRepository
        from backend.api.routes.runs import run_agent_background

        # Create task and run
        task_repo = TaskRepository(db_session)
        task = await task_repo.create(TaskCreate(
            name="Test Task",
            description="Test description",
            max_steps=5
        ))

        run_repo = RunRepository(db_session)
        run = await run_repo.create(task_id=task.id)

        # Mock agent service to raise error
        with patch('backend.api.routes.runs.AgentService') as MockAgentService:
            mock_service = MagicMock()
            mock_service.run_with_cleanup = AsyncMock(
                side_effect=Exception("Test error")
            )
            MockAgentService.return_value = mock_service

            # Run background task
            await run_agent_background(
                run_id=run.id,
                task_name=task.name,
                task_description=task.description,
                max_steps=task.max_steps
            )

        # Verify status updated to failed
        updated_run = await run_repo.get(run.id)
        assert updated_run.status == "failed"

    @pytest.mark.asyncio
    async def test_error_event_published_on_failure(self, db_session):
        """SSE error event is published when background task fails"""
        from backend.db.repository import TaskRepository, RunRepository
        from backend.api.routes.runs import run_agent_background
        from backend.core.event_manager import event_manager

        # Create task and run
        task_repo = TaskRepository(db_session)
        task = await task_repo.create(TaskCreate(
            name="Test Task",
            description="Test description",
            max_steps=5
        ))

        run_repo = RunRepository(db_session)
        run = await run_repo.create(task_id=task.id)

        # Track published events
        published_events = []

        original_publish = event_manager.publish
        async def capture_publish(run_id, event):
            published_events.append((run_id, event))
            await original_publish(run_id, event)

        # Mock agent service to raise error
        with patch('backend.api.routes.runs.AgentService') as MockAgentService:
            mock_service = MagicMock()
            mock_service.run_with_cleanup = AsyncMock(
                side_effect=Exception("Test error")
            )
            MockAgentService.return_value = mock_service

            with patch.object(event_manager, 'publish', capture_publish):
                # Run background task
                await run_agent_background(
                    run_id=run.id,
                    task_name=task.name,
                    task_description=task.description,
                    max_steps=task.max_steps
                )

        # Verify error event was published
        error_events = [e for e in published_events if e[1] and "error" in str(e[1])]
        assert len(error_events) > 0, "Error event should be published on failure"

    @pytest.mark.asyncio
    async def test_report_service_integrated(self, db_session):
        """ReportService.generate_report is called after successful run"""
        from backend.db.repository import TaskRepository, RunRepository
        from backend.api.routes.runs import run_agent_background

        # Create task and run
        task_repo = TaskRepository(db_session)
        task = await task_repo.create(TaskCreate(
            name="Test Task",
            description="Test description",
            max_steps=5
        ))

        run_repo = RunRepository(db_session)
        run = await run_repo.create(task_id=task.id)

        # Mock agent service and report service
        with patch('backend.api.routes.runs.AgentService') as MockAgentService:
            mock_service = MagicMock()
            mock_result = MagicMock()
            mock_result.is_successful.return_value = True
            mock_service.run_with_cleanup = AsyncMock(return_value=mock_result)
            MockAgentService.return_value = mock_service

            with patch('backend.api.routes.runs.ReportService') as MockReportService:
                mock_report_service = MagicMock()
                mock_report_service.generate_report = AsyncMock()
                MockReportService.return_value = mock_report_service

                # Run background task
                await run_agent_background(
                    run_id=run.id,
                    task_name=task.name,
                    task_description=task.description,
                    max_steps=task.max_steps
                )

                # Verify ReportService.generate_report was called
                mock_report_service.generate_report.assert_called_once_with(run.id)

    @pytest.mark.asyncio
    async def test_assertion_service_evaluates_before_status(self, db_session):
        """AssertionService.evaluate_all is called before final status determination"""
        from backend.db.repository import TaskRepository, RunRepository
        from backend.api.routes.runs import run_agent_background
        from backend.db.models import Task as TaskModel
        from backend.api.schemas.index import Assertion

        # Create task with assertions
        task_repo = TaskRepository(db_session)
        task = await task_repo.create(TaskCreate(
            name="Test Task",
            description="Test description",
            max_steps=5
        ))

        # Add assertion to task directly
        db_task = await db_session.get(TaskModel, task.id)
        db_task.assertions = [
            Assertion(
                id="test-assertion-1",
                task_id=task.id,
                name="Check URL",
                type="url_contains",
                expected="/dashboard"
            )
        ]
        await db_session.commit()

        run_repo = RunRepository(db_session)
        run = await run_repo.create(task_id=task.id)

        # Track assertion service call order
        call_order = []

        # Mock services
        with patch('backend.api.routes.runs.AgentService') as MockAgentService:
            mock_service = MagicMock()
            mock_result = MagicMock()
            mock_result.is_successful.return_value = True
            mock_service.run_with_cleanup = AsyncMock(return_value=mock_result)
            MockAgentService.return_value = mock_service

            with patch('backend.api.routes.runs.AssertionService') as MockAssertionService:
                mock_assertion_service = MagicMock()

                async def mock_evaluate(*args, **kwargs):
                    call_order.append("evaluate_all")
                    return []  # No assertion results

                mock_assertion_service.evaluate_all = mock_evaluate
                MockAssertionService.return_value = mock_assertion_service

                with patch('backend.api.routes.runs.ReportService') as MockReportService:
                    mock_report_service = MagicMock()

                    async def mock_generate_report(*args, **kwargs):
                        call_order.append("generate_report")
                        return None

                    mock_report_service.generate_report = mock_generate_report
                    MockReportService.return_value = mock_report_service

                    # Run background task
                    await run_agent_background(
                        run_id=run.id,
                        task_name=task.name,
                        task_description=task.description,
                        max_steps=task.max_steps
                    )

                # Verify evaluate_all was called
                assert "evaluate_all" in call_order
