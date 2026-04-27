"""执行管理路由"""

import asyncio
import json
import logging
import traceback
from datetime import datetime
from typing import Any

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import PlainTextResponse, StreamingResponse
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
    TaskUpdate,
)
from backend.core.agent_service import AgentService
from backend.core.self_healing_runner import SelfHealingRunner
from backend.core.event_manager import event_manager
from backend.core.report_service import ReportService
from backend.core.assertion_service import AssertionService
from backend.core.precondition_service import PreconditionService
from backend.core.external_precondition_bridge import execute_all_assertions
from backend.db.repository import AssertionResultRepository, PreconditionResultRepository

logger = logging.getLogger(__name__)

# Module-level concurrency guard for code execution (per D-08)
_code_execution_semaphore = asyncio.Semaphore(1)
_active_code_execution: dict[str, str] = {}  # run_id -> started_at ISO


def _sanitize_variables(variables: dict) -> dict:
    """Filter out non-JSON-serializable values from a variables dict.

    External precondition code may store arbitrary Python objects (type
    objects, class instances, etc.) in the context.  Only JSON-safe
    primitives are kept for SSE broadcast and database persistence.
    """
    return {
        k: v for k, v in variables.items()
        if isinstance(v, (str, int, float, bool, list, dict, type(None)))
    }


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


def get_code_gen_llm_config() -> dict:
    """获取代码生成专用 LLM 配置。

    优先使用 code_gen_* 配置（如 DeepSeek-V4-Pro），
    未配置时 fallback 到默认 LLM 配置。
    """
    settings = get_settings()
    if settings.code_gen_model:
        return {
            "model": settings.code_gen_model,
            "api_key": settings.code_gen_api_key,
            "base_url": settings.code_gen_base_url,
            "temperature": settings.code_gen_temperature,
        }
    return get_llm_config()


router = APIRouter(prefix="/runs", tags=["runs"])


def _format_code_with_line_numbers(content: str) -> str:
    """Format code with right-aligned line numbers (per D-01).

    Format: "{line_num:>width} | {line_content}"
    Example: "  1 | def test_xxx():"
    """
    lines = content.splitlines()
    max_width = len(str(len(lines)))
    formatted = [f"{i + 1:>{max_width}} | {line}" for i, line in enumerate(lines)]
    return "\n".join(formatted)


def _validate_code_path(code_path: str) -> Path:
    """Validate code path exists and is within outputs/ directory (per D-03).

    Returns resolved Path if valid.
    Raises HTTPException on validation failure.
    """
    resolved = Path(code_path).resolve()
    outputs_root = Path("outputs").resolve()
    if not str(resolved).startswith(str(outputs_root)):
        raise HTTPException(status_code=403, detail="非法文件路径")
    if not resolved.exists():
        raise HTTPException(status_code=404, detail="代码文件不存在")
    return resolved


