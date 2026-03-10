"""循环控制模块 - 整合感知、决策、执行，实现带反思的执行循环"""

import json
import logging
from pathlib import Path
from datetime import datetime

from playwright.async_api import Page

from backend.llm.base import BaseLLM
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
    ):
        """初始化 Agent

        Args:
            task: 任务描述
            llm: LLM 实例（支持 vision）
            page: Playwright Page 对象
            output_dir: 输出目录（截图、日志等）
            max_steps: 最大执行步数
            max_retries: 单步最大重试次数
            timeout: 操作超时时间（毫秒）
        """
        self.task = task
        self.llm = llm
        self.page = page
        self.max_steps = max_steps
        self.max_retries = max_retries
        self.timeout = timeout

        # 初始化子模块
        self.perception = Perception(page)
        self.decision = Decision(llm)
        self.executor = Executor(page, timeout=timeout)

        # 输出目录
        self.output_dir = Path(output_dir)
        self.task_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.screenshot_manager = ScreenshotManager(output_dir, self.task_id)

        # 执行历史
        self.history: list[Step] = []

    def _detect_loop(self) -> bool:
        """检测是否陷入循环"""
        if len(self.history) < 4:
            return False

        recent = self.history[-4:]

        # 检测 1: 连续相同动作
        actions = [(s.action.action, s.action.target) for s in recent]
        if len(set(str(a) for a in actions)) <= 2:
            logger.warning("检测到循环：连续相同动作")
            return True

        # 检测 2: 页面状态无变化
        page_hashes = [s.state.state_hash for s in recent if s.state.state_hash]
        if len(page_hashes) >= 4 and len(set(page_hashes)) == 1:
            logger.warning("检测到循环：页面状态无变化")
            return True

        # 检测 3: 高失败率
        failed_count = sum(1 for s in recent if not s.result.success)
        if failed_count >= 3:
            logger.warning(f"检测到循环：高失败率 {failed_count}/4")
            return True

        return False

    async def _recover_from_loop(self) -> bool:
        """从循环中恢复"""
        logger.info("尝试从循环中恢复...")

        recovery_actions = [
            ("wait", "等待页面加载", lambda: self.page.wait_for_timeout(2000)),
            (
                "scroll_down",
                "滚动到页面底部",
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

    async def run(self) -> AgentResult:
        """执行任务

        Returns:
            AgentResult: 任务执行结果
        """
        logger.info(f"开始执行任务: {self.task}")
        logger.info(f"最大步数: {self.max_steps}, 最大重试: {self.max_retries}")

        for step_num in range(1, self.max_steps + 1):
            logger.info(f"\n{'='*50}")
            logger.info(f"Step {step_num}/{self.max_steps}")
            logger.info(f"{'='*50}")

            # 检测循环
            if self._detect_loop():
                recovered = await self._recover_from_loop()
                if not recovered:
                    logger.error("无法从循环中恢复")
                    # 继续执行，让 LLM 决定下一步

            # 1. 感知页面
            state = await self.perception.get_state()
            logger.info(f"页面: {state.title}")
            logger.info(f"URL: {state.url}")
            logger.info(f"元素数量: {len(state.elements)}")

            # 2. LLM 决策
            action = await self.decision.decide(self.task, state)

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

            # 保存截图（设置超时避免阻塞）
            screenshot_path = self.screenshot_manager.get_path(step_num, f"_retry{retry}" if retry > 0 else "")
            try:
                await self.page.screenshot(
                    path=screenshot_path,
                    timeout=10000,  # 10 秒超时
                    animations="disabled",  # 禁用动画加速截图
                )
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
            response = await self.llm.chat_with_vision(
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
