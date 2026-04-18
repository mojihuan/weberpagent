"""LocatorChainBuilder 单元测试 -- 定位器链提取验证。

验证 LocatorChainBuilder 从 DOMInteractedElement 元数据提取最多 3 个 Playwright 定位器字符串。
使用 MockDOMElement 模拟 browser-use DOMInteractedElement。
"""

from dataclasses import dataclass

import pytest

from backend.core.locator_chain_builder import LocatorChainBuilder


# ---------------------------------------------------------------------------
# Helper: 模拟 DOMInteractedElement
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MockDOMElement:
    """模拟 DOMInteractedElement 的 frozen dataclass。"""

    x_path: str = "/html/body/div"
    node_name: str = "DIV"
    attributes: dict[str, str] | None = None
    ax_name: str | None = None


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def builder() -> LocatorChainBuilder:
    """每个测试创建新的 LocatorChainBuilder 实例。"""
    return LocatorChainBuilder()


# ---------------------------------------------------------------------------
# 定位器提取测试
# ---------------------------------------------------------------------------


class TestLocatorExtraction:
    """定位器提取优先级和数量验证。"""

    def test_three_locators_from_rich_element(self, builder: LocatorChainBuilder) -> None:
        """有 x_path + id + data-testid 的元素返回 3 个定位器。"""
        elem = MockDOMElement(
            x_path="/html/body/div[2]/form/button",
            node_name="BUTTON",
            attributes={"id": "submit-btn", "data-testid": "submit"},
        )
        locators = builder.extract(elem, "click_element")

        assert len(locators) == 3
        # XPath locator
        assert 'page.locator("xpath=/html/body/div[2]/form/button")' in locators[0]
        # CSS ID locator (using [id="..."] per Pitfall 3)
        assert 'page.locator("[id=\\"submit-btn\\"]")' in locators[1]
        # data-testid locator
        assert 'page.get_by_test_id("submit")' in locators[2]

    def test_xpath_and_role_from_button_with_ax_name(
        self, builder: LocatorChainBuilder
    ) -> None:
        """有 x_path + ax_name 的 BUTTON 返回 xpath + get_by_role 定位器。"""
        elem = MockDOMElement(
            x_path="/html/body/div/button",
            node_name="BUTTON",
            ax_name="提交",
        )
        locators = builder.extract(elem, "click_element")

        assert len(locators) == 2
        assert 'page.locator("xpath=/html/body/div/button")' in locators[0]
        assert 'page.get_by_role("button", name="提交")' in locators[1]

    def test_placeholder_locator_for_input_text(
        self, builder: LocatorChainBuilder
    ) -> None:
        """INPUT 有 placeholder 时返回 get_by_placeholder 定位器（仅 input_text）。"""
        elem = MockDOMElement(
            x_path="/html/body/div/input",
            node_name="INPUT",
            attributes={"placeholder": "请输入名称"},
        )
        locators = builder.extract(elem, "input_text")

        # 应包含 get_by_placeholder
        placeholder_locators = [l for l in locators if "get_by_placeholder" in l]
        assert len(placeholder_locators) == 1
        assert "请输入名称" in placeholder_locators[0]

    def test_no_placeholder_for_click_element(
        self, builder: LocatorChainBuilder
    ) -> None:
        """click_element 操作不包含 get_by_placeholder 定位器。"""
        elem = MockDOMElement(
            x_path="/html/body/div/input",
            node_name="INPUT",
            attributes={"placeholder": "请输入名称"},
        )
        locators = builder.extract(elem, "click_element")

        placeholder_locators = [l for l in locators if "get_by_placeholder" in l]
        assert len(placeholder_locators) == 0

    def test_none_attributes_safe(self, builder: LocatorChainBuilder) -> None:
        """attributes 为 None 时不崩溃，只返回 xpath 定位器。"""
        elem = MockDOMElement(
            x_path="/html/body/div",
            node_name="DIV",
            attributes=None,
        )
        locators = builder.extract(elem, "click_element")

        assert len(locators) == 1
        assert "xpath=/html/body/div" in locators[0]

    def test_empty_xpath_returns_empty(self, builder: LocatorChainBuilder) -> None:
        """x_path 为空字符串时返回空列表。"""
        elem = MockDOMElement(x_path="", node_name="DIV")
        locators = builder.extract(elem, "click_element")

        assert locators == []

    def test_max_three_locators(self, builder: LocatorChainBuilder) -> None:
        """最多返回 3 个定位器 (D-02)，即使有更多可用选项。"""
        elem = MockDOMElement(
            x_path="/html/body/form/input",
            node_name="INPUT",
            attributes={
                "id": "name-input",
                "data-testid": "name-field",
                "placeholder": "请输入名称",
            },
            ax_name="名称",
        )
        locators = builder.extract(elem, "input_text")

        assert len(locators) == 3

    def test_link_role_mapping(self, builder: LocatorChainBuilder) -> None:
        """A 标签映射到 "link" 角色。"""
        elem = MockDOMElement(
            x_path="/html/body/a",
            node_name="A",
            ax_name="点击这里",
        )
        locators = builder.extract(elem, "click_element")

        role_locators = [l for l in locators if "get_by_role" in l]
        assert len(role_locators) == 1
        assert 'page.get_by_role("link", name="点击这里")' in role_locators[0]


class TestNodeToRoleMapping:
    """node_name 到 ARIA role 的映射验证。"""

    def test_button_to_button(self, builder: LocatorChainBuilder) -> None:
        """BUTTON -> "button"。"""
        elem = MockDOMElement(x_path="/btn", node_name="BUTTON", ax_name="OK")
        locators = builder.extract(elem, "click_element")
        assert any("get_by_role" in l and '"button"' in l for l in locators)

    def test_a_to_link(self, builder: LocatorChainBuilder) -> None:
        """A -> "link"。"""
        elem = MockDOMElement(x_path="/a", node_name="A", ax_name="Home")
        locators = builder.extract(elem, "click_element")
        assert any("get_by_role" in l and '"link"' in l for l in locators)

    def test_input_to_textbox(self, builder: LocatorChainBuilder) -> None:
        """INPUT -> "textbox"。"""
        elem = MockDOMElement(x_path="/input", node_name="INPUT", ax_name="用户名")
        locators = builder.extract(elem, "input_text")
        assert any("get_by_role" in l and '"textbox"' in l for l in locators)

    def test_no_role_without_ax_name(self, builder: LocatorChainBuilder) -> None:
        """ax_name 为 None 时不生成 get_by_role 定位器。"""
        elem = MockDOMElement(x_path="/btn", node_name="BUTTON", ax_name=None)
        locators = builder.extract(elem, "click_element")

        assert not any("get_by_role" in l for l in locators)

    def test_unknown_node_no_role(self, builder: LocatorChainBuilder) -> None:
        """未知 node_name 不生成 get_by_role 定位器。"""
        elem = MockDOMElement(x_path="/div", node_name="SPAN", ax_name="text")
        locators = builder.extract(elem, "click_element")

        assert not any("get_by_role" in l for l in locators)
