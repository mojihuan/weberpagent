"""CodeReviewer 单元测试"""

import pytest
from backend.agent_simple.form_filler.code_reviewer import CodeReviewer
from backend.agent_simple.types import InteractiveElement


@pytest.fixture
def reviewer():
    return CodeReviewer()


@pytest.fixture
def sample_elements():
    return [
        InteractiveElement(index=0, tag="INPUT", placeholder="姓名"),
        InteractiveElement(index=1, tag="INPUT", placeholder="手机号"),
        InteractiveElement(index=2, tag="BUTTON", text="提交"),
    ]


def test_review_safe_code(reviewer, sample_elements):
    """测试审查安全代码"""
    code = '''
async def fill_form(page):
    await page.get_by_placeholder("姓名").fill("张三")
    await page.get_by_placeholder("手机号").fill("13812345678")
    await page.get_by_role("button", name="提交").click()
'''
    result = reviewer.review(code, sample_elements)
    assert result.approved is True


def test_review_dangerous_code(reviewer, sample_elements):
    """测试审查危险代码"""
    code = '''
async def fill_form(page):
    import os
    os.system("rm -rf /")
'''
    result = reviewer.review(code, sample_elements)
    assert result.approved is False
    assert any(i.severity == "CRITICAL" for i in result.issues)


def test_review_syntax_error(reviewer, sample_elements):
    """测试审查语法错误"""
    code = "this is not valid python"
    result = reviewer.review(code, sample_elements)
    assert result.approved is False
    assert any(i.severity == "HIGH" for i in result.issues)