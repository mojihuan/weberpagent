"""E2E test for SelfHealingRunner repair pipeline (E2E-01, E2E-02).

Validates Plan 01 changes work end-to-end:
- Content-matching _apply_fix with multi-line replacement (HEAL-01)
- Code locator to DOM mapping (HEAL-02)
- Structured LLM repair prompt with 20-line context (HEAL-03)
- ast.parse rollback on invalid repair (HEAL-04)

Tests the full execute-code path: API endpoint -> background task ->
SelfHealingRunner -> LLMHealer (mocked) -> _apply_fix -> DB update.

These tests do NOT require DASHSCOPE_API_KEY -- LLM is mocked.
Playwright must be installed for the subprocess pytest execution.
"""

import asyncio
import shutil
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from backend.core.account_service import AccountInfo
from backend.core.llm_healer import LLMHealResult

# ---------------------------------------------------------------------------
# Playwright availability check
# ---------------------------------------------------------------------------


def _has_playwright() -> bool:
    """Check if Playwright chromium is installed."""
    return bool(shutil.which("playwright"))


pytestmark = pytest.mark.skipif(
    not _has_playwright(),
    reason="Playwright not installed",
)

# ---------------------------------------------------------------------------
# Sample test code strings
# ---------------------------------------------------------------------------

SAMPLE_FAILING_LOCATOR_TEST = '''"""Sample test with failing locator for healing pipeline E2E."""
from playwright.sync_api import Page


def test_e2e_healing_locator(page: Page) -> None:
    """Test that fails due to non-existent locator, then heals."""
    page.goto("https://example.com")
    page.get_by_text("NonExistentButton12345").click()
    assert "Example" in page.title() or page.title() != ""
'''

SAMPLE_SYNTAX_BREAK_TEST = '''"""Sample test for ast rollback E2E."""
from playwright.sync_api import Page


def test_e2e_healing_syntax(page: Page) -> None:
    """Test that receives a syntax-breaking repair from LLM."""
    page.goto("https://example.com")
    page.get_by_text("AnotherMissingButton9999").click()
    assert "Example" in page.title() or page.title() != ""
'''

# ---------------------------------------------------------------------------
# Polling helper
# ---------------------------------------------------------------------------

_EXEC_POLL_INTERVAL = 1
_EXEC_POLL_TIMEOUT = 180


async def _poll_execute_completion(
    client, run_id: str, timeout: int = _EXEC_POLL_TIMEOUT,
) -> dict:
    """Poll GET /api/runs/{run_id} until healing_status reaches terminal state."""
    loop = asyncio.get_event_loop()
    deadline = loop.time() + timeout
    while True:
        resp = await client.get(f"/api/runs/{run_id}")
        assert resp.status_code == 200
        data = resp.json()
        status = data.get("healing_status", "unknown")
        print(f"[E2E-Healing] Polling run {run_id}... healing_status={status}")
        if status in ("passed", "failed", "skipped"):
            return data
        remaining = deadline - loop.time()
        if remaining <= 0:
            raise TimeoutError(
                f"Execute did not complete in {timeout}s. Last healing_status: {status}"
            )
        await asyncio.sleep(min(_EXEC_POLL_INTERVAL, remaining))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_auth():
    """Mock auth chain to avoid ERP dependency."""
    with patch(
        "backend.core.self_healing_runner.auth_service.fetch_token",
    ) as mock_fetch, patch(
        "backend.core.account_service.account_service.resolve",
    ) as mock_resolve:
        mock_resolve.return_value = AccountInfo(
            account="test_user", password="test_pass", role="main",
        )
        mock_fetch.return_value = "fake-test-token-12345"
        yield


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _setup_mock_run(client, sample_code: str) -> str:
    """Create a Task, Run, write code file, update generated_code_path.

    Returns run_id.
    """
    from backend.db.database import async_session
    from backend.db.repository import RunRepository

    # Step 1: Create Task via API (must include login_role)
    task_resp = await client.post(
        "/api/tasks",
        json={
            "name": "E2E\u81ea\u6108\u4fee\u590d\u7ba1\u9053",
            "description": "\u9a8c\u8bc1\u81ea\u6108\u4fee\u590d\u94fe\u8def",
            "target_url": "",
            "max_steps": 3,
            "login_role": "main",
        },
    )
    assert task_resp.status_code == 200, f"POST /api/tasks failed: {task_resp.text}"
    task_id = task_resp.json()["id"]

    # Step 2: Create Run via API
    run_resp = await client.post("/api/runs", params={"task_id": task_id})
    assert run_resp.status_code == 200, f"POST /api/runs failed: {run_resp.text}"
    run_id = run_resp.json()["id"]

    # Step 3: Write code file
    code_path = Path(f"outputs/{run_id}/generated/test_{run_id}.py")
    code_path.parent.mkdir(parents=True, exist_ok=True)
    code_path.write_text(sample_code, encoding="utf-8")

    # Step 4: Update run.generated_code_path via DB
    async with async_session() as session:
        repo = RunRepository(session)
        run = await repo.get(run_id)
        assert run is not None, f"Run {run_id} not found in DB"
        run.generated_code_path = str(code_path)
        await session.commit()

    return run_id


