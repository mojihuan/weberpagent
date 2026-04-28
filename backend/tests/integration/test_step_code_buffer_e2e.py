"""E2E integration test for StepCodeBuffer in runs.py context.

Tests VAL-03: Complete incremental code generation pipeline works end-to-end
using mock agent/LLM. Validates StepCodeBuffer lifecycle as wired in runs.py:
1. Create buffer before on_step closure
2. Call append_step_async with real action_dicts
3. Call assemble with precondition_config + assertions_config
4. Write output to tmp_path (simulating code generation block)
5. Read back and verify with ast.parse
"""

import ast
from pathlib import Path

import pytest

from backend.core.step_code_buffer import StepCodeBuffer


class MockDOMElement:
    """Simulates browser-use DOMInteractedElement for testing.

    Mirrors the key attributes: x_path, node_name, attributes, ax_name.
    Does not depend on browser-use internal types.
    """

    def __init__(
        self,
        x_path: str = "/html/body/div",
        node_name: str = "DIV",
        attributes: dict | None = None,
        ax_name: str | None = None,
    ):
        self.x_path = x_path
        self.node_name = node_name
        self.attributes = attributes
        self.ax_name = ax_name


# --- Action dict patterns (real format from browser-use model_actions) ---
# Format: {"action_type": {params}, "interacted_element": DOMElement | None}

NAVIGATE_ACTION = {
    "navigate": {"url": "https://erp.example.com"},
    "interacted_element": None,
}

CLICK_ACTION = {
    "click": {"index": 5},
    "interacted_element": MockDOMElement(
        x_path="/html/body/div[2]/form/button",
        node_name="BUTTON",
        attributes={"class": "submit", "type": "submit"},
    ),
}

INPUT_ACTION = {
    "input": {"index": 0, "text": "admin"},
    "interacted_element": MockDOMElement(
        x_path="/html/body/div[2]/form/input[1]",
        node_name="INPUT",
        attributes={"class": "username", "type": "text"},
    ),
}


