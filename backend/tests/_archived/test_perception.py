"""测试 perception 模块"""

import asyncio
from playwright.async_api import async_playwright

from backend.agent_simple.perception import Perception
from backend.agent_simple.prompts import format_elements_for_prompt


async def test_perception():
    """测试页面感知功能"""

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 打开一个测试页面（百度首页）
        print("正在打开百度首页...")
        await page.goto("https://www.baidu.com")
        await page.wait_for_load_state("networkidle")

        # 创建感知模块
        perception = Perception(page)

        # 获取页面状态
        print("\n获取页面状态...")
        state = await perception.get_state()

        # 打印结果
        print(f"\n=== 页面信息 ===")
        print(f"URL: {state.url}")
        print(f"标题: {state.title}")
        print(f"截图大小: {len(state.screenshot_base64)} bytes (base64)")

        print(f"\n=== 可交互元素 ({len(state.elements)} 个) ===")
        for el in state.elements[:10]:  # 只显示前 10 个
            print(f"  [{el.index}] {el.tag} | 文本: {el.text} | 类型: {el.type}")

        if len(state.elements) > 10:
            print(f"  ... 还有 {len(state.elements) - 10} 个元素")

        print(f"\n=== Prompt 格式 ===")
        print(format_elements_for_prompt(state.elements[:5]))

        # 关闭浏览器
        await browser.close()

        print("\n测试完成!")


if __name__ == "__main__":
    asyncio.run(test_perception())
