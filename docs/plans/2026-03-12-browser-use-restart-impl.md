# Browser-Use 重新集成实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 重新启用 browser-use 库，使用官方 OpenAI GPT-4o 完成 ERP 登录自动化测试

**Architecture:** 直接使用 browser-use 原生 API + langchain-openai，零封装零适配器，历史代码归档到 `_archived/` 目录

**Tech Stack:** Python, browser-use, langchain-openai, playwright, pytest

---

## Phase 1: 代码归档

### Task 1: 创建归档目录结构

**Files:**
- Create: `backend/_archived/__init__.py`
- Create: `backend/_archived/agent_simple/__init__.py`
- Create: `backend/_archived/llm/__init__.py`
- Create: `backend/_archived/proxy/__init__.py`
- Create: `backend/_archived/tests/__init__.py`

**Step 1: 创建归档目录**

```bash
mkdir -p backend/_archived/agent_simple
mkdir -p backend/_archived/llm
mkdir -p backend/_archived/proxy
mkdir -p backend/_archived/tests
```

**Step 2: 创建 __init__.py 文件**

```python
# backend/_archived/__init__.py
"""
归档代码目录

此目录包含已弃用的代码，保留供历史参考。
不再维护，请勿在新代码中使用。
"""
```

```python
# backend/_archived/agent_simple/__init__.py
"""SimpleAgent 归档代码"""
```

```python
# backend/_archived/llm/__init__.py
"""LLM 适配器归档代码"""
```

```python
# backend/_archived/proxy/__init__.py
"""代理服务归档代码"""
```

```python
# backend/_archived/tests/__init__.py
"""旧测试脚本归档"""
```

**Step 3: 验证目录结构**

```bash
ls -la backend/_archived/
```

Expected: 4 directories (agent_simple, llm, proxy, tests) and __init__.py

**Step 4: Commit**

```bash
git add backend/_archived/
git commit -m "chore: 创建归档目录结构"
```

---

### Task 2: 归档 SimpleAgent 代码

**Files:**
- Move: `backend/agent_simple/*` → `backend/_archived/agent_simple/`

**Step 1: 移动 SimpleAgent 代码**

```bash
mv backend/agent_simple/* backend/_archived/agent_simple/
rmdir backend/agent_simple
```

**Step 2: 添加归档注释到主文件**

编辑 `backend/_archived/agent_simple/agent.py`，在文件顶部添加：

```python
"""
⚠️ 已归档 - 2026-03-12

原因：切换到 browser-use + 官方 OpenAI API，不再需要自研 Agent。
保留供历史参考。

替代方案：直接使用 browser_use.Agent + langchain_openai.ChatOpenAI

原 SimpleAgent 架构：
- perception.py: 页面感知
- decision.py: LLM 决策
- executor.py: 动作执行
- agent.py: 循环控制
"""
```

**Step 3: 验证移动完成**

```bash
ls backend/_archived/agent_simple/
```

Expected: agent.py, perception.py, decision.py, executor.py, prompts.py, memory.py, types.py, form_filler/, __init__.py

**Step 4: Commit**

```bash
git add backend/_archived/agent_simple/
git add -A backend/agent_simple/  # 处理删除
git commit -m "chore: 归档 SimpleAgent 代码"
```

---

### Task 3: 归档 LLM 适配器

**Files:**
- Move: `backend/llm/browser_use_adapter.py` → `backend/_archived/llm/`
- Move: `backend/llm/qwen.py` → `backend/_archived/llm/`
- Move: `backend/llm/deepseek.py` → `backend/_archived/llm/`
- Move: `backend/llm/azure_openai.py` → `backend/_archived/llm/`

**Step 1: 移动 LLM 适配器文件**

```bash
mv backend/llm/browser_use_adapter.py backend/_archived/llm/
mv backend/llm/qwen.py backend/_archived/llm/
mv backend/llm/deepseek.py backend/_archived/llm/
mv backend/llm/azure_openai.py backend/_archived/llm/
```

**Step 2: 添加归档注释**

编辑 `backend/_archived/llm/browser_use_adapter.py`，在顶部添加：

```python
"""
⚠️ 已归档 - 2026-03-12

原因：切换到官方 OpenAI API，不再需要国产模型适配器。
保留供历史参考。

替代方案：直接使用 langchain_openai.ChatOpenAI
"""
```

**Step 3: 更新 backend/llm/__init__.py**

```python
# backend/llm/__init__.py
"""
LLM 模块

当前仅支持 OpenAI 官方 API。
历史适配器已归档到 _archived/llm/
"""

from .base import BaseLLM
from .openai import OpenAIChat
from .config import LLMConfig, get_config
from .factory import LLMFactory, get_llm

__all__ = [
    "BaseLLM",
    "OpenAIChat",
    "LLMConfig",
    "get_config",
    "LLMFactory",
    "get_llm",
]
```

