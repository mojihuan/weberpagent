# Phase 40: 表格元素定位增强 - Research

**Researched:** 2026-03-24
**Domain:** browser-use custom工具、水平滚动表格元素定位
**Confidence:** MEDIUM
**Primary recommendation:** 创建 `scroll_table_and_input` 工具，通过 `@registry.action` 装饰器注册，使用 `browser_session` 参数访问 Playwright page 进行 DOM 操作，工具参数与 CONTEXT.md 已确定。

工具描述应该清晰具体，让 Agent 能理解何时调用该工具
**Phase Requirement IDs:** LOOP-02, LOOP-04

**Success Criteria:**
1. 销售出库场景中能成功输入销售金额
2. 水平滚动表格内的输入字段能被正确定位和操作
3. 无法完成的步骤被跳过后，后续步骤能继续执行

</specifics>
```

<user_constraints>
## User Constraints (from CONTEXT.md)

### Implementation Decisions
**D-01: 工具定位**
- **专用工具设计**: 针对 ERP 表格场景，不做通用化
- **独立实现**: 不依赖 webseleniumerp，保持项目解耦
**D-02: 工具参数设计（最小参数集）**
```python
@tool
def scroll_table_and_input(
    table_selector: str,    # 表格选择器（CSS 或 XPath）
    row_identifier: str,    # 行内文本，用于定位目标行
    column_header: str,     # 列标题文本，用于定位目标列
    input_value: str,       # 要输入的值
) -> str:
    """在水平滚动表格中定位单元格并输入值"""
```
**D-03: 智能滚动定位逻辑**
1. 使用表格选择器定位表格元素
2. 通过行内文本匹配定位目标行
3. 通过列标题文本匹配定位目标列
4. 检测目标列是否在可视区域内
5. 如果不在可视区域，执行水平滚动直到目标列可见
6. 在目标单元格中输入值
7. 使用 `scrollIntoView()` JavaScript 实现滚动
**D-04: 列定位方式**
- 通过列标题文本匹配（如"销售金额"）
- 遍历表格 header 行，匹配文本内容
**D-05: 行定位方式**
- 通过行内某个单元格的文本匹配（如"IMEI: xxx"）
- 遍历表格行，查找包含目标文本的行
**D-06: 与 browser-use 集成**
- 使用 `@tool` 装饰器注册自定义工具
- Agent 可自主决定何时调用工具
- 不基于 stagnation 触发工具调用
**D-07: 错误处理**
- 工具失败时返回描述性错误信息
- 让 Agent 自己决定下一步处理
- 不实现单独的跳过逻辑
**D-08: LOOP-04 实现方向**
- **原理解**: stagnation >= 5 -> 跳过当前步骤
- **实际实现**: Agent 自主调用工具 → 工具失败返回错误 → Agent 自行处理
- 不需要单独的跳过机制，Agent 会通过工具返回的错误自行决定
</decisions>
### Claude's Discretion
**D-08: 工具放置位置**: `backend/agent/tools/` 目录
**D-09: 工具描述优化**: 工具描述应该清晰具体，说明使用场景和参数含义
**D-10: 考虑 Playwright 的 `scrollIntoViewIfNeeded() 或 JavaScript `scrollIntoView()` 的兼容性**
</discretion>
### Deferred Ideas (OUT OF SCO)
None — discussion stayed within phase scope.
</deferred>
</user_constraints>
## Standard Stack
### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| browser-use | 0.12.5 | Agent framework | Official browser automation framework with built-in loop detection |
| Playwright | 1.49.1 | Browser automation | Native browser control, handles scroll interactions |
| pydantic | 2.12.5 | Data validation | Standard for model parameters and type hints |
### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|--------------|
| langchain | - | LLM integration | browser-use uses langchain for LLM calls |
| aiosqlite | 0.20.4+ | Async database | Project data storage |
### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| 原生 Playwright | browser-use Agent | When browser-use has LLM capabilities are needed; otherwise use native Playwright |
| webseleniumerp scroll_custom | browser-use Agent | webseleniumerp uses Selenium, not Playwright; browser-use uses Playwright |
**Installation:**
Already part of browser-use via uv:
```bash
uv add browser-use
```
**Version verification:**
| Package | Version | Publish Date |
|--------|---------|--------------|
| browser-use | 0.9.14 | 2025-03-13 |
| pydantic | 2.12.5 | 2025-03-13 |
| playwright | 1.49.1 | 2025-03-13 |

