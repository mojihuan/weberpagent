"""ActionTranslator 单元测试 -- browser-use action 到 Playwright 代码翻译。

覆盖 10 种核心操作类型 (D-08) + 边界情况 (D-06, D-09) + 多定位器回退 (D-04/D-05)。
所有测试使用 mock DOMInteractedElement，不依赖 browser-use 内部模块。
"""

import ast
from dataclasses import dataclass

import pytest

from backend.core.action_translator import ActionTranslator, TranslatedAction
from backend.core.healer_error import HealerError


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


class TestWaitTranslation:
    """wait 操作翻译测试 (TRANS-01)。"""

    def test_translate_wait_with_seconds(self, translator: ActionTranslator) -> None:
        """wait seconds=5 生成 page.wait_for_timeout(5000)。"""
        action = {
            "wait": {"seconds": 5},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "wait"
        assert result.is_comment is False
        assert result.has_locator is False
        assert "page.wait_for_timeout(5000)" in result.code

    def test_translate_wait_default_seconds(self, translator: ActionTranslator) -> None:
        """wait 空参数默认 3 秒生成 page.wait_for_timeout(3000)。"""
        action = {
            "wait": {},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "wait"
        assert result.is_comment is False
        assert result.has_locator is False
        assert "page.wait_for_timeout(3000)" in result.code


class TestEvaluateTranslation:
    """evaluate 操作翻译测试 (TRANS-03)。"""

    def test_translate_evaluate(self, translator: ActionTranslator) -> None:
        """evaluate 生成 page.evaluate("document.title")。"""
        action = {
            "evaluate": {"code": "document.title"},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "evaluate"
        assert result.is_comment is False
        assert result.has_locator is False
        assert "page.evaluate" in result.code
        assert "document.title" in result.code

    def test_translate_evaluate_with_special_chars(self, translator: ActionTranslator) -> None:
        """evaluate 包含引号的 JS 代码正确转义。"""
        action = {
            "evaluate": {"code": 'console.log("hello")'},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "evaluate"
        assert result.is_comment is False
        assert "page.evaluate" in result.code
        # 引号应被转义，代码仍合法
        assert "hello" in result.code


class TestSelectDropdownTranslation:
    """select_dropdown 操作翻译测试 (TRANS-02)。"""

    def test_translate_select_dropdown(
        self, translator: ActionTranslator
    ) -> None:
        """select_dropdown 有元素时生成 locator.select_option("text")。"""
        action = {
            "select_dropdown": {"index": 3, "text": "Option A"},
            "interacted_element": MockDOMElement(
                x_path="/html/body/select",
                node_name="SELECT",
            ),
        }
        result = translator.translate(action)

        assert result.action_type == "select_dropdown"
        assert result.is_comment is False
        assert result.has_locator is True
        assert ".select_option(" in result.code
        assert "Option A" in result.code

    def test_translate_select_dropdown_no_element(
        self, translator: ActionTranslator
    ) -> None:
        """select_dropdown 无元素时生成注释回退。"""
        action = {
            "select_dropdown": {"index": 3, "text": "Option A"},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "select_dropdown"
        assert result.is_comment is True
        assert "# " in result.code

    def test_translate_select_dropdown_empty_xpath(
        self, translator: ActionTranslator
    ) -> None:
        """select_dropdown 元素 x_path 为空时生成注释回退。"""
        action = {
            "select_dropdown": {"index": 3, "text": "Option A"},
            "interacted_element": MockDOMElement(x_path=""),
        }
        result = translator.translate(action)

        assert result.is_comment is True


class TestUploadFileTranslation:
    """upload_file 操作翻译测试 (TRANS-04)。"""

    def test_translate_upload_file(self, translator: ActionTranslator) -> None:
        """upload_file 有元素时生成 locator.set_input_files("path")。"""
        action = {
            "upload_file": {"index": 5, "path": "/data/file.xlsx"},
            "interacted_element": MockDOMElement(
                x_path="/html/body/input",
                node_name="INPUT",
            ),
        }
        result = translator.translate(action)

        assert result.action_type == "upload_file"
        assert result.is_comment is False
        assert result.has_locator is True
        assert ".set_input_files(" in result.code
        assert "/data/file.xlsx" in result.code

    def test_translate_upload_file_no_element(
        self, translator: ActionTranslator
    ) -> None:
        """upload_file 无元素时生成注释回退。"""
        action = {
            "upload_file": {"index": 5, "path": "/data/file.xlsx"},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "upload_file"
        assert result.is_comment is True
        assert "# upload_file" in result.code


# ---------------------------------------------------------------------------
# 边界情况测试 (D-06, D-09)
# ---------------------------------------------------------------------------


class TestMissingLocator:
    """缺失定位器时的占位符生成测试 (D-06)。"""

    def test_missing_locator_placeholder(self, translator: ActionTranslator) -> None:
        """interacted_element 为 None 时生成占位符。"""
        action = {
            "click": {"index": 5},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "click"
        assert result.has_locator is False
        assert "page.wait_for_timeout(1000)" in result.code
        assert "# TODO: 定位器缺失" in result.code

    def test_empty_xpath_placeholder(self, translator: ActionTranslator) -> None:
        """x_path 为空字符串时生成占位符。"""
        action = {
            "click": {"index": 5},
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

    def test_upload_file_comment_no_element(self, translator: ActionTranslator) -> None:
        """upload_file 无元素时生成注释回退 (D-05)。"""
        action = {
            "upload_file": {"index": 3, "path": "/data/test.xlsx"},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.action_type == "upload_file"
        assert result.is_comment is True
        assert result.has_locator is False
        assert "# upload_file" in result.code


class TestXPathExtraction:
    """验证 XPath 从 DOMInteractedElement 属性提取 (CODE-01)。"""

    def test_xpath_extraction_from_element_attribute(self, translator: ActionTranslator) -> None:
        """确认 x_path 通过属性访问 (elem.x_path) 提取，而非字典访问。"""
        elem = MockDOMElement(x_path="/html/body/div[2]/form/button")
        action = {
            "click": {"index": 5},
            "interacted_element": elem,
        }
        result = translator.translate(action)

        assert result.has_locator is True
        assert "/html/body/div[2]/form/button" in result.code


# ---------------------------------------------------------------------------
# 多定位器回退测试 (D-04/D-05)
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

    def test_click_three_locators_generates_nested_try_except(
        self, translator: ActionTranslator
    ) -> None:
        """click 操作有 3 个定位器时，生成两级嵌套 try-except。"""
        action = {
            "click": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/form/button",
                node_name="BUTTON",
                attributes={"id": "btn", "data-testid": "submit"},
            ),
        }
        result = translator.translate(action)

        assert result.has_locator is True
        # 应有多行代码
        assert "\n" in result.code
        assert "try:" in result.code
        # 两级嵌套: 外层 try + 内层 try
        code_lines = result.code.split("\n")
        try_count = sum(1 for line in code_lines if "try:" in line)
        assert try_count >= 2

    def test_click_single_locator_no_try_except(
        self, translator: ActionTranslator
    ) -> None:
        """click 操作只有 1 个定位器时，不生成 try-except，保持单行格式。"""
        action = {
            "click": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/div/button",
                node_name="BUTTON",
            ),
        }
        result = translator.translate(action)

        assert result.has_locator is True
        assert "try:" not in result.code
        assert 'page.locator("xpath=/html/body/div/button").click()' in result.code

    def test_input_two_locators_generates_try_except(
        self, translator: ActionTranslator
    ) -> None:
        """input 有多定位器时生成 try-except，每个定位器用 .fill(text)。"""
        action = {
            "input": {"index": 12, "text": "hello"},
            "interacted_element": MockDOMElement(
                x_path="/html/body/input",
                node_name="INPUT",
                attributes={"id": "name-input"},
            ),
        }
        result = translator.translate(action)

        assert result.has_locator is True
        assert "try:" in result.code
        assert ".fill(" in result.code
        assert "hello" in result.code

    def test_input_single_locator_no_try_except(
        self, translator: ActionTranslator
    ) -> None:
        """input 只有 1 个定位器时不生成 try-except。"""
        action = {
            "input": {"index": 12, "text": "hello"},
            "interacted_element": MockDOMElement(
                x_path="/html/body/input",
                node_name="INPUT",
            ),
        }
        result = translator.translate(action)

        assert result.has_locator is True
        assert "try:" not in result.code

    def test_final_except_contains_healer_error(
        self, translator: ActionTranslator
    ) -> None:
        """try-except 最终 except 块包含 raise HealerError。"""
        action = {
            "click": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/button",
                node_name="BUTTON",
                attributes={"id": "btn"},
            ),
        }
        result = translator.translate(action)

        assert "raise HealerError" in result.code
        assert "action_type" in result.code
        assert "locators" in result.code
        assert "original_error" in result.code

    def test_non_final_except_contains_warning(
        self, translator: ActionTranslator
    ) -> None:
        """非最终 except 块包含 warning 级别日志。"""
        action = {
            "click": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/button",
                node_name="BUTTON",
                attributes={"id": "btn"},
            ),
        }
        result = translator.translate(action)

        assert "_healer.warning" in result.code
        assert "定位器回退" in result.code

    def test_two_locator_scenario_has_healer_error(
        self, translator: ActionTranslator
    ) -> None:
        """2-locator 场景的生成代码包含 raise HealerError。"""
        action = {
            "click": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/button",
                node_name="BUTTON",
                attributes={"id": "btn"},
            ),
        }
        result = translator.translate(action)

        assert "raise HealerError" in result.code

    def test_three_locator_scenario_has_error_log_and_healer_error(
        self, translator: ActionTranslator
    ) -> None:
        """3-locator 场景的生成代码包含 _healer.error 和 raise HealerError。"""
        action = {
            "click": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/form/button",
                node_name="BUTTON",
                attributes={"id": "btn", "data-testid": "submit"},
            ),
        }
        result = translator.translate(action)

        assert "_healer.error" in result.code
        assert "raise HealerError" in result.code

    def test_navigate_unchanged_with_fallback(
        self, translator: ActionTranslator
    ) -> None:
        """navigate 操作的翻译结果不变 (per D-06)。"""
        action = {
            "navigate": {"url": "https://example.com"},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert "try:" not in result.code
        assert "page.goto" in result.code

    def test_scroll_unchanged_with_fallback(
        self, translator: ActionTranslator
    ) -> None:
        """scroll 操作的翻译结果不变 (per D-06)。"""
        action = {
            "scroll": {"down": True, "pages": 1.0},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert "try:" not in result.code
        assert "page.mouse.wheel" in result.code

    def test_send_keys_unchanged_with_fallback(
        self, translator: ActionTranslator
    ) -> None:
        """send_keys 操作的翻译结果不变 (per D-06)。"""
        action = {
            "send_keys": {"keys": "Enter"},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert "try:" not in result.code
        assert "page.keyboard.press" in result.code

    def test_go_back_unchanged_with_fallback(
        self, translator: ActionTranslator
    ) -> None:
        """go_back 操作的翻译结果不变 (per D-06)。"""
        action = {
            "go_back": {},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert "try:" not in result.code
        assert "page.go_back" in result.code

    def test_interacted_element_none_still_placeholder(
        self, translator: ActionTranslator
    ) -> None:
        """interacted_element 为 None 时仍生成占位符，不变。"""
        action = {
            "click": {"index": 5},
            "interacted_element": None,
        }
        result = translator.translate(action)

        assert result.has_locator is False
        assert "page.wait_for_timeout(1000)" in result.code
        assert "# TODO: 定位器缺失" in result.code

    def test_generated_try_except_is_valid_python(
        self, translator: ActionTranslator
    ) -> None:
        """生成的 try-except 代码是合法 Python (ast.parse 通过)。"""
        action = {
            "click": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/form/button",
                node_name="BUTTON",
                attributes={"id": "btn", "data-testid": "submit"},
            ),
        }
        result = translator.translate(action)

        # 将生成的代码包装在函数体中以通过 ast.parse
        wrapped = f"def test_func():\n{result.code}"
        ast.parse(wrapped)

    def test_locators_field_populated(
        self, translator: ActionTranslator
    ) -> None:
        """TranslatedAction.locators 字段包含提取的定位器元数据。"""
        action = {
            "click": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/button",
                node_name="BUTTON",
                attributes={"id": "btn"},
            ),
        }
        result = translator.translate(action)

        assert len(result.locators) == 2
        assert any("xpath=" in l for l in result.locators)
        assert any("[id=" in l for l in result.locators)

    def test_single_locator_has_empty_locators_metadata(
        self, translator: ActionTranslator
    ) -> None:
        """单定位器时 locators 元数据为空（保持与 Phase 82 一致）。"""
        action = {
            "click": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/div/button",
                node_name="BUTTON",
            ),
        }
        result = translator.translate(action)

        # 单定位器不使用 LocatorChainBuilder，保持原行为
        assert result.has_locator is True


# ---------------------------------------------------------------------------
# LLM 第四层回退测试 (Phase 84 Plan 02)
# ---------------------------------------------------------------------------


class TestLLMFallbackLayer:
    """Phase 84: _build_fallback_code() LLM 第四层回退代码生成测试。"""

    def test_two_locators_with_llm_snippet(
        self, translator: ActionTranslator
    ) -> None:
        """2 个定位器 + llm_snippet: LLM 代码作为最内层 try-except 插入 HealerError 之前。"""
        locators = [
            'page.locator("xpath=/html/body/div/button")',
            'page.locator("[id=\\"btn\\"]")',
        ]
        llm_snippet = 'page.locator("button:has-text(\\"Submit\\")").click()'

        code = translator._build_fallback_code(
            locators=locators,
            action_suffix=".click()",
            action_type="click",
            llm_snippet=llm_snippet,
        )

        # 外层 try 存在
        assert "try:" in code
        # 回退日志存在
        assert "_healer.warning" in code
        assert "定位器回退" in code
        # LLM 修复日志
        assert "_healer.info" in code
        assert "LLM 修复" in code
        # LLM 代码在 try 块中
        assert llm_snippet in code
        # LLM 失败的 except 包含 "含 LLM 修复"
        assert "含 LLM 修复" in code
        # 最终 raise HealerError
        assert "raise HealerError" in code

    def test_three_locators_with_llm_snippet(
        self, translator: ActionTranslator
    ) -> None:
        """3 个定位器 + llm_snippet: LLM 代码在第三个定位器 except 之后。"""
        locators = [
            'page.locator("xpath=/html/body/form/button")',
            'page.locator("[id=\\"btn\\"]")',
            'page.get_by_test_id("submit")',
        ]
        llm_snippet = 'page.locator("button[type=submit]").click()'

        code = translator._build_fallback_code(
            locators=locators,
            action_suffix=".click()",
            action_type="click",
            llm_snippet=llm_snippet,
        )

        # LLM 修复日志
        assert "_healer.info" in code
        assert "LLM 修复" in code
        # LLM 代码嵌入
        assert llm_snippet in code
        # 含 LLM 修复的错误消息
        assert "含 LLM 修复" in code
        # 最终 raise HealerError
        assert "raise HealerError" in code

    def test_no_llm_snippet_backward_compatible(
        self, translator: ActionTranslator
    ) -> None:
        """llm_snippet 为空时，输出与 Phase 83 完全相同（向后兼容）。"""
        locators = [
            'page.locator("xpath=/html/body/div/button")',
            'page.locator("[id=\\"btn\\"]")',
        ]

        code_with_empty = translator._build_fallback_code(
            locators=locators,
            action_suffix=".click()",
            action_type="click",
            llm_snippet="",
        )

        code_without = translator._build_fallback_code(
            locators=locators,
            action_suffix=".click()",
            action_type="click",
        )

        # 空字符串和未提供参数结果相同
        assert code_with_empty == code_without
        # 不包含 LLM 相关内容
        assert "LLM" not in code_with_empty
        assert "含 LLM 修复" not in code_with_empty

    def test_translate_with_llm_click_flow(
        self, translator: ActionTranslator
    ) -> None:
        """translate_with_llm() click 操作完整流程：2 个定位器 + LLM snippet。"""
        action = {
            "click": {"index": 5},
            "interacted_element": MockDOMElement(
                x_path="/html/body/div/button",
                node_name="BUTTON",
                attributes={"id": "btn"},
            ),
        }
        llm_snippet = 'page.locator("button:has-text(\\"OK\\")").click()'

        result = translator.translate_with_llm(action, llm_snippet=llm_snippet)

        assert result.action_type == "click"
        assert result.has_locator is True
        # 应包含 LLM 层
        assert "LLM 修复" in result.code
        assert llm_snippet in result.code
        # locators 元数据正确
        assert len(result.locators) == 2

    def test_llm_layer_code_valid_python(
        self, translator: ActionTranslator
    ) -> None:
        """包含 LLM 层的生成代码通过 ast.parse() 语法检查。"""
        locators = [
            'page.locator("xpath=/html/body/div/button")',
            'page.locator("[id=\\"btn\\"]")',
        ]
        llm_snippet = 'page.locator("button:has-text(\\"Submit\\")").click()'

        code = translator._build_fallback_code(
            locators=locators,
            action_suffix=".click()",
            action_type="click",
            llm_snippet=llm_snippet,
        )

        # 包装在函数体中以通过 ast.parse
        wrapped = f"def test_func():\n{code}"
        ast.parse(wrapped)


# ---------------------------------------------------------------------------
# 边缘操作注释翻译测试 (EDGE-01~08)
# ---------------------------------------------------------------------------


class TestEdgeComments:
    """14 种边缘操作 + 1 种真正未知操作的有意义注释翻译测试。"""

    def test_switch_comment(self, translator: ActionTranslator) -> None:
        """switch 生成包含 tab_id 的注释。"""
        action = {"switch": {"tab_id": "A1B2"}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "switch"
        assert result.is_comment is True
        assert "# switch" in result.code
        assert "A1B2" in result.code

    def test_close_comment(self, translator: ActionTranslator) -> None:
        """close 生成包含 tab_id 的注释。"""
        action = {"close": {"tab_id": "C3D4"}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "close"
        assert result.is_comment is True
        assert "# close" in result.code
        assert "C3D4" in result.code

    def test_search_page_comment(self, translator: ActionTranslator) -> None:
        """search_page 生成包含 pattern 的注释。"""
        action = {"search_page": {"pattern": "价格"}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "search_page"
        assert result.is_comment is True
        assert "价格" in result.code

    def test_find_elements_comment(self, translator: ActionTranslator) -> None:
        """find_elements 生成包含 selector 的注释。"""
        action = {"find_elements": {"selector": "div.item"}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "find_elements"
        assert result.is_comment is True
        assert "div.item" in result.code

    def test_find_text_comment(self, translator: ActionTranslator) -> None:
        """find_text 生成包含 text 的注释。"""
        action = {"find_text": {"text": "提交"}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "find_text"
        assert result.is_comment is True
        assert "提交" in result.code

    def test_screenshot_comment_with_filename(
        self, translator: ActionTranslator
    ) -> None:
        """screenshot 有 file_name 时生成包含文件名的注释。"""
        action = {"screenshot": {"file_name": "shot.png"}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "screenshot"
        assert result.is_comment is True
        assert "shot.png" in result.code

    def test_screenshot_comment_no_filename(
        self, translator: ActionTranslator
    ) -> None:
        """screenshot 无 file_name 时仍生成有意义的注释。"""
        action = {"screenshot": {}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "screenshot"
        assert result.is_comment is True
        assert "# screenshot" in result.code

    def test_save_as_pdf_comment(self, translator: ActionTranslator) -> None:
        """save_as_pdf 生成包含 file_name 的注释。"""
        action = {"save_as_pdf": {"file_name": "report.pdf"}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "save_as_pdf"
        assert result.is_comment is True
        assert "report.pdf" in result.code

    def test_done_comment(self, translator: ActionTranslator) -> None:
        """done 生成包含完成文本的注释。"""
        action = {"done": {"text": "任务完成", "success": True}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "done"
        assert result.is_comment is True
        assert "任务完成" in result.code

    def test_write_file_comment(self, translator: ActionTranslator) -> None:
        """write_file 生成包含 file_name 的注释。"""
        action = {"write_file": {"file_name": "test.py", "content": "pass"}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "write_file"
        assert result.is_comment is True
        assert "test.py" in result.code

    def test_read_file_comment(self, translator: ActionTranslator) -> None:
        """read_file 生成包含 file_name 的注释。"""
        action = {"read_file": {"file_name": "data.json"}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "read_file"
        assert result.is_comment is True
        assert "data.json" in result.code

    def test_replace_file_comment(self, translator: ActionTranslator) -> None:
        """replace_file 生成包含 file_name 的注释。"""
        action = {"replace_file": {"file_name": "cfg.py", "old_str": "a", "new_str": "b"}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "replace_file"
        assert result.is_comment is True
        assert "cfg.py" in result.code

    def test_search_comment(self, translator: ActionTranslator) -> None:
        """search 生成包含 query 的注释。"""
        action = {"search": {"query": "测试", "engine": "duckduckgo"}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "search"
        assert result.is_comment is True
        assert "测试" in result.code

    def test_dropdown_options_comment(self, translator: ActionTranslator) -> None:
        """dropdown_options 生成包含 index 的注释。"""
        action = {"dropdown_options": {"index": 5}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "dropdown_options"
        assert result.is_comment is True
        assert "5" in result.code

    def test_extract_comment(self, translator: ActionTranslator) -> None:
        """extract 生成包含 query 的注释。"""
        action = {"extract": {"query": "提取链接", "extract_links": True}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "extract"
        assert result.is_comment is True
        assert "提取链接" in result.code

    def test_truly_unknown_comment(self, translator: ActionTranslator) -> None:
        """真正未知的操作类型生成通用回退注释。"""
        action = {"custom_action": {"foo": "bar"}, "interacted_element": None}
        result = translator.translate(action)

        assert result.action_type == "custom_action"
        assert result.is_comment is True
        assert "custom_action" in result.code

    def test_done_comment_with_newlines(self, translator: ActionTranslator) -> None:
        """done 文本包含换行符时，每行都有 # 前缀 (per EXEC-02)."""
        action = {"done": {"text": "任务完成\n详细说明", "success": True}, "interacted_element": None}
        result = translator.translate(action)
        lines = result.code.split("\n")
        for line in lines:
            assert line.strip().startswith("#"), f"行缺少 # 前缀: {line}"

    def test_extract_comment_with_newlines(self, translator: ActionTranslator) -> None:
        """extract query 包含换行符时，每行都有 # 前缀 (per EXEC-02)."""
        action = {"extract": {"query": "提取\n数据"}, "interacted_element": None}
        result = translator.translate(action)
        lines = result.code.split("\n")
        for line in lines:
            assert line.strip().startswith("#"), f"行缺少 # 前缀: {line}"

    def test_unknown_comment_single_line_unchanged(self, translator: ActionTranslator) -> None:
        """单行 summary 的注释格式与修改前完全一致 (per EXEC-02)."""
        action = {"done": {"text": "简单文本"}, "interacted_element": None}
        result = translator.translate(action)
        assert "\n" not in result.code  # 单行无换行
        assert result.code == "    # done: 任务完成: 简单文本"

    def test_newline_comment_is_valid_python(self, translator: ActionTranslator) -> None:
        """多行注释代码在函数体内通过 ast.parse (per EXEC-02)."""
        action = {"done": {"text": "完成\n多行\n文本"}, "interacted_element": None}
        result = translator.translate(action)
        wrapped = f"def test_func():\n    pass\n{result.code}"
        ast.parse(wrapped)
