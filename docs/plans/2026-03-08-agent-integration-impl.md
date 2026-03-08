# Phase 3: Agent 改造实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将国内模型（通义千问）集成到 Browser-Use 框架，实现 AI 决策 + Playwright 执行的技术闭环。

**Architecture:** 采用混合方案 - LLM 适配器 + 自定义 System Prompt 扩展。通过 BrowserUseAdapter 将 QwenChat 适配到 Browser-Use 的 BaseChatModel Protocol，通过 extend_system_message 注入中文化 Prompt。

**Tech Stack:** Python, Browser-Use, Playwright, 通义千问 (qwen-vl-max), pydantic

---

## Task 1: 实现截图管理工具

**Files:**
- Create: `backend/utils/screenshot.py`

**Step 1: 创建截图管理类**

```python
"""截图文件管理"""

from pathlib import Path
from datetime import datetime


class ScreenshotManager:
    """截图文件管理器"""

    def __init__(self, output_dir: str, task_id: str):
        """初始化截图管理器

        Args:
            output_dir: 输出根目录
            task_id: 任务 ID，用于创建子目录
        """
        self.screenshot_dir = Path(output_dir) / "screenshots" / task_id
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def get_path(self, step: int, suffix: str = "") -> str:
        """生成截图文件路径

        Args:
            step: 步骤编号
            suffix: 文件名后缀（可选）

        Returns:
            截图文件的完整路径
        """
        filename = f"step_{step:03d}{suffix}.png"
        return str(self.screenshot_dir / filename)

    def get_dir(self) -> str:
        """获取截图目录路径"""
        return str(self.screenshot_dir)
```

**Step 2: 验证语法正确**

Run: `python -c "from backend.utils.screenshot import ScreenshotManager; print('OK')"`
Expected: OK

**Step 3: Commit**

```bash
git add backend/utils/screenshot.py
git commit -m "feat(utils): add ScreenshotManager for step screenshots"
```

---

## Task 2: 实现结构化日志工具

**Files:**
- Create: `backend/utils/logger.py`

**Step 1: 创建结构化日志类**

```python
"""结构化日志工具"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StructuredLogger:
    """结构化日志记录器，输出 JSONL 格式"""

    def __init__(self, output_dir: str, task_id: str):
        """初始化日志记录器

        Args:
            output_dir: 输出根目录
            task_id: 任务 ID，用于创建日志文件名
        """
        self.log_dir = Path(output_dir) / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"{task_id}.jsonl"

    def log_step(
        self,
        step: int,
        action: str,
        selector: str | None,
        reasoning: str,
        success: bool,
        screenshot_path: str | None = None,
        error: str | None = None,
        **extra: Any,
    ) -> None:
        """记录执行步骤

        Args:
            step: 步骤编号
            action: 执行的动作类型
            selector: 目标元素选择器
            reasoning: AI 的推理说明
            success: 是否成功
            screenshot_path: 截图文件路径
            error: 错误信息（如果有）
            **extra: 其他额外字段
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "action": action,
            "selector": selector,
            "reasoning": reasoning,
            "success": success,
            "screenshot": screenshot_path,
            "error": error,
            **extra,
        }
        self._write_entry(entry)

    def log_error(self, step: int, error: str, **extra: Any) -> None:
        """记录错误信息"""
        self.log_step(
            step=step,
            action="error",
            selector=None,
            reasoning="",
            success=False,
            error=error,
            **extra,
        )

    def log_summary(
        self,
        total_steps: int,
        success: bool,
        duration_seconds: float,
        **extra: Any,
    ) -> None:
        """记录执行摘要"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "summary",
            "total_steps": total_steps,
            "success": success,
            "duration_seconds": duration_seconds,
            **extra,
        }
        self._write_entry(entry)

    def _write_entry(self, entry: dict) -> None:
        """写入日志条目"""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_log_file(self) -> str:
        """获取日志文件路径"""
        return str(self.log_file)
```

**Step 2: 验证语法正确**

Run: `python -c "from backend.utils.logger import StructuredLogger; print('OK')"`
Expected: OK

**Step 3: 更新 utils 模块导出**

修改 `backend/utils/__init__.py`:

