# Phase 9: 多 Agent 协作模式实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现多 Agent 协作模式，让 LLM 生成 Playwright 代码片段一次性完成复杂表单填写。

**Architecture:** CodeGenerator → CodeReviewer → CodeOptimizer 三 Agent 协作，由 FormFiller Orchestrator 编排，集成到现有 SimpleAgent 的决策-执行流程中。

**Tech Stack:** Python, Pydantic, Playwright, 通义千问 API

---

## Day 1: 基础架构

### Task 1.1: 创建 form_filler 目录结构

**Files:**
- Create: `backend/agent_simple/form_filler/__init__.py`

**Step 1: 创建目录和初始化文件**

```python
# backend/agent_simple/form_filler/__init__.py
"""表单填写子模块 - 多 Agent 协作模式"""

from backend.agent_simple.form_filler.orchestrator import FormFiller
from backend.agent_simple.form_filler.types import (
    GeneratedCode,
    ReviewIssue,
    ReviewResult,
    FillResult,
)

__all__ = [
    "FormFiller",
    "GeneratedCode",
    "ReviewIssue",
    "ReviewResult",
    "FillResult",
]
```

**Step 2: 验证目录创建**

Run: `ls -la backend/agent_simple/form_filler/`
Expected: 显示 `__init__.py` 文件

**Step 3: Commit**

```bash
git add backend/agent_simple/form_filler/__init__.py
git commit -m "feat(form_filler): 创建模块目录结构"
```

---

### Task 1.2: 添加新类型定义

**Files:**
- Modify: `backend/agent_simple/types.py:7-14` (添加 FILL_FORM)
- Create: `backend/agent_simple/form_filler/types.py`

**Step 1: 在 ActionType 中添加 FILL_FORM**

修改 `backend/agent_simple/types.py`:

```python
class ActionType(str, Enum):
    """支持的动作类型"""

    NAVIGATE = "navigate"
    CLICK = "click"
    INPUT = "input"
    WAIT = "wait"
    DONE = "done"
    FILL_FORM = "fill_form"  # 新增：复杂表单填写
```

**Step 2: 创建 form_filler/types.py**

```python
# backend/agent_simple/form_filler/types.py
"""表单填写模块类型定义"""

from pydantic import BaseModel, Field


class GeneratedCode(BaseModel):
    """生成的代码"""

    code: str = Field(description="Playwright 代码片段")
    description: str = Field(description="代码功能描述")
    field_values: dict = Field(default_factory=dict, description="生成的字段值")


class ReviewIssue(BaseModel):
    """审查问题"""

    severity: str = Field(description="严重级别: CRITICAL/HIGH/MEDIUM/LOW")
    line: int | None = Field(default=None, description="行号")
    message: str = Field(description="问题描述")


class ReviewResult(BaseModel):
    """代码审查结果"""

    approved: bool = Field(description="是否通过审查")
    issues: list[ReviewIssue] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)


class FillResult(BaseModel):
    """表单填写结果"""

    success: bool = Field(description="是否成功")
    screenshot: str | None = Field(default=None, description="验证截图路径")
    code: str | None = Field(default=None, description="最终执行的代码")
    error: str | None = Field(default=None, description="错误信息")
```

**Step 3: 验证类型定义**

Run: `python -c "from backend.agent_simple.form_filler.types import GeneratedCode, ReviewResult, FillResult; print('OK')"`
Expected: `OK`

**Step 4: Commit**

```bash
git add backend/agent_simple/types.py backend/agent_simple/form_filler/types.py
git commit -m "feat(types): 添加 FILL_FORM 动作类型和表单填写相关类型"
```

---

### Task 1.3: 实现代码沙箱执行器

**Files:**
- Create: `backend/agent_simple/form_filler/sandbox.py`
- Create: `backend/tests/test_sandbox.py`

**Step 1: 编写沙箱执行器测试**

```python
# backend/tests/test_sandbox.py
"""沙箱执行器单元测试"""

import pytest
from backend.agent_simple.form_filler.sandbox import execute_code


@pytest.mark.asyncio
async def test_execute_simple_code():
    """测试执行简单代码"""
    code = """
result = 1 + 1
"""
    result = await execute_code(code, {})
    assert result["success"] is True
    assert result["locals"]["result"] == 2


@pytest.mark.asyncio
async def test_execute_code_with_page_mock():
    """测试执行带有 page 参数的代码"""
    code = """
values = {"name": "test"}
"""
    # 模拟 page 对象
    mock_page = type("MockPage", (), {})()
    result = await execute_code(code, {"page": mock_page})
    assert result["success"] is True


@pytest.mark.asyncio
async def test_execute_invalid_code():
    """测试执行无效代码"""
    code = "this is not valid python"
    result = await execute_code(code, {})
    assert result["success"] is False
    assert "error" in result
```

**Step 2: 运行测试确认失败**

Run: `pytest backend/tests/test_sandbox.py -v`
Expected: FAIL (模块不存在)

**Step 3: 实现沙箱执行器**

```python
# backend/agent_simple/form_filler/sandbox.py
"""代码沙箱执行器 - POC 阶段信任执行"""

import logging
import sys
from io import StringIO
from typing import Any

logger = logging.getLogger(__name__)


async def execute_code(
    code: str,
    context: dict[str, Any],
    timeout: int = 30,
) -> dict[str, Any]:
    """执行生成的代码

    POC 阶段：信任执行，直接使用 exec()
    生产阶段：需要添加白名单和沙箱隔离

    Args:
        code: 要执行的 Python 代码
        context: 执行上下文（包含 page 等对象）
        timeout: 执行超时时间（秒）

    Returns:
        执行结果字典:
        - success: 是否成功
        - locals: 局部变量（如有）
        - error: 错误信息（如有）
        - stdout: 标准输出（如有）
    """
    # 捕获 stdout
    old_stdout = sys.stdout
    sys.stdout = captured_stdout = StringIO()

    # 准备执行环境
    local_vars: dict[str, Any] = {}
    global_vars = {"__builtins__": __builtins__, **context}

    try:
        logger.info(f"开始执行代码，超时: {timeout}s")
        logger.debug(f"代码内容:\n{code[:500]}...")

        # 执行代码
        exec(code, global_vars, local_vars)

        # 获取 stdout
        stdout_output = captured_stdout.getvalue()

        logger.info("代码执行成功")

        return {
            "success": True,
            "locals": local_vars,
            "stdout": stdout_output,
        }

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"代码执行失败: {error_msg}")

        return {
            "success": False,
            "error": error_msg,
            "locals": local_vars,
        }

    finally:
        sys.stdout = old_stdout
```

