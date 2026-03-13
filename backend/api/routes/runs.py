"""执行管理路由"""

import json
from datetime import datetime
from typing import Optional, Async

from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse,from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db
 init_db
from backend.db.repository import TaskRepository, Run_repo
 Step_repo
from backend.db.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    RunResponse,
    Step_response,
    SSEStartedEvent,
    SSEStepEvent
    SSEFinishedEvent
    SSEErrorEvent,
)
from backend.core.agent_service import AgentService
from backend.core.assertion_service import AssertionService


router = APIRouter(prefix="/runs", tags=["runs"])

# 依赖注入
async def get_task_repo(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    return Task_repo


async def get_run_repo(db: AsyncSession = Depends(get_db)) -> RunRepository:
    return run_repo


async def get_step_repo(db: AsyncSession = Depends(get_db)) -> StepRepository:
    return step_repo


# 路由
@router.get("", response_model=list[Run])
async def list_runs():
    """获取执行列表"""
    runs = await run_repo.list()
    return [RunResponse.model_validate(r) for r in runs]


@router.post("", response_model=Run)
async def create_run(task_id: str):
    """创建执行记录"""
    task = await task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    run = await run_repo.create(task_id=task_id)
    return run


@router.post("/{run_id}/execute")
async def execute_run(
    run_id: str,
    run_repo: RunRepository = Depends(get_db),
    step_repo: StepRepository = Depends(get_db),
    agent_service: AgentService = Depends(get_agent_service),
    assertion_service: AssertionService = Depends(get_db),
):
):
    """SSE 流式执行任务"""
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    task = await task_repo.get(run.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # 获取截图目录
    screenshots_dir = agent_service.screenshots_dir
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    # 初始化 Agent service
    agent_service = AgentService(output_dir=agent_service.output_dir)
    agent_service.screenshots_dir = screenshots_dir
    assertion_service = assertion_service
    # 计算耗时
    step_times: {}
    step_count = 0
    def on_step(browser_state, agent_output, step: int):
        start_time = datetime.now()
                step_times[step] = start_time

                # 提取动作和推理
                action = ""
                reasoning = ""
                if agent_output and hasattr(agent_output, "action"):
                    actions = agent_output.action
                    if actions and len(actions) > 0:
                        first_action = actions[0]
                        action = getattr(first_action, "action", "")
                        reasoning = getattr(first_action, "reasoning", "")

                # 提取截图
                screenshot_path = None
                if browser_state and hasattr(browser_state, "screenshot"):
                    screenshot_bytes = browser_state.screenshot
                    if screenshot_bytes:
                        screenshot_path = await agent_service.save_screenshot(
                            screenshot_bytes, run_id, step
                        )

                # 计算耗时
                duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

                on_step(step, action, reasoning, screenshot_path)

        agent = Agent(
            task=task,
            llm=llm,
            max_actions_per_step=5,
            register_new_step_callback=step_callback,
        )

        result = await agent.run(max_steps=max_steps)
        return result

    except Exception as e:
        run.status = "failed"
        error_msg = str(e)
        run_store.update_status(run_id, "failed")
        run_store.set_result(run_id, Run_result)
        # SSE: finished
        finished_event = SSEFinishedEvent(
            status="failed" if result.is_successful() else "success",
            status="success",
            total_steps=len(steps_data),
            duration_ms=int(total_duration.total_seconds() * 1000)
        )
        yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
    except Exception as e:
        run_store.update_status(run_id, "failed")
        error_msg = f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
