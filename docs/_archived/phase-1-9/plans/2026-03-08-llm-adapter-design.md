# Phase 2: 模型适配 - 设计文档

> 创建日期: 2026-03-08
> 状态: 已批准

## 1. 概述

### 目标

实现通义千问视觉模型的适配层，为 Browser-Use Agent 提供多模态能力。

### 范围

- 实现统一 LLM 接口（`BaseLLM`）
- 适配通义千问 qwen-vl-max 模型
- 验证图像理解能力

### 不包含

- 智谱 GLM 适配（备选，后续添加）
- DeepSeek 适配（备选，后续添加）

## 2. 技术选型

| 项目 | 选择 | 理由 |
|------|------|------|
| 模型 | qwen-vl-max | 最强视觉理解能力 |
| SDK | dashscope | 阿里官方 SDK，API 稳定 |
| 接口风格 | LangChain 兼容 | 与 Browser-Use 生态一致 |
| 错误处理 | 内置重试（tenacity） | 调用方无需关心重试逻辑 |

## 3. 文件结构

```
backend/llm/
├── __init__.py           # 导出和工厂函数
├── base.py               # BaseLLM, LLMResponse, ActionResult
├── qwen.py               # QwenChat 实现
└── utils.py              # 图像编码工具

backend/tests/
└── test_qwen_vision.py   # 验证测试
```

## 4. 接口设计

### 4.1 BaseLLM 抽象类

```python
# backend/llm/base.py
from abc import ABC, abstractmethod
from pydantic import BaseModel


class ActionResult(BaseModel):
    """解析后的动作结果"""
    action: str           # 动作类型: click, fill, goto, etc.
    selector: str | None  # 目标元素选择器
    value: str | None     # 输入值（fill 时使用）
    reasoning: str        # AI 的推理说明


class LLMResponse(BaseModel):
    """LLM 响应封装"""
    content: str          # 原始文本响应
    action: ActionResult | None  # 解析后的动作（如果适用）
    usage: dict           # token 使用统计


class BaseLLM(ABC):
    """国内模型统一接口"""

    @abstractmethod
    async def chat_with_vision(
        self,
        messages: list[dict],
        images: list[str]  # 支持 URL 或 base64
    ) -> LLMResponse:
        """带图像理解的对话"""
        pass

    @abstractmethod
    def parse_action(self, response: str) -> ActionResult | None:
        """解析模型输出为结构化动作"""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """返回模型名称，用于日志"""
        pass
```

### 4.2 QwenChat 实现

```python
# backend/llm/qwen.py
import os
from typing import Any
import dashscope
from dashscope import MultiModalConversation
from tenacity import retry, stop_after_attempt, wait_exponential

from .base import BaseLLM, LLMResponse, ActionResult
from .utils import encode_image_to_base64


class QwenChat(BaseLLM):
    """通义千问视觉模型实现"""

    def __init__(
        self,
        model: str = "qwen-vl-max",
        api_key: str | None = None,
        max_retries: int = 3,
    ):
        self.model = model
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.max_retries = max_retries

        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 未配置")

        dashscope.api_key = self.api_key

    @property
    def model_name(self) -> str:
        return self.model

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    async def chat_with_vision(
        self,
        messages: list[dict],
        images: list[str],
    ) -> LLMResponse:
        """调用通义千问视觉模型"""

        # 构建消息内容
        content = self._build_content(messages, images)

        response = MultiModalConversation.call(
            model=self.model,
            messages=[{"role": "user", "content": content}],
        )

        if response.status_code != 200:
            raise RuntimeError(f"API 调用失败: {response.message}")

        text = response.output.choices[0].message.content

        return LLMResponse(
            content=text,
            action=self.parse_action(text),
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
        )

    def _build_content(self, messages: list[dict], images: list[str]) -> list:
        """构建多模态消息内容"""
        content = []

        # 添加图像
        for img in images:
            if img.startswith("http"):
                content.append({"image": img})
            else:
                # 本地文件转 base64
                base64_data = encode_image_to_base64(img)
                content.append({"image": f"data:image/png;base64,{base64_data}"})

        # 添加文本消息
        text = "\n".join(
            f"{m['role']}: {m['content']}"
            for m in messages
        )
        content.append({"text": text})

        return content

    def parse_action(self, response: str) -> ActionResult | None:
        """解析 Browser-Use 格式的动作输出"""
        import json

        try:
            # 尝试提取 JSON 块
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                data = json.loads(response[json_start:json_end])
                return ActionResult(
                    action=data.get("action"),
                    selector=data.get("selector"),
                    value=data.get("value"),
                    reasoning=data.get("reasoning", ""),
                )
        except json.JSONDecodeError:
            pass

        return None
```

### 4.3 工具函数

```python
# backend/llm/utils.py
import base64
from pathlib import Path


def encode_image_to_base64(image_path: str) -> str:
    """将图像文件编码为 base64 字符串"""
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"图像文件不存在: {image_path}")

    supported_formats = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
    if path.suffix.lower() not in supported_formats:
        raise ValueError(f"不支持的图像格式: {path.suffix}")

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
```

### 4.4 模块导出

```python
# backend/llm/__init__.py
"""LLM 模块 - 国内模型适配层"""

from .base import BaseLLM, LLMResponse, ActionResult
from .qwen import QwenChat

__all__ = [
    "BaseLLM",
    "LLMResponse",
    "ActionResult",
    "QwenChat",
]


def get_default_llm() -> BaseLLM:
    """获取默认的 LLM 实例（通义千问）"""
    return QwenChat()
```

## 5. 验证测试

### 5.1 测试用例

| 测试 | 验证目标 | 优先级 |
|------|----------|--------|
| 基础对话 | API 连接正常，文本响应正确 | P0 |
| 图像 URL | 能理解网络图片内容 | P0 |
| 动作解析 | 能从文本中提取 JSON 动作 | P0 |
| 本地图像 | 能处理本地截图文件 | P1 |

### 5.2 测试文件

详见 `backend/tests/test_qwen_vision.py`

## 6. 依赖

### 新增依赖

```toml
# pyproject.toml
langchain-core = ">=0.3.0"
dashscope = ">=1.14.0"
tenacity = ">=8.0.0"
```

## 7. 验收标准

- [ ] `BaseLLM` 接口定义完成
- [ ] `QwenChat` 实现完成
- [ ] 工具函数实现完成
- [ ] 基础文本对话测试通过
- [ ] 图像 URL 理解测试通过
- [ ] 动作解析测试通过
- [ ] 本地截图处理测试通过

## 8. 风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| qwen-vl-max API 限流 | 测试中断 | 内置重试机制 |
| 图像大小超限 | 调用失败 | 添加图像压缩（如需要） |
| 动作解析格式不一致 | 解析失败 | 容错处理，记录原始响应 |

## 9. 预估工时

| 任务 | 预估时间 |
|------|----------|
| 实现 BaseLLM 接口 | 30 分钟 |
| 实现 QwenChat | 1 小时 |
| 实现工具函数 | 30 分钟 |
| 编写验证测试 | 1 小时 |
| 调试和修复 | 1-2 小时 |
| **总计** | **4-5 小时** |
