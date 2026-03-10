"""M2: 侧边栏一级菜单测试

任务: 点击侧边栏"采购管理"菜单并验证子菜单展开
起点: 登录成功后的首页
成功标准: 连续 2 次通过
验证点:
  - "采购管理"菜单展开
  - 子菜单项可见（如"采购订单"）
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


async def run_single_test(page, llm, config, output_dir: Path) -> bool:
    """运行单次测试"""
    login_config = config["login"]
    purchase_config = config["purchase"]

    task_output = output_dir / "test"
    task_output.mkdir(parents=True, exist_ok=True)

    # 任务：登录后点击一级菜单
    task = f"""
    在 ERP 系统执行以下操作：
    1. 打开 {config['base_url']}
    2. 输入账号 {login_config['account']} 和密码 {login_config['password']}
    3. 点击登录按钮
    4. 登录成功后，点击侧边栏"{purchase_config['navigation'][0]}"菜单
    5. 确认子菜单已展开（如果点击后子菜单未展开，尝试悬停在菜单上）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=15,
        max_retries=3,
    )

    result = await agent.run()

    status = "✅ 通过" if result.success else "❌ 失败"
    print(f"  结果: {status}, 步数: {len(result.steps)}")

    return result.success


async def run_test():
    """运行 M2 侧边栏一级菜单测试（需要连续 2 次通过）"""
    print("=" * 50)
    print("M2: 侧边栏一级菜单测试")
    print("成功标准: 连续 2 次通过")
    print("=" * 50)

    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return False

    config = load_config()
    llm = QwenChat(model="qwen-vl-max")

    consecutive_success = 0
    required_success = 2

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)

        run_num = 1
        while consecutive_success < required_success:
            print(f"\n第 {run_num} 次测试:")

            output_dir = Path(f"outputs/tests/phase7/m2_sidebar_l1/run{run_num}")
            output_dir.mkdir(parents=True, exist_ok=True)

            page = await browser.new_page()
            success = await run_single_test(page, llm, config, output_dir)
            await page.close()

            if success:
                consecutive_success += 1
                print(f"  ✅ 连续成功: {consecutive_success}/{required_success}")
            else:
                consecutive_success = 0
                print(f"  ❌ 重置连续成功计数")

            run_num += 1

            # 防止无限循环（最多 10 次）
            if run_num > 10:
                print("\n⚠️ 达到最大尝试次数 10 次")
                break

        await browser.close()

    final_status = "✅ 通过" if consecutive_success >= required_success else "❌ 失败"
    print(f"\n最终结果: {final_status} (连续成功 {consecutive_success}/{required_success})")

    return consecutive_success >= required_success


if __name__ == "__main__":
    success = asyncio.run(run_test())
    sys.exit(0 if success else 1)
