"""执行管理路由"""

import asyncio
import json
import logging
import traceback
from datetime import datetime
from typing import Any, AsyncGenerator

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from backend.api.helpers import _parse_task_json_fields, raise_not_found
from fastapi.responses import PlainTextResponse, StreamingResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import get_settings
from backend.db import get_db
from backend.db.database import async_session
from backend.db.repository import TaskRepository, RunRepository, StepRepository
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
from backend.core.event_manager import event_manager
from backend.core.report_service import ReportService
from backend.core.assertion_service import AssertionService
from backend.core.precondition_service import PreconditionService
from backend.core.external_precondition_bridge import execute_all_assertions
from backend.core.step_code_buffer import StepCodeBuffer
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


_CONFTEST_TEMPLATE = '''"""Auto-generated conftest for Playwright storage_state injection."""
import json
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Inject storage_state from .storage_state.json in the test file directory."""
    state_file = Path(__file__).parent / ".storage_state.json"
    if state_file.exists():
        with open(state_file, encoding="utf-8") as f:
            return {**browser_context_args, "storage_state": json.load(f)}
    return browser_context_args
'''


def _build_storage_state(login_role: str) -> dict:
    """Build Playwright storage_state dict with auth token for the given role."""
    from backend.core.account_service import account_service
    from backend.core.auth_service import auth_service
    from urllib.parse import urlparse

    account_info = account_service.resolve(login_role)
    token = auth_service.fetch_token(account_info.account, account_info.password, role=login_role)
    settings = get_settings()
    parsed = urlparse(settings.erp_base_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    return {
        "cookies": [],
        "origins": [{
            "origin": origin,
            "localStorage": [
                {"name": "Admin-Token", "value": token},
                {"name": "Admin-Expires-In", "value": "720"},
            ],
        }],
    }


def _write_test_support_files(test_file_dir: str, storage_state: dict) -> tuple[Path, Path]:
    """Write conftest.py and .storage_state.json to the test file directory."""
    conftest_path = Path(test_file_dir) / "conftest.py"
    storage_state_path = Path(test_file_dir) / ".storage_state.json"
    storage_state_path.write_text(json.dumps(storage_state, ensure_ascii=False), encoding="utf-8")
    conftest_path.write_text(_CONFTEST_TEMPLATE, encoding="utf-8")
    return conftest_path, storage_state_path


async def _execute_code_background(
    run_id: str,
    test_file_path: str,
    login_role: str,
    task_id: str,
) -> None:
    """Background task: execute generated Playwright code via pytest once and update run status."""
    import subprocess

    async with _code_execution_semaphore:
        _active_code_execution[run_id] = datetime.now().isoformat()
        test_file_dir = str(Path(test_file_path).parent)

        try:
            storage_state = _build_storage_state(login_role)
            conftest_path, storage_state_path = _write_test_support_files(test_file_dir, storage_state)

            proc = subprocess.run(
                ["uv", "run", "pytest", test_file_path, "--timeout=60", "-v"],
                capture_output=True, text=True, timeout=120,
            )
            result_status = "success" if proc.returncode == 0 else "failed"
            logger.info(f"[{run_id}] pytest 执行完成: returncode={proc.returncode}, status={result_status}")

            async with async_session() as session:
                run_repo = RunRepository(session)
                await run_repo.update_status(run_id, result_status)
                if result_status == "success":
                    task_repo = TaskRepository(session)
                    await task_repo.update(task_id, TaskUpdate(status="success"))

        except Exception as e:
            logger.error(f"[{run_id}] 代码执行后台任务异常: {e}", exc_info=True)
            try:
                async with async_session() as session:
                    run_repo = RunRepository(session)
                    await run_repo.update_status(run_id, "failed")
            except Exception:
                pass
        finally:
            for p in (Path(test_file_dir) / "conftest.py", Path(test_file_dir) / ".storage_state.json"):
                try:
                    p.unlink(missing_ok=True)
                except Exception:
                    pass
            _active_code_execution.pop(run_id, None)


async def _run_preconditions(
    run_id: str,
    preconditions: list[str] | None,
    external_module_path: str | None,
    shared_cache: Any,
    run_repo: RunRepository,
    precondition_result_repo: PreconditionResultRepository,
    global_seq: int,
) -> tuple[dict[str, Any], str, int] | None:
    """Execute preconditions and return (context, task_description, global_seq).

    Returns None if a precondition fails (caller should return early).
    The task_description is returned unchanged; caller applies variable
    substitution using the returned context.
    """
    if not preconditions:
        return {}, "", global_seq

    precondition_service = PreconditionService(external_module_path=external_module_path, cache=shared_cache)

    for i, code in enumerate(preconditions):
        if not code.strip():
            continue

        # Send precondition running event
        code_display = code[:100] + "..." if len(code) > 100 else code
        pre_event = SSEPreconditionEvent(index=i, code=code_display, status="running")
        await event_manager.publish(run_id, f"event: precondition\ndata: {pre_event.model_dump_json()}\n\n")

        result = await precondition_service.execute_single(code, i)

        # Send precondition result event
        _safe_vars = _sanitize_variables(result.variables) if (result.success and result.variables) else None
        pre_event = SSEPreconditionEvent(
            index=i, code=code_display,
            status="success" if result.success else "failed",
            error=result.error, duration_ms=result.duration_ms, variables=_safe_vars,
        )
        await event_manager.publish(run_id, f"event: precondition\ndata: {pre_event.model_dump_json()}\n\n")

        # Persist precondition result (Phase 59)
        global_seq += 1
        await precondition_result_repo.create(
            run_id=run_id, sequence_number=global_seq, index=i, code=code,
            status="success" if result.success else "failed",
            error=result.error, duration_ms=result.duration_ms,
            variables=json.dumps(_safe_vars) if _safe_vars else None,
        )

        if not result.success:
            await run_repo.update_status(run_id, "failed")
            event_manager.set_status(run_id, "failed")
            finished = SSEFinishedEvent(status="failed", total_steps=0, duration_ms=0)
            await event_manager.publish(run_id, f"event: finished\ndata: {finished.model_dump_json()}\n\n")
            await event_manager.publish(run_id, None)
            return None

    context = precondition_service.get_context()
    logger.info(f"[{run_id}] 前置条件执行完成，变量: {list(context.keys())}")
    return context, "", global_seq


async def _run_auth_and_session(
    run_id: str,
    login_role: str | None,
    account_info: Any,
    login_url: str | None,
    shared_cache: Any,
    context: dict[str, Any],
    task_description: str,
    target_url: str | None,
    agent_service: AgentService,
    settings: Any,
) -> tuple[Any, str | None, str, bool]:
    """Handle programmatic login or fallback to text login.

    Returns (authenticated_session, effective_target_url, task_description, auth_pre_nav_ok).
    If login_role is None, returns (None, target_url, task_description, False).
    """
    if not login_role:
        return None, target_url, task_description, False

    from backend.core.test_flow_service import TestFlowService
    from backend.core.agent_service import create_browser_session
    from urllib.parse import urlparse

    flow = TestFlowService()
    cache_values = shared_cache.all() if shared_cache else {}

    authenticated_session = create_browser_session()
    _parsed = urlparse(settings.erp_base_url)
    effective_target_url = f"{_parsed.scheme}://{_parsed.netloc}"

    # Perform programmatic form login
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
        task_description = flow.replace_cached_variables_only(task_description, cache_values)
        logger.info(f"[{run_id}] 编程式登录成功，跳过登录步骤")
        return authenticated_session, effective_target_url, task_description, True

    # Fallback: close the failed session and rebuild task with login text
    logger.warning(
        f"[{run_id}] [代码登录回退] 角色={login_role} 原因=预导航失败，回退到文字登录模式"
    )
    try:
        await authenticated_session.stop()
    except Exception:
        pass

    task_description = flow._build_description(
        task_description=task_description, login_url=login_url,
        account=account_info.account, password=account_info.password,
        context=context if isinstance(context, dict) else {},
        cache_values=cache_values,
    )
    logger.info(f"[{run_id}] 回退文字登录，任务描述: {task_description[:150]}...")
    return None, None, task_description, False


async def _run_ui_assertions(
    run_id: str,
    run: Any,
    result: Any,
    assertion_service: AssertionService,
    assertion_result_repo: AssertionResultRepository,
    global_seq: int,
) -> tuple[str, int]:
    """Evaluate UI assertions from the task.

    Returns (final_status, global_seq). Status is 'failed' if any
    assertion fails, otherwise unchanged from the caller's determination.
    """
    if not run or not run.task or not run.task.assertions:
        return "", global_seq

    assertion_map = {a.id: a for a in run.task.assertions}
    assertion_results = await assertion_service.evaluate_all(
        run_id=run_id, assertions=run.task.assertions, history=result,
    )
    for ar in assertion_results:
        global_seq += 1
        await assertion_result_repo.update_sequence_number(ar.id, global_seq)
        source_assertion = assertion_map.get(ar.assertion_id)
        assertion_event = SSEAssertionEvent(
            assertion_id=ar.assertion_id,
            assertion_name=source_assertion.name if source_assertion else "未知断言",
            assertion_type=source_assertion.type if source_assertion else "unknown",
            status=ar.status, message=ar.message, actual_value=ar.actual_value,
        )
        await event_manager.publish(
            run_id, f"event: assertion\ndata: {assertion_event.model_dump_json()}\n\n"
        )

    if any(ar.status == "fail" for ar in assertion_results):
        logger.info(f"[{run_id}] 断言评估完成，存在失败断言，状态设为 failed")
        return "failed", global_seq

    logger.info(f"[{run_id}] 断言评估完成，全部通过")
    return "", global_seq


async def _publish_external_assertion_results(
    run_id: str,
    summary: dict,
    run_repo: RunRepository,
    event_manager_obj: Any,
    session: Any,
    global_seq: int,
) -> int:
    """Publish SSE events for each external assertion result and persist to DB.

    Returns the updated global_seq.
    """
    results_count = len(summary.get('results', []))
    for idx, ext_result in enumerate(summary.get('results', [])):
        global_seq += 1
        assertion_name = f"{ext_result.get('class_name', '?')}.{ext_result.get('method', '?')}"
        status_str = 'pass' if ext_result.get('passed') else 'fail'
        message_parts = []
        if ext_result.get('error'):
            message_parts.append(ext_result['error'])
        field_results = ext_result.get('field_results', [])
        for fr in field_results:
            fr_status = 'pass' if fr.get('passed') else 'fail'
            message_parts.append(f"{fr.get('field_name', '?')}: {fr_status}")
        ext_assertion_event = SSEAssertionEvent(
            assertion_id=f"ext-{idx}", assertion_name=assertion_name,
            assertion_type="external", status=status_str,
            message='; '.join(message_parts) if message_parts else None,
            actual_value=None, field_results=field_results if field_results else None,
        )
        await event_manager_obj.publish(
            run_id, f"event: assertion\ndata: {ext_assertion_event.model_dump_json()}\n\n"
        )

    # Send summary event
    summary_event = {
        "type": "external_assertions_complete", "total": summary['total'],
        "passed": summary['passed'], "failed": summary['failed'],
        "errors": summary['errors'], "timestamp": datetime.now().isoformat(),
    }
    await event_manager_obj.publish(
        run_id, f"event: external_assertions\ndata: {json.dumps(summary_event)}\n\n"
    )

    # Store external assertion results in DB for report
    run_obj = await run_repo.get(run_id)
    if run_obj:
        results_to_store = []
        for idx, ext_result in enumerate(summary.get('results', [])):
            results_to_store.append({
                "sequence_number": global_seq - results_count + idx + 1,
                "assertion_name": f"{ext_result.get('class_name', '?')}.{ext_result.get('method', '?')}",
                "status": 'pass' if ext_result.get('passed') else 'fail',
                "message": ext_result.get('error'),
                "field_results": ext_result.get('field_results'),
                "duration": ext_result.get('duration'),
            })
        run_obj.external_assertion_results = json.dumps(results_to_store)
        await session.commit()

    return global_seq


async def _run_external_assertions(
    run_id: str,
    external_assertions: list[dict] | None,
    context: dict[str, Any],
    shared_cache: Any,
    run_repo: RunRepository,
    event_manager_obj: Any,
    session: Any,
    global_seq: int,
) -> tuple[str, int]:
    """Execute external assertions and publish SSE events.

    Returns (final_status_delta, global_seq). final_status_delta is 'failed'
    if any external assertion failed/errored, otherwise empty string.
    """
    if not external_assertions:
        return "", global_seq

    from backend.core.precondition_service import ContextWrapper

    if not isinstance(context, ContextWrapper):
        context_wrapper = ContextWrapper(cache=shared_cache)
        context_wrapper._data = context.copy() if context else {}
    else:
        context_wrapper = context

    logger.info(f"[{run_id}] Starting external assertion execution ({len(external_assertions)} assertions)")

    try:
        summary = await execute_all_assertions(
            assertions=external_assertions, context=context_wrapper, timeout_per_assertion=30.0,
        )
        logger.info(
            f"[{run_id}] External assertions complete: "
            f"{summary['passed']}/{summary['total']} passed, "
            f"{summary['failed']} failed, {summary['errors']} errors"
        )

        global_seq = await _publish_external_assertion_results(
            run_id, summary, run_repo, event_manager_obj, session, global_seq,
        )
        context['external_assertion_summary'] = summary

        if summary['failed'] > 0 or summary['errors'] > 0:
            logger.info(f"[{run_id}] External assertions have failures/errors, status set to failed")
            return "failed", global_seq

    except Exception as e:
        logger.error(f"[{run_id}] External assertion execution failed: {e}", exc_info=True)
        await event_manager_obj.publish(
            run_id, f"event: external_assertions\ndata: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        )

    return "", global_seq


async def _run_code_generation(
    run_id: str,
    task_name: str,
    task_id: str,
    effective_target_url: str | None,
    run: Any,
    code_buffer: StepCodeBuffer,
    run_repo: RunRepository,
) -> None:
    """Assemble generated Playwright code from buffer and write to file."""
    try:
        from pathlib import Path as PathLib
        _precondition_config = {"target_url": effective_target_url} if effective_target_url else None
        _assertions_config = None
        if run and run.task and run.task.assertions:
            _assertions_config = [
                {"type": a.type, "expected": a.expected, "name": a.name}
                for a in run.task.assertions
            ]
        _content = code_buffer.assemble(
            run_id=run_id, task_name=task_name, task_id=task_id,
            precondition_config=_precondition_config, assertions_config=_assertions_config,
        )
        _output_dir = PathLib("outputs") / run_id / "generated"
        _output_dir.mkdir(parents=True, exist_ok=True)
        _output_path = _output_dir / f"test_{run_id}.py"
        _output_path.write_text(_content, encoding="utf-8")
        _code_path = str(_output_path)
        await run_repo.update_generated_code_path(run_id, _code_path)
        logger.info(f"[{run_id}] 生成 Playwright 代码: {_code_path}")
    except Exception as e:
        logger.error(f"[{run_id}] 代码生成失败（非阻塞）: {e}")


def _create_on_step(
    run_id: str,
    run_repo: RunRepository,
    code_buffer: StepCodeBuffer,
    counters: dict[str, int],
) -> Any:
    """Create on_step callback closure for agent step events.

    Uses mutable counters dict for step_count and global_seq instead
    of nonlocal (not possible across function boundary).
    """
    async def on_step(
        step: int, action: str, reasoning: str, screenshot_path: str | None,
        step_stats_json: str | None = None, action_dict: dict | None = None,
    ) -> None:
        counters["step_count"] = step
        counters["global_seq"] += 1
        # Save step to DB
        try:
            step_data = {
                "step_index": step, "action": action, "reasoning": reasoning,
                "screenshot_path": screenshot_path, "status": "success",
                "duration_ms": 0, "step_stats": step_stats_json,
                "sequence_number": counters["global_seq"],
            }
            await run_repo.add_step(run_id, step_data)
        except Exception as e:
            logger.error(f"[{run_id}] 保存步骤失败: {e}")
        # Send SSE step event
        screenshot_url = f"/runs/{run_id}/screenshots/{step}" if screenshot_path else None
        step_stats_dict = None
        if step_stats_json:
            try:
                step_stats_dict = json.loads(step_stats_json)
            except json.JSONDecodeError:
                pass
        event = SSEStepEvent(
            index=step, action=action, reasoning=reasoning,
            screenshot_url=screenshot_url, status="success",
            duration_ms=0, step_stats=step_stats_dict,
        )
        await event_manager.publish(run_id, f"event: step\ndata: {event.model_dump_json()}\n\n")
        # Incremental code translation (Phase 112, INTEG-01/D-02)
        if action_dict is not None:
            _duration = None
            if step_stats_json:
                try:
                    _stats = json.loads(step_stats_json)
                    _ms = _stats.get("duration_ms", 0)
                    _duration = _ms / 1000.0 if _ms > 0 else None
                except (json.JSONDecodeError, TypeError):
                    pass
            try:
                code_buffer.append_step(action_dict, duration=_duration)
            except Exception as _buf_err:
                logger.error(f"[{run_id}] buffer append 失败（非阻塞）: {_buf_err}")

    return on_step


def _resolve_login_context(
    login_role: str | None,
) -> tuple[Any, str | None, Any]:
    """Resolve login credentials and cache when login_role is set.

    Returns (account_info, login_url, shared_cache).
    All values are None when login_role is None.
    """
    if not login_role:
        return None, None, None
    from backend.core.account_service import account_service
    from backend.core.cache_service import CacheService
    account_info = account_service.resolve(login_role)
    login_url = account_info.get_login_url()
    shared_cache = CacheService()
    return account_info, login_url, shared_cache


async def _finalize_run(
    run_id: str,
    final_status: str,
    step_count: int,
    run_repo: RunRepository,
    report_service: ReportService,
) -> None:
    """Update run status, send finished event, and generate report."""
    await run_repo.update_status(run_id, final_status)
    event_manager.set_status(run_id, final_status)
    finished = SSEFinishedEvent(status=final_status, total_steps=step_count, duration_ms=0)
    await event_manager.publish(run_id, f"event: finished\ndata: {finished.model_dump_json()}\n\n")
    logger.info(f"[{run_id}] 已发送 finished 事件, status={final_status}")
    await report_service.generate_report(run_id)
    logger.info(f"[{run_id}] 报告已生成")


async def run_agent_background(
    run_id: str, task_id: str, task_name: str, task_description: str, max_steps: int,
    preconditions: list[str] | None = None, external_assertions: list[dict] | None = None,
    target_url: str | None = None, login_role: str | None = None,
) -> None:
    """后台执行 agent 任务 — pipeline orchestrator calling extracted sub-functions."""
    logger.info(f"[{run_id}] 开始后台执行: task_id={task_id}, task_name={task_name}, max_steps={max_steps}")
    llm_config = get_llm_config()
    settings = get_settings()
    account_info, login_url, shared_cache = _resolve_login_context(login_role)
    if login_role:
        logger.info(f"[{run_id}] 登录角色: {login_role}, 账号: {account_info.account}")

    async with async_session() as session:
        run_repo = RunRepository(session)
        agent_service = AgentService()
        report_service = ReportService(session)
        assertion_service = AssertionService(session)
        assertion_result_repo = AssertionResultRepository(session)
        precondition_result_repo = PreconditionResultRepository(session)

        # Step 1: preconditions
        precond_result = await _run_preconditions(
            run_id, preconditions, settings.erp_api_module_path, shared_cache,
            run_repo, precondition_result_repo, 0,
        )
        if precond_result is None:
            return
        context, _, global_seq = precond_result
        if context:
            task_description = PreconditionService.substitute_variables(task_description, context)

        # Step 2: auth and session
        authenticated_session, effective_target_url, task_description, _ = await _run_auth_and_session(
            run_id, login_role, account_info, login_url, shared_cache,
            context, task_description, target_url, agent_service, settings,
        )
        await run_repo.update_status(run_id, "running")
        started = SSEStartedEvent(run_id=run_id, task_id=task_id, task_name=task_name)
        await event_manager.publish(run_id, f"event: started\ndata: {started.model_dump_json()}\n\n")
        code_buffer = StepCodeBuffer(base_dir="outputs", run_id=run_id, llm_config=get_code_gen_llm_config())
        counters = {"step_count": 0, "global_seq": global_seq}
        on_step = _create_on_step(run_id, run_repo, code_buffer, counters)

        try:
            # Step 3: run agent
            result = await agent_service.run_with_cleanup(
                task=task_description, run_id=run_id, on_step=on_step,
                max_steps=max_steps, llm_config=llm_config,
                target_url=effective_target_url, browser_session=authenticated_session,
            )
            final_status = "success" if result.is_successful() else "failed"
            # Step 4: UI assertions
            run = await run_repo.get_with_task(run_id)
            ui_status, counters["global_seq"] = await _run_ui_assertions(
                run_id, run, result, assertion_service, assertion_result_repo, counters["global_seq"],
            )
            if ui_status == "failed":
                final_status = "failed"
            # Step 5: external assertions
            ext_status, counters["global_seq"] = await _run_external_assertions(
                run_id, external_assertions, context, shared_cache,
                run_repo, event_manager, session, counters["global_seq"],
            )
            if ext_status == "failed":
                final_status = "failed"
            # Step 6: finalize + code generation
            await _finalize_run(run_id, final_status, counters["step_count"], run_repo, report_service)
            await _run_code_generation(run_id, task_name, task_id, effective_target_url, run, code_buffer, run_repo)

        except Exception as e:
            logger.error(f"[{run_id}] 执行失败: {e}\n{traceback.format_exc()}")
            await run_repo.update_status(run_id, "failed")
            event_manager.set_status(run_id, "failed")
            await event_manager.publish(run_id, f"event: error\ndata: {SSEErrorEvent(error=str(e)).model_dump_json()}\n\n")
        finally:
            await event_manager.publish(run_id, None)
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
) -> list[RunResponse]:
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
) -> RunResponse:
    """创建执行记录并启动后台执行"""
    task = await task_repo.get(task_id)
    if not task:
        raise_not_found("Task", task_id)

    run = await run_repo.create(task_id=task_id)

    # 解析 preconditions 和 external_assertions
    preconditions, external_assertions = _parse_task_json_fields(task)

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
) -> RunResponse:
    """获取执行详情"""
    run = await run_repo.get(run_id)
    if not run:
        raise_not_found("Run", run_id)
    return run


