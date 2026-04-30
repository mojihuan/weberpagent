# 定位器策略改进 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 改进 Playwright 测试代码生成的定位器策略：CSS 选择器增加文本过滤消除泛化问题，回退链增加前置等待提升可靠性。

**Architecture:** 修改两个管道文件 — `locator_chain_builder.py` 的 CSS 选择器生成逻辑增加 ax_name 文本过滤；`action_translator.py` 的回退代码生成增加 `wait_for(state="visible")` 前置等待。

**Tech Stack:** Python 3.11, Playwright locators, Element UI ERP 应用

---

### Task 1: CSS 选择器增加文本过滤

**Files:**
- Modify: `backend/core/locator_chain_builder.py:113-116` (调用处)
- Modify: `backend/core/locator_chain_builder.py:145-167` (`_build_class_selector` 方法)

**Step 1: 修改 `_build_class_selector` 方法签名和实现**

将 `ax_name` 参数加入方法签名。当 `ax_name` 非空时生成 `.filter(has_text="...")` 替代 `.first`。

把方法从 `@staticmethod` 改为普通方法（或保持 static 增加 `ax_name` 参数）：

```python
@staticmethod
def _build_class_selector(class_value: str, node_name: str, ax_name: str | None = None) -> str | None:
    """从 class 属性生成 CSS 选择器定位器。

    选择第一个有意义的 CSS class（排除过短的通用 class），
    与 tag name 组合成 CSS 选择器。

    当 ax_name 存在时，使用 .filter(has_text="...") 精确定位；
    否则使用 .first 避免 strict mode 冲突。

    Args:
        class_value: 元素的 class 属性值。
        node_name: 元素标签名（大写）。
        ax_name: 元素的 accessible name，用于文本过滤。

    Returns:
        CSS 选择器定位器字符串，或 None。
    """
    classes = class_value.split()
    tag = node_name.lower()
    for cls in classes:
        if len(cls) < 5:
            continue
        escaped_cls = _escape_string(cls)
        base = f'page.locator("{tag}.{escaped_cls}")'
        if ax_name:
            escaped_name = _escape_string(ax_name)
            return f'{base}.filter(has_text="{escaped_name}")'
        return f'{base}.first'
    return None
```

**Step 2: 更新 `extract` 方法中的调用处**

在 `extract` 方法中，将 `ax_name` 传给 `_build_class_selector`：

当前代码（第 113-116 行）：
```python
class_value = attrs.get("class", "")
if class_value and len(locators) < 3:
    css_selector = self._build_class_selector(class_value, elem.node_name)
```

改为：
```python
class_value = attrs.get("class", "")
if class_value and len(locators) < 3:
    css_selector = self._build_class_selector(class_value, elem.node_name, ax_name=ax_name)
```

**Step 3: 验证语法**

Run: `cd /Users/huhu/project/weberpagent && python -c "import ast; ast.parse(open('backend/core/locator_chain_builder.py').read()); print('OK')"`
Expected: OK

**Step 4: 提交**

```bash
git add backend/core/locator_chain_builder.py
git commit -m "feat: CSS class locator adds text filter when ax_name available"
```

---

### Task 2: 回退链增加前置等待

**Files:**
- Modify: `backend/core/action_translator.py:344-425` (`_build_fallback_code` 方法)

**Step 1: 修改两定位器回退代码生成**

在 `locators[1]` 操作前增加 `wait_for`：

当前代码（第 371-372 行）：
```python
lines.append(f"{indent}    try:")
lines.append(f"{indent}        {locators[1]}{action_suffix}")
```

改为：
```python
lines.append(f"{indent}    try:")
lines.append(f"{indent}        {locators[1]}.wait_for(state='visible', timeout=3000)")
lines.append(f"{indent}        {locators[1]}{action_suffix}")
```

**Step 2: 修改三定位器回退代码生成**

在 `locators[1]` 和 `locators[2]` 操作前增加 `wait_for`：

当前代码（第 399-400 行）：
```python
lines.append(f"{indent}    try:")
lines.append(f"{indent}        {locators[1]}{action_suffix}")
```

改为：
```python
lines.append(f"{indent}    try:")
lines.append(f"{indent}        {locators[1]}.wait_for(state='visible', timeout=3000)")
lines.append(f"{indent}        {locators[1]}{action_suffix}")
```

当前代码（第 407-408 行）：
```python
lines.append(f"{indent}        try:")
lines.append(f"{indent}            {locators[2]}{action_suffix}")
```

改为：
```python
lines.append(f"{indent}        try:")
lines.append(f"{indent}            {locators[2]}.wait_for(state='visible', timeout=3000)")
lines.append(f"{indent}            {locators[2]}{action_suffix}")
```

**Step 3: 验证语法**

Run: `cd /Users/huhu/project/weberpagent && python -c "import ast; ast.parse(open('backend/core/action_translator.py').read()); print('OK')"`
Expected: OK

**Step 4: 提交**

```bash
git add backend/core/action_translator.py
git commit -m "feat: fallback locators add wait_for before action for reliability"
```

---

### Task 3: 端到端验证

**Step 1: 启动后端服务，执行一次测试用例生成**

通过 UI 或 API 触发一次测试用例生成，验证生成代码中：
- CSS 选择器包含 `.filter(has_text="...")` 而不是 `.first`（当 ax_name 存在时）
- 回退定位器包含 `.wait_for(state='visible', timeout=3000)` 前置等待

**Step 2: 检查生成的测试代码能正常运行**

验证 pytest 执行生成的测试不再出现之前的定位器失败问题。
