"""动作执行模块 - 执行 Playwright 动作"""

import logging
import re
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

from backend.agent_simple.types import Action, ActionResult, InteractiveElement, PageState
from backend.agent_simple.form_filler.orchestrator import FormFiller

logger = logging.getLogger(__name__)


def _normalize_text(text: str) -> str:
    """规范化文本用于比较

    - 移除所有空白字符
    - 转为小写

    Args:
        text: 原始文本

    Returns:
        规范化后的文本
    """
    return re.sub(r'\s+', '', text.lower())


class Executor:
    """动作执行模块

    负责将 LLM 决策的动作转换为 Playwright 操作并执行
    """

    # 区域选择器映射
    REGION_SELECTORS = {
        'sidebar': 'aside, .sidebar, .side-nav, nav',
        'header': 'header, .header',
        'main': 'main, .main, .content',
        'footer': 'footer, .footer',
        'modal': '.modal, .dialog, [role="dialog"]',
    }

    def __init__(self, page: Page, llm=None, timeout: int = 30000):
        """初始化执行模块

        Args:
            page: Playwright Page 对象
            llm: LLM 实例（用于 fill_form）
            timeout: 操作超时时间（毫秒）
        """
        self.page = page
        self.llm = llm
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
            elif action.action == "fill_form":
                return await self._fill_form(action, elements)
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
        # 使用 domcontentloaded 而非 load，更快响应
        await self.page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")
        # 等待网络稳定，但使用较短的超时
        try:
            await self.page.wait_for_load_state("networkidle", timeout=10000)
        except PlaywrightTimeoutError:
            logger.warning("networkidle 超时，继续执行")
        # 额外等待确保页面渲染
        await self.page.wait_for_timeout(1000)

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
            try:
                # 策略 1: 正常点击
                await locator.click(timeout=self.timeout)
                logger.info(f"点击成功: {target}")
                return ActionResult(success=True)
            except Exception as e:
                error_str = str(e).lower()

                # 策略 1.5: 如果是 strict mode 违规（多个匹配元素），尝试 .first
                if "strict mode violation" in error_str:
                    try:
                        await locator.first.click(timeout=self.timeout)
                        logger.info(f"通过 .first 点击成功（解决 strict mode）: {target}")
                        return ActionResult(success=True)
                    except Exception as first_error:
                        logger.debug(f".first 点击也失败: {first_error}")

                # 策略 2: force 点击（跳过可见性检查）
                if "not visible" in error_str or "covered" in error_str:
                    try:
                        await locator.click(force=True, timeout=self.timeout)
                        logger.info(f"Force 点击成功: {target}")
                        return ActionResult(success=True)
                    except Exception as force_error:
                        pass

                # 策略 3: JavaScript 点击
                try:
                    element_handle = await locator.element_handle(timeout=5000)
                    await self.page.evaluate("el => el.click()", element_handle)
                    logger.info(f"JavaScript 点击成功: {target}")
                    return ActionResult(success=True)
                except Exception as js_error:
                    logger.warning(f"所有点击策略都失败: {target}")

                return ActionResult(success=False, error=f"点击失败: {str(e)[:100]}")
        else:
            # 策略 4: 在侧边栏区域内查找（优先）
            try:
                sidebar_locator = self.page.locator(
                    'aside, .sidebar, .side-nav, nav, .ant-layout-sider, .el-aside, [class*="sidebar"], [class*="menu"]'
                ).get_by_text(target, exact=True).first
                await sidebar_locator.click(timeout=self.timeout)
                logger.info(f"通过侧边栏区域限定点击成功: {target}")
                return ActionResult(success=True)
            except Exception as e:
                logger.debug(f"侧边栏区域限定点击失败: {e}")

            # 策略 5: 使用 .first 避免严格模式错误
            try:
                await self.page.get_by_text(target).first.click(timeout=self.timeout)
                logger.info(f"通过 .first 点击成功: {target}")
                return ActionResult(success=True)
            except Exception as e:
                # 策略 6: 通过 role 点击
                try:
                    await self.page.get_by_role("button", name=target).click(timeout=self.timeout)
                    logger.info(f"通过 role 点击成功: {target}")
                    return ActionResult(success=True)
                except Exception:
                    return ActionResult(success=False, error=f"无法找到元素: {target}")

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
            try:
                # 尝试正常点击和输入
                await locator.click(timeout=self.timeout)
                await locator.fill(value, timeout=self.timeout)
                logger.info(f"输入成功: {target} <- {value}")
                return ActionResult(success=True)
            except Exception as e:
                error_str = str(e).lower()
                # 如果是可见性问题或超时，尝试 force 模式
                if "not visible" in error_str or "not attached" in error_str or "timeout" in error_str:
                    try:
                        # 使用 Playwright 的 force 模式（跳过可见性检查，但保留原生行为）
                        await locator.fill(value, timeout=self.timeout, force=True)
                        logger.info(f"强制输入成功: {target} <- {value}")
                        return ActionResult(success=True)
                    except Exception as force_error:
                        try:
                            # 最后尝试：使用 JavaScript 直接操作（确保视觉更新）
                            element_handle = await locator.element_handle(timeout=5000)
                            await self.page.evaluate(
                                """([el, val]) => {
                                    // 使用原生 setter 确保响应式更新
                                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                                        window.HTMLInputElement.prototype, 'value'
                                    ).set;
                                    nativeInputValueSetter.call(el, val);

                                    // 触发 React/Vue 需要的事件
                                    el.dispatchEvent(new Event('input', { bubbles: true }));
                                    el.dispatchEvent(new Event('change', { bubbles: true }));
                                }""",
                                [element_handle, value]
                            )
                            logger.info(f"JavaScript 输入成功: {target} <- {value}")
                            return ActionResult(success=True)
                        except Exception as js_error:
                            logger.warning(f"JavaScript 输入也失败: {target}, 错误: {js_error}")

                logger.warning(f"输入失败: {target}, 错误: {e}")
                return ActionResult(success=False, error=f"输入失败: {str(e)[:100]}")

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
        """等待页面稳定

        策略：
        1. 先等待 1 秒让页面有时间响应
        2. 尝试等待 networkidle（最多 5 秒）
        3. 如果超时，降级为 domcontentloaded
        4. 最后再等待 500ms 确保渲染完成
        """
        logger.info("等待页面加载...")
        await self.page.wait_for_timeout(1000)

        # 尝试等待 networkidle，但有超时保护
        try:
            await self.page.wait_for_load_state("networkidle", timeout=5000)
            logger.info("页面网络空闲")
        except PlaywrightTimeoutError:
            logger.warning("networkidle 超时，降级为 domcontentloaded")
            # 降级：等待 domcontentloaded（通常已经满足）
            try:
                await self.page.wait_for_load_state("domcontentloaded", timeout=3000)
            except PlaywrightTimeoutError:
                logger.warning("domcontentloaded 也超时，继续执行")

        # 额外等待确保渲染
        await self.page.wait_for_timeout(500)
        return ActionResult(success=True)

    async def validate_action(
        self,
        action,  # Action type from types.py
        elements: list,  # list[InteractiveElement]
    ) -> tuple[bool, str | None]:
        """执行前验证动作是否可行

        Args:
            action: 要验证的动作
            elements: 可交互元素列表

        Returns:
            (is_valid, error_message)
        """
        if action.action == "done":
            return True, None

        if action.action == "navigate":
            if not action.value:
                return False, "navigate 动作需要 value（URL）"
            return True, None

        if action.action in ["click", "input"]:
            if not action.target:
                return False, f"{action.action} 动作需要 target"

            # 检测数字索引
            if action.target.strip().isdigit():
                return False, f"禁止使用数字索引 '{action.target}'，请使用元素文本、placeholder 或 ID"

            # 检查元素是否存在
            locator = await self._locate_element(action.target, elements)
            if not locator:
                return False, f"找不到元素: {action.target}"

            # 检查元素是否可见
            try:
                is_visible = await locator.is_visible()
                if not is_visible:
                    logger.warning(f"元素存在但不可见: {action.target}")
                    # 不阻止执行，因为可以用 force 或 JS
            except:
                pass

            # 额外检查 input 动作需要 value
            if action.action == "input" and action.value is None:
                return False, "input 动作需要 value"

            return True, None

        return True, None

    async def _locate_element(
        self,
        target: str,
        elements: list[InteractiveElement],
    ):
        """定位元素

        定位策略（优先级从高到低）：
        1. CSS ID 选择器（如果 target 匹配某元素的 id）
        2. CSS name 选择器（如果 target 匹配某元素的 name）
        3. 精确匹配文本（忽略空格）
        4. 精确匹配 aria-label
        5. 精确匹配 title
        6. 精确匹配 placeholder
        7. 模糊匹配文本
        8. 模糊匹配 placeholder
        9. 按钮角色定位（适用于 button 元素）
        10. 索引定位（如果 target 是数字，不推荐）

        Args:
            target: 目标元素描述
            elements: 可交互元素列表

        Returns:
            Playwright Locator 或 None
        """
        logger.info(f"尝试定位元素: '{target}'")
        target_normalized = _normalize_text(target)

        # 检测数字索引并警告，自动转换为文本定位
        if target.strip().isdigit():
            logger.warning(f"⚠️ 检测到数字索引 '{target}'，这是不允许的！尝试转换为文本定位...")
            idx = int(target)
            if 0 <= idx < len(elements):
                el = elements[idx]
                # 优先使用文本，其次 placeholder，再次 aria_label
                actual_target = el.text or el.placeholder or el.aria_label or el.id
                if actual_target:
                    logger.info(f"转换为文本定位: '{actual_target}'")
                    target = actual_target
                    target_normalized = _normalize_text(target)

        # 1. CSS ID 选择器（最可靠）
        for el in elements:
            if el.id and _normalize_text(el.id) == target_normalized:
                logger.debug(f"ID 选择器: #{el.id}")
                return self.page.locator(f"#{el.id}")

        # 2. CSS name 选择器
        for el in elements:
            if el.name and _normalize_text(el.name) == target_normalized:
                logger.debug(f"name 选择器: [name='{el.name}']")
                return self.page.locator(f"[name='{el.name}']")

        # 3. 精确匹配文本（忽略空格）+ 区域消歧
        for el in elements:
            if el.text and _normalize_text(el.text) == target_normalized:
                logger.debug(f"精确匹配文本: {el.text}")
                locator = self.page.get_by_text(el.text, exact=True)

                # 检查是否匹配多个元素，如果是则用区域限定
                try:
                    count = await locator.count()
                    if count > 1:
                        if el.region:
                            region_sel = self.REGION_SELECTORS.get(el.region)
                            if region_sel:
                                logger.info(f"检测到多个匹配元素，使用区域限定: {el.region}")
                                region_locator = self.page.locator(region_sel).get_by_text(el.text, exact=True)
                                region_count = await region_locator.count()
                                if region_count == 1:
                                    return region_locator
                                elif region_count > 1:
                                    # 区域限定后仍多个，使用 .first
                                    logger.info(f"区域限定后仍有 {region_count} 个匹配，使用 .first")
                                    return region_locator.first
                        else:
                            # 无区域信息，直接使用 .first
                            logger.info(f"检测到 {count} 个匹配元素且无区域信息，使用 .first")
                            return locator.first
                except PlaywrightTimeoutError as e:
                    logger.debug(f"区域消歧检查超时: {e}")
                except Exception as e:
                    logger.warning(f"区域消歧检查失败: {e}")

                return locator

        # 3.5. 通过按钮角色定位（适用于 button 元素）
        for el in elements:
            if el.tag == "BUTTON" and el.text:
                # 尝试 get_by_role 定位
                if target_normalized in _normalize_text(el.text):
                    logger.debug(f"按钮角色定位: {el.text}")
                    return self.page.get_by_role("button", name=el.text)

        # 4. 精确匹配 aria-label
        for el in elements:
            if el.aria_label and _normalize_text(el.aria_label) == target_normalized:
                logger.debug(f"精确匹配 aria-label: {el.aria_label}")
                return self.page.locator(f'[aria-label="{el.aria_label}"]')

        # 5. 精确匹配 title
        for el in elements:
            if el.title and _normalize_text(el.title) == target_normalized:
                logger.debug(f"精确匹配 title: {el.title}")
                return self.page.locator(f'[title="{el.title}"]')

        # 6. 精确匹配 placeholder
        for el in elements:
            if el.placeholder and _normalize_text(el.placeholder) == target_normalized:
                logger.debug(f"精确匹配 placeholder: {el.placeholder}")
                return self.page.get_by_placeholder(el.placeholder, exact=True)

        # 7. 模糊匹配文本
        for el in elements:
            if el.text and target_normalized in _normalize_text(el.text):
                logger.debug(f"模糊匹配文本: {el.text}")
                return self.page.get_by_text(el.text)

        # 8. 模糊匹配 placeholder
        for el in elements:
            if el.placeholder and target_normalized in _normalize_text(el.placeholder):
                logger.debug(f"模糊匹配 placeholder: {el.placeholder}")
                return self.page.get_by_placeholder(el.placeholder)

        # 9. 索引定位
        if target.isdigit():
            idx = int(target)
            if 0 <= idx < len(elements):
                el = elements[idx]
                logger.debug(f"索引定位: [{idx}] {el.tag}")
                return self.page.locator(f"{el.tag.lower()}:visible >> nth={idx}")

        return None

    async def _fill_form(
        self,
        action: Action,
        elements: list[InteractiveElement],
    ) -> ActionResult:
        """执行复杂表单填写

        Args:
            action: 动作对象
            elements: 元素列表

        Returns:
            ActionResult: 执行结果
        """
        from backend.agent_simple.perception import Perception

        logger.info("使用 FormFiller 填写表单")

        if not self.llm:
            return ActionResult(
                success=False,
                error="Executor 未配置 LLM，无法使用 fill_form"
            )

        try:
            # 获取当前页面状态
            perception = Perception(self.page)
            screenshot_base64 = await perception.take_screenshot_base64()

            state = PageState(
                screenshot_base64=screenshot_base64,
                url=self.page.url,
                title=await self.page.title(),
                elements=elements,
            )

            # 使用 FormFiller
            filler = FormFiller(self.llm, self.page)
            result = await filler.fill_form(state, action.target or "填写表单")

            if result.success:
                logger.info("表单填写成功")
                return ActionResult(success=True, error=None)
            else:
                logger.error(f"表单填写失败: {result.error}")
                return ActionResult(success=False, error=result.error)

        except Exception as e:
            logger.error(f"表单填写异常: {e}")
            return ActionResult(success=False, error=str(e))
