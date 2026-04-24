"""Unit tests for SelfHealingRunner -- pytest re-execution orchestrator.

Tests mock auth_service, LLMHealer, and subprocess calls to avoid
real network/browser/subprocess dependencies.

Covers:
  1. Skip when login_role is None (D-04)
  2. Skip when AuthService raises TokenFetchError (D-04)
  3. Pass on first pytest success (D-08)
  4. Retry on failure then pass after LLM repair (D-06, D-07)
  5. Failed after max 2 retries (D-07)
  6. Timeout handling (RESEARCH Pitfall 3)
  7. Conftest generation with browser_context_args fixture
  8. Error truncation keeping tail
  9. LLM repair applies fix and validates syntax
"""

import asyncio
import dataclasses
import json
import subprocess
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.core.auth_service import TokenFetchError
from backend.core.llm_healer import LLMHealResult
from backend.core.self_healing_runner import (
    CONFTEST_TEMPLATE,
    HealingResult,
    SelfHealingRunner,
    _build_storage_state,
    _get_storage_state_for_role,
)
from backend.core.account_service import AccountInfo
from backend.config.settings import Settings


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

LLM_CONFIG = {"model": "test-model", "api_key": "test-key"}
STORAGE_STATE = {
    "cookies": [],
    "origins": [
        {
            "origin": "https://example.com",
            "localStorage": [{"name": "Admin-Token", "value": "jwt-token"}],
        }
    ],
}


@pytest.fixture
def runner() -> SelfHealingRunner:
    """Create SelfHealingRunner with test LLM config."""
    return SelfHealingRunner(LLM_CONFIG)


@pytest.fixture
def tmp_test_dir(tmp_path: Path) -> Path:
    """Create a temp directory with a test file."""
    test_file = tmp_path / "test_example.py"
    test_file.write_text(
        'from playwright.sync_api import Page\n\n'
        'def test_demo(page: Page) -> None:\n'
        "    page.goto('https://example.com')\n"
        "    page.locator('button').click()\n",
        encoding="utf-8",
    )
    return tmp_path


