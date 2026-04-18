"""PlaywrightCodeGenerator -- 从翻译后的操作生成完整的 pytest Playwright 测试文件。

将 ActionTranslator 翻译的 TranslatedAction 列表组装为完整的 Python 测试文件。
输出结构 (per D-01/D-02):
- 元数据注释头部 (D-04)
- Import 语句
- def test_xxx(page: Page) -> None: 函数体
- 每个操作为一行 Playwright API 调用

Phase 84: 集成 LLMHealer，对弱步骤（elem=None 或 <=1 locator）进行 LLM 修复。
"""

import ast
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.core.action_translator import ActionTranslator, TranslatedAction
from backend.core.llm_healer import LLMHealer

logger = logging.getLogger(__name__)


class PlaywrightCodeGenerator:
    """生成完整的 pytest Playwright 测试文件。

    输出结构 (per D-01/D-02):
    - 元数据注释头部 (D-04)
    - Import 语句
    - def test_xxx(page: Page) -> None: 函数体
    - 每个操作为一行 Playwright API 调用
    """

    def __init__(self) -> None:
        self._translator = ActionTranslator()

    def generate(
        self,
        run_id: str,
        task_name: str,
        task_id: str,
        actions: list[TranslatedAction],
    ) -> str:
        """生成完整的测试文件内容。

        Args:
            run_id: 执行记录 ID
            task_name: 任务名称（用于函数名和注释）
            task_id: 任务 ID
            actions: 翻译后的操作列表

        Returns:
            完整的 Python 文件内容字符串。
        """
        header = self._build_header(run_id, task_name, task_id)
        func_name = self._sanitize_function_name(task_name)
        body = self._build_body(actions)
        needs_logging = self._needs_logging(actions)

        parts = [header, ""]
        parts.append("from playwright.sync_api import Page")

        # 条件 logging import (per D-08): 有回退定位器时添加
        if needs_logging:
            parts.append("import logging")
            parts.append("from backend.core.healer_error import HealerError")

        parts.append("")
        parts.append(f"def {func_name}(page: Page) -> None:")
        parts.append(f'    """Auto-generated test from agent execution: {task_name}"""')

        # 条件 healer logger 初始化 (per D-08)
        if needs_logging:
            parts.append('    _healer = logging.getLogger("healer")')

        if body:
            parts.append(body)

        return "\n".join(parts) + "\n"

    async def generate_and_save(
        self,
        run_id: str,
        task_name: str,
        task_id: str,
        agent_history: Any,
        base_dir: str = "outputs",
        llm_config: dict | None = None,
    ) -> str:
        """从 agent 执行历史生成代码文件并保存到磁盘。

        Args:
            agent_history: AgentHistoryList 对象，有 model_actions() 方法
            llm_config: 可选 LLM 配置，提供时启用 LLM 修复弱步骤

        Returns:
            生成文件的绝对路径。
        """
        raw_actions = agent_history.model_actions()

        # Phase 84: LLM healing for weak steps
        llm_snippets: dict[int, str] = {}
        if llm_config is not None:
            llm_snippets = await self._heal_weak_steps(
                raw_actions, run_id, base_dir, llm_config
            )

        # 翻译所有操作，有 LLM snippet 的步骤使用 translate_with_llm
        translated = [
            self._translator.translate_with_llm(a, llm_snippets.get(i, ""))
            for i, a in enumerate(raw_actions)
        ]
        content = self.generate(run_id, task_name, task_id, translated)

        output_dir = Path(base_dir) / run_id / "generated"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"test_{run_id}.py"
        output_path.write_text(content, encoding="utf-8")

        result_path = str(output_path)
        logger.info(f"[{run_id}] 生成 Playwright 代码: {result_path}")
        return result_path

    async def _heal_weak_steps(
        self,
        raw_actions: list[dict],
        run_id: str,
        base_dir: str,
        llm_config: dict,
    ) -> dict[int, str]:
        """识别弱步骤并调用 LLMHealer 修复。

        弱步骤条件 (per D-07): elem=None 或 <=1 locator。
        仅处理 click_element 和 input_text 操作。

        Args:
            raw_actions: model_actions() 返回的原始操作列表。
            run_id: 执行记录 ID，用于日志和 DOM 路径。
            base_dir: 输出基础目录，DOM snapshot 所在位置。
            llm_config: LLM 配置，用于创建 LLMHealer 实例。

        Returns:
            字典: action index -> LLM code snippet。
        """
        healer = LLMHealer(llm_config)
        llm_snippets: dict[int, str] = {}

        for i, action in enumerate(raw_actions):
            action_type = self._translator._identify_action_type(action)

            # 仅处理 click/input (per D-07)
            if action_type not in ("click_element", "input_text"):
                continue

            elem = action.get("interacted_element")

            # 判断是否需要 healing
            needs_healing = False
            failed_locators: tuple[str, ...] = ()

            if elem is None:
                needs_healing = True
            else:
                locators = self._translator._chain_builder.extract(elem, action_type)
                if len(locators) <= 1:
                    needs_healing = True
                    failed_locators = tuple(locators)

            if not needs_healing:
                continue

            # 读取 DOM snapshot (1-indexed per RESEARCH Pitfall 2)
            dom_path = Path(base_dir) / run_id / "dom" / f"step_{i + 1}.txt"
            if not dom_path.exists():
                logger.debug(
                    f"[{run_id}] Step {i + 1} DOM snapshot missing, skip healing"
                )
                continue

            dom_content = dom_path.read_text(encoding="utf-8")
            action_params = action.get(action_type, {})

            try:
                result = await healer.heal(
                    action_type, failed_locators, dom_content, action_params
                )
            except Exception as exc:
                logger.warning(
                    f"[{run_id}] Step {i + 1} LLM heal error: {exc}"
                )
                continue

            if result.success:
                llm_snippets[i] = result.code_snippet

            logger.info(
                f"[{run_id}] Step {i + 1} LLM 修复"
                f"{'成功' if result.success else '失败'}"
            )

        return llm_snippets

    @staticmethod
    def _needs_logging(actions: list[TranslatedAction]) -> bool:
        """检查操作列表中是否有需要 logging 的回退代码。"""
        return any(action.locators for action in actions)

    def _sanitize_function_name(self, task_name: str) -> str:
        """将任务名称转换为合法的 Python 函数名 (per D-03)。

        中文保留（Python 3 支持 Unicode 标识符），特殊字符替换为下划线。
        """
        if not task_name.strip():
            return "test_unnamed"

        sanitized = re.sub(r"[^a-zA-Z0-9_\u4e00-\u9fff]", "_", task_name)
        # 去除前导数字和下划线
        sanitized = re.sub(r"^[0-9_]+", "", sanitized)

        if not sanitized:
            return "test_unnamed"

        return f"test_{sanitized}"

    def _build_header(self, run_id: str, task_name: str, task_id: str) -> str:
        """构建元数据注释头部 (per D-04)。"""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return "\n".join([
            "# Generated by aiDriveUITest",
            f"# Task: {task_name}",
            f"# Run ID: {run_id}",
            f"# Task ID: {task_id}",
            f"# Generated: {timestamp}",
            "# Source: model_actions() from browser-use Agent",
        ])

    def _build_body(self, actions: list[TranslatedAction]) -> str:
        """构建测试函数体。"""
        if not actions:
            return ""

        lines: list[str] = []
        prev_type: str | None = None

        for action in actions:
            # 不同操作类型之间插入空行分隔
            if prev_type is not None and action.action_type != prev_type:
                lines.append("")
            lines.append(action.code)
            prev_type = action.action_type

        return "\n".join(lines)

    def validate_syntax(self, code: str) -> bool:
        """验证生成的代码是否为合法 Python。"""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
