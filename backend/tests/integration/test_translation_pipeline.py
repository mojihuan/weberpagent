"""Integration tests for translator -> buffer full chain (TEST-01, TEST-02).

Validates that the StepCodeBuffer incremental translation pipeline works
correctly end-to-end: from browser-use action dicts to generated .py
file output. Covers click/input key names and wait/select_dropdown/evaluate operations.
"""

import ast
import json
from dataclasses import dataclass
from pathlib import Path

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


def test_full_chain_click_input_produces_playwright_code(
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
        buffer.append_step(action_dict)

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


def test_full_chain_wait_evaluate_produces_correct_code(
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
        buffer.append_step(action_dict)

    content = buffer.assemble(run_id="int_test_2", task_name="操作测试", task_id="t2")

    # wait -> page.wait_for_timeout(ms)
    assert "page.wait_for_timeout(2000)" in content

    # evaluate -> page.evaluate(...)
    assert "page.evaluate" in content

    # select_dropdown -> .select_option(...)
    assert ".select_option" in content

    # Verify generated code is valid Python
    ast.parse(content)

