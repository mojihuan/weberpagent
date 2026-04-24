"""Integration tests for translator -> generator full chain (TEST-01, TEST-02, TEST-03).

Validates that Phases 99 (key name fix) and 100 (operation translation expansion)
work correctly end-to-end: from browser-use model_actions() input to generated .py
file output. Covers click/input key names, wait/select_dropdown/evaluate operations,
and healing path for click/input weak steps.
"""

import ast
import tempfile
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.core.code_generator import PlaywrightCodeGenerator


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
def generator() -> PlaywrightCodeGenerator:
    """Create a fresh PlaywrightCodeGenerator for each test."""
    return PlaywrightCodeGenerator()


# ---------------------------------------------------------------------------
# TEST-01: click/input key names produce correct Playwright code
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_full_chain_click_input_produces_playwright_code(
    generator: PlaywrightCodeGenerator,
) -> None:
    """click/input action dicts with browser-use format produce page.locator().click()/.fill() in generated .py file."""
    mock_history = MagicMock()
    mock_history.model_actions.return_value = [
        {"navigate": {"url": "https://erp.example.com/login"}, "interacted_element": None},
        {"input": {"index": 0, "text": "admin"}, "interacted_element": MockDOMElement(x_path="/html/body/input[1]", node_name="INPUT")},
        {"input": {"index": 1, "text": "password123"}, "interacted_element": MockDOMElement(x_path="/html/body/input[2]", node_name="INPUT")},
        {"click": {"index": 2}, "interacted_element": MockDOMElement(x_path="/html/body/button", node_name="BUTTON")},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        code_path = await generator.generate_and_save(
            run_id="int_test_1",
            task_name="登录测试",
            task_id="t1",
            agent_history=mock_history,
            base_dir=tmpdir,
        )

        content = Path(code_path).read_text()

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
    generator: PlaywrightCodeGenerator,
) -> None:
    """wait/select_dropdown/evaluate action dicts produce correct Playwright code in full chain output."""
    mock_history = MagicMock()
    mock_history.model_actions.return_value = [
        {"navigate": {"url": "https://example.com"}, "interacted_element": None},
        {"wait": {"seconds": 2}, "interacted_element": None},
        {"evaluate": {"code": "document.title"}, "interacted_element": None},
        {"select_dropdown": {"index": 3, "text": "Option A"}, "interacted_element": MockDOMElement(x_path="/html/body/select", node_name="SELECT")},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        code_path = await generator.generate_and_save(
            run_id="int_test_2",
            task_name="操作测试",
            task_id="t2",
            agent_history=mock_history,
            base_dir=tmpdir,
        )

        content = Path(code_path).read_text()

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
    generator: PlaywrightCodeGenerator,
) -> None:
    """_heal_weak_steps() triggers LLMHealer.heal() exactly for click/input actions with elem=None, and not for other types."""
    run_id = "heal_int_test"

    mock_history = MagicMock()
    mock_history.model_actions.return_value = [
        {"navigate": {"url": "https://example.com"}, "interacted_element": None},
        {"click": {"index": 5}, "interacted_element": None},                    # Weak -> triggers heal
        {"input": {"index": 12, "text": "hello"}, "interacted_element": None},   # Weak -> triggers heal
        {"wait": {"seconds": 3}, "interacted_element": None},                    # NOT weak (not click/input)
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create DOM snapshot files for click (index 1 -> step_2.txt) and input (index 2 -> step_3.txt)
        dom_dir = Path(tmpdir) / run_id / "dom"
        dom_dir.mkdir(parents=True, exist_ok=True)
        (dom_dir / "step_2.txt").write_text("<html><button>OK</button></html>")
        (dom_dir / "step_3.txt").write_text("<html><input /></html>")

        with patch("backend.core.code_generator.LLMHealer") as mock_cls:
            mock_instance = MagicMock()
            mock_instance.heal = AsyncMock(return_value=MagicMock(
                success=True,
                code_snippet='page.locator("button").click()',
                raw_response="...",
                locator="button",
            ))
            mock_cls.return_value = mock_instance

            await generator.generate_and_save(
                run_id=run_id,
                task_name="Healing测试",
                task_id="t_heal",
                agent_history=mock_history,
                base_dir=tmpdir,
                llm_config={"model": "test", "api_key": "key"},
            )

            # Exactly 2 heal calls: one for click, one for input
            assert mock_instance.heal.call_count == 2


# ---------------------------------------------------------------------------
# TEST-03 supplement: non-click/input actions skip healing entirely
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_non_click_input_actions_skip_healing(
    generator: PlaywrightCodeGenerator,
) -> None:
    """navigate/scroll/wait actions never trigger LLM healing."""
    mock_history = MagicMock()
    mock_history.model_actions.return_value = [
        {"navigate": {"url": "https://example.com"}, "interacted_element": None},
        {"scroll": {"down": True, "pages": 1.0}, "interacted_element": None},
        {"wait": {"seconds": 2}, "interacted_element": None},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("backend.core.code_generator.LLMHealer") as mock_cls:
            mock_instance = MagicMock()
            mock_instance.heal = AsyncMock()
            mock_cls.return_value = mock_instance

            code_path = await generator.generate_and_save(
                run_id="no_heal_test",
                task_name="无Healing测试",
                task_id="t_no_heal",
                agent_history=mock_history,
                base_dir=tmpdir,
                llm_config={"model": "test", "api_key": "key"},
            )

            # No healing for non-click/input actions
            mock_instance.heal.assert_not_called()

            # Generated file is valid Python
            content = Path(code_path).read_text()
            ast.parse(content)
