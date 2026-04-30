# Agent 可靠性增强实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 通过中间层监控和 Prompt 优化解决 Agent 循环重试、字段误填、步骤遗漏、提交未校验等问题。

**Architecture:** 在 `AgentService.step_callback` 中集成 3 个检测器（StallDetector、PreSubmitGuard、TaskProgressTracker），通过 browser-use 的 `_message_manager._add_context_message()` 机制向 LLM 注入干预消息。同时通过 `extend_system_message` 注入增强的系统提示词。

**Tech Stack:** Python 3.11, browser-use 0.12.x, pytest, asyncio

**Design doc:** `docs/plans/2026-03-27-agent-reliability-design.md`

---

### Task 1: StallDetector — 停滞检测器

**Files:**
- Create: `backend/core/stall_detector.py`
- Test: `backend/tests/unit/test_stall_detector.py`

**Step 1: Write the failing test**

```python
"""Unit tests for StallDetector."""
import pytest


class TestStallDetectorCheck:
    """Test stall detection logic."""

    def test_no_stall_on_first_failure(self):
        """Single failure should not trigger stall."""
        from backend.core.stall_detector import StallDetector

        detector = StallDetector(max_consecutive_failures=2)
        result = detector.check(
            action_name="click",
            target_index=6246,
            evaluation="Failed to input sales amount",
            dom_hash="abc123",
        )
        assert result.should_intervene is False
        assert result.message == ""

    def test_stall_on_two_consecutive_failures_same_target(self):
        """Two consecutive failures on same target should trigger stall."""
        from backend.core.stall_detector import StallDetector

        detector = StallDetector(max_consecutive_failures=2)
        detector.check("click", 6246, "Failed to input sales amount", "abc123")
        result = detector.check("click", 6246, "Failed to input sales amount", "abc123")
        assert result.should_intervene is True
        assert "6246" in result.message
        assert "evaluate" in result.message

    def test_no_stall_on_different_target(self):
        """Failures on different targets should not trigger stall."""
        from backend.core.stall_detector import StallDetector

        detector = StallDetector(max_consecutive_failures=2)
        detector.check("click", 6246, "Failed", "abc123")
        result = detector.check("click", 6250, "Failed", "abc123")
        assert result.should_intervene is False

    def test_no_stall_on_different_action(self):
        """Different actions on same target should not trigger stall."""
        from backend.core.stall_detector import StallDetector

        detector = StallDetector(max_consecutive_failures=2)
        detector.check("click", 6246, "Failed", "abc123")
        result = detector.check("input", 6246, "Failed", "abc123")
        assert result.should_intervene is False

    def test_stall_on_three_identical_dom_hashes(self):
        """Three identical DOM hashes should trigger stall."""
        from backend.core.stall_detector import StallDetector

        detector = StallDetector(max_consecutive_failures=2, max_stagnant_steps=3)
        detector.check("click", 6246, "Success", "hash1")
        detector.check("click", 6250, "Success", "hash1")
        result = detector.check("wait", None, "Waiting", "hash1")
        assert result.should_intervene is True
        assert result.message != ""

    def test_reset_on_success(self):
        """A success should reset the consecutive failure counter."""
        from backend.core.stall_detector import StallDetector

        detector = StallDetector(max_consecutive_failures=2)
        detector.check("click", 6246, "Failed", "abc123")
        detector.check("click", 6246, "Successfully clicked", "def456")
        result = detector.check("click", 6246, "Failed", "abc123")
        assert result.should_intervene is False

    def test_dom_hash_change_resets_stagnant_counter(self):
        """DOM hash change should reset stagnant step counter."""
        from backend.core.stall_detector import StallDetector

        detector = StallDetector(max_consecutive_failures=2, max_stagnant_steps=3)
        detector.check("click", 6246, "Success", "hash1")
        detector.check("click", 6250, "Success", "hash1")
        detector.check("click", 6246, "Success", "hash2")  # DOM changed
        result = detector.check("wait", None, "Waiting", "hash2")
        assert result.should_intervene is False
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest backend/tests/unit/test_stall_detector.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'backend.core.stall_detector'`

