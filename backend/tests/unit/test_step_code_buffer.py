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