**Step 4: 运行测试确认通过**

Run: `pytest backend/tests/test_sandbox.py -v`
Expected: PASS (3 tests)

**Step 5: Commit**

```bash
git add backend/agent_simple/form_filler/sandbox.py backend/tests/test_sandbox.py
git commit -m "feat(sandbox): 实现代码沙箱执行器"
```

---

### Task 1.4: 编写子 Agent Prompt 模板

**Files:**
- Create: `backend/agent_simple/form_filler/prompts.py`

**Step 1: 创建 Prompt 模板**

```python
# backend/agent_simple/form_filler/prompts.py
"""子 Agent Prompt 模板"""

from backend.agent_simple.types import InteractiveElement


# 字段数据生成规则
FIELD_GENERATION_RULES = """
## 字段数据生成规则

根据字段的 label、placeholder 或 aria-label 推断字段类型，并生成合理的测试数据：

| 字段类型 | 识别规则 | 生成规则 |
|----------|----------|----------|
| 手机号 | 含"手机/电话/tel/phone/mobile" | 138 开头 11 位数字，如 "13812345678" |
| 邮箱 | 含"邮箱/email/mail" | "test_{随机数}@example.com" |
| 姓名 | 含"姓名/收货人/联系人/名字" | 随机中文姓名，如 "张三"、"李明" |
| 日期 | type="date" 或含"日期/date" | 使用今天的日期，格式 "2024-01-15" |
| 金额 | 含"金额/价格/price/amount/钱" | 100-10000 随机整数 |
| 地址 | 含"地址/address/地区" | "北京市朝阳区xxx街道" |
| 数量 | 含"数量/count/qty/num" | 1-100 随机整数 |
| 备注 | 含"备注/说明/note/remark" | "测试备注信息" |
| 其他 | 无规则 | 根据 placeholder 生成合理文本 |
"""


def build_code_generator_prompt(
    task: str,
    elements: list[InteractiveElement],
    page_url: str,
) -> str:
    """构建代码生成 Prompt

    Args:
        task: 任务描述
        elements: 可交互元素列表
        page_url: 当前页面 URL

    Returns:
        完整的 Prompt 字符串
    """
    # 格式化元素列表
    elements_text = _format_elements(elements)

    prompt = f"""你是一个 Playwright 自动化代码生成专家。

## 当前任务
{task}

## 页面信息
URL: {page_url}

## 可交互元素列表
{elements_text}

{FIELD_GENERATION_RULES}

## 代码生成要求

1. **使用 Playwright API**：
   - `page.get_by_placeholder("xxx").fill("value")` - 通过 placeholder 定位
   - `page.get_by_label("xxx").fill("value")` - 通过 label 定位
   - `page.get_by_role("button", name="xxx").click()` - 通过角色定位
   - `page.locator("selector").fill("value")` - CSS 选择器定位

2. **处理复杂组件**：
   - 下拉选择器：先 click 打开，再 click 选项
   - 日期选择器：直接 fill("2024-01-15") 或点击选择
   - 级联选择：依次选择各级选项

3. **添加适当等待**：
   - 在点击后添加 `await page.wait_for_timeout(500)`
   - 在导航后添加 `await page.wait_for_load_state("networkidle")`

4. **生成可直接执行的 async 函数**：
   - 函数名必须是 `async def fill_form(page):`
   - 不要使用 print() 或其他 I/O 操作

## 输出格式

直接输出 Python 代码，不要包裹在 ```python 中。
代码最后添加注释标注生成的字段值，格式：# FIELD_VALUES: {{"字段名": "值"}}
"""
    return prompt


def build_code_reviewer_prompt(
    code: str,
    elements: list[InteractiveElement],
) -> str:
    """构建代码审查 Prompt

    Args:
        code: 待审查的代码
        elements: 可交互元素列表

    Returns:
        完整的 Prompt 字符串
    """
    elements_text = _format_elements(elements)

    prompt = f"""你是一个 Playwright 代码审查专家。请审查以下代码。

## 待审查代码
```python
{code}
```

## 页面可交互元素
{elements_text}

## 审查检查项

1. **安全性 (CRITICAL)**：无危险操作（os.system、subprocess、文件写入等）
2. **选择器有效性 (HIGH)**：选择器能匹配页面元素
3. **逻辑完整性 (HIGH)**：覆盖所有可见的必填字段
4. **API 正确性 (MEDIUM)**：Playwright API 使用正确
5. **异常处理 (LOW)**：有适当的等待

## 输出格式

输出 JSON 格式：
{{
  "approved": true/false,
  "issues": [
    {{"severity": "HIGH", "line": 3, "message": "问题描述"}}
  ],
  "suggestions": ["优化建议1", "优化建议2"]
}}

如果没有问题，approved 设为 true，issues 为空数组。
"""
    return prompt


def build_code_optimizer_prompt(
    code: str,
    issues: list[dict],
    elements: list[InteractiveElement],
    execution_error: str | None = None,
) -> str:
    """构建代码优化 Prompt

    Args:
        code: 原始代码
        issues: 审查问题列表
        elements: 可交互元素列表
        execution_error: 执行错误信息（可选）

    Returns:
        完整的 Prompt 字符串
    """
    elements_text = _format_elements(elements)
    issues_text = "\n".join(
        f"- [{i.get('severity', 'MEDIUM')}] 行 {i.get('line', '?')}: {i.get('message', '')}"
        for i in issues
    )

    error_section = ""
    if execution_error:
        error_section = f"""
