"""沙箱执行器单元测试"""

import pytest
from backend.agent_simple.form_filler.sandbox import execute_code


@pytest.mark.asyncio
async def test_execute_simple_code():
    """测试执行简单代码"""
    code = """
result = 1 + 1
"""
    result = await execute_code(code, {})
    assert result["success"] is True
    assert result["locals"]["result"] == 2


@pytest.mark.asyncio
async def test_execute_code_with_page_mock():
    """测试执行带有 page 参数的代码"""
    code = """
values = {"name": "test"}
"""
    # 模拟 page 对象
    mock_page = type("MockPage", (), {})()
    result = await execute_code(code, {"page": mock_page})
    assert result["success"] is True


@pytest.mark.asyncio
async def test_execute_invalid_code():
    """测试执行无效代码"""
    code = "this is not valid python"
    result = await execute_code(code, {})
    assert result["success"] is False
    assert "error" in result