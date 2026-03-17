#!/usr/bin/env python
"""Phase 7 验证脚本

验证动态数据支持功能：
- DYN-01: 随机数生成（SF 物流单号、手机号等）
- DYN-02: API 数据获取
- DYN-03: 跨步骤数据缓存
- DYN-04: 时间计算

用法:
    uv run python backend/tests/run_phase7.py
    uv run python backend/tests/run_phase7.py --modules --all
"""

import subprocess
import sys
from pathlib import Path


def run_test(test_path: str, description: str) -> bool:
    """运行测试并返回结果"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Test: {test_path}")
    print('='*60)

    result = subprocess.run(
        ["uv", "run", "pytest", test_path, "-v"],
        capture_output=False,
    )
    return result.returncode == 0


def main():
    """运行所有 Phase 7 验证"""
    print("\n" + "="*60)
    print("Phase 7: 动态数据支持 - 验证开始")
    print("="*60)

    results = {}

    # DYN-01: 随机数生成器
    results["DYN-01 (随机数生成器)"] = run_test(
        "backend/tests/unit/test_random_generators.py",
        "随机数生成器单元测试"
    )

    # DYN-04: 时间计算工具
    results["DYN-04 (时间计算)"] = run_test(
        "backend/tests/unit/test_time_utils.py",
        "时间计算工具单元测试"
    )

    # DYN-01, DYN-03, DYN-04: PreconditionService 集成
    results["DYN-01/03/04 (集成)"] = run_test(
        "backend/tests/unit/test_precondition_service.py",
        "PreconditionService 动态数据集成测试"
    )

    # DYN-01, DYN-02, DYN-03, DYN-04: 端到端流程
    results["DYN-01/02/03/04 (端到端)"] = run_test(
        "backend/tests/integration/test_dynamic_data_flow.py",
        "动态数据端到端集成测试"
    )

    # 输出结果摘要
    print("\n" + "="*60)
    print("Phase 7 验证结果摘要")
    print("="*60)

    all_passed = True
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False

    print("="*60)

    if all_passed:
        print("\nPhase 7 验证全部通过!")
        return 0
    else:
        print("\nPhase 7 验证存在失败项")
        return 1


if __name__ == "__main__":
    sys.exit(main())
