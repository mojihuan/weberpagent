"""LLMHealer -- LLM-driven locator healing for Playwright automation.

When all locator chain attempts fail, LLMHealer calls the LLM
to analyze the page DOM and generate a repaired Playwright code snippet.

Per D-03: Uses create_llm() to get browser-use ChatOpenAI instance.
Per D-04: 90s asyncio.wait_for timeout.
Per D-07: Returns LLMHealResult frozen dataclass.
Per D-08: Extracts response via result.completion (NOT .content).
Per D-10: Validates with ast.parse() before accepting.
"""

import ast
import dataclasses
import json
import logging
import re

import asyncio

from backend.llm.factory import create_llm
from browser_use.llm.messages import SystemMessage, UserMessage

logger = logging.getLogger(__name__)

DOM_TRUNCATION_THRESHOLD = 15000
LLM_TIMEOUT_SECONDS = 90.0

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

# Self-healing runner 专用: 修复测试代码行
REPAIR_SYSTEM_PROMPT = (
    "你是 Playwright 自动化测试修复专家。\n"
    "用户会提供失败的测试代码上下文、错误信息和可选的 DOM 快照。\n"
    "你的任务：修复失败的那一行代码。\n\n"
    "规则：\n"
    "1. 只返回修复后的单行代码（必须保持原始缩进）\n"
    "2. 不要用 markdown 代码块包裹\n"
    "3. 不要添加解释说明\n"
    "4. 保持原始缩进（前导空格）完全不变\n"
    "5. 代码必须是合法 Python 语句\n"
    "6. 只修改出错的代码行，不要添加新行"
)

REPAIR_USER_TEMPLATE = (
    "失败行号: {line_number}\n"
    "失败行代码: {failing_line}\n\n"
    "测试代码上下文 (前后各 20 行):\n{code_context}\n\n"
    "错误信息:\n{error_message}\n\n"
    "{dom_section}"
)

# Self-healing runner 专用 V2: 结构化多行修复 prompt
REPAIR_SYSTEM_PROMPT_V2 = (
    "你是 Playwright 自动化测试修复专家。\n"
    "用户会提供失败的测试代码上下文、错误信息和可选的 DOM 快照。\n"
    "你的任务：找到失败代码，提供修复方案。\n\n"
    "规则：\n"
    '1. 返回 JSON 格式：{"target_snippet": "要替换的原始代码", "replacement": "新代码"}\n'
    "2. target_snippet 必须是原文中的精确片段 (至少 20 个字符)\n"
    "3. replacement 可以是多行代码 (如 try-except 块)\n"
    "4. 保持原始缩进完全不变\n"
    "5. 不要用 markdown 代码块包裹 JSON\n"
    "6. 只修改出错的代码区域，不要重写整个函数"
)

_CODE_CONTEXT_WINDOW = 20  # 失败行前后各取 20 行


@dataclasses.dataclass(frozen=True)
class LLMHealResult:
    """Immutable result from LLM healing attempt.

    Attributes:
        success: Whether the LLM produced valid Playwright code.
        code_snippet: The validated Playwright code (empty string on failure).
        raw_response: The raw LLM response text for debugging.
        locator: The extracted locator expression for logging.
        target_snippet: Original code to replace (structured repair, D-01).
        replacement: New code to insert (structured repair, D-01).
    """

    success: bool
    code_snippet: str
    raw_response: str
    locator: str
    target_snippet: str = ""   # D-01: original code to replace
    replacement: str = ""      # D-01: new code to insert


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


