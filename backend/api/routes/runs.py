"""执行管理路由"""

import asyncio
import json
import logging
import traceback
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import get_settings
from backend.db import get_db
from backend.db.database import async_session
from backend.db.repository import TaskRepository, RunRepository, StepRepository, ReportRepository
from backend.db.schemas import (
    RunResponse,
    SSEStartedEvent,
    SSEStepEvent,
    SSEFinishedEvent,
    SSEErrorEvent,
    SSEPreconditionEvent,
    SSEAssertionEvent,
)
from backend.core.agent_service import AgentService
from backend.core.event_manager import event_manager
from backend.core.report_service import ReportService
from backend.core.assertion_service import AssertionService
from backend.core.precondition_service import PreconditionService
from backend.core.external_precondition_bridge import execute_all_assertions
from backend.db.repository import AssertionResultRepository, PreconditionResultRepository

logger = logging.getLogger(__name__)


def get_llm_config() -> dict:
    """获取 LLM 配置，从集中配置读取

    使用 temperature=0 确保确定性输出
    """
    settings = get_settings()
    return {
        "model": settings.llm_model,
        "api_key": settings.dashscope_api_key or settings.openai_api_key,
        "base_url": settings.llm_base_url,
        "temperature": settings.llm_temperature,
    }


router = APIRouter(prefix="/runs", tags=["runs"])


