"""M1: 登录验证测试

任务: 登录系统
成功标准: 单次通过
验证点:
  - URL 变为首页/仪表盘
  - 页面包含用户名或退出按钮
"""

import asyncio
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat
import yaml


def load_config():
    """加载测试配置"""
    config_path = Path(__file__).parent.parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def run_test():
    """运行 M1 登录验证测试"""
    print("=" * 50)
    print("M1: 登录验证测试")
    print("成功标准: 单次通过")
    print("=" * 50)

    # 检查 API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return False

    # 加载配置
    config = load_config()
    login_config = config["login"]

    # 创建输出目录
    output_dir = Path("outputs/tests/phase7/m1_login")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 初始化 LLM
    llm = QwenChat(model="qwen-vl-max")

    # 构建任务
    task = f"""
    在 ERP 系统执行登录操作：
    1. 打开 {config['base_url']}
    2. 在账号输入框输入 {login_config['account']}
    3. 在密码输入框输入 {login_config['password']}
    4. 点击登录按钮
    5. 确认登录成功（检测页面标题变化或出现用户信息）
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        page = await browser.new_page()

        agent = SimpleAgent(
            task=task,
            llm=llm,
            page=page,
            output_dir=str(output_dir),
            max_steps=15,
            max_retries=3,
        )

        start_time = time.time()
        result = await agent.run()
        duration = time.time() - start_time

        await browser.close()

    # 打印结果
    status = "✅ 通过" if result.success else "❌ 失败"
    print(f"\n结果: {status}")
    print(f"步数: {len(result.steps)}")
    print(f"耗时: {duration:.1f}s")

    if not result.success and result.error:
        print(f"错误: {result.error}")

    return result.success


if __name__ == "__main__":
    success = asyncio.run(run_test())
    sys.exit(0 if success else 1)
