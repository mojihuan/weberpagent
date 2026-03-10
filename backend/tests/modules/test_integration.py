"""整合测试: 完整采购单流程

任务: M1→M2→M3→M4→M5 完整流程
成功标准: 连续 2 次通过
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime
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


async def run_single_test(page, llm, config, output_dir: Path) -> tuple[bool, int, float]:
    """运行单次整合测试

    Returns:
        (success, steps, duration)
    """
    login_config = config["login"]
    purchase_config = config["purchase"]

    task_output = output_dir / "test"
    task_output.mkdir(parents=True, exist_ok=True)

    device_types = "、".join(purchase_config["device_types"])
    nav_steps = " → ".join(purchase_config["navigation"])

    task = f"""
    在 ERP 系统完成新增采购单操作：
    1. 打开 {config['base_url']}
    2. 在账号输入框输入 {login_config['account']}
    3. 在密码输入框输入 {login_config['password']}
    4. 点击登录按钮
    5. 登录成功后，依次点击侧边栏菜单：{nav_steps}
    6. 点击"{purchase_config['add_button']}"按钮
    7. 选择设备类型（可选：{device_types}）
    8. 填写表单中的必填字段（根据页面实际情况填写）
    9. 点击提交或保存按钮
    10. 确认成功（检测按钮下方是否出现新记录或成功提示）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=30,
        max_retries=3,
    )

    start_time = time.time()
    result = await agent.run()
    duration = time.time() - start_time

    status = "✅ 通过" if result.success else "❌ 失败"
    print(f"  结果: {status}, 步数: {len(result.steps)}, 耗时: {duration:.1f}s")

    return result.success, len(result.steps), duration


async def run_test():
    """运行整合测试（需要连续 2 次通过）"""
    print("=" * 50)
    print("整合测试: 完整采购单流程")
    print("成功标准: 连续 2 次通过")
    print("=" * 50)

    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return False

    config = load_config()
    llm = QwenChat(model="qwen-vl-max")

    consecutive_success = 0
    required_success = 2
    all_results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)

        run_num = 1
        while consecutive_success < required_success:
            print(f"\n第 {run_num} 次测试:")

            output_dir = Path(f"outputs/tests/phase7/integration/run{run_num}")
            output_dir.mkdir(parents=True, exist_ok=True)

            page = await browser.new_page()
            success, steps, duration = await run_single_test(page, llm, config, output_dir)
            await page.close()

            all_results.append({
                "run": run_num,
                "success": success,
                "steps": steps,
                "duration": duration,
            })

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

    # 生成汇总报告
    final_status = "✅ 通过" if consecutive_success >= required_success else "❌ 失败"
    print(f"\n最终结果: {final_status} (连续成功 {consecutive_success}/{required_success})")

    # 保存报告
    report = {
        "phase": "Phase 7 整合测试",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": "采购单场景连续 2 次通过",
        "consecutive_success": consecutive_success,
        "target_achieved": consecutive_success >= required_success,
        "results": all_results,
    }

    report_path = Path("outputs/tests/phase7/integration/summary.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"报告已保存: {report_path}")

    return consecutive_success >= required_success


if __name__ == "__main__":
    success = asyncio.run(run_test())
    sys.exit(0 if success else 1)
