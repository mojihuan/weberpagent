"""
⚠️ 已归档 - 2026-03-12

原因：旧的 Browser-Use 验证脚本，使用国产模型适配器。
保留供历史参考。

替代方案：使用 pytest + browser-use 原生 API
"""

"""登录场景验证运行脚本 (Azure OpenAI 版本)

批量运行渐进式测试，统计成功率、耗时等指标，生成验证报告。
使用 Azure OpenAI 模型（推荐 gpt-4o）。
"""

import argparse
import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from statistics import mean

# 加载 .env 文件
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env")

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


async def run_single_test(level: int, llm, config: dict) -> dict:
    """运行单个测试用例

    Args:
        level: 测试层级 (1, 2, 3)
        llm: LLM 实例 (BaseChatModel)
        config: 测试配置

    Returns:
        测试结果字典
    """
    from browser_use import Agent

    base_url = config["base_url"]
    username = config["username"]
    password = config["password"]
    success_indicators = "、".join(config["success_indicators"])

    # 根据层级定义任务
    tasks = {
        1: f"打开 {base_url}",
        2: f"""
        打开 {base_url}
        找到用户名输入框，输入 {username}
        找到密码输入框，输入 {password}
        不要点击登录按钮
        """,
        3: f"""
        执行登录操作：
        1. 打开 {base_url}
        2. 找到用户名输入框，输入 {username}
        3. 找到密码输入框，输入 {password}
        4. 点击登录按钮
        5. 确认登录成功，页面应该包含以下关键词之一：{success_indicators}
        """,
    }

    output_dir = Path(f"outputs/validation/level{level}")
    output_dir.mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    step_count = 0

    try:
        # 创建 Browser-Use Agent
        agent = Agent(
            task=tasks[level],
            llm=llm,
            max_failures=5,
            use_vision=True,
        )

        # 执行
        result = await agent.run()
        # 获取步数
        if hasattr(result, '__len__'):
            step_count = len(result)
        elif hasattr(result, 'history'):
            step_count = len(result.history)
        else:
            step_count = 1

        # 判断成功 - is_done 是方法，需要调用
        if callable(getattr(result, 'is_done', None)):
            success = result.is_done()
        elif hasattr(result, 'is_done'):
            success = result.is_done
        else:
            # 检查 final_result
            final = result.final_result() if hasattr(result, 'final_result') else None
            success = final is not None and '成功' in str(final)

        duration = time.time() - start_time

        return {
            "level": level,
            "success": success,
            "steps": step_count,
            "duration_seconds": round(duration, 2),
            "error": None,
        }

    except Exception as e:
        duration = time.time() - start_time
        return {
            "level": level,
            "success": False,
            "steps": step_count,
            "duration_seconds": round(duration, 2),
            "error": str(e),
        }
    finally:
        # 确保清理浏览器资源
        if 'agent' in dir():
            try:
                await agent.close()
            except:
                pass