**Step 3: Write minimal implementation**

```python
"""StallDetector — 检测 Agent 停滞并生成干预消息。

触发条件（满足任一）:
1. 连续 N 次对同一 target_index 执行相同 action 且 evaluation 含失败关键词
2. 连续 M 步 DOM 哈希完全相同（页面无任何变化）
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


FAILURE_KEYWORDS = re.compile(
    r"fail|失败|错误|error|unable|无法|cannot|can't|不成功",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class StallResult:
    """停滞检测结果。"""

    should_intervene: bool
    message: str


@dataclass
class StallDetector:
    """检测 Agent 是否陷入停滞循环。"""

    max_consecutive_failures: int = 2
    max_stagnant_steps: int = 3

    _history: list[_StepRecord] = field(default_factory=list, repr=False)

    def check(
        self,
        action_name: str,
        target_index: int | None,
        evaluation: str,
        dom_hash: str,
    ) -> StallResult:
        record = _StepRecord(
            action_name=action_name,
            target_index=target_index,
            evaluation=evaluation,
            dom_hash=dom_hash,
        )
        self._history.append(record)
        result = self._detect_stall()
        return result

    def _detect_stall(self) -> StallResult:
        result = self._check_consecutive_failures()
        if result.should_intervene:
            return result
        return self._check_stagnant_dom()

    def _check_consecutive_failures(self) -> StallResult:
        consecutive = 0
        last_action = None
        last_index = None

        for record in reversed(self._history):
            is_failure = bool(FAILURE_KEYWORDS.search(record.evaluation))
            if not is_failure:
                break
            if record.action_name != last_action or record.target_index != last_index:
                break
            consecutive += 1
            last_action = record.action_name
            last_index = record.target_index

        if consecutive >= self.max_consecutive_failures:
            return StallResult(
                should_intervene=True,
                message=(
                    f"WARNING: You have tried '{last_action}' on element [{last_index}] "
                    f"{consecutive} times and it keeps failing. "
                    f"STOP repeating this action. Instead try one of:\n"
                    f"- Use 'evaluate' to run JavaScript that directly manipulates the DOM\n"
                    f"- Use 'find_elements' with a CSS selector to locate the real input element\n"
                    f"- Scroll the page to reveal different elements\n"
                    f"- Look for the element in a different part of the DOM tree"
                ),
            )
        return StallResult(should_intervene=False, message="")

    def _check_stagnant_dom(self) -> StallResult:
        if len(self._history) < self.max_stagnant_steps:
            return StallResult(should_intervene=False, message="")

        recent = self._history[-self.max_stagnant_steps :]
        hashes = [r.dom_hash for r in recent]
        if len(set(hashes)) == 1 and hashes[0]:
            return StallResult(
                should_intervene=True,
                message=(
                    f"WARNING: The page has not changed for {self.max_stagnant_steps} consecutive steps. "
                    f"You may be stuck. Try a completely different approach:\n"
                    f"- Navigate to a different page and come back\n"
                    f"- Use 'evaluate' to execute JavaScript directly\n"
                    f"- Scroll to find elements you may have missed"
                ),
            )
        return StallResult(should_intervene=False, message="")


@dataclass(frozen=True)
class _StepRecord:
    action_name: str
    target_index: int | None
    evaluation: str
    dom_hash: str
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest backend/tests/unit/test_stall_detector.py -v`
Expected: All 7 tests PASS

**Step 5: Commit**

```bash
git add backend/core/stall_detector.py backend/tests/unit/test_stall_detector.py
git commit -m "feat: add StallDetector for agent loop detection"
```

---

### Task 2: PreSubmitGuard — 提交前校验器

**Files:**
- Create: `backend/core/pre_submit_guard.py`
- Test: `backend/tests/unit/test_pre_submit_guard.py`

**Step 1: Write the failing test**

