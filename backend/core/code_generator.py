"""PlaywrightCodeGenerator -- 从翻译后的操作生成完整的 pytest Playwright 测试文件。

将 ActionTranslator 翻译的 TranslatedAction 列表组装为完整的 Python 测试文件。
输出结构 (per D-01/D-02):
- 元数据注释头部 (D-04)
- Import 语句
- def test_xxx(page: Page) -> None: 函数体
- 每个操作为一行 Playwright API 调用
"""

import ast
import logging
import re
from datetime import datetime, timezone

from backend.core.action_translator import ActionTranslator, TranslatedAction

logger = logging.getLogger(__name__)


class PlaywrightCodeGenerator:
    """生成完整的 pytest Playwright 测试文件。

    输出结构 (per D-01/D-02):
    - 元数据注释头部 (D-04)
    - Import 语句
    - def test_xxx(page: Page) -> None: 函数体
    - 每个操作为一行 Playwright API 调用
    """

    _RANDOM_FUNC_DEFS: dict[str, list[str]] = {
        "random_imei": [
            "def random_imei():",
            "    return 'I' + ''.join(random.choices('0123456789', k=14))",
        ],
        "random_phone": [
            "def random_phone():",
            "    return '13' + ''.join(random.choices('0123456789', k=9))",
        ],
        "sf_waybill": [
            "def sf_waybill():",
            "    uuid_hex = uuid.uuid4().hex[:12].upper()",
            '    return f"SF{uuid_hex}"',
        ],
        "random_serial": [
            "def random_serial():",
            "    return ''.join(random.choices('0123456789', k=8))",
        ],
        "random_numbers": [
            "def random_numbers(n):",
            "    return ''.join(random.choices('0123456789', k=n))",
        ],
    }

    def __init__(self) -> None:
        self._translator = ActionTranslator()

    @classmethod
    def _detect_needed_functions(cls, precondition_code: list[str]) -> list[str]:
        """检测前置条件代码需要哪些随机函数定义。"""
        all_code = "\n".join(precondition_code)
        needed: list[str] = []
        for func_name, func_lines in cls._RANDOM_FUNC_DEFS.items():
            if f"{func_name}(" in all_code:
                needed.extend(func_lines)
                needed.append("")
        return needed

    def generate(
        self,
        run_id: str,
        task_name: str,
        task_id: str,
        actions: list[TranslatedAction],
        precondition_config: dict | None = None,
        assertions_config: list[dict] | None = None,
        precondition_code: list[str] | None = None,
        variable_map: dict[str, str] | None = None,
    ) -> str:
        """生成完整的测试文件内容。

        Args:
            run_id: 执行记录 ID
            task_name: 任务名称（用于函数名和注释）
            task_id: 任务 ID
            actions: 翻译后的操作列表

        Returns:
            完整的 Python 文件内容字符串。
        """
        header = self._build_header(run_id, task_name, task_id)
        func_name = self._sanitize_function_name(task_name)
        body = self._build_body(actions)
        needs_logging = self._needs_logging(actions)

        parts = [header, ""]

        # 条件 import: expect when assertions present (per D-03)
        if assertions_config:
            parts.append("from playwright.sync_api import Page, expect")
        else:
            parts.append("from playwright.sync_api import Page")

        # 条件 import re for url_contains (per D-10)
        if assertions_config and any(
            a.get("type") == "url_contains" for a in assertions_config
        ):
            parts.append("import re")

        # 条件 logging import (per D-08): 有回退定位器或有断言时添加
        _needs_logger = needs_logging or bool(assertions_config)
        if _needs_logger:
            parts.append("import logging")

        # 条件 import: 前置条件需要的模块
        if precondition_code:
            all_pre_code = "\n".join(precondition_code)
            if "random_" in all_pre_code:
                parts.append("import random")
            if "uuid" in all_pre_code:
                parts.append("import uuid")

        # HealerError 类定义: 有定位器回退代码时添加
        needs_healer_error = any(action.locators for action in actions)
        if needs_healer_error:
            parts.append("")
            parts.append("")
            parts.append("class HealerError(Exception):")
            parts.append('    """定位器全部失败时抛出的异常。"""')
            parts.append("")
            parts.append("    def __init__(self, action_type: str = \"\", locators: tuple = (), original_error: str = \"\"):")
            parts.append("        self.action_type = action_type")
            parts.append("        self.locators = locators")
            parts.append("        self.original_error = original_error")
            parts.append("        super().__init__(f\"[{action_type}] 所有定位器失败: {original_error}\")")

        # 注入随机函数定义（模块级别，在 test 函数外）
        if precondition_code:
            needed_funcs = self._detect_needed_functions(precondition_code)
            if needed_funcs:
                parts.append("")
                parts.extend(needed_funcs)
            # 检测是否需要 _get_data 辅助函数
            _all_pre = "\n".join(precondition_code)
            if "get_data(" in _all_pre:
                parts.append("")
                parts.append("")
                parts.append("def _get_data(class_name, method_name, **params):")
                parts.append('    """外部数据获取 — 需要 ERP 网络可达 + 外部模块可用。"""')
                parts.append("    import asyncio")
                parts.append("    from backend.core.external_precondition_bridge import execute_data_method")
                parts.append("    result = asyncio.run(execute_data_method(class_name, method_name, params))")
                parts.append("    if not result['success']:")
                parts.append('        raise RuntimeError(f"get_data 失败: {result[\'error\']}")')
                parts.append("    return result['data']")

        parts.append("")
        parts.append(f"def {func_name}(page: Page) -> None:")
        parts.append(f'    """Auto-generated test from agent execution: {task_name}"""')

        # 条件 healer logger 初始化 (per D-08)
        if _needs_logger:
            parts.append('    _logger = logging.getLogger("healer")')

        # no_errors js_errors collector (per D-08/D-09): 在前置条件之前注入
        if assertions_config and any(
            a.get("type") == "no_errors" for a in assertions_config
        ):
            parts.append("    js_errors = []")
            parts.append('    page.on("pageerror", lambda e: js_errors.append(str(e)))')

        # 注入前置条件代码（函数体内，在 page.goto 之前）
        if precondition_code:
            parts.append("    # === Precondition: 动态数据生成 ===")
            for code_block in precondition_code:
                for raw_line in code_block.split("\n"):
                    stripped = raw_line.strip()
                    if not stripped:
                        continue
                    if "get_data(" in stripped:
                        # 将 context.get_data(...) 转换为 _get_data(...)
                        converted = stripped.replace("context.get_data(", "_get_data(")
                        parts.append(f"    {converted}")
                    elif "context.cache(" in stripped:
                        parts.append(f"    # NOTE: {stripped}")
                        parts.append("    #       cache 调用无法自包含，已跳过")
                    else:
                        # 移除 context['var'] = 前缀，直接赋值变量
                        _ctx_match = re.match(r"context\[\'(\w+)\'\]\s*=\s*(.+)", stripped)
                        if _ctx_match:
                            _vn = _ctx_match.group(1)
                            _vv = _ctx_match.group(2)
                            parts.append(f"    {_vn} = {_vv}")
                        else:
                            parts.append(f"    {stripped}")
            parts.append("")

        # 前置条件注入 (per PREC-01)
        if precondition_config and precondition_config.get("target_url"):
            parts.append(self._build_precondition(precondition_config["target_url"]))

        if body and variable_map:
            body = self._substitute_variables_in_code(body, variable_map)

        if body:
            parts.append(body)

        # 断言步骤注入 (per ASRT-01)
        if assertions_config:
            assertions_code = self._build_assertions(assertions_config)
            if assertions_code:
                parts.append(assertions_code)

        content = "\n".join(parts) + "\n"

        # D-05: 防御性语法验证 -- 记录 warning 但不阻止生成
        if not self.validate_syntax(content):
            try:
                ast.parse(content)
            except SyntaxError as e:
                logger.warning(
                    f"[{run_id}] 生成代码语法验证失败: {e.msg} (line {e.lineno})"
                )

        return content

    @staticmethod
    def _needs_logging(actions: list[TranslatedAction]) -> bool:
        """检查操作列表中是否有需要 logging 的回退代码。"""
        return any(action.locators for action in actions)

    def _sanitize_function_name(self, task_name: str) -> str:
        """将任务名称转换为合法的 Python 函数名 (per D-03)。

        中文保留（Python 3 支持 Unicode 标识符），特殊字符替换为下划线。
        """
        if not task_name.strip():
            return "test_unnamed"

        sanitized = re.sub(r"[^a-zA-Z0-9_\u4e00-\u9fff]", "_", task_name)
        # 去除前导数字和下划线
        sanitized = re.sub(r"^[0-9_]+", "", sanitized)

        if not sanitized:
            return "test_unnamed"

        return f"test_{sanitized}"

    def _build_header(self, run_id: str, task_name: str, task_id: str) -> str:
        """构建元数据注释头部 (per D-04)。"""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return "\n".join([
            "# Generated by aiDriveUITest",
            f"# Task: {task_name}",
            f"# Run ID: {run_id}",
            f"# Task ID: {task_id}",
            f"# Generated: {timestamp}",
            "# Source: model_actions() from browser-use Agent",
        ])

    def _build_body(self, actions: list[TranslatedAction]) -> str:
        """构建测试函数体。"""
        if not actions:
            return ""

        lines: list[str] = []
        prev_type: str | None = None

        for action in actions:
            # 不同操作类型之间插入空行分隔
            if prev_type is not None and action.action_type != prev_type:
                lines.append("")
            lines.append(action.code)
            prev_type = action.action_type

        raw = "\n".join(lines)

        # D-04: 缩进后处理 -- 确保非空行以 4 空格开头
        fixed_lines: list[str] = []
        for line in raw.split("\n"):
            if line.strip() and not line.startswith("    "):
                fixed_lines.append(f"    {line}")
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def _build_precondition(self, target_url: str) -> str:
        """生成 page.goto 前置条件代码 (per PREC-01).

        输出 page.goto + wait_for_load_state("networkidle") 带超时保护。
        wait_for_load_state 用 try-except 包裹，超时不影响后续操作。

        Args:
            target_url: 目标 ERP URL。

        Returns:
            缩进的代码块字符串。
        """
        lines = [
            f'    page.goto("{target_url}")',
            "    try:",
            '        page.wait_for_load_state("networkidle", timeout=10000)',
            "    except Exception:",
            "        pass  # 超时不影响后续操作",
        ]
        return "\n".join(lines)

    def _build_assertions(self, assertions_config: list[dict]) -> str:
        """生成断言 expect()/assert 代码块 (per ASRT-01).

        每个断言用 try-except 包裹，失败时记录日志但不停止测试。

        Args:
            assertions_config: 断言配置列表，每个 dict 含 type/expected/name。

        Returns:
            缩进的代码块字符串。
        """
        lines = ["", "    # Assertions"]
        for assertion in assertions_config:
            atype = assertion.get("type", "")
            expected = assertion.get("expected", "")
            if atype == "url_contains":
                lines.extend(self._translate_url_contains(str(expected)))
            elif atype == "text_exists":
                lines.extend(self._translate_text_exists(str(expected)))
            elif atype == "no_errors":
                lines.extend(self._translate_no_errors())
            elif atype == "element_exists":
                lines.extend(self._translate_element_exists(str(expected)))
            else:
                lines.append(f"    # unknown assertion: {atype}")
            lines.append("")
        return "\n".join(lines)

    def _translate_url_contains(self, expected: str) -> list[str]:
        """翻译 url_contains 断言为 expect(page).to_have_url(re.compile(...))."""
        return [
            "    try:",
            f'        expect(page).to_have_url(re.compile(".*{expected}.*"))',
            "    except AssertionError as e:",
            '        _logger.warning(f"Assertion failed (url_contains): {e}")',
        ]

    def _translate_text_exists(self, expected: str) -> list[str]:
        """翻译 text_exists 断言为 expect(page.locator('body')).to_contain_text(...)."""
        return [
            "    try:",
            f'        expect(page.locator("body")).to_contain_text("{expected}")',
            "    except AssertionError as e:",
            '        _logger.warning(f"Assertion failed (text_exists): {e}")',
        ]

    def _translate_no_errors(self) -> list[str]:
        """翻译 no_errors 断言为 assert len(js_errors) == 0."""
        return [
            "    try:",
            '        assert len(js_errors) == 0, f"JS errors: {js_errors}"',
            "    except AssertionError as e:",
            '        _logger.warning(f"Assertion failed (no_errors): {e}")',
        ]

    def _translate_element_exists(self, expected: str) -> list[str]:
        """翻译 element_exists 断言为 expect(locator).to_be_visible().

        Locator 推断逻辑 (per D-06):
        - CSS 选择器 (# . [ xpath= //) -> page.locator(expected)
        - 纯文本短 (<=4 chars) -> page.get_by_text(expected, exact=True)
        - 纯文本长 (>4 chars) -> page.get_by_text(expected)
        """
        if expected.startswith(("#", ".", "[", "xpath=", "//")):
            locator = f'page.locator("{expected}")'
        elif len(expected) <= 4:
            locator = f'page.get_by_text("{expected}", exact=True)'
        else:
            locator = f'page.get_by_text("{expected}")'
        return [
            "    try:",
            f"        expect({locator}).to_be_visible()",
            "    except AssertionError as e:",
            '        _logger.warning(f"Assertion failed (element_exists): {e}")',
        ]

    @staticmethod
    def _substitute_variables_in_code(code: str, variable_map: dict[str, str]) -> str:
        """将 fill/select 中的硬编码值替换为变量引用。

        只替换引号内的值。按值长度降序排列防止子串误替换。
        """
        if not variable_map:
            return code
        sorted_vars = sorted(variable_map.items(), key=lambda x: len(str(x[1])), reverse=True)
        for var_name, actual_value in sorted_vars:
            if not actual_value or not isinstance(actual_value, str):
                continue
            escaped = actual_value.replace("\\", "\\\\").replace('"', '\\"')
            code = code.replace(f'"{escaped}"', var_name)
        return code

    def validate_syntax(self, code: str) -> bool:
        """验证生成的代码是否为合法 Python。"""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