```python
"""工具函数模块"""

from .logger import StructuredLogger
from .screenshot import ScreenshotManager

__all__ = [
    "StructuredLogger",
    "ScreenshotManager",
]
```

**Step 4: 验证导入正确**

Run: `python -c "from backend.utils import StructuredLogger, ScreenshotManager; print('OK')"`
Expected: OK

**Step 5: Commit**

```bash
git add backend/utils/logger.py backend/utils/__init__.py
git commit -m "feat(utils): add StructuredLogger for JSONL logging"
```

---

## Task 3: 实现中文化 Prompt 模板

**Files:**
- Create: `backend/agent/prompts.py`

**Step 1: 创建 Prompt 模板**

```python
"""Agent Prompt 模板"""

# 中文页面处理增强指令
# 通过 Browser-Use 的 extend_system_message 参数注入
CHINESE_ENHANCEMENT = """
## 中文页面处理增强

1. **元素识别优先级**
   - 优先使用可见文本（按钮文字、链接文字）
   - 其次使用 placeholder 属性
   - 最后使用 aria-label 或 title

2. **常见中文表单字段**
   - 用户名/账号: username, account, login, 用户名, 账号
   - 密码: password, pwd, passwd, 密码
   - 登录: 登录, 登入, 确定, 提交, Login
   - 搜索: 搜索, 查询, 检索, Search
   - 取消: 取消, 关闭, Cancel

3. **错误处理策略**
   - 遇到验证码时，等待 5 秒后重试
   - 页面加载超时时，刷新页面
   - 元素未找到时，先滚动页面再查找
   - 表单提交失败时，检查错误提示并调整

4. **动作输出格式**
   始终输出标准 JSON 格式：
   ```json
   {
     "action": "click|fill|goto|select|scroll|wait|done",
     "selector": "CSS选择器或文本",
     "value": "输入值（fill时使用）",
     "reasoning": "执行此动作的原因"
   }
   ```

5. **选择器策略**
   - 优先使用文本选择器: text=登录
   - 其次使用 role 选择器: role=button[name="登录"]
   - 最后使用 CSS 选择器: button.login-btn
"""

# 登录场景专用 Prompt
LOGIN_TASK_PROMPT = """
执行登录操作：
1. 打开登录页面
2. 找到用户名输入框，输入账号
3. 找到密码输入框，输入密码
4. 点击登录按钮
5. 验证登录是否成功（检查是否跳转到主页或显示用户信息）
"""
```

**Step 2: 验证语法正确**

Run: `python -c "from backend.agent.prompts import CHINESE_ENHANCEMENT; print('OK')"`
Expected: OK

**Step 3: Commit**

```bash
git add backend/agent/prompts.py
git commit -m "feat(agent): add Chinese enhancement prompts"
```

---

## Task 4: 实现 Browser-Use 适配器

**Files:**
- Create: `backend/llm/browser_use_adapter.py`
- Modify: `backend/llm/__init__.py`

**Step 1: 创建适配器类**

