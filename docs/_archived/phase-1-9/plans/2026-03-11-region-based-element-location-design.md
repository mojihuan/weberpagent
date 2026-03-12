# 基于区域的元素定位方案

## 问题背景

页面上存在多个相同文本的元素（如侧边栏和主内容区都有"商品采购"），Playwright strict mode 要求定位器必须唯一匹配，导致定位失败。

**错误示例**：
```
Locator.hover: Error: strict mode violation: get_by_text("商品采购") resolved to 2 elements:
    1) <span>商品采购</span>
    2) <div class="text" data-v-753f7723=""> 商品采购 </div>
```

## 解决方案

**方案 C1：轻量级 - 区域信息 + 智能消歧**

- 感知层：提取元素所在区域（sidebar/header/main/footer/modal）
- 执行层：当匹配多个元素时，用区域选择器限定
- Prompt 层：展示区域信息，让 LLM 理解上下文

## 设计细节

### 1. 类型定义修改 (`types.py`)

```python
class InteractiveElement(BaseModel):
    """可交互元素"""
    index: int
    tag: str
    text: str = ""
    type: str | None = None
    id: str | None = None
    placeholder: str | None = None
    name: str | None = None
    aria_label: str | None = None
    title: str | None = None
    region: str | None = None  # 新增：所在区域
```

**区域值**：
- `sidebar` - 侧边栏
- `header` - 顶部导航
- `main` - 主内容区
- `footer` - 页脚
- `modal` - 弹窗
- `null` - 未知

### 2. 感知模块修改 (`perception.py`)

在 `_extract_elements()` 方法的 JavaScript 中添加区域检测：

```javascript
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

### 3. 执行模块修改 (`executor.py`)

修改 `_locate_element()` 方法：

```python
async def _locate_element(self, target: str, elements: list[InteractiveElement]):
    # ... 现有逻辑 ...

    # 当通过文本定位时，尝试用区域限定
    for el in elements:
        if el.text and _normalize_text(el.text) == target_normalized:
            locator = self.page.get_by_text(el.text, exact=True)

            # 检查是否匹配多个元素
            count = await locator.count()
            if count > 1 and el.region:
                # 使用区域限定
                region_selectors = {
                    'sidebar': 'aside, .sidebar, .side-nav, nav',
                    'header': 'header, .header',
                    'main': 'main, .main, .content',
                    'footer': 'footer, .footer',
                    'modal': '.modal, .dialog, [role="dialog"]',
                }
                region_sel = region_selectors.get(el.region)
                if region_sel:
                    locator = self.page.locator(region_sel).get_by_text(el.text, exact=True)

            return locator
```

**核心逻辑**：
1. 先检查 `locator.count()`
2. 如果 > 1 且有区域信息，用区域选择器限定
3. 返回限定后的 locator

### 4. Prompt 模块修改 (`prompts.py`)

在构建元素列表时展示区域信息：

```python
def _format_elements(elements: list[InteractiveElement]) -> str:
    """格式化元素列表为 Prompt 文本"""
    lines = []
    for i, el in enumerate(elements):
        parts = [f"[{i}] {el.tag}"]

        if el.text:
            parts.append(f'文本: "{el.text}"')
        if el.region:
            region_cn = {
                'sidebar': '侧边栏',
                'header': '顶部导航',
                'main': '主内容区',
                'footer': '页脚',
                'modal': '弹窗',
            }.get(el.region, '')
            if region_cn:
                parts.append(f'区域: {region_cn}')

        lines.append(' | '.join(parts))
    return '\n'.join(lines)
```

**效果示例**：
```
[0] BUTTON | 文本: "商品采购" | 区域: 侧边栏
[1] DIV | 文本: "商品采购" | 区域: 主内容区
```

## 改动文件

| 模块 | 文件 | 改动 |
|------|------|------|
| 类型 | `backend/agent_simple/types.py` | 添加 `region` 字段 |
| 感知 | `backend/agent_simple/perception.py` | 提取元素区域 |
| 执行 | `backend/agent_simple/executor.py` | 区域限定定位 |
| Prompt | `backend/agent_simple/prompts.py` | 展示区域信息 |

**预计代码量**：约 50-80 行

## 预期效果

1. 感知模块能识别元素所在区域
2. 执行模块能智能消歧，优先选择指定区域的元素
3. LLM 能在 Prompt 中看到区域信息，做出更精确的决策
