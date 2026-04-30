# Codegen Pipeline Fix Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix two code generation pipeline bugs — P1 CSS filter strict mode violation, P2 evaluate-to-fill conversion for input actions.

**Architecture:** P1 is a 1-line fix in `locator_chain_builder.py`. P2 adds evaluate smart detection in `step_code_buffer.py` — detect JS input-value-setting patterns, extract text, reuse preceding click's locator, generate `.fill()` code.

**Tech Stack:** Python 3.11, no test suite — verify via pyflakes + import check.

---

### Task 1: P1 — CSS filter 追加 `.first`

**Files:**
- Modify: `backend/core/locator_chain_builder.py:171`

**Step 1: 修改代码**

`backend/core/locator_chain_builder.py` 第 171 行：

```python
# 前:
return f'{base}.filter(has_text="{escaped_name}")'
# 后:
return f'{base}.filter(has_text="{escaped_name}").first'
```

**Step 2: 验证语法**

Run: `python -c "import ast; ast.parse(open('backend/core/locator_chain_builder.py').read()); print('OK')"`
Expected: `OK`

**Step 3: pyflakes 检查**

Run: `python -m pyflakes backend/core/locator_chain_builder.py`
Expected: 无输出（零警告）

**Step 4: Commit**

```bash
git add backend/core/locator_chain_builder.py
git commit -m "fix: add .first to CSS filter locator to avoid strict mode violation"
```

---

### Task 2: P2 — evaluate 智能转换（核心实现）

**Files:**
- Modify: `backend/core/step_code_buffer.py:59-83`（`append_step` 方法）
- Modify: `backend/core/step_code_buffer.py`（新增 `_try_convert_evaluate_to_fill` 和 `_extract_fill_value_from_js` 方法）

**Step 1: 新增 `_extract_fill_value_from_js` 静态方法**

在 `StepCodeBuffer` 类中 `_is_popup_element` 方法之后添加：

```python
@staticmethod
def _extract_fill_value_from_js(code: str) -> str | None:
    """从 evaluate 的 JS 代码中提取 input 填入的文本值。

    检测两种常见模式:
    1. nativeInputValueSetter: setter.call(element, "value")
    2. 直接赋值: element.value = "value" 或 element.value = 'value'

    Args:
        code: evaluate action 的 JavaScript 代码字符串。

    Returns:
        提取到的文本值，或 None。
    """
    import re

    # 模式 1: setter.call(inp, "xxx123") 或 setter.call(inp, 'xxx123')
    setter_match = re.search(
        r'setter\.call\([^,]+,\s*"((?:[^"\\]|\\.)*)"\)', code
    ) or re.search(
        r"setter\.call\([^,]+,\s*'((?:[^'\\]|\\.)*')'\)", code
    )
    if setter_match:
        return setter_match.group(1).replace('\\"', '"').replace("\\'", "'")

    # 模式 2: .value = "xxx" 或 .value = 'xxx'
    value_match = re.search(
        r'\.value\s*=\s*"((?:[^"\\]|\\.)*)"', code
    ) or re.search(
        r"\.value\s*=\s*'((?:[^'\\]|\\.)*)'", code
    )
    if value_match:
        return value_match.group(1).replace('\\"', '"').replace("\\'", "'")

    return None
```

**Step 2: 新增 `_try_convert_evaluate_to_fill` 方法**

在 `_extract_fill_value_from_js` 方法之后添加：

