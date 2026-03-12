"""FormFiller Orchestrator 单元测试"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from backend.agent_simple.form_filler.orchestrator import FormFiller
from backend.agent_simple.types import PageState, InteractiveElement
from backend.agent_simple.form_filler.types import GeneratedCode, ReviewResult


@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.chat_with_vision = AsyncMock()
    llm.model_name = "test-model"
    return llm


@pytest.fixture
def mock_page():
    page = MagicMock()
    page.url = "https://example.com/form"
    return page


@pytest.fixture
def sample_state():
    return PageState(
        screenshot_base64="fake_base64",
        url="https://example.com/form",
        title="测试表单",
        elements=[InteractiveElement(index=0, tag="INPUT", placeholder="姓名")],
    )


@pytest.mark.asyncio
async def test_fill_form_success(mock_llm, mock_page, sample_state):
    """测试表单填写成功流程"""
    with patch.object(FormFiller, '_execute_code', return_value={"success": True, "stdout": ""}):
        # Mock 代码生成
        with patch('backend.agent_simple.form_filler.orchestrator.CodeGenerator') as MockGenerator:
            mock_generator = MockGenerator.return_value
            mock_generator.generate = AsyncMock(return_value=GeneratedCode(
                code='async def fill_form(page): pass',
                description="test",
                field_values={}
            ))

            # Mock 代码审查
            with patch('backend.agent_simple.form_filler.orchestrator.CodeReviewer') as MockReviewer:
                mock_reviewer = MockReviewer.return_value
                mock_reviewer.review = AsyncMock(return_value=ReviewResult(
                    approved=True, issues=[], suggestions=[]
                ))

                filler = FormFiller(mock_page, llm=mock_llm)
                result = await filler.fill_form(sample_state, "填写表单")

                assert result.success is True


@pytest.mark.asyncio
async def test_fill_form_generation_failure(mock_llm, mock_page, sample_state):
    """测试代码生成失败场景"""
    with patch('backend.agent_simple.form_filler.orchestrator.CodeGenerator') as MockGenerator:
        mock_generator = MockGenerator.return_value
        mock_generator.generate = AsyncMock(side_effect=Exception("LLM error"))

        filler = FormFiller(mock_page, llm=mock_llm)
        result = await filler.fill_form(sample_state, "填写表单")

        assert result.success is False
        assert "代码生成失败" in result.error


@pytest.mark.asyncio
async def test_fill_form_review_with_optimization(mock_llm, mock_page, sample_state):
    """测试审查未通过后优化场景"""
    with patch.object(FormFiller, '_execute_code', return_value={"success": True, "stdout": ""}):
        with patch('backend.agent_simple.form_filler.orchestrator.CodeGenerator') as MockGenerator:
            mock_generator = MockGenerator.return_value
            mock_generator.generate = AsyncMock(return_value=GeneratedCode(
                code='async def fill_form(page): pass',
                description="test",
                field_values={}
            ))

            with patch('backend.agent_simple.form_filler.orchestrator.CodeReviewer') as MockReviewer:
                mock_reviewer = MockReviewer.return_value
                # 第一次审查失败，第二次通过
                mock_reviewer.review = AsyncMock(side_effect=[
                    ReviewResult(approved=False, issues=[], suggestions=["需要优化"]),
                    ReviewResult(approved=True, issues=[], suggestions=[]),
                ])

                with patch('backend.agent_simple.form_filler.orchestrator.CodeOptimizer') as MockOptimizer:
                    mock_optimizer = MockOptimizer.return_value
                    mock_optimizer.optimize = AsyncMock(return_value='async def fill_form(page): await page.fill("input", "value")')

                    filler = FormFiller(mock_page, llm=mock_llm)
                    result = await filler.fill_form(sample_state, "填写表单")

                    assert result.success is True


@pytest.mark.asyncio
async def test_fill_form_execution_failure_with_retry(mock_llm, mock_page, sample_state):
    """测试执行失败后优化重试场景"""
    with patch('backend.agent_simple.form_filler.orchestrator.CodeGenerator') as MockGenerator:
        mock_generator = MockGenerator.return_value
        mock_generator.generate = AsyncMock(return_value=GeneratedCode(
            code='async def fill_form(page): pass',
            description="test",
            field_values={}
        ))

        with patch('backend.agent_simple.form_filler.orchestrator.CodeReviewer') as MockReviewer:
            mock_reviewer = MockReviewer.return_value
            mock_reviewer.review = AsyncMock(return_value=ReviewResult(
                approved=True, issues=[], suggestions=[]
            ))

            with patch('backend.agent_simple.form_filler.orchestrator.CodeOptimizer') as MockOptimizer:
                mock_optimizer = MockOptimizer.return_value
                mock_optimizer.optimize = AsyncMock(return_value='async def fill_form(page): await page.fill("input", "value")')

                # 模拟第一次执行失败，第二次成功
                call_count = [0]

                async def mock_execute(code):
                    call_count[0] += 1
                    if call_count[0] == 1:
                        raise Exception("Element not found")
                    return {"success": True, "stdout": ""}

                with patch.object(FormFiller, '_execute_code', side_effect=mock_execute):
                    filler = FormFiller(mock_page, llm=mock_llm)
                    result = await filler.fill_form(sample_state, "填写表单")

                    assert result.success is True


@pytest.mark.asyncio
async def test_fill_form_execution_failure_final(mock_llm, mock_page, sample_state):
    """测试执行失败最终失败场景"""
    with patch('backend.agent_simple.form_filler.orchestrator.CodeGenerator') as MockGenerator:
        mock_generator = MockGenerator.return_value
        mock_generator.generate = AsyncMock(return_value=GeneratedCode(
            code='async def fill_form(page): pass',
            description="test",
            field_values={}
        ))

        with patch('backend.agent_simple.form_filler.orchestrator.CodeReviewer') as MockReviewer:
            mock_reviewer = MockReviewer.return_value
            mock_reviewer.review = AsyncMock(return_value=ReviewResult(
                approved=True, issues=[], suggestions=[]
            ))

            with patch('backend.agent_simple.form_filler.orchestrator.CodeOptimizer') as MockOptimizer:
                mock_optimizer = MockOptimizer.return_value
                mock_optimizer.optimize = AsyncMock(return_value='async def fill_form(page): pass')

                # 两次执行都失败
                async def mock_execute(code):
                    raise Exception("Timeout")

                with patch.object(FormFiller, '_execute_code', side_effect=mock_execute):
                    filler = FormFiller(mock_page, llm=mock_llm)
                    result = await filler.fill_form(sample_state, "填写表单")

                    assert result.success is False
                    assert "执行失败" in result.error