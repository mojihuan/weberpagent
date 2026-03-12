"""Browser-Use 登录测试

使用官方 OpenAI GPT-4o 进行 ERP 登录自动化测试。
"""

import pytest
from browser_use import Agent
from langchain_openai import ChatOpenAI


@pytest.mark.asyncio
async def test_login_with_browser_use(erp_config):
    """测试 ERP 登录场景

    使用 browser-use + GPT-4o 自动完成登录流程。
    """
    # 1. 初始化 LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.1,
    )

    # 2. 定义登录任务
    task = f"""
    登录 ERP 系统，步骤如下：

    1. 打开登录页面：{erp_config['base_url']}/login
    2. 如果显示手机验证码登录，点击切换到"密码登录"
    3. 输入用户名：{erp_config['username']}
    4. 输入密码：{erp_config['password']}
    5. 点击登录按钮
    6. 确认登录成功（页面跳转到首页或显示欢迎信息）

    注意：
    - 如果有弹窗，先关闭弹窗
    - 如果登录失败，检查错误信息并重试
    """

    # 3. 创建 Agent
    agent = Agent(
        task=task,
        llm=llm,
        use_vision=True,
        max_actions_per_step=5,
    )

    # 4. 执行任务
    result = await agent.run()

    # 5. 验证结果
    assert result.is_done, "登录任务未完成"
    assert result.success, f"登录失败: {result.final_result}"


@pytest.mark.asyncio
async def test_login_with_screenshot(erp_config, tmp_path):
    """测试登录并保存截图

    每一步都保存截图用于调试。
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

    task = f"""
    登录 ERP 系统：
    1. 打开 {erp_config['base_url']}/login
    2. 切换到密码登录
    3. 输入用户名：{erp_config['username']}
    4. 输入密码：{erp_config['password']}
    5. 点击登录
    """

    agent = Agent(
        task=task,
        llm=llm,
        use_vision=True,
        save_conversation_path=str(tmp_path / "conversation"),
    )

    result = await agent.run()

    # 验证截图已保存
    conversation_dir = tmp_path / "conversation"
    if conversation_dir.exists():
        screenshots = list(conversation_dir.glob("*.png"))
        assert len(screenshots) > 0, "没有保存截图"

    assert result.is_done, "登录任务未完成"