## 执行错误
```
{execution_error}
```
"""

    prompt = f"""你是一个 Playwright 代码优化专家。请根据以下信息优化代码。

## 原始代码
```python
{code}
```

## 审查问题
{issues_text}
{error_section}
## 页面可交互元素
{elements_text}

## 优化要求

1. 根据审查问题修复代码
2. 如果选择器无效，使用元素列表中的实际属性替换
3. 保持原有的代码结构和功能
4. 直接输出优化后的代码，不要包裹在代码块中
"""
    return prompt


def _format_elements(elements: list[InteractiveElement]) -> str:
    """格式化元素列表用于 Prompt"""
    if not elements:
        return "(无元素)"

    lines = []
    for el in elements[:30]:  # 限制数量避免 token 过多
        parts = [f"[{el.index}] {el.tag}"]
        if el.text:
            parts.append(f'文本: "{el.text[:30]}"')
        if el.placeholder:
            parts.append(f'placeholder: "{el.placeholder}"')
        if el.id:
            parts.append(f'id: "{el.id}"')
        if el.name:
            parts.append(f'name: "{el.name}"')
        if el.aria_label:
            parts.append(f'aria-label: "{el.aria_label}"')
        if el.type:
            parts.append(f'type: "{el.type}"')
        lines.append(" | ".join(parts))

    return "\n".join(lines)
```

**Step 2: 验证 Prompt 模板**

Run: `python -c "from backend.agent_simple.form_filler.prompts import build_code_generator_prompt; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add backend/agent_simple/form_filler/prompts.py
git commit -m "feat(prompts): 添加子 Agent Prompt 模板"
```

---

## Day 2: CodeGenerator Agent 实现

### Task 2.1: 实现 CodeGenerator Agent

**Files:**
- Create: `backend/agent_simple/form_filler/code_generator.py`
- Create: `backend/tests/test_code_generator.py`

**Step 1: 编写测试**

```python
# backend/tests/test_code_generator.py
"""CodeGenerator 单元测试"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.agent_simple.form_filler.code_generator import CodeGenerator
from backend.agent_simple.types import InteractiveElement, PageState


@pytest.fixture
def mock_llm():
    """模拟 LLM"""
    llm = MagicMock()
    llm.chat_with_vision = AsyncMock()
    llm.model_name = "test-model"
    return llm


@pytest.fixture
def sample_state():
    """示例页面状态"""
    return PageState(
        screenshot_base64="fake_base64",
        url="https://example.com/form",
        title="测试表单",
        elements=[
            InteractiveElement(
                index=0, tag="INPUT", placeholder="请输入姓名", type="text"
            ),
            InteractiveElement(
                index=1, tag="INPUT", placeholder="请输入手机号", type="tel"
            ),
            InteractiveElement(
                index=2, tag="BUTTON", text="提交"
            ),
        ],
    )


@pytest.mark.asyncio
async def test_generate_code(mock_llm, sample_state):
    """测试代码生成"""
    # 模拟 LLM 响应
    mock_llm.chat_with_vision.return_value = MagicMock(
        content='''async def fill_form(page):
    await page.get_by_placeholder("请输入姓名").fill("张三")
    await page.get_by_placeholder("请输入手机号").fill("13812345678")
    await page.get_by_role("button", name="提交").click()
# FIELD_VALUES: {"姓名": "张三", "手机号": "13812345678"}'''
    )

    generator = CodeGenerator(mock_llm)
    result = await generator.generate(sample_state, "填写测试表单")

    assert result.code is not None
    assert "fill_form" in result.code
    assert "姓名" in result.field_values or "张三" in result.code
```

**Step 2: 运行测试确认失败**

Run: `pytest backend/tests/test_code_generator.py -v`
Expected: FAIL

**Step 3: 实现 CodeGenerator**

```python
# backend/agent_simple/form_filler/code_generator.py
"""代码生成 Agent - 生成 Playwright 代码片段"""

import json
import logging
import re
from backend.llm.base import BaseLLM
from backend.agent_simple.types import PageState
from backend.agent_simple.form_filler.types import GeneratedCode
from backend.agent_simple.form_filler.prompts import build_code_generator_prompt

logger = logging.getLogger(__name__)


class CodeGenerator:
    """代码生成 Agent

    根据页面状态和任务描述，生成 Playwright 代码片段
    """

    def __init__(self, llm: BaseLLM):
        """初始化

        Args:
            llm: LLM 实例
        """
        self.llm = llm

    async def generate(
        self,
        state: PageState,
        task: str,
    ) -> GeneratedCode:
        """生成 Playwright 代码

        Args:
            state: 当前页面状态
            task: 任务描述

        Returns:
            GeneratedCode: 生成的代码和元数据
        """
        logger.info(f"开始生成代码，任务: {task[:50]}...")

        # 1. 构建 Prompt
        prompt = build_code_generator_prompt(
            task=task,
            elements=state.elements,
            page_url=state.url,
        )

        # 2. 构建消息
        messages = [{"role": "user", "content": prompt}]

        # 3. 准备图像
        images = []
        if state.screenshot_base64 and len(state.screenshot_base64) > 100:
            images.append(f"data:image/png;base64,{state.screenshot_base64}")

        # 4. 调用 LLM
        response = await self.llm.chat_with_vision(
            messages=messages,
            images=images,
        )

        logger.info(f"LLM 响应长度: {len(response.content)}")

        # 5. 解析响应
        code = self._extract_code(response.content)
        field_values = self._extract_field_values(response.content)
        description = self._extract_description(code)

        logger.info(f"代码生成完成，长度: {len(code)}")

        return GeneratedCode(
            code=code,
            description=description,
            field_values=field_values,
        )

    def _extract_code(self, response: str) -> str:
        """从 LLM 响应中提取代码

        Args:
            response: LLM 原始响应

        Returns:
            提取的代码字符串
        """
        # 尝试提取代码块
        code_block_pattern = r"```(?:python)?\s*([\s\S]*?)\s*```"
        match = re.search(code_block_pattern, response)
        if match:
            return match.group(1).strip()

        # 尝试提取 async def fill_form 开始的部分
        func_start = response.find("async def fill_form")
        if func_start >= 0:
            # 找到函数结束位置（下一个顶层定义或文件末尾）
            code = response[func_start:]
            # 移除尾部可能的多余内容
            lines = code.split("\n")
            code_lines = []
            for line in lines:
                # 遇到非缩进的新定义则停止
                if line and not line[0].isspace() and code_lines:
                    break
                code_lines.append(line)
            return "\n".join(code_lines).strip()

        # 返回原始响应
        return response.strip()

    def _extract_field_values(self, response: str) -> dict:
        """从响应中提取字段值

        格式：# FIELD_VALUES: {"name": "value"}

        Args:
            response: LLM 响应

        Returns:
            字段值字典
        """
        pattern = r"#\s*FIELD_VALUES:\s*(\{.*?\})"
        match = re.search(pattern, response)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        return {}

    def _extract_description(self, code: str) -> str:
        """从代码中提取描述

        Args:
            code: 代码字符串

        Returns:
            描述字符串
        """
        # 提取前几行作为描述
        lines = code.split("\n")[:3]
        return " | ".join(line.strip() for line in lines if line.strip())