**Step 4: 验证 LLM 目录**

```bash
ls backend/llm/
```

Expected: __init__.py, base.py, openai.py, config.py, factory.py

**Step 5: Commit**

```bash
git add backend/llm/__init__.py
git add backend/_archived/llm/
git commit -m "chore: 归档国产模型 LLM 适配器"
```

---

### Task 4: 归档代理服务

**Files:**
- Move: `backend/proxy/*` → `backend/_archived/proxy/`

**Step 1: 移动代理服务代码**

```bash
mv backend/proxy/* backend/_archived/proxy/
rmdir backend/proxy
```

**Step 2: 添加归档注释**

编辑 `backend/_archived/proxy/openai_proxy.py`，在顶部添加：

```python
"""
⚠️ 已归档 - 2026-03-12

原因：切换到官方 OpenAI API，不再需要代理服务。
保留供历史参考。

替代方案：直接使用 api.openai.com
"""
```

**Step 3: Commit**

```bash
git add backend/_archived/proxy/
git add -A backend/proxy/
git commit -m "chore: 归档代理服务代码"
```

---

### Task 5: 归档旧测试脚本

**Files:**
- Move: `backend/tests/run_validation.py` → `backend/_archived/tests/`
- Move: `backend/tests/run_validation_azure.py` → `backend/_archived/tests/`

**Step 1: 移动旧验证脚本**

```bash
mv backend/tests/run_validation.py backend/_archived/tests/ 2>/dev/null || true
mv backend/tests/run_validation_azure.py backend/_archived/tests/ 2>/dev/null || true
```

**Step 2: 添加归档注释**

```python
# backend/_archived/tests/run_validation.py 顶部添加
"""
⚠️ 已归档 - 2026-03-12

原因：旧的 Browser-Use 验证脚本，使用国产模型适配器。
保留供历史参考。

替代方案：使用 pytest + browser-use 原生 API
"""
```

**Step 3: Commit**

```bash
git add backend/_archived/tests/
git commit -m "chore: 归档旧验证测试脚本"
```

---

## Phase 2: 依赖更新

### Task 6: 更新 pyproject.toml

**Files:**
- Modify: `pyproject.toml`

**Step 1: 更新依赖清单**

编辑 `pyproject.toml`，确保 dependencies 包含：

```toml
[project]
dependencies = [
    "browser-use>=0.12.0",
    "langchain-openai>=0.3.0",
    "playwright>=1.40.0",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "pyyaml>=6.0",
    "python-dotenv>=1.0.0",
    "fastapi>=0.135.1",
    "uvicorn>=0.34.0",
]
```

**Step 2: 同步依赖**

```bash
uv sync
```

Expected: 依赖安装成功，无错误

**Step 3: 验证安装**

```bash
uv run python -c "from browser_use import Agent; from langchain_openai import ChatOpenAI; print('OK')"
```

Expected: 输出 "OK"

**Step 4: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "chore: 更新依赖，添加 langchain-openai"
```

---

## Phase 3: OpenAI 封装

### Task 7: 创建 OpenAI 封装

**Files:**
- Create: `backend/llm/openai.py`

**Step 1: 编写 OpenAI 封装**

```python
# backend/llm/openai.py
"""OpenAI LLM 封装

提供简洁的 OpenAI API 封装，用于 browser-use 集成。
"""

import os
from typing import Any

from langchain_openai import ChatOpenAI

from .base import BaseLLM


