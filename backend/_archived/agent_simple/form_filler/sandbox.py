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
        import asyncio

        try:
            tree = ast.parse(code)
            for i, node in enumerate(tree.body):
                # 获取当前节点的源代码
                start_line = node.lineno - 1
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 1
                node_code = '\n'.join(code_lines[start_line:end_line])

                # 检查是否是函数定义
                is_function_def = isinstance(node, ast.AsyncFunctionDef) or isinstance(node, ast.FunctionDef)
                func_name = node.name if is_function_def else None

                logger.info(f"📍 执行第 {i+1} 个语句 (行 {start_line+1}-{end_line}):")
                if is_function_def:
                    logger.info(f"   定义函数: {func_name}")
                else:
                    logger.info(f"   {node_code[:100]}{'...' if len(node_code) > 100 else ''}")

                # 执行当前节点
                try:
                    exec(compile(ast.Module([node], []), '<string>', 'exec'), global_vars, local_vars)
                    logger.info(f"   ✅ 成功")

                    # 如果是函数定义，执行完后调用它
                    if is_function_def and func_name:
                        logger.info(f"📍 调用函数: {func_name}(page)")
                        func = local_vars.get(func_name)
                        if func and callable(func):
                            result = func(page=context.get('page'))
                            # 如果是协程，需要 await
                            if asyncio.iscoroutine(result):
                                await result
                            logger.info(f"   ✅ 函数执行成功")
                        else:
                            logger.error(f"   ❌ 函数 {func_name} 未找到或不可调用")

                except Exception as e:
                    import traceback
                    # 获取详细的错误堆栈，找出失败的行号
                    tb = traceback.extract_tb(e.__traceback__)
                    error_detail = f"{type(e).__name__}: {e}"

                    # 查找代码中的失败行
                    for frame in reversed(tb):
                        if frame.filename == '<string>':
                            failed_line = frame.lineno
                            line_content = code_lines[failed_line - 1] if failed_line <= len(code_lines) else "未知"
                            logger.error(f"   ❌ 失败 (行 {failed_line}): {line_content.strip()}")
                            logger.error(f"   ❌ 错误: {error_detail}")
                            break
                    else:
                        logger.error(f"   ❌ 失败: {error_detail}")
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