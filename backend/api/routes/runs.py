"""执行管理路由"""

import json
from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.api.schemas.index import Run, Step, RunResult
from backend.storage.run_store import RunStore
from backend.storage.task_store import TaskStore
from backend.core.agent_service import AgentService
from backend.core.assertion_service import AssertionService

router = APIRouter(prefix="/runs", tags=["runs"])

run_store = RunStore()
task_store = TaskStore()
agent_service = AgentService()
assertion_service = AssertionService()


@router.get("", response_model=list[Run])
async def list_runs():
    """获取执行列表"""
    return run_store.list()


@router.post("", response_model=Run)
async def create_run(task_id: str):
    """创建执行记录"""
    task = task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return run_store.create(task_id=task_id)


@router.get("/{run_id}", response_model=Run)
async def get_run(run_id: str):
    """获取执行详情"""
    run = run_store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("/{run_id}/execute")
async def execute_run(run_id: str):
    """执行任务并返回 SSE 流"""
    run = run_store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    task = task_store.get(run.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    async def event_generator():
        start_time = datetime.now()
        run_store.update_status(run_id, "running")

        yield f"event: start\ndata: {json.dumps({'run_id': run_id, 'task': task.name})}\n\n"

        try:
            steps_data = []

            def on_step(step: int, action: str, reasoning: str, screenshot: str | None):
                step_obj = Step(
                    step=step,
                    action=action,
                    reasoning=reasoning,
                    screenshot=screenshot,
                )
                steps_data.append(step_obj.model_dump())
                run_store.add_step(run_id, step_obj)

            result = await agent_service.run_simple(task=task.description)

            assertion_results = assertion_service.run_all_assertions(result, task.assertions)

            duration = (datetime.now() - start_time).total_seconds()
            total_steps = len(steps_data)

            run_result = RunResult(
                success=result.is_done if hasattr(result, "is_done") else True,
                ai_assertion={"passed": result.is_done if hasattr(result, "is_done") else True},
                code_assertion=assertion_results,
                duration_seconds=duration,
                total_steps=total_steps,
            )

            run_store.set_result(run_id, run_result)
            run_store.update_status(run_id, "completed")

            yield f"event: complete\ndata: {json.dumps(run_result.model_dump())}\n\n"

        except Exception as e:
            run_store.update_status(run_id, "failed")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.post("/{run_id}/stop")
async def stop_run(run_id: str):
    """停止执行"""
    run = run_store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    if run.status != "running":
        raise HTTPException(status_code=400, detail="Run is not running")

    run_store.update_status(run_id, "failed")
    return {"status": "stopped"}
