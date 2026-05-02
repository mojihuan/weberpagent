"""LocatorChainBuilder -- 从 DOMInteractedElement 提取多策略定位器链。

按优先级排序 (语义优先): get_by_role -> get_by_text/CSS[placeholder] -> CSS class -> XPath。
- 非 INPUT 元素: get_by_role -> get_by_text -> get_by_placeholder -> CSS class -> XPath
- INPUT/TEXTAREA: get_by_role -> CSS[placeholder] -> CSS class -> XPath
  (跳过 get_by_text，因为 placeholder 不是 text node；用 CSS 属性选择器替代 get_by_placeholder)
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

        对于 INPUT/TEXTAREA 元素：
        - 跳过 get_by_text（placeholder 不是 text node，根本性错误）
        - 优先 CSS 属性选择器 (input[placeholder='...'])，比 get_by_placeholder 更底层可靠

        Args:
            elem: DOMInteractedElement 实例 (属性访问 x_path, node_name, attributes, ax_name)。
            action_type: 操作类型 ("click" or "input")。

        Returns:
            Playwright 定位器表达式字符串列表，如 ['page.get_by_text("...")', ...]。
        """
        locators: list[str] = []
        attrs = elem.attributes or {}
        is_input_elem = elem.node_name in ("INPUT", "TEXTAREA")

        # D-06: 入口统一过滤 icon font 私有区字符，.strip() 去除首尾空白
        ax_name = _strip_pua_chars(elem.ax_name).strip() if elem.ax_name else None

        # 0. 如果 ax_name 为空，尝试从 title/aria-label 提取文本
        if not ax_name:
            for attr_key in ("title", "aria-label"):
                val = attrs.get(attr_key, "")
                if val:
                    ax_name = _strip_pua_chars(val).strip()
                    break

        # 1. 语义定位器 — role 优先于 text (ARIA 语义锚定更稳定)
        if ax_name:
            escaped_name = _escape_string(ax_name)
            # 优先使用元素实际的 role 属性（如 Element UI InputNumber 的 spinbutton），
            # 回退到标签名 → ARIA role 的默认映射
            actual_role = attrs.get("role", "")
            role = actual_role or _NODE_TO_ROLE.get(elem.node_name)
            if role:
                # INPUT/TEXTAREA 在表格中可能有多个同 placeholder 的 input，
                # 加 .first 避免 strict mode 报错
                suffix = ".first" if is_input_elem else ""
                locators.append(
                    f'page.get_by_role("{role}", name="{escaped_name}"){suffix}'
                )
            # INPUT/TEXTAREA 的 ax_name 通常来自 placeholder，
            # get_by_text 匹配的是 text node 而非属性值，对 input 无效
            if not is_input_elem:
                if len(ax_name) <= 4:
                    locators.append(
                        f'page.get_by_text("{escaped_name}", exact=True)'
                    )
                else:
                    locators.append(
                        f'page.get_by_text("{escaped_name}")'
                    )

        # 2. INPUT/TEXTAREA: CSS 属性选择器优先于 get_by_placeholder
        #    CSS 选择器更底层，不受 Playwright 语义解析影响
        #    外层用双引号，属性值内用转义双引号
        #    加 .first 避免 strict mode（表格中可能有多个同 placeholder 的 input）
        placeholder = attrs.get("placeholder", "")
        if placeholder and is_input_elem:
            escaped_placeholder = _escape_string(placeholder)
            tag = elem.node_name.lower()
            locators.append(
                f'page.locator("{tag}[placeholder=\\"{escaped_placeholder}\\"]").first'
            )

        # 3. get_by_placeholder (非 INPUT/TEXTAREA 或无 placeholder 时的回退;
        #    click 操作也可能需要通过 placeholder 定位输入框)
        if placeholder and not is_input_elem:
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

        # 6. CSS class-based locator — 使用元素的 class 属性生成 CSS 选择器
        #    对于绝对 xpath 定位的弹窗/下拉选项元素，CSS class 更稳定
        class_value = attrs.get("class", "")
        if class_value and len(locators) < 3:
            css_selector = self._build_class_selector(class_value, elem.node_name, ax_name=ax_name)
            if css_selector:
                locators.append(css_selector)

        # 7. XPath — 优先相对路径，绝对路径作为最后兜底
        # D-03/D-04: 相对 XPath 优先语义属性 (data-testid > id)，无语义属性时回退绝对路径
        x_path = elem.x_path
        if x_path and len(locators) < 3:
            testid_attr = attrs.get("data-testid", "")
            elem_id_attr = attrs.get("id", "")
            tag = elem.node_name.lower()
            if testid_attr:
                escaped = _escape_string(testid_attr)
                locators.append(f'page.locator("xpath=//{tag}[@data-testid=\\"{escaped}\\"]")')
            elif elem_id_attr:
                escaped = _escape_string(elem_id_attr)
                locators.append(f'page.locator("xpath=//{tag}[@id=\\"{escaped}\\"]")')
            else:
                # 尝试生成相对 XPath (去掉 html/body/div[N]/ 前缀)
                relative_xpath = self._to_relative_xpath(x_path, tag)
                if relative_xpath and relative_xpath != x_path:
                    escaped = _escape_string(relative_xpath)
                    locators.append(f'page.locator("xpath={escaped}")')
                # 绝对路径作为最终兜底
                if len(locators) < 3:
                    escaped = _escape_string(x_path)
                    locators.append(f'page.locator("xpath={escaped}")')

        # D-02: 最多 3 个定位器
        return locators[:3]

    @staticmethod
    def _build_class_selector(class_value: str, node_name: str, ax_name: str | None = None) -> str | None:
        """从 class 属性生成 CSS 选择器定位器。

        选择第一个有意义的 CSS class（排除过短的通用 class），
        与 tag name 组合成 CSS 选择器。

        - 非 INPUT 元素：当 ax_name 可用时使用 .filter(has_text="...") 精确定位
        - INPUT/TEXTAREA 元素：使用 .first（has_text 对 input 无效）

        Args:
            class_value: 元素的 class 属性值。
            node_name: 元素标签名（大写）。
            ax_name: 元素的 accessible name，用于文本过滤精确定位。

        Returns:
            CSS 选择器定位器字符串，或 None。
        """
        is_input = node_name in ("INPUT", "TEXTAREA")
        classes = class_value.split()
        tag = node_name.lower()
        for cls in classes:
            # 跳过过短的 class（通常是通用样式如 'active', 'selected'）
            if len(cls) < 5:
                continue
            escaped_cls = _escape_string(cls)
            base = f'page.locator("{tag}.{escaped_cls}")'
            # INPUT/TEXTAREA 的 ax_name 来自 placeholder，不是 text node
            if is_input:
                return f'{base}.first'
            if ax_name:
                escaped_name = _escape_string(ax_name)
                return f'{base}.filter(has_text="{escaped_name}").first'
            return f'{base}.first'
        return None

    @staticmethod
    def _to_relative_xpath(x_path: str, tag: str) -> str | None:
        """将绝对 XPath 转换为相对 XPath，去掉不稳定的 body/div[N] 前缀。

        例如: html/body/div[5]/div[1]/div[1]/ul/li[2]/span
              -> //ul/li[2]/span

        策略: 找到第一个语义标签 (ul, ol, table, form, nav, section, main, aside)
        作为相对起点，保留后续路径。

        Args:
            x_path: 绝对 XPath 字符串。
            tag: 元素标签名（小写）。

        Returns:
            相对 XPath 字符串，或 None 如果无法生成有意义的相对路径。
        """
        # 从 xpath 中找到第一个语义标签的位置
        semantic_tags = {"ul", "ol", "table", "form", "nav", "section", "main", "aside", "header", "footer"}
        parts = x_path.split("/")
        for i, part in enumerate(parts):
            # 提取标签名（去掉 [N] 索引）
            tag_name = part.split("[")[0].lower()
            if tag_name in semantic_tags:
                relative = "/".join(parts[i:])
                return f"//{relative}"
        return None
