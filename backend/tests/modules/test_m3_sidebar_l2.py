"""M3: 侧边栏二级菜单测试

任务: 依次点击"采购订单" → "商品采购"
起点: M2 完成后的状态（采购管理已展开）
成功标准: 连续 2 次通过
验证点:
  - URL 变为商品采购页面
  - 页面包含"新增"按钮或采购列表
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

    # 导航路径
    nav_steps = " → ".join(purchase_config["navigation"])

    task = f"""
    在 ERP 系统执行以下操作：
    1. 打开 {config['base_url']}
    2. 输入账号 {login_config['account']} 和密码 {login_config['password']}
    3. 点击登录按钮
    4. 登录成功后，依次点击侧边栏菜单：{nav_steps}
    5. 确认已进入商品采购页面（检测 URL 变化或页面标题）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=20,
        max_retries=3,
    )

    result = await agent.run()

    status = "✅ 通过" if result.success else "❌ 失败"
    print(f"  结果: {status}, 步数: {len(result.steps)}")

    return result.success


async def run_test():
    """运行 M3 侧边栏二级菜单测试（需要连续 2 次通过）"""
    print("=" * 50)
    print("M3: 侧边栏二级菜单测试")
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

            output_dir = Path(f"outputs/tests/phase7/m3_sidebar_l2/run{run_num}")
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
