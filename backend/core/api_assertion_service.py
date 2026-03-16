"""接口断言执行服务"""

import asyncio
import logging
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, StrictUndefined, UndefinedError

logger = logging.getLogger(__name__)


@dataclass
class FieldAssertionResult:
    """单个字段断言结果"""
    field_name: str
    expected: Any
    actual: Any
    passed: bool = False
    message: str = ""
    assertion_type: str = "exact"  # exact, contains, time, decimal


@dataclass
class ApiAssertionResult:
    """接口断言执行结果"""
    index: int
    code: str
    success: bool = False
    error: str | None = None
    duration_ms: int = 0
    field_results: list[FieldAssertionResult] = field(default_factory=list)


class ApiAssertionService:
    """接口断言执行服务

    复用 PreconditionService 的 exec() 执行机制，
    新增断言判断逻辑（时间、精确匹配、包含匹配、小数近似）
    """

    TIME_TOLERANCE_SECONDS = 60  # +/-1 分钟
    DECIMAL_TOLERANCE = 0.01

    def __init__(self, external_module_path: str | None = None):
        """初始化服务

        Args:
            external_module_path: 外部 API 模块路径（可选）
        """
        self.external_module_path = external_module_path
        self.context: dict[str, Any] = {}

    def check_time_within_range(
        self,
        actual_time: datetime | str,
        tolerance_seconds: int = 60
    ) -> tuple[bool, str]:
        """检查时间是否在当前时间 +/-tolerance_seconds 范围内

        Args:
            actual_time: 实际时间（datetime 对象或 ISO 格式字符串）
            tolerance_seconds: 容差秒数，默认 60 秒（+/-1 分钟）

        Returns:
            (是否通过, 错误信息)
        """
        try:
            # 解析时间
            if isinstance(actual_time, str):
                # 尝试多种格式解析
                actual = None
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
                    try:
                        actual = datetime.strptime(actual_time, fmt)
                        break
                    except ValueError:
                        continue
                if actual is None:
                    return False, f"无法解析时间格式: {actual_time}"
            else:
                actual = actual_time

            now = datetime.now()
            diff = abs((now - actual).total_seconds())

            if diff <= tolerance_seconds:
                return True, ""
            else:
                return False, f"时间差 {diff:.1f} 秒超出容差范围 +/-{tolerance_seconds} 秒"

        except Exception as e:
            return False, f"时间断言错误: {str(e)}"

    def check_exact_match(self, actual: Any, expected: Any) -> tuple[bool, str]:
        """精确匹配断言

        Args:
            actual: 实际值
            expected: 期望值

        Returns:
            (是否通过, 错误信息)
        """
        if actual == expected:
            return True, ""
        return False, f"期望 '{expected}'，实际 '{actual}'"

    def check_contains_match(self, actual: str, expected: str) -> tuple[bool, str]:
        """包含匹配断言

        Args:
            actual: 实际字符串
            expected: 期望包含的字符串

        Returns:
            (是否通过, 错误信息)
        """
        if expected in str(actual):
            return True, ""
        return False, f"'{actual}' 不包含 '{expected}'"

    def check_decimal_approx(
        self,
        actual: float,
        expected: float,
        tolerance: float = 0.01
    ) -> tuple[bool, str]:
        """小数近似断言

        Args:
            actual: 实际值
            expected: 期望值
            tolerance: 容差，默认 0.01

        Returns:
            (是否通过, 错误信息)
        """
        diff = abs(actual - expected)
        if diff <= tolerance:
            return True, ""
        return False, f"差值 {diff} 超出容差 {tolerance}"

    def _setup_execution_env(self) -> dict:
        """创建执行环境"""
        if self.external_module_path:
            path = Path(self.external_module_path)
            if path.exists() and str(path) not in sys.path:
                sys.path.insert(0, str(path))

        return {
            '__builtins__': __builtins__,
            'context': self.context,
            'assert_time': self._assert_time,
            'assert_exact': self._assert_exact,
            'assert_contains': self._assert_contains,
            'assert_decimal': self._assert_decimal,
        }

    def _assert_time(self, actual_time: Any) -> bool:
        """时间断言辅助函数"""
        passed, _ = self.check_time_within_range(actual_time)
        return passed

    def _assert_exact(self, actual: Any, expected: Any) -> bool:
        """精确匹配辅助函数"""
        passed, _ = self.check_exact_match(actual, expected)
        return passed

    def _assert_contains(self, actual: str, expected: str) -> bool:
        """包含匹配辅助函数"""
        passed, _ = self.check_contains_match(actual, expected)
        return passed

    def _assert_decimal(self, actual: float, expected: float, tolerance: float = 0.01) -> bool:
        """小数近似辅助函数"""
        passed, _ = self.check_decimal_approx(actual, expected, tolerance)
        return passed

    @staticmethod
    def substitute_variables(text: str, context: dict[str, Any]) -> str:
        """使用 Jinja2 进行变量替换"""
        if not text or '{{' not in text:
            return text

        env = Environment(
            variable_start_string='{{',
            variable_end_string='}}',
            undefined=StrictUndefined,
        )
        template = env.from_string(text)
        return template.render(**context)

    async def execute_single(
        self,
        code: str,
        index: int,
        timeout: float = 30.0
    ) -> ApiAssertionResult:
        """执行单个接口断言"""
        result = ApiAssertionResult(index=index, code=code)
        start_time = time.time()

        try:
            # 变量替换
            code = self.substitute_variables(code, self.context)
        except UndefinedError as e:
            result.error = f"变量未定义: {str(e)}"
            result.duration_ms = int((time.time() - start_time) * 1000)
            return result

        env = self._setup_execution_env()

        try:
            loop = asyncio.get_event_loop()
            await asyncio.wait_for(
                loop.run_in_executor(None, lambda: exec(code, env)),
                timeout=timeout
            )
            result.success = True
            logger.info(f"接口断言 {index} 执行成功")
        except asyncio.TimeoutError:
            result.error = f"执行超时（超过 {timeout} 秒）"
            logger.warning(f"接口断言 {index} 超时")
        except SyntaxError as e:
            result.error = f"语法错误: {e.msg} (行 {e.lineno})"
            logger.error(f"接口断言 {index} 语法错误: {e}")
        except AssertionError as e:
            result.error = f"断言失败: {str(e)}"
            logger.info(f"接口断言 {index} 断言失败: {e}")
        except Exception as e:
            result.error = f"执行错误: {str(e)}"
            logger.error(f"接口断言 {index} 执行错误: {e}", exc_info=True)

        result.duration_ms = int((time.time() - start_time) * 1000)
        return result

    async def execute_all(
        self,
        assertions: list[str],
        timeout_each: float = 30.0
    ) -> list[ApiAssertionResult]:
        """执行所有接口断言（不终止，收集所有结果）"""
        results = []

        for i, code in enumerate(assertions):
            if not code.strip():
                continue

            result = await self.execute_single(code, i, timeout_each)
            results.append(result)

        return results

    def get_context(self) -> dict[str, Any]:
        """获取当前执行上下文（变量存储）"""
        return dict(self.context)
