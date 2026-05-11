"""前置条件执行服务"""

import asyncio
import copy
import logging
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jinja2 import Environment, StrictUndefined

from backend.core.cache_service import CacheService
from backend.core.excel_fill_service import ExcelFillService
from backend.core.external_execution_engine import execute_operations
from backend.core.external_precondition_bridge import execute_data_method
from backend.core.random_generators import (
    random_imei,
    random_numbers,
    random_phone,
    random_serial,
    sf_waybill,
)
from backend.core.time_utils import time_now

logger = logging.getLogger(__name__)


class DataMethodError(Exception):
    """Raised when data method execution fails.

    Provides detailed error information including the full method call.
    """
    pass


def execute_data_method_sync(class_name: str, method_name: str, params: dict) -> dict:
    """Synchronous wrapper for async execute_data_method.

    Handles event loop detection to work in both sync and async contexts.

    Args:
        class_name: Name of the class in base_params module
        method_name: Name of the method to execute
        params: Dictionary of parameters to pass to the method

    Returns:
        dict with success, data/error, and error_type fields
    """
    import nest_asyncio

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        # No running loop, create new one
        return asyncio.run(execute_data_method(class_name, method_name, params))

    # Already in async context - use nest_asyncio for nested execution
    # This is safe because we're in run_in_executor which runs in a thread pool
    nest_asyncio.apply()
    return asyncio.run(execute_data_method(class_name, method_name, params))


class ContextWrapper:
    """Wrapper providing dict-like interface plus get_data() method.

    Used as the 'context' object in precondition execution environment.
    Supports both variable storage (context['var'] = value) and
    data method calls (context.get_data('Class', 'method', i=2)).
    """

    def __init__(self, *, cache: CacheService | None = None, run_id: str | None = None):
        self._data: dict[str, Any] = {}
        self._cache = cache or CacheService()
        self._run_id = run_id
        self._excel_service: ExcelFillService | None = None
        self._assertion_count = 0  # Track number of assertions stored
        self._assertion_summary = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0
        }

    def cache(self, key: str, value: Any) -> Any:
        """Store value in cache and return it for chaining.

        Delegates to the internal CacheService instance.
        """
        return self._cache.cache(key, value)

    def cached(self, key: str) -> Any:
        """Retrieve a cached value. Returns None if missing.

        Delegates to the internal CacheService instance.
        """
        return self._cache.cached(key)

    def get_data(self, class_name: str, method_name: str, **params) -> Any:
        """Execute a data method and return the result.

        Args:
            class_name: Name of the class in base_params module (e.g., 'BaseParams')
            method_name: Name of the method to execute (e.g., 'inventory_list_data')
            **params: Parameters to pass to the method (e.g., i=2, j=13)

        Returns:
            The data returned by the method

        Raises:
            DataMethodError: If the method execution fails, with detailed message
        """
        result = execute_data_method_sync(class_name, method_name, params)

        if not result['success']:
            # Format params for error message
            params_str = ', '.join(f"{k}={v!r}" for k, v in params.items())
            raise DataMethodError(
                f"{class_name}.{method_name}({params_str}) failed: {result['error']}"
            )

        return result['data']

    def _get_excel_service(self) -> ExcelFillService:
        """Lazily create ExcelFillService on first use."""
        if self._excel_service is None:
            if not self._run_id:
                raise RuntimeError(
                    "Excel filling requires a run_id. "
                    "Ensure the pipeline passes run_id to ContextWrapper."
                )
            from backend.config.settings import get_settings
            settings = get_settings()
            self._excel_service = ExcelFillService(
                templates_dir=settings.templates_dir,
                filled_dir=settings.filled_dir,
                run_id=self._run_id,
            )
        return self._excel_service

    def fill_excel(
        self,
        template_name: str,
        sheet: str = "Sheet1",
        row: int = 2,
        col: int = 1,
        value: str | int | float | None = None,
    ) -> "ContextWrapper":
        """Fill a cell in an Excel template copy.

        Copies the template to a run-specific directory on first call,
        then writes value to the specified cell.

        Args:
            template_name: Template filename without .xlsx extension.
            sheet: Sheet name (default 'Sheet1').
            row: Row number (1-based).
            col: Column number (1-based).
            value: Value to write.

        Returns:
            self for chaining.
        """
        svc = self._get_excel_service()
        svc.fill_excel(template_name, sheet, row, col, value)
        return self

    def get_excel_path(self, template_name: str) -> str:
        """Get the absolute path to a filled Excel file as string.

        If fill_excel hasn't been called for this template yet,
        returns the original template path.

        Args:
            template_name: Template filename without .xlsx extension.

        Returns:
            Absolute file path as string.
        """
        svc = self._get_excel_service()
        return str(svc.get_excel_path(template_name))

    # Dict-like interface methods
    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def keys(self) -> list[str]:
        return self._data.keys()

    def to_dict(self) -> dict[str, Any]:
        """Return a deep copy for variable substitution."""
        return copy.deepcopy(self._data)

    def store_assertion_result(self, index: int, result: dict) -> None:
        """Store an assertion result in context.

        Args:
            index: Assertion index (0-based)
            result: Assertion result dict from execute_assertion_method()
                   Contains: success, passed, method, class_name,
                            field_results, duration, error, error_type
        """
        # Store with index-based key
        key = f"assertion_result_{index}"
        self._data[key] = result

        # Update summary
        self._assertion_summary["total"] += 1
        if result.get("passed"):
            self._assertion_summary["passed"] += 1
        elif result.get("error_type"):
            self._assertion_summary["errors"] += 1
        else:
            self._assertion_summary["failed"] += 1

        # Also store summary for easy access
        self._data["assertion_results"] = self._assertion_summary.copy()

    def get_assertion_results_summary(self) -> dict:
        """Get summary of all assertion results.

        Returns:
            dict with total, passed, failed, errors counts
        """
        return self._assertion_summary.copy()

    def reset_assertion_tracking(self) -> None:
        """Reset assertion tracking state.

        Called at the start of assertion execution to ensure clean state.
        """
        self._assertion_count = 0
        self._assertion_summary = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0
        }
        # Remove any existing assertion results from _data
        keys_to_remove = [k for k in self._data if k.startswith("assertion_result_")]
        for key in keys_to_remove:
            del self._data[key]
        if "assertion_results" in self._data:
            del self._data["assertion_results"]


