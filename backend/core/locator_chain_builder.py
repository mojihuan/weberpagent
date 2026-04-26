"""LocatorChainBuilder -- 从 DOMInteractedElement 提取多策略定位器链。

按优先级排序 (语义优先): get_by_text -> get_by_role -> get_by_placeholder -> CSS by ID -> CSS by data-testid -> XPath。
语义定位器（text/role/placeholder）对动态 DOM 更健壮，XPath 相对路径优先语义属性，绝对路径作为最后兜底。
每个操作最多 3 个定位器 (per D-02)。
"""

from __future__ import annotations

from typing import Any


# node_name (大写 HTML 标签) -> ARIA role 映射
_NODE_TO_ROLE: dict[str, str] = {
    "BUTTON": "button",
    "A": "link",
    "INPUT": "textbox",
    "SELECT": "combobox",
    "TEXTAREA": "textbox",
    "IMG": "img",
}


def _escape_string(value: str) -> str:
    """转义字符串中的特殊字符 (复用 ActionTranslator 的逻辑)。"""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _strip_pua_chars(text: str) -> str:
    """过滤 Unicode 基本私有使用区字符 (U+E000-U+F8FF)。

    这些是 icon font 渲染字符，不应出现在定位器文本中 (D-05)。
    仅过滤基本私有区，不过滤增补私有区（实际 ERP 场景几乎用不到）。
    """
    return "".join(c for c in text if not (0xE000 <= ord(c) <= 0xF8FF))


class LocatorChainBuilder:
    """从 DOMInteractedElement 元数据生成 Playwright 定位器字符串列表。

    根据元素可用的属性 (x_path, id, data-testid, ax_name, placeholder)
    按优先级生成定位器表达式字符串，最多 3 个 (per D-02)。
    """

    def extract(self, elem: Any, action_type: str) -> list[str]:
        """从 DOMInteractedElement 提取最多 3 个定位器字符串。

        语义定位器优先（对动态 DOM 更健壮），XPath 绝对路径作为最后兜底。

        Args:
            elem: DOMInteractedElement 实例 (属性访问 x_path, node_name, attributes, ax_name)。
            action_type: 操作类型 ("click" or "input")。

        Returns:
            Playwright 定位器表达式字符串列表，如 ['page.get_by_text("...")', ...]。
        """
        locators: list[str] = []
        attrs = elem.attributes or {}
        # D-06: 入口统一过滤 icon font 私有区字符，.strip() 去除首尾空白
        ax_name = _strip_pua_chars(elem.ax_name).strip() if elem.ax_name else None

        # 1. get_by_text — 有 ax_name 时优先使用文本定位
        # D-01: 短文本 (<=4 字符) 保留精确匹配，长文本使用模糊匹配
        if ax_name:
            escaped_name = _escape_string(ax_name)
            if len(ax_name) <= 4:
                locators.append(
                    f'page.get_by_text("{escaped_name}", exact=True)'
                )
            else:
                locators.append(
                    f'page.get_by_text("{escaped_name}")'
                )

        # 2. get_by_role (当 node_name 映射到已知 ARIA role 时)
        if ax_name:
            role = _NODE_TO_ROLE.get(elem.node_name)
            if role:
                escaped_name = _escape_string(ax_name)
                locators.append(
                    f'page.get_by_role("{role}", name="{escaped_name}")'
                )

        # 3. get_by_placeholder (仅 input 操作且有 placeholder)
        if action_type == "input":
            placeholder = attrs.get("placeholder", "")
            if placeholder:
                escaped_placeholder = _escape_string(placeholder)
                locators.append(
                    f'page.get_by_placeholder("{escaped_placeholder}")'
                )

        # 4. CSS by ID (使用 [id="..."] 避免 CSS 特殊字符问题)
        elem_id = attrs.get("id", "")
        if elem_id:
            escaped_id = _escape_string(elem_id)
            locators.append(f'page.locator("[id=\\"{escaped_id}\\"]")')

        # 5. CSS by data-testid
        testid = attrs.get("data-testid", "")
        if testid:
            escaped_testid = _escape_string(testid)
            locators.append(f'page.get_by_test_id("{escaped_testid}")')

        # 6. XPath — 相对路径优先语义属性，绝对路径作为最后兜底
        # D-03/D-04: 相对 XPath 优先语义属性 (data-testid > id)，无语义属性时回退绝对路径
        x_path = elem.x_path
        if x_path:
            testid = attrs.get("data-testid", "")
            elem_id = attrs.get("id", "")
            tag = elem.node_name.lower()
            if testid:
                escaped = _escape_string(testid)
                locators.append(f'page.locator("xpath=//{tag}[@data-testid=\\"{escaped}\\"]")')
            elif elem_id:
                escaped = _escape_string(elem_id)
                locators.append(f'page.locator("xpath=//{tag}[@id=\\"{escaped}\\"]")')
            else:
                escaped = _escape_string(x_path)
                locators.append(f'page.locator("xpath={escaped}")')

        # D-02: 最多 3 个定位器
        return locators[:3]