def _parse_repair_response(raw: str) -> tuple[str, str] | None:
    """Parse LLM repair response into (target_snippet, replacement).

    Tries JSON parse after stripping markdown fences.
    Falls back to None if response is not valid JSON or fields are too short.
    """
    cleaned = _strip_markdown_fences(raw)
    # Try direct JSON parse
    try:
        parsed = json.loads(cleaned)
        target = parsed.get("target_snippet", "")
        replacement = parsed.get("replacement", "")
        if len(target) >= 20 and replacement:
            return (target, replacement)
    except (json.JSONDecodeError, AttributeError):
        pass
    # Fallback: try to extract JSON from surrounding text
    json_match = re.search(
        r'\{[^{}]*"target_snippet"[^{}]*"replacement"[^{}]*\}',
        cleaned,
        re.DOTALL,
    )
    if json_match:
        try:
            parsed = json.loads(json_match.group(0))
            target = parsed.get("target_snippet", "")
            replacement = parsed.get("replacement", "")
            if len(target) >= 20 and replacement:
                return (target, replacement)
        except (json.JSONDecodeError, AttributeError):
            pass
    return None


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
            action_type: The type of action that failed (e.g. "click").
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

    async def repair_code(
        self,
        test_code: str,
        error_line: int | None,
        error_message: str,
        dom_snapshot: str = "",
    ) -> LLMHealResult:
        """Attempt LLM-based repair for a failing test code line.

        Unlike heal() which fixes a single locator, this method receives the
        full test code context and asks the LLM to return the fixed line
        with correct indentation preserved.

        Args:
            test_code: Full test file content.
            error_line: 1-indexed line number of the failure (None if unknown).
            error_message: Pytest error output (truncated internally).
            dom_snapshot: Optional DOM snapshot for context.

        Returns:
            LLMHealResult with success=True and fixed code line, or failure result.
        """
        # Extract failing line and context window
        lines = test_code.splitlines()
        if error_line is not None and 1 <= error_line <= len(lines):
            failing_line = lines[error_line - 1]
            start = max(0, error_line - 1 - _CODE_CONTEXT_WINDOW)
            end = min(len(lines), error_line - 1 + _CODE_CONTEXT_WINDOW + 1)
            code_context = "\n".join(
                f"{i + 1:>4}: {lines[i]}" for i in range(start, end)
            )
        else:
            failing_line = "(未知)"
            code_context = "\n".join(f"{i + 1:>4}: {l}" for i, l in enumerate(lines[:30]))

        dom_section = ""
        if dom_snapshot:
            dom_section = f"DOM 快照:\n{_truncate_dom(dom_snapshot)}"

        messages = [
            SystemMessage(content=REPAIR_SYSTEM_PROMPT_V2),
            UserMessage(
                content=REPAIR_USER_TEMPLATE.format(
                    line_number=error_line or "未知",
                    failing_line=failing_line,
                    code_context=code_context,
                    error_message=error_message[:1000],
                    dom_section=dom_section,
                ),
            ),
        ]

        try:
            result = await asyncio.wait_for(
                self._llm.ainvoke(messages),
                timeout=LLM_TIMEOUT_SECONDS,
            )
        except asyncio.TimeoutError:
            self._logger.warning("LLM repair timed out after %ss", LLM_TIMEOUT_SECONDS)
            return LLMHealResult(
                success=False, code_snippet="", raw_response="", locator="",
            )
        except Exception as exc:
            self._logger.warning("LLM repair failed: %s", exc)
            return LLMHealResult(
                success=False, code_snippet="", raw_response=str(exc), locator="",
            )

        response_text = result.completion.strip()
        if not response_text:
            return LLMHealResult(
                success=False, code_snippet="", raw_response="", locator="",
            )

        # Parse structured JSON response (target_snippet + replacement)
        parsed = _parse_repair_response(response_text)
        if parsed is None:
            self._logger.warning(
                "LLM repair returned non-JSON or invalid response: %s",
                response_text[:200],
            )
            return LLMHealResult(
                success=False,
                code_snippet="",
                raw_response=response_text,
                locator="",
            )

        target_snippet, replacement = parsed
        locator = _extract_locator(replacement)
        return LLMHealResult(
            success=True,
            code_snippet=replacement,  # backward compat
            raw_response=result.completion,
            locator=locator,
            target_snippet=target_snippet,
            replacement=replacement,
        )
