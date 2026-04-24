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

SYSTEM_PROMPT_FRAGMENT = "Playwright"
USER_PROMPT_ACTION_TYPE = "click"


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
# Test 3: Invalid syntax returns failure
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_heal_invalid_syntax_returns_failure(healer, mock_llm):
    """LLMHealer returns failure when LLM returns code with syntax errors."""
    broken_code = "page.locator(\"btn).click('"
    mock_llm.ainvoke.return_value = _make_completion(broken_code)

    result = await healer.heal(
        action_type="click",
        failed_locators=("page.locator('btn')",),
        dom_snapshot="<div>btn</div>",
        action_params={},
    )

    assert result.success is False


# ---------------------------------------------------------------------------
# Test 4: Markdown code fences are stripped
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_heal_strips_markdown_fences(healer, mock_llm):
    """LLMHealer strips markdown code fences before validation."""
    fenced = "```python\npage.locator(\"button\").click()\n```"
    mock_llm.ainvoke.return_value = _make_completion(fenced)

    result = await healer.heal(
        action_type="click",
        failed_locators=("page.locator('old')",),
        dom_snapshot="<div><button>OK</button></div>",
        action_params={},
    )

    assert result.success is True
    assert result.code_snippet == 'page.locator("button").click()'


# ---------------------------------------------------------------------------
# Test 5: Empty response returns failure
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_heal_empty_response_returns_failure(healer, mock_llm):
    """LLMHealer returns failure when LLM returns empty string."""
    mock_llm.ainvoke.return_value = _make_completion("")

    result = await healer.heal(
        action_type="click",
        failed_locators=("page.locator('x')",),
        dom_snapshot="<div>x</div>",
        action_params={},
    )

    assert result.success is False


# ---------------------------------------------------------------------------
# Test 6: DOM snapshot is truncated when exceeding 5000 chars
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_heal_truncates_large_dom(healer, mock_llm):
    """LLMHealer truncates DOM snapshots exceeding 5000 chars."""
    long_dom = "<div>" + "x" * 6000 + "</div>"
    code = "page.locator('button').click()"
    mock_llm.ainvoke.return_value = _make_completion(code)

    await healer.heal(
        action_type="click",
        failed_locators=("page.locator('btn')",),
        dom_snapshot=long_dom,
        action_params={},
    )

    # Verify the LLM was called exactly once
    mock_llm.ainvoke.assert_called_once()
    call_args = mock_llm.ainvoke.call_args
    messages = call_args[0][0] if call_args[0] else call_args.kwargs.get("messages", [])

    # Find the UserMessage and check its content is truncated
    user_msg = [m for m in messages if hasattr(m, "content") and "DOM" in m.content or long_dom[:100] in m.content]
    # If no match by content, just check the second message
    if not user_msg:
        user_msg = [messages[-1]]

    assert len(user_msg) > 0
    # The user message content should be less than original DOM length
    msg_content = user_msg[0].content
    assert len(msg_content) < len(long_dom)


# ---------------------------------------------------------------------------
# Test 7: LLMHealResult is a frozen dataclass
# ---------------------------------------------------------------------------

def test_llm_heal_result_is_frozen():
    """LLMHealResult is a frozen dataclass (immutable per project convention)."""
    result = LLMHealResult(
        success=True,
        code_snippet="page.locator('x').click()",
        raw_response="page.locator('x').click()",
        locator="page.locator('x')",
    )
    assert dataclasses.is_dataclass(result)
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.success = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Test 8: Prompt construction contains required fields
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_heal_prompt_contains_required_fields(healer, mock_llm):
    """LLMHealer constructs prompt with action_type, failed_locators, DOM."""
    code = "page.locator('button').click()"
    mock_llm.ainvoke.return_value = _make_completion(code)

    dom = "<button>Click me</button>"
    await healer.heal(
        action_type="click",
        failed_locators=("page.locator('old')",),
        dom_snapshot=dom,
        action_params={},
    )

    mock_llm.ainvoke.assert_called_once()
    messages = mock_llm.ainvoke.call_args[0][0]

    # SystemMessage should mention Playwright
    system_msgs = [m for m in messages if getattr(m, "role", None) == "system"]
    assert len(system_msgs) == 1
    assert SYSTEM_PROMPT_FRAGMENT in system_msgs[0].content

    # UserMessage should contain action_type, failed_locators, and dom
    user_msgs = [m for m in messages if getattr(m, "role", None) == "user"]
    assert len(user_msgs) == 1
    user_content = user_msgs[0].content
    assert "click" in user_content
    assert "page.locator('old')" in user_content
    assert "<button>Click me</button>" in user_content
