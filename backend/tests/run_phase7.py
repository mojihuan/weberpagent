"""Phase 7 运行入口 - 采购单场景分模块测试

用法:
    python -m backend.tests.run_phase7 --module m1
    python -m backend.tests.run_phase7 --all
    python -m backend.tests.run_phase7 --integration
"""

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


async def run_module(module: str):
    """运行单个模块测试"""
    print(f"\n{'='*50}")
    print(f"运行模块: {module.upper()}")
    print(f"{'='*50}\n")

    if module == "m1":
        from backend.tests.modules.test_m1_login import run_test
        await run_test()
    elif module == "m2":
        from backend.tests.modules.test_m2_sidebar_l1 import run_test
        await run_test()
    elif module == "m3":
        from backend.tests.modules.test_m3_sidebar_l2 import run_test
        await run_test()
    elif module == "m4":
        from backend.tests.modules.test_m4_form import run_test
        await run_test()
    elif module == "m5":
        from backend.tests.modules.test_m5_submit import run_test
        await run_test()
    else:
        print(f"未知模块: {module}")
        return False

    return True


async def run_all_modules():
    """按顺序运行所有模块"""
    modules = ["m1", "m2", "m3", "m4", "m5"]
    results = {}

    for module in modules:
        try:
            success = await run_module(module)
            results[module] = success
            if not success:
                print(f"\n❌ 模块 {module.upper()} 失败，停止后续测试")
                break
        except Exception as e:
            print(f"\n❌ 模块 {module.upper()} 异常: {e}")
            results[module] = False
            break

    # 打印汇总
    print(f"\n{'='*50}")
    print("模块测试汇总")
    print(f"{'='*50}")
    for module, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {module.upper()}: {status}")

    return all(results.values())


async def run_integration():
    """运行整合测试"""
    print(f"\n{'='*50}")
    print("运行整合测试")
    print(f"{'='*50}\n")

    from backend.tests.modules.test_integration import run_test
    await run_test()


def main():
    parser = argparse.ArgumentParser(description="Phase 7 模块测试")
    parser.add_argument("--module", "-m", help="运行指定模块 (m1-m5)")
    parser.add_argument("--all", "-a", action="store_true", help="运行所有模块")
    parser.add_argument("--integration", "-i", action="store_true", help="运行整合测试")

    args = parser.parse_args()

    if args.module:
        asyncio.run(run_module(args.module))
    elif args.all:
        asyncio.run(run_all_modules())
    elif args.integration:
        asyncio.run(run_integration())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
