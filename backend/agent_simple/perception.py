"""页面感知模块 - 获取截图和可交互元素"""

import base64
from typing import Any

from playwright.async_api import Page

from backend.agent_simple.types import PageState, InteractiveElement


class Perception:
    """页面感知模块

    负责获取页面截图和提取可交互元素列表
    """

    # 可交互元素的 CSS 选择器
    INTERACTIVE_SELECTORS = [
        "button",
        "a[href]",
        "input",
        "select",
        "textarea",
        "[onclick]",
        '[role="button"]',
        '[role="link"]',
        '[role="checkbox"]',
        '[role="radio"]',
        '[tabindex]:not([tabindex="-1"])',
    ]

    def __init__(self, page: Page):
        """初始化感知模块

        Args:
            page: Playwright Page 对象
        """
        self.page = page

    async def get_state(self) -> PageState:
        """获取当前页面状态

        Returns:
            PageState: 包含截图和可交互元素的页面状态
        """
        # 1. 截图并转为 base64
        screenshot_bytes = await self.page.screenshot(type="png")
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")

        # 2. 获取页面基本信息
        url = self.page.url
        title = await self.page.title()

        # 3. 提取可交互元素
        elements = await self._extract_elements()

        return PageState(
            screenshot_base64=screenshot_base64,
            url=url,
            title=title,
            elements=elements,
        )

    # 元素数量上限
    MAX_ELEMENTS = 30

    async def _extract_elements(self) -> list[InteractiveElement]:
        """提取页面上的可交互元素

        优化：
        1. 提取 aria-label 和 title 属性
        2. 清理文本（去除多余空格）
        3. 限制元素数量（优先保留有文本/placeholder 的元素）

        Returns:
            可交互元素列表
        """
        selector = ", ".join(self.INTERACTIVE_SELECTORS)

        # 使用参数传递方式避免引号转义问题
        elements_data = await self.page.evaluate(
            """
            ([selector, maxElements]) => {
                const elements = document.querySelectorAll(selector);
                const result = [];

                elements.forEach((el, index) => {
                    // 跳过隐藏元素
                    const style = window.getComputedStyle(el);
                    if (style.display === 'none' || style.visibility === 'hidden') {
                        return;
                    }

                    // 跳过禁用元素
                    if (el.disabled) {
                        return;
                    }

                    // 清理文本：去除多余空格和换行
                    let text = (el.innerText || el.value || '')
                        .replace(/\\s+/g, ' ')
                        .trim()
                        .slice(0, 50);

                    result.push({
                        index: index,
                        tag: el.tagName,
                        text: text,
                        type: el.type || null,
                        id: el.id || null,
                        placeholder: el.placeholder || null,
                        name: el.name || null,
                        aria_label: el.getAttribute('aria-label') || null,
                        title: el.getAttribute('title') || null
                    });
                });

                // 优先保留有文本、placeholder、aria-label 的元素
                const withContent = result.filter(el =>
                    el.text || el.placeholder || el.aria_label
                );
                const withoutContent = result.filter(el =>
                    !el.text && !el.placeholder && !el.aria_label
                );

                // 合并并限制数量
                const sorted = [...withContent, ...withoutContent];
                return sorted.slice(0, maxElements);
            }
        """,
            [selector, self.MAX_ELEMENTS],
        )

        return [InteractiveElement(**el) for el in elements_data]

    def format_elements_for_prompt(self, elements: list[InteractiveElement]) -> str:
        """格式化元素列表用于 Prompt

        Args:
            elements: 可交互元素列表

        Returns:
            格式化后的字符串
        """
        if not elements:
            return "（页面上没有可交互元素）"

        lines = []
        for el in elements:
            # 构建元素描述
            parts = [f"[{el.index}] <{el.tag}>"]

            if el.text:
                parts.append(f'文本: "{el.text}"')
            if el.type:
                parts.append(f"类型: {el.type}")
            if el.placeholder:
                parts.append(f'占位符: "{el.placeholder}"')
            if el.id:
                parts.append(f"ID: {el.id}")
            if el.name:
                parts.append(f"Name: {el.name}")

            lines.append(" | ".join(parts))

        return "\n".join(lines)
