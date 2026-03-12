# 基于区域的元素定位 实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 解决页面上多个相同文本元素的定位冲突问题，通过区域信息实现智能消歧。

**Architecture:** 在感知层提取元素区域信息，执行层使用区域选择器限定定位范围，Prompt 层展示区域信息帮助 LLM 做出更精确的决策。

**Tech Stack:** Python, Playwright, Pydantic

---

## Task 1: 修改类型定义

**Files:**
- Modify: `backend/agent_simple/types.py:18-29`

**Step 1: 添加 region 字段到 InteractiveElement**

在 `InteractiveElement` 类中添加 `region` 字段：

```python
class InteractiveElement(BaseModel):
    """可交互元素"""

    index: int = Field(description="元素索引")
    tag: str = Field(description="标签名 (BUTTON, INPUT, A, ...)")
    text: str = Field(default="", description="显示文本（截取前 50 字符）")
    type: str | None = Field(default=None, description="input 类型")
    id: str | None = Field(default=None, description="元素 id")
    placeholder: str | None = Field(default=None, description="占位文本")
    name: str | None = Field(default=None, description="元素 name 属性")
    aria_label: str | None = Field(default=None, description="aria-label 属性")
    title: str | None = Field(default=None, description="title 属性（悬停提示）")
    region: str | None = Field(default=None, description="元素所在区域 (sidebar/header/main/footer/modal)")
```

**Step 2: 验证类型定义**

运行: `python -c "from backend.agent_simple.types import InteractiveElement; print(InteractiveElement.model_fields.keys())"`

预期输出包含 `region` 字段。

**Step 3: Commit**

```bash
git add backend/agent_simple/types.py
git commit -m "feat(agent): 添加 region 字段到 InteractiveElement 类型"
```

---

## Task 2: 修改感知模块

**Files:**
- Modify: `backend/agent_simple/perception.py:121-206`

**Step 1: 修改 JavaScript 代码添加区域检测**

在 `_extract_elements` 方法的 `page.evaluate` 中，在 `result.push` 之前添加区域检测逻辑：

找到这段代码（约第 180 行）：
```python
                    result.push({
                        index: index,
                        tag: el.tagName,
```

在 `result.push` 之前添加区域检测：

```javascript
                    // 检测元素所在区域
                    const region = (() => {
                        if (el.closest('aside, .sidebar, .side-nav, .ant-layout-sider, .el-aside, nav')) {
                            return 'sidebar';
                        }
                        if (el.closest('header, .header, .ant-layout-header, .el-header')) {
                            return 'header';
                        }
                        if (el.closest('main, .main, .content, .ant-layout-content, .el-main')) {
                            return 'main';
                        }
                        if (el.closest('footer, .footer, .ant-layout-footer, .el-footer')) {
                            return 'footer';
                        }
                        if (el.closest('.modal, .dialog, .ant-modal, .el-dialog, [role="dialog"]')) {
                            return 'modal';
                        }
                        return null;
                    })();
```

然后在 `result.push` 中添加 `region` 字段：

```javascript
                    result.push({
                        index: index,
                        tag: el.tagName,
                        text: text,
                        type: el.type || null,
                        id: el.id || null,
                        placeholder: el.placeholder || null,
                        name: el.name || null,
                        aria_label: el.getAttribute('aria-label') || null,
                        title: el.getAttribute('title') || null,
                        region: region,
                        _priority: priority,
                        _isInViewport: isInViewport
                    });
```

**Step 2: 运行感知模块测试**

运行: `python -m pytest backend/tests/test_perception.py -v`

预期: 测试通过（现有测试不需要修改，因为 region 是可选字段）

**Step 3: Commit**

```bash
git add backend/agent_simple/perception.py
git commit -m "feat(perception): 添加元素区域检测功能"
```

---

## Task 3: 修改执行模块

**Files:**
- Modify: `backend/agent_simple/executor.py:422-528`

**Step 1: 添加区域选择器映射常量**

在 `Executor` 类中添加类常量（约第 27 行后）：

```python
class Executor:
    """动作执行模块

    负责将 LLM 决策的动作转换为 Playwright 操作并执行
    """

    # 区域选择器映射
    REGION_SELECTORS = {
        'sidebar': 'aside, .sidebar, .side-nav, nav',
        'header': 'header, .header',
        'main': 'main, .main, .content',
        'footer': 'footer, .footer',
        'modal': '.modal, .dialog, [role="dialog"]',
    }
```

**Step 2: 修改 _locate_element 方法添加区域消歧**

找到精确匹配文本的代码块（约第 476-480 行）：

```python
        # 3. 精确匹配文本（忽略空格）
        for el in elements:
            if el.text and _normalize_text(el.text) == target_normalized:
                logger.debug(f"精确匹配文本: {el.text}")
                return self.page.get_by_text(el.text, exact=True)
```

替换为：

