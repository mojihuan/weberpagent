"""ActionTranslator -- 将 browser-use model_actions() 操作翻译为 Playwright Python 代码。

每个 model_actions() 条目翻译为一条 TranslatedAction，包含 Playwright API 调用字符串。
处理 10 种核心操作类型 (per D-08)，其他类型生成注释 (per D-09)。

Phase 83 扩展: click/input 操作支持多定位器 try-except 回退 (per D-04/D-05)。
Phase 100 扩展: 新增 wait/evaluate/select_dropdown/upload_file 4 种可执行类型。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from backend.core.healer_error import HealerError
from backend.core.locator_chain_builder import LocatorChainBuilder


@dataclass(frozen=True)
class TranslatedAction:
    """单个操作的 Playwright 翻译结果（不可变）。"""

    code: str  # 生成的 Playwright 代码行（可能是多行 try-except）
    action_type: str  # 原始操作类型
    is_comment: bool  # True 表示代码是注释（未翻译的操作）
    has_locator: bool  # True 表示使用了定位器
    locators: tuple[str, ...] = ()  # 定位器链元数据，用于调试和 Phase 84


class ActionTranslator:
    """将 browser-use actions 翻译为 Playwright Python 代码。

    处理 10 种核心操作类型 (per D-08):
    click, input, navigate, scroll, send_keys, go_back,
    wait, evaluate, select_dropdown, upload_file

    其他类型生成注释 (per D-09)。

    Phase 83: click/input 操作支持多定位器 try-except 回退 (per D-04/D-05)。
    Phase 100: 新增 wait/evaluate/select_dropdown/upload_file 翻译。
    """

    VIEWPORT_HEIGHT: int = 1000  # 滚动像素计算基准 (per Pitfall 3)

    _CORE_TYPES: set[str] = frozenset({
        "click",
        "input",
        "navigate",
        "scroll",
        "send_keys",
        "go_back",
        "wait",
        "evaluate",
        "select_dropdown",
        "upload_file",
    })

    def __init__(self) -> None:
        self._chain_builder = LocatorChainBuilder()

    # -- 公共接口 --------------------------------------------------------

    def translate(self, action: dict) -> TranslatedAction:
        """翻译单个 model_actions() 条目为 Playwright 代码。

        Args:
            action: model_actions() 返回的字典，包含操作参数和 interacted_element。

        Returns:
            TranslatedAction 包含生成的代码行和元数据。
        """
        action_type = self._identify_action_type(action)
        params = action.get(action_type, {})

        if action_type not in self._CORE_TYPES:
            return self._translate_unknown(action_type, params)

        elem = action.get("interacted_element")

        # 核心操作分派
        if action_type == "click":
            return self._translate_click(params, elem)
        if action_type == "input":
            return self._translate_input(params, elem)
        if action_type == "navigate":
            return self._translate_navigate(params)
        if action_type == "scroll":
            return self._translate_scroll(params)
        if action_type == "send_keys":
            return self._translate_send_keys(params)
        if action_type == "go_back":
            return self._translate_go_back()
        if action_type == "wait":
            return self._translate_wait(params)
        if action_type == "evaluate":
            return self._translate_evaluate(params)
        if action_type == "select_dropdown":
            return self._translate_select_dropdown(params, elem)
        if action_type == "upload_file":
            return self._translate_upload_file(params, elem)

        # 不应到达此处（已在 _CORE_TYPES 检查中过滤）
        return self._translate_unknown(action_type, params)

    def translate_with_llm(
        self, action: dict, llm_snippet: str = ""
    ) -> TranslatedAction:
        """翻译操作并插入 LLM 修复代码作为第 4 层回退。

        与 translate() 行为一致，但 click/input 操作的多定位器回退代码
        会额外插入 LLM 修复层。

        Args:
            action: model_actions() 返回的字典。
            llm_snippet: LLM 生成的 Playwright 代码片段（空字符串 = 无 LLM 层）。

        Returns:
            TranslatedAction 包含生成的代码行和元数据。
        """
        action_type = self._identify_action_type(action)
        params = action.get(action_type, {})

        if action_type not in self._CORE_TYPES:
            return self._translate_unknown(action_type, params)

        elem = action.get("interacted_element")

        if action_type == "click":
            return self._translate_click(params, elem, llm_snippet=llm_snippet)
        if action_type == "input":
            return self._translate_input(params, elem, llm_snippet=llm_snippet)
        if action_type == "navigate":
            return self._translate_navigate(params)
        if action_type == "scroll":
            return self._translate_scroll(params)
        if action_type == "send_keys":
            return self._translate_send_keys(params)
        if action_type == "go_back":
            return self._translate_go_back()
        if action_type == "wait":
            return self._translate_wait(params)
        if action_type == "evaluate":
            return self._translate_evaluate(params)
        if action_type == "select_dropdown":
            return self._translate_select_dropdown(params, elem)
        if action_type == "upload_file":
            return self._translate_upload_file(params, elem)

        return self._translate_unknown(action_type, params)

    # -- 私有方法 --------------------------------------------------------

    @staticmethod
    def _identify_action_type(action: dict) -> str:
        """识别 action dict 中的操作类型键。

        model_actions() 返回的 dict 格式：
        {"click": {"index": 5}, "interacted_element": ...}
        操作类型键是除 "interacted_element" 以外的键。
        """
        for key in action:
            if key != "interacted_element":
                return key
        return "unknown"

    @staticmethod
    def _extract_xpath(action: dict) -> str | None:
        """从 interacted_element 安全提取 XPath (per D-05, D-06)。

        DOMInteractedElement 是 dataclass，使用属性访问 (elem.x_path)，
        不是字典访问 (elem["x_path"]) (per Pitfall 1)。
        """
        elem = action.get("interacted_element")
        if elem is None:
            return None
        xpath = elem.x_path  # 属性访问，不是字典访问
        return xpath if xpath else None

    @staticmethod
    def _build_placeholder(action_type: str) -> TranslatedAction:
        """生成定位器缺失时的占位符 (per D-06)。"""
        return TranslatedAction(
            code='    page.wait_for_timeout(1000)  # TODO: 定位器缺失',
            action_type=action_type,
            is_comment=False,
            has_locator=False,
        )

    @staticmethod
    def _build_llm_only_code(action_type: str, llm_snippet: str) -> TranslatedAction:
        """生成仅包含 LLM 修复代码的 TranslatedAction。

        当 elem=None 或无定位器但有 LLM snippet 时使用。
        将 LLM 代码包装在 try-except 中，失败时 raise HealerError。
        """
        escaped_snippet = llm_snippet.replace("\\", "\\\\").replace('"', '\\"')
        code = (
            f'    _healer.info("LLM 修复: {escaped_snippet[:80]}")\n'
            f"    try:\n"
            f"        {llm_snippet}\n"
            f"    except Exception as _e:\n"
            f'        _healer.error("LLM 修复失败 [{action_type}]")\n'
            f'        raise HealerError('
            f'action_type="{action_type}", '
            f"locators=(), "
            f"original_error=str(_e))"
        )
        return TranslatedAction(
            code=code,
            action_type=action_type,
            is_comment=False,
            has_locator=True,
            locators=(),
        )

    def _translate_click(
        self, params: dict, elem: Any, *, llm_snippet: str = ""
    ) -> TranslatedAction:
        """click -> page.locator("xpath=...").click()

        有多定位器时生成 try-except 回退代码 (per D-04/D-05)。
        当 llm_snippet 非空时，作为第 4 层 LLM 回退插入。
        当 elem=None 但 llm_snippet 非空时，直接使用 LLM 代码。
        """
        if elem is None:
            if llm_snippet:
                return self._build_llm_only_code("click", llm_snippet)
            return self._build_placeholder("click")

        locators = self._chain_builder.extract(elem, "click")
        if not locators:
            if llm_snippet:
                return self._build_llm_only_code("click", llm_snippet)
            return self._build_placeholder("click")

        # 单定位器: 保持 Phase 82 格式 (per Pitfall 5)
        if len(locators) == 1:
            escaped = self._escape_string(elem.x_path)
            return TranslatedAction(
                code=f'    page.locator("xpath={escaped}").click()',
                action_type="click",
                is_comment=False,
                has_locator=True,
            )

        # 多定位器: 生成 try-except 回退代码 (含可选 LLM 第 4 层)
        code = self._build_fallback_code(
            locators, ".click()", "click", llm_snippet=llm_snippet
        )
        return TranslatedAction(
            code=code,
            action_type="click",
            is_comment=False,
            has_locator=True,
            locators=tuple(locators),
        )

    def _translate_input(
        self, params: dict, elem: Any, *, llm_snippet: str = ""
    ) -> TranslatedAction:
        """input -> page.locator("xpath=...").fill(text)

        有多定位器时生成 try-except 回退代码 (per D-04/D-05)。
        当 llm_snippet 非空时，作为第 4 层 LLM 回退插入。
        当 elem=None 但 llm_snippet 非空时，直接使用 LLM 代码。
        """
        if elem is None:
            if llm_snippet:
                return self._build_llm_only_code("input", llm_snippet)
            return self._build_placeholder("input")

        locators = self._chain_builder.extract(elem, "input")
        if not locators:
            if llm_snippet:
                return self._build_llm_only_code("input", llm_snippet)
            return self._build_placeholder("input")

        text = params.get("text", "")
        escaped_text = self._escape_string(text)
        action_suffix = f'.fill("{escaped_text}")'

        # 单定位器: 保持 Phase 82 格式
        if len(locators) == 1:
            escaped_xpath = self._escape_string(elem.x_path)
            return TranslatedAction(
                code=f'    page.locator("xpath={escaped_xpath}").fill("{escaped_text}")',
                action_type="input",
                is_comment=False,
                has_locator=True,
            )

        # 多定位器: 生成 try-except 回退代码 (含可选 LLM 第 4 层)
        code = self._build_fallback_code(
            locators, action_suffix, "input", llm_snippet=llm_snippet
        )
        return TranslatedAction(
            code=code,
            action_type="input",
            is_comment=False,
            has_locator=True,
            locators=tuple(locators),
        )

    def _build_fallback_code(
        self,
        locators: list[str],
        action_suffix: str,
        action_type: str,
        *,
        llm_snippet: str = "",
    ) -> str:
        """生成 try-except 回退代码 (per D-04/D-05).

        所有定位器失败时 raise HealerError (per D-07)。
        回退成功记录 warning 级别日志 (per D-08)。
        当 llm_snippet 非空时，在 HealerError 之前插入 LLM 修复层 (Phase 84)。
        """
        lines: list[str] = []
        indent = "    "  # 函数体缩进

        if len(locators) == 2:
            # 两级: 外层 try -> except (try 第二个) -> except (LLM 或 raise HealerError)
            lines.append(f"{indent}try:")
            lines.append(f"{indent}    {locators[0]}{action_suffix}")
            lines.append(f"{indent}except Exception as _e1:")
            short0 = self._short_locator(locators[0])
            short1 = self._short_locator(locators[1])
            lines.append(
                f'{indent}    _healer.warning("定位器回退: {short0} 失败, 尝试 {short1}")'
            )
            lines.append(f"{indent}    try:")
            lines.append(f"{indent}        {locators[1]}{action_suffix}")
            lines.append(f"{indent}    except Exception as _e2:")
            if llm_snippet:
                self._append_llm_layer(lines, indent * 3, llm_snippet, action_type, locators, "_e3")
            else:
                short_all = ", ".join(self._short_locator(l) for l in locators)
                lines.append(
                    f'{indent}        _healer.error("定位器全部失败 [{action_type}]: {short_all}")'
                )
                locators_repr = ", ".join(repr(l) for l in locators)
                lines.append(
                    f"{indent}        raise HealerError("
                    f'action_type="{action_type}", '
                    f"locators=({locators_repr}), "
                    f"original_error=str(_e2))"
                )

        elif len(locators) == 3:
            # 三级嵌套
            lines.append(f"{indent}try:")
            lines.append(f"{indent}    {locators[0]}{action_suffix}")
            lines.append(f"{indent}except Exception as _e1:")
            short0 = self._short_locator(locators[0])
            short1 = self._short_locator(locators[1])
            lines.append(
                f'{indent}    _healer.warning("定位器回退: {short0} 失败, 尝试 {short1}")'
            )
            lines.append(f"{indent}    try:")
            lines.append(f"{indent}        {locators[1]}{action_suffix}")
            lines.append(f"{indent}    except Exception as _e2:")
            short1b = self._short_locator(locators[1])
            short2 = self._short_locator(locators[2])
            lines.append(
                f'{indent}        _healer.warning("定位器回退: {short1b} 失败, 尝试 {short2}")'
            )
            lines.append(f"{indent}        try:")
            lines.append(f"{indent}            {locators[2]}{action_suffix}")
            lines.append(f"{indent}        except Exception as _e3:")
            if llm_snippet:
                self._append_llm_layer(lines, indent * 4, llm_snippet, action_type, locators, "_e4")
            else:
                short_all = ", ".join(self._short_locator(l) for l in locators)
                lines.append(
                    f'{indent}            _healer.error("定位器全部失败 [{action_type}]: {short_all}")'
                )
                locators_repr = ", ".join(repr(l) for l in locators)
                lines.append(
                    f"{indent}            raise HealerError("
                    f'action_type="{action_type}", '
                    f"locators=({locators_repr}), "
                    f"original_error=str(_e3))"
                )

        return "\n".join(lines)

    def _append_llm_layer(
        self,
        lines: list[str],
        base_indent: str,
        llm_snippet: str,
        action_type: str,
        locators: list[str],
        except_var: str,
    ) -> None:
        """向 lines 追加 LLM 修复 try-except 层。

        Args:
            lines: 当前正在构建的代码行列表。
            base_indent: LLM 层的缩进（最内层 except 块内部）。
            llm_snippet: LLM 生成的 Playwright 代码。
            action_type: 操作类型。
            locators: 已失败的定位器列表。
            except_var: LLM 层的 except 变量名（如 "_e3", "_e4"）。
        """
        short_llm = self._escape_string(llm_snippet[:80])
        short_all = ", ".join(self._short_locator(l) for l in locators)
        locators_repr = ", ".join(repr(l) for l in locators)

        lines.append(
            f'{base_indent}_healer.info("LLM 修复: {short_llm}")'
        )
        lines.append(f"{base_indent}try:")
        lines.append(f"{base_indent}    {llm_snippet}")
        lines.append(f"{base_indent}except Exception as {except_var}:")
        lines.append(
            f'{base_indent}    _healer.error("定位器全部失败（含 LLM 修复）[{action_type}]: {short_all}")'
        )
        lines.append(
            f"{base_indent}    raise HealerError("
            f'action_type="{action_type}", '
            f"locators=({locators_repr}), "
            f"original_error=str({except_var}))"
        )

    @staticmethod
    def _short_locator(locator: str) -> str:
        """从完整定位器表达式提取简短描述用于日志。

        返回不含双引号的简短描述，避免嵌入日志字符串时引号冲突。
        使用单引号包裹标识符，确保日志字符串中的可读性。
        """
        # page.locator("xpath=...") -> xpath=...
        xpath_match = re.search(r'page\.locator\("xpath=(.+?)"\)', locator)
        if xpath_match:
            return f"xpath={xpath_match.group(1)}"

        # page.locator("[id='...']") -> id=...
        id_match = re.search(r'page\.locator\("\[id=\\\\?"(.+?)\\\\?"\]"\)', locator)
        if id_match:
            return f"id={id_match.group(1)}"

        # page.locator("[id=...]") 通用匹配
        id_match2 = re.search(r'\[id=.+?"(.+?)".*?\]', locator)
        if id_match2:
            return f"id={id_match2.group(1)}"

        # page.get_by_test_id("...") -> test_id=...
        testid_match = re.search(r'page\.get_by_test_id\("(.+?)"\)', locator)
        if testid_match:
            return f"test_id={testid_match.group(1)}"

        # page.get_by_role("...", name="...") -> role=button name=Submit
        role_match = re.search(r'page\.get_by_role\("(.+?)"(?:,\s*name="(.+?)")?\)', locator)
        if role_match:
            role = role_match.group(1)
            name = role_match.group(2)
            if name:
                return f"role={role} name={name}"
            return f"role={role}"

        # page.get_by_placeholder("...") -> placeholder=...
        placeholder_match = re.search(r'page\.get_by_placeholder\("(.+?)"\)', locator)
        if placeholder_match:
            return f"placeholder={placeholder_match.group(1)}"

        # page.get_by_text("...", exact=True) -> text=...
        text_match = re.search(r'page\.get_by_text\("(.+?)"', locator)
        if text_match:
            return f"text={text_match.group(1)}"

        # 通用回退: 截断到合理长度
        return locator[:50]

    @staticmethod
    def _translate_navigate(params: dict) -> TranslatedAction:
        """navigate -> page.goto(url)"""
        url = params.get("url", "")
        escaped = ActionTranslator._escape_string(url)
        return TranslatedAction(
            code=f'    page.goto("{escaped}")',
            action_type="navigate",
            is_comment=False,
            has_locator=False,
        )

    def _translate_scroll(self, params: dict) -> TranslatedAction:
        """scroll -> page.mouse.wheel(0, delta)

        delta = int(pages * VIEWPORT_HEIGHT) * (1 if down else -1)
        (per Pitfall 3)
        """
        down = params.get("down", True)
        pages = params.get("pages", 1.0)
        delta = int(pages * self.VIEWPORT_HEIGHT) * (1 if down else -1)
        return TranslatedAction(
            code=f"    page.mouse.wheel(0, {delta})",
            action_type="scroll",
            is_comment=False,
            has_locator=False,
        )

    @staticmethod
    def _translate_send_keys(params: dict) -> TranslatedAction:
        """send_keys -> page.keyboard.press(keys)"""
        keys = params.get("keys", "")
        escaped = ActionTranslator._escape_string(keys)
        return TranslatedAction(
            code=f'    page.keyboard.press("{escaped}")',
            action_type="send_keys",
            is_comment=False,
            has_locator=False,
        )

    @staticmethod
    def _translate_go_back() -> TranslatedAction:
        """go_back -> page.go_back()"""
        return TranslatedAction(
            code="    page.go_back()",
            action_type="go_back",
            is_comment=False,
            has_locator=False,
        )

    @staticmethod
    def _translate_wait(params: dict) -> TranslatedAction:
        """wait -> page.wait_for_timeout(seconds * 1000)

        browser-use wait(seconds=3) -- seconds defaults to 3.
        model_dump() outputs {"wait": {}} or {"wait": {"seconds": 5}}.
        """
        seconds = params.get("seconds", 3)
        ms = int(seconds * 1000)
        return TranslatedAction(
            code=f"    page.wait_for_timeout({ms})",
            action_type="wait",
            is_comment=False,
            has_locator=False,
        )

    @staticmethod
    def _translate_evaluate(params: dict) -> TranslatedAction:
        """evaluate -> page.evaluate(code)

        browser-use evaluate(code="...") -- JavaScript code string.
        Defensively escape newlines and quotes to prevent syntax errors.
        """
        code_str = params.get("code", "")
        escaped = ActionTranslator._escape_string(code_str).replace("\n", "\\n")
        return TranslatedAction(
            code=f'    page.evaluate("{escaped}")',
            action_type="evaluate",
            is_comment=False,
            has_locator=False,
        )

    def _translate_select_dropdown(
        self, params: dict, elem: Any
    ) -> TranslatedAction:
        """select_dropdown -> page.locator("xpath=...").select_option(text)

        Uses single locator mode (per D-04). Falls back to comment when
        elem=None or no xpath (per D-05). No multi-locator fallback (per D-06).
        """
        if elem is None:
            return self._build_edge_comment("select_dropdown", params)
        locators = self._chain_builder.extract(elem, "select_dropdown")
        if not locators:
            return self._build_edge_comment("select_dropdown", params)
        text = params.get("text", "")
        escaped_text = self._escape_string(text)
        return TranslatedAction(
            code=f'    {locators[0]}.select_option("{escaped_text}")',
            action_type="select_dropdown",
            is_comment=False,
            has_locator=True,
        )

    def _translate_upload_file(
        self, params: dict, elem: Any
    ) -> TranslatedAction:
        """upload_file -> page.locator("xpath=...").set_input_files(path)

        Uses single locator mode (per D-04). Falls back to comment when
        elem=None or no xpath (per D-05). No multi-locator fallback (per D-06).
        """
        if elem is None:
            return self._build_edge_comment("upload_file", params)
        locators = self._chain_builder.extract(elem, "upload_file")
        if not locators:
            return self._build_edge_comment("upload_file", params)
        path = params.get("path", "")
        escaped_path = self._escape_string(path)
        return TranslatedAction(
            code=f'    {locators[0]}.set_input_files("{escaped_path}")',
            action_type="upload_file",
            is_comment=False,
            has_locator=True,
        )

    @staticmethod
    def _build_edge_comment(action_type: str, params: dict) -> TranslatedAction:
        """生成定位器缺失时的注释回退 (per D-05).

        select_dropdown/upload_file 无定位器时使用此方法，
        不触发 LLM healing (per D-06)。
        """
        return TranslatedAction(
            code=f"    # {action_type}: 定位器缺失 {params}",
            action_type=action_type,
            is_comment=True,
            has_locator=False,
        )

    @staticmethod
    def _translate_unknown(action_type: str, params: dict) -> TranslatedAction:
        """边缘操作生成有意义的参数摘要注释 (per D-07/D-08).

        不在 _CORE_TYPES 中的操作类型按类型生成包含参数摘要的注释。
        真正未知的操作类型生成通用回退注释。
        """
        # 按操作类型定义参数摘要生成函数
        summaries: dict[str, callable] = {
            "switch": lambda p: f"切换到标签页 #{p.get('tab_id', '?')}",
            "close": lambda p: f"关闭标签页 #{p.get('tab_id', '?')}",
            "search_page": lambda p: f"搜索页面: {p.get('pattern', '')}",
            "find_elements": lambda p: f"查找元素: {p.get('selector', '')}",
            "find_text": lambda p: f"查找文本: {p.get('text', p.get('pattern', ''))}",
            "screenshot": lambda p: f"截图 -> {p['file_name']}" if p.get("file_name") else "截图",
            "save_as_pdf": lambda p: f"保存 PDF -> {p['file_name']}" if p.get("file_name") else "保存 PDF",
            "done": lambda p: f"任务完成: {p.get('text', '')[:50]}",
            "write_file": lambda p: f"写入文件: {p.get('file_name', '')}",
            "read_file": lambda p: f"读取文件: {p.get('file_name', '')}",
            "replace_file": lambda p: f"替换文件内容: {p.get('file_name', '')}",
            "search": lambda p: f"搜索: {p.get('query', '')} ({p.get('engine', 'duckduckgo')})",
            "dropdown_options": lambda p: f"获取下拉选项 (元素 #{p.get('index', '?')})",
            "extract": lambda p: f"提取数据: {p.get('query', '')[:50]}",
        }

        summarizer = summaries.get(action_type)
        if summarizer:
            summary = summarizer(params)
        else:
            # D-01: 显示原始参数摘要，QA 可从参数看出发生了什么
            summary = f"参数={params}"

        # 处理 summary 中的换行符，确保每行都有 # 前缀 (per EXEC-02)
        if "\n" in summary:
            lines = summary.split("\n")
            prefixed_lines = [f"    # {action_type}: {lines[0]}"] + [f"    # {line}" for line in lines[1:]]
            comment_code = "\n".join(prefixed_lines)
        else:
            comment_code = f"    # {action_type}: {summary}"

        return TranslatedAction(
            code=comment_code,
            action_type=action_type,
            is_comment=True,
            has_locator=False,
        )

    @staticmethod
    def _escape_string(value: str) -> str:
        """转义字符串中的特殊字符，防止生成的代码语法错误。

        对双引号和反斜杠进行转义，确保生成的 Playwright 代码字符串有效。
        XPath 路径通常不包含引号 (per Pitfall 2)，但做防御性转义。
        """
        return value.replace("\\", "\\\\").replace('"', '\\"')