@dataclass
class PreconditionResult:
    """单个前置条件执行结果"""
    index: int
    code: str
    success: bool = False
    error: str | None = None
    duration_ms: int = 0
    variables: dict[str, Any] = field(default_factory=dict)


class PreconditionService:
    """前置条件执行服务

    使用 exec() 执行用户提供的 Python 代码，
    通过 context['变量名'] 存储结果供后续步骤使用。
    """

    def __init__(
        self,
        external_module_path: str | None = None,
        *,
        cache: CacheService | None = None,
        run_id: str | None = None,
    ):
        """初始化服务

        Args:
            external_module_path: 外部 API 模块路径（可选）
            cache: External CacheService instance to share across phases (keyword-only per D-08)
            run_id: Run ID for Excel filling and other run-scoped operations
        """
        self.external_module_path = external_module_path
        self.context: ContextWrapper = ContextWrapper(cache=cache, run_id=run_id)

    def _setup_execution_env(self) -> dict:
        """创建执行环境

        包含动态数据辅助函数，供前置条件代码调用。

        Returns:
            exec() 使用的全局命名空间
        """
        # 添加外部模块路径
        if self.external_module_path:
            path = Path(self.external_module_path)
            if not path.exists():
                logger.warning(f"外部模块路径不存在: {path}")
            elif str(path) not in sys.path:
                sys.path.insert(0, str(path))
                logger.info(f"添加外部模块路径: {path}")
            else:
                logger.debug(f"外部模块路径已在 sys.path 中: {path}")

        # 受限的全局环境 + 动态数据辅助函数
        return {
            '__builtins__': __builtins__,
            'context': self.context,
            # 随机数生成函数
            'sf_waybill': sf_waybill,
            'random_phone': random_phone,
            'random_imei': random_imei,
            'random_serial': random_serial,
            'random_numbers': random_numbers,
            # 时间计算函数
            'time_now': time_now,
        }

    def validate_external_module_path(self) -> tuple[bool, str]:
        """验证外部模块路径是否有效

        Returns:
            (是否有效, 错误信息或成功消息)
        """
        if not self.external_module_path:
            return True, "未配置外部模块路径"

        path = Path(self.external_module_path)
        if not path.exists():
            return False, f"模块路径不存在: {self.external_module_path}"
        if not path.is_dir():
            return False, f"模块路径不是目录: {self.external_module_path}"

        return True, f"外部模块路径有效: {self.external_module_path}"

    async def execute_single(
        self,
        code: str,
        index: int,
        timeout: float = 30.0
    ) -> PreconditionResult:
        """执行单个前置条件

        Args:
            code: Python 代码字符串
            index: 前置条件索引（用于日志）
            timeout: 超时时间（秒）

        Returns:
            执行结果
        """
        result = PreconditionResult(index=index, code=code)
        start_time = time.time()

        env = self._setup_execution_env()

        try:
            loop = asyncio.get_event_loop()
            await asyncio.wait_for(
                loop.run_in_executor(None, lambda: exec(code, env)),
                timeout=timeout
            )

            # Auto-execute precondition operation codes if present
            op_codes = self.context.get('preconditions')
            if isinstance(op_codes, list) and len(op_codes) > 0:
                executed = self.context.get('_executed_operations', set())
                pending = [c for c in op_codes if c not in executed]
                if pending:
                    captured_pending = list(pending)
                    success, error, _ = await asyncio.wait_for(
                        loop.run_in_executor(
                            None, lambda: execute_operations(captured_pending)
                        ),
                        timeout=timeout,
                    )
                    if not success:
                        raise RuntimeError(
                            f"Precondition operations failed: {error}"
                        )
                    executed.update(pending)
                    self.context['_executed_operations'] = executed
                    logger.info(
                        f"前置条件 {index}: 自动执行操作码 {pending}"
                    )

            result.success = True
            result.variables = self.context.to_dict()  # 快照当前变量
            logger.info(f"前置条件 {index} 执行成功，变量: {list(result.variables.keys())}")
        except asyncio.TimeoutError:
            result.error = f"执行超时（超过 {timeout} 秒）"
            logger.warning(f"前置条件 {index} 超时")
        except SyntaxError as e:
            result.error = f"语法错误: {e.msg} (行 {e.lineno})"
            logger.error(f"前置条件 {index} 语法错误: {e}")
        except Exception as e:
            result.error = f"执行错误: {str(e)}"
            logger.error(f"前置条件 {index} 执行错误: {e}", exc_info=True)

        result.duration_ms = int((time.time() - start_time) * 1000)
        return result

    async def execute_all(
        self,
        preconditions: list[str],
        timeout_each: float = 30.0
    ) -> tuple[bool, list[PreconditionResult]]:
        """执行所有前置条件，任一失败则停止

        Args:
            preconditions: 前置条件代码列表
            timeout_each: 每个前置条件的超时时间

        Returns:
            (是否全部成功, 结果列表)
        """
        results = []

        for i, code in enumerate(preconditions):
            if not code.strip():
                continue

            result = await self.execute_single(code, i, timeout_each)
            results.append(result)

            if not result.success:
                logger.error(f"前置条件 {i} 失败，停止执行")
                return False, results

        return True, results

    def get_context(self) -> dict[str, Any]:
        """获取当前执行上下文（变量存储）

        Returns:
            context 字典的副本
        """
        return self.context.to_dict()

    @staticmethod
    def substitute_variables(text: str, context: dict[str, Any]) -> str:
        """使用 Jinja2 进行变量替换

        将文本中的 {{变量名}} 替换为 context 中的对应值。
        如果变量未定义，会抛出 UndefinedError。

        Args:
            text: 包含 {{变量名}} 的文本
            context: 变量上下文

        Returns:
            替换后的文本

        Raises:
            UndefinedError: 变量未定义时
        """
        if not text or '{{' not in text:
            return text

        env = Environment(
            variable_start_string='{{',
            variable_end_string='}}',
            undefined=StrictUndefined,  # 未定义变量时报错
        )
        template = env.from_string(text)
        return template.render(**context)