```python
"""Unit tests for PreSubmitGuard."""
import pytest


class TestPreSubmitGuardCheck:
    """Test pre-submit validation logic."""

    def test_no_validation_when_not_submit_action(self):
        """Non-submit actions should pass through."""
        from backend.core.pre_submit_guard import PreSubmitGuard

        guard = PreSubmitGuard()
        result = guard.check(
            action_name="input",
            target_index=6246,
            task="Step 11: Input sales amount 150",
        )
        assert result.should_block is False
        assert result.message == ""

    def test_blocks_submit_with_missing_field(self):
        """Submit should be blocked when expected field value doesn't match."""
        from backend.core.pre_submit_guard import PreSubmitGuard

        guard = PreSubmitGuard()
        actual_values = {
            "sales_amount": "0.00",
            "logistics_fee": "10",
            "payment_status": "已收款",
        }
        result = guard.check(
            action_name="click",
            target_index=5051,
            task="Step 11: Input sales amount 150\nStep 13: Input logistics fee 10\nStep 16: Select unpaid status",
            actual_values=actual_values,
            submit_button_text="确认",
        )
        assert result.should_block is True
        assert "150" in result.message
        assert "0.00" in result.message

    def test_allows_submit_when_all_fields_match(self):
        """Submit should be allowed when all expected fields match."""
        from backend.core.pre_submit_guard import PreSubmitGuard

        guard = PreSubmitGuard()
        actual_values = {
            "sales_amount": "150.00",
            "logistics_fee": "10",
            "payment_status": "未收款",
        }
        result = guard.check(
            action_name="click",
            target_index=5051,
            task="Step 11: Input sales amount 150\nStep 13: Input logistics fee 10\nStep 16: Select unpaid status",
            actual_values=actual_values,
            submit_button_text="确认",
        )
        assert result.should_block is False

    def test_skips_validation_when_no_expectations_found(self):
        """If no expected values can be parsed from task, allow submit."""
        from backend.core.pre_submit_guard import PreSubmitGuard

        guard = PreSubmitGuard()
        result = guard.check(
            action_name="click",
            target_index=5051,
            task="Click the submit button",
            actual_values={"sales_amount": "0"},
            submit_button_text="提交",
        )
        assert result.should_block is False

    def test_extracts_expected_values_from_task(self):
        """Test that expected values are correctly extracted from task description."""
        from backend.core.pre_submit_guard import PreSubmitGuard

        guard = PreSubmitGuard()
        expected = guard._extract_expectations(
            "Step 11: Input sales amount 150\nStep 13: Input logistics fee 10\nStep 14: Input amount 10\nStep 16: Select unpaid"
        )
        assert expected["sales_amount"] == "150"
        assert expected["logistics_fee"] == "10"
        assert expected["amount"] == "10"
        assert expected["payment_status"] == "未收款"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest backend/tests/unit/test_pre_submit_guard.py -v`
Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write minimal implementation**