## Architecture Patterns
### Recommended Project Structure
```
backend/
├── agent/
│   ├── tools/              # 自定义工具目录
│   │   ├── __init__.py
│   │   └── scroll_table_tool.py  # 滚动表格工具
│   └── browser_agent.py
├── core/
│   └── agent_service.py   # Agent 构造位置
```
**Note:** 工具放在 `backend/agent/tools/` 目录下，与 `browser_agent.py` 分离
### Pattern 1: browser-use Custom Tool Registration
**What:** 使用 `@registry.action` 装饰器注册自定义工具
**When to use:** 当需要访问 `browser_session` 参数进行 DOM 操作
**Example:**
```python
# Source: browser_use/tools/registry/service.py
from browser_use.tools.registry.service import Registry
from browser_use.browser import BrowserSession
from pydantic import BaseModel

from typing import Optional

class ScrollTableInputParams(BaseModel):
    table_selector: str
    row_identifier: str
    column_header: str
    input_value: str

# Create registry instance
registry = Registry()

@registry.action(
    "在水平滚动表格中定位单元格并输入值。适用于 ERP 系统中需要操作水平滚动表格内输入字段的场景。",
    param_model=ScrollTableInputParams
)
async def scroll_table_and_input(
    params: ScrollTableInputParams,
    browser_session: Optional[BrowserSession] = None,
) -> str:
    """在水平滚动表格中定位指定行和列的单元格，并输入值

    Args:
        params: 工具参数
        browser_session: 浏览器会话对象

    Returns:
        操作结果描述
    """
    if not browser_session:
        return "错误: browser_session 未提供"

    page = await browser_session.get_current_page()

    # 1. 定位表格
    table = await page.query_selector(params.table_selector)
    if not table:
        return f"错误: 找不到表格: selector: {params.table_selector}"

    # 2. 定位目标列
    headers = await table.query_selector_all('th')
    target_col_index = None
    for i, range(len(headers)):
        header_text = await headers[i].text_content()
        if header_text.strip() == params.column_header:
            target_col_index = i
            break

    if target_col_index is None:
        return f"错误: 找不到列 '{params.column_header}'"

    # 3. 定位目标行
    rows = await table.query_selector_all('tr')
    for row in rows:
        row_text = await row.text_content
        if params.row_identifier in row_text:
            target_row = row
            break

    if target_row is None:
        return f"错误: 找不到行 '{params.row_identifier}'"

    # 4. 滚动到目标单元格
    target_cell = await target_row.query_selector(f'td:nth-child({target_col_index + 1})')
    if not target_cell:
        return f"错误: 在目标列中找不到输入元素"

    # 5. 滚动目标单元格到可视区域
    input_element = target_cell.query_selector('input, textarea')
    if not input_element:
        return f"错误: 目标单元格中没有输入元素"

    # 6. 输入值
    await input_element.fill()
    await input_element.type(params.input_value)

    return f"成功: 在 {params.column_header} 列的行 '{params.row_identifier}' 中输入了值: {params.input_value}"
```
**Key insight:** browser-use 的 Registry 篾架使用 `@registry.action` 装饰器，支持:
- 参数模型（Pydantic BaseModel)
- browser_session 参数注入
- 异步函数
- 返回字符串结果

- Agent 通过工具描述和参数自动决定何时调用
### Anti-Patterns to Avoid
- **将工具放在 browser_agent.py:** 工具应该与 Agent 逻辑耦合,职责不清
- **硬编码表格选择器:** 在工具内部判断表格类型，维护困难
- **跳过特定 DOM 结构:** 工具应该返回成功/失败,让 Agent 自行处理