def _make_completed_process(
    returncode: int = 0,
    stdout: str = "",
    stderr: str = "",
) -> subprocess.CompletedProcess:
    """Create a CompletedProcess mock."""
    return subprocess.CompletedProcess(
        args=["pytest"],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


# ---------------------------------------------------------------------------
# Test 1: Skip when login_role is None (D-04)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_skip_no_login_role(runner: SelfHealingRunner, tmp_test_dir: Path):
    """run() returns skipped when login_role is None."""
    test_file = str(tmp_test_dir / "test_example.py")
    result = await runner.run("run1", test_file, login_role=None)

    assert result.final_status == "skipped"
    assert result.attempts == 0
    assert result.error_message == ""


# ---------------------------------------------------------------------------
# Test 2: Skip when AuthService raises TokenFetchError (D-04)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_skip_auth_service_failure(runner: SelfHealingRunner, tmp_test_dir: Path):
    """run() returns skipped when AuthService raises TokenFetchError."""
    test_file = str(tmp_test_dir / "test_example.py")

    with patch(
        "backend.core.self_healing_runner._get_storage_state_for_role",
        new_callable=AsyncMock,
        side_effect=TokenFetchError(role="main", reason="请求超时"),
    ):
        result = await runner.run("run1", test_file, login_role="main")

    assert result.final_status == "skipped"
    assert result.attempts == 0
    assert "超时" in result.error_message


# ---------------------------------------------------------------------------
# Test 3: Pass on first try (D-08)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_passed_on_first_try(runner: SelfHealingRunner, tmp_test_dir: Path):
    """run() returns passed when pytest exit code is 0 on first attempt."""
    test_file = str(tmp_test_dir / "test_example.py")

    with (
        patch(
            "backend.core.self_healing_runner._get_storage_state_for_role",
            new_callable=AsyncMock,
            return_value=STORAGE_STATE,
        ),
        patch(
            "backend.core.self_healing_runner.asyncio.to_thread",
            new_callable=AsyncMock,
        ) as mock_to_thread,
    ):
        mock_to_thread.return_value = _make_completed_process(returncode=0)

        result = await runner.run("run1", test_file, login_role="main")

    assert result.final_status == "passed"
    assert result.attempts == 1


# ---------------------------------------------------------------------------
# Test 3b: pytest args exclude --headed (EXEC-01)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_pytest_args_no_headed(runner: SelfHealingRunner, tmp_test_dir: Path):
    """subprocess.run args 不包含 --headed 或 --headed=false (per EXEC-01)."""
    test_file = str(tmp_test_dir / "test_example.py")

    with (
        patch(
            "backend.core.self_healing_runner._get_storage_state_for_role",
            new_callable=AsyncMock,
            return_value=STORAGE_STATE,
        ),
        patch(
            "backend.core.self_healing_runner.asyncio.to_thread",
            new_callable=AsyncMock,
        ) as mock_to_thread,
    ):
        mock_to_thread.return_value = _make_completed_process(returncode=0)

        await runner.run("run1", test_file, login_role="main")

    # 提取 subprocess.run 的 args 参数
    call_args = mock_to_thread.call_args
    # asyncio.to_thread(subprocess.run, [args...], ...) -> call_args[0][1] is the list
    pytest_args = call_args[0][1]
    headed_args = [arg for arg in pytest_args if str(arg).startswith("--headed")]
    assert headed_args == [], f"pytest args 包含 --headed 参数: {headed_args}"


# ---------------------------------------------------------------------------
# Test 4: Retry on failure then pass (D-06, D-07)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_retry_on_failure_then_pass(
    runner: SelfHealingRunner, tmp_test_dir: Path
):
    """run() calls _llm_repair on failure and retries, passes on second attempt."""
    test_file = str(tmp_test_dir / "test_example.py")

    with (
        patch(
            "backend.core.self_healing_runner._get_storage_state_for_role",
            new_callable=AsyncMock,
            return_value=STORAGE_STATE,
        ),
        patch(
            "backend.core.self_healing_runner.asyncio.to_thread",
            new_callable=AsyncMock,
        ) as mock_to_thread,
        patch(
            "backend.core.self_healing_runner.LLMHealer"
        ) as mock_healer_cls,
    ):
        # First call fails, second call passes
        mock_to_thread.side_effect = [
            _make_completed_process(returncode=1, stderr="AssertionError"),
            _make_completed_process(returncode=0),
        ]

        # LLMHealer returns successful repair
        mock_healer = MagicMock()
        mock_healer.heal = AsyncMock(
            return_value=LLMHealResult(
                success=True,
                code_snippet="page.locator('button').click()",
                raw_response="page.locator('button').click()",
                locator="page.locator('button')",
            )
        )
        mock_healer_cls.return_value = mock_healer

        result = await runner.run("run1", test_file, login_role="main")

    assert result.final_status == "passed"
    assert result.attempts == 2
    mock_healer_cls.assert_called_once_with(LLM_CONFIG)


# ---------------------------------------------------------------------------
# Test 5: Max retries then failed (D-07)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_max_retries_then_failed(
    runner: SelfHealingRunner, tmp_test_dir: Path
):
    """run() returns failed after max 2 retries (3 total iterations)."""
    test_file = str(tmp_test_dir / "test_example.py")

    with (
        patch(
            "backend.core.self_healing_runner._get_storage_state_for_role",
            new_callable=AsyncMock,
            return_value=STORAGE_STATE,
        ),
        patch(
            "backend.core.self_healing_runner.asyncio.to_thread",
            new_callable=AsyncMock,
        ) as mock_to_thread,
        patch(
            "backend.core.self_healing_runner.LLMHealer"
        ) as mock_healer_cls,
    ):
        # All calls fail
        mock_to_thread.return_value = _make_completed_process(
            returncode=1, stderr="AssertionError in test"
        )

        # LLMHealer returns success but pytest still fails
        mock_healer = MagicMock()
        mock_healer.heal = AsyncMock(
            return_value=LLMHealResult(
                success=True,
                code_snippet="page.locator('#btn').click()",
                raw_response="page.locator('#btn').click()",
                locator="page.locator('#btn')",
            )
        )
        mock_healer_cls.return_value = mock_healer

        result = await runner.run("run1", test_file, login_role="main")

    assert result.final_status == "failed"
    assert result.attempts == 3