async def run_agent_background(
    run_id: str,
    task_id: str,
    task_name: str,
    task_description: str,
    max_steps: int,
    preconditions: list[str] | None = None,
    external_assertions: list[dict] | None = None,
    target_url: str | None = None,
    login_role: str | None = None,
):
    """后台执行 agent 任务"""
    logger.info(f"[{run_id}] 开始后台执行: task_id={task_id}, task_name={task_name}, max_steps={max_steps}")

    # 获取 LLM 配置
    llm_config = get_llm_config()
    logger.info(f"[{run_id}] LLM 配置: model={llm_config['model']}, base_url={llm_config['base_url']}")

    # 获取外部模块路径配置
    settings = get_settings()
    external_module_path = settings.erp_api_module_path

    # Resolve login credentials if login_role is set (per D-14, D-15)
    account_info = None
    login_url = None
    shared_cache = None
    if login_role:
        from backend.core.account_service import account_service
        from backend.core.cache_service import CacheService

        account_info = account_service.resolve(login_role)
        login_url = account_service.get_login_url()
        shared_cache = CacheService()
        logger.info(f"[{run_id}] 登录角色: {login_role}, 账号: {account_info.account}")

    async with async_session() as session:
        run_repo = RunRepository(session)
        agent_service = AgentService()
        report_service = ReportService(session)
        assertion_service = AssertionService(session)
        assertion_result_repo = AssertionResultRepository(session)
        precondition_result_repo = PreconditionResultRepository(session)
        global_seq = 0

        # === 执行前置条件 ===
        context: dict[str, Any] = {}

        if preconditions:
            precondition_service = PreconditionService(external_module_path=external_module_path, cache=shared_cache)

            for i, code in enumerate(preconditions):
                if not code.strip():
                    continue

                # 发送 precondition 事件（running）
                code_display = code[:100] + "..." if len(code) > 100 else code
                pre_event = SSEPreconditionEvent(
                    index=i,
                    code=code_display,
                    status="running",
                )
                await event_manager.publish(run_id, f"event: precondition\ndata: {pre_event.model_dump_json()}\n\n")

                # 执行前置条件
                result = await precondition_service.execute_single(code, i)

                # 发送 precondition 事件（success/failed）
                pre_event = SSEPreconditionEvent(
                    index=i,
                    code=code_display,
                    status="success" if result.success else "failed",
                    error=result.error,
                    duration_ms=result.duration_ms,
                    variables=result.variables if result.success else None,
                )
                await event_manager.publish(run_id, f"event: precondition\ndata: {pre_event.model_dump_json()}\n\n")

                # Phase 59: 持久化前置条件结果
                global_seq += 1
                await precondition_result_repo.create(
                    run_id=run_id,
                    sequence_number=global_seq,
                    index=i,
                    code=code,
                    status="success" if result.success else "failed",
                    error=result.error,
                    duration_ms=result.duration_ms,
                    variables=json.dumps(result.variables) if (result.success and result.variables) else None,
                )

                if not result.success:
                    # 前置条件失败，终止执行
                    await run_repo.update_status(run_id, "failed")
                    event_manager.set_status(run_id, "failed")
                    finished = SSEFinishedEvent(status="failed", total_steps=0, duration_ms=0)
                    await event_manager.publish(run_id, f"event: finished\ndata: {finished.model_dump_json()}\n\n")
                    await event_manager.publish(run_id, None)
                    return

            # 获取 context 用于变量替换
            context = precondition_service.get_context()
            logger.info(f"[{run_id}] 前置条件执行完成，变量: {list(context.keys())}")

            # 替换 task_description 中的变量
            task_description = PreconditionService.substitute_variables(task_description, context)
            logger.info(f"[{run_id}] 变量替换后的任务描述: {task_description[:100]}...")

        # Pre-injection branch: try cookie injection, fallback to text login (D-07, D-08, D-09)
        authenticated_session = None
        effective_target_url = None if login_role else target_url

        if login_role:
            from backend.core.auth_session_factory import create_authenticated_session
            from backend.core.auth_service import TokenFetchError

            # Try cookie pre-injection
            try:
                authenticated_session = await create_authenticated_session(login_role)
            except TokenFetchError as e:
                logger.warning(
                    "Cookie预注入失败，回退到文字登录 | 角色=%s | 原因=%s",
                    e.role, e.reason,
                )

            if authenticated_session:
                # Pre-injection success (D-08): cached variable replacement only, no login prefix
                from backend.core.test_flow_service import TestFlowService

                flow = TestFlowService()
                cache_values = shared_cache.all() if shared_cache else {}
                task_description = flow.replace_cached_variables_only(
                    task_description, cache_values
                )
                # Use ERP homepage URL, not login page (D-01)
                effective_target_url = settings.erp_base_url.rstrip("/")
                logger.info(f"[{run_id}] Cookie预注入成功，跳过登录步骤")
            else:
                # Pre-injection failure (D-09): existing full login flow
                from backend.core.test_flow_service import TestFlowService

                flow = TestFlowService()
                cache_values = shared_cache.all() if shared_cache else {}
                task_description = flow._build_description(
                    task_description=task_description,
                    login_url=login_url,
                    account=account_info.account,
                    password=account_info.password,
                    context=context if isinstance(context, dict) else {},
                    cache_values=cache_values,
                )
                effective_target_url = None
                logger.info(f"[{run_id}] 注入登录步骤后的任务描述: {task_description[:150]}...")

        # === 前置条件执行结束 ===

        try:
            await run_repo.update_status(run_id, "running")
            logger.info(f"[{run_id}] 状态更新为 running")
        except Exception as e:
            logger.error(f"[{run_id}] 更新状态失败: {e}")
            raise

        # 发送 started 事件
        started = SSEStartedEvent(run_id=run_id, task_id=task_id, task_name=task_name)
        await event_manager.publish(run_id, f"event: started\ndata: {started.model_dump_json()}\n\n")
        logger.info(f"[{run_id}] 已发送 started 事件")

        step_count = 0

        async def on_step(step: int, action: str, reasoning: str, screenshot_path: str | None, step_stats_json: str | None = None):
            nonlocal step_count, global_seq
            step_count = step
            logger.info(f"[{run_id}] 步骤 {step}: action={action[:50]}...")

            # Phase 59: assign global sequence number
            global_seq += 1

            # 保存步骤到数据库
            try:
                step_data = {
                    "step_index": step,
                    "action": action,
                    "reasoning": reasoning,
                    "screenshot_path": screenshot_path,
                    "status": "success",
                    "duration_ms": 0,
                    "step_stats": step_stats_json,  # Pass JSON string directly to repository (Phase 41, LOG-02)
                    "sequence_number": global_seq,  # Phase 59
                }
                await run_repo.add_step(run_id, step_data)
                logger.debug(f"[{run_id}] 步骤 {step} 已保存到数据库")
            except Exception as e:
                logger.error(f"[{run_id}] 保存步骤失败: {e}")

            # 构造截图 URL（相对路径，前端会添加 API_BASE）
            screenshot_url = f"/runs/{run_id}/screenshots/{step}" if screenshot_path else None

            # Parse step_stats_json back to dict for SSE event (Phase 41, LOG-02)
            step_stats_dict = None
            if step_stats_json:
                try:
                    step_stats_dict = json.loads(step_stats_json)
                except json.JSONDecodeError:
                    pass  # Keep as None if parsing fails

            # 发送 step 事件
            event = SSEStepEvent(
                index=step,
                action=action,
                reasoning=reasoning,
                screenshot_url=screenshot_url,
                status="success",
                duration_ms=0,
                step_stats=step_stats_dict,
            )
            await event_manager.publish(run_id, f"event: step\ndata: {event.model_dump_json()}\n\n")

        try:
            logger.info(f"[{run_id}] 开始执行 agent_service.run_with_cleanup...")
            result = await agent_service.run_with_cleanup(
                task=task_description,
                run_id=run_id,
                on_step=on_step,
                max_steps=max_steps,
                llm_config=llm_config,
                target_url=effective_target_url,
                browser_session=authenticated_session,
            )
            logger.info(f"[{run_id}] agent 执行完成, is_successful={result.is_successful()}")

            # 确定最终状态
            final_status = "success" if result.is_successful() else "failed"

            # 评估断言（如果任务有断言）
            run = await run_repo.get_with_task(run_id)
            if run and run.task and run.task.assertions:
                # Build lookup map for assertion names
                assertion_map = {a.id: a for a in run.task.assertions}
                assertion_results = await assertion_service.evaluate_all(
                    run_id=run_id,
                    assertions=run.task.assertions,
                    history=result,
                )
                # Phase 59: assign sequence numbers to UI assertion results
                for ar in assertion_results:
                    global_seq += 1
                    await assertion_result_repo.update_sequence_number(ar.id, global_seq)
                    # Send SSE event for each assertion result
                    source_assertion = assertion_map.get(ar.assertion_id)
                    assertion_event = SSEAssertionEvent(
                        assertion_id=ar.assertion_id,
                        assertion_name=source_assertion.name if source_assertion else "未知断言",
                        assertion_type=source_assertion.type if source_assertion else "unknown",
                        status=ar.status,
                        message=ar.message,
                        actual_value=ar.actual_value,
                    )
                    await event_manager.publish(
                        run_id,
                        f"event: assertion\ndata: {assertion_event.model_dump_json()}\n\n"
                    )
                # 如果任何断言失败，整体状态为失败
                if any(ar.status == "fail" for ar in assertion_results):
                    final_status = "failed"
                    logger.info(f"[{run_id}] 断言评估完成，存在失败断言，状态设为 failed")
                else:
                    logger.info(f"[{run_id}] 断言评估完成，全部通过")

            # ========== Execute External Assertions (Phase 25) ==========
            if external_assertions:
                from backend.core.precondition_service import ContextWrapper

                # Create context wrapper if not already created
                if not isinstance(context, ContextWrapper):
                    context_wrapper = ContextWrapper(cache=shared_cache)
                    context_wrapper._data = context.copy() if context else {}
                else:
                    context_wrapper = context

                logger.info(f"[{run_id}] Starting external assertion execution ({len(external_assertions)} assertions)")

                try:
                    external_assertion_summary = await execute_all_assertions(
                        assertions=external_assertions,
                        context=context_wrapper,
                        timeout_per_assertion=30.0
                    )

                    logger.info(
                        f"[{run_id}] External assertions complete: "
                        f"{external_assertion_summary['passed']}/{external_assertion_summary['total']} passed, "
                        f"{external_assertion_summary['failed']} failed, {external_assertion_summary['errors']} errors"
                    )

                    # Send individual SSE events for each external assertion result
                    for idx, ext_result in enumerate(external_assertion_summary.get('results', [])):
                        global_seq += 1
                        assertion_name = f"{ext_result.get('class_name', '?')}.{ext_result.get('method', '?')}"
                        status_str = 'pass' if ext_result.get('passed') else 'fail'
                        message_parts = []
                        if ext_result.get('error'):
                            message_parts.append(ext_result['error'])
                        # Build field_results summary
                        field_results = ext_result.get('field_results', [])
                        if field_results:
                            for fr in field_results:
                                fr_status = 'pass' if fr.get('passed') else 'fail'
                                message_parts.append(f"{fr.get('field_name', '?')}: {fr_status}")

                        ext_assertion_event = SSEAssertionEvent(
                            assertion_id=f"ext-{idx}",
                            assertion_name=assertion_name,
                            assertion_type="external",
                            status=status_str,
                            message='; '.join(message_parts) if message_parts else None,
                            actual_value=None,
                            field_results=field_results if field_results else None,
                        )
                        await event_manager.publish(
                            run_id,
                            f"event: assertion\ndata: {ext_assertion_event.model_dump_json()}\n\n"
                        )

                    # Also send summary event
                    assertion_event = {
                        "type": "external_assertions_complete",
                        "total": external_assertion_summary['total'],
                        "passed": external_assertion_summary['passed'],
                        "failed": external_assertion_summary['failed'],
                        "errors": external_assertion_summary['errors'],
                        "timestamp": datetime.now().isoformat()
                    }
                    await event_manager.publish(
                        run_id,
                        f"event: external_assertions\ndata: {json.dumps(assertion_event)}\n\n"
                    )

                    # Store external assertion results in DB for report
                    run_obj = await run_repo.get(run_id)
                    if run_obj:
                        results_to_store = []
                        for idx, ext_result in enumerate(external_assertion_summary.get('results', [])):
                            results_to_store.append({
                                "sequence_number": global_seq - len(external_assertion_summary.get('results', [])) + idx + 1,
                                "assertion_name": f"{ext_result.get('class_name', '?')}.{ext_result.get('method', '?')}",
                                "status": 'pass' if ext_result.get('passed') else 'fail',
                                "message": ext_result.get('error'),
                                "field_results": ext_result.get('field_results'),
                                "duration": ext_result.get('duration'),
                            })
                        run_obj.external_assertion_results = json.dumps(results_to_store)
                        await session.commit()

                    # Store summary in context for potential later use
                    context['external_assertion_summary'] = external_assertion_summary

                    # Update final status if any external assertions failed
                    if external_assertion_summary['failed'] > 0 or external_assertion_summary['errors'] > 0:
                        final_status = "failed"
                        logger.info(f"[{run_id}] External assertions have failures/errors, status set to failed")

                except Exception as e:
                    logger.error(f"[{run_id}] External assertion execution failed: {e}", exc_info=True)
                    # Non-fail-fast: continue even on error
                    await event_manager.publish(
                        run_id,
                        f"event: external_assertions\ndata: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
                    )
            # === External Assertions End ===

            # 更新状态
            await run_repo.update_status(run_id, final_status)
            event_manager.set_status(run_id, final_status)

            # 发送 finished 事件
            finished = SSEFinishedEvent(
                status=final_status,
                total_steps=step_count,
                duration_ms=0,
            )
            await event_manager.publish(run_id, f"event: finished\ndata: {finished.model_dump_json()}\n\n")
            logger.info(f"[{run_id}] 已发送 finished 事件, status={final_status}")

            # 使用 ReportService 生成报告
            await report_service.generate_report(run_id)
            logger.info(f"[{run_id}] 报告已生成")

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
    runs = await run_repo.list_with_details()
    return [
        RunResponse(
            id=run.id,
            task_id=run.task_id,
            status=run.status,
            started_at=run.started_at,
            finished_at=run.finished_at,
            created_at=run.created_at,
            task_name=run.task.name if run.task else None,
            steps_count=len(run.steps) if run.steps else 0,
        )
        for run in runs
    ]


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

    # 解析 preconditions
    preconditions = None
    if task.preconditions:
        try:
            preconditions = json.loads(task.preconditions)
        except json.JSONDecodeError:
            logger.warning(f"Task {task_id} preconditions JSON 解析失败")

    # 解析 external_assertions (Phase 25)
    external_assertions = None
    if hasattr(task, 'external_assertions') and task.external_assertions:
        try:
            external_assertions = json.loads(task.external_assertions)
            logger.info(f"Task {task_id} loaded {len(external_assertions)} external assertions")
        except json.JSONDecodeError:
            logger.warning(f"Task {task_id} external_assertions JSON 解析失败")

    # 启动后台执行
    background_tasks.add_task(
        run_agent_background,
        run.id,
        task_id,
        task.name,
        task.description,
        task.max_steps,
        preconditions,
        external_assertions,  # Phase 25: external assertions
        task.target_url,  # 目标 URL
        task.login_role,  # Login role for ERP integration (per D-15)
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
