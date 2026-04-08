"""Batch execution service with Semaphore-gated concurrency control"""

import asyncio
import logging
from datetime import datetime
from typing import Any

from backend.db.database import async_session
from backend.db.repository import BatchRepository, RunRepository
from backend.api.routes.runs import run_agent_background

logger = logging.getLogger(__name__)

MAX_CONCURRENCY = 4  # Hard cap per D-09

# Module-level registry to prevent GC of active services per RESEARCH Pitfall 5
_active_batches: dict[str, "BatchExecutionService"] = {}


class BatchExecutionService:
    """Coordinates parallel execution of multiple runs with Semaphore concurrency control.

    Per D-08: standalone service class for Semaphore, task scheduling, error isolation.
    Per D-09: asyncio.Semaphore default 2, hard limit 4.
    Per D-10: single task failure does not affect others.
    Per D-11: reuses existing run_agent_background for individual execution.
    """

    def __init__(self, batch_id: str, concurrency: int = 2):
        self.batch_id = batch_id
        effective_concurrency = min(concurrency, MAX_CONCURRENCY)
        self._semaphore = asyncio.Semaphore(effective_concurrency)
        self._tasks: list[asyncio.Task] = []

    async def start(self, run_configs: list[dict[str, Any]]) -> None:
        """Start all runs with semaphore-gated concurrency.

        Args:
            run_configs: List of dicts, each containing the kwargs for run_agent_background.
                         Required keys: run_id, task_id, task_name, task_description, max_steps
                         Optional keys: preconditions, external_assertions, target_url
        """
        _active_batches[self.batch_id] = self

        # Update batch status to running
        async with async_session() as session:
            repo = BatchRepository(session)
            await repo.update_status(self.batch_id, "running")

        logger.info(f"[Batch {self.batch_id}] Starting {len(run_configs)} runs with concurrency={self._semaphore._value}")

        # Create one asyncio.Task per run
        self._tasks = [
            asyncio.create_task(self._execute_run(config))
            for config in run_configs
        ]

        # Wait for all to complete (return_exceptions=True prevents one failure from canceling others)
        await asyncio.gather(*self._tasks, return_exceptions=True)

        # Finalize batch status
        await self._finalize_batch()

    async def _execute_run(self, config: dict[str, Any]) -> None:
        """Execute a single run under semaphore control.

        Per D-10: errors are caught and logged but do not propagate.
        The run_agent_background function already handles its own error recording.
        """
        async with self._semaphore:
            run_id = config.get("run_id", "unknown")
            try:
                logger.info(f"[Batch {self.batch_id}] Run {run_id} starting (semaphore acquired)")
                await run_agent_background(**config)
                logger.info(f"[Batch {self.batch_id}] Run {run_id} completed")
            except Exception as e:
                # Per D-10: single failure does not affect others
                # run_agent_background already records failure in Run status
                logger.error(f"[Batch {self.batch_id}] Run {run_id} failed: {e}")
                # Ensure run status is set to failed if not already
                try:
                    async with async_session() as session:
                        run_repo = RunRepository(session)
                        run = await run_repo.get(run_id)
                        if run and run.status not in ("success", "failed", "stopped"):
                            await run_repo.update_status(run_id, "failed")
                except Exception as status_err:
                    logger.error(f"[Batch {self.batch_id}] Failed to update run {run_id} status: {status_err}")

    async def _finalize_batch(self) -> None:
        """Aggregate run statuses and update batch to completed.

        Per D-07: all runs in terminal state (success/failed/stopped) -> batch completed.
        Wrapped in try/finally to ensure cleanup of _active_batches registry.
        """
        try:
            async with async_session() as session:
                batch_repo = BatchRepository(session)
                await batch_repo.update_status(
                    self.batch_id, "completed",
                    finished_at=datetime.now(),
                )
                logger.info(f"[Batch {self.batch_id}] Finalized as completed")
        except Exception as e:
            logger.error(f"[Batch {self.batch_id}] Failed to finalize batch: {e}")
        finally:
            _active_batches.pop(self.batch_id, None)