```python
"""Browser-Use LLM 适配器"""

import logging
from typing import Any

from pydantic import BaseModel

from browser_use.llm.base import BaseChatModel
from browser_use.llm.messages import BaseMessage
from browser_use.llm.views import ChatInvokeCompletion

from .base import BaseLLM

logger = logging.getLogger(__name__)


class BrowserUseAdapter(BaseChatModel):
    """将国内模型适配到 Browser-Use 的 BaseChatModel Protocol

    这个适配器将我们的 QwenChat（或其他 BaseLLM 实现）
    转换为 Browser-Use 期望的接口格式。
    """

    _verified_api_keys: bool = True  # 跳过 Browser-Use 的 API Key 验证

    def __init__(self, llm: BaseLLM):
        """初始化适配器

        Args:
            llm: 底层 LLM 实例（如 QwenChat）
        """
        self._llm = llm
        self.model = llm.model_name

    @property
    def provider(self) -> str:
        """返回提供商名称"""
        return "chinese-domestic"

    @property
    def name(self) -> str:
        """返回模型名称"""
        return self.model

    async def ainvoke(
        self,
        messages: list[BaseMessage],
        output_format: type[BaseModel] | None = None,
        **kwargs: Any,
    ) -> ChatInvokeCompletion[str]:
        """调用底层 LLM 并返回结果

        Args:
            messages: Browser-Use 格式的消息列表
            output_format: 期望的输出格式（用于结构化输出）
            **kwargs: 其他参数

        Returns:
            ChatInvokeCompletion 包含响应内容
        """
        # 1. 转换消息格式
        converted_messages, images = self._convert_messages(messages)

        # 2. 调用底层 LLM
        response = await self._llm.chat_with_vision(
            messages=converted_messages,
            images=images,
        )

        # 3. 返回 Browser-Use 期望的格式
        return ChatInvokeCompletion(
            content=response.content,
            usage=response.usage,
        )

    def _convert_messages(
        self, messages: list[BaseMessage]
    ) -> tuple[list[dict], list[str]]:
        """转换消息格式并提取图像

        Args:
            messages: Browser-Use 格式的消息列表

        Returns:
            (转换后的消息列表, 图像列表)
        """
        converted = []
        images = []

        for msg in messages:
            # 提取角色
            role = getattr(msg, "role", "user")

            # 处理内容（可能是字符串或列表）
            content = getattr(msg, "content", "")
            text_parts = []
            image_urls = []

            if isinstance(content, str):
                text_parts.append(content)
            elif isinstance(content, list):
                for part in content:
                    if isinstance(part, dict):
                        if part.get("type") == "text":
                            text_parts.append(part.get("text", ""))
                        elif part.get("type") == "image_url":
                            url = part.get("image_url", {})
                            if isinstance(url, dict):
                                image_urls.append(url.get("url", ""))
                            elif isinstance(url, str):
                                image_urls.append(url)
                        elif part.get("type") == "image":
                            # 处理 image 类型
                            img_data = part.get("image", "")
                            if img_data:
                                image_urls.append(img_data)

            # 合并文本
            full_text = "\n".join(text_parts)
            converted.append({"role": role, "content": full_text})

            # 收集图像
            images.extend(image_urls)

        return converted, images
```

**Step 2: 验证语法正确**

Run: `python -c "from backend.llm.browser_use_adapter import BrowserUseAdapter; print('OK')"`
Expected: OK

**Step 3: 更新 LLM 模块导出**

修改 `backend/llm/__init__.py`，添加导出：

```python
"""LLM 模块 - 国内模型适配层"""

from .base import BaseLLM, LLMResponse, ActionResult
from .qwen import QwenChat
from .browser_use_adapter import BrowserUseAdapter

__all__ = [
    "BaseLLM",
    "LLMResponse",
    "ActionResult",
    "QwenChat",
    "BrowserUseAdapter",
]


def get_default_llm() -> BaseLLM:
    """获取默认的 LLM 实例（通义千问）"""
    return QwenChat()
```

**Step 4: 验证导入正确**

Run: `python -c "from backend.llm import BrowserUseAdapter, QwenChat; print('OK')"`
Expected: OK

**Step 5: Commit**

```bash
git add backend/llm/browser_use_adapter.py backend/llm/__init__.py
git commit -m "feat(llm): add BrowserUseAdapter for domestic LLM integration"
```

---

## Task 5: 实现 Agent 封装类

**Files:**
- Create: `backend/agent/browser_agent.py`
- Modify: `backend/agent/__init__.py`

**Step 1: 创建 Agent 封装类**

