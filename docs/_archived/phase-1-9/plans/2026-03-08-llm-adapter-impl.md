# LLM Adapter Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现通义千问视觉模型适配层，为 Browser-Use Agent 提供多模态能力。

**Architecture:** 采用抽象基类 + 具体实现的模式。BaseLLM 定义统一接口，QwenChat 实现通义千问的视觉能力调用，使用 tenacity 处理重试。

**Tech Stack:** Python, dashscope SDK, tenacity, pydantic

---

## Task 1: 更新依赖配置

**Files:**
- Modify: `pyproject.toml`

**Step 1: 检查当前依赖**

Run: `cat pyproject.toml`
Expected: 显示现有依赖列表

**Step 2: 添加新依赖**

在 `dependencies` 数组中添加：

```toml
    "tenacity>=8.0.0",
```

注意：`dashscope` 和 `langchain-core` 可能已存在，只添加 `tenacity`。

**Step 3: 安装依赖**

Run: `pip install tenacity`
Expected: Successfully installed tenacity-x.x.x

**Step 4: Commit**

```bash
git add pyproject.toml
git commit -m "chore: add tenacity dependency for retry mechanism"
```

---

## Task 2: 实现 BaseLLM 抽象接口

**Files:**
- Create: `backend/llm/base.py`

**Step 1: 创建 base.py 文件**

```python
"""LLM 抽象基类和数据模型"""

from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel


class ActionResult(BaseModel):
    """解析后的动作结果"""

    action: str  # 动作类型: click, fill, goto, etc.
    selector: str | None = None  # 目标元素选择器
    value: str | None = None  # 输入值（fill 时使用）
    reasoning: str = ""  # AI 的推理说明


class LLMResponse(BaseModel):
    """LLM 响应封装"""

    content: str  # 原始文本响应
    action: ActionResult | None = None  # 解析后的动作（如果适用）
    usage: dict = {}  # token 使用统计


class BaseLLM(ABC):
    """国内模型统一接口"""

    @abstractmethod
    async def chat_with_vision(
        self,
        messages: list[dict],
        images: list[str],  # 支持 URL 或 base64
    ) -> LLMResponse:
        """带图像理解的对话

        Args:
            messages: OpenAI 格式的消息列表
            images: 图像列表（URL 或 base64 字符串）

        Returns:
            LLMResponse 包含响应内容和解析后的动作
        """
        pass

    @abstractmethod
    def parse_action(self, response: str) -> ActionResult | None:
        """解析模型输出为结构化动作

        Args:
            response: 模型的原始文本输出

        Returns:
            ActionResult 或 None（如果无法解析）
        """
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """返回模型名称，用于日志"""
        pass
```

**Step 2: 验证语法正确**

Run: `python -c "from backend.llm.base import BaseLLM, LLMResponse, ActionResult; print('OK')"`
Expected: OK

**Step 3: Commit**

```bash
git add backend/llm/base.py
git commit -m "feat(llm): add BaseLLM abstract interface"
```

---

## Task 3: 实现工具函数

**Files:**
- Create: `backend/llm/utils.py`

**Step 1: 创建 utils.py 文件**

```python
"""LLM 模块工具函数"""

import base64
from pathlib import Path


def encode_image_to_base64(image_path: str) -> str:
    """将图像文件编码为 base64 字符串

    Args:
        image_path: 图像文件路径

    Returns:
        base64 编码的字符串

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 不支持的图像格式
    """
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"图像文件不存在: {image_path}")

    # 支持的格式
    supported_formats = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
    if path.suffix.lower() not in supported_formats:
        raise ValueError(f"不支持的图像格式: {path.suffix}")

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
```

**Step 2: 验证语法正确**

Run: `python -c "from backend.llm.utils import encode_image_to_base64; print('OK')"`
Expected: OK

**Step 3: Commit**

```bash
git add backend/llm/utils.py
git commit -m "feat(llm): add image encoding utility"
```

---

## Task 4: 实现 QwenChat 类

