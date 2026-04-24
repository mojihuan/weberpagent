"""LocatorChainBuilder -- 从 DOMInteractedElement 提取多策略定位器链。

按优先级排序 (per D-01): XPath -> CSS by ID -> CSS by data-testid -> get_by_role -> get_by_placeholder。
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


class LocatorChainBuilder:
    """从 DOMInteractedElement 元数据生成 Playwright 定位器字符串列表。

    根据元素可用的属性 (x_path, id, data-testid, ax_name, placeholder)
    按优先级生成定位器表达式字符串，最多 3 个 (per D-02)。
    """

    def extract(self, elem: Any, action_type: str) -> list[str]:
        """从 DOMInteractedElement 提取最多 3 个定位器字符串。

        Args:
            elem: DOMInteractedElement 实例 (属性访问 x_path, node_name, attributes, ax_name)。
            action_type: 操作类型 ("click" or "input")。

        Returns:
            Playwright 定位器表达式字符串列表，如 ['page.locator("xpath=...")', ...]。
        """
        locators: list[str] = []

        # 1. XPath — 始终作为主定位器
        x_path = elem.x_path
        if not x_path:
            return []

        escaped_xpath = _escape_string(x_path)
        locators.append(f'page.locator("xpath={escaped_xpath}")')

        attrs = elem.attributes or {}

        # 2. CSS by ID (使用 [id="..."] 避免 CSS 特殊字符问题, per Pitfall 3)
        elem_id = attrs.get("id", "")
        if elem_id:
            escaped_id = _escape_string(elem_id)
            locators.append(f'page.locator("[id=\\"{escaped_id}\\"]")')

        # 3. CSS by data-testid
        testid = attrs.get("data-testid", "")
        if testid:
            escaped_testid = _escape_string(testid)
            locators.append(f'page.get_by_test_id("{escaped_testid}")')

        # 4. get_by_role (仅当 ax_name 存在且 node_name 映射到已知 role)
        ax_name = elem.ax_name
        if ax_name:
            role = _NODE_TO_ROLE.get(elem.node_name)
            if role:
                escaped_name = _escape_string(ax_name)
                locators.append(
                    f'page.get_by_role("{role}", name="{escaped_name}")'
                )

        # 5. get_by_placeholder (仅 input 操作且有 placeholder)
        if action_type == "input":
            placeholder = attrs.get("placeholder", "")
            if placeholder:
                escaped_placeholder = _escape_string(placeholder)
                locators.append(
                    f'page.get_by_placeholder("{escaped_placeholder}")'
                )

        # D-02: 最多 3 个定位器
        return locators[:3]