```python
def _try_convert_evaluate_to_fill(
    self, action_dict: dict, translated: TranslatedAction,
) -> TranslatedAction | None:
    """尝试将 evaluate 设置 input 值的操作转换为 .fill() 代码。

    检测 evaluate action 是否在设置 input 元素的值，如果是则复用
    前一步 click 操作的定位器生成 .fill(value) 代码。

    Args:
        action_dict: 原始操作字典。
        translated: 翻译后的 TranslatedAction。

    Returns:
        转换后的 TranslatedAction，或 None（无法转换时保留原始 evaluate）。
    """
    # 仅处理 evaluate 类型
    action_type = ActionTranslator._identify_action_type(action_dict)
    if action_type != "evaluate":
        return None

    # 从 JS 代码中提取填入值
    params = action_dict.get("evaluate", {})
    js_code = params.get("code", "")
    if not js_code:
        return None

    fill_value = self._extract_fill_value_from_js(js_code)
    if fill_value is None:
        return None

    # 从前一步 click 复用定位器
    if not self._records:
        return None

    prev_record = self._records[-1]
    if prev_record.action.action_type != "click":
        return None

    # 复用前一步的定位器链
    prev_locators = prev_record.action.locators
    if not prev_locators:
        return None

    # 用第一个定位器生成 fill 代码
    escaped_value = fill_value.replace("\\", "\\\\").replace('"', '\\"')
    primary_locator = prev_locators[0]

    # 生成回退代码（复用定位器链）
    if len(prev_locators) == 1:
        code = (
            "    try:\n"
            f'        {primary_locator}.fill("{escaped_value}", timeout=5000)\n'
            "    except Exception as _e1:\n"
            f'        _logger.warning("定位器失败 [fill], 等待重试: {primary_locator[:40]}")\n'
            "        try:\n"
            f"            {primary_locator}.wait_for(state='visible', timeout=5000)\n"
            f'            {primary_locator}.fill("{escaped_value}", timeout=5000)\n'
            "        except Exception as _e2:\n"
            f'            _logger.error("定位器重试失败 [fill]")\n'
            "            raise HealerError(\n"
            f'                action_type="input",\n'
            f"                locators=(repr({primary_locator}),),\n"
            f"                original_error=str(_e2))"
        )
    else:
        # 多定位器回退
        escaped_value = fill_value.replace("\\", "\\\\").replace('"', '\\"')
        action_suffix = f'.fill("{escaped_value}", timeout=5000)'
        from backend.core.action_translator import ActionTranslator
        translator = ActionTranslator()
        code = translator._build_fallback_code(
            list(prev_locators), action_suffix, "input"
        )

    return TranslatedAction(
        code=code,
        action_type="input",
        is_comment=False,
        has_locator=True,
        locators=prev_locators,
    )
```

**Step 3: 修改 `append_step` 方法**

在 `append_step` 方法中，翻译完成后、创建 StepRecord 之前，插入 evaluate 转换逻辑：

`backend/core/step_code_buffer.py` 第 69-83 行，替换为：

```python
def append_step(self, action_dict: dict, duration: float | None = None) -> None:
    """同步翻译 action_dict 并存储为 StepRecord。"""
    # 同步翻译操作
    translated = self._translator.translate(action_dict)

    # P2: evaluate 智能转换 — 检测 JS 设置 input 值并转换为 .fill()
    converted = self._try_convert_evaluate_to_fill(action_dict, translated)
    if converted is not None:
        translated = converted

    # 推导等待策略
    action_type = ActionTranslator._identify_action_type(action_dict)
    if converted is not None:
        action_type = "input"  # 转换后按 input 类型推导等待
    wait_code = self._derive_wait(action_type, duration, action_dict)

    # 创建 StepRecord 并追加
    record = StepRecord(
        action=translated,
        wait_before=wait_code,
        step_index=self._next_index,
    )
    self._records.append(record)
    self._next_index += 1
```

**Step 4: 验证语法**

Run: `python -c "import ast; ast.parse(open('backend/core/step_code_buffer.py').read()); print('OK')"`
Expected: `OK`

**Step 5: pyflakes 检查**

Run: `python -m pyflakes backend/core/step_code_buffer.py`
Expected: 无输出（零警告）

**Step 6: 导入验证**

Run: `python -c "from backend.core.step_code_buffer import StepCodeBuffer; print('Import OK')"`
Expected: `Import OK`

**Step 7: Commit**

```bash
git add backend/core/step_code_buffer.py
git commit -m "feat: convert evaluate input-value-setting JS to .fill() in codegen pipeline"
```

---

### Task 3: 端到端验证

**Step 1: 重新触发代码生成**

在前端 UI 中触发一次 "销售出库-未收款测试" 的代码生成。

**Step 2: 检查生成代码**

验证生成代码中：
- CSS filter 包含 `.first`（如 `page.locator("span.el-dropdown-link").filter(has_text="添加").first`）
- evaluate 设置 input 值的操作已转换为 `.fill("xxx")` 而非 `page.evaluate("...")`

**Step 3: 执行生成的测试代码**

Run: `cd outputs/<run_id>/generated && python -m pytest test_<run_id>.py -v`
Expected: returncode=0

**Step 4: 最终 commit（如有手动调整）**

```bash
git add -A
git commit -m "fix: codegen pipeline P1+P2 verified end-to-end"
```