class OpenAIChat(BaseLLM):
    """OpenAI Chat 模型封装

    直接使用 langchain_openai，无需额外适配。
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.1,
        api_key: str | None = None,
        **kwargs: Any,
    ):
        """初始化 OpenAI Chat

        Args:
            model: 模型名称，默认 gpt-4o
            temperature: 温度参数
            api_key: API Key，默认从环境变量读取
            **kwargs: 其他参数传递给 ChatOpenAI
        """
        self.model_name = model
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self._api_key:
            raise ValueError("OPENAI_API_KEY not set")

        self._llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=self._api_key,
            **kwargs,
        )

    @property
    def llm(self) -> ChatOpenAI:
        """获取 langchain ChatOpenAI 实例

        可直接传递给 browser-use Agent
        """
        return self._llm

    async def chat(self, messages: list[dict]) -> str:
        """聊天接口

        Args:
            messages: 消息列表

        Returns:
            模型响应文本
        """
        from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

        lc_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                lc_messages.append(SystemMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))
            else:
                lc_messages.append(HumanMessage(content=content))

        response = await self._llm.ainvoke(lc_messages)
        return response.content

    async def chat_with_vision(
        self,
        messages: list[dict],
        images: list[str] | None = None,
    ) -> Any:
        """带视觉的聊天接口

        Args:
            messages: 消息列表
            images: 图像 URL 列表

        Returns:
            模型响应
        """
        # GPT-4o 原生支持多模态，直接使用 chat
        if images:
            # 将图像添加到最后一条用户消息
            for msg in reversed(messages):
                if msg.get("role") == "user":
                    content = msg.get("content", "")
                    image_content = [{"type": "image_url", "image_url": {"url": img}} for img in images]
                    msg["content"] = [{"type": "text", "text": content}] + image_content
                    break

        return await self.chat(messages)
```

**Step 2: 更新 base.py（如果需要）**

确保 `backend/llm/base.py` 包含 BaseLLM 接口：

```python
# backend/llm/base.py
"""LLM 基础接口"""

from abc import ABC, abstractmethod
from typing import Any


class BaseLLM(ABC):
    """LLM 基础接口"""

    model_name: str

    @abstractmethod
    async def chat(self, messages: list[dict]) -> str:
        """聊天接口"""
        pass

    @abstractmethod
    async def chat_with_vision(
        self,
        messages: list[dict],
        images: list[str] | None = None,
    ) -> Any:
        """带视觉的聊天接口"""
        pass
```

**Step 3: 验证导入**

```bash
uv run python -c "from backend.llm import OpenAIChat; print('OK')"
```

Expected: 输出 "OK"

**Step 4: Commit**

```bash
git add backend/llm/openai.py backend/llm/base.py backend/llm/__init__.py
git commit -m "feat: 添加 OpenAI 封装模块"
```

---

## Phase 4: 测试脚本

### Task 8: 创建登录测试

**Files:**
- Create: `backend/tests/test_login_browser_use.py`

**Step 1: 编写测试配置 fixture**

```python
# backend/tests/conftest.py 添加以下内容

import os
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def erp_config():
    """ERP 测试配置"""
    return {
        "base_url": os.getenv("ERP_BASE_URL", "https://erp.example.com"),
        "username": os.getenv("ERP_USERNAME", "test_user"),
        "password": os.getenv("ERP_PASSWORD", ""),
    }
```

**Step 2: 编写登录测试**

```python
# backend/tests/test_login_browser_use.py
"""Browser-Use 登录测试

使用官方 OpenAI GPT-4o 进行 ERP 登录自动化测试。
"""

import pytest
from browser_use import Agent
from langchain_openai import ChatOpenAI


@pytest.mark.asyncio
async def test_login_with_browser_use(erp_config):
    """测试 ERP 登录场景

    使用 browser-use + GPT-4o 自动完成登录流程。
    """
    # 1. 初始化 LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.1,
    )

    # 2. 定义登录任务
    task = f"""
    登录 ERP 系统，步骤如下：

    1. 打开登录页面：{erp_config['base_url']}/login
    2. 如果显示手机验证码登录，点击切换到"密码登录"
    3. 输入用户名：{erp_config['username']}
    4. 输入密码：{erp_config['password']}
    5. 点击登录按钮
    6. 确认登录成功（页面跳转到首页或显示欢迎信息）

    注意：
    - 如果有弹窗，先关闭弹窗
    - 如果登录失败，检查错误信息并重试
    """

    # 3. 创建 Agent
    agent = Agent(
        task=task,
        llm=llm,
        use_vision=True,
        max_actions_per_step=5,
    )

    # 4. 执行任务
    result = await agent.run()

    # 5. 验证结果
    assert result.is_done, "登录任务未完成"
    assert result.success, f"登录失败: {result.final_result}"


@pytest.mark.asyncio
async def test_login_with_screenshot(erp_config, tmp_path):
    """测试登录并保存截图

    每一步都保存截图用于调试。
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

    task = f"""
    登录 ERP 系统：
    1. 打开 {erp_config['base_url']}/login
    2. 切换到密码登录
    3. 输入用户名：{erp_config['username']}
    4. 输入密码：{erp_config['password']}
    5. 点击登录
    """

    agent = Agent(
        task=task,
        llm=llm,
        use_vision=True,
        save_conversation_path=str(tmp_path / "conversation"),
    )

    result = await agent.run()

    # 验证截图已保存
    conversation_dir = tmp_path / "conversation"
    if conversation_dir.exists():
        screenshots = list(conversation_dir.glob("*.png"))
        assert len(screenshots) > 0, "没有保存截图"

    assert result.is_done, "登录任务未完成"
```

**Step 3: 更新 pytest.ini 支持异步**

确保 `pyproject.toml` 包含：

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["backend/tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
```

**Step 4: 验证测试发现**

```bash
uv run pytest backend/tests/test_login_browser_use.py --collect-only
```

Expected: 显示 2 个测试用例

**Step 5: Commit**

```bash
git add backend/tests/test_login_browser_use.py backend/tests/conftest.py pyproject.toml
git commit -m "feat: 添加 browser-use 登录测试"
```