async def _execute_code_background(
    run_id: str,
    test_file_path: str,
    login_role: str,
    task_id: str,
) -> None:
    """Background task: run SelfHealingRunner and update healing status + Task status.

    Per D-04: reuses SelfHealingRunner.run() completely.
    Per D-06: updates healing_status field (pending -> healing -> passed/failed).
    Per D-09: updates Task.status = "success" on passed result.
    """
    async with _code_execution_semaphore:
        _active_code_execution[run_id] = datetime.now().isoformat()
        try:
            runner = SelfHealingRunner(get_code_gen_llm_config())
            result = await runner.run(
                run_id=run_id,
                test_file_path=test_file_path,
                login_role=login_role,
                base_dir="outputs",
            )
            # Update healing status (D-06)
            async with async_session() as session:
                run_repo = RunRepository(session)
                await run_repo.update_healing_status(
                    run_id=run_id,
                    status=result.final_status,
                    attempts=result.attempts,
                    error=result.error_message or None,
                    code_path=result.repaired_code_path or None,
                    error_category=result.error_category,
                )
                # D-09: Update Task.status on success
                if result.final_status == "passed":
                    task_repo = TaskRepository(session)
                    await task_repo.update(task_id, TaskUpdate(status="success"))
            logger.info(
                f"[{run_id}] 代码执行完成: status={result.final_status}, "
                f"attempts={result.attempts}"
            )
        except Exception as e:
            logger.error(f"[{run_id}] 代码执行后台任务异常: {e}", exc_info=True)
            # Ensure healing status reflects failure
            try:
                async with async_session() as session:
                    run_repo = RunRepository(session)
                    await run_repo.update_healing_status(
                        run_id=run_id,
                        status="failed",
                        attempts=0,
                        error=str(e)[:2000],
                    )
            except Exception:
                pass  # Non-blocking
        finally:
            _active_code_execution.pop(run_id, None)


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
                # Sanitize variables: only include JSON-serializable values
                _safe_vars = _sanitize_variables(result.variables) if (result.success and result.variables) else None
                pre_event = SSEPreconditionEvent(
                    index=i,
                    code=code_display,
                    status="success" if result.success else "failed",
                    error=result.error,
                    duration_ms=result.duration_ms,
                    variables=_safe_vars,
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
                    variables=json.dumps(_safe_vars) if _safe_vars else None,
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

        # Pre-injection branch: programmatic login with clean session, fallback to text login
        authenticated_session = None
        effective_target_url = None if login_role else target_url
        auth_pre_nav_ok = False

        if login_role:
            from backend.core.auth_service import TokenFetchError
            from backend.core.test_flow_service import TestFlowService

            flow = TestFlowService()
            cache_values = shared_cache.all() if shared_cache else {}

            # Use a clean BrowserSession (no storage_state injection).
            # Phase 86 research confirmed storage_state injection fails for Vue SPA:
            # the SPA's Vuex/Pinia store ignores injected localStorage tokens.
            # Worse, the CDP init script from storage_state interferes with
            # the programmatic login, causing the login button click to silently fail.
            from backend.core.agent_service import create_browser_session

            authenticated_session = create_browser_session()
            from urllib.parse import urlparse
            _parsed = urlparse(settings.erp_base_url)
            effective_target_url = f"{_parsed.scheme}://{_parsed.netloc}"

            # Perform programmatic form login (fill form + click via dispatchEvent)
            try:
                auth_pre_nav_ok = await agent_service.pre_navigate(
                    run_id, effective_target_url, authenticated_session,
                    login_account=account_info.account,
                    login_password=account_info.password,
                )
            except Exception as e:
                logger.warning(f"[{run_id}] [代码登录回退] 角色={login_role} 原因=预导航异常: {e}")
                auth_pre_nav_ok = False

            if auth_pre_nav_ok:
                # Programmatic login succeeded — skip login in task description
                task_description = flow.replace_cached_variables_only(
                    task_description, cache_values
                )
                logger.info(f"[{run_id}] 编程式登录成功，跳过登录步骤")
            else:
                logger.warning(
                    f"[{run_id}] [代码登录回退] 角色={login_role} 原因=预导航失败，"
                    f"回退到文字登录模式"
                )
                # Fallback: close the failed session and rebuild task with login text
                try:
                    await authenticated_session.stop()
                except Exception:
                    pass
                authenticated_session = None
                effective_target_url = None

                # Rebuild task description with login prefix
                task_description = flow._build_description(
                    task_description=task_description,
                    login_url=login_url,
                    account=account_info.account,
                    password=account_info.password,
                    context=context if isinstance(context, dict) else {},
                    cache_values=cache_values,
                )
                logger.info(
                    f"[{run_id}] 回退文字登录，任务描述: "
                    f"{task_description[:150]}..."
                )

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

            # === Code Generation (Phase 82, CODE-01 / Phase 84 LLM healing) ===
            try:
                from backend.core.code_generator import PlaywrightCodeGenerator
                code_generator = PlaywrightCodeGenerator()
                # PREC-02: 传递 effective_target_url 作为前置条件
                _precondition_config = (
                    {"target_url": effective_target_url}
                    if effective_target_url
                    else None
                )
                # ASRT-02: 传递任务断言给代码生成器
                _assertions_config = None
                if run and run.task and run.task.assertions:
                    _assertions_config = [
                        {"type": a.type, "expected": a.expected, "name": a.name}
                        for a in run.task.assertions
                    ]
                code_path = await code_generator.generate_and_save(
                    run_id=run_id,
                    task_name=task_name,
                    task_id=task_id,
                    agent_history=result,
                    llm_config=get_code_gen_llm_config(),
                    precondition_config=_precondition_config,
                    assertions_config=_assertions_config,
                )
                await run_repo.update_generated_code_path(run_id, code_path)
                logger.info(f"[{run_id}] 生成 Playwright 代码: {code_path}")
            except Exception as e:
                logger.error(f"[{run_id}] 代码生成失败（非阻塞）: {e}")

            # === Self-Healing Re-execution (Phase 85, HEAL-03) ===
            try:
                # 获取生成的代码路径（可能在上面的代码生成块中已设置）
                run_obj = await run_repo.get(run_id)
                if run_obj and run_obj.generated_code_path:
                    from backend.core.self_healing_runner import SelfHealingRunner
                    healing_runner = SelfHealingRunner(get_code_gen_llm_config())
                    healing_result = await healing_runner.run(
                        run_id=run_id,
                        test_file_path=run_obj.generated_code_path,
                        login_role=login_role,
                        base_dir="outputs",
                    )
                    await run_repo.update_healing_status(
                        run_id=run_id,
                        status=healing_result.final_status,
                        attempts=healing_result.attempts,
                        error=healing_result.error_message or None,
                        code_path=healing_result.repaired_code_path or None,
                    )
                    logger.info(
                        f"[{run_id}] 自愈结果: status={healing_result.final_status}, "
                        f"attempts={healing_result.attempts}"
                    )
                else:
                    # 无生成代码，标记跳过
                    await run_repo.update_healing_status(
                        run_id=run_id, status="skipped", attempts=0,
                    )
                    logger.info(f"[{run_id}] 无生成代码，跳过自愈")
            except Exception as e:
                # 自愈失败不阻塞主流程
                logger.error(f"[{run_id}] 自愈执行失败（非阻塞）: {e}")
                try:
                    await run_repo.update_healing_status(
                        run_id=run_id, status="failed", attempts=0,
                        error=str(e)[:2000],
                    )
                except Exception:
                    pass  # 即使更新状态失败也不阻塞

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


@router.get("/{run_id}/code")
async def get_run_code(
    run_id: str,
    run_repo: RunRepository = Depends(get_run_repo),
):
    """获取执行记录生成的 Playwright 代码内容 (CODE-01)"""
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="执行记录不存在")
    if not run.generated_code_path:
        raise HTTPException(status_code=404, detail="该执行记录无生成代码")

    # Path traversal protection (D-03)
    resolved = _validate_code_path(run.generated_code_path)

    content = resolved.read_text(encoding="utf-8")
    formatted = _format_code_with_line_numbers(content)
    return PlainTextResponse(formatted)