# ---------------------------------------------------------------------------
# Test 6: Timeout handling (RESEARCH Pitfall 3)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_timeout_handling(runner: SelfHealingRunner, tmp_test_dir: Path):
    """run() handles subprocess.TimeoutExpired as failure."""
    test_file = str(tmp_test_dir / "test_example.py")

    with (
        patch(
            "backend.core.self_healing_runner._get_storage_state_for_role",
            new_callable=AsyncMock,
            return_value=STORAGE_STATE,
        ),
        patch(
            "backend.core.self_healing_runner.asyncio.to_thread",
            new_callable=AsyncMock,
        ) as mock_to_thread,
        patch(
            "backend.core.self_healing_runner.LLMHealer"
        ) as mock_healer_cls,
    ):
        # All calls timeout
        mock_to_thread.side_effect = subprocess.TimeoutExpired(
            cmd=["pytest"], timeout=120
        )

        # LLMHealer returns success but pytest keeps timing out
        mock_healer = MagicMock()
        mock_healer.heal = AsyncMock(
            return_value=LLMHealResult(
                success=True,
                code_snippet="page.locator('#fix').click()",
                raw_response="page.locator('#fix').click()",
                locator="page.locator('#fix')",
            )
        )
        mock_healer_cls.return_value = mock_healer

        result = await runner.run("run1", test_file, login_role="main")

    assert result.final_status == "failed"
    assert "超时" in result.error_message


# ---------------------------------------------------------------------------
# Test 7: Conftest generation
# ---------------------------------------------------------------------------


def test_conftest_generation(runner: SelfHealingRunner, tmp_path: Path):
    """_generate_conftest creates valid conftest.py with browser_context_args."""
    runner._generate_conftest(tmp_path)

    conftest_path = tmp_path / "conftest.py"
    assert conftest_path.exists()

    content = conftest_path.read_text(encoding="utf-8")
    assert "browser_context_args" in content
    assert "storage_state" in content
    assert ".storage_state.json" in content


# ---------------------------------------------------------------------------
# Test 8: Error truncation
# ---------------------------------------------------------------------------


def test_truncate_error(runner: SelfHealingRunner):
    """_truncate_error truncates long errors, keeping tail."""
    long_error = "x" * 3000
    result = SelfHealingRunner._truncate_error(long_error, max_length=2000)

    assert len(result) <= 2000
    assert result.startswith("...")
    assert result.endswith("x")


def test_truncate_error_short(runner: SelfHealingRunner):
    """_truncate_error preserves short errors unchanged."""
    short_error = "short error"
    result = SelfHealingRunner._truncate_error(short_error, max_length=2000)

    assert result == short_error


# ---------------------------------------------------------------------------
# Test 9: LLM repair applies fix to test file
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_llm_repair_applies_fix(
    runner: SelfHealingRunner, tmp_test_dir: Path
):
    """_llm_repair applies LLM fix to test file and validates syntax."""
    test_file = tmp_test_dir / "test_example.py"
    original_content = test_file.read_text(encoding="utf-8")

    # Create a DOM snapshot for the repair to read
    dom_dir = tmp_test_dir.parent / "run1" / "dom"
    dom_dir.mkdir(parents=True, exist_ok=True)
    (dom_dir / "step_1.txt").write_text("<button>Fixed</button>", encoding="utf-8")

    with patch(
        "backend.core.self_healing_runner.LLMHealer"
    ) as mock_healer_cls:
        mock_healer = MagicMock()
        mock_healer.heal = AsyncMock(
            return_value=LLMHealResult(
                success=True,
                code_snippet="    page.locator('#new-btn').click()",
                raw_response="page.locator('#new-btn').click()",
                locator="page.locator('#new-btn')",
            )
        )
        mock_healer_cls.return_value = mock_healer

        # Provide error with line number pointing to a page. line
        error_output = "test_example.py:4: AssertionError"
        result = await runner._llm_repair(
            "run1", str(test_file), error_output, str(tmp_test_dir.parent)
        )

    assert result is True

    repaired_content = test_file.read_text(encoding="utf-8")
    assert repaired_content != original_content
    assert "#new-btn" in repaired_content


