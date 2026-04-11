"""TestFlowService — login prefix injection and two-phase variable substitution.

Orchestrates login step injection and variable replacement for ERP test flows.
When a task has a login_role, this service:
1. Generates a 5-line login instruction prefix
2. Replaces {{cached:KEY}} with cache values via regex (phase 1)
3. Replaces {{variable}} with context values via Jinja2 (phase 2)
4. Shifts user step numbers by +5 to account for injected login steps
5. Concatenates login prefix + processed user description
"""

import logging
import re
from typing import Any

from jinja2 import Environment, StrictUndefined, UndefinedError

logger = logging.getLogger(__name__)

# Number of login steps injected before user steps.
LOGIN_STEP_COUNT = 5


def build_login_prefix(login_url: str, account: str, password: str) -> str:
    """Generate a 5-line login instruction prefix.

    Each line is a numbered step the AI agent will execute.

    Args:
        login_url: ERP login page URL.
        account: Login account/username.
        password: Login password.

    Returns:
        5-line string with login steps, each ending with newline.
    """
    lines = [
        f"1. 打开 {login_url}",
        f"2. 在账号输入框输入 {account}",
        f"3. 在密码输入框输入 {password}",
        "4. 点击登录按钮",
        "5. 确认登录成功（检测到用户信息或首页内容）",
    ]
    return "\n".join(lines) + "\n"


class TestFlowService:
    """Orchestrates login prefix injection and two-phase variable substitution.

    Phase 1 (regex): Replace {{cached:KEY}} with values from cache_values dict.
    Phase 2 (Jinja2): Replace {{variable}} with values from context dict.
    Order matters — Jinja2 StrictUndefined would crash on {{cached:xxx}} if
    reversed (per D-06).
    """

    # Regex pattern for {{cached:KEY}} — key is one or more word characters.
    _CACHED_PATTERN = re.compile(r"\{\{cached:(\w+)\}\}")

    # Regex pattern for step numbers like 步骤N： or 步骤N:
    _STEP_NUMBER_PATTERN = re.compile(r"步骤(\d+)[：:]")

    def _build_description(
        self,
        *,
        task_description: str,
        login_url: str,
        account: str,
        password: str,
        context: dict[str, Any],
        cache_values: dict[str, Any],
    ) -> str:
        """Build the full task description with login prefix and variable substitution.

        Args:
            task_description: Original user-provided task description with steps.
            login_url: ERP login page URL for prefix generation.
            account: Login account for prefix generation.
            password: Login password for prefix generation.
            context: Variable context for Jinja2 {{variable}} replacement.
            cache_values: Cached values for {{cached:KEY}} replacement.

        Returns:
            Complete description: login prefix + processed user steps.
        """
        # Step 1: Generate login prefix
        login_prefix = build_login_prefix(login_url, account, password)

        # Step 2: Regex phase — replace {{cached:KEY}} with cache values
        description = self._replace_cached_variables(task_description, cache_values)

        # Step 3: Jinja2 phase — replace {{variable}} with context values
        description = self._replace_context_variables(description, context)

        # Step 4: Shift user step numbers by +5
        description = self._shift_step_numbers(description, LOGIN_STEP_COUNT)

        # Step 5: Concatenate login prefix + processed description
        return login_prefix + description

    def _replace_cached_variables(
        self, text: str, cache_values: dict[str, Any]
    ) -> str:
        """Replace {{cached:KEY}} patterns with values from cache_values.

        Missing keys produce empty string replacement with a warning log
        (per D-05). No error is raised.

        Args:
            text: Text potentially containing {{cached:KEY}} patterns.
            cache_values: Dict of cached key-value pairs.

        Returns:
            Text with all {{cached:KEY}} patterns replaced.
        """

        def _replacer(match: re.Match) -> str:
            key = match.group(1)
            if key in cache_values:
                return str(cache_values[key])
            logger.warning("cache key '%s' not found, replacing with empty string", key)
            return ""

        return self._CACHED_PATTERN.sub(_replacer, text)

    def _replace_context_variables(
        self, text: str, context: dict[str, Any]
    ) -> str:
        """Replace {{variable}} patterns with values from context via Jinja2.

        Skips Jinja2 processing entirely if no {{ patterns remain after
        the regex phase. Uses StrictUndefined for safety, but catches
        UndefinedError gracefully (per D-06).

        Args:
            text: Text potentially containing {{variable}} patterns.
            context: Variable context dict for substitution.

        Returns:
            Text with {{variable}} patterns replaced.
        """
        if not text or "{{" not in text:
            return text

        env = Environment(
            variable_start_string="{{",
            variable_end_string="}}",
            undefined=StrictUndefined,
        )
        try:
            template = env.from_string(text)
            return template.render(**context)
        except UndefinedError as exc:
            logger.warning("Jinja2 undefined variable: %s", exc)
            return text

    @staticmethod
    def _shift_step_numbers(text: str, offset: int) -> str:
        """Shift Chinese step numbers by a fixed offset.

        Replaces patterns like 步骤1： or 步骤2: with 步骤{1+offset}： etc.

        Args:
            text: Text containing step number patterns.
            offset: Number to add to each step number.

        Returns:
            Text with shifted step numbers.
        """

        def _replacer(match: re.Match) -> str:
            original_num = int(match.group(1))
            new_num = original_num + offset
            separator = match.group(0)[-1]  # Preserve ： or :
            return f"步骤{new_num}{separator}"

        return re.sub(r"步骤(\d+)([：:])", _replacer, text)
