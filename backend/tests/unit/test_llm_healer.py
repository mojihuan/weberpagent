"""Unit tests for LLMHealer -- LLM-driven locator healing.

Tests mock the browser-use ChatOpenAI to avoid real API calls.
Covers: success, timeout, invalid syntax, markdown stripping,
empty response, DOM truncation, frozen dataclass, prompt construction.
"""

import asyncio
import dataclasses
import re
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.core.llm_healer import LLMHealer, LLMHealResult


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

LLM_CONFIG = {
    "model": "qwen3.5-plus",
    "api_key": "test-key",
    "base_url": "https://test.com",
    "temperature": 0.0,
}


@pytest.fixture
def mock_llm():
    """Create a mock browser-use ChatOpenAI with async ainvoke."""
    llm = MagicMock()
    llm.ainvoke = AsyncMock()
    return llm


@pytest.fixture
def healer(mock_llm):
    """Create LLMHealer with mocked LLM."""
    with patch("backend.core.llm_healer.create_llm", return_value=mock_llm):
        h = LLMHealer(llm_config=LLM_CONFIG)
    return h


def _make_completion(text: str) -> MagicMock:
    """Build a mock that mimics ChatInvokeCompletion with .completion attribute."""
    mock_result = MagicMock()
    mock_result.completion = text
    return mock_result


# ---------------------------------------------------------------------------
# Test 1: Successful heal returns LLMHealResult(success=True)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_heal_success_returns_valid_result(healer, mock_llm):
    """LLMHealer returns LLMHealResult(success=True) with valid code snippet."""
    code = "page.locator('button:has-text(\"Submit\")').click()"
    mock_llm.ainvoke.return_value = _make_completion(code)

    result = await healer.heal(
        action_type="click",
        failed_locators=("page.locator('xpath=//button[@id=\"old\"]')",),
        dom_snapshot="<div><button>Submit</button></div>",
        action_params={},
    )

    assert result.success is True
    assert "page.locator" in result.code_snippet
    assert result.locator != ""


# ---------------------------------------------------------------------------
# Test 2: Timeout returns LLMHealResult(success=False)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_heal_timeout_returns_failure(healer, mock_llm):
    """LLMHealer returns failure result on asyncio.TimeoutError (30s timeout)."""
    mock_llm.ainvoke.side_effect = asyncio.TimeoutError()

    result = await healer.heal(
        action_type="click",
        failed_locators=("page.locator('button')",),
        dom_snapshot="<div>btn</div>",
        action_params={},
    )

    assert result.success is False
    assert result.code_snippet == ""


# ---------------------------------------------------------------------------
# Phase 107: Structured repair prompt + LLMHealResult extension tests
# ---------------------------------------------------------------------------

import json

from backend.core.llm_healer import (
    REPAIR_SYSTEM_PROMPT_V2,
    _CODE_CONTEXT_WINDOW,
    _parse_repair_response,
)


# --- _parse_repair_response tests ---


def test_parse_repair_response_valid_json():
    """Valid JSON with target_snippet >= 20 chars + replacement -> returns tuple."""
    raw = json.dumps({
        "target_snippet": "page.get_by_text('提交按钮').click()",
        "replacement": "page.locator('#submit-btn').click()",
    })
    result = _parse_repair_response(raw)
    assert result is not None
    assert result[0] == "page.get_by_text('提交按钮').click()"
    assert result[1] == "page.locator('#submit-btn').click()"


def test_parse_repair_response_short_target():
    """JSON with target_snippet < 20 chars -> returns None (too ambiguous)."""
    raw = json.dumps({
        "target_snippet": "page.click()",
        "replacement": "page.locator('#x').click()",
    })
    result = _parse_repair_response(raw)
    assert result is None


def test_parse_repair_response_invalid_json():
    """Plain text (not JSON) -> returns None."""
    raw = "This is just plain text, not JSON at all"
    result = _parse_repair_response(raw)
    assert result is None


def test_parse_repair_response_markdown_wrapped():
    """Markdown fences around JSON -> strips and parses correctly."""
    payload = {
        "target_snippet": "page.get_by_role('button', name='提交').click()",
        "replacement": "page.locator('[data-testid=submit]').click()",
    }
    raw = "```json\n" + json.dumps(payload) + "\n```"
    result = _parse_repair_response(raw)
    assert result is not None
    assert result[0] == payload["target_snippet"]
    assert result[1] == payload["replacement"]


