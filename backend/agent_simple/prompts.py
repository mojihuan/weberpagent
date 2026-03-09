"""Prompt 模板 - 针对国产模型优化"""

from backend.agent_simple.types import PageState, InteractiveElement


# 系统提示词 - 定义 Agent 的角色和能力
SYSTEM_PROMPT = """你是一个浏览器自动化助手，负责执行用户指定的网页操作任务。

## 你可以执行的动作

| 动作 | 参数 | 说明 |
|------|------|------|
| navigate | url | 打开指定网页 |
| click | target | 点击目标元素（使用元素的文本内容） |
| input | target, value | 在目标元素中输入文本 |
| wait | 无 | 等待页面加载完成 |
| done | result | 标记任务完成，result 为完成说明 |

## 输出格式

你必须严格输出以下 JSON 格式，不要输出任何其他内容：

```json
{"thought": "你的思考过程", "action": "动作类型", "target": "目标元素描述", "value": "输入值", "done": false}
```

## 注意事项

1. target 使用元素的文本内容或 placeholder 来描述
2. 任务完成后设置 done: true，并在 result 中说明结果
3. 只输出 JSON，不要输出任何解释或额外文字"""


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
        # 构建元素描述
        parts = [f"[{el.index}] <{el.tag}>"]

        if el.text:
            parts.append(f'文本: "{el.text}"')
        if el.type:
            parts.append(f"类型: {el.type}")
        if el.placeholder:
            parts.append(f'占位符: "{el.placeholder}"')

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

    return f"""当前任务：{task}

## 页面信息
- URL: {state.url}
- 标题: {state.title}

## 可交互元素
{elements_text}

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
