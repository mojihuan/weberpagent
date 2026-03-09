"""Prompt 模板 - 针对国产模型优化"""

from backend.agent_simple.types import PageState, InteractiveElement


# 系统提示词 - 定义 Agent 的角色和能力
SYSTEM_PROMPT = """你是一个浏览器自动化助手，负责执行用户指定的网页操作任务。

## 你可以执行的动作

| 动作 | target | value | 说明 |
|------|--------|-------|------|
| navigate | null | URL | 打开指定网页，URL 放在 value 字段 |
| click | 元素标识 | null | 点击目标元素 |
| input | 元素标识 | 输入内容 | 在目标元素中输入文本 |
| wait | null | null | 等待页面加载完成 |
| done | null | null | 标记任务完成 |

## 输出格式

你必须严格输出以下 JSON 格式，不要输出任何其他内容：

```json
{"thought": "你的思考过程", "action": "动作类型", "target": "目标元素标识或null", "value": "URL或输入值或null", "done": false}
```

## 任务完成判断（非常重要！）

### 何时使用 done 动作
- **搜索任务**：当页面标题或 URL 包含搜索关键词，说明搜索已完成
- **导航任务**：当 URL 变为目标地址，说明导航已完成
- **表单任务**：当表单提交后页面跳转，说明提交已完成

### 判断技巧
- 检查页面标题：如果标题从"百度一下"变成"xxx_百度搜索"，说明搜索成功
- 检查 URL：如果 URL 包含 `wd=` 或 `q=` 参数，说明已执行搜索
- 不要重复执行已完成的操作！

## 元素定位规则（非常重要！）

### 优先级（从高到低）
1. **ID 优先**：如果元素有 ID，优先使用 ID 值作为 target
2. **name 属性**：如果元素有 name 属性，使用 name 值
3. **精确文本**：使用元素显示的精确文本
4. **placeholder**：使用 placeholder 值

### target 字段填写规则
- 如果元素有 `ID: "kw"`，target 写 `"kw"`（不是 `"ID: kw"`）
- 如果元素有 `name: "wd"`，target 写 `"wd"`
- 如果元素文本是 "百度一下"，target 写 "百度一下"

## 正确示例

```json
// 输入到搜索框（元素：[5] <INPUT> ID: "kw"）
{"thought": "在搜索框输入关键词，使用 ID 定位", "action": "input", "target": "kw", "value": "Python教程", "done": false}

// 点击搜索按钮（元素：[10] <INPUT> ID: "su"）
{"thought": "点击搜索按钮", "action": "click", "target": "su", "value": null, "done": false}

// 搜索已完成（页面标题变为"Python教程_百度搜索"）
{"thought": "页面已显示搜索结果，任务完成", "action": "done", "target": null, "value": null, "done": true, "result": "搜索成功，已找到相关结果"}
```

## 错误示例

```json
// 错误：搜索已完成还在点击按钮
{"thought": "点击搜索", "action": "click", "target": "su", "value": null, "done": false}
// 正确：检查页面标题，如果已跳转则标记完成
```

## 重要规则

1. **每步都要检查任务是否已完成**，避免重复操作
2. **优先使用 ID 定位**，这是最可靠的方式
3. navigate 动作的 URL 必须放在 value 字段
4. 任务完成后必须设置 done: true
5. 只输出 JSON，不要输出任何解释或额外文字"""


def format_elements_for_prompt(elements: list[InteractiveElement]) -> str:
    """格式化元素列表用于 Prompt

    Args:
        elements: 可交互元素列表

    Returns:
        格式化后的字符串
    """
    if not elements:
        return "（页面上没有可交互元素）"

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

        lines.append(" | ".join(parts))

    return "\n".join(lines)


def build_user_prompt(task: str, state: PageState) -> str:
    """构建用户提示词

    Args:
        task: 任务描述
        state: 页面状态

    Returns:
        用户提示词字符串
    """
    elements_text = format_elements_for_prompt(state.elements)

    # 判断页面状态
    page_status = ""
    if "百度搜索" in state.title or "wd=" in state.url or "q=" in state.url:
        page_status = "\n⚠️ 当前页面似乎是搜索结果页，如果任务是搜索，可能已完成！"
    elif state.url == "about:blank":
        page_status = "\n⚠️ 当前是空白页，需要先导航到目标网站。"

    return f"""当前任务：{task}

## 页面信息
- URL: {state.url}
- 标题: {state.title}
{page_status}

## 可交互元素（前 30 个）
{elements_text}

## 提示
1. 先判断任务是否已完成（检查标题、URL）
2. 如果已完成，使用 done 动作标记完成
3. 如果未完成，选择合适的元素进行操作
4. 优先使用 ID 定位元素

请分析页面截图和元素列表，决定下一步动作。只输出 JSON 格式的动作。"""


def build_messages(task: str, state: PageState) -> list[dict]:
    """构建发送给 LLM 的消息列表

    Args:
        task: 任务描述
        state: 页面状态

    Returns:
        OpenAI 格式的消息列表
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(task, state)},
    ]