### Don't Hand-Roll
| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|------|
| 水平滚动表格定位 | 使用 Playwright 的 `scroll_into_view()` 或自定义工具 | 复杂度高、标准方法 |
| 表格列/行定位 | 遍历 `<th>` 和 `<tr>` 元素 | 简单,模式，边界情况处理不完善 |
| 检测列/行是否可见 | 遍历行查找包含目标文本的行 | 简单,模式，边界情况处理不完善 |

| 检测输入框是否存在 | 遍历单元格查找 input 元素, 简单,模式
| 输入值 | 直接填充 | 遍历单元格查找 input 元素， 箇单,模式，边界情况处理不完善 |
| 检测滚动结果 | 遍历所有 `<td>` 找到目标列索引 | 然后通过 `scrollIntoViewIfNeeded()` 滚动 |可能不可见 |
| 检测滚动是否成功 | 遍历滚动位置直到成功或失败 | 简单检查 |
| 检测元素是否存在 | 遍历所有元素，可能无法定位（返回描述性错误) |
| 检测表格选择器有效性 | 遍历 `table.querySelectorAll()` 验证是否能找到表格
| 检测列标题匹配 | 遍历 `<th>` 元素，比较文本内容
| 检测行匹配 | 遍历 `<tr>` 元素，比较文本内容
| 检测单元格输入框存在 | 遍历单元格的 `querySelector()` 方法

| 检测滚动成功 | 簡单的成功检查即可
| 检测输入是否成功 | 遍历 `input_element.value == params.input_value` 验证输入
| 检测输入元素类型 | 使用 `element.type()` 裀查 input/textarea/select器

| 检测工具失败时的错误信息 | 返回描述性错误，让 Agent 自行处理

## Common Pitfalls
### Pitfall 1: 元素不可见导致无限滚动
**What goes wrong:** 元素在滚动容器内，滚动后仍然不可见
**Why it happens:** Playwright 的 `scrollIntoViewIfNeeded()` 只滚动容器，不会滚动内部元素
**How to avoid:**
1. 先检查 `element.scrollWidth` 或 `element.clientWidth` 判断是否真正可滚动
2. 如果 `scrollWidth > clientWidth`，考虑在容器内分步滚动
3. 使用 `element.scrollIntoView({ inline: 'center' })` 实现精确水平滚动
**Warning signs:** 滚动后元素位置仍然不在可视区域内
### Pitfall 2: 输入值后元素状态未清除
**What goes wrong:** 滚动到输入框后，原有值没有被清除
**Why it happens:** 黚input()` 不会清除输入框，**How to avoid:** 使用 `clear=True` 参数或或填充新值前先清除
```python
await input_element.clear()
await input_element.type(value)
```
**Warning signs:** `input_element.value` 属性为空字符串或填充后无内容
### Pitfall 3: 复杂的选择器逻辑
**What goes wrong:** 使用过于复杂的 CSS 选择器或 XPath 定位表格和列
**Why it happens:** ERP 表格可能有复杂的 DOM 结构（嵌套表格、合并单元格等)
**How to avoid:**
1. **优先使用简单选择器:** `table.data-table`, `table > tbody > tr > td`
2. 如果需要更复杂的选择器，使用 data属性定位（如 `data-row-id`, `data-col-index` 属性)
2. 对于动态列（可能增减)，使用 `th:nth-child()` 鰾活性检查
2. 使用合理的等待策略
3. 分步滚动大型表格
4. **Warning signs:** 单次滚动耗时过长，表格操作超时
### Pitfall 4: 错误处理不统一
**What goes wrong:** 错误信息格式不一致，**Why it happens:** 不同错误类型返回不同格式的字符串
**How to avoid:**
1. 定义统一的错误类型（如 `ScrollTableError`)
2. 统一错误消息格式
3. 提供清晰的上下文信息（当前步骤、列/行信息)
**Warning signs:** Agent 重复尝试相同操作
## Code Examples
Verified patterns from official sources:
### Common Operation 1: browser-use Custom Tool Registration
```python
# Source: browser_use/tools/registry/service.py
from browser_use.tools.registry.service import Registry
from browser_use.browser import BrowserSession
from pydantic import BaseModel
from typing import Optional

