"""CodeOptimizer 单元测试"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.agent_simple.form_filler.code_optimizer import CodeOptimizer
from backend.agent_simple.types import InteractiveElement
from backend.agent_simple.form_filler.types import ReviewIssue


@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.chat_with_vision = AsyncMock()
    llm.model_name = "test-model"
    return llm


@pytest.fixture
def sample_elements():
    return [
        InteractiveElement(index=0, tag="INPUT", placeholder="姓名"),
        InteractiveElement(index=1, tag="INPUT", placeholder="手机号"),
    ]


@pytest.mark.asyncio
async def test_optimize_with_issues(mock_llm, sample_elements):
    """测试根据审查问题优化代码"""
    mock_llm.chat_with_vision.return_value = MagicMock(
        content='''```python
async def fill_form(page):
    await page.get_by_placeholder("姓名").fill("张三")
    await page.get_by_placeholder("手机号").fill("13812345678")
```'''
    )

    optimizer = CodeOptimizer(mock_llm)
    issues = [ReviewIssue(severity="HIGH", line=1, message="测试问题")]

    result = await optimizer.optimize(
        code="original code",
        elements=sample_elements,
        issues=issues,
    )

    assert result is not None
    assert "fill_form" in result


@pytest.mark.asyncio
async def test_optimize_with_execution_error(mock_llm, sample_elements):
    """测试根据执行错误优化代码"""
    mock_llm.chat_with_vision.return_value = MagicMock(
        content='''```python
async def fill_form(page):
    await page.wait_for_timeout(1000)
    await page.get_by_placeholder("姓名").fill("张三")
```'''
    )

    optimizer = CodeOptimizer(mock_llm)
    result = await optimizer.optimize(
        code="original code",
        elements=sample_elements,
        execution_error="TimeoutError: locator.click",
    )

    assert "fill_form" in result


@pytest.mark.asyncio
async def test_no_optimization_needed(mock_llm, sample_elements):
    """测试无需优化时返回原代码"""
    optimizer = CodeOptimizer(mock_llm)
    result = await optimizer.optimize(
        code="async def fill_form(page): pass",
        elements=sample_elements,
    )

    assert result == "async def fill_form(page): pass"