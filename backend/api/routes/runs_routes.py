"""Run HTTP endpoint routes.

Split from runs.py per D-06: HTTP endpoints separated from pipeline logic.
Pipeline functions live in run_pipeline.py.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import AsyncGenerator

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from backend.api.helpers import _parse_task_json_fields, raise_not_found
from fastapi.responses import PlainTextResponse, StreamingResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import get_settings
from backend.db import get_db
from backend.db.database import async_session
from backend.db.repository import TaskRepository, RunRepository, StepRepository
from backend.db.schemas import RunResponse, TaskUpdate
from backend.core.event_manager import event_manager
from backend.core.error_utils import non_blocking_execute, silent_execute
from backend.api.routes.run_pipeline import run_agent_background

logger = logging.getLogger(__name__)

# Module-level concurrency guard for code execution (per D-08)
_code_execution_semaphore = asyncio.Semaphore(1)
_active_code_execution: dict[str, str] = {}  # run_id -> started_at ISO


def _format_code_with_line_numbers(content: str) -> str:
    """Format code with right-aligned line numbers (per D-01)."""
    lines = content.splitlines()
    max_width = len(str(len(lines)))
    formatted = [f"{i + 1:>{max_width}} | {line}" for i, line in enumerate(lines)]
    return "\n".join(formatted)


def _validate_code_path(code_path: str) -> Path:
    """Validate code path exists and is within outputs/ directory (per D-03)."""
    resolved = Path(code_path).resolve()
    outputs_root = Path("outputs").resolve()
    if not str(resolved).startswith(str(outputs_root)):
        raise HTTPException(status_code=403, detail="非法文件路径")
    if not resolved.exists():
        raise HTTPException(status_code=404, detail="代码文件不存在")
    return resolved


_CONFTEST_TEMPLATE = '''"""Auto-generated conftest: form-based login for ERP auth."""
import json
from pathlib import Path

import pytest
from playwright.sync_api import Page, BrowserContext


def _form_login(page: Page, origin: str, account: str, password: str) -> bool:
    """Perform real form login (same as browser-use _programmatic_login)."""
    page.goto(f"{origin}/login")
    page.wait_for_load_state("networkidle", timeout=10000)

    # Switch to password login tab if present
    tab_info = page.evaluate("""() => {
        var divs = document.querySelectorAll('div');
        for (var i = 0; i < divs.length; i++) {
            if (divs[i].textContent.trim() === '密码登录'
                && divs[i].offsetParent !== null) {
                var r = divs[i].getBoundingClientRect();
                return JSON.stringify({x: r.x + r.width/2, y: r.y + r.height/2});
            }
        }
        return null;
    }""")
    if tab_info:
        pos = json.loads(tab_info)
        page.mouse.click(pos['x'], pos['y'])
        page.wait_for_timeout(1000)

    # Fill account input via nativeInputValueSetter
    acc_ok = page.evaluate("""(account) => {
        var inp = document.querySelector('input[placeholder="请输入账号"]');
        if (!inp) {
            var all = document.querySelectorAll('input');
            for (var i = 0; i < all.length; i++) {
                if (all[i].placeholder && all[i].placeholder.indexOf('账号') >= 0) { inp = all[i]; break; }
            }
        }
        if (!inp) return false;
        var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(inp, account);
        inp.dispatchEvent(new Event('input', {bubbles: true}));
        inp.dispatchEvent(new Event('change', {bubbles: true}));
        return true;
    }""", account)
    if not acc_ok:
        return False

    page.wait_for_timeout(300)

    # Fill password input
    pwd_ok = page.evaluate("""(password) => {
        var inp = document.querySelector('input[placeholder="请输入密码"]');
        if (!inp) inp = document.querySelector('input[type="password"]');
        if (!inp) return false;
        var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(inp, password);
        inp.dispatchEvent(new Event('input', {bubbles: true}));
        inp.dispatchEvent(new Event('change', {bubbles: true}));
        return true;
    }""", password)
    if not pwd_ok:
        return False

    page.wait_for_timeout(300)

    # Click login button
    btn_info = page.evaluate("""() => {
        var btns = document.querySelectorAll('button');
        for (var i = 0; i < btns.length; i++) {
            var t = btns[i].textContent.trim();
            if (t === '登 录' || t === '登录' || t === 'Login') {
                var r = btns[i].getBoundingClientRect();
                return JSON.stringify({x: r.x + r.width/2, y: r.y + r.height/2, text: t});
            }
        }
        return null;
    }""")
    if not btn_info:
        return False

    pos = json.loads(btn_info)
    page.mouse.click(pos['x'], pos['y'])

    # Wait for redirect away from /login
    for _ in range(5):
        page.wait_for_timeout(2000)
        if "/login" not in page.url:
            return True
    return False


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Create authenticated page via real form login."""
    p = context.new_page()
    cred_file = Path(__file__).parent / ".login_credentials.json"
    if cred_file.exists():
        with open(cred_file, encoding="utf-8") as f:
            creds = json.load(f)
        _form_login(p, creds["origin"], creds["account"], creds["password"])
    return p
'''


async def _build_login_credentials(login_role: str) -> dict:
    """Build login credentials dict for the given role."""
    from backend.core.account_service import account_service
    from urllib.parse import urlparse

    account_info = account_service.resolve(login_role)
    settings = get_settings()
    parsed = urlparse(settings.erp_base_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    return {
        "origin": origin,
        "account": account_info.account,
        "password": account_info.password,
    }


def _write_test_support_files(test_file_dir: str, credentials: dict) -> tuple[Path, Path]:
    """Write conftest.py and .login_credentials.json to the test file directory."""
    conftest_path = Path(test_file_dir) / "conftest.py"
    cred_path = Path(test_file_dir) / ".login_credentials.json"
    cred_path.write_text(json.dumps(credentials, ensure_ascii=False), encoding="utf-8")
    conftest_path.write_text(_CONFTEST_TEMPLATE, encoding="utf-8")
    return conftest_path, cred_path


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
            credentials = await _build_login_credentials(login_role)
            conftest_path, cred_path = _write_test_support_files(test_file_dir, credentials)

            proc = subprocess.run(
                ["uv", "run", "pytest", test_file_path, "--timeout=60", "-v"],
                capture_output=True, text=True, timeout=120,
            )
            result_status = "success" if proc.returncode == 0 else "failed"
            logger.info(f"[{run_id}] pytest 执行完成: returncode={proc.returncode}, status={result_status}")
            if result_status == "failed":
                if proc.stdout:
                    logger.info(f"[{run_id}] pytest stdout:\n{proc.stdout}")
                if proc.stderr:
                    logger.warning(f"[{run_id}] pytest stderr:\n{proc.stderr}")

            async with async_session() as session:
                run_repo = RunRepository(session)
                await run_repo.update_status(run_id, result_status)
                if result_status == "success":
                    task_repo = TaskRepository(session)
                    await task_repo.update(task_id, TaskUpdate(status="success"))

        except Exception as e:
            logger.error(f"[{run_id}] 代码执行后台任务异常: {e}", exc_info=True)

            async def _mark_failed() -> None:
                async with async_session() as session:
                    run_repo = RunRepository(session)
                    await run_repo.update_status(run_id, "failed")

            await non_blocking_execute(
                _mark_failed,
                error_msg=f"[{run_id}] Failed to mark run as failed",
            )
        finally:
            for p in (Path(test_file_dir) / "conftest.py", Path(test_file_dir) / ".login_credentials.json"):
                silent_execute(p.unlink, missing_ok=True)
            _active_code_execution.pop(run_id, None)


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
