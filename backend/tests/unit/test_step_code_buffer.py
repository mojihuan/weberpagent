"""StepCodeBuffer 单元测试 -- VAL-01 同步翻译、wait 推导、assemble 组装。"""

import ast
from unittest.mock import MagicMock

import pytest

from backend.core.action_translator import TranslatedAction
from backend.core.code_generator import PlaywrightCodeGenerator
from backend.core.step_code_buffer import StepCodeBuffer, StepRecord


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def buffer():
    """返回 StepCodeBuffer() 实例。"""
    return StepCodeBuffer()


@pytest.fixture
def mock_elem():
    """模拟 interacted_element，具有 attributes/node_name/x_path/ax_name 属性。"""
    elem = MagicMock()
    elem.attributes = {}
    elem.node_name = "BUTTON"
    elem.x_path = "//button[@id='submit']"
    elem.ax_name = "提交"
    return elem


@pytest.fixture
def click_action(mock_elem):
    """click 操作字典。"""
    return {"click": {"index": 5}, "interacted_element": mock_elem}


@pytest.fixture
def navigate_action():
    """navigate 操作字典。"""
    return {"navigate": {"url": "https://example.com"}}


@pytest.fixture
def input_action(mock_elem):
    """input 操作字典。"""
    return {"input": {"text": "hello", "index": 3}, "interacted_element": mock_elem}


@pytest.fixture
def scroll_action():
    """scroll 操作字典。"""
    return {"scroll": {"direction": "down", "amount": 500}}


# ---------------------------------------------------------------------------
# append_step 同步翻译测试
# ---------------------------------------------------------------------------

class TestAppendStep:
    """append_step 同步翻译测试。"""

    def test_append_step_sync(self, buffer, click_action):
        """append_step(click_action) 后 records 长度 1，record 是 StepRecord 实例。"""
        buffer.append_step(click_action)
        records = buffer.records
        assert len(records) == 1
        record = records[0]
        assert isinstance(record, StepRecord)
        assert record.step_index == 0
        assert isinstance(record.action, TranslatedAction)
        assert record.action.code != ""

    def test_append_step_increments_index(self, buffer, click_action):
        """连续 3 次 append_step，step_index 分别为 0, 1, 2。"""
        buffer.append_step(click_action)
        buffer.append_step(click_action)
        buffer.append_step(click_action)
        records = buffer.records
        assert len(records) == 3
        assert records[0].step_index == 0
        assert records[1].step_index == 1
        assert records[2].step_index == 2

    def test_append_multiple_steps(self, buffer, click_action):
        """3 次 append_step 后 _records 长度为 3。"""
        buffer.append_step(click_action)
        buffer.append_step(click_action)
        buffer.append_step(click_action)
        assert len(buffer.records) == 3

    def test_append_step_navigate_generates_wait(self, buffer, navigate_action):
        """navigate 操作的 record.wait_before 包含 wait_for_load_state。"""
        buffer.append_step(navigate_action)
        record = buffer.records[0]
        assert "wait_for_load_state" in record.wait_before


# ---------------------------------------------------------------------------
# _derive_wait 策略测试
# ---------------------------------------------------------------------------

class TestDeriveWait:
    """_derive_wait 三种等待策略测试。"""

    def test_derive_wait_navigate(self, buffer):
        """navigate 返回 wait_for_load_state("networkidle")。"""
        result = buffer._derive_wait("navigate", None)
        assert result == '    page.wait_for_load_state("networkidle")'

    def test_derive_wait_click(self, buffer):
        """click + duration=None 返回 wait_for_timeout(300)。"""
        result = buffer._derive_wait("click", None)
        assert result == '    page.wait_for_timeout(300)'

    def test_derive_wait_long_duration(self, buffer):
        """input + duration=1.5 (>0.8) 返回 wait_for_timeout(1500)。"""
        result = buffer._derive_wait("input", 1.5)
        assert result == '    page.wait_for_timeout(1500)'

    def test_derive_wait_no_wait(self, buffer):
        """scroll + duration=0.3 (<0.8) 返回空字符串。"""
        result = buffer._derive_wait("scroll", 0.3)
        assert result == ""

    def test_derive_wait_navigate_ignores_duration(self, buffer):
        """navigate + duration=2.0 仍然返回 wait_for_load_state（优先级最高）。"""
        result = buffer._derive_wait("navigate", 2.0)
        assert result == '    page.wait_for_load_state("networkidle")'


