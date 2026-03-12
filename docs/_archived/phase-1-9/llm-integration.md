# LLM 集成

本文档描述项目的 LLM 适配层设计和使用方式。

---

## 统一接口

项目使用统一 LLM 接口，支持多个国产模型：

```python
class BaseLLM(ABC):
    """LLM 统一接口"""

    @abstractmethod
    async def chat_with_vision(
        self,
        messages: list[dict],
        images: list[str],  # 支持 URL、文件路径、data URI
    ) -> LLMResponse:
        """带图像理解的对话"""
        pass

    @abstractmethod
    def parse_action(self, response: str) -> ActionResult | None:
        """解析模型输出为结构化动作"""
        pass
```

## 支持的模型

| 模型 | 文件 | 视觉能力 | 状态 |
|------|------|----------|------|
| 通义千问 qwen-vl-max | `backend/llm/qwen.py` | ✅ | Primary |
| DeepSeek | `backend/llm/deepseek.py` | ❌ | Backup |
| Azure OpenAI | `backend/llm/azure_openai.py` | ✅ | Backup |

## 动作输出格式

LLM 需要输出以下 JSON 格式（针对国产模型优化）：

```json
{
  "thought": "分析当前页面，发现需要点击登录按钮",
  "action": "click",
  "target": "登录",
  "value": null,
  "done": false
}
```

### 支持的动作类型

| 动作 | 说明 | 参数 |
|------|------|------|
| `navigate` | 导航到 URL | value 为 URL |
| `click` | 点击元素 | target 为元素文本 |
| `input` | 输入文本 | target 为元素，value 为内容 |
| `wait` | 等待页面加载 | - |
| `done` | 任务完成 | - |
| `fill_form` | 复杂表单填写 | 调用多 Agent 协作 |

## 使用示例

```python
from backend.agent_simple import SimpleAgent
from backend.llm.qwen import QwenChat

agent = SimpleAgent(
    task="在百度搜索 Python 教程",
    llm=QwenChat(model="qwen-vl-max"),
    page=page,
)
result = await agent.run()
```

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| Max steps | 20 | 每个任务最大步数 |
| Step timeout | 30s | 单步超时时间 |
| Max retries | 3 | 失败重试次数 |
| Screenshots | enabled | 每步保存截图 |
