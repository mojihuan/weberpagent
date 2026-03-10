"""记忆模块集成测试"""

from backend.agent_simple.memory import Memory
from backend.agent_simple.types import Step, Action, ActionResult, PageState


def test_memory_integration():
    """测试记忆模块在模拟流程中的表现"""
    memory = Memory(max_steps=5)

    # 模拟登录流程
    steps = [
        Step(
            step_num=1,
            state=PageState(screenshot_base64="", url="https://example.com/login", title="登录"),
            action=Action(thought="点击登录", action="click", target="登录", done=False),
            result=ActionResult(success=True),
        ),
        Step(
            step_num=2,
            state=PageState(screenshot_base64="", url="https://example.com/login", title="登录"),
            action=Action(thought="输入账号", action="input", target="账号", value="test", done=False),
            result=ActionResult(success=False, error="元素未找到"),
        ),
        Step(
            step_num=3,
            state=PageState(screenshot_base64="", url="https://example.com/login", title="登录"),
            action=Action(thought="用 ID 输入账号", action="input", target="account", value="test", done=False),
            result=ActionResult(success=True),
        ),
    ]

    for step in steps:
        memory.add_step(step)

    # 打印格式化的记忆
    print("\n" + "=" * 60)
    print("记忆上下文输出:")
    print("=" * 60)
    print(memory.format_for_prompt())
    print("=" * 60)

    # 验证
    assert len(memory.steps) == 3
    assert len(memory.get_failed_actions()) == 1

    failed_actions = memory.get_failed_actions()
    assert failed_actions[0][0].target == "账号"
    assert "元素未找到" in failed_actions[0][1]

    print("\n✅ 集成测试通过!")


if __name__ == "__main__":
    test_memory_integration()