async def run_validation(runs_per_level: int = 5, levels: list[int] | None = None) -> dict:
    """运行完整验证

    Args:
        runs_per_level: 每个层级的运行次数
        levels: 要运行的层级列表，默认全部

    Returns:
        验证报告字典
    """
    from backend.llm import AzureOpenAIChat

    # 检查 Azure OpenAI 配置
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    if not api_key or not endpoint:
        print("错误: Azure OpenAI 配置不完整")
        print("请在 .env 文件中添加:")
        print("  AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/")
        print("  AZURE_OPENAI_API_KEY=xxx")
        print("  AZURE_OPENAI_DEPLOYMENT=gpt-4o")
        return {}

    # 配置
    config = {
        "base_url": "https://erptest.epbox.cn/",
        "username": "Y59800075",
        "password": "Aa123456",
        "success_indicators": ["首页", "欢迎", "用户", "工作台"],
    }

    if levels is None:
        levels = [1, 2, 3]

    # 初始化 LLM (Azure OpenAI)
    llm = AzureOpenAIChat(deployment=deployment)
    print(f"使用模型: Azure OpenAI ({deployment})")
    print(f"端点: {endpoint}")

    # 结果收集
    all_results = {f"level{lv}": [] for lv in levels}

    print("=" * 60)
    print(f"登录场景验证 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"每个层级运行 {runs_per_level} 次")
    print("=" * 60)

    # 运行测试
    for level in levels:
        level_name = f"level{level}"
        print(f"\n>>> Level {level}: ", end="", flush=True)

        for run_idx in range(runs_per_level):
            print(f"#{run_idx + 1} ", end="", flush=True)

            try:
                result = await run_single_test(level, llm, config)
                all_results[level_name].append(result)

                # 简短状态
                status = "✓" if result["success"] else "✗"
                print(f"{status} ", end="", flush=True)

            except Exception as e:
                print(f"ERR ", end="", flush=True)
                all_results[level_name].append({
                    "level": level,
                    "success": False,
                    "steps": 0,
                    "duration_seconds": 0,
                    "error": str(e),
                })

        print()

    # 统计结果
    report = generate_report(all_results, runs_per_level)

    # 打印摘要
    print_summary(report)

    return report


def generate_report(all_results: dict, runs_per_level: int) -> dict:
    """生成统计报告

    Args:
        all_results: 所有测试结果
        runs_per_level: 每层运行次数

    Returns:
        统计报告
    """
    report = {
        "test_date": datetime.now().strftime("%Y-%m-%d"),
        "test_time": datetime.now().strftime("%H:%M:%S"),
        "runs_per_level": runs_per_level,
        "total_runs": sum(len(v) for v in all_results.values()),
        "results": {},
    }

    for level_name, results in all_results.items():
        if not results:
            continue

        successes = [r for r in results if r["success"]]
        steps_list = [r["steps"] for r in results if r["steps"] > 0]
        durations = [r["duration_seconds"] for r in results if r["duration_seconds"] > 0]

        # 计算单步平均耗时
        avg_step_time = 0
        if steps_list and durations:
            total_steps = sum(steps_list)
            total_duration = sum(durations)
            if total_steps > 0:
                avg_step_time = round(total_duration / total_steps, 2)

        report["results"][level_name] = {
            "success_count": len(successes),
            "total_count": len(results),
            "success_rate": round(len(successes) / len(results), 2) if results else 0,
            "avg_steps": round(mean(steps_list), 1) if steps_list else 0,
            "avg_duration": round(mean(durations), 1) if durations else 0,
            "avg_step_time": avg_step_time,
            "details": results,
        }

    return report


def print_summary(report: dict):
    """打印摘要

    Args:
        report: 统计报告
    """
    print("\n" + "=" * 60)
    print("验证结果摘要")
    print("=" * 60)

    level_names = {
        "level1": "Level 1 (打开页面)",
        "level2": "Level 2 (填写输入)",
        "level3": "Level 3 (完整登录)",
    }

    print(f"{'测试层级':<20} {'成功率':<10} {'平均步数':<10} {'平均耗时':<12} {'单步耗时':<10}")
    print("-" * 60)

    for level_key, name in level_names.items():
        if level_key not in report["results"]:
            continue

        data = report["results"][level_key]
        success_rate = f"{data['success_rate'] * 100:.0f}%"
        avg_steps = f"{data['avg_steps']:.1f}"
        avg_duration = f"{data['avg_duration']:.1f}s"
        avg_step_time = f"{data['avg_step_time']:.1f}s"

        print(f"{name:<20} {success_rate:<10} {avg_steps:<10} {avg_duration:<12} {avg_step_time:<10}")

    print("=" * 60)

    # 验收标准检查
    print("\n验收标准检查:")

    checks = [
        ("Level 1 成功率 100%", report["results"].get("level1", {}).get("success_rate", 0) >= 1.0),
        ("Level 2 成功率 ≥80%", report["results"].get("level2", {}).get("success_rate", 0) >= 0.8),
        ("Level 3 成功率 ≥60%", report["results"].get("level3", {}).get("success_rate", 0) >= 0.6),
    ]

    # 检查单步耗时
    all_step_times = []
    for level_data in report["results"].values():
        if level_data.get("avg_step_time", 0) > 0:
            all_step_times.append(level_data["avg_step_time"])

    avg_step_time_overall = mean(all_step_times) if all_step_times else 0
    checks.append(("单步推理耗时 ≤10s", avg_step_time_overall <= 10))

    for check_name, passed in checks:
        status = "✓ 通过" if passed else "✗ 未通过"
        print(f"  {check_name}: {status}")


def save_report(report: dict, output_path: str = "outputs/validation_report_azure.json"):
    """保存报告到文件

    Args:
        report: 统计报告
        output_path: 输出路径
    """
    # 确保目录存在
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n报告已保存: {output_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="登录场景验证运行脚本 (Azure OpenAI)")
    parser.add_argument(
        "-n", "--runs",
        type=int,
        default=5,
        help="每个层级的运行次数 (默认: 5)"
    )
    parser.add_argument(
        "-l", "--levels",
        type=str,
        default="1,2,3",
        help="要运行的层级，逗号分隔 (默认: 1,2,3)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="outputs/validation_report_azure.json",
        help="报告输出路径"
    )

    args = parser.parse_args()

    # 解析层级
    levels = [int(l.strip()) for l in args.levels.split(",")]

    # 运行验证
    report = asyncio.run(run_validation(runs_per_level=args.runs, levels=levels))

    if report:
        save_report(report, args.output)


if __name__ == "__main__":
    main()
