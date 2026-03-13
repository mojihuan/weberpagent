"""执行管理路由"""

import asyncio
import logging
import os
import traceback
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db
from backend.db.database import async_session
from backend.db.repository import TaskRepository, RunRepository, StepRepository, ReportRepository
from backend.db.schemas import (
    RunResponse,
    SSEStartedEvent,
    SSEStepEvent,
    SSEFinishedEvent,
    SSEErrorEvent,
)
from backend.core.agent_service import AgentService
from backend.core.event_manager import event_manager

logger = logging.getLogger(__name__)


def get_llm_config() -> dict:
    """获取 LLM 配置，从环境变量读取

    默认使用阿里云 DashScope + qwen3.5-plus
    """
    return {
        "model": os.getenv("LLM_MODEL", "qwen3.5-plus"),
        "api_key": os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY"),
        "base_url": os.getenv(
            "LLM_BASE_URL",
            "https://dashscope.aliyuncs.com/compatible-mode/v1"
        ),
        "temperature": float(os.getenv("LLM_TEMPERATURE", "0.1")),
    }


router = APIRouter(prefix="/runs", tags=["runs"])


async def run_agent_background(run_id: str, task_name: str, task_description: str, max_steps: int):
    """后台执行 agent 任务"""
    logger.info(f"[{run_id}] 开始后台执行: task_name={task_name}, max_steps={max_steps}")

    # 获取 LLM 配置
    llm_config = get_llm_config()
    logger.info(f"[{run_id}] LLM 配置: model={llm_config['model']}, base_url={llm_config['base_url']}")

    async with async_session() as session:
        run_repo = RunRepository(session)
        agent_service = AgentService()

        try:
            await run_repo.update_status(run_id, "running")
            logger.info(f"[{run_id}] 状态更新为 running")
        except Exception as e:
            logger.error(f"[{run_id}] 更新状态失败: {e}")
            raise

        # 发送 started 事件
        started = SSEStartedEvent(run_id=run_id, task_name=task_name)
        await event_manager.publish(run_id, f"event: started\ndata: {started.model_dump_json()}\n\n")
        logger.info(f"[{run_id}] 已发送 started 事件")

        step_count = 0

        async def on_step(step: int, action: str, reasoning: str, screenshot_path: str | None):
            nonlocal step_count
            step_count = step
            logger.info(f"[{run_id}] 步骤 {step}: action={action[:50]}...")

            # 保存步骤到数据库
            try:
                step_data = {
                    "step_index": step,
                    "action": action,
                    "reasoning": reasoning,
                    "screenshot_path": screenshot_path,
                    "status": "success",
                    "duration_ms": 0,
                }
                await run_repo.add_step(run_id, step_data)
                logger.debug(f"[{run_id}] 步骤 {step} 已保存到数据库")
            except Exception as e:
                logger.error(f"[{run_id}] 保存步骤失败: {e}")

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
            await event_manager.publish(run_id, f"event: step\ndata: {event.model_dump_json()}\n\n")

        try:
            logger.info(f"[{run_id}] 开始执行 agent_service.run_with_streaming...")
            result = await agent_service.run_with_streaming(
                task=task_description,
                run_id=run_id,
                on_step=on_step,
                max_steps=max_steps,
                llm_config=llm_config,
            )
            logger.info(f"[{run_id}] agent 执行完成, is_successful={result.is_successful()}")

            # 发送 finished 事件
            final_status = "success" if result.is_successful() else "failed"
            await run_repo.update_status(run_id, final_status)
            event_manager.set_status(run_id, final_status)

            finished = SSEFinishedEvent(
                status=final_status,
                total_steps=step_count,
                duration_ms=0,
            )
            await event_manager.publish(run_id, f"event: finished\ndata: {finished.model_dump_json()}\n\n")
            logger.info(f"[{run_id}] 已发送 finished 事件, status={final_status}")

            # 生成报告
            try:
                # 获取 run 信息以计算执行时间
                run = await run_repo.get(run_id)
                duration_ms = 0
                if run and run.started_at and run.finished_at:
                    duration_ms = int((run.finished_at - run.started_at).total_seconds() * 1000)

                # 获取步骤统计
                steps = await run_repo.get_steps(run_id)
                success_steps = sum(1 for s in steps if s.status == "success")
                failed_steps = sum(1 for s in steps if s.status == "failed")

                # 获取 task 信息
                task_repo = TaskRepository(session)
                task = await task_repo.get(run.task_id) if run else None
                task_name = task.name if task else "Unknown"

                # 创建报告
                report_repo = ReportRepository(session)
                await report_repo.create(
                    run_id=run_id,
                    task_id=run.task_id if run else "",
                    task_name=task_name,
                    status=final_status,
                    total_steps=step_count,
                    success_steps=success_steps,
                    failed_steps=failed_steps,
                    duration_ms=duration_ms,
                )
                logger.info(f"[{run_id}] 报告已生成")
            except Exception as report_error:
                logger.error(f"[{run_id}] 生成报告失败: {report_error}")

        except Exception as e:
            logger.error(f"[{run_id}] 执行失败: {e}")
            logger.error(f"[{run_id}] 异常堆栈:\n{traceback.format_exc()}")

            await run_repo.update_status(run_id, "failed")
            event_manager.set_status(run_id, "failed")

            error = SSEErrorEvent(error=str(e))
            await event_manager.publish(run_id, f"event: error\ndata: {error.model_dump_json()}\n\n")
            logger.info(f"[{run_id}] 已发送 error 事件")

        finally:
            await event_manager.publish(run_id, None)  # 结束信号
            logger.info(f"[{run_id}] 后台执行结束")


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
    background_tasks: BackgroundTasks,
    task_repo: TaskRepository = Depends(get_task_repo),
    run_repo: RunRepository = Depends(get_run_repo),
):
    """创建执行记录并启动后台执行"""
    task = await task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    run = await run_repo.create(task_id=task_id)

    # 启动后台执行
    background_tasks.add_task(
        run_agent_background,
        run.id,
        task.name,
        task.description,
        task.max_steps,
    )

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


@router.get("/{run_id}/stream")
async def stream_run(
    run_id: str,
    run_repo: RunRepository = Depends(get_run_repo),
):
    """SSE 订阅执行流"""
    # 验证 run 存在
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    async def event_generator():
        async for event in event_manager.subscribe(run_id):
            if event is None:
                break
            yield event

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
