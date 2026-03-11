"""代码沙箱执行器 - POC 阶段信任执行"""

import json
import logging
import re
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
    # 预加载常用标准库模块，供生成代码使用
    local_vars: dict[str, Any] = {}
    global_vars = {
        "__builtins__": __builtins__,
        # 常用标准库
        "json": json,
        "re": re,
        **context,
    }

    try:
        code_lines = code.split('\n')
        logger.info(f"开始执行代码，超时: {timeout}s，共 {len(code_lines)} 行")
        logger.debug("=" * 60)
        for i, line in enumerate(code_lines, 1):
            logger.debug(f"{i:3d} | {line}")
        logger.debug("=" * 60)

        # ========== 调试：逐行执行并记录 ==========
        # 将代码按顶层语句分割执行
        import ast
        try:
            tree = ast.parse(code)
            for i, node in enumerate(tree.body):
                # 获取当前节点的源代码
                start_line = node.lineno - 1
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 1
                node_code = '\n'.join(code_lines[start_line:end_line])

                logger.info(f"📍 执行第 {i+1} 个语句 (行 {start_line+1}-{end_line}):")
                logger.info(f"   {node_code[:100]}{'...' if len(node_code) > 100 else ''}")

                # 执行当前节点
                try:
                    exec(compile(ast.Module([node], []), '<string>', 'exec'), global_vars, local_vars)
                    logger.info(f"   ✅ 成功")
                except Exception as e:
                    logger.error(f"   ❌ 失败: {type(e).__name__}: {e}")
                    raise
        except SyntaxError as e:
            logger.error(f"代码语法错误: {e}")
            raise

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