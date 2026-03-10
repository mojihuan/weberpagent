"""Phase 6 采购表单测试与优化

迭代运行采购单场景测试，直到连续 2 次通过或达到最大轮次 3
"""

import asyncio
import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat
from backend.tests.reporter import TestResult
import yaml


def load_config():
    """加载测试配置"""
    config_path = Path(__file__).parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def run_purchase_test(page, llm, config, output_dir) -> TestResult:
    """运行采购单测试"""
    login_config = config["login"]
    purchase_config = config["purchase"]

    task_output = output_dir / "purchase"
    task_output.mkdir(parents=True, exist_ok=True)

    device_types = "、".join(purchase_config["device_types"])

    task = f"""
    在 ERP 系统完成新增采购单操作：
    1. 打开 {config['base_url']}
    2. 在账号输入框输入 {login_config['account']}
    3. 在密码输入框输入 {login_config['password']}
    4. 点击登录按钮
    5. 登录成功后，点击侧边栏"{purchase_config['navigation'][0]}"
    6. 点击"{purchase_config['navigation'][1]}"
    7. 点击"{purchase_config['navigation'][2]}"
    8. 点击"{purchase_config['add_button']}"按钮
    9. 选择设备类型（可选：{device_types}）
    10. 填写表单中的必填字段（根据页面实际情况填写，可以自由发挥）
    11. 点击提交或保存按钮
    12. 确认成功（检测按钮下方是否出现新记录）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=25,
        max_retries=3,
    )

    start_time = time.time()
    result = await agent.run()
    duration = time.time() - start_time

    screenshots = [str(s) for s in task_output.glob("*.png")]

    return TestResult(
        scenario="新增采购单",
        success=result.success,
        steps=len(result.steps),
        duration=duration,
        error=result.error if not result.success else None,
        screenshots=screenshots,
    )


async def run_single_iteration(page, llm, config, output_dir, run_num: int) -> tuple[bool, TestResult]:
    """运行单次测试，返回 (是否通过, 测试结果)"""
    print(f"\n{'='*50}")
    print(f"第 {run_num} 轮测试")
    print(f"{'='*50}")

    try:
        result = await run_purchase_test(page, llm, config, output_dir)

        status = "✅ 通过" if result.success else "❌ 失败"
        print(f"\n第 {run_num} 轮结果: {status}")
        print(f"  步数: {result.steps}")
        print(f"  耗时: {result.duration:.1f}s")

        if not result.success and result.error:
            print(f"  错误: {result.error}")

        return result.success, result

    except Exception as e:
        print(f"\n❌ 第 {run_num} 轮异常: {e}")

        error_result = TestResult(
            scenario="新增采购单",
            success=False,
            steps=0,
            duration=0,
            error=str(e),
            screenshots=[],
        )
        return False, error_result


async def main():
    """Phase 6 主函数 - 迭代运行直到成功"""
    # 检查 API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return False

    print("=" * 50)
    print("Phase 6: 采购表单测试与优化")
    print("=" * 50)
    print("目标: 采购单场景连续 2 次通过")
    print("最大迭代轮次: 3")
    print()

    # 加载配置
    config = load_config()

    # 初始化 LLM
    llm = QwenChat(model="qwen-vl-max")

    # 创建输出目录
    output_base = Path("outputs/tests/phase6")
    output_base.mkdir(parents=True, exist_ok=True)

    # 追踪连续成功次数
    consecutive_success = 0
    max_iterations = 3
    all_results: list[TestResult] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=100,
        )

        for iteration in range(1, max_iterations + 1):
            run_dir = output_base / f"run{iteration}"
            run_dir.mkdir(parents=True, exist_ok=True)

            # 为每轮测试创建新的页面
            page = await browser.new_page()

            success, result = await run_single_iteration(
                page, llm, config, run_dir, iteration
            )
            all_results.append(result)

            await page.close()

            if success:
                consecutive_success += 1
                print(f"\n✅ 第 {iteration} 轮通过！连续成功: {consecutive_success}/2")

                if consecutive_success >= 2:
                    print("\n🎉 目标达成！连续 2 次通过！")
                    break
            else:
                consecutive_success = 0  # 重置连续成功计数
                print(f"\n❌ 第 {iteration} 轮失败，重置连续成功计数")

                if iteration < max_iterations:
                    print("  准备下一轮测试...")

        await browser.close()

    # 生成汇总报告
    summary = {
        "phase": "Phase 6",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": "采购单场景连续 2 次通过",
        "max_iterations": max_iterations,
        "consecutive_success": consecutive_success,
        "target_achieved": consecutive_success >= 2,
        "results": [
            {
                "run": i + 1,
                "scenario": r.scenario,
                "success": r.success,
                "steps": r.steps,
                "duration": r.duration,
                "error": r.error,
            }
            for i, r in enumerate(all_results)
        ],
    }

    # 保存汇总报告
    summary_path = output_base / "phase6_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print("Phase 6 测试完成")
    print(f"{'='*50}")
    print(f"总轮次: {len(all_results)}")
    print(f"连续成功: {consecutive_success}/2")
    print(f"目标达成: {'✅ 是' if consecutive_success >= 2 else '❌ 否'}")
    print(f"报告已保存: {summary_path}")

    return consecutive_success >= 2


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