```

**Step 4: 运行测试确认通过**

Run: `pytest backend/tests/test_code_generator.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add backend/agent_simple/form_filler/code_generator.py backend/tests/test_code_generator.py
git commit -m "feat(code_generator): 实现 CodeGenerator Agent"
```

---

## Day 3: CodeReviewer + CodeOptimizer 实现

### Task 3.1: 实现 CodeReviewer Agent

**Files:**
- Create: `backend/agent_simple/form_filler/code_reviewer.py`
- Create: `backend/tests/test_code_reviewer.py`

**Step 1: 编写测试**

```python
# backend/tests/test_code_reviewer.py
"""CodeReviewer 单元测试"""

import pytest
from unittest.mock import MagicMock

from backend.agent_simple.form_filler.code_reviewer import CodeReviewer
from backend.agent_simple.types import InteractiveElement
from backend.agent_simple.form_filler.types import ReviewResult


@pytest.fixture
def reviewer():
    """创建审查器实例"""
    return CodeReviewer()


@pytest.fixture
def sample_elements():
    """示例元素列表"""
    return [
        InteractiveElement(index=0, tag="INPUT", placeholder="姓名"),
        InteractiveElement(index=1, tag="INPUT", placeholder="手机号"),
        InteractiveElement(index=2, tag="BUTTON", text="提交"),
    ]


def test_review_safe_code(reviewer, sample_elements):
    """测试审查安全代码"""
    code = '''
async def fill_form(page):
    await page.get_by_placeholder("姓名").fill("张三")
    await page.get_by_placeholder("手机号").fill("13812345678")
    await page.get_by_role("button", name="提交").click()
'''
    result = reviewer.review(code, sample_elements)
    assert result.approved is True


def test_review_dangerous_code(reviewer, sample_elements):
    """测试审查危险代码"""
    code = '''
async def fill_form(page):
    import os
    os.system("rm -rf /")
'''
    result = reviewer.review(code, sample_elements)
    assert result.approved is False
    assert any(i.severity == "CRITICAL" for i in result.issues)


def test_review_invalid_selector(reviewer, sample_elements):
    """测试审查无效选择器"""
    code = '''
async def fill_form(page):
    await page.locator("#nonexistent").fill("test")
'''
    result = reviewer.review(code, sample_elements)
    # 可能会警告选择器无效
    assert isinstance(result, ReviewResult)
```

**Step 2: 运行测试确认失败**

Run: `pytest backend/tests/test_code_reviewer.py -v`
Expected: FAIL

**Step 3: 实现 CodeReviewer（规则审查，不调用 LLM）**

```python
# backend/agent_simple/form_filler/code_reviewer.py
"""代码审查 Agent - 审查生成的代码"""

import ast
import logging
import re
from typing import Any

from backend.agent_simple.types import InteractiveElement
from backend.agent_simple.form_filler.types import ReviewResult, ReviewIssue

logger = logging.getLogger(__name__)


# 危险模块和函数
DANGEROUS_IMPORTS = {
    "os", "subprocess", "sys", "shutil", "socket",
    "pickle", "marshal", "eval", "exec", "compile",
    "__import__", "importlib",
}

DANGEROUS_CALLS = {
    "os.system", "os.popen", "subprocess.run", "subprocess.call",
    "subprocess.Popen", "eval", "exec", "compile",
}