```python
"""Browser Agent 封装类"""

import asyncio
import logging
import time
import uuid
from pathlib import Path

from browser_use import Agent
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContext

from ..llm.base import BaseLLM
from ..llm.browser_use_adapter import BrowserUseAdapter
from ..utils.logger import StructuredLogger
from ..utils.screenshot import ScreenshotManager
from .prompts import CHINESE_ENHANCEMENT

logger = logging.getLogger(__name__)


class UIBrowserAgent:
    """封装 Browser-Use Agent，集成国内模型

    提供简化的接口来执行 UI 自动化任务：
    - 自动集成国内 LLM（通义千问）
    - 自动保存截图和日志
    - 支持回调函数监控执行过程
    """

    def __init__(
        self,
        task: str,
        llm: BaseLLM,
        output_dir: str = "outputs",
        task_id: str | None = None,
        max_failures: int = 3,
        max_steps: int = 20,
        use_vision: bool = True,
    ):
        """初始化 Agent

        Args:
            task: 任务描述（自然语言）
            llm: LLM 实例（如 QwenChat）
            output_dir: 输出目录
            task_id: 任务 ID（可选，自动生成）
            max_failures: 最大失败次数
            max_steps: 最大执行步数
            use_vision: 是否使用视觉能力
        """
        self.task = task
        self.llm = llm
        self.output_dir = output_dir
        self.task_id = task_id or str(uuid.uuid4())[:8]
        self.max_failures = max_failures
        self.max_steps = max_steps
        self.use_vision = use_vision

        # 创建适配器
        self.adapter = BrowserUseAdapter(llm)

        # 初始化工具
        self.screenshot_manager = ScreenshotManager(output_dir, self.task_id)
        self.logger = StructuredLogger(output_dir, self.task_id)

        # 执行状态
        self._step_count = 0
        self._start_time: float | None = None

    async def run(self) -> dict:
        """执行任务

        Returns:
            执行结果字典，包含：
            - success: 是否成功
            - steps: 执行步数
            - duration_seconds: 执行时长
            - history: 执行历史
            - screenshot_dir: 截图目录
            - log_file: 日志文件
        """
        self._start_time = time.time()
        self._step_count = 0

        logger.info(f"开始执行任务: {self.task[:50]}...")
        logger.info(f"任务 ID: {self.task_id}")

        try:
            # 创建 Browser-Use Agent
            agent = Agent(
                task=self.task,
                llm=self.adapter,
                extend_system_message=CHINESE_ENHANCEMENT,
                max_failures=self.max_failures,
                use_vision=self.use_vision,
            )

            # 注册回调
            agent.register_new_step_callback(self._on_step)

            # 执行
            result = await agent.run()

            # 记录摘要
            duration = time.time() - self._start_time
            self.logger.log_summary(
                total_steps=self._step_count,
                success=result.is_done,
                duration_seconds=duration,
            )

            logger.info(f"任务完成: 成功={result.is_done}, 步数={self._step_count}")

            return {
                "success": result.is_done,
                "steps": self._step_count,
                "duration_seconds": duration,
                "history": result.history,
                "screenshot_dir": self.screenshot_manager.get_dir(),
                "log_file": self.logger.get_log_file(),
            }

        except Exception as e:
            logger.error(f"任务执行失败: {e}")
            self.logger.log_error(self._step_count, str(e))

            duration = time.time() - self._start_time if self._start_time else 0
            return {
                "success": False,
                "steps": self._step_count,
                "duration_seconds": duration,
                "error": str(e),
                "screenshot_dir": self.screenshot_manager.get_dir(),
                "log_file": self.logger.get_log_file(),
            }

    async def _on_step(self, browser_state, agent_output, step: int) -> None:
        """每步回调函数

        Args:
            browser_state: 浏览器状态
            agent_output: Agent 输出
            step: 步骤编号
        """
        self._step_count = step

        # 提取动作信息
        action = ""
        selector = None
        reasoning = ""

        if agent_output and hasattr(agent_output, "action"):
            actions = agent_output.action
            if actions and len(actions) > 0:
                first_action = actions[0]
                action = getattr(first_action, "action", "")
                selector = getattr(first_action, "selector", None)
                reasoning = getattr(first_action, "reasoning", "")

        # 获取截图
        screenshot_path = None
        try:
            if browser_state and hasattr(browser_state, "page"):
                screenshot_path = self.screenshot_manager.get_path(step)
                await browser_state.page.screenshot(path=screenshot_path)
        except Exception as e:
            logger.warning(f"截图失败: {e}")

        # 记录日志
        self.logger.log_step(
            step=step,
            action=action,
            selector=selector,
            reasoning=reasoning,
            success=True,
            screenshot_path=screenshot_path,
        )

        logger.info(f"步骤 {step}: {action} - {reasoning[:50] if reasoning else ''}")
```

**Step 2: 更新 agent 模块导出**

修改 `backend/agent/__init__.py`:

```python
"""Agent 模块"""

from .browser_agent import UIBrowserAgent
from .prompts import CHINESE_ENHANCEMENT, LOGIN_TASK_PROMPT

__all__ = [
    "UIBrowserAgent",
    "CHINESE_ENHANCEMENT",
    "LOGIN_TASK_PROMPT",
]
```

