"""TaskProgressTracker -- tracks step progress and warns when budget is tight.

Parses task descriptions into structured step lists, tracks which steps have been
completed via evaluation keyword matching, and emits warnings when the remaining
step budget is tight relative to remaining tasks.

Returns frozen ProgressResult dataclass (immutable) per project coding conventions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

STEP_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"^\s*Step\s+(\d+)\s*[:：]\s*(.+)$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^\s*第(\d+)步\s*[:：]?\s*(.+)$", re.MULTILINE),
    re.compile(r"^\s*-\s*\[[\sx]\]\s*(.+)$", re.MULTILINE),
    re.compile(r"^\s*(\d+)[\.、)]\s*(.+)$", re.MULTILINE),
]


@dataclass(frozen=True)
class ProgressResult:
    """Immutable result from TaskProgressTracker.check_progress()."""

    should_warn: bool
    level: str  # "", "warning", "urgent"
    message: str
    remaining_steps: int
    remaining_tasks: int


@dataclass
class TaskProgressTracker:
    """Tracks task step progress and warns when step budget is tight.

    - Parses task descriptions into structured step lists (MON-07).
    - Emits warning when remaining_steps < remaining_tasks * 1.5 (MON-08).
    - Emits urgent when remaining_steps <= remaining_tasks (MON-08).
    - Returns empty ProgressResult for tasks with no parseable steps.
    """

    _steps: list[str] = field(default_factory=list, repr=False)
    _completed_steps: set[int] = field(default_factory=set, repr=False)

    def parse_task(self, task: str) -> None:
        """Parse task description into a list of step descriptions.

        Tries each STEP_PATTERN in priority order. First pattern with >= 1
        match wins. Step descriptions are stored without step numbers.

        Args:
            task: The task description text to parse.
        """
        self._completed_steps = set()

        for pattern in STEP_PATTERNS:
            matches = pattern.findall(task)
            if matches:
                is_numbered = len(matches[0]) == 2 and matches[0][0].isdigit()
                if is_numbered:
                    sorted_matches = sorted(matches, key=lambda m: int(m[0]))
                    self._steps = [desc.strip() for _, desc in sorted_matches]
                else:
                    self._steps = [m.strip() for m in matches]
                return

        self._steps = []

    def check_progress(self, current_step: int, max_steps: int) -> ProgressResult:
        """Check progress and emit warnings when step budget is tight.

        Args:
            current_step: The current step number (0-based or 1-based, used as-is).
            max_steps: Maximum allowed steps.

        Returns:
            Frozen ProgressResult with warning level and message.
        """
        if not self._steps:
            return ProgressResult(
                should_warn=False,
                level="",
                message="",
                remaining_steps=0,
                remaining_tasks=0,
            )

        remaining_steps = max_steps - current_step
        remaining_tasks = len(self._steps) - len(self._completed_steps)

        if remaining_tasks <= 0:
            return ProgressResult(
                should_warn=False,
                level="",
                message="",
                remaining_steps=remaining_steps,
                remaining_tasks=0,
            )

        if remaining_steps <= remaining_tasks:
            level = "urgent"
        elif remaining_steps < remaining_tasks * 1.5:
            level = "warning"
        else:
            level = ""

        if level == "warning":
            message = (
                f"【进度预警】剩余{remaining_steps}步，"
                f"还有{remaining_tasks}个任务未完成。"
                "建议加快节奏，优先完成关键步骤。"
            )
        elif level == "urgent":
            message = (
                f"【进度紧迫】剩余{remaining_steps}步，"
                f"还有{remaining_tasks}个任务未完成！"
                "建议立即跳过非关键步骤，专注于核心任务。"
            )
        else:
            message = ""

        return ProgressResult(
            should_warn=(level != ""),
            level=level,
            message=message,
            remaining_steps=remaining_steps,
            remaining_tasks=remaining_tasks,
        )

    def update_from_evaluation(self, evaluation: str) -> None:
        """Mark steps as completed based on keyword matching in evaluation text.

        For each uncompleted step, extracts the first 3 significant words
        from the step description and checks if ANY of those words appear
        in the evaluation text (case-insensitive, loose matching).

        Args:
            evaluation: The evaluation/result text from a step.
        """
        evaluation_lower = evaluation.lower()

        for i, step_text in enumerate(self._steps):
            if i in self._completed_steps:
                continue

            words = step_text.split()
            keywords = words[:3]

            if any(keyword.lower() in evaluation_lower for keyword in keywords):
                self._completed_steps.add(i)
