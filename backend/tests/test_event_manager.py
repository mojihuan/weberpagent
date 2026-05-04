"""Tests for EventManager cleanup, heartbeat cancellation, and _finalize_run integration.

Tests MEM-01 (cleanup removes run data) and MEM-02 (heartbeat task cancellation on
re-subscribe). Also verifies _finalize_run calls event_manager.cleanup(run_id) (MEM-01).
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.core.event_manager import EventManager


class TestEventManager:
    """Unit tests for EventManager cleanup and heartbeat behavior."""

    def test_cleanup_removes_all_run_data(self) -> None:
        """cleanup(run_id) must remove the run from _events, _subscribers, _status, and _heartbeat_tasks.

        MEM-01: After cleanup, no references to the run_id should remain in any
        internal dict, preventing memory leaks from accumulated run data.
        """
        mgr = EventManager()
        run_id = "test-run"

        # Populate all internal dicts
        mgr._events[run_id].append("event1")
        mgr._subscribers[run_id].append(asyncio.Queue())
        mgr._status[run_id] = "success"
        mgr._heartbeat_tasks[run_id] = MagicMock()

        # Act
        mgr.cleanup(run_id)

        # Assert: all dicts should no longer contain the run_id
        assert run_id not in mgr._events
        assert run_id not in mgr._subscribers
        assert run_id not in mgr._status
        assert run_id not in mgr._heartbeat_tasks

    @pytest.mark.asyncio
    async def test_subscribe_cancels_old_heartbeat(self) -> None:
        """Re-subscribing to the same run_id must cancel the previous heartbeat task.

        MEM-02: When a client disconnects and reconnects to the same run, the old
        heartbeat asyncio.Task must be cancelled before a new one is created.
        Without this, old tasks accumulate and consume resources.

        We test this by manually calling the subscribe() method's setup logic
        (the part before the first yield) and verifying the old task is cancelled.
        """
        mgr = EventManager(heartbeat_interval=9999)
        run_id = "run-1"
        mgr.set_status(run_id, "running")

        # First subscription: drive the generator to create the first heartbeat task
        gen1 = mgr.subscribe(run_id)

        # Advance the generator: the first __anext__ triggers the setup code
        # (queue creation, subscriber registration, heartbeat task creation)
        # then yields the first history event (none in this case) or blocks.
        # Since _events is empty, it goes straight to the while-loop and blocks.
        # We need to unblock it: publish an event so gen1.__anext__ returns.
        asyncio.get_event_loop().call_soon(
            lambda: asyncio.ensure_future(mgr._subscribers[run_id][0].put(":test\n\n"))
        )
        _ = await gen1.__anext__()

        # Capture the first heartbeat task
        first_task = mgr._heartbeat_tasks.get(run_id)
        assert first_task is not None, "First heartbeat task should exist"
        assert not first_task.done(), "First heartbeat task should be running"

        # Now subscribe again for the same run_id
        # The subscribe() generator creates a new queue and heartbeat task.
        # The implementation should cancel the old task before creating the new one.
        gen2 = mgr.subscribe(run_id)

        # Schedule an event so gen2.__anext__ returns
        asyncio.get_event_loop().call_soon(
            lambda: asyncio.ensure_future(mgr._subscribers[run_id][-1].put(":test2\n\n"))
        )
        _ = await gen2.__anext__()

        # Allow event loop to process any pending cancellation
        await asyncio.sleep(0.05)

        assert first_task.cancelled(), (
            "Old heartbeat task must be cancelled when re-subscribing"
        )

        # Clean up
        mgr.set_status(run_id, "success")

    @pytest.mark.asyncio
    async def test_finalize_run_calls_cleanup(self) -> None:
        """_finalize_run must call event_manager.cleanup(run_id) after report generation.

        MEM-01: The pipeline must clean up EventManager resources when a run finishes,
        otherwise _events dict grows without bound across multiple runs.
        """
        from backend.api.routes.run_pipeline import _finalize_run

        run_id = "finalize-test"

        mock_run_repo = AsyncMock()
        mock_report_service = AsyncMock()

        mock_em = MagicMock()
        mock_em.publish = AsyncMock()
        mock_em.set_status = MagicMock()
        mock_em.cleanup = MagicMock()

        with patch("backend.api.routes.run_pipeline.event_manager", mock_em):
            await _finalize_run(
                run_id=run_id,
                final_status="success",
                step_count=5,
                run_repo=mock_run_repo,
                report_service=mock_report_service,
            )

            # Verify cleanup was called with the correct run_id
            mock_em.cleanup.assert_called_once_with(run_id)
