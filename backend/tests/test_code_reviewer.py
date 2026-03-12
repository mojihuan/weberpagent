"""CodeReviewer 单元测试"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.agent_simple.form_filler.code_reviewer import CodeReviewer
from backend.agent_simple.types import InteractiveElement
from backend.llm.base import LLMResponse


@pytest.fixture
def reviewer():
    return CodeReviewer()


@pytest.fixture
def mock_llm():
    """创建模拟的 LLM 实例"""
    llm = MagicMock()
    llm.chat_with_vision = AsyncMock()
    return llm


@pytest.fixture
def sample_elements():
    return [
        InteractiveElement(index=0, tag="INPUT", placeholder="姓名"),
        InteractiveElement(index=1, tag="INPUT", placeholder="手机号"),
        InteractiveElement(index=2, tag="BUTTON", text="提交"),
    ]


@pytest.mark.asyncio
async def test_review_safe_code(reviewer, sample_elements):
    """测试审查安全代码"""
    code = '''
async def fill_form(page):
    await page.get_by_placeholder("姓名").fill("张三")
    await page.get_by_placeholder("手机号").fill("13812345678")
    await page.get_by_role("button", name="提交").click()
'''
    result = await reviewer.review(code, sample_elements)
    assert result.approved is True


@pytest.mark.asyncio
async def test_review_dangerous_code(reviewer, sample_elements):
    """测试审查危险代码"""
    code = '''
async def fill_form(page):
    import os
    os.system("rm -rf /")
'''
    result = await reviewer.review(code, sample_elements)
    assert result.approved is False
    assert any(i.severity == "CRITICAL" for i in result.issues)


@pytest.mark.asyncio
async def test_review_syntax_error(reviewer, sample_elements):
    """测试审查语法错误"""
    code = "this is not valid python"
    result = await reviewer.review(code, sample_elements)
    assert result.approved is False
    assert any(i.severity == "HIGH" for i in result.issues)


@pytest.mark.asyncio
async def test_llm_review_called_when_provided(mock_llm, sample_elements):
    """测试 LLM 审查被调用"""
    # 配置 mock LLM 返回审查结果
    mock_llm.chat_with_vision.return_value = LLMResponse(
        content='{"approved": true, "issues": [], "suggestions": ["建议1"]}',
        usage={}
    )

    reviewer = CodeReviewer(llm=mock_llm)
    code = '''
async def fill_form(page):
    await page.get_by_placeholder("姓名").fill("张三")
'''
    result = await reviewer.review(code, sample_elements)

    # 验证 LLM 被调用
    mock_llm.chat_with_vision.assert_called_once()
    assert "建议1" in result.suggestions


@pytest.mark.asyncio
async def test_llm_failure_does_not_crash(mock_llm, sample_elements):
    """测试 LLM 失败不会导致崩溃"""
    # 配置 mock LLM 抛出异常
    mock_llm.chat_with_vision.side_effect = Exception("LLM 服务不可用")

    reviewer = CodeReviewer(llm=mock_llm)
    code = '''
async def fill_form(page):
    await page.get_by_placeholder("姓名").fill("张三")
'''
    # 应该不抛出异常
    result = await reviewer.review(code, sample_elements)

    # 基础规则检查应该仍然工作
    assert result.approved is True


@pytest.mark.asyncio
async def test_llm_review_adds_issues(mock_llm, sample_elements):
    """测试 LLM 审查添加问题"""
    # 配置 mock LLM 返回带有问题的审查结果
    mock_llm.chat_with_vision.return_value = LLMResponse(
        content='''```json
{
    "approved": false,
    "issues": [
        {
            "severity": "HIGH",
            "line": 3,
            "message": "缺少错误处理"
        }
    ],
    "suggestions": ["建议添加 try-except"]
}
```''',
        usage={}
    )

    reviewer = CodeReviewer(llm=mock_llm)
    code = '''
async def fill_form(page):
    await page.get_by_placeholder("姓名").fill("张三")
'''
    result = await reviewer.review(code, sample_elements)

    # 验证 LLM 返回的问题被添加
    assert any(i.message == "缺少错误处理" for i in result.issues)
    assert "建议添加 try-except" in result.suggestions


@pytest.mark.asyncio
async def test_llm_review_with_invalid_json(mock_llm, sample_elements):
    """测试 LLM 返回无效 JSON 时的处理"""
    # 配置 mock LLM 返回无效 JSON
    mock_llm.chat_with_vision.return_value = LLMResponse(
        content='这不是有效的 JSON',
        usage={}
    )

    reviewer = CodeReviewer(llm=mock_llm)
    code = '''
async def fill_form(page):
    await page.get_by_placeholder("姓名").fill("张三")
'''
    # 应该不抛出异常
    result = await reviewer.review(code, sample_elements)

    # 基础规则检查应该仍然工作
    assert result.approved is True


@pytest.mark.asyncio
async def test_no_llm_backward_compatible(sample_elements):
    """测试不传入 LLM 时行为与之前相同"""
    reviewer = CodeReviewer()  # 不传入 LLM
    code = '''
async def fill_form(page):
    await page.get_by_placeholder("姓名").fill("张三")
    await page.get_by_placeholder("手机号").fill("13812345678")
    await page.get_by_role("button", name="提交").click()
'''
    result = await reviewer.review(code, sample_elements)
    assert result.approved is True
