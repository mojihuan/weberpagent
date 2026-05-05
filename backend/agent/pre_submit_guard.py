"""PreSubmitGuard -- validates form fields before submit clicks.

Extracts expected values (sales amount, logistics fee, amount, payment status)
from the task description using regex. Currently only extracts expectations;
comparison against actual page values is deferred until actual_values are
provided by the caller. Returns frozen GuardResult dataclass (immutable)
per project coding conventions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


EXPECTATION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"销售金额[：:]*\s*(\d+(?:\.\d+)?)\s*元?"), "销售金额"),
    (re.compile(r"物流费用[：:]*\s*(\d+(?:\.\d+)?)\s*元?"), "物流费用"),
    (re.compile(r"金额[：:]*\s*(\d+(?:\.\d+)?)\s*元?"), "金额"),
    (re.compile(r"付款状态[：:]*\s*(已付款|未付款|部分付款|待付款)"), "付款状态"),
]

SUBMIT_KEYWORDS: set[str] = {
    "确认",
    "提交",
    "保存",
    "确定",
    "submit",
    "confirm",
    "save",
    "ok",
}


@dataclass(frozen=True)
class GuardResult:
    """Immutable result from PreSubmitGuard.check()."""

    should_block: bool
    message: str


@dataclass
class PreSubmitGuard:
    """Validates form fields before submit clicks.

    - Extracts expected values from task description via regex (MON-04).
    - Comparison against actual page values deferred until actual_values
      are provided by the caller (currently always None).
    - Skips blocking when no expectations can be extracted (MON-06).
    """

    def check(
        self,
        action_name: str,
        target_index: int | None,
        task: str,
        actual_values: dict[str, str] | None,
        submit_button_text: str | None = None,
    ) -> GuardResult:
        """Check whether a submit action should be blocked.

        Currently extracts expectations but does not compare them against
        actual values, as the caller always passes actual_values=None.
        Will be extended when DOM value extraction is implemented.

        Args:
            action_name: The action being performed (e.g. "click", "input").
            target_index: The target element index, or None.
            task: The task description containing expected values.
            actual_values: Current field values from the page, or None if
                JS evaluation is not available.
            submit_button_text: Text of the button being clicked, or None.

        Returns:
            Frozen GuardResult indicating whether to block and a message.
        """
        if action_name != "click":
            return GuardResult(should_block=False, message="")

        expectations = self._extract_expectations(task)
        if not expectations:
            return GuardResult(should_block=False, message="")

        return GuardResult(should_block=False, message="")

    def _extract_expectations(self, task: str) -> dict[str, str]:
        """Extract expected field values from the task description.

        Iterates EXPECTATION_PATTERNS (ordered specific-to-generic) and
        returns a dict mapping field names to extracted values. Overlapping
        matches are skipped -- once a span is consumed by a more specific
        pattern, a less specific one cannot reuse it.

        Args:
            task: The task description text.

        Returns:
            Dict mapping field name to extracted value string.
        """
        result: dict[str, str] = {}
        used_spans: list[tuple[int, int]] = []
        for pattern, field_name in EXPECTATION_PATTERNS:
            match = pattern.search(task)
            if match:
                span = match.span()
                # Skip if this match overlaps with an already-consumed span
                if any(
                    span[0] < used_end and span[1] > used_start
                    for used_start, used_end in used_spans
                ):
                    continue
                result[field_name] = match.group(1)
                used_spans.append(span)
        return result
