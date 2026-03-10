"""M4: 表单填写测试

任务: 点击新增按钮，填写采购表单
起点: M3 完成后的商品采购页面
成功标准: 连续 2 次通过
验证点:
  - 表单页面打开
  - 必填字段已填写
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

    device_types = "、".join(purchase_config["device_types"])
    nav_steps = " → ".join(purchase_config["navigation"])

    # 任务：导航到商品采购页面并填写表单
    task = f"""
    在 ERP 系统执行以下操作：
    1. 打开 {config['base_url']}
    2. 输入账号 {login_config['account']} 和密码 {login_config['password']}
    3. 点击登录按钮
    4. 登录成功后，依次点击侧边栏菜单：{nav_steps}
    5. 点击"{purchase_config['add_button']}"按钮
    6. 在表单中填写必填字段（设备类型可选：{device_types}，其他字段根据页面实际情况填写）
    7. 确认表单已填写完整（检查必填字段是否有值）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=25,
        max_retries=3,
    )

    result = await agent.run()

    status = "✅ 通过" if result.success else "❌ 失败"
    print(f"  结果: {status}, 步数: {len(result.steps)}")

    return result.success


async def run_test():
    """运行 M4 表单填写测试（需要连续 2 次通过）"""
    print("=" * 50)
    print("M4: 表单填写测试")
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

            output_dir = Path(f"outputs/tests/phase7/m4_form/run{run_num}")
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