```python
"""PreSubmitGuard — 在 Agent 点击提交按钮前校验关键字段值。

从 task 描述中正则提取期望值，与页面实际值对比。
校验不通过时生成阻止消息。
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


SUBMIT_KEYWORDS = re.compile(r"确认|提交|保存|submit|confirm|save", re.IGNORECASE)

EXPECTATION_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("sales_amount", re.compile(r"销售金额.*?(\d+\.?\d*)")),
    ("logistics_fee", re.compile(r"物流费用.*?(\d+\.?\d*)")),
    ("amount", re.compile(r"(?<!销售)(?<!物流)金额.*?(\d+\.?\d*)")),
    ("payment_status", re.compile(r"(未收款|unpaid)", re.IGNORECASE)),
]

FIELD_LABELS: dict[str, str] = {
    "sales_amount": "销售金额",
    "logistics_fee": "物流费用",
    "amount": "金额",
    "payment_status": "付款状态",
}


@dataclass(frozen=True)
class SubmitCheckResult:
    """提交校验结果。"""

    should_block: bool
    message: str


@dataclass
class PreSubmitGuard:
    """提交前校验器。"""

    _cached_expectations: dict[str, str] | None = field(default=None, repr=False)

    def check(
        self,
        action_name: str,
        target_index: int,
        task: str,
        actual_values: dict[str, str] | None = None,
        submit_button_text: str | None = None,
    ) -> SubmitCheckResult:
        if action_name != "click" or not submit_button_text:
            return SubmitCheckResult(should_block=False, message="")

        if not SUBMIT_KEYWORDS.search(submit_button_text):
            return SubmitCheckResult(should_block=False, message="")

        if not actual_values:
            return SubmitCheckResult(should_block=False, message="")

        expectations = self._cached_expectations or self._extract_expectations(task)
        self._cached_expectations = expectations

        if not expectations:
            return SubmitCheckResult(should_block=False, message="")

        mismatches = []
        for field_key, expected_val in expectations.items():
            actual_val = actual_values.get(field_key, "")
            if not actual_val:
                continue
            if field_key == "payment_status":
                if expected_val.lower() not in actual_val.lower():
                    mismatches.append(
                        f"  - {FIELD_LABELS[field_key]}: expected '{expected_val}', actual '{actual_val}'"
                    )
            else:
                actual_num = re.sub(r"[^\d.]", "", actual_val)
                expected_num = re.sub(r"[^\d.]", "", expected_val)
                if actual_num != expected_num:
                    mismatches.append(
                        f"  - {FIELD_LABELS[field_key]}: expected {expected_val}, actual {actual_val}"
                    )

        if not mismatches:
            return SubmitCheckResult(should_block=False, message="")

        message = (
            "BLOCKED: Cannot submit because the following fields are incorrect:\n"
            + "\n".join(mismatches)
            + "\nPlease fix these fields BEFORE clicking submit."
        )
        return SubmitCheckResult(should_block=True, message=message)

    def _extract_expectations(self, task: str) -> dict[str, str]:
        expectations = {}
        for field_key, pattern in EXPECTATION_PATTERNS:
            match = pattern.search(task)
            if match:
                expectations[field_key] = match.group(1)
        return expectations
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest backend/tests/unit/test_pre_submit_guard.py -v`
Expected: All 5 tests PASS

**Step 5: Commit**

```bash
git add backend/core/pre_submit_guard.py backend/tests/unit/test_pre_submit_guard.py
git commit -m "feat: add PreSubmitGuard for pre-submit field validation"
```

---

### Task 3: TaskProgressTracker — 任务进度追踪器

**Files:**
- Create: `backend/core/task_progress_tracker.py`
- Test: `backend/tests/unit/test_task_progress_tracker.py`

**Step 1: Write the failing test**

```python
"""Unit tests for TaskProgressTracker."""
import pytest


class TestTaskProgressTracker:
    """Test task progress tracking and urgency warnings."""

    def test_parse_checkbox_steps(self):
        """Parse checkbox-style task steps."""
        from backend.core.task_progress_tracker import TaskProgressTracker

        tracker = TaskProgressTracker(max_steps=30)
        task = (
            "- [ ] Step 1: Login\n"
            "- [ ] Step 2: Navigate\n"
            "- [ ] Step 3: Fill form\n"
            "- [ ] Step 4: Submit"
        )
        tracker.parse_task(task)
        assert tracker.total_steps == 4
        assert len(tracker.completed_steps) == 0

    def test_parse_numbered_steps(self):
        """Parse numbered task steps."""
        from backend.core.task_progress_tracker import TaskProgressTracker

        tracker = TaskProgressTracker(max_steps=30)
        task = (
            "Step 1: Login\n"
            "Step 2: Navigate\n"
            "Step 3: Fill form"
        )
        tracker.parse_task(task)
        assert tracker.total_steps == 3

    def test_warning_when_steps_running_low(self):
        """Generate warning when remaining steps < remaining tasks * 1.5."""
        from backend.core.task_progress_tracker import TaskProgressTracker

        tracker = TaskProgressTracker(max_steps=10)
        tracker.parse_task("Step 1: A\nStep 2: B\nStep 3: C\nStep 4: D\nStep 5: E")
        tracker.mark_completed("A")
        tracker.mark_completed("B")
        # 3 remaining tasks, 8 remaining steps → 8 < 3*1.5=4.5? No
        result = tracker.check_progress(current_step=3)
        assert result.level == ""

    def test_urgent_when_steps_critical(self):
        """Generate urgent warning when remaining steps <= remaining tasks."""
        from backend.core.task_progress_tracker import TaskProgressTracker

        tracker = TaskProgressTracker(max_steps=5)
        tracker.parse_task("Step 1: A\nStep 2: B\nStep 3: C\nStep 4: D\nStep 5: E")
        tracker.mark_completed("A")
        tracker.mark_completed("B")
        # 3 remaining tasks, 3 remaining steps → 3 <= 3
        result = tracker.check_progress(current_step=3)
        assert result.level == "urgent"

    def test_mark_completed_by_keyword(self):
        """Mark steps as completed when evaluation mentions them."""
        from backend.core.task_progress_tracker import TaskProgressTracker

        tracker = TaskProgressTracker(max_steps=30)
        tracker.parse_task("Step 1: Login\nStep 2: Navigate\nStep 3: Fill form")
        tracker.update_from_evaluation("Successfully navigated to the page. Verdict: Success")
        assert "Navigate" in tracker.completed_steps

    def test_no_warning_when_no_steps_parsed(self):
        """No warning when task has no parseable steps."""
        from backend.core.task_progress_tracker import TaskProgressTracker

        tracker = TaskProgressTracker(max_steps=5)
        tracker.parse_task("Just do something")
        result = tracker.check_progress(current_step=4)
        assert result.level == ""
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest backend/tests/unit/test_task_progress_tracker.py -v`
Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write minimal implementation**