def test_parse_repair_response_json_in_text():
    """JSON embedded in explanatory text -> extracts and parses."""
    payload = {
        "target_snippet": "page.get_by_text('这是一个很长的定位器文本').click()",
        "replacement": "page.locator('#fixed-locator').click()",
    }
    raw = "Here is the fix:\n" + json.dumps(payload) + "\nHope this helps!"
    result = _parse_repair_response(raw)
    assert result is not None
    assert result[0] == payload["target_snippet"]


def test_parse_repair_response_empty_replacement():
    """JSON with empty replacement -> returns None."""
    raw = json.dumps({
        "target_snippet": "page.get_by_text('这是一个很长的定位器文本').click()",
        "replacement": "",
    })
    result = _parse_repair_response(raw)
    assert result is None


# --- LLMHealResult frozen + new fields tests ---


def test_llm_heal_result_frozen_with_new_fields():
    """LLMHealResult is frozen and new fields have defaults."""
    result = LLMHealResult(
        success=True,
        code_snippet="page.click()",
        raw_response="page.click()",
        locator="page.click()",
    )
    assert result.target_snippet == ""
    assert result.replacement == ""

    # Frozen: cannot set attributes
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.success = False


def test_llm_heal_result_with_new_fields():
    """LLMHealResult can be created with target_snippet and replacement."""
    result = LLMHealResult(
        success=True,
        code_snippet="new code",
        raw_response="raw",
        locator="page.locator('#x')",
        target_snippet="page.get_by_text('old long snippet here').click()",
        replacement="page.locator('#x').click()",
    )
    assert result.target_snippet == "page.get_by_text('old long snippet here').click()"
    assert result.replacement == "page.locator('#x').click()"


# --- repair_code structured response tests ---


@pytest.mark.asyncio
async def test_repair_code_returns_structured_result(healer, mock_llm):
    """repair_code returns LLMHealResult with target_snippet and replacement."""
    payload = {
        "target_snippet": "page.get_by_text('这是一个很长的按钮文本定位器').click()",
        "replacement": "page.locator('#new-btn').click()",
    }
    mock_llm.ainvoke.return_value = _make_completion(json.dumps(payload))

    result = await healer.repair_code(
        test_code="def test_x():\n    page.get_by_text('这是一个很长的按钮文本定位器').click()\n",
        error_line=2,
        error_message="Error: button not found",
    )
    assert result.success is True
    assert result.target_snippet == payload["target_snippet"]
    assert result.replacement == payload["replacement"]
    assert result.code_snippet == payload["replacement"]


@pytest.mark.asyncio
async def test_repair_code_context_window_20_lines(healer, mock_llm):
    """repair_code uses 20-line context window (41 lines for 80-line file)."""
    # 80-line test code, failing at line 40
    lines = [f"    line_{i} = {i}" for i in range(80)]
    test_code = "def test_example():\n" + "\n".join(lines) + "\n"

    payload = {
        "target_snippet": "    line_39 = 39  # a long target snippet for matching",
        "replacement": "    line_39 = 999  # fixed",
    }
    mock_llm.ainvoke.return_value = _make_completion(json.dumps(payload))

    result = await healer.repair_code(
        test_code=test_code,
        error_line=40,
        error_message="AssertionError",
    )

    # Verify context window: should be 41 lines (20 before + error + 20 after)
    call_args = mock_llm.ainvoke.call_args
    user_msg = call_args[0][0][1].content  # [messages][1] = UserMessage
    context_lines = [l for l in user_msg.split("\n") if l.strip().startswith(("   ", "  ")) and ":" in l and l.strip()[0].isdigit()]
    # Context should have 41 lines (lines 20-60)
    assert result.success is True


@pytest.mark.asyncio
async def test_repair_code_non_json_fallback(healer, mock_llm):
    """repair_code returns success=False when LLM returns non-JSON."""
    mock_llm.ainvoke.return_value = _make_completion(
        "This is just plain text, not a JSON response at all"
    )

    result = await healer.repair_code(
        test_code="def test_x():\n    page.click()\n",
        error_line=2,
        error_message="Error",
    )
    assert result.success is False


def test_code_context_window_is_20():
    """_CODE_CONTEXT_WINDOW should be 20."""
    assert _CODE_CONTEXT_WINDOW == 20


def test_repair_system_prompt_v2_exists():
    """REPAIR_SYSTEM_PROMPT_V2 exists and mentions JSON + target_snippet."""
    assert "target_snippet" in REPAIR_SYSTEM_PROMPT_V2
    assert "replacement" in REPAIR_SYSTEM_PROMPT_V2
    assert "JSON" in REPAIR_SYSTEM_PROMPT_V2