@router.post("/{run_id}/execute-code", status_code=202)
async def execute_run_code(
    run_id: str,
    background_tasks: BackgroundTasks,
    run_repo: RunRepository = Depends(get_run_repo),
):
    """触发 Playwright 代码执行 (CODE-02)"""
    # Pre-check 1: run exists
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="执行记录不存在")

    # Pre-check 2: has generated code
    if not run.generated_code_path:
        raise HTTPException(status_code=400, detail="该执行记录无生成代码")

    # Pre-check 3: task has login_role (per D-07)
    async with async_session() as session:
        run_with_task = await RunRepository(session).get_with_task(run_id)
    task = run_with_task.task if run_with_task else None
    if not task or not task.login_role:
        raise HTTPException(status_code=400, detail="任务未配置登录角色，无法执行")

    # Pre-check 4: concurrent execution (per D-08)
    if run_id in _active_code_execution:
        raise HTTPException(status_code=409, detail="已有代码执行正在进行中，请稍后重试")

    # Update healing_status to "healing" before starting (D-06)
    async with async_session() as session:
        repo = RunRepository(session)
        await repo.update_healing_status(run_id, status="healing", attempts=0)

    # Launch background execution
    background_tasks.add_task(
        _execute_code_background,
        run_id=run_id,
        test_file_path=run.generated_code_path,
        login_role=task.login_role,
        task_id=task.id,
    )

    return {"run_id": run_id, "status": "healing"}


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
