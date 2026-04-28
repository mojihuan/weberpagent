"""Integration tests for translator -> buffer full chain (TEST-01, TEST-02, TEST-03).

Validates that the StepCodeBuffer incremental translation pipeline works
correctly end-to-end: from browser-use action dicts to generated .py
file output. Covers click/input key names, wait/select_dropdown/evaluate operations,
and healing path for click/input weak steps.
"""

import ast
import json
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.core.step_code_buffer import StepCodeBuffer


# ---------------------------------------------------------------------------
# Helper: mock DOMInteractedElement (same pattern as test_action_translator.py)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MockDOMElement:
    """Simulates browser-use DOMInteractedElement for testing.

    Mirrors the key attributes: x_path, node_name, attributes, ax_name.
    Does not depend on browser-use internal types.
    """

    x_path: str = "/html/body/div"
    node_name: str = "DIV"
    attributes: dict[str, str] | None = None
    ax_name: str | None = None


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def buffer(tmp_path: Path) -> StepCodeBuffer:
    """Create a fresh StepCodeBuffer for each test."""
    return StepCodeBuffer(base_dir=str(tmp_path), run_id="int_test")


# ---------------------------------------------------------------------------
# TEST-01: click/input key names produce correct Playwright code
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_full_chain_click_input_produces_playwright_code(
    buffer: StepCodeBuffer, tmp_path: Path,
) -> None:
    """click/input action dicts with browser-use format produce page.locator().click()/.fill() in generated .py file."""
    actions = [
        {"navigate": {"url": "https://erp.example.com/login"}, "interacted_element": None},
        {"input": {"index": 0, "text": "admin"}, "interacted_element": MockDOMElement(x_path="/html/body/input[1]", node_name="INPUT")},
        {"input": {"index": 1, "text": "password123"}, "interacted_element": MockDOMElement(x_path="/html/body/input[2]", node_name="INPUT")},
        {"click": {"index": 2}, "interacted_element": MockDOMElement(x_path="/html/body/button", node_name="BUTTON")},
    ]

    for action_dict in actions:
        await buffer.append_step_async(action_dict)

    content = buffer.assemble(run_id="int_test_1", task_name="登录测试", task_id="t1")

    # Verify click/input produce correct Playwright locator calls
    assert 'page.locator("xpath=/html/body/input[1]").fill("admin")' in content
    assert 'page.locator("xpath=/html/body/input[2]").fill("password123")' in content
    assert 'page.locator("xpath=/html/body/button").click()' in content

    # Verify navigate produces page.goto
    assert "page.goto" in content

    # Verify generated code is valid Python
    ast.parse(content)


# ---------------------------------------------------------------------------
# TEST-02: wait/select_dropdown/evaluate produce correct Playwright code
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_full_chain_wait_evaluate_produces_correct_code(
    buffer: StepCodeBuffer, tmp_path: Path,
) -> None:
    """wait/select_dropdown/evaluate action dicts produce correct Playwright code in full chain output."""
    actions = [
        {"navigate": {"url": "https://example.com"}, "interacted_element": None},
        {"wait": {"seconds": 2}, "interacted_element": None},
        {"evaluate": {"code": "document.title"}, "interacted_element": None},
        {"select_dropdown": {"index": 3, "text": "Option A"}, "interacted_element": MockDOMElement(x_path="/html/body/select", node_name="SELECT")},
    ]

    for action_dict in actions:
        await buffer.append_step_async(action_dict)

    content = buffer.assemble(run_id="int_test_2", task_name="操作测试", task_id="t2")

    # wait -> page.wait_for_timeout(ms)
    assert "page.wait_for_timeout(2000)" in content

    # evaluate -> page.evaluate(...)
    assert "page.evaluate" in content

    # select_dropdown -> .select_option(...)
    assert ".select_option" in content

    # Verify generated code is valid Python
    ast.parse(content)


# ---------------------------------------------------------------------------
# TEST-03: healing triggers exactly for click/input weak steps, not others
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_healing_triggers_only_for_click_and_input_weak_steps(
    tmp_path: Path,
) -> None:
    """append_step_async triggers LLMHealer.heal() exactly for click/input actions with elem=None, and not for other types."""
    run_id = "heal_int_test"
    buffer = StepCodeBuffer(base_dir=str(tmp_path), run_id=run_id, llm_config={"model": "test", "api_key": "key"})

    actions = [
        {"navigate": {"url": "https://example.com"}, "interacted_element": None},
        {"click": {"index": 5}, "interacted_element": None},                    # Weak -> triggers heal
        {"input": {"index": 12, "text": "hello"}, "interacted_element": None},   # Weak -> triggers heal
        {"wait": {"seconds": 3}, "interacted_element": None},                    # NOT weak (not click/input)
    ]

    # Create DOM snapshot files for click (step index 1 -> step_2.txt) and input (step index 2 -> step_3.txt)
    dom_dir = tmp_path / run_id / "dom"
    dom_dir.mkdir(parents=True, exist_ok=True)
    (dom_dir / "step_2.txt").write_text("<html><button>OK</button></html>")
    (dom_dir / "step_3.txt").write_text("<html><input /></html>")

    with patch("backend.core.step_code_buffer.LLMHealer") as mock_cls:
        mock_instance = MagicMock()
        mock_instance.heal = AsyncMock(return_value=MagicMock(
            success=True,
            code_snippet='page.locator("button").click()',
            raw_response="...",
            locator="button",
        ))
        mock_cls.return_value = mock_instance

        for action_dict in actions:
            await buffer.append_step_async(action_dict)

        # Exactly 2 heal calls: one for click, one for input
        assert mock_instance.heal.call_count == 2


# ---------------------------------------------------------------------------
# TEST-03 supplement: non-click/input actions skip healing entirely
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_non_click_input_actions_skip_healing(
    tmp_path: Path,
) -> None:
    """navigate/scroll/wait actions never trigger LLM healing."""
    buffer = StepCodeBuffer(base_dir=str(tmp_path), run_id="no_heal_test", llm_config={"model": "test", "api_key": "key"})

    actions = [
        {"navigate": {"url": "https://example.com"}, "interacted_element": None},
        {"scroll": {"down": True, "pages": 1.0}, "interacted_element": None},
        {"wait": {"seconds": 2}, "interacted_element": None},
    ]

    with patch("backend.core.step_code_buffer.LLMHealer") as mock_cls:
        mock_instance = MagicMock()
        mock_instance.heal = AsyncMock()
        mock_cls.return_value = mock_instance

        for action_dict in actions:
            await buffer.append_step_async(action_dict)

        # No healing for non-click/input actions
        mock_instance.heal.assert_not_called()

    # Assembled code is valid Python
    content = buffer.assemble(run_id="no_heal_test", task_name="无Healing测试", task_id="t_no_heal")
    ast.parse(content)