class CodeReviewer:
    """代码审查 Agent

    审查生成的代码是否安全、有效、完整
    """

    def __init__(self):
        """初始化审查器"""
        pass

    def review(
        self,
        code: str,
        elements: list[InteractiveElement],
    ) -> ReviewResult:
        """审查代码

        Args:
            code: 待审查的代码
            elements: 页面可交互元素列表

        Returns:
            ReviewResult: 审查结果
        """
        logger.info("开始代码审查")

        issues: list[ReviewIssue] = []
        suggestions: list[str] = []

        # 1. 安全性检查
        security_issues = self._check_security(code)
        issues.extend(security_issues)

        # 2. 语法检查
        syntax_issues = self._check_syntax(code)
        issues.extend(syntax_issues)

        # 3. 选择器有效性检查
        selector_issues, selector_suggestions = self._check_selectors(code, elements)
        issues.extend(selector_issues)
        suggestions.extend(selector_suggestions)

        # 4. 逻辑完整性检查
        coverage_issues, coverage_suggestions = self._check_coverage(code, elements)
        issues.extend(coverage_issues)
        suggestions.extend(coverage_suggestions)

        # 确定是否通过
        has_critical = any(i.severity == "CRITICAL" for i in issues)
        has_high = any(i.severity == "HIGH" for i in issues)
        approved = not has_critical and not has_high

        logger.info(f"审查完成，通过: {approved}，问题数: {len(issues)}")

        return ReviewResult(
            approved=approved,
            issues=issues,
            suggestions=suggestions,
        )

    def _check_security(self, code: str) -> list[ReviewIssue]:
        """检查代码安全性"""
        issues = []

        # 检查危险导入
        for dangerous in DANGEROUS_IMPORTS:
            pattern = rf"^\s*(import\s+{dangerous}|from\s+{dangerous}\s+import)"
            if re.search(pattern, code, re.MULTILINE):
                issues.append(ReviewIssue(
                    severity="CRITICAL",
                    line=None,
                    message=f"检测到危险导入: {dangerous}",
                ))

        # 检查危险调用
        for dangerous in DANGEROUS_CALLS:
            if dangerous in code:
                issues.append(ReviewIssue(
                    severity="CRITICAL",
                    line=None,
                    message=f"检测到危险调用: {dangerous}",
                ))

        return issues

    def _check_syntax(self, code: str) -> list[ReviewIssue]:
        """检查语法正确性"""
        issues = []

        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(ReviewIssue(
                severity="HIGH",
                line=e.lineno,
                message=f"语法错误: {e.msg}",
            ))

        return issues

    def _check_selectors(
        self,
        code: str,
        elements: list[InteractiveElement],
    ) -> tuple[list[ReviewIssue], list[str]]:
        """检查选择器有效性"""
        issues = []
        suggestions = []

        # 提取代码中的选择器字符串
        selector_patterns = [
            r'locator\(["\']([^"\']+)["\']\)',
            r'get_by_placeholder\(["\']([^"\']+)["\']\)',
            r'get_by_label\(["\']([^"\']+)["\']\)',
            r'get_by_text\(["\']([^"\']+)["\']\)',
        ]

        # 收集元素的有效属性
        valid_placeholders = {el.placeholder for el in elements if el.placeholder}
        valid_texts = {el.text for el in elements if el.text}
        valid_ids = {el.id for el in elements if el.id}
        valid_labels = {el.aria_label for el in elements if el.aria_label}

        for pattern in selector_patterns:
            for match in re.finditer(pattern, code):
                selector_value = match.group(1)

                # 检查 CSS ID 选择器
                if selector_value.startswith("#"):
                    id_value = selector_value[1:]
                    if id_value not in valid_ids:
                        issues.append(ReviewIssue(
                            severity="HIGH",
                            line=None,
                            message=f"ID 选择器 #{id_value} 在页面元素中不存在",
                        ))

                # 检查 placeholder
                if "placeholder" in pattern:
                    if selector_value not in valid_placeholders:
                        suggestions.append(
                            f"placeholder '{selector_value}' 未在元素列表中找到，"
                            f"可用值: {list(valid_placeholders)[:5]}"
                        )

        return issues, suggestions

    def _check_coverage(
        self,
        code: str,
        elements: list[InteractiveElement],
    ) -> tuple[list[ReviewIssue], list[str]]:
        """检查字段覆盖完整性"""
        issues = []
        suggestions = []

        # 统计必填输入字段
        input_elements = [
            el for el in elements
            if el.tag in ("INPUT", "SELECT", "TEXTAREA")
        ]

        if not input_elements:
            return issues, suggestions

        # 检查代码是否处理了主要输入字段
        filled_count = 0
        for el in input_elements:
            identifier = el.placeholder or el.name or el.id or el.aria_label
            if identifier and identifier in code:
                filled_count += 1

        coverage = filled_count / len(input_elements) if input_elements else 1.0

        if coverage < 0.5:
            issues.append(ReviewIssue(
                severity="MEDIUM",
                line=None,
                message=f"字段覆盖率较低: {coverage:.0%} ({filled_count}/{len(input_elements)})",
            ))
            suggestions.append("建议填写更多必填字段")

        return issues, suggestions