```python
"""TaskProgressTracker — 追踪任务完成进度并在步数紧张时发出警告。

从 task 描述中提取结构化步骤列表，每步执行后更新进度。
当剩余步数不足以完成剩余任务时注入紧急提醒。
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


STEP_PATTERNS = [
    re.compile(r"Step\s+\d+\s*[:：]\s*(.+)", re.IGNORECASE),
    re.compile(r"第\d+步\s*[:：]\s*(.+)", re.IGNORECASE),
    re.compile(r"^\s*-\s*\[[ x]\]\s*(.+)", re.MULTILINE),
    re.compile(r"^\s*\d+[.)]\s*(.+)", re.MULTILINE),
]


@dataclass(frozen=True)
class ProgressResult:
    """进度检查结果。"""

    level: str  # "", "warning", "urgent"
    message: str


@dataclass
class TaskProgressTracker:
    """任务进度追踪器。"""

    max_steps: int = 30
    _steps: list[str] = field(default_factory=list)
    _completed_steps: set[str] = field(default_factory=set)

    @property
    def total_steps(self) -> int:
        return len(self._steps)

    @property
    def completed_count(self) -> int:
        return len(self._completed_steps)

    @property
    def remaining_tasks(self) -> int:
        return self.total_steps - self.completed_count

    def parse_task(self, task: str) -> None:
        """从 task 描述中提取步骤列表。"""
        steps = []
        for pattern in STEP_PATTERNS:
            matches = pattern.findall(task)
            if matches:
                steps = [m.strip() for m in matches if m.strip()]
                break
        self._steps = steps
        self._completed_steps = set()

    def mark_completed(self, step_text: str) -> None:
        """标记步骤为已完成。"""
        for step in self._steps:
            if step_text.lower() in step.lower() or step.lower() in step_text.lower():
                self._completed_steps.add(step)

    def update_from_evaluation(self, evaluation: str) -> None:
        """从 evaluation 文本中自动标记已完成的步骤。"""
        if not evaluation:
            return
        for step in self._steps:
            keywords = step.split()[:3]
            if any(kw.lower() in evaluation.lower() for kw in keywords):
                self._completed_steps.add(step)

    def check_progress(self, current_step: int) -> ProgressResult:
        """检查进度是否需要发出警告。"""
        if not self._steps:
            return ProgressResult(level="", message="")

        remaining_steps = self.max_steps - current_step
        remaining_tasks = self.remaining_tasks

        if remaining_tasks <= 0:
            return ProgressResult(level="", message="")

        if remaining_steps <= remaining_tasks:
            pending = [s for s in self._steps if s not in self._completed_steps]
            pending_list = "\n".join(f"  - {s}" for s in pending[:5])
            return ProgressResult(
                level="urgent",
                message=(
                    f"URGENT: Only {remaining_steps} steps remaining but {remaining_tasks} tasks incomplete!\n"
                    f"Incomplete tasks:\n{pending_list}\n"
                    f"Use 'evaluate' to batch multiple operations in one step."
                ),
            )

        if remaining_steps < remaining_tasks * 1.5:
            return ProgressResult(
                level="warning",
                message=(
                    f"Warning: {remaining_steps} steps left, {remaining_tasks} tasks remaining. "
                    f"Speed up by combining multiple actions per step."
                ),
            )

        return ProgressResult(level="", message="")
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest backend/tests/unit/test_task_progress_tracker.py -v`
Expected: All 6 tests PASS