**Step 3: 验证语法正确**

Run: `python -c "from backend.agent import UIBrowserAgent; print('OK')"`
Expected: OK

**Step 4: Commit**

```bash
git add backend/agent/browser_agent.py backend/agent/__init__.py
git commit -m "feat(agent): add UIBrowserAgent wrapper with logging and screenshots"
```

---

## Task 6: 创建验证脚本

**Files:**
- Create: `backend/tests/verify_agent.py`

**Step 1: 创建验证脚本**

```python
"""验证 Agent 基础执行流程"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv()


async def verify_basic_flow():
    """验证 Agent 基础执行流程 - 打开页面并截图"""
    from backend.agent import UIBrowserAgent
    from backend.llm import QwenChat

    print("=" * 50)
    print("Agent 基础流程验证")
    print("=" * 50)

    # 检查 API Key
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ 未配置 DASHSCOPE_API_KEY")
        return False

    # 初始化 LLM
    print("\n1. 初始化通义千问...")
    llm = QwenChat(model="qwen-vl-max")
    print(f"   ✓ 模型: {llm.model_name}")

    # 创建 Agent
    print("\n2. 创建 Agent...")
    agent = UIBrowserAgent(
        task="打开 https://example.com 并截图",
        llm=llm,
        output_dir="outputs/verify",
    )
    print(f"   ✓ 任务 ID: {agent.task_id}")

    # 执行任务
    print("\n3. 执行任务...")
    result = await agent.run()

    # 输出结果
    print("\n4. 执行结果:")
    print(f"   - 成功: {result['success']}")
    print(f"   - 步数: {result['steps']}")
    print(f"   - 耗时: {result['duration_seconds']:.2f}s")
    print(f"   - 截图: {result['screenshot_dir']}")
    print(f"   - 日志: {result['log_file']}")

    return result["success"]


async def verify_login_page():
    """验证 Agent 能打开登录页面"""
    from backend.agent import UIBrowserAgent
    from backend.llm import QwenChat

    print("=" * 50)
    print("登录页面访问验证")
    print("=" * 50)

    llm = QwenChat(model="qwen-vl-max")

    agent = UIBrowserAgent(
        task="打开 https://erptest.epbox.cn/ 登录页面，描述页面内容",
        llm=llm,
        output_dir="outputs/verify_login",
    )

    result = await agent.run()

    print(f"\n执行结果: 成功={result['success']}, 步数={result['steps']}")
    return result["success"]


async def main():
    """运行所有验证"""
    print("\n" + "=" * 60)
    print("Phase 3: Agent 改造验证")
    print("=" * 60)

    tests = [
        ("基础流程", verify_basic_flow),
        ("登录页面", verify_login_page),
    ]

    results = []
    for name, test in tests:
        print(f"\n>>> 测试: {name}")
        try:
            success = await test()
            results.append((name, success))
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            results.append((name, False))

    # 汇总
    print("\n" + "=" * 60)
    print("验证结果汇总:")
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}")

    all_passed = all(r[1] for r in results)
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
```

**Step 2: Commit**

```bash
git add backend/tests/verify_agent.py
git commit -m "test(agent): add basic agent verification script"
```

---

## Task 7: 创建登录场景测试

**Files:**
- Create: `backend/tests/test_login.py`

**Step 1: 创建登录测试**