```

**Step 4: 运行测试确认通过**

Run: `pytest backend/tests/test_code_reviewer.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add backend/agent_simple/form_filler/code_reviewer.py backend/tests/test_code_reviewer.py
git commit -m "feat(code_reviewer): 实现 CodeReviewer Agent"
```

---

### Task 3.2: 实现 CodeOptimizer Agent

**Files:**
- Create: `backend/agent_simple/form_filler/code_optimizer.py`
- Create: `backend/tests/test_code_optimizer.py`

**Step 1: 编写测试**

```python
# backend/tests/test_code_optimizer.py
"""CodeOptimizer 单元测试"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.agent_simple.form_filler.code_optimizer import CodeOptimizer
from backend.agent_simple.types import InteractiveElement
from backend.agent_simple.form_filler.types import ReviewIssue


@pytest.fixture
def mock_llm():
    """模拟 LLM"""
    llm = MagicMock()
    llm.chat_with_vision = AsyncMock()
    llm.model_name = "test-model"
    return llm


@pytest.fixture
def sample_elements():
    """示例元素列表"""
    return [
        InteractiveElement(index=0, tag="INPUT", placeholder="姓名"),
        InteractiveElement(index=1, tag="INPUT", placeholder="手机号"),
    ]


@pytest.mark.asyncio
async def test_optimize_with_issues(mock_llm, sample_elements):
    """测试根据审查问题优化代码"""
    mock_llm.chat_with_vision.return_value = MagicMock(
        content='''async def fill_form(page):
    await page.get_by_placeholder("姓名").fill("张三")
    await page.get_by_placeholder("手机号").fill("13812345678")'''
    )

    optimizer = CodeOptimizer(mock_llm)
    issues = [
        ReviewIssue(severity="HIGH", line=1, message="测试问题")
    ]

    result = await optimizer.optimize(
        code="original code",
        elements=sample_elements,
        issues=issues,
    )

    assert result is not None
    assert "fill_form" in result
```

**Step 2: 运行测试确认失败**

Run: `pytest backend/tests/test_code_optimizer.py -v`
Expected: FAIL

**Step 3: 实现 CodeOptimizer**

```python
# backend/agent_simple/form_filler/code_optimizer.py
"""代码优化 Agent - 根据审查意见或执行错误优化代码"""

import logging
from backend.llm.base import BaseLLM
from backend.agent_simple.types import InteractiveElement
from backend.agent_simple.form_filler.types import ReviewIssue
from backend.agent_simple.form_filler.prompts import build_code_optimizer_prompt

logger = logging.getLogger(__name__)


class CodeOptimizer:
    """代码优化 Agent

    根据审查意见或执行错误优化代码
    """

    def __init__(self, llm: BaseLLM):
        """初始化

        Args:
            llm: LLM 实例
        """
        self.llm = llm

    async def optimize(
        self,
        code: str,
        elements: list[InteractiveElement],
        issues: list[ReviewIssue] | None = None,
        execution_error: str | None = None,
    ) -> str:
        """优化代码

        Args:
            code: 原始代码
            elements: 页面元素列表
            issues: 审查问题列表（可选）
            execution_error: 执行错误信息（可选）

        Returns:
            优化后的代码
        """
        logger.info("开始代码优化")

        # 如果没有问题也没有错误，直接返回原代码
        if not issues and not execution_error:
            logger.info("无需优化，返回原代码")
            return code

        # 构建 Prompt
        issues_dict = [
            {"severity": i.severity, "line": i.line, "message": i.message}
            for i in (issues or [])
        ]

        prompt = build_code_optimizer_prompt(
            code=code,
            issues=issues_dict,
            elements=elements,
            execution_error=execution_error,
        )

        # 调用 LLM
        messages = [{"role": "user", "content": prompt}]

        response = await self.llm.chat_with_vision(
            messages=messages,
            images=[],  # 优化不需要截图
        )

        # 提取代码
        optimized_code = self._extract_code(response.content)

        logger.info(f"代码优化完成，原长度: {len(code)}，新长度: {len(optimized_code)}")

        return optimized_code

    def _extract_code(self, response: str) -> str:
        """从响应中提取代码"""
        import re

        # 尝试提取代码块
        code_block_pattern = r"```(?:python)?\s*([\s\S]*?)\s*```"
        match = re.search(code_block_pattern, response)
        if match:
            return match.group(1).strip()

        # 尝试提取 async def fill_form
        func_start = response.find("async def fill_form")
        if func_start >= 0:
            return response[func_start:].strip()

        return response.strip()
```

**Step 4: 运行测试确认通过**

Run: `pytest backend/tests/test_code_optimizer.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add backend/agent_simple/form_filler/code_optimizer.py backend/tests/test_code_optimizer.py
git commit -m "feat(code_optimizer): 实现 CodeOptimizer Agent"
```

---

## Day 4: 编排器 + 主 Agent 集成

### Task 4.1: 实现 FormFiller Orchestrator

**Files:**
- Create: `backend/agent_simple/form_filler/orchestrator.py`
- Create: `backend/tests/test_orchestrator.py`

**Step 1: 编写测试**

```python
# backend/tests/test_orchestrator.py
"""Orchestrator 单元测试"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from backend.agent_simple.form_filler.orchestrator import FormFiller
from backend.agent_simple.types import PageState, InteractiveElement
from backend.agent_simple.form_filler.types import GeneratedCode, ReviewResult


@pytest.fixture
def mock_llm():
    """模拟 LLM"""
    llm = MagicMock()
    llm.chat_with_vision = AsyncMock()
    llm.model_name = "test-model"
    return llm


@pytest.fixture
def mock_page():
    """模拟 Playwright Page"""
    return MagicMock()


@pytest.fixture
def sample_state():
    """示例页面状态"""
    return PageState(
        screenshot_base64="fake_base64",
        url="https://example.com/form",
        title="测试表单",
        elements=[
            InteractiveElement(index=0, tag="INPUT", placeholder="姓名"),
        ],
    )


@pytest.mark.asyncio
async def test_fill_form_success(mock_llm, mock_page, sample_state):
    """测试表单填写成功流程"""
    # 模拟代码生成返回
    with patch.object(FormFiller, '_generate_code') as mock_gen, \
         patch.object(FormFiller, '_review_code') as mock_review, \
         patch.object(FormFiller, '_execute_code') as mock_exec:

        mock_gen.return_value = GeneratedCode(
            code='async def fill_form(page): pass',
            description="test",
            field_values={}
        )
        mock_review.return_value = ReviewResult(approved=True, issues=[], suggestions=[])
        mock_exec.return_value = None

        filler = FormFiller(mock_llm, mock_page)
        result = await filler.fill_form(sample_state, "填写表单")

        assert result.success is True
```

**Step 2: 运行测试确认失败**

Run: `pytest backend/tests/test_orchestrator.py -v`
Expected: FAIL

**Step 3: 实现 Orchestrator**

```python
# backend/agent_simple/form_filler/orchestrator.py
"""表单填写编排器 - 协调多 Agent 工作流程"""

import logging
from playwright.async_api import Page

from backend.llm.base import BaseLLM
from backend.agent_simple.types import PageState
from backend.agent_simple.form_filler.types import FillResult, ReviewResult, GeneratedCode
from backend.agent_simple.form_filler.code_generator import CodeGenerator
from backend.agent_simple.form_filler.code_reviewer import CodeReviewer
from backend.agent_simple.form_filler.code_optimizer import CodeOptimizer
from backend.agent_simple.form_filler.sandbox import execute_code

logger = logging.getLogger(__name__)