class TestStepCodeBufferE2E:
    """E2E integration tests for StepCodeBuffer in runs.py context."""

    @pytest.mark.asyncio
    async def test_multi_step_accumulation(self):
        """Multi-step buffer accumulation produces valid code with all actions.

        Simulates: buffer created, navigate + click + input appended,
        assembled with precondition_config and assertions_config.
        Verifies output contains page.goto, page.locator, page.fill
        and passes ast.parse.
        """
        buffer = StepCodeBuffer(
            base_dir="outputs",
            run_id="run_test_multi",
            llm_config={},
        )

        # Step 1: Navigate
        await buffer.append_step_async(NAVIGATE_ACTION, duration=1.2)
        # Step 2: Input
        await buffer.append_step_async(INPUT_ACTION, duration=0.5)
        # Step 3: Click
        await buffer.append_step_async(CLICK_ACTION, duration=0.3)

        precondition_config = {"target_url": "https://erp.example.com"}
        assertions_config = [
            {"type": "text_visible", "expected": "Dashboard", "name": "assert_dashboard"},
        ]

        code = buffer.assemble(
            run_id="run_test_multi",
            task_name="Multi-step test",
            task_id="task_001",
            precondition_config=precondition_config,
            assertions_config=assertions_config,
        )

        # Verify all action types present in generated code
        assert "page.goto" in code, "Missing page.goto for navigate action"
        assert "page.locator" in code, "Missing page.locator for click/input actions"
        assert ".fill(" in code, "Missing .fill() for input action"
        assert ".click()" in code, "Missing .click() for click action"

        # Verify wait strategies present
        assert "wait_for_load_state" in code, "Missing wait_for_load_state for navigate"

        # Verify syntax validity
        ast.parse(code)

    @pytest.mark.asyncio
    async def test_assemble_writes_file(self, tmp_path: Path):
        """Buffer assemble writes valid .py file to tmp_path.

        Simulates the runs.py code generation block:
        1. Assemble content
        2. Create output dir under tmp_path
        3. Write assembled content
        4. Read back and verify file exists, passes ast.parse, contains def test_
        """
        buffer = StepCodeBuffer(
            base_dir="outputs",
            run_id="run_test_file",
            llm_config={},
        )

        await buffer.append_step_async(NAVIGATE_ACTION, duration=1.0)
        await buffer.append_step_async(INPUT_ACTION, duration=0.3)

        code = buffer.assemble(
            run_id="run_test_file",
            task_name="File write test",
            task_id="task_002",
        )

        # Simulate runs.py code generation block
        output_dir = tmp_path / "outputs" / "run_test_file" / "generated"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "test_run_test_file.py"
        output_path.write_text(code, encoding="utf-8")

        # Verify file exists on disk
        assert output_path.exists(), "Output file should exist on disk"

        # Read back and verify content
        content = output_path.read_text(encoding="utf-8")
        assert content == code, "Read-back content should match assembled code"

        # Verify syntax validity
        ast.parse(content)

        # Verify contains test function definition
        assert "def test_" in content, "Generated code should contain test function"

    @pytest.mark.asyncio
    async def test_empty_buffer_valid(self):
        """Empty buffer produces valid minimal test file.

        When no steps are appended, assemble() should still produce
        syntactically valid Python with a function def but no actions.
        """
        buffer = StepCodeBuffer(
            base_dir="outputs",
            run_id="run_test_empty",
            llm_config={},
        )

        # No steps appended
        code = buffer.assemble(
            run_id="run_test_empty",
            task_name="Empty test",
            task_id="task_003",
        )

        # Verify syntax validity -- even empty buffer should produce valid Python
        ast.parse(code)

        # Should contain a test function definition
        assert "def test_" in code, "Should contain function definition even with no steps"

    @pytest.mark.asyncio
    async def test_closure_captured_buffer(self):
        """Closure-captured buffer accumulates correctly (on_step pattern).

        Simulates the on_step callback pattern from runs.py:
        - Create buffer in outer scope
        - Define inner async function that captures buffer
        - Call inner function multiple times with different action_dicts
        - Verify buffer.records length matches call count
        """
        buffer = StepCodeBuffer(
            base_dir="outputs",
            run_id="run_test_closure",
            llm_config={},
        )

        # Simulate on_step closure capturing buffer
        async def on_step(action_dict: dict, duration: float | None = None):
            await buffer.append_step_async(action_dict, duration=duration)

        # Simulate 4 agent steps
        await on_step(NAVIGATE_ACTION, duration=1.5)
        await on_step(INPUT_ACTION, duration=0.4)
        await on_step(CLICK_ACTION, duration=0.2)
        await on_step(INPUT_ACTION, duration=0.6)

        # Verify accumulation
        assert len(buffer.records) == 4, (
            f"Expected 4 records after 4 on_step calls, got {len(buffer.records)}"
        )

        # Verify step indices are sequential
        indices = [r.step_index for r in buffer.records]
        assert indices == [0, 1, 2, 3], f"Expected sequential indices, got {indices}"

        # Verify assembled code passes ast.parse
        code = buffer.assemble(
            run_id="run_test_closure",
            task_name="Closure test",
            task_id="task_004",
        )
        ast.parse(code)

    @pytest.mark.asyncio
    async def test_full_precondition_assertions(self):
        """Generated code with precondition + assertions is syntactically valid.

        Appends navigate step, assembles with precondition_config and
        url_contains assertion. Verifies page.goto, wait_for_load_state,
        re.compile all present and ast.parse passes.
        """
        buffer = StepCodeBuffer(
            base_dir="outputs",
            run_id="run_test_prec",
            llm_config={},
        )

        await buffer.append_step_async(NAVIGATE_ACTION, duration=2.0)
        await buffer.append_step_async(CLICK_ACTION, duration=0.3)

        precondition_config = {"target_url": "https://erp.example.com/dashboard"}
        assertions_config = [
            {"type": "url_contains", "expected": "/dashboard", "name": "assert_url"},
        ]

        code = buffer.assemble(
            run_id="run_test_prec",
            task_name="Precondition test",
            task_id="task_005",
            precondition_config=precondition_config,
            assertions_config=assertions_config,
        )

        # Verify precondition injection
        assert "page.goto" in code, "Missing page.goto from precondition"
        assert "wait_for_load_state" in code, "Missing wait_for_load_state"

        # Verify assertion with re.compile for url_contains
        assert "re.compile" in code, "Missing re.compile for url_contains assertion"

        # Verify syntax validity
        ast.parse(code)
