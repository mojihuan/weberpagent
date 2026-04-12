"""Batch execution routes"""

import asyncio
import json
import logging

from fastapi import APIRouter, HTTPException

from backend.db.database import async_session
from backend.db.repository import BatchRepository, RunRepository, TaskRepository
from backend.db.schemas import BatchCreateRequest, BatchResponse, BatchRunSummary
from backend.core.batch_execution import BatchExecutionService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/batches", tags=["batches"])


@router.post("", response_model=BatchResponse)
async def create_batch(request: BatchCreateRequest):
    """Create a batch execution for multiple tasks.

    Per D-13: creates Batch record + Run per task, starts parallel execution.
    """
    async with async_session() as session:
        task_repo = TaskRepository(session)
        run_repo = RunRepository(session)
        batch_repo = BatchRepository(session)

        # Validate all tasks exist
        tasks = []
        for task_id in request.task_ids:
            task = await task_repo.get(task_id)
            if not task:
                raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
            tasks.append(task)

        # Create batch record
        batch = await batch_repo.create(concurrency=request.concurrency)

        # Create runs and collect configs for batch execution
        run_configs = []
        for task in tasks:
            run = await run_repo.create(task_id=task.id)
            # Link run to batch
            run.batch_id = batch.id
            await session.commit()
            await session.refresh(run)

            # Parse preconditions
            preconditions = None
            if task.preconditions:
                try:
                    preconditions = json.loads(task.preconditions)
                except json.JSONDecodeError:
                    logger.warning(f"Task {task.id} preconditions JSON parse failed")

            # Parse external_assertions
            external_assertions = None
            if hasattr(task, 'external_assertions') and task.external_assertions:
                try:
                    external_assertions = json.loads(task.external_assertions)
                except json.JSONDecodeError:
                    logger.warning(f"Task {task.id} external_assertions JSON parse failed")

            run_configs.append({
                "run_id": run.id,
                "task_id": task.id,
                "task_name": task.name,
                "task_description": task.description,
                "max_steps": task.max_steps,
                "preconditions": preconditions,
                "external_assertions": external_assertions,
                "target_url": task.target_url,
                "login_role": task.login_role,
            })

        # Start batch execution in background (fire-and-forget)
        service = BatchExecutionService(batch.id, request.concurrency)
        asyncio.create_task(service.start(run_configs))

        logger.info(f"Batch {batch.id} created with {len(tasks)} tasks, concurrency={request.concurrency}")

        # Return batch response
        return BatchResponse(
            id=batch.id,
            concurrency=batch.concurrency,
            status=batch.status,
            created_at=batch.created_at,
            finished_at=batch.finished_at,
        )


@router.get("/{batch_id}", response_model=BatchResponse)
async def get_batch(batch_id: str):
    """Get batch status with run summaries.

    Per D-14: returns batch status + run status summary.
    """
    async with async_session() as session:
        batch_repo = BatchRepository(session)
        batch = await batch_repo.get_with_runs(batch_id)
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")

        run_summaries = []
        if batch.runs:
            for run in batch.runs:
                run_summaries.append(BatchRunSummary(
                    id=run.id,
                    task_id=run.task_id,
                    task_name=run.task.name if run.task else None,
                    status=run.status,
                    started_at=run.started_at,
                    finished_at=run.finished_at,
                ))

        return BatchResponse(
            id=batch.id,
            concurrency=batch.concurrency,
            status=batch.status,
            created_at=batch.created_at,
            finished_at=batch.finished_at,
            runs=run_summaries,
        )


@router.get("/{batch_id}/runs", response_model=list[BatchRunSummary])
async def get_batch_runs(batch_id: str):
    """Get runs belonging to a batch.

    Per D-15: returns runs for Phase 73 batch progress UI.
    """
    async with async_session() as session:
        batch_repo = BatchRepository(session)
        batch = await batch_repo.get(batch_id)
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")

        runs = await batch_repo.list_runs_by_batch(batch_id)
        return [
            BatchRunSummary(
                id=run.id,
                task_id=run.task_id,
                task_name=run.task.name if run.task else None,
                status=run.status,
                started_at=run.started_at,
                finished_at=run.finished_at,
            )
            for run in runs
        ]