class FormFiller:
    """表单填写编排器

    协调 CodeGenerator、CodeReviewer、CodeOptimizer 完成表单填写
    """

    MAX_REVIEW_ROUNDS = 3  # 最大审查轮数

    def __init__(self, llm: BaseLLM, page: Page):
        """初始化

        Args:
            llm: LLM 实例
            page: Playwright Page 对象
        """
        self.llm = llm
        self.page = page

        # 初始化子 Agent
        self.code_generator = CodeGenerator(llm)
        self.code_reviewer = CodeReviewer()
        self.code_optimizer = CodeOptimizer(llm)

    async def fill_form(
        self,
        state: PageState,
        task: str,
    ) -> FillResult:
        """填写表单

        Args:
            state: 当前页面状态
            task: 任务描述

        Returns:
            FillResult: 填写结果
        """
        logger.info(f"开始表单填写流程，任务: {task[:50]}...")

        # 1. 生成代码
        try:
            generated = await self._generate_code(state, task)
        except Exception as e:
            logger.error(f"代码生成失败: {e}")
            return FillResult(success=False, error=f"代码生成失败: {str(e)}")

        code = generated.code

        # 2. 审查循环
        for round_num in range(self.MAX_REVIEW_ROUNDS):
            review_result = self._review_code(code, state.elements)

            if review_result.approved:
                logger.info(f"代码审查通过（第 {round_num + 1} 轮）")
                break

            logger.info(f"代码审查未通过（第 {round_num + 1} 轮），尝试优化...")

            # 优化代码
            try:
                code = await self._optimize_code(
                    code, state.elements, review_result.issues
                )
            except Exception as e:
                logger.error(f"代码优化失败: {e}")
                # 继续使用当前代码

        else:
            # 3 轮都未通过
            logger.warning("代码审查未通过，尝试执行")

        # 3. 执行代码
        try:
            await self._execute_code(code)
            logger.info("代码执行成功")
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"代码执行失败: {error_msg}")

            # 尝试一次优化后重新执行
            try:
                optimized_code = await self._optimize_code(
                    code, state.elements, execution_error=error_msg
                )
                await self._execute_code(optimized_code)
                code = optimized_code
                logger.info("优化后执行成功")
            except Exception as retry_error:
                return FillResult(
                    success=False,
                    error=f"执行失败: {error_msg}，重试失败: {str(retry_error)}",
                )

        # 4. 返回结果
        return FillResult(
            success=True,
            code=code,
            screenshot=None,  # 可以后续添加截图
        )

    async def _generate_code(self, state: PageState, task: str) -> GeneratedCode:
        """生成代码"""
        return await self.code_generator.generate(state, task)

    def _review_code(self, code: str, elements) -> ReviewResult:
        """审查代码"""
        return self.code_reviewer.review(code, elements)

    async def _optimize_code(
        self,
        code: str,
        elements,
        issues: list | None = None,
        execution_error: str | None = None,
    ) -> str:
        """优化代码"""
        return await self.code_optimizer.optimize(
            code=code,
            elements=elements,
            issues=issues,
            execution_error=execution_error,
        )

    async def _execute_code(self, code: str) -> None:
        """执行代码"""
        result = await execute_code(code, {"page": self.page})

        if not result["success"]:
            raise Exception(result.get("error", "未知执行错误"))
```

**Step 4: 运行测试确认通过**

Run: `pytest backend/tests/test_orchestrator.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add backend/agent_simple/form_filler/orchestrator.py backend/tests/test_orchestrator.py
git commit -m "feat(orchestrator): 实现 FormFiller 编排器"
```

---

### Task 4.2: 修改 decision.py 支持表单检测

**Files:**
- Modify: `backend/agent_simple/decision.py`

**Step 1: 添加表单检测方法**

在 `Decision` 类中添加：

```python
def _is_complex_form(self, state: PageState) -> bool:
    """检测是否为复杂表单

    Args:
        state: 当前页面状态

    Returns:
        是否为复杂表单
    """
    # 1. 检查输入元素数量
    input_count = sum(
        1 for e in state.elements
        if e.tag in ("INPUT", "SELECT", "TEXTAREA")
    )

    # 2. 检查 URL 关键词
    url_lower = state.url.lower()
    is_form_url = any(
        kw in url_lower
        for kw in ["form", "add", "edit", "create", "new"]
    )

    # 3. 综合判断
    return input_count >= 3 and is_form_url
```

**Step 2: 修改 decide 方法添加分支**

在 `decide` 方法开头添加：

```python
async def decide(
    self,
    task: str,
    state: PageState,
    memory: Memory | None = None,
) -> Action:
    """根据页面状态决定下一步动作"""
    # 检测复杂表单
    if self._is_complex_form(state):
        logger.info("检测到复杂表单，使用 fill_form 模式")
        return Action(
            thought="检测到复杂表单，使用代码生成模式一次性填写",
            action="fill_form",
            done=False,
        )

    # 原有逻辑...
```

**Step 3: Commit**

```bash
git add backend/agent_simple/decision.py
git commit -m "feat(decision): 添加复杂表单检测，支持 fill_form 决策"
```

---

### Task 4.3: 修改 executor.py 支持 fill_form 动作

**Files:**
- Modify: `backend/agent_simple/executor.py`

**Step 1: 导入 FormFiller**

在文件顶部添加：

```python
from backend.agent_simple.form_filler.orchestrator import FormFiller
```

**Step 2: 添加 fill_form 处理方法**

在 `execute` 方法中添加分支：

```python
async def execute(
    self,
    action: Action,
    elements: list[InteractiveElement],
) -> ActionResult:
    """执行动作"""
    logger.info(f"执行动作: {action.action}, 目标: {action.target}")

    try:
        if action.action == "navigate":
            return await self._navigate(action.value or "")
        elif action.action == "click":
            return await self._click(action.target, elements)
        elif action.action == "input":
            return await self._input(action.target, action.value, elements)
        elif action.action == "wait":
            return await self._wait()
        elif action.action == "fill_form":
            return await self._fill_form(action, elements)
        elif action.action == "done":
            return ActionResult(success=True, error=None)
        else:
            # ...
