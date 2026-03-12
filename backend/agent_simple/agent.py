"""循环控制模块 - 整合感知、决策、执行，实现带反思的执行循环"""

import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime

from playwright.async_api import Page

from backend.llm.base import BaseLLM
from backend.llm.factory import LLMFactory
from backend.agent_simple.types import (
    Action,
    ActionResult,
    PageState,
    AgentResult,
    Step,
    Reflection,
    ReflectionStrategy,
)
from backend.agent_simple.perception import Perception
from backend.agent_simple.decision import Decision
from backend.agent_simple.executor import Executor
from backend.agent_simple.memory import Memory
from backend.agent_simple.prompts import (
    SYSTEM_PROMPT,
    REFLECTION_PROMPT,
    format_elements_for_prompt,
)
from backend.utils.screenshot import ScreenshotManager

logger = logging.getLogger(__name__)


class SimpleAgent:
    """自研简化版 Agent

    整合感知、决策、执行模块，实现带反思的执行循环
    """

    def __init__(
        self,
        task: str,
        llm: BaseLLM,
        page: Page,
        output_dir: str = "outputs",
        max_steps: int = 20,
        max_retries: int = 3,
        timeout: int = 60000,
        reflect_llm: BaseLLM | None = None,
    ):
        """初始化 Agent

        Args:
            task: 任务描述
            llm: LLM 实例（用于决策）
            page: Playwright Page 对象
            output_dir: 输出目录（截图、日志等）
            max_steps: 最大执行步数
            max_retries: 单步最大重试次数
            timeout: 操作超时时间（毫秒）
            reflect_llm: 反思专用 LLM（可选，默认从工厂获取）
        """
        self.task = task
        self.llm = llm
        self.page = page
        self.max_steps = max_steps
        self.max_retries = max_retries
        self.timeout = timeout

        # 反思专用 LLM
        self.reflect_llm = reflect_llm or LLMFactory.get_reflect_llm()

        # 初始化子模块
        self.perception = Perception(page)
        self.decision = Decision(llm)
        self.executor = Executor(page, llm=llm, timeout=timeout)

        # 输出目录
        self.output_dir = Path(output_dir)
        self.task_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.screenshot_manager = ScreenshotManager(output_dir, self.task_id)

        # 执行历史
        self.history: list[Step] = []

        # 记忆模块
        self.memory = Memory(max_steps=5)

        # 循环检测状态
        self._last_loop_type: str | None = None

    def _detect_loop(self) -> tuple[bool, str | None]:
        """检测是否陷入循环

        Returns:
            (is_loop, loop_type): 是否陷入循环，以及循环类型描述
        """
        if len(self.history) < 4:
            return False, None

        recent = self.history[-4:]

        # 检测 1: 连续相同动作
        actions = [(s.action.action, s.action.target) for s in recent]
        unique_actions = len(set(str(a) for a in actions))
        if unique_actions <= 2:
            loop_type = f"连续执行相同动作: {actions[0][0]} -> {actions[0][1]}"
            logger.warning(f"检测到循环：{loop_type}")
            return True, loop_type

        # 检测 2: 页面状态无变化
        page_hashes = [s.state.state_hash for s in recent if s.state.state_hash]
        if len(page_hashes) >= 4 and len(set(page_hashes)) == 1:
            loop_type = "页面状态连续 4 步无变化"
            logger.warning(f"检测到循环：{loop_type}")
            return True, loop_type

        # 检测 3: 高失败率
        failed_count = sum(1 for s in recent if not s.result.success)
        if failed_count >= 3:
            loop_type = f"连续 4 步中 {failed_count} 步失败"
            logger.warning(f"检测到循环：{loop_type}")
            return True, loop_type

        return False, None

    async def _recover_from_loop(self, loop_type: str | None = None) -> bool:
        """从循环中恢复

        Args:
            loop_type: 循环类型描述，用于智能选择恢复策略
        """
        logger.info(f"尝试从循环中恢复... (循环类型: {loop_type})")

        # 根据循环类型选择不同的恢复策略
        if loop_type and "相同动作" in loop_type:
            # 连续相同动作：尝试滚动或等待，让页面状态发生变化
            recovery_actions = [
                (
                    "scroll_down",
                    "滚动到页面底部寻找新元素",
                    lambda: self.page.evaluate(
                        "window.scrollTo(0, document.body.scrollHeight)"
                    ),
                ),
                (
                    "scroll_up",
                    "滚动回页面顶部",
                    lambda: self.page.evaluate("window.scrollTo(0, 0)"),
                ),
                ("wait", "等待页面加载", lambda: self.page.wait_for_timeout(2000)),
            ]
        elif loop_type and "失败" in loop_type:
            # 高失败率：可能是元素定位问题，尝试滚动
            recovery_actions = [
                (
                    "scroll_down",
                    "滚动查找元素",
                    lambda: self.page.evaluate(
                        "window.scrollTo(0, document.body.scrollHeight)"
                    ),
                ),
                (
                    "scroll_up",
                    "滚动到页面顶部",
                    lambda: self.page.evaluate("window.scrollTo(0, 0)"),
                ),
            ]
        else:
            # 默认恢复策略
            recovery_actions = [
                ("wait", "等待页面加载", lambda: self.page.wait_for_timeout(2000)),
                (
                    "scroll_down",
                    "滚动到页面底部",
                    lambda: self.page.evaluate(
                        "window.scrollTo(0, document.body.scrollHeight)"
                    ),
                ),
            ]

        for action_name, description, action_func in recovery_actions:
            try:
                logger.info(f"尝试恢复动作: {description}")
                await action_func()
                await self.page.wait_for_timeout(500)
                return True
            except Exception as e:
                logger.warning(f"恢复动作失败 {action_name}: {e}")
                continue

        return False

    def _build_history_context(self) -> str:
        """构建历史记忆上下文"""
        if not self.history:
            return "（这是第一步）"

        parts = []

        # 如果检测到循环，添加明确的警告
        if self._last_loop_type:
            parts.append("⚠️ 循环警告：检测到 " + self._last_loop_type)
            parts.append("请换一种策略，不要重复之前的动作！\n")

        # 最近 3 步的摘要
        recent = self.history[-3:] if len(self.history) >= 3 else self.history
        for step in recent:
            status = "✅" if step.result.success else "❌"
            target = step.action.target or ""
            value = step.action.value or ""
            action_desc = f"{step.action.action}"
            if target:
                action_desc += f" -> {target}"
            if value:
                action_desc += f" = {value}"

            parts.append(f"Step {step.step_num}: {action_desc} {status}")

        # 失败模式检测
        failed_actions = [s for s in self.history if not s.result.success]
        if failed_actions:
            parts.append("\n⚠️ 已失败的动作（请避免重复）：")
            for f in failed_actions[-2:]:
                parts.append(f"  - {f.action.action} -> {f.action.target}")

        return "\n".join(parts)

    async def _setup_font_blocker(self):
        """设置字体拦截器，解决截图等待字体超时问题

        方案1: 使用 route 拦截字体网络请求
        方案2: 在页面加载后注入脚本，替换 FontFace

        两种方案结合使用，确保字体不会阻塞截图。
        """
        # 方案1: route 拦截字体请求
        async def block_font_requests(route):
            if route.request.resource_type == "font":
                logger.debug(f"🚫 拦截字体请求: {route.request.url[:50]}")
                await route.abort()
            else:
                await route.continue_()

        await self.page.route("**", block_font_requests)

        # 方案2: 在当前页面注入 FontFace 替换脚本
        await self.page.evaluate("""
            () => {
                // 如果已经设置过，跳过
                if (window.__fontBlockerSet) return;
                window.__fontBlockerSet = true;

                // 保存原始 FontFace
                const OriginalFontFace = window.FontFace;

                // 替换 FontFace 构造函数
                window.FontFace = function(family, source, descriptors) {
                    console.log('🚫 FontFace 拦截:', family);

                    // 创建一个使用本地字体的 FontFace
                    const fontFace = new OriginalFontFace(
                        family,
                        'local("Arial")',
                        descriptors || {}
                    );

                    // 立即设置为已加载状态
                    Object.defineProperty(fontFace, 'status', {
                        get: () => 'loaded',
                        configurable: true
                    });

                    // 让 load() 立即返回
                    fontFace.load = () => Promise.resolve(fontFace);

                    return fontFace;
                };

                // 复制静态属性
                Object.setPrototypeOf(window.FontFace, OriginalFontFace);

                console.log('✅ FontFace 拦截器已启用');
            }
        """)

        logger.info("🔧 字体拦截器已启用 (route + evaluate)")

    async def run(self) -> AgentResult:
        """执行任务

        Returns:
            AgentResult: 任务执行结果
        """
        # 设置字体拦截器（避免截图等待字体加载）
        await self._setup_font_blocker()

        logger.info(f"开始执行任务: {self.task}")
        logger.info(f"最大步数: {self.max_steps}, 最大重试: {self.max_retries}")

        for step_num in range(1, self.max_steps + 1):
            logger.info(f"\n{'='*50}")
            logger.info(f"Step {step_num}/{self.max_steps}")
            logger.info(f"{'='*50}")

            # 检测循环
            is_loop, loop_type = self._detect_loop()
            if is_loop:
                recovered = await self._recover_from_loop(loop_type)
                if not recovered:
                    logger.error("无法从循环中恢复")
                    # 继续执行，让 LLM 决定下一步
                # 记录循环警告，用于构建上下文
                self._last_loop_type = loop_type

            # 1. 感知页面
            state = await self.perception.get_state()
            logger.info(f"页面: {state.title}")
            logger.info(f"URL: {state.url}")
            logger.info(f"元素数量: {len(state.elements)}")

            # 2. LLM 决策（传入记忆）
            action = await self.decision.decide(self.task, state, self.memory)

            # 3. 执行动作（带反思重试）
            result = await self._execute_with_reflection(action, state, step_num)

            # 4. 记录历史
            step = Step(
                step_num=step_num,
                state=state,
                action=action,
                result=result,
            )
            self.history.append(step)
            self.memory.add_step(step)  # 同时更新记忆

            # 5. 检查任务完成
            if action.done:
                logger.info(f"\n任务完成: {action.result}")
                return AgentResult(
                    success=True,
                    result=action.result,
                    steps=self.history,
                )

            # 6. 检查执行失败
            if not result.success:
                logger.warning(f"步骤 {step_num} 执行失败: {result.error}")
                # 继续执行，让 LLM 决定下一步

        # 超过最大步数
        logger.error(f"超过最大步数 {self.max_steps}")
        return AgentResult(
            success=False,
            error=f"超过最大步数 {self.max_steps}",
            steps=self.history,
        )

    async def _execute_with_reflection(
        self,
        action: Action,
        state: PageState,
        step_num: int,
    ) -> ActionResult:
        """带反思的执行

        执行动作，如果失败则进行反思并尝试修复

        Args:
            action: 要执行的动作
            state: 当前页面状态
            step_num: 步骤编号

        Returns:
            ActionResult: 执行结果
        """
        current_action = action

        for retry in range(self.max_retries):
            # 执行动作
            result = await self.executor.execute(current_action, state.elements)

            # 保存截图（使用 CDP 绕过字体等待）
            screenshot_path = self.screenshot_manager.get_path(step_num, f"_retry{retry}" if retry > 0 else "", ext="jpg")
            try:
                # 使用 CDP 截图，不等待字体加载
                # 使用 JPEG 格式 + 质量 60，极致压缩体积
                cdp = await self.page.context.new_cdp_session(self.page)
                result_cdp = await cdp.send("Page.captureScreenshot", {
                    "format": "jpeg",
                    "quality": 60,
                    "captureBeyondViewport": False,
                })
                await cdp.detach()

                # 保存到文件
                import base64
                screenshot_bytes = base64.b64decode(result_cdp["data"])
                Path(screenshot_path).write_bytes(screenshot_bytes)
                result.screenshot_path = screenshot_path
            except Exception as e:
                logger.warning(f"截图保存失败: {e}，跳过截图")
                result.screenshot_path = None

            if result.success:
                logger.info(f"动作执行成功")
                return result

            logger.warning(f"动作执行失败 (重试 {retry + 1}/{self.max_retries}): {result.error}")

            # 如果是 done 动作失败，直接返回
            if current_action.action == "done":
                return result

            # 反思分析
            reflection = await self._reflect(current_action, result, state)

            if reflection.strategy == ReflectionStrategy.SKIP:
                logger.info(f"反思策略: SKIP - 跳过当前步骤")
                return ActionResult(
                    success=False,
                    error=f"跳过: {reflection.reason}",
                )

            elif reflection.strategy == ReflectionStrategy.ALTERNATIVE:
                logger.info(f"反思策略: ALTERNATIVE - {reflection.reason}")
                if reflection.adjusted_action:
                    current_action = reflection.adjusted_action
                    logger.info(f"调整后的动作: {current_action.action}, 目标: {current_action.target}")
                continue

            elif reflection.strategy == ReflectionStrategy.RETRY:
                logger.info(f"反思策略: RETRY - {reflection.reason}")
                # 原样重试
                continue

            elif reflection.strategy == ReflectionStrategy.ROLLBACK:
                logger.info(f"反思策略: ROLLBACK - {reflection.reason}")
                # Navigate back to previous page
                try:
                    await self.page.go_back()
                    await self.page.wait_for_load_state("networkidle")
                    logger.info("已回退到上一页")
                    return ActionResult(
                        success=True,
                        error=f"回退: {reflection.reason}",
                    )
                except Exception as e:
                    logger.warning(f"回退失败: {e}")
                    continue

        # 重试次数耗尽
        return ActionResult(
            success=False,
            error=f"重试 {self.max_retries} 次后仍然失败",
        )

    async def _reflect(
        self,
        action: Action,
        result: ActionResult,
        state: PageState,
    ) -> Reflection:
        """反思失败原因并生成修复策略

        Args:
            action: 失败的动作
            result: 执行结果
            state: 页面状态

        Returns:
            Reflection: 反思结果
        """
        # 构建反思 prompt
        elements_text = format_elements_for_prompt(state.elements[:10])
        history_context = self._build_history_context()

        prompt = REFLECTION_PROMPT.format(
            task=self.task,
            history=history_context,
            thought=action.thought,
            action=action.action,
            target=action.target or "无",
            value=action.value or "无",
            error=result.error or "未知错误",
            url=state.url,
            title=state.title,
            elements=elements_text,
        )

        # 调用 LLM 进行反思
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        try:
            # 使用 reflect_llm 而不是 self.llm
            response = await self.reflect_llm.chat_with_vision(
                messages=messages,
                images=[f"data:image/png;base64,{state.screenshot_base64}"],
            )

            # 解析反思结果
            return self._parse_reflection(response.content)

        except Exception as e:
            logger.error(f"反思失败: {e}")
            # 默认重试策略
            return Reflection(
                reason=f"反思调用失败: {e}",
                strategy=ReflectionStrategy.RETRY,
            )

    def _parse_reflection(self, response: str) -> Reflection:
        """解析 LLM 反思输出

        Args:
            response: LLM 原始输出

        Returns:
            Reflection: 解析后的反思结果
        """
        # 尝试提取 JSON
        json_start = response.find("{")
        json_end = response.rfind("}") + 1

        if json_start >= 0 and json_end > json_start:
            try:
                data = json.loads(response[json_start:json_end])

                # 解析策略
                strategy_str = data.get("strategy", "retry").lower()
                strategy = ReflectionStrategy.RETRY
                if strategy_str == "alternative":
                    strategy = ReflectionStrategy.ALTERNATIVE
                elif strategy_str == "skip":
                    strategy = ReflectionStrategy.SKIP
                elif strategy_str == "rollback":
                    strategy = ReflectionStrategy.ROLLBACK

                # 解析调整后的动作
                adjusted_action = None
                if strategy == ReflectionStrategy.ALTERNATIVE and "adjusted_action" in data:
                    adj = data["adjusted_action"]
                    adjusted_action = Action(
                        thought=adj.get("thought", ""),
                        action=adj.get("action", "wait"),
                        target=adj.get("target"),
                        value=adj.get("value"),
                        done=adj.get("done", False),
                    )

                return Reflection(
                    reason=data.get("reason", "未提供原因"),
                    strategy=strategy,
                    adjusted_action=adjusted_action,
                )

            except json.JSONDecodeError as e:
                logger.warning(f"反思 JSON 解析失败: {e}")

        # 解析失败，默认重试
        return Reflection(
            reason="无法解析反思输出",
            strategy=ReflectionStrategy.RETRY,
        )
