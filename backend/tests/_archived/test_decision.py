"""测试 decision + prompts 模块"""

import asyncio
import os
from playwright.async_api import async_playwright

from backend.agent_simple.perception import Perception
from backend.agent_simple.decision import Decision
from backend.agent_simple.prompts import build_user_prompt, SYSTEM_PROMPT
from backend.llm.qwen import QwenChat


async def test_prompts():
    """测试 Prompt 生成"""
    print("\n=== 测试 Prompt 生成 ===\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.baidu.com")
        await page.wait_for_load_state("networkidle")

        perception = Perception(page)
        state = await perception.get_state()

        # 测试 Prompt 生成
        user_prompt = build_user_prompt("搜索 Python 教程", state)

        print("--- System Prompt (前 300 字符) ---")
        print(SYSTEM_PROMPT[:300] + "...")

        print("\n--- User Prompt (前 500 字符) ---")
        print(user_prompt[:500] + "...")

        await browser.close()

    print("\n✅ Prompt 生成测试通过")


async def test_decision():
    """测试 LLM 决策（需要 API Key）"""
    print("\n=== 测试 LLM 决策 ===\n")

    # 检查 API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("⚠️ DASHSCOPE_API_KEY 未配置，跳过 LLM 调用测试")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.baidu.com")
        await page.wait_for_load_state("networkidle")

        # 获取页面状态
        perception = Perception(page)
        state = await perception.get_state()

        print(f"页面: {state.title}")
        print(f"元素数量: {len(state.elements)}")

        # 创建决策模块
        llm = QwenChat(model="qwen-vl-max")
        decision = Decision(llm)

        # 执行决策
        print("\n正在调用 LLM 进行决策...")
        action = await decision.decide(
            task="在百度搜索框中输入 'Python 教程' 并搜索",
            state=state,
        )

        print(f"\n--- 决策结果 ---")
        print(f"思考: {action.thought}")
        print(f"动作: {action.action}")
        print(f"目标: {action.target}")
        print(f"值: {action.value}")
        print(f"完成: {action.done}")

        await browser.close()

    print("\n✅ LLM 决策测试通过")


async def main():
    """运行所有测试"""
    await test_prompts()
    await test_decision()
    print("\n=== 所有测试完成 ===")


if __name__ == "__main__":
    asyncio.run(main())