```python
        # 3. 精确匹配文本（忽略空格）+ 区域消歧
        for el in elements:
            if el.text and _normalize_text(el.text) == target_normalized:
                logger.debug(f"精确匹配文本: {el.text}")
                locator = self.page.get_by_text(el.text, exact=True)

                # 检查是否匹配多个元素，如果是则用区域限定
                try:
                    count = await locator.count()
                    if count > 1 and el.region:
                        region_sel = self.REGION_SELECTORS.get(el.region)
                        if region_sel:
                            logger.info(f"检测到多个匹配元素，使用区域限定: {el.region}")
                            locator = self.page.locator(region_sel).get_by_text(el.text, exact=True)
                except Exception as e:
                    logger.debug(f"区域消歧检查失败: {e}")

                return locator
```

**Step 3: 运行执行模块测试**

运行: `python -m pytest backend/tests/test_executor.py -v`

预期: 测试通过

**Step 4: Commit**

```bash
git add backend/agent_simple/executor.py
git commit -m "feat(executor): 添加区域消歧逻辑解决多元素定位冲突"
```

---

## Task 4: 修改 Prompt 模块

**Files:**
- Modify: `backend/agent_simple/prompts.py:311-346`

**Step 1: 添加区域中文名称映射**

在 `format_elements_for_prompt` 函数开头添加映射：

```python
# 区域中文名称映射
REGION_NAMES = {
    'sidebar': '侧边栏',
    'header': '顶部导航',
    'main': '主内容区',
    'footer': '页脚',
    'modal': '弹窗',
}
```

**Step 2: 在元素格式化中添加区域信息**

在 `format_elements_for_prompt` 函数的循环中，在 `if el.type` 判断之后添加：

```python
        if el.region and el.region in REGION_NAMES:
            parts.append(f'区域: {REGION_NAMES[el.region]}')
```

完整的修改后的循环：

```python
    lines = []
    for el in elements:
        # 构建元素描述 - ID 放在最前面
        parts = [f"[{el.index}] <{el.tag}>"]

        # ID 优先显示（最重要的定位信息）
        if el.id:
            parts.append(f'ID: "{el.id}"')
        if el.name:
            parts.append(f'name: "{el.name}"')
        if el.text:
            parts.append(f'文本: "{el.text}"')
        if el.placeholder:
            parts.append(f'占位符: "{el.placeholder}"')
        if el.aria_label:
            parts.append(f'aria-label: "{el.aria_label}"')
        if el.title:
            parts.append(f'title: "{el.title}"')
        if el.type and el.tag == "INPUT":
            parts.append(f"类型: {el.type}")
        if el.region and el.region in REGION_NAMES:
            parts.append(f'区域: {REGION_NAMES[el.region]}')

        lines.append(" | ".join(parts))
```

**Step 3: 验证 Prompt 输出格式**

运行: `python -c "
from backend.agent_simple.prompts import format_elements_for_prompt
from backend.agent_simple.types import InteractiveElement

elements = [
    InteractiveElement(index=0, tag='BUTTON', text='商品采购', region='sidebar'),
    InteractiveElement(index=1, tag='DIV', text='商品采购', region='main'),
]
print(format_elements_for_prompt(elements))
"`

预期输出包含 `区域: 侧边栏` 和 `区域: 主内容区`

**Step 4: Commit**

```bash
git add backend/agent_simple/prompts.py
git commit -m "feat(prompts): 在元素列表中展示区域信息"
```

---

## Task 5: 集成测试验证

**Files:**
- Run: 集成测试

**Step 1: 运行完整 Agent 测试**

运行: `python -m backend.tests.test_agent`

观察日志，确认：
1. 感知模块提取到 `region` 字段
2. 执行模块在多元素匹配时使用区域限定
3. Prompt 中展示区域信息

**Step 2: 手动验证 - 运行发货单测试**

运行: `python -m backend.tests.test_shipping_form`

观察是否能正确定位侧边栏的"商品采购"菜单。

**Step 3: 更新调优记录**

如果测试成功，在 `docs/3_agent调优.md` 中记录本次优化。

**Step 4: 最终 Commit**

```bash
git add -A
git commit -m "feat: 完成基于区域的元素定位功能

- 添加 InteractiveElement.region 字段
- 感知模块提取元素所在区域
- 执行模块使用区域选择器消歧
- Prompt 展示区域信息帮助 LLM 决策"
```

---

## 预期效果

修改完成后，当页面上有多个相同文本的元素时：

1. **感知层**：元素列表会显示区域信息
   ```
   [0] BUTTON | 文本: "商品采购" | 区域: 侧边栏
   [1] DIV | 文本: "商品采购" | 区域: 主内容区
   ```

2. **执行层**：当 `get_by_text()` 匹配多个时，自动用区域选择器限定
   ```python
   # 原来: page.get_by_text("商品采购") → 报错 strict mode violation
   # 现在: page.locator('aside, .sidebar, nav').get_by_text("商品采购") → 精确定位
   ```

3. **LLM 决策**：能看到区域信息，做出更精确的判断