**Files:**
- Create: `backend/llm/qwen.py`

**Step 1: 创建 qwen.py 文件**

```python
"""通义千问视觉模型实现"""

import json
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
            f"{m['role']}: {m['content']}" for m in messages
        )
        content.append({"text": text})

        return content

    def parse_action(self, response: str) -> ActionResult | None:
        """解析 Browser-Use 格式的动作输出"""
        try:
            # 尝试提取 JSON 块
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                data = json.loads(response[json_start:json_end])
                return ActionResult(
                    action=data.get("action", ""),
                    selector=data.get("selector"),
                    value=data.get("value"),
                    reasoning=data.get("reasoning", ""),
                )
        except json.JSONDecodeError:
            pass

        return None
```

**Step 2: 验证语法正确**

Run: `python -c "from backend.llm.qwen import QwenChat; print('OK')"`
Expected: OK

**Step 3: Commit**

```bash
git add backend/llm/qwen.py
git commit -m "feat(llm): implement QwenChat with vision support"
```

---

## Task 5: 更新模块导出

**Files:**
- Modify: `backend/llm/__init__.py`

**Step 1: 查看当前内容**

Run: `cat backend/llm/__init__.py`
Expected: 可能是空文件或简单内容

**Step 2: 更新 __init__.py**

```python
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

**Step 3: 验证导入正确**

Run: `python -c "from backend.llm import QwenChat, get_default_llm; print('OK')"`
Expected: OK

**Step 4: Commit**

```bash
git add backend/llm/__init__.py
git commit -m "feat(llm): add module exports and factory function"
```

---

## Task 6: 编写验证测试

**Files:**
- Create: `backend/tests/test_qwen_vision.py`

**Step 1: 创建测试文件**

```python
"""验证通义千问视觉能力"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv()


async def test_basic_chat():
    """测试基础文本对话"""
    from backend.llm import QwenChat

    llm = QwenChat()

    response = await llm.chat_with_vision(
        messages=[{"role": "user", "content": "你好，请回复'OK'"}],
        images=[],
    )

    assert response.content, "响应内容不应为空"
    print(f"✅ 基础对话测试通过: {response.content}")
    return True


async def test_vision_with_url():
    """测试图像 URL 理解能力"""
    from backend.llm import QwenChat

    llm = QwenChat()

    # 使用公开测试图片
    test_image = "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0033279361/p405458.png"

    response = await llm.chat_with_vision(
        messages=[{"role": "user", "content": "请描述这张图片的内容"}],
        images=[test_image],
    )

    assert response.content, "响应内容不应为空"
    print(f"✅ 图像 URL 测试通过: {response.content[:100]}...")
    return True


async def test_action_parsing():
    """测试动作解析能力"""
    from backend.llm import QwenChat

    llm = QwenChat()

    # 模拟包含动作的响应
    test_response = '''
    根据页面内容，我需要点击登录按钮。
    {"action": "click", "selector": "#login-btn", "reasoning": "用户需要登录"}
    '''

    result = llm.parse_action(test_response)

    assert result is not None, "应该能解析出动作"
    assert result.action == "click"
    assert result.selector == "#login-btn"
    print(f"✅ 动作解析测试通过: {result}")
    return True


async def test_vision_with_local_file():
    """测试本地图像文件理解能力"""
    from backend.llm import QwenChat

    llm = QwenChat()

    # 使用 screenshots 目录中的测试图片（如果存在）
    screenshot_dir = Path(__file__).parent.parent.parent / "outputs" / "screenshots"
    test_images = list(screenshot_dir.glob("*.png")) if screenshot_dir.exists() else []

    if not test_images:
        print("⏭️ 跳过本地图像测试（无测试图片）")
        return True

    response = await llm.chat_with_vision(
        messages=[{"role": "user", "content": "请描述这个页面的主要元素"}],
        images=[str(test_images[0])],
    )

    assert response.content, "响应内容不应为空"
    print(f"✅ 本地图像测试通过: {response.content[:100]}...")
    return True


async def main():
    """运行所有验证测试"""
    print("=" * 50)
    print("通义千问视觉能力验证")
    print("=" * 50)

    # 检查 API Key
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key or api_key == "your_dashscope_api_key_here":
        print("❌ 未配置 DASHSCOPE_API_KEY")
        return False

    tests = [
        ("基础对话", test_basic_chat),
        ("图像 URL", test_vision_with_url),
        ("动作解析", test_action_parsing),
        ("本地图像", test_vision_with_local_file),
    ]

    results = []
    for name, test in tests:
        print(f"\n测试: {name}")
        try:
            result = await test()
            results.append((name, result))
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            results.append((name, False))

    print("\n" + "=" * 50)
    print("测试结果汇总:")
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}")

    all_passed = all(r[1] for r in results)
    print("=" * 50)
    return all_passed


if __name__ == "__main__":
    import asyncio

    success = asyncio.run(main())
    sys.exit(0 if success else 1)
```

**Step 2: Commit**

```bash
git add backend/tests/test_qwen_vision.py
git commit -m "test(llm): add qwen vision verification tests"
```

---

## Task 7: 运行验证测试

**Files:**
- None (verification only)

**Step 1: 运行测试脚本**

Run: `python backend/tests/test_qwen_vision.py`
Expected:
```
==================================================
通义千问视觉能力验证
==================================================

测试: 基础对话
✅ 基础对话测试通过: ...

测试: 图像 URL
✅ 图像 URL 测试通过: ...

测试: 动作解析
✅ 动作解析测试通过: ...

测试: 本地图像
⏭️ 跳过本地图像测试（无测试图片）

==================================================
测试结果汇总:
  ✅ 基础对话
  ✅ 图像 URL
  ✅ 动作解析
  ✅ 本地图像
==================================================
```

**Step 2: 如果测试失败，检查 API Key 配置**

Run: `echo $DASHSCOPE_API_KEY | head -c 10`
Expected: 显示 API Key 前 10 个字符（确认已配置）

---

## Task 8: 更新进度文档

**Files:**
- Modify: `docs/progress.md`
- Modify: `docs/1_后端主计划.md`

**Step 1: 更新 progress.md**

在 `### Phase 2: 模型适配` 部分替换为：

```markdown
### Phase 2: 模型适配 ✅
- **完成日期**: 2026-03-08
- **更新内容**: 实现统一 LLM 接口、适配通义千问 qwen-vl-max、验证图像理解能力
```

**Step 2: 更新 1_后端主计划.md**

将 Phase 2 的任务勾选：

```markdown
### Phase 2: 模型适配（2-3 天）✅

- [x] 2.1 实现统一 LLM 接口
- [x] 2.2 适配通义千问（首选）
- [ ] 2.3 适配智谱 GLM（备选）
- [x] 2.4 验证图像理解能力
```

**Step 3: Commit**

```bash
git add docs/progress.md docs/1_后端主计划.md
git commit -m "docs: 记录 Phase 2 完成 - 模型适配"
```

---

## Summary

| Task | Description | Est. Time |
|------|-------------|-----------|
| 1 | 更新依赖配置 | 5 min |
| 2 | 实现 BaseLLM 抽象接口 | 10 min |
| 3 | 实现工具函数 | 5 min |
| 4 | 实现 QwenChat 类 | 15 min |
| 5 | 更新模块导出 | 5 min |
| 6 | 编写验证测试 | 15 min |
| 7 | 运行验证测试 | 10 min |
| 8 | 更新进度文档 | 5 min |
| **Total** | | **~70 min** |

---

## Verification Checklist

- [ ] `tenacity` 依赖已添加
- [ ] `BaseLLM` 接口可导入
- [ ] `QwenChat` 类可实例化
- [ ] 基础对话测试通过
- [ ] 图像 URL 测试通过
- [ ] 动作解析测试通过
- [ ] 进度文档已更新