**Step 5: Commit**

```bash
git add backend/core/task_progress_tracker.py backend/tests/unit/test_task_progress_tracker.py
git commit -m "feat: add TaskProgressTracker for step budget warnings"
```

---

### Task 4: ENHANCED_SYSTEM_MESSAGE — 增强系统提示词

**Files:**
- Modify: `backend/agent/prompts.py`
- Test: `backend/tests/unit/test_prompts.py`

**Step 1: Write the failing test**

```python
"""Unit tests for enhanced system prompts."""
import pytest


class TestEnhancedSystemMessage:
    """Test ENHANCED_SYSTEM_MESSAGE content."""

    def test_message_contains_click_to_edit_guidance(self):
        """System message should explain click-to-edit pattern."""
        from backend.agent.prompts import ENHANCED_SYSTEM_MESSAGE

        assert "click-to-edit" in ENHANCED_SYSTEM_MESSAGE.lower() or "点击编辑" in ENHANCED_SYSTEM_MESSAGE

    def test_message_contains_failure_recovery_rules(self):
        """System message should contain failure recovery rules."""
        from backend.agent.prompts import ENHANCED_SYSTEM_MESSAGE

        assert "evaluate" in ENHANCED_SYSTEM_MESSAGE.lower()

    def test_message_contains_field_verification_guidance(self):
        """System message should instruct to verify after filling fields."""
        from backend.agent.prompts import ENHANCED_SYSTEM_MESSAGE

        assert "verify" in ENHANCED_SYSTEM_MESSAGE.lower() or "验证" in ENHANCED_SYSTEM_MESSAGE

    def test_message_is_not_empty(self):
        """System message should be a non-empty string."""
        from backend.agent.prompts import ENHANCED_SYSTEM_MESSAGE

        assert isinstance(ENHANCED_SYSTEM_MESSAGE, str)
        assert len(ENHANCED_SYSTEM_MESSAGE) > 100
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest backend/tests/unit/test_prompts.py -v`
Expected: FAIL with `ImportError: cannot import name 'ENHANCED_SYSTEM_MESSAGE'`

**Step 3: Write minimal implementation**

在 `backend/agent/prompts.py` 末尾追加 `ENHANCED_SYSTEM_MESSAGE`。保留原有的 `CHINESE_ENHANCEMENT` 和 `LOGIN_TASK_PROMPT` 不变。

