"""Unit tests for assertion step generation in PlaywrightCodeGenerator.

Tests ASRT-01, ASRT-02, ASRT-03:
- ASRT-01: 4 assertion types map to correct Playwright expect()/assert statements
- ASRT-02: assertions_config parameter on generate() and StepCodeBuffer.assemble()
- ASRT-03: Assertion translation unit tests
"""

import ast
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from backend.core.action_translator import TranslatedAction
from backend.core.code_generator import PlaywrightCodeGenerator


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _simple_click_action() -> TranslatedAction:
    """Return a minimal click TranslatedAction for testing."""
    return TranslatedAction(
        code='page.locator("#btn").click()',
        action_type="click",
        is_comment=False,
        has_locator=True,
    )


def _url_contains_config() -> list[dict]:
    return [{"type": "url_contains", "expected": "/sales", "name": "check_url"}]


def _text_exists_config() -> list[dict]:
    return [{"type": "text_exists", "expected": "销售出库", "name": "check_text"}]


def _no_errors_config() -> list[dict]:
    return [{"type": "no_errors", "expected": "true", "name": "check_noerr"}]


def _element_exists_css_config() -> list[dict]:
    return [{"type": "element_exists", "expected": "#submit-btn", "name": "check_elem"}]


def _element_exists_short_text_config() -> list[dict]:
    return [{"type": "element_exists", "expected": "提交", "name": "check_short"}]


def _element_exists_long_text_config() -> list[dict]:
    return [{"type": "element_exists", "expected": "销售出库单", "name": "check_long"}]


# ---------------------------------------------------------------------------
# Test Class
# ---------------------------------------------------------------------------