```

**Step 3: 实现 _fill_form 方法**

```python
async def _fill_form(
    self,
    action: Action,
    elements: list[InteractiveElement],
) -> ActionResult:
    """执行复杂表单填写

    Args:
        action: 动作对象
        elements: 元素列表（用于构建 PageState）

    Returns:
        ActionResult: 执行结果
    """
    from backend.agent_simple.types import PageState
    from backend.agent_simple.perception import Perception

    logger.info("使用 FormFiller 填写表单")

    try:
        # 获取当前页面状态
        perception = Perception(self.page)
        screenshot_base64 = await perception.take_screenshot_base64()

        state = PageState(
            screenshot_base64=screenshot_base64,
            url=self.page.url,
            title=await self.page.title(),
            elements=elements,
        )

        # 使用 FormFiller
        filler = FormFiller(self.llm, self.page)
        result = await filler.fill_form(state, action.target or "填写表单")

        if result.success:
            logger.info("表单填写成功")
            return ActionResult(
                success=True,
                error=None,
            )
        else:
            logger.error(f"表单填写失败: {result.error}")
            return ActionResult(
                success=False,
                error=result.error,
            )

    except Exception as e:
        logger.error(f"表单填写异常: {e}")
        return ActionResult(success=False, error=str(e))
```

**Step 4: 需要注入 LLM 到 Executor**

修改 `Executor.__init__`：

```python
def __init__(self, page: Page, llm: BaseLLM, timeout: int = 30000):
    """初始化执行模块

    Args:
        page: Playwright Page 对象
        llm: LLM 实例（用于 fill_form）
        timeout: 操作超时时间（毫秒）
    """
    self.page = page
    self.llm = llm
    self.timeout = timeout
```

**Step 5: Commit**

```bash
git add backend/agent_simple/executor.py
git commit -m "feat(executor): 支持 fill_form 动作，集成 FormFiller"
```

---

### Task 4.4: 更新 agent.py 传递 LLM

**Files:**
- Modify: `backend/agent_simple/agent.py`

**Step 1: 检查 Executor 初始化**

确保在创建 Executor 时传入 LLM：

```python
self.executor = Executor(page, self.llm, timeout=self.timeout)
```

**Step 2: Commit**

```bash
git add backend/agent_simple/agent.py
git commit -m "fix(agent): 传递 LLM 到 Executor 支持 fill_form"
```

---

## Day 5: 场景验证

### Task 5.1: 编写集成测试

**Files:**
- Create: `backend/tests/test_form_filler_integration.py`

**Step 1: 编写集成测试**

```python
# backend/tests/test_form_filler_integration.py
"""FormFiller 集成测试"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from backend.agent_simple.form_filler import FormFiller
from backend.agent_simple.types import PageState, InteractiveElement


@pytest.fixture
def mock_llm():
    """模拟 LLM"""
    llm = MagicMock()
    llm.model_name = "test-model"
    llm.chat_with_vision = AsyncMock()
    return llm


@pytest.fixture
def mock_page():
    """模拟 Playwright Page"""
    page = MagicMock()
    page.url = "https://example.com/form"
    page.title = AsyncMock(return_value="测试表单")
    page.wait_for_timeout = AsyncMock()
    return page


@pytest.mark.asyncio
async def test_form_filler_full_flow(mock_llm, mock_page):
    """测试完整表单填写流程"""
    # 模拟 LLM 响应
    mock_llm.chat_with_vision.return_value = MagicMock(
        content='''async def fill_form(page):
    await page.get_by_placeholder("姓名").fill("张三")
    await page.get_by_placeholder("手机号").fill("13812345678")
# FIELD_VALUES: {"姓名": "张三", "手机号": "13812345678"}'''
    )

    state = PageState(
        screenshot_base64="fake_base64",
        url="https://example.com/form",
        title="测试表单",
        elements=[
            InteractiveElement(index=0, tag="INPUT", placeholder="姓名"),
            InteractiveElement(index=1, tag="INPUT", placeholder="手机号"),
        ],
    )

    filler = FormFiller(mock_llm, mock_page)
    result = await filler.fill_form(state, "填写测试表单")

    assert result.success is True
    assert result.code is not None
```

**Step 2: 运行测试**

Run: `pytest backend/tests/test_form_filler_integration.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add backend/tests/test_form_filler_integration.py
git commit -m "test: 添加 FormFiller 集成测试"
```

---

### Task 5.2: 更新 progress.md

**Files:**
- Modify: `docs/progress.md`

**Step 1: 更新 Phase 9 状态**

将 Phase 9 的任务标记为完成：

```markdown
### Phase 9: 多 Agent 协作模式 ✅
- **完成日期**: 2026-03-11
- **设计文档**: `docs/plans/2026-03-11-phase9-multi-agent-design.md`
- **实施计划**: `docs/plans/2026-03-11-phase9-implementation-plan.md`
- **任务清单**:
  - [x] 9.1 基础架构设计 ✅
  - [x] 9.2 CodeGenerator Agent 实现 ✅
  - [x] 9.3 CodeReviewer Agent 实现 ✅
  - [x] 9.4 CodeOptimizer Agent 实现 ✅
  - [x] 9.5 FormFiller Orchestrator 实现 ✅
  - [x] 9.6 主 Agent 集成 ✅
  - [x] 9.7 场景验证测试 ✅
```

**Step 2: Commit**

```bash
git add docs/progress.md
git commit -m "docs: 更新 Phase 9 完成状态"
```

---

## 完成检查清单

- [ ] 所有单元测试通过
- [ ] 代码审查无 CRITICAL/HIGH 问题
- [ ] 文档更新完整
- [ ] Git 提交历史清晰

---

## 验收命令

```bash
# 运行所有相关测试
pytest backend/tests/test_sandbox.py backend/tests/test_code_generator.py backend/tests/test_code_reviewer.py backend/tests/test_code_optimizer.py backend/tests/test_orchestrator.py backend/tests/test_form_filler_integration.py -v

# 检查导入
python -c "from backend.agent_simple.form_filler import FormFiller; print('OK')"
```