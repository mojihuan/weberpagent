"""验证 Playwright 基础功能"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from playwright.async_api import async_playwright


async def verify_playwright() -> bool:
    """验证 Playwright 能正常启动浏览器并截图"""
    print("正在验证 Playwright...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 访问百度首页
        await page.goto("https://www.baidu.com", timeout=30000)
        title = await page.title()

        print(f"✅ Playwright 正常工作")
        print(f"   页面标题: {title}")

        await browser.close()
        return True


if __name__ == "__main__":
    try:
        result = asyncio.run(verify_playwright())
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"❌ Playwright 验证失败: {e}")
        sys.exit(1)
