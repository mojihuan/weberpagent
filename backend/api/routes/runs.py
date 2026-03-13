"""执行管理路由"""

import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db
from backend.db.repository import TaskRepository, RunRepository, StepRepository
from backend.db.schemas import (
    RunResponse,
    SSEStartedEvent,
    SSEStepEvent,
    SSEFinishedEvent,
    SSEErrorEvent,
)
from backend.core.agent_service import AgentService


router = APIRouter(prefix="/runs", tags=["runs"])


def get_task_repo(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


def get_run_repo(db: AsyncSession = Depends(get_db)) -> RunRepository:
    return RunRepository(db)


def get_step_repo(db: AsyncSession = Depends(get_db)) -> StepRepository:
    return StepRepository(db)


@router.get("", response_model=list[RunResponse])
async def list_runs(
    run_repo: RunRepository = Depends(get_run_repo),
):
    """获取执行列表"""
    runs = await run_repo.list()
    return [RunResponse.model_validate(r) for r in runs]


@router.post("", response_model=RunResponse)
async def create_run(
    task_id: str,
    task_repo: TaskRepository = Depends(get_task_repo),
    run_repo: RunRepository = Depends(get_run_repo),
):
    """创建执行记录"""
    task = await task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    run = await run_repo.create(task_id=task_id)
    return run


@router.get("/{run_id}", response_model=RunResponse)
async def get_run(
    run_id: str,
    run_repo: RunRepository = Depends(get_run_repo),
):
    """获取执行详情"""
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("/{run_id}/execute")
async def execute_run(
    run_id: str,
    run_repo: RunRepository = Depends(get_run_repo),
    step_repo: StepRepository = Depends(get_step_repo),
):
    """SSE 流式执行任务"""
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    run_with_task = await run_repo.get_with_task(run_id)
    if not run_with_task or not run_with_task.task:
        raise HTTPException(status_code=404, detail="Task not found")

    task = run_with_task.task
    agent_service = AgentService()

    async def event_generator():
        start_time = datetime.now()
        await run_repo.update_status(run_id, "running")

        # 发送 started 事件
        started = SSEStartedEvent(run_id=run_id, task_name=task.name)
        yield f"event: started\ndata: {started.model_dump_json()}\n\n"

        try:
            step_count = 0
            steps_data = []

            def on_step(step: int, action: str, reasoning: str, screenshot_path: str | None):
                nonlocal step_count
                step_count = step

                # 保存步骤到数据库 (同步调用)
                import asyncio
                loop = asyncio.get_event_loop()
                step_data = {
                    "step_index": step,
                    "action": action,
                    "reasoning": reasoning,
                    "screenshot_path": screenshot_path,
                    "status": "success",
                    "duration_ms": 0,
                }
                loop.run_until_complete(step_repo.add_step(run_id, step_data))

                # 构造截图 URL
                screenshot_url = f"/api/runs/{run_id}/screenshots/{step}" if screenshot_path else None

                # 发送 step 事件
                event = SSEStepEvent(
                    index=step,
                    action=action,
                    reasoning=reasoning,
                    screenshot_url=screenshot_url,
                    status="success",
                    duration_ms=0,
                )
                steps_data.append(event.model_dump())
                yield f"event: step\ndata: {event.model_dump_json()}\n\n"

            # 执行任务
            result = await agent_service.run_with_streaming(
                task=task.description,
                run_id=run_id,
                on_step=lambda s, a, r, p: list(on_step(s, a, r, p)),
                max_steps=task.max_steps,
            )

            # 计算总耗时
            total_duration = int((datetime.now() - start_time).total_seconds() * 1000)

            # 发送 finished 事件
            final_status = "success" if result.is_successful() else "failed"
            await run_repo.update_status(run_id, final_status)

            finished = SSEFinishedEvent(
                status=final_status,
                total_steps=step_count,
                duration_ms=total_duration,
            )
            yield f"event: finished\ndata: {finished.model_dump_json()}\n\n"

        except Exception as e:
            await run_repo.update_status(run_id, "failed")
            error = SSEErrorEvent(error=str(e))
            yield f"event: error\ndata: {error.model_dump_json()}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.post("/{run_id}/stop")
async def stop_run(
    run_id: str,
    run_repo: RunRepository = Depends(get_run_repo),
):
    """停止执行"""
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    if run.status != "running":
        raise HTTPException(status_code=400, detail="Run is not running")

    await run_repo.update_status(run_id, "stopped")
    return {"status": "stopped"}


@router.get("/{run_id}/screenshots/{step_index}")
async def get_screenshot(
    run_id: str,
    step_index: int,
    step_repo: StepRepository = Depends(get_step_repo),
):
    """获取截图"""
    step = await step_repo.get_by_index(run_id, step_index)

    if not step or not step.screenshot_path:
        raise HTTPException(status_code=404, detail="Screenshot not found")

    from fastapi.responses import FileResponse
    return FileResponse(
        step.screenshot_path,
        media_type="image/png",
    )
