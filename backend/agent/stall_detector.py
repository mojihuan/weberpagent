"""StallDetector -- detects Agent stall via consecutive failures and stagnant DOM.

Identifies when the Agent is stuck in a loop (repeated failures on same element)
or when the page is not changing (stagnant DOM). Returns frozen StallResult
dataclass (immutable) per project coding conventions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


FAILURE_KEYWORDS = re.compile(
    r"fail|失败|错误|error|unable|无法|cannot|can't|不成功",
    re.IGNORECASE,
)

_WRONG_COLUMN_KEYWORDS = re.compile(
    r"wrong.?column|错误列|误点|非目标列|clicked.*wrong",
    re.IGNORECASE,
)

_EDIT_NOT_ACTIVE_KEYWORDS = re.compile(
    r"not.?editable|无法输入|元素不可操作|cannot.?type|not.?interactable",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class StallResult:
    """Immutable result from StallDetector.check()."""

    should_intervene: bool
    message: str


@dataclass(frozen=True)
class FailureDetectionResult:
    """失败模式检测结果（不可变）。

    Per D-02: 与 StallResult 平级的 frozen dataclass。
    failure_mode=None 表示未检测到失败模式。
    details 包含诊断信息（关键词匹配、hash 比对结果等）。
    """

    failure_mode: str | None
    details: dict


@dataclass
class _StepRecord:
    """Internal record of a single step for stall tracking."""

    action_name: str
    target_index: int | None
    evaluation: str
    dom_hash: str


@dataclass
class StallDetector:
    """Detects Agent stall via consecutive failures and stagnant DOM.

    - Consecutive failures: triggers when N consecutive steps fail on the same
      action and target_index (MON-01).
    - Stagnant DOM: triggers when N consecutive steps have identical dom_hash
      (MON-02).
    - Success resets the consecutive failure counter (MON-03).
    """

    max_consecutive_failures: int = 2
    max_stagnant_steps: int = 3
    _MAX_HISTORY: int = 1000
    _history: list[_StepRecord] = field(default_factory=list, repr=False)

    def check(
        self,
        action_name: str,
        target_index: int | None,
        evaluation: str,
        dom_hash: str,
    ) -> StallResult:
        """Record a step and check for stall conditions.

        Args:
            action_name: The action taken (e.g. "click", "input").
            target_index: The target element index, or None.
            evaluation: The evaluation/result text from the step.
            dom_hash: A hash fingerprint of the DOM state.

        Returns:
            Frozen StallResult indicating whether to intervene and a message.
        """
        record = _StepRecord(
            action_name=action_name,
            target_index=target_index,
            evaluation=evaluation,
            dom_hash=dom_hash,
        )
        self._history.append(record)
        if len(self._history) > self._MAX_HISTORY:
            self._history = self._history[-self._MAX_HISTORY:]
        return self._detect_stall()

    def _detect_stall(self) -> StallResult:
        """Check all stall conditions, returning the first match."""
        failure_result = self._check_consecutive_failures()
        if failure_result.should_intervene:
            return failure_result
        return self._check_stagnant_dom()

    def _check_consecutive_failures(self) -> StallResult:
        """Check for consecutive failures on same action+target (MON-01, MON-03)."""
        consecutive = 0
        last_action: str | None = None
        last_index: int | None = None

        for record in reversed(self._history):
            is_failure = bool(FAILURE_KEYWORDS.search(record.evaluation))
            if not is_failure:
                break  # Success resets
            if last_action is None:
                # First failure record -- set baseline before comparison
                last_action = record.action_name
                last_index = record.target_index
                consecutive = 1
                continue
            if record.action_name != last_action or record.target_index != last_index:
                break  # Different action or target
            consecutive += 1

        if consecutive >= self.max_consecutive_failures:
            message = (
                f"\u3010\u505c\u6ede\u8b66\u544a\u3011\u8fde\u7eed{consecutive}\u6b21\u5bf9\u5143\u7d20#{last_index}"
                f"\u6267\u884c'{last_action}'\u5931\u8d25\u3002"
                "\u5efa\u8bae\uff1a\u4f7f\u7528evaluate\u6267\u884cJavaScript\u76f4\u63a5\u64cd\u4f5cDOM"
                "\u3001\u4f7f\u7528find_elements\u67e5\u627e\u771f\u5b9einput\u5143\u7d20"
                "\u3001\u6216\u6eda\u52a8\u9875\u9762\u67e5\u627e\u5176\u4ed6\u5143\u7d20\u3002"
            )
            return StallResult(should_intervene=True, message=message)

        return StallResult(should_intervene=False, message="")

    def _check_stagnant_dom(self) -> StallResult:
        """Check for stagnant DOM -- identical dom_hash across recent steps (MON-02)."""
        if len(self._history) < self.max_stagnant_steps:
            return StallResult(should_intervene=False, message="")

        recent = self._history[-self.max_stagnant_steps :]
        hashes = {record.dom_hash for record in recent}

        if len(hashes) == 1:
            message = (
                f"\u3010\u9875\u9762\u505c\u6ede\u3011\u8fde\u7eed{self.max_stagnant_steps}"
                "\u6b65\u9875\u9762\u65e0\u53d8\u5316\uff08DOM\u6307\u7eb9\u76f8\u540c\uff09\u3002"
                "\u5efa\u8bae\uff1a\u6eda\u52a8\u9875\u9762"
                "\u3001\u70b9\u51fb\u5c55\u5f00\u6298\u53e0\u533a\u57df"
                "\u3001\u6216\u68c0\u67e5\u662f\u5426\u9700\u8981\u5207\u6362\u5230\u5176\u4ed6iframe\u3002"
            )
            return StallResult(should_intervene=True, message=message)

        return StallResult(should_intervene=False, message="")

    def detect_failure_mode(
        self,
        action_name: str,
        target_index: int | None,
        evaluation: str,
        dom_hash_before: str,
        dom_hash_after: str,
    ) -> FailureDetectionResult:
        """检测三种 ERP 表格交互失败模式。

        Per D-03: 与 check() 平级的独立方法，不修改 _history。
        检测顺序: wrong_column -> edit_not_active -> click_no_effect。

        Args:
            action_name: 操作类型（click, input 等）。
            target_index: 目标元素索引。
            evaluation: Agent 评估文本。
            dom_hash_before: 操作前 DOM 哈希。
            dom_hash_after: 操作后 DOM 哈希。

        Returns:
            FailureDetectionResult（frozen），failure_mode=None 表示无失败。
        """
        # 检测 wrong_column（evaluation 关键词匹配）
        wrong_match = _WRONG_COLUMN_KEYWORDS.search(evaluation)
        if wrong_match:
            return FailureDetectionResult(
                failure_mode="wrong_column",
                details={
                    "keywords_matched": [wrong_match.group()],
                    "evaluation_snippet": evaluation[:100],
                    "target_index": target_index,
                },
            )

        # 检测 edit_not_active（input 操作 + evaluation 关键词）
        if action_name == "input":
            edit_match = _EDIT_NOT_ACTIVE_KEYWORDS.search(evaluation)
            if edit_match:
                return FailureDetectionResult(
                    failure_mode="edit_not_active",
                    details={
                        "keywords_matched": [edit_match.group()],
                        "evaluation_snippet": evaluation[:100],
                        "target_index": target_index,
                    },
                )

        # 检测 click_no_effect（click 操作 + DOM 无变化）
        if action_name == "click" and dom_hash_before == dom_hash_after:
            return FailureDetectionResult(
                failure_mode="click_no_effect",
                details={
                    "target_index": target_index,
                    "dom_hash": dom_hash_before,
                },
            )

        # 无失败
        return FailureDetectionResult(failure_mode=None, details={})