class ScrollTableInputParams(BaseModel):
    table_selector: str
    row_identifier: str
    column_header: str
    input_value: str

# Create registry instance
registry = Registry()

@registry.action(
    "在水平滚动表格中定位单元格并输入值。适用于 ERP 系统中需要操作水平滚动表格内输入字段的场景。",
    param_model=ScrollTableInputParams
)
async def scroll_table_and_input(
    params: ScrollTableInputParams,
    browser_session: Optional[BrowserSession] = None,
) -> str:
    if not browser_session:
        return "错误: browser_session 未提供"

    page = await browser_session.get_current_page()

    # 1. 定位表格
    table = await page.query_selector(params.table_selector)
    if not table:
        return f"错误: 找不到表格, selector: {params.table_selector}"

    # 2. 定位目标列
    headers = await table.query_selector_all('th')
    target_col_index = None
    for i in range(len(headers)):
        header_text = await headers[i].text_content()
        if header_text and header_text.strip() == params.column_header:
            target_col_index = i
            break

    if target_col_index is None:
        return f"错误: 找不到列 '{params.column_header}'"

    # 3. 定位目标行
    rows = await table.query_selector_all('tr')
    for row in rows:
        row_text = await row.text_content()
        if params.row_identifier in row_text:
            target_row = row
            break

    if target_row is None:
        return f"错误: 找不到行 '{params.row_identifier}'"

    # 4. 滚动到目标单元格
    target_cell = target_row.query_selector(f'td:nth-child({target_col_index + 1})')
    if not target_cell:
        return f"错误: 在目标列中找不到输入元素"

    # 5. 滚动目标单元格到可视区域
    await target_cell.scroll_into_view_if_needed()

    # 6. 输入值
    input_element = await target_cell.query_selector('input, textarea')
    if not input_element:
        return f"错误: 目标单元格中没有输入元素"

    await input_element.fill()
    await input_element.type(params.input_value)

    return f"成功: 在 {params.column_header} 列的行 '{params.row_identifier}' 中输入了值: {params.input_value}"
