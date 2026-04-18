"""LLMHealer -- LLM-driven locator healing for Playwright automation.

When all locator chain attempts fail, LLMHealer calls the LLM (Qwen 3.5 Plus)
to analyze the page DOM and generate a repaired Playwright code snippet.

Per D-03: Uses create_llm() to get browser-use ChatOpenAI instance.
Per D-04: 30s asyncio.wait_for timeout.
Per D-07: Returns LLMHealResult frozen dataclass.
Per D-08: Extracts response via result.completion (NOT .content).
Per D-10: Validates with ast.parse() before accepting.
"""

import ast
import dataclasses
import logging
import re

import asyncio

from backend.llm.factory import create_llm
from browser_use.llm.messages import SystemMessage, UserMessage

logger = logging.getLogger(__name__)

DOM_TRUNCATION_THRESHOLD = 5000
LLM_TIMEOUT_SECONDS = 30.0

SYSTEM_PROMPT = (
    "你是 Playwright 自动化测试专家。"
    "用户会提供一个 DOM 快照和失败的操作信息。\n"
    "你的任务：根据 DOM 快照，生成一个 Playwright 代码行来定位并操作目标元素。\n\n"
    "规则：\n"
    "1. 只返回一个 Playwright API 调用"
    "（如 page.locator('...').click() 或 page.locator('...').fill('...')）\n"
    "2. 不要用 markdown 代码块包裹\n"
    "3. 不要添加解释说明\n"
    "4. 优先使用精确的定位器（CSS selector、text selector）\n"
    "5. 代码必须是合法 Python 表达式"
)

USER_PROMPT_TEMPLATE = (
    "操作类型: {action_type}\n"
    "失败的定位器: {failed_locators}\n"
    "操作参数: {action_params}\n"
    "DOM 快照:\n"
    "{dom_content}"
)


@dataclasses.dataclass(frozen=True)
class LLMHealResult:
    """Immutable result from LLM healing attempt.

    Attributes:
        success: Whether the LLM produced valid Playwright code.
        code_snippet: The validated Playwright code (empty string on failure).
        raw_response: The raw LLM response text for debugging.
        locator: The extracted locator expression for logging.
    """

    success: bool
    code_snippet: str
    raw_response: str
    locator: str


def _strip_markdown_fences(text: str) -> str:
    """Remove leading/trailing markdown code fences from LLM output.

    Handles patterns like:
        ```python\\ncode\\n```
        ```\\ncode\\n```
    """
    text = re.sub(r"^```(?:python)?\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)
    return text.strip()


def _extract_locator(code: str) -> str:
    """Extract the locator expression from a Playwright code line.

    Searches for page.locator(...) or page.get_by_xxx(...) patterns.
    Returns the full page.locator/get_by expression, or empty string.
    """
    match = re.search(r"page\.(locator|get_by_\w+)\([^)]*\)", code)
    if match:
        return match.group(0)
    return ""


def _truncate_dom(dom_snapshot: str) -> str:
    """Truncate DOM snapshot if it exceeds the threshold.

    Returns the original snapshot if within limit, otherwise truncates
    with a notice appended.
    """
    if len(dom_snapshot) <= DOM_TRUNCATION_THRESHOLD:
        return dom_snapshot
    return dom_snapshot[:DOM_TRUNCATION_THRESHOLD] + "\n... (DOM truncated)"


class LLMHealer:
    """LLM-based locator healer for Playwright automation.

    When the locator chain exhausts all fallback attempts, LLMHealer
    sends the page DOM and failure context to the LLM to generate
    a corrected Playwright code snippet.
    """

    def __init__(self, llm_config: dict) -> None:
        self._llm = create_llm(llm_config)
        self._logger = logging.getLogger(__name__)

    async def heal(
        self,
        action_type: str,
        failed_locators: tuple[str, ...],
        dom_snapshot: str,
        action_params: dict,
    ) -> LLMHealResult:
        """Attempt LLM-based healing for a failed locator.

        Args:
            action_type: The type of action that failed (e.g. "click_element").
            failed_locators: Tuple of locator expressions that were attempted.
            dom_snapshot: Current page DOM snapshot.
            action_params: Additional action parameters (e.g. input text).

        Returns:
            LLMHealResult with success=True and valid code, or failure result.
        """
        dom_content = _truncate_dom(dom_snapshot)

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            UserMessage(
                content=USER_PROMPT_TEMPLATE.format(
                    action_type=action_type,
                    failed_locators=list(failed_locators),
                    action_params=action_params,
                    dom_content=dom_content,
                ),
            ),
        ]

        try:
            result = await asyncio.wait_for(
                self._llm.ainvoke(messages),
                timeout=LLM_TIMEOUT_SECONDS,
            )
        except asyncio.TimeoutError:
            self._logger.warning(
                "LLM heal timed out after %ss for action_type=%s",
                LLM_TIMEOUT_SECONDS,
                action_type,
            )
            return LLMHealResult(
                success=False,
                code_snippet="",
                raw_response="",
                locator="",
            )
        except Exception as exc:
            self._logger.warning(
                "LLM heal failed for action_type=%s: %s",
                action_type,
                exc,
            )
            return LLMHealResult(
                success=False,
                code_snippet="",
                raw_response=str(exc),
                locator="",
            )

        response_text = result.completion.strip()

        if not response_text:
            self._logger.warning(
                "LLM returned empty response for action_type=%s",
                action_type,
            )
            return LLMHealResult(
                success=False,
                code_snippet="",
                raw_response="",
                locator="",
            )

        cleaned_code = _strip_markdown_fences(response_text)

        # Validate syntax with ast.parse
        try:
            ast.parse(cleaned_code)
        except SyntaxError:
            self._logger.warning(
                "LLM returned invalid syntax for action_type=%s: %s",
                action_type,
                response_text,
            )
            return LLMHealResult(
                success=False,
                code_snippet="",
                raw_response=response_text,
                locator="",
            )

        locator = _extract_locator(cleaned_code)

        return LLMHealResult(
            success=True,
            code_snippet=cleaned_code,
            raw_response=result.completion,
            locator=locator,
        )
