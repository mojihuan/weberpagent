# Phase 1: 环境搭建实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 完成 AI + Playwright UI 自动化测试 POC 的开发环境搭建

**Architecture:** 使用 uv 管理 Python 依赖，创建标准化的 backend 模块结构，配置通义千问 API，验证 Playwright 和 LLM 连接

**Tech Stack:** Python 3.11+, uv, Browser-Use, Playwright, DashScope (通义千问 SDK)

---

## Task 1: 创建项目配置文件

**Files:**
- Create: `pyproject.toml`
- Create: `.python-version`
- Create: `.gitignore`

**Step 1: 创建 pyproject.toml**

```toml
[project]
name = "jianzhi-ui-test"
version = "0.1.0"
description = "AI + Playwright UI 自动化测试 POC"
requires-python = ">=3.11"
dependencies = [
    "browser-use>=0.1.0",
    "langchain-core>=0.3.0",
    "dashscope>=1.20.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "ruff>=0.4.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["backend/tests"]

[tool.ruff]
line-length = 100
target-version = "py311"
```

**Step 2: 创建 .python-version**

```
3.11
```

**Step 3: 创建 .gitignore**

```gitignore
# 环境变量
.env

# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
*.egg-info/
dist/
build/

# 输出目录
outputs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Playwright
playwright-report/
test-results/
```

**Step 4: 验证文件创建成功**

Run: `ls -la pyproject.toml .python-version .gitignore`
Expected: 三个文件都存在

**Step 5: Commit**

```bash
git add pyproject.toml .python-version .gitignore
git commit -m "chore: 初始化项目配置文件"
```

---

## Task 2: 创建 backend 目录结构

**Files:**
- Create: `backend/__init__.py`
- Create: `backend/agent/__init__.py`
- Create: `backend/llm/__init__.py`
- Create: `backend/utils/__init__.py`
- Create: `backend/config/__init__.py`
- Create: `backend/tests/__init__.py`

**Step 1: 创建目录结构**

Run: `mkdir -p backend/agent backend/llm backend/utils backend/config backend/tests outputs/screenshots outputs/traces outputs/reports`
Expected: 目录创建成功

**Step 2: 创建 backend/__init__.py**

```python
"""AI + Playwright UI 自动化测试 POC 后端模块"""
__version__ = "0.1.0"
```

**Step 3: 创建 backend/agent/__init__.py**

```python
"""Browser-Use Agent 改造模块"""
```

**Step 4: 创建 backend/llm/__init__.py**

```python
"""国内 LLM 模型适配模块"""
```

**Step 5: 创建 backend/utils/__init__.py**

```python
"""工具函数模块"""
```

**Step 6: 创建 backend/config/__init__.py**

```python
"""配置模块"""
```

**Step 7: 创建 backend/tests/__init__.py**

```python
"""POC 测试用例"""
```

**Step 8: 验证目录结构**

Run: `find backend -type f -name "*.py" | sort`
Expected:
```
backend/__init__.py
backend/agent/__init__.py
backend/config/__init__.py
backend/llm/__init__.py
backend/tests/__init__.py
backend/utils/__init__.py
```

**Step 9: Commit**

```bash
git add backend/ outputs/
git commit -m "chore: 创建 backend 目录结构"
```

---

## Task 3: 安装依赖

**Files:**
- Modify: `.venv/` (虚拟环境)

**Step 1: 使用 uv 安装依赖**

Run: `uv sync --all-extras`
Expected: 依赖安装成功，无报错

**Step 2: 验证安装**

Run: `uv run python -c "import browser_use; import dashscope; print('依赖安装成功')"`
Expected: 输出 "依赖安装成功"

**Step 3: 安装 Playwright 浏览器**

Run: `uv run playwright install chromium`
Expected: Chromium 浏览器下载安装成功

**Step 4: 验证 Playwright 安装**

Run: `uv run playwright --version`
Expected: 显示 Playwright 版本号

---

## Task 4: 配置环境变量

**Files:**
- Create: `.env.example`
- Create: `.env` (用户手动配置)

**Step 1: 创建 .env.example 模板**

```bash
# 通义千问 API
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# 可选：智谱 GLM（备选）
ZHIPU_API_KEY=your_zhipu_api_key_here

# 可选：DeepSeek（备选）
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 模型选择（默认 qwen）
LLM_PROVIDER=qwen

# 测试目标配置
TEST_BASE_URL=https://your-test-system.com
```

**Step 2: 复制模板创建 .env（提醒用户填入真实 API Key）**

Run: `cp .env.example .env`
Expected: .env 文件创建成功

**Step 3: Commit .env.example**

```bash
git add .env.example
git commit -m "chore: 添加环境变量模板"
```

**注意:** `.env` 文件已在 `.gitignore` 中，不会被提交

---

## Task 5: 创建 Playwright 验证脚本

**Files:**
- Create: `backend/tests/verify_playwright.py`

**Step 1: 创建验证脚本**

```python
"""验证 Playwright 基础功能"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from playwright.async_api import async_playwright


async def verify_playwright() -> bool:
    """验证 Playwright 能正常启动浏览器并截图"""
    print("正在验证 Playwright...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 访问百度首页
        await page.goto("https://www.baidu.com", timeout=30000)
        title = await page.title()

        print(f"✅ Playwright 正常工作")
        print(f"   页面标题: {title}")

        await browser.close()
        return True


if __name__ == "__main__":
    try:
        result = asyncio.run(verify_playwright())
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"❌ Playwright 验证失败: {e}")
        sys.exit(1)
```

**Step 2: 运行验证脚本**

