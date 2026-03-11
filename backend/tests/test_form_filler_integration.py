"""FormFiller 集成测试"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from backend.agent_simple.form_filler import FormFiller
from backend.agent_simple.types import PageState, InteractiveElement


@pytest.fixture
def mock_llm():
    """模拟 LLM"""
    llm = MagicMock()
    llm.model_name = "test-model"
    llm.chat_with_vision = AsyncMock()
    # 返回生成的代码
    llm.chat_with_vision.return_value = MagicMock(
        content='''```python
async def fill_form(page):
    await page.get_by_placeholder("姓名").fill("张三")
    await page.get_by_placeholder("手机号").fill("13812345678")
# FIELD_VALUES: {"姓名": "张三", "手机号": "13812345678"}
```'''
    )
    return llm


@pytest.fixture
def mock_page():
    """模拟 Playwright Page"""
    page = MagicMock()
    page.url = "https://example.com/form"
    page.title = AsyncMock(return_value="测试表单")
    page.wait_for_timeout = AsyncMock()
    page.get_by_placeholder = MagicMock()
    page.get_by_role = MagicMock()
    return page


@pytest.fixture
def sample_state():
    """示例页面状态"""
    return PageState(
        screenshot_base64="fake_base64",
        url="https://example.com/form",
        title="测试表单",
        elements=[
            InteractiveElement(index=0, tag="INPUT", placeholder="姓名"),
            InteractiveElement(index=1, tag="INPUT", placeholder="手机号"),
        ],
    )


@pytest.mark.asyncio
async def test_form_filler_full_flow(mock_llm, mock_page, sample_state):
    """测试完整表单填写流程"""
    # Mock sandbox 执行成功
    with patch('backend.agent_simple.form_filler.orchestrator.execute_code') as mock_exec:
        mock_exec.return_value = {"success": True, "locals": {}}

        filler = FormFiller(mock_llm, mock_page)
        result = await filler.fill_form(sample_state, "填写测试表单")

        assert result.success is True
        assert result.code is not None


@pytest.mark.asyncio
async def test_form_filler_with_retry(mock_llm, mock_page, sample_state):
    """测试执行失败后的重试"""
    call_count = 0

    def mock_execute(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {"success": False, "error": "Timeout"}
        return {"success": True, "locals": {}}

    with patch('backend.agent_simple.form_filler.orchestrator.execute_code', side_effect=mock_execute):
        filler = FormFiller(mock_llm, mock_page)
        result = await filler.fill_form(sample_state, "填写测试表单")

        # 应该重试成功
        assert result.success is True


@pytest.mark.asyncio
async def test_form_filler_generation_failure(mock_llm, mock_page, sample_state):
    """测试代码生成失败的情况"""
    mock_llm.chat_with_vision.side_effect = Exception("LLM API Error")

    filler = FormFiller(mock_llm, mock_page)
    result = await filler.fill_form(sample_state, "填写测试表单")

    assert result.success is False
    assert "代码生成失败" in result.error


@pytest.mark.asyncio
async def test_form_filler_execution_failure_with_retry(mock_llm, mock_page, sample_state):
    """测试执行失败且重试也失败的情况"""
    with patch('backend.agent_simple.form_filler.orchestrator.execute_code') as mock_exec:
        mock_exec.return_value = {"success": False, "error": "Element not found"}

        filler = FormFiller(mock_llm, mock_page)
        result = await filler.fill_form(sample_state, "填写测试表单")

        assert result.success is False
        assert "执行失败" in result.error