"""动作执行模块 - 执行 Playwright 动作"""

import logging
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

from backend.agent_simple.types import Action, ActionResult, InteractiveElement

logger = logging.getLogger(__name__)


class Executor:
    """动作执行模块

    负责将 LLM 决策的动作转换为 Playwright 操作并执行
    """

    def __init__(self, page: Page, timeout: int = 30000):
        """初始化执行模块

        Args:
            page: Playwright Page 对象
            timeout: 操作超时时间（毫秒）
        """
        self.page = page
        self.timeout = timeout

    async def execute(
        self,
        action: Action,
        elements: list[InteractiveElement],
    ) -> ActionResult:
        """执行动作

        Args:
            action: LLM 决策的动作
            elements: 当前页面的可交互元素列表

        Returns:
            ActionResult: 执行结果
        """
        logger.info(f"执行动作: {action.action}, 目标: {action.target}, 值: {action.value}")

        try:
            if action.action == "navigate":
                return await self._navigate(action.value or "")
            elif action.action == "click":
                return await self._click(action.target, elements)
            elif action.action == "input":
                return await self._input(action.target, action.value, elements)
            elif action.action == "wait":
                return await self._wait()
            elif action.action == "done":
                return ActionResult(success=True, error=None)
            else:
                return ActionResult(
                    success=False,
                    error=f"未知动作类型: {action.action}",
                )
        except PlaywrightTimeoutError as e:
            logger.error(f"动作执行超时: {e}")
            return ActionResult(success=False, error=f"操作超时: {str(e)}")
        except Exception as e:
            logger.error(f"动作执行失败: {e}")
            return ActionResult(success=False, error=str(e))

    async def _navigate(self, url: str) -> ActionResult:
        """导航到指定 URL"""
        if not url:
            return ActionResult(success=False, error="URL 不能为空")

        # 自动补全协议
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        logger.info(f"导航到: {url}")
        await self.page.goto(url, timeout=self.timeout)
        await self.page.wait_for_load_state("networkidle")

        return ActionResult(success=True)

    async def _click(
        self,
        target: str | None,
        elements: list[InteractiveElement],
    ) -> ActionResult:
        """点击目标元素"""
        if not target:
            return ActionResult(success=False, error="点击目标不能为空")

        # 尝试定位元素
        locator = await self._locate_element(target, elements)

        if locator:
            await locator.click(timeout=self.timeout)
            logger.info(f"点击成功: {target}")
            return ActionResult(success=True)
        else:
            # 直接尝试通过文本点击
            try:
                await self.page.get_by_text(target).click(timeout=self.timeout)
                logger.info(f"通过文本点击成功: {target}")
                return ActionResult(success=True)
            except Exception as e:
                logger.warning(f"点击失败: {target}, 错误: {e}")
                return ActionResult(
                    success=False,
                    error=f"无法找到元素: {target}",
                )

    async def _input(
        self,
        target: str | None,
        value: str | None,
        elements: list[InteractiveElement],
    ) -> ActionResult:
        """在目标元素中输入文本"""
        if not target:
            return ActionResult(success=False, error="输入目标不能为空")
        if value is None:
            return ActionResult(success=False, error="输入值不能为空")

        # 尝试定位元素
        locator = await self._locate_element(target, elements)

        if locator:
            # 先点击聚焦，再输入
            await locator.click(timeout=self.timeout)
            await locator.fill(value, timeout=self.timeout)
            logger.info(f"输入成功: {target} <- {value}")
            return ActionResult(success=True)
        else:
            # 直接尝试通过 placeholder 定位
            try:
                await self.page.get_by_placeholder(target).fill(
                    value, timeout=self.timeout
                )
                logger.info(f"通过 placeholder 输入成功: {target}")
                return ActionResult(success=True)
            except Exception:
                # 尝试通过 label 定位
                try:
                    await self.page.get_by_label(target).fill(
                        value, timeout=self.timeout
                    )
                    logger.info(f"通过 label 输入成功: {target}")
                    return ActionResult(success=True)
                except Exception as e:
                    logger.warning(f"输入失败: {target}, 错误: {e}")
                    return ActionResult(
                        success=False,
                        error=f"无法找到输入框: {target}",
                    )

    async def _wait(self) -> ActionResult:
        """等待页面稳定"""
        logger.info("等待页面加载...")
        await self.page.wait_for_timeout(1000)
        await self.page.wait_for_load_state("networkidle")
        return ActionResult(success=True)

    async def _locate_element(
        self,
        target: str,
        elements: list[InteractiveElement],
    ):
        """定位元素

        定位策略（优先级从高到低）：
        1. 精确匹配文本
        2. 精确匹配 placeholder
        3. 模糊匹配文本
        4. 模糊匹配 placeholder
        5. 索引定位（如果 target 是数字）

        Args:
            target: 目标元素描述
            elements: 可交互元素列表

        Returns:
            Playwright Locator 或 None
        """
        # 1. 精确匹配文本
        for el in elements:
            if el.text and target == el.text:
                logger.debug(f"精确匹配文本: {el.text}")
                return self.page.get_by_text(el.text, exact=True)

        # 2. 精确匹配 placeholder
        for el in elements:
            if el.placeholder and target == el.placeholder:
                logger.debug(f"精确匹配 placeholder: {el.placeholder}")
                return self.page.get_by_placeholder(el.placeholder, exact=True)

        # 3. 模糊匹配文本
        for el in elements:
            if el.text and target in el.text:
                logger.debug(f"模糊匹配文本: {el.text}")
                return self.page.get_by_text(el.text)

        # 4. 模糊匹配 placeholder
        for el in elements:
            if el.placeholder and target in el.placeholder:
                logger.debug(f"模糊匹配 placeholder: {el.placeholder}")
                return self.page.get_by_placeholder(el.placeholder)

        # 5. 索引定位
        if target.isdigit():
            idx = int(target)
            if 0 <= idx < len(elements):
                el = elements[idx]
                logger.debug(f"索引定位: [{idx}] {el.tag}")
                # 使用通用选择器
                return self.page.locator(
                    f"{el.tag.lower()}:visible >> nth={idx}"
                )

        return None
