"""代码沙箱执行器 - POC 阶段信任执行"""

import logging
import sys
from io import StringIO
from typing import Any

logger = logging.getLogger(__name__)


async def execute_code(
    code: str,
    context: dict[str, Any],
    timeout: int = 30,
) -> dict[str, Any]:
    """执行生成的代码

    POC 阶段：信任执行，直接使用 exec()
    生产阶段：需要添加白名单和沙箱隔离

    Args:
        code: 要执行的 Python 代码
        context: 执行上下文（包含 page 等对象）
        timeout: 执行超时时间（秒）

    Returns:
        执行结果字典:
        - success: 是否成功
        - locals: 局部变量（如有）
        - error: 错误信息（如有）
        - stdout: 标准输出（如有）
    """
    # 捕获 stdout
    old_stdout = sys.stdout
    sys.stdout = captured_stdout = StringIO()

    # 准备执行环境
    local_vars: dict[str, Any] = {}
    global_vars = {"__builtins__": __builtins__, **context}

    try:
        logger.info(f"开始执行代码，超时: {timeout}s")
        logger.debug(f"代码内容:\n{code[:500]}...")

        # 执行代码
        exec(code, global_vars, local_vars)

        # 获取 stdout
        stdout_output = captured_stdout.getvalue()

        logger.info("代码执行成功")

        return {
            "success": True,
            "locals": local_vars,
            "stdout": stdout_output,
        }

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"代码执行失败: {error_msg}")

        return {
            "success": False,
            "error": error_msg,
            "locals": local_vars,
        }

    finally:
        sys.stdout = old_stdout