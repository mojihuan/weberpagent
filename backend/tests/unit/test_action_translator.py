"""ActionTranslator 单元测试 -- browser-use action 到 Playwright 代码翻译。

覆盖 6 种核心操作类型 (D-08) + 边界情况 (D-06, D-09)。
所有测试使用 mock DOMInteractedElement，不依赖 browser-use 内部模块。
"""

from dataclasses import dataclass

import pytest

from backend.core.action_translator import ActionTranslator, TranslatedAction


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
# 核心操作类型翻译测试 (D-08)
# ---------------------------------------------------------------------------


class TestClickTranslation:
    """click_element 操作翻译测试。"""

    def test_translate_click(self, translator: ActionTranslator) -> None:
        action = {
            "click_element": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/div[2]/form/button",
                node_name="BUTTON",
            ),
        }
        result = translator.translate(action)

        assert result.action_type == "click_element"
        assert result.is_comment is False
        assert result.has_locator is True
        assert 'page.locator("xpath=/html/body/div[2]/form/button").click()' in result.code


class TestInputTranslation:
    """input_text 操作翻译测试。"""

    def test_translate_input(self, translator: ActionTranslator) -> None:
        action = {
            "input_text": {"index": 12, "text": "测试数据", "clear": True},
            "interacted_element": MockDOMElement(
                x_path="/html/body/div[2]/form/input[1]",
                node_name="INPUT",
            ),
        }
        result = translator.translate(action)

        assert result.action_type == "input_text"
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


class TestScrollTranslation:
    """scroll 操作翻译测试。"""

    def test_translate_scroll_down(self, translator: ActionTranslator) -> None:
        action = {
            "scroll": {"down": True, "pages": 1.0},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "scroll"
        assert result.is_comment is False
        assert result.has_locator is False
        assert "page.mouse.wheel(0, 1000)" in result.code

    def test_translate_scroll_up(self, translator: ActionTranslator) -> None:
        action = {
            "scroll": {"down": False, "pages": 1.0},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "scroll"
        assert "page.mouse.wheel(0, -1000)" in result.code

    def test_translate_scroll_custom_pages(self, translator: ActionTranslator) -> None:
        """滚动多页时 delta = pages * VIEWPORT_HEIGHT。"""
        action = {
            "scroll": {"down": True, "pages": 2.0},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert "page.mouse.wheel(0, 2000)" in result.code


class TestSendKeysTranslation:
    """send_keys 操作翻译测试。"""

    def test_translate_send_keys(self, translator: ActionTranslator) -> None:
        action = {
            "send_keys": {"keys": "Enter"},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "send_keys"
        assert result.is_comment is False
        assert result.has_locator is False
        assert 'page.keyboard.press("Enter")' in result.code or "page.keyboard.press('Enter')" in result.code


class TestGoBackTranslation:
    """go_back 操作翻译测试。"""

    def test_translate_go_back(self, translator: ActionTranslator) -> None:
        action = {
            "go_back": {},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "go_back"
        assert result.is_comment is False
        assert result.has_locator is False
        assert "page.go_back()" in result.code


# ---------------------------------------------------------------------------
# 边界情况测试 (D-06, D-09)
# ---------------------------------------------------------------------------


class TestMissingLocator:
    """缺失定位器时的占位符生成测试 (D-06)。"""

    def test_missing_locator_placeholder(self, translator: ActionTranslator) -> None:
        """interacted_element 为 None 时生成占位符。"""
        action = {
            "click_element": {"index": 5},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "click_element"
        assert result.has_locator is False
        assert "page.wait_for_timeout(1000)" in result.code
        assert "# TODO: 定位器缺失" in result.code

    def test_empty_xpath_placeholder(self, translator: ActionTranslator) -> None:
        """x_path 为空字符串时生成占位符。"""
        action = {
            "click_element": {"index": 5},
            "interacted_element": MockDOMElement(x_path=""),
        }
        result = translator.translate(action)

        assert result.has_locator is False
        assert "page.wait_for_timeout(1000)" in result.code
        assert "# TODO: 定位器缺失" in result.code


class TestNonCoreActions:
    """非核心操作类型生成注释 (D-08, D-09)。"""

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

    def test_upload_file_comment(self, translator: ActionTranslator) -> None:
        """upload_file 操作生成注释，包含文件路径 (D-09)。"""
        action = {
            "upload_file": {"index": 3, "path": "/data/test.xlsx"},
            "interacted_element": MockDOMElement(
                x_path="/html/body/div/form/input",
            ),
        }
        result = translator.translate(action)

        assert result.action_type == "upload_file"
        assert result.is_comment is True
        assert result.has_locator is False
        assert "# upload_file: /data/test.xlsx" in result.code


class TestXPathExtraction:
    """验证 XPath 从 DOMInteractedElement 属性提取 (CODE-01)。"""

    def test_xpath_extraction_from_element_attribute(self, translator: ActionTranslator) -> None:
        """确认 x_path 通过属性访问 (elem.x_path) 提取，而非字典访问。"""
        elem = MockDOMElement(x_path="/html/body/div[2]/form/button")
        action = {
            "click_element": {"index": 5},
            "interacted_element": elem,
        }
        result = translator.translate(action)

        assert result.has_locator is True
        assert "/html/body/div[2]/form/button" in result.code
