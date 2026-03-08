"""验证 Agent 基础执行流程"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv()


async def verify_basic_flow():
    """验证 Agent 基础执行流程 - 打开页面并截图"""
    from backend.agent import UIBrowserAgent
    from backend.llm import QwenChat

    print("=" * 50)
    print("Agent 基础流程验证")
    print("=" * 50)

    # 检查 API Key
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ 未配置 DASHSCOPE_API_KEY")
        return False

    # 初始化 LLM
    print("\n1. 初始化通义千问...")
    llm = QwenChat(model="qwen-vl-max")
    print(f"   ✓ 模型: {llm.model_name}")

    # 创建 Agent
    print("\n2. 创建 Agent...")
    agent = UIBrowserAgent(
        task="打开 https://example.com 并截图",
        llm=llm,
        output_dir="outputs/verify",
    )
    print(f"   ✓ 任务 ID: {agent.task_id}")

    # 执行任务
    print("\n3. 执行任务...")
    result = await agent.run()

    # 输出结果
    print("\n4. 执行结果:")
    print(f"   - 成功: {result['success']}")
    print(f"   - 步数: {result['steps']}")
    print(f"   - 耗时: {result['duration_seconds']:.2f}s")
    print(f"   - 截图: {result['screenshot_dir']}")
    print(f"   - 日志: {result['log_file']}")

    return result["success"]


async def verify_login_page():
    """验证 Agent 能打开登录页面"""
    from backend.agent import UIBrowserAgent
    from backend.llm import QwenChat

    print("=" * 50)
    print("登录页面访问验证")
    print("=" * 50)

    llm = QwenChat(model="qwen-vl-max")

    agent = UIBrowserAgent(
        task="打开 https://erptest.epbox.cn/ 登录页面，描述页面内容",
        llm=llm,
        output_dir="outputs/verify_login",
    )

    result = await agent.run()

    print(f"\n执行结果: 成功={result['success']}, 步数={result['steps']}")
    return result["success"]


async def main():
    """运行所有验证"""
    print("\n" + "=" * 60)
    print("Phase 3: Agent 改造验证")
    print("=" * 60)

    tests = [
        ("基础流程", verify_basic_flow),
        ("登录页面", verify_login_page),
    ]

    results = []
    for name, test in tests:
        print(f"\n>>> 测试: {name}")
        try:
            success = await test()
            results.append((name, success))
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            results.append((name, False))

    # 汇总
    print("\n" + "=" * 60)
    print("验证结果汇总:")
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}")

    all_passed = all(r[1] for r in results)
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
