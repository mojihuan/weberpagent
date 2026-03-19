"""Memory 模块单元测试"""

import pytest
from backend.agent_simple.memory import Memory
from backend.agent_simple.types import (
    Action,
    ActionResult,
    PageState,
    Step,
)


def make_step(step_num: int, action: str, target: str, success: bool, error: str = None) -> Step:
    """创建测试用 Step 对象"""
    return Step(
        step_num=step_num,
        state=PageState(
            screenshot_base64="test",
            url="https://example.com",
            title="Test Page",
        ),
        action=Action(
            thought=f"执行 {action}",
            action=action,
            target=target,
            value=None,
            done=False,
        ),
        result=ActionResult(
            success=success,
            error=error,
        ),
    )


class TestMemoryAddStep:
    """测试 add_step 方法"""

    def test_add_step_empty(self):
        """测试向空记忆添加步骤"""
        memory = Memory(max_steps=5)
        step = make_step(1, "click", "登录", True)

        memory.add_step(step)

        assert len(memory.steps) == 1
        assert memory.steps[0] == step

    def test_add_step_respects_max_steps(self):
        """测试容量限制：超过 max_steps 时移除最旧的"""
        memory = Memory(max_steps=3)

        for i in range(1, 6):
            memory.add_step(make_step(i, "click", f"按钮{i}", True))

        assert len(memory.steps) == 3
        assert memory.steps[0].step_num == 3  # 最旧的是第 3 步
        assert memory.steps[-1].step_num == 5  # 最新的是第 5 步


class TestMemoryGetFailedActions:
    """测试 get_failed_actions 方法"""

    def test_get_failed_actions_empty(self):
        """测试空记忆返回空列表"""
        memory = Memory()
        assert memory.get_failed_actions() == []

    def test_get_failed_actions_filters_success(self):
        """测试过滤成功动作"""
        memory = Memory()
        memory.add_step(make_step(1, "click", "登录", True))
        memory.add_step(make_step(2, "input", "账号", False, "元素未找到"))
        memory.add_step(make_step(3, "click", "提交", True))

        failed = memory.get_failed_actions()

        assert len(failed) == 1
        action, error = failed[0]
        assert action.action == "input"
        assert action.target == "账号"
        assert error == "元素未找到"

    def test_get_failed_actions_multiple(self):
        """测试多个失败动作"""
        memory = Memory()
        memory.add_step(make_step(1, "click", "A", False, "错误1"))
        memory.add_step(make_step(2, "input", "B", False, "错误2"))

        failed = memory.get_failed_actions()

        assert len(failed) == 2


class TestMemoryFormatForPrompt:
    """测试 format_for_prompt 方法"""

    def test_format_empty_memory(self):
        """测试空记忆的输出"""
        memory = Memory()
        result = memory.format_for_prompt()

        assert "这是第一步" in result

    def test_format_with_steps(self):
        """测试有步骤时的输出格式"""
        memory = Memory()
        memory.add_step(make_step(1, "click", "登录", True))
        memory.add_step(make_step(2, "input", "账号", False, "元素未找到"))

        result = memory.format_for_prompt()

        # 检查操作记录
        assert "Step 1" in result
        assert "click" in result
        assert "登录" in result
        assert "✅" in result

        # 检查失败警告
        assert "⚠️" in result or "失败" in result
        assert "元素未找到" in result

    def test_format_includes_suggestions(self):
        """测试失败动作包含替代建议"""
        memory = Memory()
        memory.add_step(make_step(1, "input", "账号", False, "元素未找到"))

        result = memory.format_for_prompt()

        assert "建议" in result or "ID" in result or "placeholder" in result
