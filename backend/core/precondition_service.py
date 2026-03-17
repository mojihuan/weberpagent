"""前置条件执行服务"""

import asyncio
import logging
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jinja2 import Environment, StrictUndefined, UndefinedError

from backend.core.random_generators import (
    random_imei,
    random_numbers,
    random_phone,
    random_serial,
    sf_waybill,
)
from backend.core.time_utils import time_now

logger = logging.getLogger(__name__)


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

    def __init__(self, external_module_path: str | None = None):
        """初始化服务

        Args:
            external_module_path: 外部 API 模块路径（可选）
        """
        self.external_module_path = external_module_path
        self.context: dict[str, Any] = {}

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
            result.success = True
            result.variables = dict(self.context)  # 快照当前变量
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
        return dict(self.context)

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