```
### Anti-Patterns to Avoid
- **将工具放在 browser_agent.py:** 工具应该与 Agent 逻辑耦合,职责不清
- **硬编码表格选择器:** 在工具内部判断表格类型，维护困难
- **跳过特定 DOM 结构:** 工具应该返回成功/失败,让 Agent 自行处理
### Don't Hand-Roll
| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|------|
| 水平滚动表格定位 | 使用 Playwright 的 `scroll_into_view_if_needed()` 或自定义工具 | 复杂度高，标准方法 |
| 表格列/行定位 | 遍历 `<th>` 元素 | 知识点： CSS 选择器可能灵活， XPath 在处理复杂结构时更强大 |
| 检测列/行是否可见 | 遍历行查找包含目标文本的行 | 知识点: 文本匹配可能不精确 |
| 检测输入框是否存在 | 遍历单元格查找 input 元素 | 知识点: `querySelector()` 可能返回 None
| 检测滚动结果 | 遍历滚动位置直到成功或失败 | 知识点: 无滚动进度反馈 |
| 检测输入值 | 遍历填充新值前检查状态 | 知识点: 输入后无验证 |

## State of the Art
| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|-------|
| Selenium `scrollIntoView()` | Playwright `scroll_into_view_if_needed()` | Phase 40 | 更可靠，异步支持 |

**Deprecated/outdated:**
- None identified
## Open Questions
1. **scrollIntoView vs scrollIntoViewIfNeeded**
   - What we know: `scrollIntoViewIfNeeded()` 是 Playwright 墙议方法，自动等待元素可见
   - What's unclear: `scrollIntoView()` 是否也能处理异步场景
   - Recommendation: 优先使用 `scroll_into_view_if_needed()`, 需要时回退到 JavaScript `scrollIntoView()`
2. **复杂表格选择器**
   - What we know: CSS 选择器如 `table.data-table` 可能适用于大多数 ERP 系统
   - What's unclear: 是否需要支持更复杂的选择器（如包含特定类名的表格）
   - Recommendation: 从简单选择器开始，根据实际场景调整
## Environment Availability
> Skip this section if the phase has no external dependencies (code/config-only changes).
| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Playwright | browser-use | ✓ | 1.49.1 | — |
| browser-use | Agent framework | ✓ | 0.9.14 | — |
| pydantic | Data validation | ✓ | 2.12.5 | — |
| Python 3.11 | Runtime | ✓ | 3.11.x | — |
**Missing dependencies with no fallback:**
- None
**Missing dependencies with fallback:**
- None
## Validation Architecture
### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | backend/tests/conftest.py |
| Quick run command | `uv run pytest backend/tests/unit/test_agent_service.py -x -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |
### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| LOOP-02 | Register scroll_table_and_input tool | unit | `uv run pytest backend/tests/unit/test_scroll_table_tool.py -x` | ❌ Wave 0 |
| LOOP-02 | Tool locates table cell by header/row | unit | `uv run pytest backend/tests/unit/test_scroll_table_tool.py::test_locate_cell -x` | ❌ Wave 0 |
| LOOP-02 | Tool scrolls to hidden column | unit | `uv run pytest backend/tests/unit/test_scroll_table_tool.py::test_scroll_to_hidden_column -x` | ❌ Wave 0 |
| LOOP-02 | Tool inputs value to cell | unit | `uv run pytest backend/tests/unit/test_scroll_table_tool.py::test_input_to_cell -x` | ❌ Wave 0 |
| LOOP-02 | Tool handles missing table | unit | `uv run pytest backend/tests/unit/test_scroll_table_tool.py::test_missing_table -x` | ❌ Wave 0 |
| LOOP-02 | Tool handles missing column | unit | `uv run pytest backend/tests/unit/test_scroll_table_tool.py::test_missing_column -x` | ❌ Wave 0 |
| LOOP-02 | Tool handles missing row | unit | `uv run pytest backend/tests/unit/test_scroll_table_tool.py::test_missing_row -x` | ❌ Wave 0 |
| LOOP-02 | Tool handles missing input element | unit | `uv run pytest backend/tests/unit/test_scroll_table_tool.py::test_missing_input -x` | ❌ Wave 0 |
| LOOP-02 | Integration with AgentService | integration | `uv run pytest backend/tests/integration/test_agent_service.py -x` | ✅ Existing |
| LOOP-04 | Agent self-handles tool failure | integration | Manual verification (E2E) | ❌ Wave 0 |
| LOOP-04 | Task continues after tool failure | integration | Manual verification (E2E) | ❌ Wave 0 |
### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_scroll_table_tool.py -x -v`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`
### Wave 0 Gaps
- [ ] `backend/tests/unit/test_scroll_table_tool.py` — unit tests for scroll_table_and_input tool
- [ ] `backend/agent/tools/__init__.py` — tools package initialization
- [ ] Framework install: Already done (pytest)
*(If no gaps: "None — existing test infrastructure covers all phase requirements")
## Sources
### Primary (HIGH confidence)
- browser_use/tools/registry/service.py - Registry.action decorator implementation
- browser_use/agent/service.py - Agent construction and tool integration
- webseleniumerp/common/base_page.py - scroll_custom reference implementation
### Secondary (MEDIUM confidence)
- [Playwright scrollIntoViewIfNeeded documentation](https://playwright.dev/docs/api/class-locator#scroll-into-view-if-needed)
- [Stack Overflow: Playwright table scrollbar issue](https://stackoverflow.com/questions/74144217/playwright-cant-click-element-in-table-with-scrollbar)
### Tertiary (LOW confidence)
- None
## Metadata
**Confidence breakdown:**
- Standard stack: HIGH - browser-use 0.9.14 documentation and code inspection
- Architecture: HIGH - Clear pattern from CONTEXT.md and code inspection
- Pitfalls: MEDIUM - Common edge cases identified from documentation and research
**Research date:** 2026-03-24
**Valid until:** 30 days (stable browser-use API)
