"""Phase 4 批量运行脚本

运行所有场景测试并生成报告
"""

import asyncio
import os
import sys
import time
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat
from backend.tests.reporter import TestResult, Phase4Report
import yaml


def load_config():
    """加载测试配置"""
    config_path = Path(__file__).parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def run_login_test(page, llm, config, output_dir) -> TestResult:
    """运行登录测试"""
    login_config = config["login"]
    task_output = output_dir / "login"
    task_output.mkdir(parents=True, exist_ok=True)

    task = f"""
    在 ERP 系统执行登录操作：
    1. 打开 {config['base_url']}{login_config['url']}
    2. 在账号输入框输入 {login_config['account']}
    3. 在密码输入框输入 {login_config['password']}
    4. 点击登录按钮
    5. 确认登录成功（检测"商品采购"或"欢迎"等元素出现）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=10,
        max_retries=3,
    )

    start_time = time.time()
    result = await agent.run()
    duration = time.time() - start_time

    screenshots = [str(s) for s in task_output.glob("*.png")]

    return TestResult(
        scenario="登录场景",
        success=result.success,
        steps=len(result.steps),
        duration=duration,
        error=result.error if not result.success else None,
        screenshots=screenshots,
    )


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


async def main():
    """运行所有测试"""
    # 检查 API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return False

    print("=" * 50)
    print("Phase 4: 场景验证")
    print("=" * 50)

    # 加载配置
    config = load_config()
    output_dir = Path("outputs/tests/phase4")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 创建 LLM
    llm = QwenChat(model="qwen-vl-max")

    results: list[TestResult] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=100,
        )

        # 测试 1: 登录场景
        print("\n>>> 测试 1/2: 登录场景")
        page = await browser.new_page()
        try:
            result = await run_login_test(page, llm, config, output_dir)
            results.append(result)
            print(f"    结果: {'✅ 成功' if result.success else '❌ 失败'}")
            print(f"    步数: {result.steps}, 耗时: {result.duration:.1f}s")
        except Exception as e:
            print(f"    ❌ 异常: {e}")
            results.append(TestResult(
                scenario="登录场景",
                success=False,
                steps=0,
                duration=0,
                error=str(e),
                screenshots=[],
            ))
        finally:
            await page.close()

        # 测试 2: 新增采购单场景
        print("\n>>> 测试 2/2: 新增采购单")
        page = await browser.new_page()
        try:
            result = await run_purchase_test(page, llm, config, output_dir)
            results.append(result)
            print(f"    结果: {'✅ 成功' if result.success else '❌ 失败'}")
            print(f"    步数: {result.steps}, 耗时: {result.duration:.1f}s")
        except Exception as e:
            print(f"    ❌ 异常: {e}")
            results.append(TestResult(
                scenario="新增采购单",
                success=False,
                steps=0,
                duration=0,
                error=str(e),
                screenshots=[],
            ))
        finally:
            await page.close()

        await browser.close()

    # 生成报告
    report = Phase4Report(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        results=results,
    )

    # 打印摘要
    report.print_summary()

    # 保存 JSON 报告
    report_path = output_dir / "phase4_report.json"
    report.save(report_path)

    # 返回是否全部通过
    return report.pass_rate == 1.0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
