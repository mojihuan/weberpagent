# 前置条件自包含代码生成 — 实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将前置条件代码（随机数据生成等）嵌入生成的 Playwright 测试文件中，使 fill() 中的硬编码值替换为变量引用，实现完全自包含的可运行测试。

**Architecture:** 通过 Jinja2 替换追踪的 variable_map（变量名→实际值），在代码生成阶段反向替换 fill/select 中的硬编码值。前置条件代码和随机函数定义内联到生成文件中。

**Tech Stack:** Python, Playwright, Jinja2

**Design doc:** `docs/plans/2026-04-30-precondition-self-contained-design.md`

---

### Task 1: 扩展 `code_generator.py` — 前置条件代码注入

**Files:**
- Modify: `backend/core/code_generator.py:34-131` (generate 方法)
- Modify: `backend/core/code_generator.py:194-213` (_build_precondition 方法)

**Step 1: 扩展 `generate()` 方法签名**

在 `generate()` 方法中新增两个参数：
- `precondition_code: list[str] | None = None` — 用户编写的前置条件代码列表
- `variable_map: dict[str, str] | None = None` — 变量名→实际值映射

```python
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
```

**Step 2: 在 `generate()` 中注入随机函数定义和前置条件代码**

在 `parts.append(f"def {func_name}...")` 之后，`_build_precondition` 之前，注入：

```python
        # 注入随机函数定义和前置条件代码
        if precondition_code:
            # 确定需要哪些随机函数（通过分析前置条件代码中的调用）
            needed_funcs = self._detect_needed_functions(precondition_code)
            if needed_funcs:
                parts.append("")  # 空行分隔
                for func_def in needed_funcs:
                    parts.append(func_def)
            # 注入前置条件代码（缩进为函数体内）
            parts.append("    # === Precondition: 动态数据生成 ===")
            for code_line in precondition_code:
                stripped = code_line.strip()
                if stripped:
                    parts.append(f"    {stripped}")
            parts.append("")
```

注意：随机函数定义放在 `def test_xxx()` 之前（模块级别），前置条件赋值语句放在函数体内。

**Step 3: 新增 `_detect_needed_functions` 方法**

分析前置条件代码中调用了哪些随机函数，返回对应的函数定义字符串列表：

```python
    _RANDOM_FUNC_DEFS = {
        "random_imei": [
            "def random_imei():",
            '    return "I" + \'\'\'.join(random.choices("0123456789", k=14))',
        ],
        "random_phone": [
            "def random_phone():",
            '    return "13" + \'\'\'.join(random.choices("0123456789", k=9))',
        ],
        "sf_waybill": [
            "def sf_waybill():",
            '    uuid_hex = uuid.uuid4().hex[:12].upper()',
            '    return f"SF{uuid_hex}"',
        ],
        "random_serial": [
            "def random_serial():",
            '    return \'\'\'.join(random.choices("0123456789", k=8))',
        ],
        "random_numbers": [
            "def random_numbers(n):",
            '    return \'\'\'.join(random.choices("0123456789", k=n))',
        ],
    }

    @classmethod
    def _detect_needed_functions(cls, precondition_code: list[str]) -> list[str]:
        """检测前置条件代码需要哪些随机函数定义，返回函数定义字符串列表。"""
        all_code = "\n".join(precondition_code)
        needed: list[str] = []
        needs_random = False
        needs_uuid = False
        for func_name, func_lines in cls._RANDOM_FUNC_DEFS.items():
            if func_name + "(" in all_code:
                needed.extend(func_lines)
                needed.append("")
                if func_name in ("random_imei", "random_phone", "random_serial", "random_numbers"):
                    needs_random = True
                if func_name == "sf_waybill":
                    needs_random = True
                    needs_uuid = True
        return needed
```

同时需要在 import 部分添加条件 import：

```python
        # 条件 import: 前置条件需要的模块
        if precondition_code:
            all_pre_code = "\n".join(precondition_code)
            if "random_" in all_pre_code or "random.choices" in all_pre_code:
                parts.append("import random")
            if "uuid" in all_pre_code:
                parts.append("import uuid")
```

**Step 4: 新增 `_substitute_variables_in_code` 方法**

在组装完 body 后，用 variable_map 替换硬编码值：

```python
    @staticmethod
    def _substitute_variables_in_code(code: str, variable_map: dict[str, str]) -> str:
        """将生成的代码中 fill/select 的硬编码值替换为变量引用。

        只替换引号内的值，避免误替换变量名本身。
        按值长度降序排列，防止短值匹配到长值的子串。
        """
        if not variable_map:
            return code

        # 按值长度降序排列，防止子串误替换
        sorted_vars = sorted(variable_map.items(), key=lambda x: len(x[1]), reverse=True)
        for var_name, actual_value in sorted_vars:
            if not actual_value or not isinstance(actual_value, str):
                continue
            # 只替换引号内的值 (fill("value") → fill(var_name))
            escaped = actual_value.replace("\\", "\\\\").replace('"', '\\"')
            code = code.replace(f'"{escaped}"', var_name)
        return code
```

**Step 5: 在 `generate()` 中调用替换**

在 `body` 生成后、断言之前：

```python
        # 变量替换：fill 中的硬编码值 → 变量引用
        if body and variable_map:
            body = self._substitute_variables_in_code(body, variable_map)

        if body:
            parts.append(body)
```

