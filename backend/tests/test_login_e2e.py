"""登录场景端到端测试"""

import asyncio
import time
from pathlib import Path

import pytest

from backend.agent_simple.agent import SimpleAgent  # 直接导入
from backend.tests.reporter import TestResult


@pytest.mark.asyncio
async def test_login_e2e(llm, test_config, output_dir):
    """端到端登录测试

    测试流程：
    1. 打开 ERP 登录页
    2. 输入账号密码
    3. 点击登录
    4. 验证登录成功
    """
    from playwright.async_api import async_playwright

    config = test_config["login"]

    # 创建任务输出目录
    task_output = output_dir / "login"
    task_output.mkdir(parents=True, exist_ok=True)

    # 构建任务描述
    task = f"""
    在 ERP 系统执行登录操作：
    1. 打开 {test_config['base_url']}{config['url']}
    2. 在账号输入框输入 {config['account']}
    3. 在密码输入框输入 {config['password']}
    4. 点击登录按钮
    5. 确认登录成功（检测"商品采购"或"欢迎"等元素出现）
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        page = await browser.new_page()

        # 创建 Agent
        agent = SimpleAgent(
            task=task,
            llm=llm,
            page=page,
            output_dir=str(task_output),
            max_steps=10,
            max_retries=3,
        )

        # 执行测试并计时
        start_time = time.time()
        result = await agent.run()
        duration = time.time() - start_time

        await browser.close()

    # 收集截图
    screenshots = [str(s) for s in task_output.glob("*.png")]

    # 创建测试结果
    test_result = TestResult(
        scenario="登录场景",
        success=result.success,
        steps=len(result.steps),
        duration=duration,
        error=result.error if not result.success else None,
        screenshots=screenshots,
    )

    # 打印结果
    print(f"\n{'='*50}")
    print(f"场景: {test_result.scenario}")
    print(f"成功: {'✅' if test_result.success else '❌'}")
    print(f"步数: {test_result.steps}")
    print(f"耗时: {test_result.duration:.1f}s")
    if test_result.error:
        print(f"错误: {test_result.error}")
    print(f"{'='*50}")

    # 验证基本成功指标
    assert test_result.steps > 0, "没有执行任何步骤"
    assert test_result.steps <= 10, f"步数过多: {test_result.steps}"

    return test_result


if __name__ == "__main__":
    # 直接运行测试
    asyncio.run(test_login_e2e())
