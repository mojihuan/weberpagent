"""Tests for EventManager cleanup, heartbeat cancellation, publish isolation, and
_finalize_run integration.

Tests MEM-01 (cleanup removes run data), MEM-02 (heartbeat task cancellation on
re-subscribe), ERR-01 (publish per-queue exception isolation). Also verifies
_finalize_run calls event_manager.cleanup(run_id) (MEM-01).
"""

import asyncio
import logging
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


class TestEventManagerPublish:
    """Unit tests for EventManager publish() per-queue exception isolation.

    ERR-01: A failing subscriber queue must not prevent other subscribers
    from receiving events. publish() must isolate each queue.put() in try/except.
    """

    @pytest.mark.asyncio
    async def test_publish_isolates_bad_queue(self) -> None:
        """publish() must not raise when one queue fails — other queues still receive events.

        ERR-01: If one subscriber queue raises on put(), the event must still
        be delivered to all other healthy queues, and publish must return normally.
        """
        mgr = EventManager()
        run_id = "run-err"

        # Create two queues for the same run
        good_queue: asyncio.Queue = asyncio.Queue()
        bad_queue: asyncio.Queue = asyncio.Queue()

        # Register both as subscribers
        mgr._subscribers[run_id] = [bad_queue, good_queue]

        # Make bad_queue.put raise by replacing it with a mock
        bad_queue.put = AsyncMock(side_effect=RuntimeError("queue closed"))  # type: ignore[assignment]

        # Act — should not raise despite bad_queue failing
        await mgr.publish(run_id, "test-event")

        # Assert: good_queue still received the event
        received = await asyncio.wait_for(good_queue.get(), timeout=1.0)
        assert received == "test-event"

    @pytest.mark.asyncio
    async def test_publish_logs_bad_queue_error(self, caplog: pytest.LogCaptureFixture) -> None:
        """publish() must log a warning when a queue fails.

        ERR-01: When a subscriber queue raises during put(), a warning should
        be logged so operators can diagnose subscription issues.
        """
        mgr = EventManager()
        run_id = "run-log"

        bad_queue: asyncio.Queue = asyncio.Queue()
        mgr._subscribers[run_id] = [bad_queue]
        bad_queue.put = AsyncMock(side_effect=RuntimeError("queue broken"))  # type: ignore[assignment]

        with caplog.at_level(logging.WARNING, logger="backend.core.event_manager"):
            await mgr.publish(run_id, "event")

        # Assert: a warning was logged about the failed queue
        assert any("Failed to put event" in record.message for record in caplog.records)
