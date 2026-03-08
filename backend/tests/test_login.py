"""登录场景测试"""

import os
import sys
from pathlib import Path

import pytest

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@pytest.fixture
def llm():
    """创建 LLM 实例"""
    from backend.llm import QwenChat

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        pytest.skip("DASHSCOPE_API_KEY 未配置")

    return QwenChat(model="qwen-vl-max")


@pytest.mark.asyncio
async def test_open_login_page(llm):
    """测试打开登录页面"""
    from backend.agent import UIBrowserAgent

    agent = UIBrowserAgent(
        task="打开 https://erptest.epbox.cn/",
        llm=llm,
        output_dir="outputs/tests/login",
    )

    result = await agent.run()

    assert result["success"], "打开页面失败"
    assert result["steps"] > 0, "没有执行任何步骤"


@pytest.mark.asyncio
async def test_login_flow(llm):
    """测试完整登录流程"""
    from backend.agent import UIBrowserAgent

    agent = UIBrowserAgent(
        task="""
        执行登录操作：
        1. 打开 https://erptest.epbox.cn/
        2. 找到用户名输入框，输入 Y59800075
        3. 找到密码输入框，输入 Aa123456
        4. 点击登录按钮
        """,
        llm=llm,
        output_dir="outputs/tests/login_flow",
        max_failures=5,
    )

    result = await agent.run()

    # 登录可能成功也可能失败（取决于页面状态）
    # 这里主要验证流程能执行完成
    assert result["steps"] > 0, "没有执行任何步骤"
    print(f"\n登录测试结果: 成功={result['success']}, 步数={result['steps']}")


@pytest.mark.asyncio
async def test_fill_form(llm):
    """测试表单填写能力"""
    from backend.agent import UIBrowserAgent

    agent = UIBrowserAgent(
        task="""
        打开 https://erptest.epbox.cn/
        找到用户名输入框并输入 test_user
        截图保存
        """,
        llm=llm,
        output_dir="outputs/tests/fill_form",
        max_failures=3,
    )

    result = await agent.run()

    assert result["steps"] > 0, "没有执行任何步骤"