```python
"""登录场景测试"""

import os
import sys
from pathlib import Path

import pytest

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@pytest.fixture
def llm():
    """创建 LLM 实例"""
    from backend.llm import QwenChat

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        pytest.skip("DASHSCOPE_API_KEY 未配置")

    return QwenChat(model="qwen-vl-max")


@pytest.mark.asyncio
async def test_open_login_page(llm):
    """测试打开登录页面"""
    from backend.agent import UIBrowserAgent

    agent = UIBrowserAgent(
        task="打开 https://erptest.epbox.cn/",
        llm=llm,
        output_dir="outputs/tests/login",
    )

    result = await agent.run()

    assert result["success"], "打开页面失败"
    assert result["steps"] > 0, "没有执行任何步骤"


@pytest.mark.asyncio
async def test_login_flow(llm):
    """测试完整登录流程"""
    from backend.agent import UIBrowserAgent

    agent = UIBrowserAgent(
        task="""
        执行登录操作：
        1. 打开 https://erptest.epbox.cn/
        2. 找到用户名输入框，输入 Y59800075
        3. 找到密码输入框，输入 Aa123456
        4. 点击登录按钮
        """,
        llm=llm,
        output_dir="outputs/tests/login_flow",
        max_steps=15,
    )

    result = await agent.run()

    # 登录可能成功也可能失败（取决于页面状态）
    # 这里主要验证流程能执行完成
    assert result["steps"] > 0, "没有执行任何步骤"
    print(f"\n登录测试结果: 成功={result['success']}, 步数={result['steps']}")


@pytest.mark.asyncio
async def test_fill_form(llm):
    """测试表单填写能力"""
    from backend.agent import UIBrowserAgent

    agent = UIBrowserAgent(
        task="""
        打开 https://erptest.epbox.cn/
        找到用户名输入框并输入 test_user
        截图保存
        """,
        llm=llm,
        output_dir="outputs/tests/fill_form",
        max_steps=10,
    )

    result = await agent.run()

    assert result["steps"] > 0, "没有执行任何步骤"
```

**Step 2: Commit**

```bash
git add backend/tests/test_login.py
git commit -m "test(agent): add login scenario tests"
```

---

## Task 8: 创建测试目标配置文件

**Files:**
- Create: `backend/config/test_targets.yaml`

**Step 1: 创建配置文件**

```yaml
# 测试目标配置
# 用于 POC 场景验证

# 基础 URL
base_url: "https://erptest.epbox.cn/"

# 登录场景配置
login:
  url: "/"
  account: "Y59800075"
  password: "Aa123456"
  success_indicator:
    - "首页"
    - "欢迎"
    - "用户"

# 表单场景配置（待补充）
form:
  url: "/form"
  fields: []

# 搜索场景配置（待补充）
search:
  url: "/search"
  test_keyword: "测试"
```

**Step 2: Commit**

```bash
git add backend/config/test_targets.yaml
git commit -m "chore(config): add test targets configuration"
```

---

## Task 9: 更新进度文档

**Files:**
- Modify: `docs/progress.md`
- Modify: `docs/1_后端主计划.md`

**Step 1: 更新 progress.md**

在 `### Phase 3: Agent 改造` 部分替换为：

```markdown
### Phase 3: Agent 改造 ✅
- **完成日期**: 2026-03-08
- **更新内容**: 实现 BrowserUseAdapter、UIBrowserAgent、中文化 Prompt、截图日志工具、验证脚本
```

**Step 2: 更新 1_后端主计划.md**

将 Phase 3 的任务勾选：

```markdown
### Phase 3: Agent 改造（2-3 天）✅

- [x] 3.1 集成国内模型到 Browser-Use
- [x] 3.2 优化 Prompt 模板
- [x] 3.3 实现截图和日志保存
- [x] 3.4 验证基础执行流程
```

**Step 3: Commit**

```bash
git add docs/progress.md docs/1_后端主计划.md
git commit -m "docs: 记录 Phase 3 完成 - Agent 改造"
```

---

## Summary

| Task | Description | Est. Time |
|------|-------------|-----------|
| 1 | 实现截图管理工具 | 10 min |
| 2 | 实现结构化日志工具 | 15 min |
| 3 | 实现中文化 Prompt 模板 | 10 min |
| 4 | 实现 Browser-Use 适配器 | 20 min |
| 5 | 实现 Agent 封装类 | 25 min |
| 6 | 创建验证脚本 | 15 min |
| 7 | 创建登录场景测试 | 15 min |
| 8 | 创建测试目标配置文件 | 5 min |
| 9 | 更新进度文档 | 5 min |
| **Total** | | **~2 hours** |

---

## Verification Checklist

- [ ] `ScreenshotManager` 可导入且工作正常
- [ ] `StructuredLogger` 可导入且工作正常
- [ ] `CHINESE_ENHANCEMENT` Prompt 可导入
- [ ] `BrowserUseAdapter` 可导入
- [ ] `UIBrowserAgent` 可导入
- [ ] 验证脚本 `verify_agent.py` 可运行
- [ ] 登录测试 `test_login.py` 可运行
- [ ] 进度文档已更新