async def _cleanup_outputs(run_id: str) -> None:
    """Remove generated outputs directory for this run."""
    output_dir = Path(f"outputs/{run_id}")
    if output_dir.exists():
        shutil.rmtree(output_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@pytest.mark.timeout(300)
async def test_execute_code_healing_with_failing_locator(api_client, mock_auth):
    """E2E-01: Full healing pipeline with failing locator -> mock LLM repair -> terminal state.

    Exercises:
    - SelfHealingRunner.run() retry loop
    - LLMHealer.repair_code() returns structured target_snippet/replacement
    - _apply_fix content-matching replacement
    - Pipeline reaches a terminal state (not stuck in 'healing')
    - error_category is populated
    """
    run_id = None
    try:
        run_id = await _setup_mock_run(api_client, SAMPLE_FAILING_LOCATOR_TEST)
        print(f"[E2E-Healing] Created mock run {run_id}")

        # Mock LLMHealer.repair_code to return a valid structured repair
        # target_snippet must be >= 20 chars and match a portion of the test code
        target_snippet = 'page.get_by_text("NonExistentButton12345").click()'
        replacement = 'page.get_by_text("More information").click()'

        with patch(
            "backend.core.self_healing_runner.LLMHealer",
        ) as mock_healer_cls:
            mock_healer_instance = AsyncMock()
            mock_healer_cls.return_value = mock_healer_instance
            mock_healer_instance.repair_code.return_value = LLMHealResult(
                success=True,
                code_snippet=replacement,
                raw_response='{"target_snippet": "...", "replacement": "..."}',
                locator='page.get_by_text("More information")',
                target_snippet=target_snippet,
                replacement=replacement,
            )

            # Trigger execute-code
            exec_resp = await api_client.post(
                f"/api/runs/{run_id}/execute-code",
            )
            assert (
                exec_resp.status_code == 202
            ), f"execute-code failed: {exec_resp.text}"
            exec_data = exec_resp.json()
            assert exec_data["status"] == "healing"

            # Poll for completion
            final_run = await _poll_execute_completion(api_client, run_id)

        healing_status = final_run.get("healing_status", "unknown")
        error_category = final_run.get("healing_error_category", "")
        healing_error = final_run.get("healing_error")

        # Verify terminal state (passed or failed, not stuck)
        assert healing_status in ("passed", "failed"), (
            f"Expected terminal healing_status, got '{healing_status}'. "
            f"healing_error: {healing_error}"
        )
        # error_category must be non-empty
        assert error_category not in (None, ""), (
            f"Expected non-empty error_category, got '{error_category}'. "
            f"healing_status={healing_status}"
        )
        print(
            f"[E2E-Healing] Healing pipeline completed: "
            f"healing_status={healing_status}, error_category={error_category}"
        )
    finally:
        if run_id:
            await _cleanup_outputs(run_id)


@pytest.mark.asyncio
@pytest.mark.timeout(300)
async def test_execute_code_ast_rollback(api_client, mock_auth):
    """E2E-02: ast.parse rollback prevents syntax-breaking repairs.

    Mock LLM returns a repair that would create invalid Python (missing
    closing paren). _apply_fix should return None (ast.parse rollback),
    so healing eventually fails after max retries.

    Verifies:
    - _apply_fix returns None on SyntaxError (rollback)
    - healing_status == "failed"
    - Pipeline does not get stuck
    """
    run_id = None
    try:
        run_id = await _setup_mock_run(api_client, SAMPLE_SYNTAX_BREAK_TEST)
        print(f"[E2E-Healing] Created mock run {run_id} (syntax break test)")

        # Mock LLMHealer.repair_code to return syntax-breaking repair
        target_snippet = 'page.get_by_text("AnotherMissingButton9999").click()'
        # Intentional syntax error: missing closing parenthesis
        replacement = 'page.get_by_text("More information").click('

        with patch(
            "backend.core.self_healing_runner.LLMHealer",
        ) as mock_healer_cls:
            mock_healer_instance = AsyncMock()
            mock_healer_cls.return_value = mock_healer_instance
            mock_healer_instance.repair_code.return_value = LLMHealResult(
                success=True,
                code_snippet=replacement,
                raw_response='{"target_snippet": "...", "replacement": "..."}',
                locator='page.get_by_text("More information")',
                target_snippet=target_snippet,
                replacement=replacement,
            )

            # Trigger execute-code
            exec_resp = await api_client.post(
                f"/api/runs/{run_id}/execute-code",
            )
            assert (
                exec_resp.status_code == 202
            ), f"execute-code failed: {exec_resp.text}"

            # Poll for completion
            final_run = await _poll_execute_completion(api_client, run_id)

        healing_status = final_run.get("healing_status", "unknown")
        healing_error = final_run.get("healing_error")
        error_category = final_run.get("healing_error_category", "")

        # Must be failed (syntax-breaking repair should be rejected by ast.parse)
        assert healing_status == "failed", (
            f"Expected healing_status='failed' (syntax rollback), "
            f"got '{healing_status}'. healing_error: {healing_error}"
        )
        # error_category must be populated
        assert error_category not in (None, ""), (
            f"Expected non-empty error_category, got '{error_category}'. "
            f"healing_status={healing_status}"
        )
        assert healing_error is not None, "healing_error should contain failure details"
        print(
            f"[E2E-Healing] AST rollback test completed: "
            f"healing_status={healing_status}, error_category={error_category}"
        )
    finally:
        if run_id:
            await _cleanup_outputs(run_id)
