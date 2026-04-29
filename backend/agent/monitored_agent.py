"""MonitoredAgent -- Agent subclass wiring 3 detectors into browser-use lifecycle.

Overrides _prepare_context() to inject intervention messages into LLM context
after super() clears context_messages. Overrides _execute_actions() to block
submit clicks when PreSubmitGuard detects field mismatches. Provides
create_step_callback() for register_new_step_callback integration.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
from typing import Any, Callable

from browser_use import Agent
from browser_use.agent.views import ActionResult
from browser_use.llm.messages import UserMessage

from backend.agent.action_utils import extract_action_info
from backend.agent.pre_submit_guard import PreSubmitGuard
from backend.agent.stall_detector import StallDetector
from backend.agent.task_progress_tracker import TaskProgressTracker

logger = logging.getLogger(__name__)


class MonitoredAgent(Agent):
    """Agent subclass with stall detection, submit guarding, and progress tracking.

    - _prepare_context(): injects _pending_interventions after super() clears
      context_messages (SUB-01).
    - create_step_callback(): returns async callback that stores detector
      results in _pending_interventions, not via _add_context_message (SUB-02).
    - _execute_actions(): blocks submit click when PreSubmitGuard returns
      should_block=True (SUB-03).
    - All detector calls wrapped in try/except for fault tolerance (D-07/D-08).
    """

    def __init__(
        self,
        *,
        stall_detector: StallDetector | None = None,
        pre_submit_guard: PreSubmitGuard | None = None,
        task_progress_tracker: TaskProgressTracker | None = None,
        run_logger: Any = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._stall_detector = stall_detector or StallDetector()
        self._pre_submit_guard = pre_submit_guard or PreSubmitGuard()
        self._task_tracker = task_progress_tracker or TaskProgressTracker()
        self._run_logger = run_logger
        self._pending_interventions: list[str] = []

        # Parse task for progress tracking
        try:
            self._task_tracker.parse_task(self.task)
        except Exception:
            logger.warning("Failed to parse task for progress tracking")

    async def _prepare_context(self, step_info: Any = None) -> Any:
        """Override to inject intervention messages after super() clears context.

        super()._prepare_context() calls prepare_step_state() which clears
        context_messages, then adds built-in nudges. We inject our custom
        interventions AFTER that, so they survive the clear cycle.
        """
        result = await super()._prepare_context(step_info)
        try:
            if self._pending_interventions:
                for msg in self._pending_interventions:
                    self._message_manager._add_context_message(
                        UserMessage(content=msg)
                    )
                    if self._run_logger:
                        self._run_logger.log(
                            "info", "monitor",
                            "Intervention injected",
                            detail=msg[:100],
                        )
                self._pending_interventions = []
        except Exception as e:
            logger.error("[monitor] Failed to inject interventions: %s", e)
        return result

    async def _execute_actions(self) -> None:
        """Override to block submit clicks when PreSubmitGuard detects mismatches.

        Only checks the first action for submit intent. If blocking, sets
        last_result with ActionResult containing error message and returns
        without calling super()._execute_actions().
        """
        if self.state.last_model_output is None:
            await super()._execute_actions()
            return

        actions = self.state.last_model_output.action
        if not actions:
            await super()._execute_actions()
            return

        first_action = actions[0]
        action_data = first_action.model_dump(exclude_unset=True)
        action_name = next(iter(action_data.keys()), "unknown")

        if action_name == "click":
            try:
                guard_result = self._pre_submit_guard.check(
                    action_name=action_name,
                    target_index=action_data.get("click", {}).get("index"),
                    task=self.task,
                    actual_values=None,
                    submit_button_text=None,
                )
                if guard_result.should_block:
                    self.state.last_result = [
                        ActionResult(error=guard_result.message)
                    ]
                    self._message_manager._add_context_message(
                        UserMessage(content=guard_result.message)
                    )
                    logger.warning(
                        "[PreSubmitGuard] Blocked submit: %s",
                        guard_result.message[:100],
                    )
                    if self._run_logger:
                        self._run_logger.log(
                            "warning", "monitor",
                            "Submit blocked",
                            detail=guard_result.message[:100],
                        )
                    return
            except Exception as e:
                logger.error("[monitor] PreSubmitGuard check failed: %s", e)

        await super()._execute_actions()

        # Post-upload wait: let ERP asynchronously process the uploaded file
        # (render thumbnail, send to server, etc.) before the next screenshot
        if action_name == "upload_file":
            try:
                await asyncio.sleep(3)
                logger.info("[monitor] Post-upload wait completed (3s)")
            except Exception as e:
                logger.error("[monitor] Post-upload wait failed: %s", e)

    def create_step_callback(self) -> Callable:
        """Return async step callback for register_new_step_callback.

        The callback:
        1. Extracts action_name, target_index, evaluation from parameters
        2. Computes dom_hash from dom_state
        3. Calls stall_detector.check() -> stores in _pending_interventions
        4. Calls task_tracker.check_progress() -> stores in _pending_interventions
        5. Calls task_tracker.update_from_evaluation()
        6. All wrapped in try/except for fault tolerance (D-07/D-08)
        """

        async def step_callback(
            browser_state: Any, agent_output: Any, step: int
        ) -> None:
            try:
                action_name = ""
                target_index: int | None = None
                evaluation = ""
                dom_hash = ""

                action_name, action_params = extract_action_info(agent_output)
                target_index = (
                    action_params.get("index") if action_params else None
                )

                if agent_output and hasattr(
                    agent_output, "evaluation_previous_goal"
                ):
                    evaluation = agent_output.evaluation_previous_goal or ""

                if browser_state and hasattr(browser_state, "dom_state"):
                    dom_state = browser_state.dom_state
                    if dom_state and hasattr(dom_state, "llm_representation"):
                        try:
                            dom_str = dom_state.llm_representation()
                            dom_hash = hashlib.sha256(
                                dom_str.encode("utf-8")
                            ).hexdigest()[:12]
                        except Exception:
                            dom_hash = ""

                # Stall detection
                stall_result = self._stall_detector.check(
                    action_name=action_name,
                    target_index=target_index,
                    evaluation=evaluation,
                    dom_hash=dom_hash,
                )
                if stall_result.should_intervene:
                    self._pending_interventions.append(stall_result.message)
                    logger.info(
                        "[monitor] Stall detected at step %d: %s",
                        step,
                        stall_result.message[:80],
                    )

                # Progress tracking
                progress_result = self._task_tracker.check_progress(
                    current_step=step,
                    max_steps=getattr(self.state, "max_steps", 30),
                )
                if progress_result.should_warn:
                    self._pending_interventions.append(
                        progress_result.message
                    )
                    logger.info(
                        "[monitor] Progress warning at step %d: %s",
                        step,
                        progress_result.message[:80],
                    )

                self._task_tracker.update_from_evaluation(evaluation)

            except Exception as e:
                logger.error(
                    "[monitor] step_callback error (non-blocking): %s", e
                )

        return step_callback
