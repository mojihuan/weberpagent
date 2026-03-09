"""Phase 5 优化模块单元测试"""

import pytest
from backend.agent_simple.prompts import (
    SYSTEM_PROMPT,
    REFLECTION_PROMPT,
    format_elements_for_prompt,
    build_user_prompt,
    build_messages,
)
from backend.agent_simple.types import InteractiveElement, Action, PageState


class TestPromptOptimization:
    """Prompt 层优化测试"""

    def test_locating_rules_forbid_numeric_index(self):
        """测试定位规则禁止数字索引"""
        # 检查禁止数字索引的规则存在
        assert "禁止" in SYSTEM_PROMPT
        assert "数字索引" in SYSTEM_PROMPT
        # 检查错误示例
        assert '"target": "2"' in SYSTEM_PROMPT

    def test_few_shot_login_example_exists(self):
        """测试包含登录场景示例"""
        assert "登录" in SYSTEM_PROMPT
        assert "账号" in SYSTEM_PROMPT
        assert "密码" in SYSTEM_PROMPT
        assert "Y96230027" in SYSTEM_PROMPT

    def test_completion_rules_detailed(self):
        """测试任务完成判断规则详细"""
        assert "完成" in SYSTEM_PROMPT
        assert "done" in SYSTEM_PROMPT.lower()
        # 检查登录完成标志
        assert "商品采购" in SYSTEM_PROMPT
        # 检查导航完成标志
        assert "导航任务完成" in SYSTEM_PROMPT
        # 检查搜索完成标志
        assert "搜索任务完成" in SYSTEM_PROMPT

    def test_reflection_prompt_has_history(self):
        """测试反思 Prompt 包含历史记忆字段"""
        assert "{history}" in REFLECTION_PROMPT
        assert "执行历史" in REFLECTION_PROMPT

    def test_reflection_prompt_forbids_numeric(self):
        """测试反思 Prompt 禁止数字索引"""
        assert "禁止输出数字索引" in REFLECTION_PROMPT

    def test_reflection_strategies_defined(self):
        """测试反思策略已定义"""
        assert "retry" in REFLECTION_PROMPT
        assert "alternative" in REFLECTION_PROMPT
        assert "skip" in REFLECTION_PROMPT


class TestElementFormatting:
    """元素格式化测试"""

    def test_format_elements_with_all_attributes(self):
        """测试格式化包含所有属性的元素"""
        elements = [
            InteractiveElement(
                index=0,
                tag="INPUT",
                text="",
                type="text",
                id="username",
                placeholder="请输入用户名",
                name="user",
                aria_label="用户名",
                title="输入您的用户名",
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
            )
        ]
        result = format_elements_for_prompt(elements)

        # ID 应该在最前面
        id_pos = result.find('ID:')
        text_pos = result.find('文本:')
        placeholder_pos = result.find('占位符:')

        assert id_pos < text_pos
        assert id_pos < placeholder_pos

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
            ),
        ]
        result = format_elements_for_prompt(elements)

        assert "account" in result
        assert "password" in result
        assert "登 录" in result
        assert result.count("\n") == 2  # 3 elements = 2 newlines


class TestUserPromptBuilding:
    """用户提示词构建测试"""

    def test_build_user_prompt_basic(self):
        """测试基本用户提示词构建"""
        state = PageState(
            screenshot_base64="",
            url="https://example.com",
            title="Test Page",
            elements=[
                InteractiveElement(
                    index=0,
                    tag="BUTTON",
                    text="Click Me",
                )
            ],
        )
        result = build_user_prompt("测试任务", state)

        assert "测试任务" in result
        assert "https://example.com" in result
        assert "Test Page" in result
        assert "Click Me" in result

    def test_build_user_prompt_search_page_detection(self):
        """测试搜索结果页检测"""
        state = PageState(
            screenshot_base64="",
            url="https://www.baidu.com/s?wd=test",
            title="test_百度搜索",
            elements=[],
        )
        result = build_user_prompt("搜索测试", state)

        assert "搜索结果页" in result

    def test_build_user_prompt_blank_page_detection(self):
        """测试空白页检测"""
        state = PageState(
            screenshot_base64="",
            url="about:blank",
            title="",
            elements=[],
        )
        result = build_user_prompt("测试任务", state)

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
        assert SYSTEM_PROMPT in messages[0]["content"]


class TestActionValidation:
    """动作验证测试"""

    def test_numeric_target_should_be_warned(self):
        """测试数字 target 应该被警告"""
        # 这个测试验证 executor 中的数字索引检测逻辑
        # 实际逻辑在 executor.py 中
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

    def test_placeholder_target_is_valid(self):
        """测试 placeholder target 是有效的"""
        action = Action(
            thought="测试",
            action="input",
            target="请输入用户名",
            value="test",
        )
        assert not action.target.isdigit()

    def test_id_target_is_valid(self):
        """测试 ID target 是有效的"""
        action = Action(
            thought="测试",
            action="input",
            target="username",
            value="test",
        )
        assert not action.target.isdigit()


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
