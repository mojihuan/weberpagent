"""页面感知模块 - 获取截图和可交互元素"""

import base64
import hashlib
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
        # 1. 截图并转为 base64（设置超时，避免字体加载阻塞）
        screenshot_base64 = await self._take_screenshot()

        # 2. 获取页面基本信息
        url = self.page.url
        title = await self.page.title()

        # 3. 提取可交互元素
        elements = await self._extract_elements()

        # 4. 计算页面状态哈希（用于检测页面变化）
        state_hash = await self._compute_page_hash()

        return PageState(
            screenshot_base64=screenshot_base64,
            url=url,
            title=title,
            elements=elements,
            state_hash=state_hash,
        )

    async def _take_screenshot(self, max_retries: int = 3) -> str:
        """截图并转为 base64，带重试机制

        Args:
            max_retries: 最大重试次数

        Returns:
            base64 编码的截图，失败时返回占位图片
        """
        for attempt in range(max_retries):
            try:
                # 先等待页面稳定
                await self.page.wait_for_timeout(500)

                screenshot_bytes = await self.page.screenshot(
                    type="png",
                    timeout=30000,  # 30 秒超时
                    animations="disabled",  # 禁用动画加速截图
                )
                return base64.b64encode(screenshot_bytes).decode("utf-8")
            except Exception as e:
                print(f"⚠️ 截图失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await self.page.wait_for_timeout(1000)

        # 所有尝试都失败，返回一个最小的有效 PNG 图片 (1x1 透明像素)
        # 这样可以避免 API 报错，LLM 会依赖 DOM 信息做决策
        print("⚠️ 所有截图尝试失败，使用占位图片")
        placeholder_png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        )
        return base64.b64encode(placeholder_png).decode("utf-8")

        # 2. 获取页面基本信息
        url = self.page.url
        title = await self.page.title()

        # 3. 提取可交互元素
        elements = await self._extract_elements()

        # 4. 计算页面状态哈希（用于检测页面变化）
        state_hash = await self._compute_page_hash()

        return PageState(
            screenshot_base64=screenshot_base64,
            url=url,
            title=title,
            elements=elements,
            state_hash=state_hash,
        )

    # 元素数量上限
    MAX_ELEMENTS = 30

    async def _extract_elements(self) -> list[InteractiveElement]:
        """提取页面上的可交互元素

        优化：
        1. 按优先级智能排序（视口内、有文本、按钮优先）
        2. 提取 aria-label 和 title 属性
        3. 清理文本（去除多余空格）
        4. 限制元素数量

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

                    // 获取元素位置
                    const rect = el.getBoundingClientRect();
                    const isInViewport = (
                        rect.top >= 0 &&
                        rect.left >= 0 &&
                        rect.bottom <= window.innerHeight &&
                        rect.right <= window.innerWidth
                    );

                    // 清理文本：去除多余空格和换行
                    let text = (el.innerText || el.value || '')
                        .replace(/\\s+/g, ' ')
                        .trim()
                        .slice(0, 50);

                    // 计算优先级分数
                    let priority = 0;
                    if (text) priority += 30;
                    if (el.placeholder) priority += 20;
                    if (el.getAttribute('aria-label')) priority += 15;
                    if (el.id) priority += 10;
                    if (isInViewport) priority += 25;
                    if (el.tagName === 'BUTTON') priority += 15;
                    if (el.tagName === 'A') priority += 10;
                    if (el.tagName === 'INPUT') priority += 12;

                    result.push({
                        index: index,
                        tag: el.tagName,
                        text: text,
                        type: el.type || null,
                        id: el.id || null,
                        placeholder: el.placeholder || null,
                        name: el.name || null,
                        aria_label: el.getAttribute('aria-label') || null,
                        title: el.getAttribute('title') || null,
                        _priority: priority,
                        _isInViewport: isInViewport
                    });
                });

                // 按优先级排序
                result.sort((a, b) => b._priority - a._priority);

                // 移除内部字段并限制数量
                return result.slice(0, maxElements).map(el => {
                    const { _priority, _isInViewport, ...rest } = el;
                    return rest;
                });
            }
        """,
            [selector, self.MAX_ELEMENTS],
        )

        return [InteractiveElement(**el) for el in elements_data]

    async def _compute_page_hash(self) -> str:
        """计算页面状态哈希（用于检测页面变化）

        Returns:
            16 位 MD5 哈希值
        """
        # 使用 URL + 标题 + 主要元素文本计算哈希
        content = await self.page.evaluate(
            """
            () => {
                const url = window.location.href;
                const title = document.title;
                // 获取主要元素的文本
                const mainContent = document.body.innerText.slice(0, 1000);
                return url + title + mainContent;
            }
        """
        )

        return hashlib.md5(content.encode()).hexdigest()[:16]
