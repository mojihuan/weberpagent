"""测试优化后的 SimpleAgent - 真实网站测试"""

import asyncio
import os

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat


async def test_baidu_search():
    """测试 1：百度搜索

    任务：在百度搜索 "Python 教程"
    预期：打开百度 → 输入关键词 → 点击搜索
    """
    print("\n" + "=" * 60)
    print("测试 1：百度搜索")
    print("=" * 60)

    if not os.getenv("DASHSCOPE_API_KEY"):
        print("⚠️ DASHSCOPE_API_KEY 未配置，跳过测试")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        llm = QwenChat(model="qwen-vl-max")
        agent = SimpleAgent(
            task='在百度搜索 "Python 教程"，然后点击搜索按钮',
            llm=llm,
            page=page,
            max_steps=10,
            max_retries=2,
        )

        result = await agent.run()

        print(f"\n=== 执行结果 ===")
        print(f"成功: {result.success}")
        if result.result:
            print(f"结果: {result.result}")
        if result.error:
            print(f"错误: {result.error}")
        print(f"步数: {len(result.steps)}")

        # 详细步骤
        print(f"\n=== 执行步骤 ===")
        for step in result.steps:
            print(f"\nStep {step.step_num}:")
            print(f"  思考: {step.action.thought[:50]}...")
            print(f"  动作: {step.action.action}")
            print(f"  目标: {step.action.target}")
            print(f"  值: {step.action.value}")
            print(f"  结果: {'✅ 成功' if step.result.success else '❌ 失败'}")
            if step.result.error:
                print(f"  错误: {step.result.error}")

        await browser.close()

    return result.success


async def test_baidu_form():
    """测试 2：百度高级搜索表单

    任务：在百度高级搜索页面填写搜索词
    预期：打开页面 → 识别输入框 → 填写内容
    """
    print("\n" + "=" * 60)
    print("测试 2：百度高级搜索表单")
    print("=" * 60)

    if not os.getenv("DASHSCOPE_API_KEY"):
        print("⚠️ DASHSCOPE_API_KEY 未配置，跳过测试")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        llm = QwenChat(model="qwen-vl-max")
        agent = SimpleAgent(
            task="打开百度高级搜索页面 https://www.baidu.com/gaoji/advanced.html，在第一个输入框中输入 'Playwright 教程'",
            llm=llm,
            page=page,
            max_steps=10,
            max_retries=2,
        )

        result = await agent.run()

        print(f"\n=== 执行结果 ===")
        print(f"成功: {result.success}")
        if result.result:
            print(f"结果: {result.result}")
        if result.error:
            print(f"错误: {result.error}")
        print(f"步数: {len(result.steps)}")

        # 详细步骤
        print(f"\n=== 执行步骤 ===")
        for step in result.steps:
            print(f"\nStep {step.step_num}:")
            print(f"  思考: {step.action.thought[:50]}...")
            print(f"  动作: {step.action.action}")
            print(f"  目标: {step.action.target}")
            print(f"  值: {step.action.value}")
            print(f"  结果: {'✅ 成功' if step.result.success else '❌ 失败'}")
            if step.result.error:
                print(f"  错误: {step.result.error}")

        await browser.close()

    return result.success


async def test_element_extraction():
    """测试元素提取优化

    验证：
    1. aria-label 是否被提取
    2. title 是否被提取
    3. 文本是否被清理（去除空格）
    4. 元素数量是否被限制
    """
    print("\n" + "=" * 60)
    print("测试：元素提取优化")
    print("=" * 60)

    from backend.agent_simple.perception import Perception

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 打开百度首页
        await page.goto("https://www.baidu.com")
        await page.wait_for_load_state("networkidle")

        perception = Perception(page)
        state = await perception.get_state()

        print(f"\n页面: {state.title}")
        print(f"URL: {state.url}")
        print(f"元素数量: {len(state.elements)}")

        print(f"\n=== 元素列表（前 10 个）===")
        for el in state.elements[:10]:
            attrs = []
            if el.text:
                attrs.append(f'文本="{el.text}"')
            if el.placeholder:
                attrs.append(f'placeholder="{el.placeholder}"')
            if el.aria_label:
                attrs.append(f'aria-label="{el.aria_label}"')
            if el.title:
                attrs.append(f'title="{el.title}"')
            print(f"[{el.index}] <{el.tag}> {' | '.join(attrs) if attrs else '(无属性)'}")

        # 验证
        has_aria_label = any(el.aria_label for el in state.elements)
        has_title = any(el.title for el in state.elements)
        is_limited = len(state.elements) <= 30

        print(f"\n=== 验证结果 ===")
        print(f"aria-label 提取: {'✅' if has_aria_label else '⚠️ 未发现'}")
        print(f"title 提取: {'✅' if has_title else '⚠️ 未发现'}")
        print(f"元素数量限制 (≤30): {'✅' if is_limited else '❌'} ({len(state.elements)} 个)")

        await browser.close()


async def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("优化版 Agent 测试")
    print("=" * 60)

    # 先测试元素提取（不需要 API）
    await test_element_extraction()

    # 测试百度搜索
    result1 = await test_baidu_search()

    # 测试表单填写
    result2 = await test_baidu_form()

    # 汇总
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    print(f"百度搜索: {'✅ 通过' if result1 else '❌ 失败'}")
    print(f"表单填写: {'✅ 通过' if result2 else '❌ 失败'}")


if __name__ == "__main__":
    asyncio.run(main())
