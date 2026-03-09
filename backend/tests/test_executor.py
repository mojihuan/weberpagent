"""测试 executor 模块"""

import asyncio
from contextlib import asynccontextmanager

from playwright.async_api import async_playwright, Browser, Page

from backend.agent_simple.perception import Perception
from backend.agent_simple.executor import Executor
from backend.agent_simple.types import Action


@asynccontextmanager
async def open_browser():
    """辅助函数：打开浏览器（异步上下文管理器）"""
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False)
    page = await browser.new_page()
    try:
        yield browser, page
    finally:
        await browser.close()
        await p.stop()


async def test_executor_navigate():
    """测试导航动作"""
    print("\n=== 测试 navigate 动作 ===\n")

    async with open_browser() as (browser, page):
        executor = Executor(page)

        # 测试导航
        action = Action(
            thought="打开百度首页",
            action="navigate",
            value="https://www.baidu.com",
        )
        result = await executor.execute(action, [])

        print(f"导航结果: success={result.success}, error={result.error}")
        assert result.success, "导航失败"

        print(f"当前 URL: {page.url}")
        assert "baidu.com" in page.url

    print("✅ navigate 测试通过")


async def test_executor_click():
    """测试点击动作"""
    print("\n=== 测试 click 动作 ===\n")

    async with open_browser() as (browser, page):
        executor = Executor(page)
        perception = Perception(page)

        # 先导航到百度
        await page.goto("https://www.baidu.com")
        await page.wait_for_load_state("networkidle")

        # 获取页面元素
        state = await perception.get_state()
        print(f"页面: {state.title}")
        print(f"元素数量: {len(state.elements)}")

        # 测试点击"新闻"链接
        action = Action(
            thought="点击新闻链接",
            action="click",
            target="新闻",
        )
        result = await executor.execute(action, state.elements)

        print(f"点击结果: success={result.success}, error={result.error}")

        if result.success:
            await page.wait_for_load_state("networkidle")
            print(f"点击后 URL: {page.url}")

    print("✅ click 测试通过")


async def test_executor_input():
    """测试输入动作"""
    print("\n=== 测试 input 动作 ===\n")

    async with open_browser() as (browser, page):
        executor = Executor(page)
        perception = Perception(page)

        # 导航到百度
        await page.goto("https://www.baidu.com")
        await page.wait_for_load_state("networkidle")

        # 获取页面元素
        state = await perception.get_state()

        # 查找搜索框
        search_input = None
        for el in state.elements:
            if el.tag == "INPUT" and el.type == "text":
                search_input = el
                break

        if search_input:
            print(f"找到搜索框: placeholder={search_input.placeholder}")

            # 测试输入
            action = Action(
                thought="在搜索框输入内容",
                action="input",
                target=search_input.placeholder or "搜索框",
                value="Python 教程",
            )
            result = await executor.execute(action, state.elements)

            print(f"输入结果: success={result.success}, error={result.error}")

            # 验证输入值
            if result.success:
                input_value = await page.input_value('input[type="text"]')
                print(f"输入框值: {input_value}")
                assert "Python" in input_value
        else:
            print("未找到搜索框，跳过测试")

    print("✅ input 测试通过")


async def test_executor_wait():
    """测试等待动作"""
    print("\n=== 测试 wait 动作 ===\n")

    async with open_browser() as (browser, page):
        executor = Executor(page)

        action = Action(thought="等待页面稳定", action="wait")
        result = await executor.execute(action, [])

        print(f"等待结果: success={result.success}")
        assert result.success

    print("✅ wait 测试通过")


async def main():
    """运行所有测试"""
    await test_executor_navigate()
    await test_executor_click()
    await test_executor_input()
    await test_executor_wait()
    print("\n=== 所有测试完成 ===")


if __name__ == "__main__":
    asyncio.run(main())
