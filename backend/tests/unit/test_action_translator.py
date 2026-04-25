"""ActionTranslator 单元测试 -- browser-use action 到 Playwright 代码翻译。

覆盖核心操作类型 + 边界情况 + 多定位器回退。
所有测试使用 mock DOMInteractedElement，不依赖 browser-use 内部模块。
"""

from dataclasses import dataclass

import pytest

from backend.core.action_translator import ActionTranslator


# ---------------------------------------------------------------------------
# Helper: 创建 mock DOMInteractedElement（模拟 browser-use DOMInteractedElement）
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MockDOMElement:
    """模拟 DOMInteractedElement 的 frozen dataclass，用于测试。

    复制关键属性：x_path, node_name, attributes, ax_name。
    不依赖 browser-use 内部类型。
    """

    x_path: str = "/html/body/div"
    node_name: str = "DIV"
    attributes: dict[str, str] | None = None
    ax_name: str | None = None


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def translator() -> ActionTranslator:
    """每个测试创建新的 ActionTranslator 实例。"""
    return ActionTranslator()


# ---------------------------------------------------------------------------
# 核心操作类型翻译测试
# ---------------------------------------------------------------------------


class TestClickTranslation:
    """click 操作翻译测试。"""

    def test_translate_click(self, translator: ActionTranslator) -> None:
        action = {
            "click": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/div[2]/form/button",
                node_name="BUTTON",
            ),
        }
        result = translator.translate(action)

        assert result.action_type == "click"
        assert result.is_comment is False
        assert result.has_locator is True
        assert 'page.locator("xpath=/html/body/div[2]/form/button").click()' in result.code


class TestInputTranslation:
    """input 操作翻译测试。"""

    def test_translate_input(self, translator: ActionTranslator) -> None:
        action = {
            "input": {"index": 12, "text": "测试数据", "clear": True},
            "interacted_element": MockDOMElement(
                x_path="/html/body/div[2]/form/input[1]",
                node_name="INPUT",
            ),
        }
        result = translator.translate(action)

        assert result.action_type == "input"
        assert result.is_comment is False
        assert result.has_locator is True
        assert '.fill("测试数据")' in result.code or ".fill('测试数据')" in result.code


class TestNavigateTranslation:
    """navigate 操作翻译测试。"""

    def test_translate_navigate(self, translator: ActionTranslator) -> None:
        action = {
            "navigate": {"url": "https://erp.example.com", "new_tab": False},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "navigate"
        assert result.is_comment is False
        assert result.has_locator is False
        assert 'page.goto("https://erp.example.com")' in result.code or "page.goto('https://erp.example.com')" in result.code


# ---------------------------------------------------------------------------
# 边界情况测试
# ---------------------------------------------------------------------------


class TestNonCoreActions:
    """非核心操作类型生成注释。"""

    def test_unknown_action_type_comment(self, translator: ActionTranslator) -> None:
        """未知操作类型生成注释。"""
        action = {
            "search_page": {"query": "test"},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "search_page"
        assert result.is_comment is True
        assert "# " in result.code

    # -- TRANSLATE-01: 未知类型 fallback 显示参数摘要 --

    def test_translate_unknown_fallback_shows_params(
        self, translator: ActionTranslator
    ) -> None:
        """真正未知的操作类型显示参数摘要，不显示'未翻译的操作类型'。"""
        action = {
            "custom_action": {"url": "https://example.com", "timeout": 30},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "custom_action"
        assert result.is_comment is True
        assert "# custom_action:" in result.code
        assert "参数=" in result.code
        assert "未翻译的操作类型" not in result.code

    def test_translate_unknown_fallback_empty_params(
        self, translator: ActionTranslator
    ) -> None:
        """未知类型空参数也显示参数摘要。"""
        action = {
            "mystery_op": {},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "mystery_op"
        assert result.is_comment is True
        assert "# mystery_op:" in result.code
        assert "参数={}" in result.code

    def test_translate_unknown_multiline_params(
        self, translator: ActionTranslator
    ) -> None:
        """未知类型参数含换行时，每行都有 # 前缀。"""
        action = {
            "custom_op": {"text": "line1\nline2"},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "custom_op"
        assert result.is_comment is True
        for line in result.code.split("\n"):
            assert line.startswith("    # "), f"Line does not start with '    # ': {line!r}"


# ---------------------------------------------------------------------------
# 核心 10 种操作回归测试 (TRANSLATE-02)
# ---------------------------------------------------------------------------


class TestCoreTypesRegression:
    """核心 10 种操作类型翻译不回归。

    验证所有核心类型（click, input, navigate, scroll, send_keys, go_back,
    wait, evaluate, select_dropdown, upload_file）仍然正确翻译为代码行，
    不生成注释且不含'未翻译的操作类型'。
    """

    @pytest.mark.parametrize(
        "action_type,action_data,elem",
        [
            (
                "click",
                {"index": 5},
                MockDOMElement(
                    x_path="/html/body/button",
                    node_name="BUTTON",
                ),
            ),
            (
                "input",
                {"index": 12, "text": "hello", "clear": True},
                MockDOMElement(
                    x_path="/html/body/input",
                    node_name="INPUT",
                ),
            ),
            (
                "navigate",
                {"url": "https://example.com", "new_tab": False},
                None,
            ),
            (
                "scroll",
                {"down": True, "pages": 1.0},
                None,
            ),
            (
                "send_keys",
                {"keys": "Enter"},
                None,
            ),
            (
                "go_back",
                {},
                None,
            ),
            (
                "wait",
                {"seconds": 2},
                None,
            ),
            (
                "evaluate",
                {"code": "document.title"},
                None,
            ),
            (
                "select_dropdown",
                {"index": 3, "text": "Option A"},
                MockDOMElement(
                    x_path="/html/body/select",
                    node_name="SELECT",
                ),
            ),
            (
                "upload_file",
                {"index": 2, "path": "/tmp/file.txt"},
                MockDOMElement(
                    x_path="/html/body/input[@type='file']",
                    node_name="INPUT",
                    attributes={"type": "file"},
                ),
            ),
        ],
    )
    def test_core_type_translates_to_code(
        self,
        translator: ActionTranslator,
        action_type: str,
        action_data: dict,
        elem: MockDOMElement | None,
    ) -> None:
        """每种核心操作翻译为代码行 (is_comment=False)，不含未翻译标记。"""
        action = {action_type: action_data, "interacted_element": elem}
        result = translator.translate(action)

        assert result.action_type == action_type
        assert result.is_comment is False, (
            f"{action_type} should translate to code, not comment"
        )
        assert "未翻译的操作类型" not in result.code


# ---------------------------------------------------------------------------
# 多定位器回退测试
# ---------------------------------------------------------------------------


class TestLocatorFallback:
    """多定位器 try-except 回退代码生成测试。"""

    def test_click_two_locators_generates_try_except(
        self, translator: ActionTranslator
    ) -> None:
        """click 操作有 xpath + id 两个定位器时，生成 try-except 结构。"""
        action = {
            "click": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/div/button",
                node_name="BUTTON",
                attributes={"id": "submit-btn"},
            ),
        }
        result = translator.translate(action)

        assert result.has_locator is True
        assert "try:" in result.code
        assert "except" in result.code
        assert ".click()" in result.code