# ---------------------------------------------------------------------------
# assemble 组装测试
# ---------------------------------------------------------------------------

class TestAssemble:
    """assemble 委托 PlaywrightCodeGenerator.generate() 组装测试。"""

    def test_assemble_complete(self, buffer, navigate_action, click_action, input_action):
        """3 个不同类型步骤后 assemble 返回包含 'def test_' 的字符串，ast.parse 通过。"""
        buffer.append_step(navigate_action)
        buffer.append_step(click_action)
        buffer.append_step(input_action)
        result = buffer.assemble("run1", "测试任务", "task1")
        assert "def test_" in result
        ast.parse(result)  # 不抛异常即通过

    def test_assemble_empty_buffer(self, buffer):
        """空 buffer 的 assemble 返回 ast.parse 合法的 Python。"""
        result = buffer.assemble("run1", "空任务", "task1")
        ast.parse(result)  # 不抛异常即通过

    def test_assemble_includes_waits(self, buffer, navigate_action):
        """navigate 步骤后 assemble 返回的代码包含 wait_for_load_state。"""
        buffer.append_step(navigate_action)
        result = buffer.assemble("run1", "导航任务", "task1")
        assert "wait_for_load_state" in result

    def test_assemble_syntax_valid(self, buffer, navigate_action, click_action, input_action):
        """多步骤 assemble 结果通过 PlaywrightCodeGenerator.validate_syntax()。"""
        buffer.append_step(navigate_action)
        buffer.append_step(click_action)
        buffer.append_step(input_action)
        result = buffer.assemble("run1", "语法验证", "task1")
        generator = PlaywrightCodeGenerator()
        assert generator.validate_syntax(result) is True


# ---------------------------------------------------------------------------
# 不可变性测试
# ---------------------------------------------------------------------------

class TestImmutability:
    """records 属性不可变性测试。"""

    def test_records_returns_copy(self, buffer, click_action):
        """buffer.records 的修改不影响内部 _records。"""
        buffer.append_step(click_action)
        records = buffer.records
        records.clear()
        # 清除副本后，内部 _records 仍然有 1 条
        assert len(buffer.records) == 1


# ---------------------------------------------------------------------------
# append_step_async 弱步骤修复测试 (Plan 02 -- CODEGEN-02, VAL-01)
# ---------------------------------------------------------------------------

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from backend.core.llm_healer import LLMHealResult


@pytest.fixture
def async_buffer(tmp_path):
    """返回 StepCodeBuffer 实例，配置 base_dir 和 run_id。"""
    from backend.core.step_code_buffer import StepCodeBuffer

    return StepCodeBuffer(
        base_dir=str(tmp_path),
        run_id="test_run",
        llm_config={"model": "test"},
    )


@pytest.fixture
def mock_elem_weak():
    """Mock elem 只有 1 个 locator（仅 x_path，无 ax_name/id/data-testid）。"""
    elem = MagicMock()
    elem.attributes = {}
    elem.node_name = "BUTTON"
    elem.x_path = "//button"
    elem.ax_name = None
    elem.placeholder = None
    return elem


@pytest.fixture
def mock_elem_strong():
    """Mock elem 有 2+ locator（x_path + ax_name + id）。"""
    elem = MagicMock()
    elem.attributes = {"id": "submit-btn"}
    elem.node_name = "BUTTON"
    elem.x_path = "//button[@id='submit-btn']"
    elem.ax_name = "提交"
    return elem


@pytest.fixture
def click_action_no_elem():
    """click 操作字典，interacted_element=None。"""
    return {"click": {"index": 5}, "interacted_element": None}


@pytest.fixture
def click_action_weak(mock_elem_weak):
    """click 操作字典，elem 只有 1 个 locator。"""
    return {"click": {"index": 5}, "interacted_element": mock_elem_weak}


