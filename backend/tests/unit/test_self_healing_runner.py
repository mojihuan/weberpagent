"""Unit tests for SelfHealingRunner -- slimmed.

Keeps 3 core tests:
  1. Normal retry success (pass on first try)
  2. Retry exhaustion -> failed
  3. Error category classification (ENV_INTERRUPT skips LLM)
"""

import subprocess
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.core.llm_healer import LLMHealResult
from backend.core.self_healing_runner import SelfHealingRunner


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
    return SelfHealingRunner(LLM_CONFIG)


@pytest.fixture
def tmp_test_dir(tmp_path: Path) -> Path:
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
    return subprocess.CompletedProcess(
        args=["pytest"],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_passed_on_first_try(runner: SelfHealingRunner, tmp_test_dir: Path):
    """Normal retry success: pass when pytest exit code is 0 on first attempt."""
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


@pytest.mark.asyncio
async def test_max_retries_then_failed(runner: SelfHealingRunner, tmp_test_dir: Path):
    """Retry exhaustion: returns failed after max 2 retries (3 total iterations)."""
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
        mock_to_thread.return_value = _make_completed_process(
            returncode=1, stderr="AssertionError in test"
        )

        mock_healer = MagicMock()
        mock_healer.repair_code = AsyncMock(
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


@pytest.mark.asyncio
async def test_env_error_skips_llm_repair(runner: SelfHealingRunner, tmp_test_dir: Path):
    """Error category: exit code 2 -> ENV_INTERRUPT, skips LLM repair."""
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
        mock_to_thread.return_value = _make_completed_process(
            returncode=2, stderr="KeyboardInterrupt"
        )
        result = await runner.run("run1", test_file, login_role="main")
    assert result.final_status == "failed"
    assert result.attempts == 1
    assert result.error_category == "ENV_INTERRUPT"
    mock_healer_cls.assert_not_called()


# ---------------------------------------------------------------------------
# Phase 107: _apply_fix content-matching, locator extraction, DOM search
# ---------------------------------------------------------------------------


# --- _apply_fix tests (HEAL-01, HEAL-04) ---


def test_apply_fix_content_match_single_line():
    """_apply_fix replaces single-line target_snippet with replacement."""
    code = (
        "def test_example():\n"
        "    page.get_by_text('提交按钮这是一个长定位器').click()\n"
        "    page.goto('https://example.com')\n"
    )
    result = SelfHealingRunner._apply_fix(
        code,
        "    page.get_by_text('提交按钮这是一个长定位器').click()",
        "    page.locator('#submit').click()",
    )
    assert result is not None
    assert "page.locator('#submit').click()" in result
    assert "page.get_by_text('提交按钮这是一个长定位器')" not in result
    assert "page.goto('https://example.com')" in result


def test_apply_fix_multi_line_expansion():
    """1-line target -> 4-line try-except replacement, line count increases."""
    code = (
        "def test_example():\n"
        "    page.get_by_text('提交订单按钮这是一个非常长的定位器文本').click()\n"
        "    page.goto('https://example.com')\n"
    )
    # Target includes the indentation so it matches exactly in code
    target = "    page.get_by_text('提交订单按钮这是一个非常长的定位器文本').click()"
    replacement = (
        "    try:\n"
        "        page.get_by_text('提交订单').click()\n"
        "    except Exception:\n"
        "        page.locator('#submit').click()"
    )
    result = SelfHealingRunner._apply_fix(code, target, replacement)
    assert result is not None
    assert "try:" in result
    assert "except Exception:" in result
    original_lines = code.count("\n")
    result_lines = result.count("\n")
    assert result_lines == original_lines + 3  # 1 line -> 4 lines = +3


def test_apply_fix_multi_line_shrink():
    """3-line target -> 1-line replacement, line count decreases by 2."""
    code = (
        "def test_example():\n"
        "    try:\n"
        "        page.get_by_text('提交订单按钮这是一个非常长的定位器文本').click()\n"
        "    except Exception:\n"
        "        pass\n"
        "    page.goto('https://example.com')\n"
    )
    target = (
        "    try:\n"
        "        page.get_by_text('提交订单按钮这是一个非常长的定位器文本').click()\n"
        "    except Exception:\n"
        "        pass"
    )
    replacement = "    page.locator('#submit').click()"
    result = SelfHealingRunner._apply_fix(code, target, replacement)
    assert result is not None
    assert "page.locator('#submit').click()" in result
    assert "try:" not in result
    original_lines = code.count("\n")
    result_lines = result.count("\n")
    # 4-line target replaced by 1-line = -3 newlines
    assert result_lines == original_lines - 3


def test_apply_fix_target_not_found():
    """target_snippet not in code -> returns None."""
    code = "def test_example():\n    page.click()\n"
    result = SelfHealingRunner._apply_fix(
        code,
        "this_snippet_does_not_exist_anywhere_in_code",
        "page.locator('#btn').click()",
    )
    assert result is None


def test_apply_fix_short_target_rejected():
    """target_snippet < 20 chars -> returns None."""
    code = "def test_example():\n    page.click()\n"
    result = SelfHealingRunner._apply_fix(code, "page.click()", "page.locator('#x').click()")
    assert result is None


def test_apply_fix_ast_rollback():
    """Valid replacement that creates syntax error -> returns None."""
    code = (
        "def test_example():\n"
        "    page.get_by_text('提交按钮这是一个很长的定位器文本内容').click()\n"
    )
    target = "    page.get_by_text('提交按钮这是一个很长的定位器文本内容').click()"
    # This replacement will create invalid Python syntax (unmatched paren)
    replacement = "    page.locator('#submit').click( "
    result = SelfHealingRunner._apply_fix(code, target, replacement)
    assert result is None


# --- _extract_locator_from_code tests (HEAL-02) ---


def test_extract_locator_get_by_text():
    """Extracts '提交' from page.get_by_text('提交')."""
    result = SelfHealingRunner._extract_locator_from_code(
        "    page.get_by_text('提交').click()"
    )
    assert result == "提交"


def test_extract_locator_get_by_role_name():
    """Extracts '登录' from page.get_by_role('button', name='登录')."""
    result = SelfHealingRunner._extract_locator_from_code(
        '    page.get_by_role("button", name="登录").click()'
    )
    assert result == "登录"


def test_extract_locator_locator_css():
    """Extracts '#submit' from page.locator('#submit')."""
    result = SelfHealingRunner._extract_locator_from_code(
        "    page.locator('#submit').click()"
    )
    assert result == "#submit"


def test_extract_locator_no_match():
    """page.goto('...') has no locator -> returns None."""
    result = SelfHealingRunner._extract_locator_from_code(
        "    page.goto('https://example.com')"
    )
    assert result is None


def test_extract_locator_empty():
    """Empty string -> returns None."""
    result = SelfHealingRunner._extract_locator_from_code("")
    assert result is None


# --- _search_dom_for_text tests (HEAL-02) ---


def test_search_dom_finds_context():
    """DOM with target text -> returns 5 lines before + match + 5 after."""
    lines = [f"line_{i}" for i in range(20)]
    lines[10] = "TARGET_LINE here"
    dom = "\n".join(lines)
    result = SelfHealingRunner._search_dom_for_text(dom, "TARGET_LINE")
    result_lines = result.split("\n")
    assert len(result_lines) == 11  # 5 before + match + 5 after
    assert "TARGET_LINE here" in result


def test_search_dom_not_found():
    """DOM without target -> returns truncated full DOM."""
    dom = "\n".join([f"line_{i}" for i in range(200)])
    result = SelfHealingRunner._search_dom_for_text(dom, "NOT_FOUND_TEXT")
    assert len(result) <= 2000
    assert "line_0" in result  # Falls back to full DOM


# --- _read_dom_snapshot with locator tests (HEAL-02) ---


def test_read_dom_snapshot_with_locator(tmp_path):
    """Uses code-extracted locator to find DOM file with matching text."""
    dom_dir = tmp_path / "run1" / "dom"
    dom_dir.mkdir(parents=True)
    (dom_dir / "step_1.txt").write_text("header\nnav stuff\n", encoding="utf-8")
    (dom_dir / "step_2.txt").write_text("header\nTARGET_TEXT content\nfooter\n", encoding="utf-8")
    (dom_dir / "step_3.txt").write_text("header\nother content\nfooter\n", encoding="utf-8")

    result = SelfHealingRunner._read_dom_snapshot(
        "run1",
        str(tmp_path),
        error_output="",
        failing_line="page.get_by_text('TARGET_TEXT').click()",
    )
    assert "TARGET_TEXT content" in result


def test_read_dom_snapshot_fallback_step_number(tmp_path):
    """Without failing_line, uses step number from error_output."""
    dom_dir = tmp_path / "run1" / "dom"
    dom_dir.mkdir(parents=True)
    (dom_dir / "step_1.txt").write_text("step 1 content", encoding="utf-8")
    (dom_dir / "step_2.txt").write_text("step 2 content", encoding="utf-8")
    (dom_dir / "step_3.txt").write_text("step 3 content", encoding="utf-8")

    result = SelfHealingRunner._read_dom_snapshot(
        "run1",
        str(tmp_path),
        error_output="error at step_3 something went wrong",
        failing_line="",
    )
    assert "step 3 content" in result


def test_read_dom_snapshot_no_dom_dir(tmp_path):
    """No dom directory -> returns placeholder."""
    result = SelfHealingRunner._read_dom_snapshot(
        "run1",
        str(tmp_path),
        error_output="",
        failing_line="page.get_by_text('something').click()",
    )
    assert "无 DOM 快照目录" in result