Run: `uv run python backend/tests/verify_playwright.py`
Expected: 输出 "✅ Playwright 正常工作"

**Step 3: Commit**

```bash
git add backend/tests/verify_playwright.py
git commit -m "feat: 添加 Playwright 验证脚本"
```

---

## Task 6: 创建通义千问验证脚本

**Files:**
- Create: `backend/tests/verify_qwen.py`

**Step 1: 创建验证脚本**

```python
"""验证通义千问 API 连接"""
import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv()


def verify_qwen() -> bool:
    """验证通义千问 API 能正常调用"""
    print("正在验证通义千问 API...")

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key or api_key == "your_dashscope_api_key_here":
        print("❌ 未配置 DASHSCOPE_API_KEY")
        print("   请在 .env 文件中设置有效的 API Key")
        return False

    try:
        import dashscope
        from dashscope import Generation

        dashscope.api_key = api_key

        response = Generation.call(
            model="qwen-plus",
            prompt="你好，请回复'OK'",
            max_tokens=10,
        )

        if response.status_code == 200:
            print("✅ 通义千问 API 正常")
            print(f"   响应: {response.output.text.strip()}")
            return True
        else:
            print(f"❌ API 调用失败")
            print(f"   状态码: {response.status_code}")
            print(f"   错误信息: {response.message}")
            return False

    except Exception as e:
        print(f"❌ 通义千问验证失败: {e}")
        return False


if __name__ == "__main__":
    result = verify_qwen()
    sys.exit(0 if result else 1)
```

**Step 2: 运行验证脚本**

Run: `uv run python backend/tests/verify_qwen.py`
Expected: 输出 "✅ 通义千问 API 正常"

**注意:** 确保 `.env` 文件中已配置有效的 `DASHSCOPE_API_KEY`

**Step 3: Commit**

```bash
git add backend/tests/verify_qwen.py
git commit -m "feat: 添加通义千问验证脚本"
```

---

## Task 7: 创建综合验证脚本

**Files:**
- Create: `backend/tests/verify_all.py`

**Step 1: 创建综合验证脚本**

```python
"""综合验证脚本 - 验证所有环境配置"""
import subprocess
import sys
from pathlib import Path


def run_script(script_path: str) -> bool:
    """运行验证脚本并返回结果"""
    result = subprocess.run(
        ["uv", "run", "python", script_path],
        capture_output=False,
    )
    return result.returncode == 0


def main():
    """运行所有验证"""
    print("=" * 50)
    print("Phase 1 环境验证")
    print("=" * 50)
    print()

    tests = [
        ("Playwright", "backend/tests/verify_playwright.py"),
        ("通义千问 API", "backend/tests/verify_qwen.py"),
    ]

    results = {}
    for name, script in tests:
        print(f"\n>>> 验证 {name}")
        print("-" * 40)
        results[name] = run_script(script)
        print()

    # 汇总结果
    print("=" * 50)
    print("验证结果汇总")
    print("=" * 50)
    for name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {name}: {status}")

    all_passed = all(results.values())
    print()
    if all_passed:
        print("🎉 Phase 1 环境搭建完成！")
        return 0
    else:
        print("⚠️  部分验证失败，请检查配置")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

**Step 2: 运行综合验证**

Run: `uv run python backend/tests/verify_all.py`
Expected: 所有验证通过，输出 "🎉 Phase 1 环境搭建完成！"

**Step 3: Commit**

```bash
git add backend/tests/verify_all.py
git commit -m "feat: 添加综合验证脚本"
```

---

## Task 8: 更新主计划文档

**Files:**
- Modify: `docs/1_后端主计划.md`

**Step 1: 更新 Phase 1 任务状态**

将以下内容：
```markdown
### Phase 1: 环境搭建（1-2 天）

- [ ] 1.1 初始化项目结构
- [ ] 1.2 安装 Browser-Use 及依赖
- [ ] 1.3 配置国内模型 API Key
- [ ] 1.4 验证 Playwright 基础功能
```

修改为：
```markdown
### Phase 1: 环境搭建（1-2 天）

- [x] 1.1 初始化项目结构
- [x] 1.2 安装 Browser-Use 及依赖
- [x] 1.3 配置国内模型 API Key
- [x] 1.4 验证 Playwright 基础功能
```

**Step 2: 更新里程碑状态**

将：
```markdown
- [ ] M1: 环境就绪 - Browser-Use + 国内模型 API 调通
```

修改为：
```markdown
- [x] M1: 环境就绪 - Browser-Use + 国内模型 API 调通
```

**Step 3: Commit**

```bash
git add docs/1_后端主计划.md
git commit -m "docs: 更新 Phase 1 完成状态"
```

---

## 验收清单

| 任务 | 验收命令 | 预期结果 |
|------|----------|----------|
| 项目配置 | `ls pyproject.toml .python-version .gitignore` | 三个文件存在 |
| 目录结构 | `find backend -type f -name "*.py"` | 6 个 `__init__.py` 文件 |
| 依赖安装 | `uv run python -c "import browser_use; import dashscope"` | 无报错 |
| Playwright | `uv run python backend/tests/verify_playwright.py` | ✅ Playwright 正常工作 |
| 通义千问 | `uv run python backend/tests/verify_qwen.py` | ✅ 通义千问 API 正常 |
| 综合验证 | `uv run python backend/tests/verify_all.py` | 🎉 Phase 1 环境搭建完成！ |

---

## 完成标志

Phase 1 完成后，项目应达到 **M1: 环境就绪** 里程碑：
- ✅ Browser-Use 依赖安装成功
- ✅ 通义千问 API 可正常调用
- ✅ Playwright 浏览器可正常启动
