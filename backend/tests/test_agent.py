"""测试 SimpleAgent 完整流程"""

import asyncio
import os

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat


async def test_agent_baidu_search():
    """测试 Agent 执行百度搜索任务"""
    print("\n=== 测试 SimpleAgent - 百度搜索 ===\n")

    # 检查 API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("⚠️ DASHSCOPE_API_KEY 未配置，跳过测试")
        return

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 创建 Agent
        llm = QwenChat(model="qwen-vl-max")
        agent = SimpleAgent(
            task="在百度搜索 Python 教程，然后点击搜索按钮",
            llm=llm,
            page=page,
            max_steps=10,
            max_retries=2,
        )

        # 执行任务
        result = await agent.run()

        # 打印结果
        print(f"\n=== 执行结果 ===")
        print(f"成功: {result.success}")
        if result.result:
            print(f"结果: {result.result}")
        if result.error:
            print(f"错误: {result.error}")
        print(f"步数: {len(result.steps)}")

        # 打印每一步
        print(f"\n=== 执行步骤 ===")
        for step in result.steps:
            print(f"\nStep {step.step_num}:")
            print(f"  动作: {step.action.action}")
            print(f"  目标: {step.action.target}")
            print(f"  结果: {'成功' if step.result.success else '失败'}")

        await browser.close()

    print("\n✅ 测试完成")


async def test_agent_reflection():
    """测试 Agent 反思机制（模拟失败场景）"""
    print("\n=== 测试 SimpleAgent - 反思机制 ===\n")

    # 检查 API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("⚠️ DASHSCOPE_API_KEY 未配置，跳过测试")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 创建 Agent - 使用一个需要反思的任务
        llm = QwenChat(model="qwen-vl-max")
        agent = SimpleAgent(
            task="在百度首页点击一个不存在的按钮",
            llm=llm,
            page=page,
            max_steps=5,
            max_retries=2,
        )

        # 执行任务
        result = await agent.run()

        # 检查是否有反思记录
        print(f"\n=== 执行结果 ===")
        print(f"成功: {result.success}")
        print(f"步数: {len(result.steps)}")

        await browser.close()

    print("\n✅ 测试完成")


async def main():
    """运行所有测试"""
    await test_agent_baidu_search()
    # await test_agent_reflection()  # 可选：测试反思机制
    print("\n=== 所有测试完成 ===")


if __name__ == "__main__":
    asyncio.run(main())
