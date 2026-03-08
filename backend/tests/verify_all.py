"""综合验证脚本 - 验证所有环境配置"""
import subprocess
import sys
from pathlib import Path


def run_script(script_path: str) -> bool:
    """运行验证脚本并返回结果"""
    result = subprocess.run(
        ["uv", "run", "python", script_path],
        capture_output=False,
    )
    return result.returncode == 0


def main():
    """运行所有验证"""
    print("=" * 50)
    print("Phase 1 环境验证")
    print("=" * 50)
    print()

    tests = [
        ("Playwright", "backend/tests/verify_playwright.py"),
        ("通义千问 API", "backend/tests/verify_qwen.py"),
    ]

    results = {}
    for name, script in tests:
        print(f"\n>>> 验证 {name}")
        print("-" * 40)
        results[name] = run_script(script)
        print()

    # 汇总结果
    print("=" * 50)
    print("验证结果汇总")
    print("=" * 50)
    for name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {name}: {status}")

    all_passed = all(results.values())
    print()
    if all_passed:
        print("🎉 Phase 1 环境搭建完成！")
        return 0
    else:
        print("⚠️  部分验证失败，请检查配置")
        return 1


if __name__ == "__main__":
    sys.exit(main())