# ---------------------------------------------------------------------------
# Bonus: HealingResult is frozen
# ---------------------------------------------------------------------------


def test_healing_result_is_frozen():
    """HealingResult is a frozen dataclass (immutable per project convention)."""
    result = HealingResult(
        final_status="passed",
        attempts=1,
        error_message="",
        repaired_code_path="/tmp/test.py",
    )
    assert dataclasses.is_dataclass(result)
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.final_status = "failed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Tests for _build_storage_state (per D-05)
# ---------------------------------------------------------------------------


def test_build_storage_state_token_in_localstorage():
    """_build_storage_state puts token into localStorage with correct keys."""
    with patch(
        "backend.config.settings.get_settings",
        return_value=Settings(erp_base_url="https://erp.example.com/epbox_erp"),
    ):
        result = _build_storage_state("my-jwt-token-123")

    assert result["cookies"] == []
    assert len(result["origins"]) == 1
    assert result["origins"][0]["origin"] == "https://erp.example.com"
    ls = {item["name"]: item["value"] for item in result["origins"][0]["localStorage"]}
    assert ls["Admin-Token"] == "my-jwt-token-123"
    assert ls["Admin-Expires-In"] == "720"


def test_build_storage_state_origin_with_port():
    """_build_storage_state preserves port in origin when URL has one."""
    with patch(
        "backend.config.settings.get_settings",
        return_value=Settings(erp_base_url="https://erp.example.com:8443/epbox_erp"),
    ):
        result = _build_storage_state("token-abc")

    assert result["origins"][0]["origin"] == "https://erp.example.com:8443"


# ---------------------------------------------------------------------------
# Tests for _get_storage_state_for_role (per D-06)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_storage_state_for_role_success():
    """_get_storage_state_for_role resolves credentials, fetches token, builds state."""
    with (
        patch("backend.core.account_service.account_service") as mock_acct,
        patch("backend.core.self_healing_runner.auth_service") as mock_auth,
        patch(
            "backend.config.settings.get_settings",
            return_value=Settings(erp_base_url="https://erp.example.com"),
        ),
    ):
        mock_acct.resolve.return_value = AccountInfo(
            account="Y59800075", password="secret", role="main",
        )
        mock_auth.fetch_token = AsyncMock(return_value="jwt-token-xyz")

        result = await _get_storage_state_for_role("main")

    mock_acct.resolve.assert_called_once_with("main")
    mock_auth.fetch_token.assert_awaited_once_with(
        "Y59800075", "secret", role="main",
    )
    ls = {i["name"]: i["value"] for i in result["origins"][0]["localStorage"]}
    assert ls["Admin-Token"] == "jwt-token-xyz"


@pytest.mark.asyncio
async def test_get_storage_state_for_role_fetch_fails():
    """_get_storage_state_for_role propagates TokenFetchError from fetch_token."""
    with (
        patch("backend.core.account_service.account_service") as mock_acct,
        patch("backend.core.self_healing_runner.auth_service") as mock_auth,
    ):
        mock_acct.resolve.return_value = AccountInfo(
            account="Y59800075", password="secret", role="main",
        )
        mock_auth.fetch_token = AsyncMock(
            side_effect=TokenFetchError(role="main", reason="请求超时 (>10s)"),
        )

        with pytest.raises(TokenFetchError) as exc_info:
            await _get_storage_state_for_role("main")

    assert "main" in str(exc_info.value)
    assert "超时" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_storage_state_for_role_unknown_role():
    """_get_storage_state_for_role propagates ValueError from resolve."""
    with patch("backend.core.account_service.account_service") as mock_acct:
        mock_acct.resolve.side_effect = ValueError(
            "unknown role: 'nonexistent'. available roles: camera, idle, main, ..."
        )

        with pytest.raises(ValueError) as exc_info:
            await _get_storage_state_for_role("nonexistent")

    assert "nonexistent" in str(exc_info.value)