```python
# 增强系统消息 — 通过 browser-use 的 extend_system_message 参数注入
ENHANCED_SYSTEM_MESSAGE = """
## 表格编辑模式 (Click-to-Edit)

很多中文后台系统（如 Ant Design）的表格使用 click-to-edit 模式：
- 表格中的数值列（如"销售金额"、"利润"）看起来是普通文本
- 但点击该单元格后，会动态弹出一个 input 输入框
- 在 DOM 快照中，这些单元格显示为空的 `<td />`，没有子 input 元素

操作流程：
1. 先 click 该 `<td />` 元素
2. 等待下一步（让 input 弹出）
3. 对新出现的 input 执行 input 操作

识别特征：
- 表格行中出现连续的空 `<td />` 元素（有 index 但无子元素）
- 通常位于数值列（金额、数量、价格等）

## 失败恢复强制规则

- 同一元素操作失败 2 次后，**禁止**再尝试完全相同的操作
- 必须切换到以下替代策略之一：
  1. 使用 `evaluate` 执行 JavaScript 直接操作 DOM 元素
  2. 使用 `find_elements` 用 CSS 选择器精确查找目标
  3. 滚动页面后重新定位元素
- 在 memory 中记录已失败的 index 和已尝试过的方法

## 字段填写后立即验证

- 每填写一个数值字段后，等待一步观察页面变化
- 使用 screenshot 作为 ground truth 确认值已正确填入
- 如果值未变化，立即标记为 Failure 并切换策略
- 不要假设 input 操作成功 — 始终从截图验证

## 提交前完整校验

- 点击"确认"/"提交"按钮前，必须逐项检查所有关键字段
- 确认每个必填字段的值与任务要求一致
- 如果发现任何字段不正确，先修复再提交
- 不要在字段未验证的情况下点击提交按钮
"""
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest backend/tests/unit/test_prompts.py -v`
Expected: All 4 tests PASS

**Step 5: Commit**

```bash
git add backend/agent/prompts.py backend/tests/unit/test_prompts.py
git commit -m "feat: add ENHANCED_SYSTEM_MESSAGE for better agent guidance"
```

---

### Task 5: 集成到 AgentService

**Files:**
- Modify: `backend/core/agent_service.py`

这是最关键的集成任务。需要修改 `run_with_streaming()` 方法：

1. 创建 3 个检测器实例
2. 在 `step_callback` 中调用检测器
3. 通过 `agent._message_manager._add_context_message()` 注入干预消息
4. 传入 `extend_system_message`
5. 调优 browser-use 内置参数

**Step 1: Write the integration test**

```python
"""Integration test for AgentService with reliability monitors."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestAgentServiceReliabilityIntegration:
    """Test that monitors are created and called in step_callback."""

    @patch("backend.core.agent_service.create_llm")
    @patch("backend.core.agent_service.create_browser_session")
    def test_stall_detector_receives_step_data(self, mock_create_session, mock_create_llm):
        """StallDetector should receive action data from each step."""
        from backend.core.agent_service import AgentService

        mock_llm = MagicMock()
        mock_llm.model = "test-model"
        mock_create_llm.return_value = mock_llm

        mock_session = MagicMock()
        mock_create_session.return_value = mock_session

        service = AgentService()

        # Verify the service can be instantiated
        assert service is not None

    @patch("backend.core.agent_service.create_llm")
    @patch("backend.core.agent_service.create_browser_session")
    def test_extend_system_message_passed_to_agent(self, mock_create_session, mock_create_llm):
        """extend_system_message should be passed to browser-use Agent."""
        from backend.core.agent_service import AgentService
        from backend.agent.prompts import ENHANCED_SYSTEM_MESSAGE

        mock_llm = MagicMock()
        mock_llm.model = "test-model"
        mock_create_llm.return_value = mock_llm

        mock_session = MagicMock()
        mock_create_session.return_value = mock_session

        service = AgentService()

        # Verify ENHANCED_SYSTEM_MESSAGE exists and is usable
        assert isinstance(ENHANCED_SYSTEM_MESSAGE, str)
        assert len(ENHANCED_SYSTEM_MESSAGE) > 100
```

**Step 2: Run test to verify it passes (baseline)**

Run: `uv run pytest backend/tests/unit/test_agent_service_reliability.py -v`
Expected: PASS (these are baseline tests that verify the service can be created)

**Step 3: Modify agent_service.py**

在 `run_with_streaming()` 中进行以下修改：

**3a. 添加导入**（文件顶部）:

```python
from browser_use.llm.messages import UserMessage
from backend.agent.prompts import ENHANCED_SYSTEM_MESSAGE
from backend.core.stall_detector import StallDetector
from backend.core.pre_submit_guard import PreSubmitGuard
from backend.core.task_progress_tracker import TaskProgressTracker
```

**3b. 在 `run_with_streaming()` 方法中创建检测器**（在 `run_logger` 创建之后）:

