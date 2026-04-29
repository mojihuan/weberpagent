"""StepCodeBuffer -- 逐步累积翻译结果，组装完整 Playwright 测试文件。

在 step_callback 中即时翻译每步操作，累积 StepRecord，最终组装完整测试文件。
替代旧的 generate_and_save 事后批量翻译模式。

Plan 01: 同步翻译核心 (CODEGEN-01, CODEGEN-03, CODEGEN-04)。
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from backend.core.action_translator import ActionTranslator, TranslatedAction
from backend.core.code_generator import PlaywrightCodeGenerator

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class StepRecord:
    """单个步骤的翻译结果记录（不可变）。

    Attributes:
        action: 翻译后的 Playwright 操作。
        wait_before: 操作前的等待代码（可能为空字符串）。
        step_index: 步骤序号，从 0 开始。
    """

    action: TranslatedAction
    wait_before: str = ""
    step_index: int = 0


class StepCodeBuffer:
    """逐步累积翻译结果，组装完整 Playwright 测试文件。

    使用流程:
    1. 创建 StepCodeBuffer 实例
    2. 每步操作后调用 append_step(action_dict) 同步翻译
    3. 所有步骤完成后调用 assemble() 组装完整测试文件
    """

    def __init__(
        self,
        *,
        base_dir: str = "",
        run_id: str = "",
        llm_config: dict | None = None,
    ) -> None:
        self._records: list[StepRecord] = []
        self._next_index: int = 0
        self._translator = ActionTranslator()
        self._generator = PlaywrightCodeGenerator()
        self._base_dir = base_dir
        self._run_id = run_id
        self._llm_config = llm_config or {}

    def append_step(self, action_dict: dict, duration: float | None = None) -> None:
        """同步翻译 action_dict 并存储为 StepRecord。

        通过 ActionTranslator.translate() 同步翻译，然后根据操作类型和耗时
        推导等待策略，创建 StepRecord 追加到内部列表。

        Args:
            action_dict: model_actions() 返回的单步操作字典。
            duration: 该步骤的实际执行耗时（秒），用于推导等待策略。
        """
        # 同步翻译操作
        translated = self._translator.translate(action_dict)

        # 推导等待策略
        action_type = ActionTranslator._identify_action_type(action_dict)
        wait_code = self._derive_wait(action_type, duration)

        # 创建 StepRecord 并追加
        record = StepRecord(
            action=translated,
            wait_before=wait_code,
            step_index=self._next_index,
        )
        self._records.append(record)
        self._next_index += 1

    def _derive_wait(self, action_type: str, duration: float | None = None) -> str:
        """根据操作类型和耗时推导等待策略。

        三种策略（优先级从高到低）：
        1. navigate → wait_for_load_state("networkidle")
        2. duration > 0.8s → wait_for_timeout(实际耗时ms)
        3. click → wait_for_timeout(300)
        4. 其他 → 无等待

        Args:
            action_type: 操作类型（click, input, navigate 等）。
            duration: 步骤实际执行耗时（秒）。

        Returns:
            等待代码字符串，可能为空字符串表示无需等待。
        """
        # navigate 优先级最高，无论 duration 如何都返回 wait_for_load_state
        if action_type == "navigate":
            return '    page.wait_for_load_state("networkidle")'

        # 耗时 > 800ms 的操作返回实际耗时等待
        if duration is not None and duration > 0.8:
            return f"    page.wait_for_timeout({int(duration * 1000)})"

        # click 操作默认等待 300ms
        if action_type == "click":
            return "    page.wait_for_timeout(300)"

        # 其他操作无需额外等待
        return ""

    def assemble(
        self,
        run_id: str,
        task_name: str,
        task_id: str,
        precondition_config: dict | None = None,
        assertions_config: list[dict] | None = None,
    ) -> str:
        """将 StepRecord 展平为 TranslatedAction 列表，委托 PlaywrightCodeGenerator 组装。

        遍历 self._records，将每个 StepRecord 展平为 TranslatedAction 序列：
        - 如果 wait_before 非空，创建一个 wait TranslatedAction 插入到主操作之前
        - 然后追加主操作的 TranslatedAction

        最后调用 PlaywrightCodeGenerator.generate() 组装完整测试文件。

        Args:
            run_id: 执行记录 ID。
            task_name: 任务名称。
            task_id: 任务 ID。
            precondition_config: 前置条件配置（可选）。
            assertions_config: 断言配置列表（可选）。

        Returns:
            完整的 Python 测试文件内容字符串。
        """
        # 展平 StepRecord 为 TranslatedAction 列表
        flat_actions: list[TranslatedAction] = []
        for record in self._records:
            # 如果有等待代码，插入一个 wait TranslatedAction
            if record.wait_before:
                wait_action = TranslatedAction(
                    code=record.wait_before,
                    action_type="wait",
                    is_comment=False,
                    has_locator=False,
                )
                flat_actions.append(wait_action)
            # 追加主操作
            flat_actions.append(record.action)

        # 委托 PlaywrightCodeGenerator 组装
        return self._generator.generate(
            run_id,
            task_name,
            task_id,
            flat_actions,
            precondition_config=precondition_config,
            assertions_config=assertions_config,
        )

    @property
    def records(self) -> list[StepRecord]:
        """返回 StepRecord 列表的副本，保持不可变性。"""
        return list(self._records)
