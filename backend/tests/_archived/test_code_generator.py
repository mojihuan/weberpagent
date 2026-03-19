"""CodeGenerator 单元测试"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.agent_simple.form_filler.code_generator import CodeGenerator
from backend.agent_simple.types import InteractiveElement, PageState


@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.chat_with_vision = AsyncMock()
    llm.model_name = "test-model"
    return llm


@pytest.fixture
def sample_state():
    return PageState(
        screenshot_base64="fake_base64",
        url="https://example.com/form",
        title="测试表单",
        elements=[
            InteractiveElement(index=0, tag="INPUT", placeholder="请输入姓名", type="text"),
            InteractiveElement(index=1, tag="INPUT", placeholder="请输入手机号", type="tel"),
            InteractiveElement(index=2, tag="BUTTON", text="提交"),
        ],
    )


@pytest.mark.asyncio
async def test_generate_code(mock_llm, sample_state):
    """测试代码生成"""
    mock_llm.chat_with_vision.return_value = MagicMock(
        content='''```json
{
  "code": "async def fill_form(page):\\n    await page.get_by_placeholder(\\"请输入姓名\\").fill(\\"张三\\")\\n    await page.get_by_placeholder(\\"请输入手机号\\").fill(\\"13812345678\\")\\n    await page.get_by_role(\\"button\\", name=\\"提交\\").click()",
  "description": "填写表单",
  "field_values": {"姓名": "张三", "手机号": "13812345678"}
}
```'''
    )

    generator = CodeGenerator(mock_llm)
    result = await generator.generate(sample_state, "填写测试表单")

    assert result.code is not None
    assert "fill_form" in result.code
    assert "张三" in result.code


@pytest.mark.asyncio
async def test_extract_code_from_block(mock_llm):
    """测试代码块提取"""
    generator = CodeGenerator(mock_llm)

    response = '''这是一些文本
```python
async def fill_form(page):
    pass
```
更多文本'''

    code = generator._extract_code(response)
    assert "async def fill_form" in code


@pytest.mark.asyncio
async def test_extract_field_values(mock_llm):
    """测试字段值提取"""
    generator = CodeGenerator(mock_llm)

    response = '''# FIELD_VALUES: {"name": "张三", "phone": "13812345678"}'''

    values = generator._extract_field_values(response)
    assert values["name"] == "张三"
    assert values["phone"] == "13812345678"