---

## Phase 5: 环境配置

### Task 9: 更新环境变量模板

**Files:**
- Modify: `.env.example`

**Step 1: 更新 .env.example**

```bash
# .env.example

# ============================================
# OpenAI 配置（必需）
# ============================================
OPENAI_API_KEY=sk-xxx

# ============================================
# ERP 系统配置
# ============================================
ERP_BASE_URL=https://erp.example.com
ERP_USERNAME=test_user
ERP_PASSWORD=your_password

# ============================================
# 可选配置
# ============================================
# OPENAI_MODEL=gpt-4o
# OPENAI_TEMPERATURE=0.1
```

**Step 2: 创建 .env（如果不存在）**

```bash
cp .env.example .env
```

**Step 3: 提示用户填入 API Key**

```bash
echo "请编辑 .env 文件，填入你的 OPENAI_API_KEY"
```

**Step 4: Commit**

```bash
git add .env.example
git commit -m "docs: 更新环境变量模板"
```

---

## Phase 6: 文档更新

### Task 10: 更新 CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

**Step 1: 更新架构说明**

将 CLAUDE.md 更新为：

```markdown
# CLAUDE.md

## Project Overview

AI + Playwright UI 自动化测试项目。使用 browser-use + OpenAI GPT-4o 实现 ERP 系统自动化测试。

## Tech Stack

**Backend**: Python, browser-use, langchain-openai, Playwright, pytest

**Frontend**: React 18, TypeScript, Vite 5, Tailwind CSS 3

## Architecture

```
┌─────────────────────────────────────────────┐
│              测试脚本 (pytest)               │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│           browser-use Agent (原生)           │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│           OpenAI GPT-4o (官方)               │
└─────────────────────────────────────────────┘
```

## Key Commands

**Setup**
```bash
uv sync                                    # 安装依赖
playwright install chromium                # 安装浏览器
cp .env.example .env                       # 配置环境变量
```

**Run Tests**
```bash
pytest backend/tests/test_login_browser_use.py -v
```

## Reference

- `docs/plans/2026-03-12-browser-use-restart-design.md` - 设计文档
- `backend/_archived/` - 历史代码归档
```

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: 更新 CLAUDE.md 架构说明"
```

---

### Task 11: 更新后端主计划

**Files:**
- Modify: `docs/1_后端主计划.md`

**Step 1: 添加 Phase 10**

在 `docs/1_后端主计划.md` 末尾添加：

```markdown
### Phase 10: Browser-Use 重新集成（2026-03-12）🔄

- [x] 10.0 设计文档 ✅
- [ ] 10.1 代码归档
  - [ ] 创建 `_archived/` 目录结构
  - [ ] 归档 SimpleAgent 代码
  - [ ] 归档 LLM 适配器
  - [ ] 归档代理服务
- [ ] 10.2 依赖更新
  - [ ] 添加 langchain-openai
  - [ ] 验证 browser-use 兼容性
- [ ] 10.3 OpenAI 封装
  - [ ] 创建 `backend/llm/openai.py`
- [ ] 10.4 测试脚本
  - [ ] 创建 `test_login_browser_use.py`
- [ ] 10.5 验证运行
  - [ ] 登录测试通过

**设计文档**: `docs/plans/2026-03-12-browser-use-restart-design.md`
```

**Step 2: Commit**

```bash
git add docs/1_后端主计划.md
git commit -m "docs: 更新后端主计划 Phase 10"
```

---

## Phase 7: 验证

### Task 12: 运行登录测试

**Step 1: 确认环境变量**

```bash
cat .env | grep OPENAI_API_KEY
```

Expected: 显示 OPENAI_API_KEY=sk-xxx（非空）

**Step 2: 运行测试**

```bash
uv run pytest backend/tests/test_login_browser_use.py -v --tb=short
```

Expected: 测试通过 ✅

**Step 3: 如果失败，检查日志**

```bash
uv run pytest backend/tests/test_login_browser_use.py -v -s --log-cli-level=DEBUG
```

**Step 4: 成功后 Commit**

```bash
git add -A
git commit -m "feat: browser-use 重新集成完成，登录测试通过"
```

---

## Summary

| Phase | Tasks | 预计时间 |
|-------|-------|----------|
| Phase 1: 代码归档 | Task 1-5 | 30分钟 |
| Phase 2: 依赖更新 | Task 6 | 15分钟 |
| Phase 3: OpenAI 封装 | Task 7 | 15分钟 |
| Phase 4: 测试脚本 | Task 8 | 20分钟 |
| Phase 5: 环境配置 | Task 9 | 10分钟 |
| Phase 6: 文档更新 | Task 10-11 | 15分钟 |
| Phase 7: 验证 | Task 12 | 15分钟 |
| **总计** | **12 Tasks** | **约 2 小时** |
