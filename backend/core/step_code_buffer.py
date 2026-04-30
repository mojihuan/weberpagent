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
        """同步翻译 action_dict 并存储为 StepRecord。"""
        # 同步翻译操作
        translated = self._translator.translate(action_dict)

        # evaluate 智能转换: 检测 JS 设置 input 值并转换为 .fill()
        converted = self._try_convert_evaluate_to_fill(action_dict, translated)
        if converted is not None:
            translated = converted

        # 推导等待策略
        action_type = ActionTranslator._identify_action_type(action_dict)
        if converted is not None:
            action_type = "input"
        wait_code = self._derive_wait(action_type, duration, action_dict)

        # 创建 StepRecord 并追加
        record = StepRecord(
            action=translated,
            wait_before=wait_code,
            step_index=self._next_index,
        )
        self._records.append(record)
        self._next_index += 1

    def _derive_wait(
        self,
        action_type: str,
        duration: float | None = None,
        action_dict: dict | None = None,
    ) -> str:
        """根据操作类型和耗时推导等待策略。

        四种策略（优先级从高到低）：
        1. navigate → wait_for_load_state("networkidle")
        2. duration > 0.8s → wait_for_timeout(实际耗时ms)
        3. click/input on popup → wait_for_timeout(500) (弹窗元素需更长时间)
        4. click → wait_for_timeout(300)
        5. 其他 → 无等待

        Args:
            action_type: 操作类型（click, input, navigate 等）。
            duration: 步骤实际执行耗时（秒）。
            action_dict: 操作字典，用于提取 interacted_element 信息。

        Returns:
            等待代码字符串，可能为空字符串表示无需等待。
        """
        # navigate 优先级最高，无论 duration 如何都返回 wait_for_load_state
        if action_type == "navigate":
            return '    page.wait_for_load_state("networkidle")'

        # 耗时 > 800ms 的操作返回实际耗时等待
        if duration is not None and duration > 0.8:
            return f"    page.wait_for_timeout({int(duration * 1000)})"

        # 弹窗/下拉选项元素需要更长等待
        if action_type in ("click", "input") and self._is_popup_element(action_dict):
            return "    page.wait_for_timeout(500)"

        # click 操作默认等待 300ms
        if action_type == "click":
            return "    page.wait_for_timeout(300)"

        # 其他操作无需额外等待
        return ""

    @staticmethod
    def _is_popup_element(action_dict: dict | None) -> bool:
        """检测操作目标是否为弹出/下拉元素。

        弹出元素通常被渲染在 body 下的高层级 div 中（如 div[4], div[5]），
        而不是在页面主布局 (div[1]/div[2]) 内。

        Args:
            action_dict: 操作字典。

        Returns:
            True 如果目标是弹窗/下拉元素。
        """
        if not action_dict:
            return False
        elem = action_dict.get("interacted_element")
        if elem is None:
            return False
        x_path = getattr(elem, "x_path", "")
        if not x_path:
            return False
        # 检测 body 下高层级 div（弹窗 portal 通常在 div[3]+）
        # html/body/div[N] 中 N >= 3 视为弹窗
        import re
        popup_match = re.match(r"html/body/div\[(\d+)\]", x_path)
        if popup_match:
            div_index = int(popup_match.group(1))
            return div_index >= 3
        return False

    @staticmethod
    def _extract_fill_value_from_js(code: str) -> str | None:
        """从 evaluate 的 JS 代码中提取 input 填入的文本值。

        检测两种常见模式:
        1. nativeInputValueSetter: setter.call(element, "value")
        2. 直接赋值: element.value = "value" 或 element.value = 'value'

        Args:
            code: evaluate action 的 JavaScript 代码字符串。

        Returns:
            提取到的文本值，或 None。
        """
        import re

        # 模式 1: setter.call(inp, "xxx123") 或 setter.call(inp, 'xxx123')
        setter_match = re.search(
            r'setter\.call\([^,]+,\s*"((?:[^"\\]|\\.)*)"\)', code
        ) or re.search(
            r"setter\.call\([^,]+,\s*'((?:[^'\\]|\\.)*)'", code
        )
        if setter_match:
            return setter_match.group(1).replace('\\"', '"').replace("\\'", "'")

        # 模式 2: .value = "xxx" 或 .value = 'xxx'
        value_match = re.search(
            r'\.value\s*=\s*"((?:[^"\\]|\\.)*)"', code
        ) or re.search(
            r"\.value\s*=\s*'((?:[^'\\]|\\.)*)'", code
        )
        if value_match:
            return value_match.group(1).replace('\\"', '"').replace("\\'", "'")

        return None

    def _try_convert_evaluate_to_fill(
        self, action_dict: dict, translated: TranslatedAction,
    ) -> TranslatedAction | None:
        """尝试将 evaluate 设置 input 值的操作转换为 .fill() 代码。

        检测 evaluate action 是否在设置 input 元素的值，如果是则复用
        前一步 click 操作的定位器生成 .fill(value) 代码。

        Args:
            action_dict: 原始操作字典。
            translated: 翻译后的 TranslatedAction。

        Returns:
            转换后的 TranslatedAction，或 None（无法转换时保留原始 evaluate）。
        """
        # 仅处理 evaluate 类型
        action_type = ActionTranslator._identify_action_type(action_dict)
        if action_type != "evaluate":
            return None

        # 从 JS 代码中提取填入值
        params = action_dict.get("evaluate", {})
        js_code = params.get("code", "")
        if not js_code:
            return None

        fill_value = self._extract_fill_value_from_js(js_code)
        if fill_value is None:
            return None

        # 从前一步 click 复用定位器
        if not self._records:
            return None

        prev_record = self._records[-1]
        if prev_record.action.action_type != "click":
            return None

        # 复用前一步的定位器链
        prev_locators = prev_record.action.locators
        if not prev_locators:
            return None

        escaped_value = fill_value.replace("\\", "\\\\").replace('"', '\\"')
        action_suffix = f'.fill("{escaped_value}", timeout=5000)'

        # 用 ActionTranslator 的回退代码生成器
        code = self._translator._build_fallback_code(
            list(prev_locators), action_suffix, "input"
        )

        return TranslatedAction(
            code=code,
            action_type="input",
            is_comment=False,
            has_locator=True,
            locators=prev_locators,
        )

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

            # click 操作后插入页面稳定性检查
            # 菜单/链接点击可能触发页面跳转，需等待新页面加载
            if record.action.action_type == "click":
                stability_action = TranslatedAction(
                    code=(
                        "    try:\n"
                        "        page.wait_for_load_state(\"networkidle\", timeout=1000)\n"
                        "    except Exception:\n"
                        "        pass  # 非导航点击，无需等待"
                    ),
                    action_type="wait",
                    is_comment=False,
                    has_locator=False,
                )
                flat_actions.append(stability_action)

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
