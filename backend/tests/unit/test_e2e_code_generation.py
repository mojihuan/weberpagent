"""E2E verification tests for combined precondition + assertion code generation.

Tests E2E-01 acceptance criteria:
- Generated code with precondition + actions + assertions passes ast.parse
- Generated code contains page.goto(target_url) as first action after docstring
- Generated code contains expect() statements at end when assertions provided
- Import lines include expect and re when assertions require them
- Backward compatibility: precondition only, assertions only, neither
- Structural ordering: goto < actions < assertions
"""

import ast

import pytest

from backend.core.action_translator import TranslatedAction
from backend.core.code_generator import PlaywrightCodeGenerator


def _sample_actions() -> list[TranslatedAction]:
    """Return 3 sample actions simulating a real test scenario."""
    return [
        TranslatedAction(
            code='page.locator("#menu-sales").click()',
            action_type="click",
            is_comment=False,
            has_locator=True,
        ),
        TranslatedAction(
            code='page.locator("#search-input").fill("测试商品")',
            action_type="input",
            is_comment=False,
            has_locator=True,
        ),
        TranslatedAction(
            code='page.locator("#submit-btn").click()',
            action_type="click",
            is_comment=False,
            has_locator=True,
        ),
    ]


class TestE2ECodeGeneration:
    """E2E tests for PlaywrightCodeGenerator with precondition + assertion combinations."""

    def test_full_precondition_plus_all_assertion_types(self) -> None:
        """E2E-01: 前置条件 + 全部4种断言类型的组合验证。"""
        generator = PlaywrightCodeGenerator()
        assertions = [
            {"type": "url_contains", "expected": "/sales", "name": "url_check"},
            {"type": "text_exists", "expected": "销售出库", "name": "text_check"},
            {"type": "no_errors", "expected": "true", "name": "no_errors_check"},
            {"type": "element_exists", "expected": "#submit-btn", "name": "elem_check"},
        ]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=_sample_actions(),
            precondition_config={"target_url": "https://erp.example.com"},
            assertions_config=assertions,
        )

        # Acceptance criteria 1: valid Python syntax
        ast.parse(code)

        # Acceptance criteria 2: page.goto present and before actions
        assert 'page.goto("https://erp.example.com")' in code
        lines = code.splitlines()
        goto_idx = next(i for i, l in enumerate(lines) if "page.goto(" in l)
        action_idx = next(i for i, l in enumerate(lines) if "page.locator(" in l)
        assert goto_idx < action_idx

        # Acceptance criteria 3: expect() statements for all 4 assertion types
        assert "expect(page).to_have_url(re.compile(" in code
        assert 'expect(page.locator("body")).to_contain_text("销售出库")' in code
        assert "assert len(js_errors) == 0" in code
        assert 'expect(page.locator("#submit-btn")).to_be_visible()' in code

        # Structural marker
        assert "# Assertions" in code

        # Acceptance criteria 4: correct imports
        assert "from playwright.sync_api import Page, expect" in code
        assert "import re" in code
        assert "import logging" in code

        # Internal setup lines
        assert '_healer = logging.getLogger("healer")' in code
        assert "js_errors = []" in code

    def test_precondition_only_no_assertions(self) -> None:
        """向后兼容: 只有前置条件，无断言。"""
        generator = PlaywrightCodeGenerator()
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=_sample_actions(),
            precondition_config={"target_url": "https://erp.example.com"},
            assertions_config=None,
        )

        assert 'page.goto("https://erp.example.com")' in code
        assert "from playwright.sync_api import Page" in code
        assert "Page, expect" not in code
        assert "import re" not in code
        assert "# Assertions" not in code
        assert "expect(" not in code
        ast.parse(code)

    def test_assertions_only_no_precondition(self) -> None:
        """向后兼容: 只有断言，无前置条件。"""
        generator = PlaywrightCodeGenerator()
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=_sample_actions(),
            precondition_config=None,
            assertions_config=[{"type": "text_exists", "expected": "完成", "name": "check"}],
        )

        assert "page.goto(" not in code
        assert 'expect(page.locator("body")).to_contain_text("完成")' in code
        assert "from playwright.sync_api import Page, expect" in code
        assert "import re" not in code
        ast.parse(code)

    def test_no_precondition_no_assertions(self) -> None:
        """向后兼容: 无前置条件也无断言（原始行为不变）。"""
        generator = PlaywrightCodeGenerator()
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=_sample_actions(),
            precondition_config=None,
            assertions_config=None,
        )

        assert "page.goto(" not in code
        assert "expect(" not in code
        assert "import re" not in code
        assert "# Assertions" not in code
        assert "js_errors" not in code
        ast.parse(code)

    def test_structural_ordering_all_sections(self) -> None:
        """E2E-01: 验证生成代码各部分的正确顺序。"""
        generator = PlaywrightCodeGenerator()
        assertions = [
            {"type": "url_contains", "expected": "/sales", "name": "url_check"},
            {"type": "text_exists", "expected": "销售出库", "name": "text_check"},
            {"type": "no_errors", "expected": "true", "name": "no_errors_check"},
            {"type": "element_exists", "expected": "#submit-btn", "name": "elem_check"},
        ]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=_sample_actions(),
            precondition_config={"target_url": "https://erp.example.com"},
            assertions_config=assertions,
        )

        lines = code.splitlines()
        goto_index = next(i for i, l in enumerate(lines) if "page.goto(" in l)
        first_action_index = next(i for i, l in enumerate(lines) if "page.locator(" in l)
        assertions_comment_index = next(
            i for i, l in enumerate(lines) if "# Assertions" in l
        )
        last_assertion_index = max(
            i for i, l in enumerate(lines) if "expect(" in l or "assert len(" in l
        )

        assert goto_index < first_action_index, "page.goto must come before actions"
        assert first_action_index < assertions_comment_index, "actions before assertions"
        assert assertions_comment_index < last_assertion_index, "assertions comment before last assertion"

        # Exactly 1 function definition
        tree = ast.parse(code)
        func_defs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        assert len(func_defs) == 1