**Step 6: 处理 `context.get_data()` 外部调用**

在注入前置条件代码时，检测 `get_data` 调用并添加注释：

```python
            for code_line in precondition_code:
                stripped = code_line.strip()
                if stripped:
                    if "get_data(" in stripped:
                        # 外部调用无法自包含，注释掉并使用变量硬编码
                        parts.append(f"    # NOTE: {stripped}")
                        parts.append(f"    #       外部调用无法自包含，使用执行时的值作为 fallback")
                        # 从 variable_map 找到变量赋值的 fallback
                        # 例如 context['warehouse'] = context.get_data(...) → warehouse = "实际值"
                        import re
                        assign_match = re.match(r"context\['(\w+)'\]\s*=", stripped)
                        if assign_match:
                            var_name = assign_match.group(1)
                            fallback_value = variable_map.get(var_name, "") if variable_map else ""
                            if fallback_value:
                                parts.append(f'    {var_name} = "{fallback_value}"  # fallback')
                    else:
                        parts.append(f"    {stripped}")
```

**Step 7: Commit**

```bash
git add backend/core/code_generator.py
git commit -m "feat: embed precondition code and random function defs in generated test files"
```

---

### Task 2: 扩展 `StepCodeBuffer.assemble()` — 传递变量映射

**Files:**
- Modify: `backend/core/step_code_buffer.py:288-353` (assemble 方法)

**Step 1: 扩展 `assemble()` 方法签名**

新增两个参数并传递给 `PlaywrightCodeGenerator.generate()`：

```python
    def assemble(
        self,
        run_id: str,
        task_name: str,
        task_id: str,
        precondition_config: dict | None = None,
        assertions_config: list[dict] | None = None,
        precondition_code: list[str] | None = None,
        variable_map: dict[str, str] | None = None,
    ) -> str:
```

在调用 `self._generator.generate()` 时传递新参数：

```python
        return self._generator.generate(
            run_id,
            task_name,
            task_id,
            flat_actions,
            precondition_config=precondition_config,
            assertions_config=assertions_config,
            precondition_code=precondition_code,
            variable_map=variable_map,
        )
```

**Step 2: Commit**

```bash
git add backend/core/step_code_buffer.py
git commit -m "feat: pass precondition_code and variable_map through StepCodeBuffer.assemble()"
```

---

### Task 3: 串联数据 — `run_pipeline.py`

**Files:**
- Modify: `backend/api/routes/run_pipeline.py:340-374` (_run_code_generation)
- Modify: `backend/api/routes/run_pipeline.py:462-530` (run_agent_background)

**Step 1: 扩展 `_run_code_generation` 函数签名**

新增 `precondition_code` 和 `variable_map` 参数：

```python
async def _run_code_generation(
    run_id: str,
    task_name: str,
    task_id: str,
    effective_target_url: str | None,
    run: Any,
    code_buffer: StepCodeBuffer,
    run_repo: RunRepository,
    precondition_code: list[str] | None = None,
    variable_map: dict[str, str] | None = None,
) -> None:
```

在 `code_buffer.assemble()` 调用中传递新参数：

```python
        _content = code_buffer.assemble(
            run_id=run_id, task_name=task_name, task_id=task_id,
            precondition_config=_precondition_config, assertions_config=_assertions_config,
            precondition_code=precondition_code,
            variable_map=variable_map,
        )
```

**Step 2: 在 `run_agent_background` 中传递数据**

在 `_run_code_generation` 调用处（约第 530 行），传递 `preconditions` 和 `context`：

```python
            await _run_code_generation(
                run_id, task_name, task_id, effective_target_url, run,
                code_buffer, run_repo,
                precondition_code=preconditions,
                variable_map=context if isinstance(context, dict) else None,
            )
```

**Step 3: 过滤 variable_map — 只保留字符串值**

`context` 中可能包含非字符串值（如 list, dict）或内部键（如 `assertion_results`）。在传递前过滤：

```python
            # 过滤 variable_map：只保留字符串/数字值，排除内部键
            _variable_map = None
            if isinstance(context, dict):
                _variable_map = {
                    k: str(v) for k, v in context.items()
                    if isinstance(v, (str, int, float)) and not k.startswith("assertion")
                }
                if not _variable_map:
                    _variable_map = None
```

**Step 4: Commit**

```bash
git add backend/api/routes/run_pipeline.py
git commit -m "feat: wire precondition code and variable map into code generation pipeline"
```

---

### Task 4: 端到端验证

**Step 1: 手动测试 — 无前置条件**

确认无前置条件时生成代码不变（回归测试）。

**Step 2: 手动测试 — 有前置条件**

创建一个带 `context['imei'] = random_imei()` 前置条件的任务，运行后检查生成的 `.py` 文件：
1. 包含 `import random`
2. 包含 `random_imei()` 函数定义
3. 函数体内包含 `imei = random_imei()`
4. fill 中的值替换为变量引用

**Step 3: 手动测试 — 外部调用降级**

创建一个带 `context.get_data(...)` 的前置条件，确认生成代码中有注释 + fallback。

**Step 4: Commit**

```bash
git commit --allow-empty -m "test: verify precondition self-contained code generation"
```