@router.get("/{run_id}/code")
async def get_run_code(
    run_id: str,
    run_repo: RunRepository = Depends(get_run_repo),
) -> PlainTextResponse:
    """获取执行记录生成的 Playwright 代码内容 (CODE-01)"""
    run = await run_repo.get(run_id)
    if not run:
        raise_not_found("Run", run_id)
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
) -> dict:
    """触发 Playwright 代码执行 (CODE-02)"""
    # Pre-check 1: run exists
    run = await run_repo.get(run_id)
    if not run:
        raise_not_found("Run", run_id)

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

    # Update run status to "running" before starting
    async with async_session() as session:
        repo = RunRepository(session)
        await repo.update_status(run_id, "running")

    # Launch background execution
    background_tasks.add_task(
        _execute_code_background,
        run_id=run_id,
        test_file_path=run.generated_code_path,
        login_role=task.login_role,
        task_id=task.id,
    )

    return {"run_id": run_id, "status": "executing"}


@router.get("/{run_id}/stream")
async def stream_run(
    run_id: str,
    run_repo: RunRepository = Depends(get_run_repo),
) -> StreamingResponse:
    """SSE 订阅执行流"""
    # 验证 run 存在
    run = await run_repo.get(run_id)
    if not run:
        raise_not_found("Run", run_id)

    async def event_generator() -> AsyncGenerator[str, None]:
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
) -> dict:
    """停止执行"""
    run = await run_repo.get(run_id)
    if not run:
        raise_not_found("Run", run_id)

    if run.status != "running":
        raise HTTPException(status_code=400, detail="Run is not running")

    await run_repo.update_status(run_id, "stopped")
    return {"status": "stopped"}


@router.get("/{run_id}/screenshots/{step_index}")
async def get_screenshot(
    run_id: str,
    step_index: int,
    step_repo: StepRepository = Depends(get_step_repo),
) -> FileResponse:
    """获取截图"""
    step = await step_repo.get_by_index(run_id, step_index)

    if not step or not step.screenshot_path:
        raise_not_found("Screenshot")

    return FileResponse(
        step.screenshot_path,
        media_type="image/png",
    )
