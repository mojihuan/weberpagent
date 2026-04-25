"""E2E test for execute-code pipeline (E2E-01).

Validates that Phase 102/103 fixes work end-to-end via mock-based testing.
Tests the full execute-code path: API endpoint -> background task ->
SelfHealingRunner -> subprocess pytest -> DB update -> API response with error_category.

These tests do NOT require DASHSCOPE_API_KEY or ERP_BASE_URL -- auth is mocked.
"""

import asyncio
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from backend.core.account_service import AccountInfo

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

SAMPLE_PASSING_TEST = '''"""Sample passing test for E2E verification."""
from playwright.sync_api import Page


def test_e2e_sample(page: Page) -> None:
    """Simple test that navigates and verifies page title."""
    page.goto("https://example.com")
    assert "Example" in page.title() or page.title() != ""
'''

SAMPLE_FAILING_TEST = '''"""Sample failing test for E2E verification."""
from playwright.sync_api import Page


def test_e2e_sample_fail(page: Page) -> None:
    """Simple test that fails with assertion error."""
    page.goto("https://example.com")
    assert "NonExistentString12345" in page.title()
'''

# ---------------------------------------------------------------------------
# Polling helper
# ---------------------------------------------------------------------------

_EXEC_POLL_INTERVAL = 2
_EXEC_POLL_TIMEOUT = 60


async def _poll_execute_completion(
    client, run_id: str, timeout: int = _EXEC_POLL_TIMEOUT
) -> dict:
    """Poll GET /api/runs/{run_id} until healing_status reaches terminal state."""
    loop = asyncio.get_event_loop()
    deadline = loop.time() + timeout
    while True:
        resp = await client.get(f"/api/runs/{run_id}")
        assert resp.status_code == 200
        data = resp.json()
        status = data.get("healing_status", "unknown")
        print(f"[E2E-Exec] Polling run {run_id}... healing_status={status}")
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
    """Mock auth chain to avoid ERP dependency.

    auth_service is imported at module level in self_healing_runner, so patch
    at the import location. account_service is lazily imported inside a
    function, so patch at the original module source.
    """
    with patch(
        "backend.core.self_healing_runner.auth_service.fetch_token"
    ) as mock_fetch, patch(
        "backend.core.account_service.account_service.resolve"
    ) as mock_resolve:
        mock_resolve.return_value = AccountInfo(
            account="test_user", password="test_pass", role="main"
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
            "name": "E2E\u6267\u884c\u9a8c\u8bc1-\u901a\u8fc7\u6d4b\u8bd5",
            "description": "\u9a8c\u8bc1 pytest \u6267\u884c\u94fe\u8def",
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
async def test_execute_code_passing(api_client, mock_auth):
    """E2E-01: Execute-code with passing test -> healing_status='passed', error_category non-empty."""
    run_id = None
    try:
        # Setup
        run_id = await _setup_mock_run(api_client, SAMPLE_PASSING_TEST)
        print(f"[E2E-Exec] Created mock run {run_id}")

        # Trigger execute-code
        exec_resp = await api_client.post(f"/api/runs/{run_id}/execute-code")
        assert exec_resp.status_code == 202, f"execute-code failed: {exec_resp.text}"
        exec_data = exec_resp.json()
        assert exec_data["status"] == "healing"

        # Poll for completion
        final_run = await _poll_execute_completion(api_client, run_id)
        healing_status = final_run.get("healing_status", "unknown")
        error_category = final_run.get("healing_error_category", "")
        healing_error = final_run.get("healing_error")

        # Verify terminal status
        assert healing_status == "passed", (
            f"Expected healing_status='passed', got '{healing_status}'. "
            f"healing_error: {healing_error}"
        )
        # error_category must be non-empty ('passed' for success)
        assert error_category not in (None, ""), (
            f"Expected non-empty error_category, got '{error_category}'. "
            f"healing_status={healing_status}"
        )
        print(
            f"[E2E-Exec] PASS test completed: "
            f"healing_status={healing_status}, error_category={error_category}"
        )
    finally:
        if run_id:
            await _cleanup_outputs(run_id)


@pytest.mark.asyncio
async def test_execute_code_failing(api_client, mock_auth):
    """E2E-01: Execute-code with failing test -> healing_status='failed', error_category is non-empty."""
    run_id = None
    try:
        # Setup with failing test code
        run_id = await _setup_mock_run(api_client, SAMPLE_FAILING_TEST)
        print(f"[E2E-Exec] Created mock run {run_id} (failing test)")

        # Trigger execute-code
        exec_resp = await api_client.post(f"/api/runs/{run_id}/execute-code")
        assert exec_resp.status_code == 202, f"execute-code failed: {exec_resp.text}"

        # Poll for completion
        final_run = await _poll_execute_completion(api_client, run_id)
        healing_status = final_run.get("healing_status", "unknown")
        healing_error = final_run.get("healing_error")
        error_category = final_run.get("healing_error_category", "")

        # Verify status is 'failed'
        assert healing_status == "failed", (
            f"Expected healing_status='failed', got '{healing_status}'. "
            f"healing_error: {healing_error}"
        )
        # error_category must be non-empty and non-None
        assert error_category not in (None, ""), (
            f"Expected non-empty error_category, got '{error_category}'. "
            f"healing_status={healing_status}, healing_error={healing_error}"
        )
        # Verify error info is present
        assert healing_error is not None, "healing_error should contain failure details"
        assert len(healing_error) > 0, "healing_error should not be empty"
        print(
            f"[E2E-Exec] FAIL test completed: "
            f"healing_status={healing_status}, error_category={error_category}"
        )
    finally:
        if run_id:
            await _cleanup_outputs(run_id)