@pytest.fixture
def click_action_strong(mock_elem_strong):
    """click 操作字典，elem 有 2+ locator。"""
    return {"click": {"index": 5}, "interacted_element": mock_elem_strong}


class TestAppendStepAsyncWeakHealing:
    """append_step_async 弱步骤修复测试。"""

    @pytest.mark.asyncio
    async def test_async_heals_weak_step_no_elem(self, async_buffer, click_action_no_elem, tmp_path):
        """elem=None → healer.heal() 被调用 → 成功修复后 record.action.code 包含 LLM 代码。"""
        # 创建 DOM 文件
        dom_dir = tmp_path / "test_run" / "dom"
        dom_dir.mkdir(parents=True)
        (dom_dir / "step_1.txt").write_text("<html>test</html>", encoding="utf-8")

        heal_result = LLMHealResult(
            success=True,
            code_snippet="    page.locator('.btn').click()",
            raw_response="",
            locator="page.locator('.btn')",
        )

        with patch(
            "backend.core.step_code_buffer.LLMHealer"
        ) as MockHealer:
            mock_healer_instance = MockHealer.return_value
            mock_healer_instance.heal = AsyncMock(return_value=heal_result)

            with patch.object(
                async_buffer._translator, "translate_with_llm",
                return_value=TranslatedAction(
                    code="    page.locator('.btn').click()",
                    action_type="click",
                    is_comment=False,
                    has_locator=True,
                ),
            ) as mock_translate_llm:
                await async_buffer.append_step_async(click_action_no_elem)

        mock_healer_instance.heal.assert_called_once()
        record = async_buffer.records[0]
        assert "page.locator('.btn')" in record.action.code

    @pytest.mark.asyncio
    async def test_async_heals_weak_step_single_locator(self, async_buffer, click_action_weak, tmp_path):
        """elem 有 1 个 locator → healer.heal() 被调用。"""
        dom_dir = tmp_path / "test_run" / "dom"
        dom_dir.mkdir(parents=True)
        (dom_dir / "step_1.txt").write_text("<html>test</html>", encoding="utf-8")

        heal_result = LLMHealResult(
            success=True,
            code_snippet="    page.locator('.btn').click()",
            raw_response="",
            locator="page.locator('.btn')",
        )

        with patch(
            "backend.core.step_code_buffer.LLMHealer"
        ) as MockHealer:
            mock_healer_instance = MockHealer.return_value
            mock_healer_instance.heal = AsyncMock(return_value=heal_result)

            with patch.object(
                async_buffer._translator, "translate_with_llm",
                return_value=TranslatedAction(
                    code="    page.locator('.btn').click()",
                    action_type="click",
                    is_comment=False,
                    has_locator=True,
                ),
            ):
                await async_buffer.append_step_async(click_action_weak)

        mock_healer_instance.heal.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_no_heal_strong_step(self, async_buffer, click_action_strong):
        """elem 有 2+ locator → healer.heal() 不被调用。"""
        with patch(
            "backend.core.step_code_buffer.LLMHealer"
        ) as MockHealer:
            mock_healer_instance = MockHealer.return_value
            mock_healer_instance.heal = AsyncMock()

            await async_buffer.append_step_async(click_action_strong)

        mock_healer_instance.heal.assert_not_called()
        record = async_buffer.records[0]
        # record.action 是 ActionTranslator 翻译的原始代码（非 LLM 代码）
        assert isinstance(record.action, TranslatedAction)
        assert record.action.code != ""

    @pytest.mark.asyncio
    async def test_async_reads_dom_snapshot(self, async_buffer, click_action_no_elem, tmp_path):
        """append_step_async 读取 DOM 文件，heal() 的 dom_snapshot 参数正确。"""
        dom_dir = tmp_path / "test_run" / "dom"
        dom_dir.mkdir(parents=True)
        (dom_dir / "step_1.txt").write_text("<html>test dom</html>", encoding="utf-8")

        heal_result = LLMHealResult(
            success=True,
            code_snippet="    page.locator('.btn').click()",
            raw_response="",
            locator="page.locator('.btn')",
        )

        with patch(
            "backend.core.step_code_buffer.LLMHealer"
        ) as MockHealer:
            mock_healer_instance = MockHealer.return_value
            mock_healer_instance.heal = AsyncMock(return_value=heal_result)

            with patch.object(
                async_buffer._translator, "translate_with_llm",
                return_value=TranslatedAction(
                    code="    page.locator('.btn').click()",
                    action_type="click",
                    is_comment=False,
                    has_locator=True,
                ),
            ):
                await async_buffer.append_step_async(click_action_no_elem)

        # 验证 heal 被调用时 dom_snapshot 参数正确
        call_args = mock_healer_instance.heal.call_args
        assert call_args[0][2] == "<html>test dom</html>"

    @pytest.mark.asyncio
    async def test_async_dom_missing_fallback(self, async_buffer, click_action_no_elem):
        """DOM 文件不存在 → healer.heal() 不被调用，使用原始翻译。"""
        with patch(
            "backend.core.step_code_buffer.LLMHealer"
        ) as MockHealer:
            mock_healer_instance = MockHealer.return_value
            mock_healer_instance.heal = AsyncMock()

            await async_buffer.append_step_async(click_action_no_elem)

        mock_healer_instance.heal.assert_not_called()
        record = async_buffer.records[0]
        assert isinstance(record.action, TranslatedAction)

    @pytest.mark.asyncio
    async def test_async_heal_failure_fallback(self, async_buffer, click_action_no_elem, tmp_path):
        """heal() 返回 LLMHealResult(success=False, ...) → 使用原始翻译。"""
        dom_dir = tmp_path / "test_run" / "dom"
        dom_dir.mkdir(parents=True)
        (dom_dir / "step_1.txt").write_text("<html>test</html>", encoding="utf-8")

        heal_result = LLMHealResult(
            success=False,
            code_snippet="",
            raw_response="error",
            locator="",
        )

        with patch(
            "backend.core.step_code_buffer.LLMHealer"
        ) as MockHealer:
            mock_healer_instance = MockHealer.return_value
            mock_healer_instance.heal = AsyncMock(return_value=heal_result)

            await async_buffer.append_step_async(click_action_no_elem)

        record = async_buffer.records[0]
        # 原始翻译结果（非 LLM 修复代码）
        assert isinstance(record.action, TranslatedAction)
        assert "page.locator('.btn')" not in record.action.code

    @pytest.mark.asyncio
    async def test_async_heal_exception_fallback(self, async_buffer, click_action_no_elem, tmp_path):
        """heal() 抛 RuntimeError → 使用原始翻译，不崩溃。"""
        dom_dir = tmp_path / "test_run" / "dom"
        dom_dir.mkdir(parents=True)
        (dom_dir / "step_1.txt").write_text("<html>test</html>", encoding="utf-8")

        with patch(
            "backend.core.step_code_buffer.LLMHealer"
        ) as MockHealer:
            mock_healer_instance = MockHealer.return_value
            mock_healer_instance.heal = AsyncMock(side_effect=RuntimeError("LLM timeout"))

            await async_buffer.append_step_async(click_action_no_elem)

        # 不崩溃，record 是原始翻译
        record = async_buffer.records[0]
        assert isinstance(record.action, TranslatedAction)

    @pytest.mark.asyncio
    async def test_async_non_click_input_skip(self, async_buffer, navigate_action):
        """navigate 操作 → healer.heal() 不被调用。"""
        with patch(
            "backend.core.step_code_buffer.LLMHealer"
        ) as MockHealer:
            mock_healer_instance = MockHealer.return_value
            mock_healer_instance.heal = AsyncMock()

            await async_buffer.append_step_async(navigate_action)

        mock_healer_instance.heal.assert_not_called()
        record = async_buffer.records[0]
        assert "goto" in record.action.code

    @pytest.mark.asyncio
    async def test_async_step_index_increments(self, async_buffer, click_action_strong):
        """多次 append_step_async → step_index 正确递增。"""
        await async_buffer.append_step_async(click_action_strong)
        await async_buffer.append_step_async(click_action_strong)
        await async_buffer.append_step_async(click_action_strong)

        records = async_buffer.records
        assert records[0].step_index == 0
        assert records[1].step_index == 1
        assert records[2].step_index == 2
