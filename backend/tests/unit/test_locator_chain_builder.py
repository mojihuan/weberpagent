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
        """有 x_path + id + data-testid 的元素返回 3 个定位器（无 ax_name 时 ID 优先）。"""
        elem = MockDOMElement(
            x_path="/html/body/div[2]/form/button",
            node_name="BUTTON",
            attributes={"id": "submit-btn", "data-testid": "submit"},
        )
        locators = builder.extract(elem, "click")

        assert len(locators) == 3
        # CSS ID locator (语义优先：无 ax_name 时 ID 排第一)
        assert 'page.locator("[id=\\"submit-btn\\"]")' in locators[0]
        # data-testid locator
        assert 'page.get_by_test_id("submit")' in locators[1]
        # XPath locator — 相对路径使用 data-testid (D-03 优先级)
        assert 'page.locator("xpath=//button[@data-testid=\\"submit\\"]")' in locators[2]

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
        locators = builder.extract(elem, "input")

        assert len(locators) == 3

    def test_none_attributes_safe(self, builder: LocatorChainBuilder) -> None:
        """attributes 为 None 时不崩溃，只返回 xpath 定位器（绝对路径兜底）。"""
        elem = MockDOMElement(
            x_path="/html/body/div",
            node_name="DIV",
            attributes=None,
        )
        locators = builder.extract(elem, "click")

        assert len(locators) == 1
        assert "xpath=/html/body/div" in locators[0]

    # --- Phase 106: icon font / exact / 相对 XPath 测试 ---

    def test_pua_only_ax_name_skips_text_role(self, builder: LocatorChainBuilder) -> None:
        """PUA-only ax_name (\ue6d9\ue6da) 过滤后为空，跳过 get_by_text 和 get_by_role (D-02/D-05)。"""
        elem = MockDOMElement(
            ax_name="\ue6d9\ue6da",
            x_path="/html/body/button",
            node_name="BUTTON",
        )
        locators = builder.extract(elem, "click")
        assert len(locators) > 0, "应至少有 XPath 兜底定位器"
        assert all("get_by_text" not in loc for loc in locators), (
            f"PUA-only ax_name 不应生成 get_by_text: {locators}"
        )
        assert all("get_by_role" not in loc for loc in locators), (
            f"PUA-only ax_name 不应生成 get_by_role: {locators}"
        )

    def test_pua_mixed_strips_and_keeps_text(self, builder: LocatorChainBuilder) -> None:
        """PUA 混合文本 '\ue6d9提交\ue6da' 过滤后为 '提交'，保留 text/role 定位器 (D-05/D-06/D-01)。"""
        elem = MockDOMElement(
            ax_name="\ue6d9提交\ue6da",
            x_path="/html/body/button",
            node_name="BUTTON",
        )
        locators = builder.extract(elem, "click")
        assert 'page.get_by_text("提交", exact=True)' in locators, (
            f"2 字符应保留 exact=True: {locators}"
        )
        assert 'page.get_by_role("button", name="提交")' in locators, (
            f"应生成 role 定位器: {locators}"
        )

    def test_whitespace_only_after_pua_strip(self, builder: LocatorChainBuilder) -> None:
        """PUA 过滤 + strip() 后为空字符串，跳过 get_by_text (D-02)。"""
        elem = MockDOMElement(
            ax_name="  \ue6d9  ",
            x_path="/html/body/button",
            node_name="BUTTON",
        )
        locators = builder.extract(elem, "click")
        assert len(locators) > 0, "应至少有 XPath 兜底定位器"
        assert all("get_by_text" not in loc for loc in locators), (
            f"空白-only ax_name 不应生成 get_by_text: {locators}"
        )

    def test_long_text_fuzzy_match(self, builder: LocatorChainBuilder) -> None:
        """长文本 (>4 字符) get_by_text 不带 exact=True (D-01)。"""
        elem = MockDOMElement(
            ax_name="提交并确认",
            x_path="/html/body/button",
            node_name="BUTTON",
        )
        locators = builder.extract(elem, "click")
        assert 'page.get_by_text("提交并确认")' in locators, (
            f"5 字符应不带 exact: {locators}"
        )
        text_locator = [loc for loc in locators if "get_by_text" in loc][0]
        assert "exact" not in text_locator, (
            f"长文本不应包含 exact: {text_locator}"
        )

    def test_short_text_exact_match(self, builder: LocatorChainBuilder) -> None:
        """短文本 (<=4 字符) get_by_text 保留 exact=True (D-01)。"""
        elem = MockDOMElement(
            ax_name="提交",
            x_path="/html/body/button",
            node_name="BUTTON",
        )
        locators = builder.extract(elem, "click")
        assert 'page.get_by_text("提交", exact=True)' in locators, (
            f"2 字符应保留 exact=True: {locators}"
        )

    def test_four_char_boundary_exact(self, builder: LocatorChainBuilder) -> None:
        """4 字符边界：'确认提交' 刚好 4 字符，保留 exact=True (D-01)。"""
        elem = MockDOMElement(
            ax_name="确认提交",
            x_path="/html/body/button",
            node_name="BUTTON",
        )
        locators = builder.extract(elem, "click")
        assert 'page.get_by_text("确认提交", exact=True)' in locators, (
            f"4 字符边界应保留 exact=True: {locators}"
        )

    def test_relative_xpath_with_data_testid(self, builder: LocatorChainBuilder) -> None:
        """有 data-testid 时 XPath 使用相对路径 //tagname[@data-testid] (D-03/D-04)。"""
        elem = MockDOMElement(
            x_path="/html/body/div[2]/form/button",
            node_name="BUTTON",
            attributes={"data-testid": "submit-btn"},
        )
        locators = builder.extract(elem, "click")
        assert 'page.locator("xpath=//button[@data-testid=\\"submit-btn\\"]")' in locators, (
            f"应使用 data-testid 相对 XPath: {locators}"
        )

    def test_relative_xpath_with_id_no_testid(self, builder: LocatorChainBuilder) -> None:
        """有 id 但无 data-testid 时 XPath 使用相对路径 //tagname[@id] (D-03)。"""
        elem = MockDOMElement(
            x_path="/html/body/div[2]/form/button",
            node_name="BUTTON",
            attributes={"id": "submit-btn"},
        )
        locators = builder.extract(elem, "click")
        assert 'page.locator("xpath=//button[@id=\\"submit-btn\\"]")' in locators, (
            f"应使用 id 相对 XPath: {locators}"
        )

    def test_absolute_xpath_fallback(self, builder: LocatorChainBuilder) -> None:
        """无语义属性时回退到绝对 XPath (D-03 fallback)。"""
        elem = MockDOMElement(
            x_path="/html/body/div",
            node_name="DIV",
            attributes=None,
        )
        locators = builder.extract(elem, "click")
        assert len(locators) >= 1
        assert "xpath=/html/body/div" in locators[0], (
            f"无语义属性应回退绝对路径: {locators}"
        )

    def test_data_testid_preferred_over_id(self, builder: LocatorChainBuilder) -> None:
        """同时有 data-testid 和 id 时，XPath 使用 data-testid 而非 id (D-03 priority)。"""
        elem = MockDOMElement(
            x_path="/html/body/button",
            node_name="BUTTON",
            attributes={"data-testid": "btn", "id": "submit"},
        )
        locators = builder.extract(elem, "click")
        xpath_locators = [loc for loc in locators if "xpath=" in loc]
        assert len(xpath_locators) >= 1, f"应有 XPath 定位器: {locators}"
        xpath_loc = xpath_locators[-1]
        assert "data-testid" in xpath_loc, (
            f"XPath 应优先使用 data-testid: {xpath_loc}"
        )
        assert "id=" not in xpath_loc, (
            f"XPath 不应使用 id (data-testid 优先): {xpath_loc}"
        )
