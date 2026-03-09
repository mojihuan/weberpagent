"""新增采购单场景端到端测试"""

import asyncio
import time
from pathlib import Path

import pytest

from backend.agent_simple.agent import SimpleAgent  # 直接导入
from backend.tests.reporter import TestResult


@pytest.mark.asyncio
async def test_purchase_e2e(llm, test_config, output_dir):
    """端到端新增采购单测试

    测试流程：
    1. 登录 ERP 系统
    2. 导航到采购管理页面
    3. 点击新增采购单
    4. 填写表单
    5. 提交并验证
    """
    from playwright.async_api import async_playwright

    login_config = test_config["login"]
    purchase_config = test_config["purchase"]

    # 创建任务输出目录
    task_output = output_dir / "purchase"
    task_output.mkdir(parents=True, exist_ok=True)

    # 构建任务描述
    device_types = "、".join(purchase_config["device_types"])

    task = f"""
    在 ERP 系统完成新增采购单操作：
    1. 打开 {test_config['base_url']}
    2. 在账号输入框输入 {login_config['account']}
    3. 在密码输入框输入 {login_config['password']}
    4. 点击登录按钮
    5. 登录成功后，点击侧边栏"{purchase_config['navigation'][0]}"
    6. 点击"{purchase_config['navigation'][1]}"
    7. 点击"{purchase_config['navigation'][2]}"
    8. 点击"{purchase_config['add_button']}"按钮
    9. 选择设备类型（可选：{device_types}）
    10. 填写表单中的必填字段（根据页面实际情况填写，可以自由发挥）
    11. 点击提交或保存按钮
    12. 确认成功（检测按钮下方是否出现新记录）
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
            max_steps=25,  # 采购单流程较长，增加步数
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
        scenario="新增采购单",
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

    # 打印每一步详情
    print(f"\n执行步骤详情:")
    for step in result.steps:
        action = step.action
        print(f"  Step {step.step_num}: {action.action} -> {action.target or action.value or ''}")

    return test_result


if __name__ == "__main__":
    # 直接运行测试
    asyncio.run(test_purchase_e2e())
