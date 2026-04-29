"""Unit tests for precondition injection into generated Playwright code.

Tests PREC-01, PREC-02, PREC-03:
- PREC-01: generate() accepts precondition_config, injects page.goto() + wait_for_load_state()
- PREC-02: StepCodeBuffer.assemble() passes precondition_config through to generate()
- PREC-03: Generated code compatible with pytest storage_state injection
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


def _multi_type_actions() -> list[TranslatedAction]:
    """Return actions with multiple types for integration testing."""
    return [
        TranslatedAction(
            code='page.goto("https://erp.example.com")',
            action_type="navigate",
            is_comment=False,
            has_locator=False,
        ),
        TranslatedAction(
            code='page.locator("#user").fill("admin")',
            action_type="input",
            is_comment=False,
            has_locator=True,
        ),
        TranslatedAction(
            code='page.locator("#submit").click()',
            action_type="click",
            is_comment=False,
            has_locator=True,
        ),
    ]


# ---------------------------------------------------------------------------
# Test Class
# ---------------------------------------------------------------------------


class TestPreconditionInjection:
    """Tests for PREC-01: precondition_config parameter on generate()."""

    # PREC-01: With valid target_url, code contains goto + wait_for_load_state

    def test_precondition_injects_goto(self) -> None:
        """generate() with target_url produces page.goto + wait_for_load_state."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            precondition_config={"target_url": "https://erp.example.com"},
        )

        assert 'page.goto("https://erp.example.com")' in code
        assert 'page.wait_for_load_state("networkidle", timeout=10000)' in code
        assert "try:" in code
        assert "except Exception:" in code
        assert "pass" in code
        # Full code is valid Python
        ast.parse(code)

    # PREC-01: precondition_config=None produces no goto (backward compatible)

    def test_precondition_none_no_injection(self) -> None:
        """generate() with precondition_config=None produces no page.goto."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code_with_none = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            precondition_config=None,
        )
        code_without = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
        )

        assert "page.goto(" not in code_with_none
        assert code_with_none == code_without

    # PREC-01: empty target_url produces no goto (backward compatible)

    def test_precondition_empty_url_no_injection(self) -> None:
        """generate() with empty target_url produces no page.goto."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            precondition_config={"target_url": ""},
        )

        assert "page.goto(" not in code

    # PREC-01: missing target_url key produces no goto (backward compatible)

    def test_precondition_missing_key_no_injection(self) -> None:
        """generate() with config missing target_url key produces no page.goto."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            precondition_config={},
        )

        assert "page.goto(" not in code

    # PREC-01: generated goto code is indented with 4 spaces

    def test_precondition_indent_4_spaces(self) -> None:
        """page.goto and try lines start with exactly 4 spaces."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            precondition_config={"target_url": "https://erp.example.com"},
        )

        lines = code.splitlines()
        goto_line = next(l for l in lines if "page.goto(" in l)
        try_line = next(l for l in lines if l.strip() == "try:")

        assert goto_line.startswith("    "), f"goto line not 4-space indented: {goto_line!r}"
        assert not goto_line.startswith("        "), f"goto line over-indented: {goto_line!r}"
        assert try_line.startswith("    "), f"try line not 4-space indented: {try_line!r}"

    # PREC-01: precondition code appears after docstring but before action body

    def test_precondition_position_before_body(self) -> None:
        """page.goto appears after docstring but before action steps."""
        generator = PlaywrightCodeGenerator()
        actions = [_simple_click_action()]
        code = generator.generate(
            run_id="r1",
            task_name="test",
            task_id="t1",
            actions=actions,
            precondition_config={"target_url": "https://erp.example.com"},
        )

        lines = code.splitlines()
        goto_idx = next(i for i, l in enumerate(lines) if "page.goto(" in l)
        action_idx = next(i for i, l in enumerate(lines) if "page.locator(" in l)

        assert goto_idx < action_idx, "page.goto must appear before action steps"

    # PREC-01: full generated code with precondition passes ast.parse

    def test_precondition_code_valid_syntax(self) -> None:
        """Generated code with precondition + multi-type actions passes ast.parse."""
        generator = PlaywrightCodeGenerator()
        actions = _multi_type_actions()
        code = generator.generate(
            run_id="r1",
            task_name="multi",
            task_id="t1",
            actions=actions,
            precondition_config={"target_url": "https://erp.example.com"},
        )

        tree = ast.parse(code)
        func_defs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        assert len(func_defs) == 1

    # PREC-02: StepCodeBuffer.assemble() passes precondition_config through

    async def test_buffer_assemble_passes_config(self) -> None:
        """StepCodeBuffer.assemble() passes precondition_config to generate()."""
        from backend.core.step_code_buffer import StepCodeBuffer

        buffer = StepCodeBuffer()
        navigate_action = {"navigate": {"url": "https://erp.example.com"}}
        buffer.append_step(navigate_action)

        content = buffer.assemble(
            run_id="prec02",
            task_name="config传递",
            task_id="t_prec02",
            precondition_config={"target_url": "https://erp.example.com"},
        )

        assert 'page.goto("https://erp.example.com")' in content
        ast.parse(content)


# ---------------------------------------------------------------------------
# PREC-03: storage_state + page.goto() compatibility
# ---------------------------------------------------------------------------


def test_storage_state_goto_compatibility() -> None:
    """PREC-03: 验证生成的 page.goto() 代码与 pytest storage_state 兼容。

    conftest 注入 storage_state (localStorage token)，
    生成的 page.goto() 加载 ERP 页面后 Vue app 读取 token 自动登录。
    验证代码结构正确：goto 在最前面，后续操作在其之后。
    """
    generator = PlaywrightCodeGenerator()
    actions = [
        TranslatedAction(
            code='page.locator("#menu-item").click()',
            action_type="click",
            is_comment=False,
            has_locator=True,
        ),
    ]
    code = generator.generate(
        run_id="prec03",
        task_name="storage_state兼容",
        task_id="t_prec03",
        actions=actions,
        precondition_config={"target_url": "https://erp.example.com"},
    )

    # 验证 page.goto 是函数体第一个操作（在 docstring 之后）
    lines = code.splitlines()
    goto_line = None
    click_line = None
    for i, line in enumerate(lines):
        if "page.goto(" in line:
            goto_line = i
        if "page.locator(" in line:
            click_line = i

    assert goto_line is not None, "page.goto() should be in generated code"
    assert click_line is not None, "click action should be in generated code"
    assert goto_line < click_line, "page.goto() must appear before action steps"

    # 验证完整代码通过语法检查
    ast.parse(code)

    # 验证 storage_state 注入后执行顺序：
    # 1. conftest -> browser_context_args 设置 storage_state
    # 2. pytest 创建 page (自动加载 storage_state 到 localStorage)
    # 3. test 函数 -> page.goto() 加载 ERP 页面
    # 4. Vue app 初始化 -> 读取 localStorage Admin-Token -> 自动登录
    # 5. 后续操作在已认证页面上执行
    assert "page.goto(" in code
    assert "wait_for_load_state" in code
