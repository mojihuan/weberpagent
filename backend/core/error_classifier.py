"""Error classifier for pytest exit codes -- pure function classification.

将 pytest 退出码和错误输出分类为"执行环境错误"或"代码错误",
用于 SelfHealingRunner 决定是否调用 LLM 修复。

环境错误 (退出码 2/3/4/5) LLM 无法修复, 直接终止重试。
代码错误 (退出码 1 + SyntaxError/ImportError) 可以尝试 LLM 修复。
未知模式默认 CODE_RUNTIME, 不遗漏 LLM 修复机会。
"""

import dataclasses
import enum
import re


class ErrorCategory(enum.Enum):
    """pytest 错误分类枚举."""

    PASSED = "passed"                  # 测试通过
    ENV_INTERRUPT = "ENV_INTERRUPT"    # 退出码 2, 测试被中断
    ENV_PYTEST_ERROR = "ENV_PYTEST_ERROR"  # 退出码 3/4, pytest 内部/命令行错误
    ENV_NO_TESTS = "ENV_NO_TESTS"      # 退出码 5, 未收集到测试用例
    CODE_ERROR = "CODE_ERROR"          # 退出码 1 + SyntaxError/ImportError
    CODE_RUNTIME = "CODE_RUNTIME"      # 退出码 1 无已知模式, 或未知退出码


@dataclasses.dataclass(frozen=True)
class ErrorCategoryResult:
    """错误分类结果 (不可变).

    Attributes:
        category: 错误分类.
        skip_llm_healing: 是否跳过 LLM 修复 (环境错误为 True).
        user_message: 面向用户的分类描述.
    """

    category: ErrorCategory
    skip_llm_healing: bool
    user_message: str


def classify_pytest_error(exit_code: int, error_output: str) -> ErrorCategoryResult:
    """根据 pytest 退出码和错误输出分类错误类型.

    纯函数: 无副作用, 无 IO, 相同输入永远返回相同结果.

    Args:
        exit_code: pytest 进程退出码.
        error_output: pytest stderr 或 stdout 输出.

    Returns:
        ErrorCategoryResult 包含分类、是否跳过 LLM 修复、用户消息.
    """
    # 退出码 0: 测试通过
    if exit_code == 0:
        return ErrorCategoryResult(
            category=ErrorCategory.PASSED,
            skip_llm_healing=False,
            user_message="测试通过",
        )

    # 退出码 2: 测试被中断 (KeyboardInterrupt)
    if exit_code == 2:
        return ErrorCategoryResult(
            category=ErrorCategory.ENV_INTERRUPT,
            skip_llm_healing=True,
            user_message="执行环境错误 - 测试被中断",
        )

    # 退出码 3: pytest 内部错误 (INTERNALERROR)
    if exit_code == 3:
        return ErrorCategoryResult(
            category=ErrorCategory.ENV_PYTEST_ERROR,
            skip_llm_healing=True,
            user_message="执行环境错误 - pytest 内部错误",
        )

    # 退出码 4: pytest 命令行错误
    if exit_code == 4:
        return ErrorCategoryResult(
            category=ErrorCategory.ENV_PYTEST_ERROR,
            skip_llm_healing=True,
            user_message="执行环境错误 - pytest 命令行错误",
        )

    # 退出码 5: 未收集到测试用例
    if exit_code == 5:
        return ErrorCategoryResult(
            category=ErrorCategory.ENV_NO_TESTS,
            skip_llm_healing=True,
            user_message="执行环境错误 - 未收集到测试用例",
        )

    # 退出码 1: 测试失败, 检查错误输出模式
    if exit_code == 1:
        # SyntaxError
        if re.search(r"E\s+SyntaxError:", error_output):
            return ErrorCategoryResult(
                category=ErrorCategory.CODE_ERROR,
                skip_llm_healing=False,
                user_message="代码错误 - 语法错误",
            )

        # ImportError
        if re.search(r"E\s+ImportError:", error_output):
            return ErrorCategoryResult(
                category=ErrorCategory.CODE_ERROR,
                skip_llm_healing=False,
                user_message="代码错误 - 导入错误",
            )

        # 无已知模式: 默认运行时错误
        return ErrorCategoryResult(
            category=ErrorCategory.CODE_RUNTIME,
            skip_llm_healing=False,
            user_message="测试失败 - 运行时错误",
        )

    # 未知退出码: 默认 CODE_RUNTIME, 不遗漏 LLM 修复机会
    return ErrorCategoryResult(
        category=ErrorCategory.CODE_RUNTIME,
        skip_llm_healing=False,
        user_message=f"未知退出码 ({exit_code})",
    )