class TestAssertionTranslation:
    """Tests for ASRT-01: assertion step generation in PlaywrightCodeGenerator."""

    # ASRT-01: url_contains generates expect(page).to_have_url(re.compile(...))

    def test_url_contains(self) -> None:
        """url_contains assertion generates expect(page).to_have_url(re.compile(...))."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            assertions_config=_url_contains_config(),
        )

        assert 'expect(page).to_have_url(re.compile(' in code
        assert "/sales" in code
        assert "import re" in code
        assert 'Assertion failed (url_contains)' in code
        ast.parse(code)

    # ASRT-01: text_exists generates expect(page.locator("body")).to_contain_text(...)

    def test_text_exists(self) -> None:
        """text_exists assertion generates expect(page.locator('body')).to_contain_text(...)."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            assertions_config=_text_exists_config(),
        )

        assert 'expect(page.locator("body")).to_contain_text("销售出库")' in code
        assert 'Assertion failed (text_exists)' in code
        ast.parse(code)

    # ASRT-01: no_errors generates js_errors collector + assertion block

    def test_no_errors(self) -> None:
        """no_errors assertion generates js_errors collector + assert len(js_errors) == 0."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            assertions_config=_no_errors_config(),
        )

        # Collector should be present
        assert "js_errors = []" in code
        assert 'page.on("pageerror", lambda e: js_errors.append(str(e)))' in code
        # Assertion block
        assert "assert len(js_errors) == 0" in code
        assert "Assertion failed (no_errors)" in code
        ast.parse(code)

    # ASRT-01: element_exists with CSS selector generates page.locator(...)

    def test_element_exists_css_selector(self) -> None:
        """element_exists with CSS selector generates expect(page.locator(...)).to_be_visible()."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            assertions_config=_element_exists_css_config(),
        )

        assert 'expect(page.locator("#submit-btn")).to_be_visible()' in code
        assert 'Assertion failed (element_exists)' in code
        ast.parse(code)

    # ASRT-01: element_exists with short text uses exact=True

    def test_element_exists_plain_text_short(self) -> None:
        """element_exists with short text (<=4 chars) uses get_by_text with exact=True."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            assertions_config=_element_exists_short_text_config(),
        )

        assert 'expect(page.get_by_text("提交", exact=True)).to_be_visible()' in code
        ast.parse(code)

    # ASRT-01: element_exists with long text does not use exact

    def test_element_exists_plain_text_long(self) -> None:
        """element_exists with long text (>4 chars) uses get_by_text without exact."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            assertions_config=_element_exists_long_text_config(),
        )

        assert 'expect(page.get_by_text("销售出库单")).to_be_visible()' in code
        assert "exact=True" not in code.split("销售出库单")[0].split("\n")[-1]
        ast.parse(code)

    # ASRT-01: multiple assertions of mixed types all present in output

    def test_multiple_mixed_assertions(self) -> None:
        """Multiple assertions of different types all appear in output."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        assertions = [
            {"type": "url_contains", "expected": "/dashboard", "name": "check_url"},
            {"type": "text_exists", "expected": "欢迎", "name": "check_text"},
            {"type": "no_errors", "expected": "true", "name": "check_err"},
        ]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            assertions_config=assertions,
        )

        assert "re.compile" in code
        assert "to_contain_text" in code
        assert "len(js_errors) == 0" in code
        assert "# Assertions" in code
        ast.parse(code)

    # ASRT-01: no assertions produces no expect/assert statements (backward compatible)

    def test_no_assertions_backward_compat(self) -> None:
        """assertions_config=None produces no expect/assert statements."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code_none = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            assertions_config=None,
        )
        code_no_arg = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
        )

        assert "expect(" not in code_none
        assert "js_errors" not in code_none
        assert "# Assertions" not in code_none
        assert code_none == code_no_arg

    # ASRT-01: empty assertions list produces no expect/assert statements

    def test_empty_assertions_backward_compat(self) -> None:
        """assertions_config=[] produces no expect/assert statements."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            assertions_config=[],
        )

        assert "expect(" not in code
        assert "# Assertions" not in code

    # ASRT-01: unknown assertion type generates comment

    def test_unknown_type_generates_comment(self) -> None:
        """Unknown assertion type generates # unknown assertion comment."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            assertions_config=[{"type": "custom_unknown", "expected": "x", "name": "custom"}],
        )

        assert "# unknown assertion: custom_unknown" in code
        ast.parse(code)

    # ASRT-01: assertions appear after action steps, not before

    def test_assertions_after_body_actions(self) -> None:
        """Assertions appear after action steps in generated code."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            assertions_config=_text_exists_config(),
        )

        lines = code.splitlines()
        action_idx = next(i for i, l in enumerate(lines) if "page.locator(" in l)
        assertion_idx = next(i for i, l in enumerate(lines) if "# Assertions" in l)

        assert action_idx < assertion_idx, "Assertions must appear after action steps"

    # ASRT-01: full code with precondition + actions + assertions passes ast.parse

    def test_full_code_valid_syntax(self) -> None:
        """Generated code with precondition + actions + assertions passes ast.parse."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        assertions = [
            {"type": "url_contains", "expected": "/sales", "name": "check_url"},
            {"type": "text_exists", "expected": "销售出库", "name": "check_text"},
            {"type": "no_errors", "expected": "true", "name": "check_noerr"},
            {"type": "element_exists", "expected": "#submit-btn", "name": "check_elem"},
        ]
        code = generator.generate(
            run_id="r1",
            task_name="full_test",
            task_id="t1",
            actions=actions,
            precondition_config={"target_url": "https://erp.example.com"},
            assertions_config=assertions,
        )

        tree = ast.parse(code)
        func_defs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        assert len(func_defs) == 1

        # Verify all parts present
        assert "page.goto(" in code
        assert "re.compile" in code
        assert "to_contain_text" in code
        assert "len(js_errors) == 0" in code
        assert "to_be_visible" in code
        assert "# Assertions" in code

    # ASRT-02: StepCodeBuffer.assemble() passes assertions_config through

    async def test_buffer_assemble_passes_assertions_config(self) -> None:
        """StepCodeBuffer.assemble() passes assertions_config to generate()."""
        from backend.core.step_code_buffer import StepCodeBuffer

        buffer = StepCodeBuffer()
        navigate_action = {"navigate": {"url": "https://erp.example.com"}}
        buffer.append_step(navigate_action)

        content = buffer.assemble(
            run_id="asrt02",
            task_name="断言传递",
            task_id="t_asrt02",
            assertions_config=_url_contains_config(),
        )

        assert "re.compile" in content
        assert "/sales" in content
        ast.parse(content)