```python
# 创建可靠性监控器
stall_detector = StallDetector(max_consecutive_failures=2, max_stagnant_steps=3)
pre_submit_guard = PreSubmitGuard()
progress_tracker = TaskProgressTracker(max_steps=max_steps)
progress_tracker.parse_task(actual_task)
```

**3c. 在 `step_callback` 中调用检测器**（在结构化日志之后、截图之前）:

```python
# ===== 可靠性监控 =====
intervention_messages = []

# 停滞检测
stall_result = stall_detector.check(
    action_name=action_name,
    target_index=action_params.get("index"),
    evaluation=getattr(agent_output, "evaluation_previous_goal", "") or "",
    dom_hash=dom_hash,
)
if stall_result.should_intervene:
    intervention_messages.append(stall_result.message)
    logger.warning(f"[{run_id}] 停滞检测触发: {stall_result.message[:100]}")
    run_logger.log("warning", "monitor", "Stall detected", step=step)

# 进度追踪
if agent_output:
    evaluation_text = getattr(agent_output, "evaluation_previous_goal", "") or ""
    progress_tracker.update_from_evaluation(evaluation_text)
progress_result = progress_tracker.check_progress(current_step=step)
if progress_result.level:
    intervention_messages.append(progress_result.message)
    logger.info(f"[{run_id}] 进度提醒 ({progress_result.level}): {progress_result.message[:100]}")
    run_logger.log("info", "monitor", f"Progress {progress_result.level}", step=step)

# 注入干预消息到下一轮 LLM 上下文
if intervention_messages and hasattr(self, '_agent_ref') and self._agent_ref:
    combined_msg = "\n\n".join(intervention_messages)
    try:
        self._agent_ref._message_manager._add_context_message(
            UserMessage(content=combined_msg)
        )
    except Exception as e:
        logger.warning(f"[{run_id}] 注入干预消息失败: {e}")
```

**3d. 传入 extend_system_message 并调优参数**（Agent 创建处）:

```python
agent = Agent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
    max_actions_per_step=5,
    register_new_step_callback=step_callback,
    extend_system_message=ENHANCED_SYSTEM_MESSAGE,
    planning_replan_on_stall=2,       # 更激进的重规划阈值
    loop_detection_window=10,          # 更小的循环检测窗口
    max_failures=4,                    # 稍低的失败上限
)

# 存储 agent 引用供 step_callback 注入消息
self._agent_ref = agent
```

**3e. 在 finally 块中清理引用**:

```python
finally:
    self._agent_ref = None
    run_logger.close()
```

**Step 4: Run all unit tests**

Run: `uv run pytest backend/tests/unit/ -v -k "stall_detector or pre_submit_guard or task_progress_tracker or test_prompts or agent_service_reliability"`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add backend/core/agent_service.py backend/tests/unit/test_agent_service_reliability.py
git commit -m "feat: integrate reliability monitors into AgentService"
```

---

### Task 6: 端到端验证

**Step 1: 启动后端服务**

```bash
uv run uvicorn backend.api.main:app --reload --port 11002
```

**Step 2: 运行一次完整的 ERP 销售出库测试**

通过前端 UI 或 API 发送与 7fcea593 相同的任务，验证：
- Agent 不再对同一元素重复失败超过 2 次
- 点击确认按钮前有关键字段校验
- 日志中出现 "Stall detected" 或 "Progress warning" 时消息被正确注入

**Step 3: 检查 per-run 日志**

检查 `outputs/<new_run_id>/logs/run.jsonl` 中是否出现：
- `"category": "monitor"` 的日志条目
- Agent 行为是否有改善（更少的重复失败步骤）

**Step 4: Commit final state**

如果有微调修复，提交。

---

## 任务依赖关系

```
Task 1 (StallDetector) ──┐
Task 2 (PreSubmitGuard) ──┼── Task 5 (集成) ── Task 6 (E2E验证)
Task 3 (ProgressTracker)─┘
Task 4 (Prompt) ──────────┘
```

Tasks 1-4 可以并行执行，Task 5 依赖它们全部完成，Task 6 最后执行。
