"""Browser-Use 登录测试

使用阿里云 Qwen 3.5 Plus 进行 ERP 登录自动化测试。
"""

import os

import pytest
from browser_use import Agent, ChatOpenAI


@pytest.fixture
def llm():
    """初始化 LLM (阿里云 Qwen 3.5 Plus)"""
    return ChatOpenAI(
        model="qwen3.5-plus",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )


@pytest.fixture
def erp_config():
    """ERP 配置"""
    return {
        "base_url": os.getenv("ERP_BASE_URL", "https://erptest.epbox.cn").strip(),
        "username": os.getenv("ERP_USERNAME", ""),
        "password": os.getenv("ERP_PASSWORD", ""),
    }


@pytest.mark.asyncio
async def test_browser_navigation(llm, erp_config):
    """测试浏览器基本导航

    验证 browser-use + Qwen 3.5 Plus 能正常启动和导航。
    """
    task = f"打开 {erp_config['base_url']}/login 并告诉我页面的标题。"

    agent = Agent(task=task, llm=llm, use_vision=True)
    result = await agent.run()

    assert result.is_done(), "导航任务未完成"
    assert result.is_successful(), "导航任务失败"


@pytest.mark.asyncio
async def test_erp_login(llm, erp_config):
    """测试 ERP 登录

    使用 browser-use + Qwen 3.5 Plus 自动完成登录流程。
    """
    task = f"""
    登录 ERP 系统：
    1. 打开 {erp_config['base_url']}/login
    2. 切换到密码登录（如果需要）
    3. 输入用户名：{erp_config['username']}
    4. 输入密码：{erp_config['password']}
    5. 点击登录
    6. 确认登录成功
    """

    agent = Agent(task=task, llm=llm, use_vision=True)
    result = await agent.run()

    assert result.is_done(), "登录任务未完成"
    assert result.is_successful(), "登录任务失败"
