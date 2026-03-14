"""Unit tests for browser cleanup pattern

Tests FND-05: Browser cleanup pattern implementation
"""
import pytest
import logging
from unittest.mock import patch, MagicMock, AsyncMock


class TestAgentServiceCleanup:
    """Tests for browser cleanup pattern in AgentService"""

    @pytest.mark.asyncio
    async def test_run_with_cleanup_calls_run_with_streaming(self):
        """run_with_cleanup() delegates to run_with_streaming()"""
        from backend.core.agent_service import AgentService

        service = AgentService()

        with patch.object(service, 'run_with_streaming', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = MagicMock(is_successful=lambda: True)

            result = await service.run_with_cleanup(
                task="Test task",
                run_id="test-run-1",
                on_step=lambda *args: None,
                max_steps=5,
                llm_config=None
            )

            mock_run.assert_called_once_with(
                task="Test task",
                run_id="test-run-1",
                on_step=mock_run.call_args[1]['on_step'],
                max_steps=5,
                llm_config=None
            )

    @pytest.mark.asyncio
    async def test_run_with_cleanup_logs_on_success(self, caplog):
        """run_with_cleanup() logs success message"""
        from backend.core.agent_service import AgentService

        service = AgentService()

        with patch.object(service, 'run_with_streaming', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = MagicMock(is_successful=lambda: True)

            with caplog.at_level(logging.INFO):
                await service.run_with_cleanup(
                    task="Test task",
                    run_id="test-run-2",
                    on_step=lambda *args: None
                )

            assert any("completed successfully" in record.message for record in caplog.records)
            assert any("cleanup complete" in record.message for record in caplog.records)

    @pytest.mark.asyncio
    async def test_run_with_cleanup_logs_on_error(self, caplog):
        """run_with_cleanup() logs error message on exception"""
        from backend.core.agent_service import AgentService

        service = AgentService()

        with patch.object(service, 'run_with_streaming', new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = RuntimeError("Test error")

            with caplog.at_level(logging.ERROR):
                with pytest.raises(RuntimeError):
                    await service.run_with_cleanup(
                        task="Test task",
                        run_id="test-run-3",
                        on_step=lambda *args: None
                    )

            assert any("failed with error" in record.message for record in caplog.records if record.levelno >= logging.ERROR)

    @pytest.mark.asyncio
    async def test_run_with_cleanup_finally_always_logs(self, caplog):
        """run_with_cleanup() always logs cleanup in finally block"""
        from backend.core.agent_service import AgentService

        service = AgentService()

        # Test with success
        with patch.object(service, 'run_with_streaming', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = MagicMock(is_successful=lambda: True)

            with caplog.at_level(logging.INFO):
                await service.run_with_cleanup(
                    task="Test task",
                    run_id="test-run-4a",
                    on_step=lambda *args: None
                )

            assert any("cleanup complete" in record.message for record in caplog.records)

        caplog.clear()

        # Test with exception
        with patch.object(service, 'run_with_streaming', new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = RuntimeError("Test error")

            with caplog.at_level(logging.INFO):
                with pytest.raises(RuntimeError):
                    await service.run_with_cleanup(
                        task="Test task",
                        run_id="test-run-4b",
                        on_step=lambda *args: None
                    )

            assert any("cleanup complete" in record.message for record in caplog.records)

    @pytest.mark.asyncio
    async def test_run_with_cleanup_reraises_exception(self):
        """run_with_cleanup() re-raises exceptions for caller to handle"""
        from backend.core.agent_service import AgentService

        service = AgentService()

        with patch.object(service, 'run_with_streaming', new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = ValueError("Test value error")

            with pytest.raises(ValueError, match="Test value error"):
                await service.run_with_cleanup(
                    task="Test task",
                    run_id="test-run-5",
                    on_step=lambda *args: None
                )


class TestRunAgentBackgroundWiring:
    """Tests for run_agent_background using cleanup pattern"""

    @pytest.mark.asyncio
    async def test_run_agent_background_uses_cleanup_pattern(self):
        """run_agent_background uses run_with_cleanup for background tasks"""
        from backend.api.routes.runs import run_agent_background

        with patch('backend.api.routes.runs.AgentService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.run_with_cleanup = AsyncMock(
                return_value=MagicMock(is_successful=lambda: True)
            )

            # Call the background function (matches actual signature)
            await run_agent_background(
                run_id="test-run",
                task_name="Test Task",
                task_description="Test task description",
                max_steps=10
            )

            # Verify run_with_cleanup was called (not run_with_streaming)
            mock_service.run_with_cleanup.assert_called_once()
