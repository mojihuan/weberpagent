# 多模型配置实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为不同 Agent 模块配置不同的大模型，实现成本优化和性能提升。

**Architecture:** 使用 YAML 配置文件 + 工厂模式。配置文件集中管理模型映射，工厂类根据模块名称创建对应的 LLM 实例。

**Tech Stack:** Python 3.11, PyYAML, Pydantic, dashscope SDK

---

## Task 1: 创建配置文件和配置加载类

**Files:**
- Create: `config/llm_config.yaml`
- Create: `backend/llm/config.py`
- Create: `backend/tests/test_llm_config.py`

**Step 1: 创建配置文件**

```yaml
# config/llm_config.yaml
#多模型配置 - 为不同模块指定不同的大模型

llm:
  # API 配置（使用百炼按量付费）
  api_key: ${DASHSCOPE_API_KEY}
  base_url: https://dashscope.aliyuncs.com/compatible-mode/v1

  # 默认模型
  default_model: glm-5

  # 模块专属模型配置
  agents:
    simple_agent:
      reflect: glm-5# 反思模块
    decision:
      model: qwen3.5-plus  # 决策模块（需要视觉能力）
    form_filler:
      code_generator: glm-5  # 代码生成
      code_optimizer: glm-5  # 代码优化
      code_reviewer: qwen3-coder-next  # 代码审查（LLM 语义审查）
```

**Step 2: 创建配置加载类**

```python
# backend/llm/config.py
"""LLM 配置加载模块"""

import os
import re
from pathlib import Path
from typing import Any

import yaml


class LLMConfig:
    """LLM 配置加载类

    从 YAML 文件加载配置，支持环境变量替换
    """

    _instance: "LLMConfig | None" = None
    _config_path: Path = Path("config/llm_config.yaml")

    def __new__(cls) -> "LLMConfig":
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = None
        return cls._instance

    def load(self, config_path: str | Path | None = None) -> dict[str, Any]:
        """加载配置文件

        Args:
            config_path: 配置文件路径，默认为 config/llm_config.yaml

        Returns:
            配置字典
        """
        if config_path:
            self._config_path = Path(config_path)

        if self._config is not None:
            return self._config

        # 查找配置文件（支持相对于项目根目录）
        path = self._find_config_path()

        with open(path, "r", encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)

        # 替换环境变量
        self._config = self._substitute_env_vars(raw_config)
        return self._config

    def _find_config_path(self) -> Path:
        """查找配置文件路径"""
        # 尝试当前目录
        if self._config_path.exists():
            return self._config_path

        # 尝试项目根目录
        project_root = Path(__file__).parent.parent.parent
        candidate = project_root / self._config_path
        if candidate.exists():
            return candidate

        raise FileNotFoundError(f"配置文件未找到: {self._config_path}")

    def _substitute_env_vars(self, obj: Any) -> Any:
        """递归替换环境变量 ${VAR_NAME}"""
        if isinstance(obj, dict):
            return {k: self._substitute_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._substitute_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            # 匹配 ${VAR_NAME} 模式
            pattern = r"\$\{([^}]+)\}"
            def replace(match):
                var_name = match.group(1)
                value = os.getenv(var_name)
                if value is None:
                    raise ValueError(f"环境变量未设置: {var_name}")
                return value
            return re.sub(pattern, replace, obj)
        else:
            return obj

    def get_model(self, module_path: str) -> str:
        """获取模块对应的模型名称

        Args:
            module_path: 模块路径，如 "simple_agent.reflect" 或 "decision"

        Returns:
            模型名称
        """
        config = self.load()

        # 解析模块路径
        parts = module_path.split(".")
        agents_config = config.get("llm", {}).get("agents", {})

        # 逐层查找
        current = agents_config
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                # 未找到，使用默认模型
                return config.get("llm", {}).get("default_model", "glm-5")

        # 如果找到的是字典，取 model 字段或第一个值
        if isinstance(current, dict):
            return current.get("model", config.get("llm", {}).get("default_model", "glm-5"))

        return str(current)

    def get_api_key(self) -> str:
        """获取 API Key"""
        config = self.load()
        api_key = config.get("llm", {}).get("api_key", "")
        if not api_key:
            raise ValueError("API Key 未配置")
        return api_key

    def get_base_url(self) -> str:
        """获取 Base URL"""
        config = self.load()
        return config.get("llm", {}).get("base_url", "")

    @classmethod
    def reset(cls) -> None:
        """重置单例（用于测试）"""
        cls._instance = None


def get_config() -> LLMConfig:
    """获取配置实例"""
    return LLMConfig()
```

**Step 3: 创建测试文件**

```python
# backend/tests/test_llm_config.py
"""LLM 配置加载测试"""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from backend.llm.config import LLMConfig, get_config


@pytest.fixture(autouse=True)
def reset_config():
    """每个测试前重置配置单例"""
    LLMConfig.reset()
    yield
    LLMConfig.reset()


@pytest.fixture
def sample_config(tmp_path: Path) -> Path:
    """创建示例配置文件"""
    config_content = """
llm:
  api_key: test_key_123
  base_url: https://api.example.com/v1
  default_model: glm-5
  agents:
    simple_agent:
      reflect: glm-5
    decision:
      model: qwen3.5-plus
    form_filler:
      code_generator: glm-5
      code_optimizer: glm-5
      code_reviewer: qwen3-coder-next
"""
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(config_content, encoding="utf-8")
    return config_file


class TestLLMConfig:
    """LLMConfig 测试"""

    def test_load_config(self, sample_config: Path):
        """测试加载配置文件"""
        config = get_config()
        result = config.load(sample_config)

        assert "llm" in result
        assert result["llm"]["api_key"] == "test_key_123"
        assert result["llm"]["default_model"] == "glm-5"

    def test_get_model_simple_agent_reflect(self, sample_config: Path):
        """测试获取 simple_agent.reflect 模型"""
        config = get_config()
        config.load(sample_config)

        model = config.get_model("simple_agent.reflect")
        assert model == "glm-5"

    def test_get_model_decision(self, sample_config: Path):
        """测试获取 decision 模型"""
        config = get_config()
        config.load(sample_config)

        model = config.get_model("decision")
        assert model == "qwen3.5-plus"

    def test_get_model_code_reviewer(self, sample_config: Path):
        """测试获取 code_reviewer 模型"""
        config = get_config()
        config.load(sample_config)

        model = config.get_model("form_filler.code_reviewer")
        assert model == "qwen3-coder-next"

    def test_get_model_unknown_returns_default(self, sample_config: Path):
        """测试未知模块返回默认模型"""
        config = get_config()
        config.load(sample_config)

        model = config.get_model("unknown.module")
        assert model == "glm-5"

    def test_get_api_key(self, sample_config: Path):
        """测试获取 API Key"""
        config = get_config()
        config.load(sample_config)

        api_key = config.get_api_key()
        assert api_key == "test_key_123"

    def test_get_base_url(self, sample_config: Path):
        """测试获取 Base URL"""
        config = get_config()
        config.load(sample_config)

        base_url = config.get_base_url()
        assert base_url == "https://api.example.com/v1"

    def test_env_var_substitution(self, tmp_path: Path, monkeypatch):
        """测试环境变量替换"""
        monkeypatch.setenv("TEST_API_KEY", "env_key_456")

        config_content = """
llm:
  api_key: ${TEST_API_KEY}
  default_model: glm-5
"""
        config_file = tmp_path / "env_config.yaml"
        config_file.write_text(config_content, encoding="utf-8")

        config = get_config()
        result = config.load(config_file)

        assert result["llm"]["api_key"] == "env_key_456"

    def test_singleton_pattern(self, sample_config: Path):
        """测试单例模式"""
        config1 = get_config()
        config2 = get_config()

        assert config1 is config2
```

**Step 4: 运行测试验证**

Run: `pytest backend/tests/test_llm_config.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add config/llm_config.yaml backend/llm/config.py backend/tests/test_llm_config.py
git commit -m "feat: add LLM config loader with YAML support"
```

---

## Task 2: 创建 LLM 工厂类

**Files:**
- Create: `backend/llm/factory.py`
- Create: `backend/tests/test_llm_factory.py`

**Step 1: 创建 LLM 工厂类**

```python
# backend/llm/factory.py
"""LLM 实例工厂 - 根据模块名称创建对应的 LLM 实例"""

import logging
from typing import Type

from .base import BaseLLM
from .config import LLMConfig, get_config
from .qwen import QwenChat

logger = logging.getLogger(__name__)


class LLMFactory:
    """LLM 实例工厂

    根据模块名称从配置中获取对应的模型，创建 LLM 实例
    使用缓存避免重复创建
    """

    _instances: dict[str, BaseLLM] = {}
    _llm_class: Type[BaseLLM] = QwenChat

    @classmethod
    def set_llm_class(cls, llm_class: Type[BaseLLM]) -> None:
        """设置 LLM 类（用于测试或切换实现）"""
        cls._llm_class = llm_class

    @classmethod
    def create(cls, module_path: str) -> BaseLLM:
        """创建或获取 LLM 实例

        Args:
            module_path: 模块路径，如 "simple_agent.reflect" 或 "decision"

        Returns:
            LLM 实例
        """
        config = get_config()
        model = config.get_model(module_path)

        # 使用 model 作为缓存 key（同模型共享实例）
        cache_key = f"{cls._llm_class.__name__}:{model}"

        if cache_key not in cls._instances:
            logger.info(f"创建 LLM 实例: model={model}, module={module_path}")
            api_key = config.get_api_key()
            cls._instances[cache_key] = cls._llm_class(
                model=model,
                api_key=api_key,
            )
        else:
            logger.debug(f"复用 LLM 实例: model={model}")

        return cls._instances[cache_key]

    @classmethod
    def get_reflect_llm(cls) -> BaseLLM:
        """获取反思模块 LLM"""
        return cls.create("simple_agent.reflect")

    @classmethod
    def get_decision_llm(cls) -> BaseLLM:
        """获取决策模块 LLM"""
        return cls.create("decision")

    @classmethod
    def get_code_generator_llm(cls) -> BaseLLM:
        """获取代码生成模块 LLM"""
        return cls.create("form_filler.code_generator")

    @classmethod
    def get_code_optimizer_llm(cls) -> BaseLLM:
        """获取代码优化模块 LLM"""
        return cls.create("form_filler.code_optimizer")

    @classmethod
    def get_code_reviewer_llm(cls) -> BaseLLM:
        """获取代码审查模块 LLM"""
        return cls.create("form_filler.code_reviewer")

    @classmethod
    def clear_cache(cls) -> None:
        """清除缓存（用于测试）"""
        cls._instances.clear()


def get_llm(module_path: str) -> BaseLLM:
    """便捷函数：获取指定模块的 LLM 实例"""
    return LLMFactory.create(module_path)
```

**Step 2: 更新 __init__.py 导出**

```python
# backend/llm/__init__.py
"""LLM 模块 - 多模型适配层"""

from .base import BaseLLM, LLMResponse, ActionResult
from .qwen import QwenChat
from .deepseek import DeepSeekChat
from .azure_openai import AzureOpenAIChat
from .browser_use_adapter import BrowserUseAdapter
from .config import LLMConfig, get_config
from .factory import LLMFactory, get_llm

__all__ = [
    "BaseLLM",
    "LLMResponse",
    "ActionResult",
    "QwenChat",
    "DeepSeekChat",
    "AzureOpenAIChat",
    "BrowserUseAdapter",
    "LLMConfig",
    "get_config",
    "LLMFactory",
    "get_llm",
]


def get_default_llm() -> BaseLLM:
    """获取默认的 LLM 实例"""
    return LLMFactory.get_decision_llm()
```

**Step 3: 创建工厂测试**

```python
# backend/tests/test_llm_factory.py
"""LLM 工厂测试"""

import pytest

from backend.llm.config import LLMConfig
from backend.llm.factory import LLMFactory, get_llm
from backend.llm.base import BaseLLM


@pytest.fixture(autouse=True)
def reset():
    """每个测试前重置"""
    LLMConfig.reset()
    LLMFactory.clear_cache()
    yield
    LLMConfig.reset()
    LLMFactory.clear_cache()


@pytest.fixture
def mock_config(tmp_path, monkeypatch):
    """创建模拟配置"""
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test_key")

    config_content = """
llm:
  api_key: ${DASHSCOPE_API_KEY}
  default_model: glm-5
  agents:
    simple_agent:
      reflect: glm-5
    decision:
      model: qwen3.5-plus
    form_filler:
      code_generator: glm-5
      code_reviewer: qwen3-coder-next
"""
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content, encoding="utf-8")

    config = LLMConfig()
    config.load(config_file)
    return config


class TestLLMFactory:
    """LLMFactory 测试"""

    def test_create_returns_llm_instance(self, mock_config):
        """测试 create 返回 LLM 实例"""
        llm = LLMFactory.create("decision")
        assert isinstance(llm, BaseLLM)

    def test_create_uses_correct_model(self, mock_config):
        """测试使用正确的模型"""
        llm = LLMFactory.create("decision")
        assert llm.model_name == "qwen3.5-plus"

        llm2 = LLMFactory.create("form_filler.code_reviewer")
        assert llm2.model_name == "qwen3-coder-next"

    def test_same_model_shares_instance(self, mock_config):
        """测试相同模型共享实例"""
        llm1 = LLMFactory.create("simple_agent.reflect")
        llm2 = LLMFactory.create("form_filler.code_generator")

        # 两者都使用 glm-5，应该共享实例
        assert llm1 is llm2

    def test_different_model_creates_new_instance(self, mock_config):
        """测试不同模型创建新实例"""
        llm1 = LLMFactory.create("decision")
        llm2 = LLMFactory.create("form_filler.code_reviewer")

        # qwen3.5-plus vs qwen3-coder-next，应该是不同实例
        assert llm1 is not llm2

    def test_convenience_methods(self, mock_config):
        """测试便捷方法"""
        reflect_llm = LLMFactory.get_reflect_llm()
        assert reflect_llm.model_name == "glm-5"

        decision_llm = LLMFactory.get_decision_llm()
        assert decision_llm.model_name == "qwen3.5-plus"

        reviewer_llm = LLMFactory.get_code_reviewer_llm()
        assert reviewer_llm.model_name == "qwen3-coder-next"

    def test_get_llm_function(self, mock_config):
        """测试 get_llm 便捷函数"""
        llm = get_llm("decision")
        assert llm.model_name == "qwen3.5-plus"
```

**Step 4: 运行测试验证**

Run: `pytest backend/tests/test_llm_factory.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add backend/llm/factory.py backend/llm/__init__.py backend/tests/test_llm_factory.py
git commit -m "feat: add LLMFactory for multi-model instantiation"
```

---

## Task 3: 改造 CodeReviewer 增加 LLM 审查

**Files:**
- Modify: `backend/agent_simple/form_filler/code_reviewer.py`
- Modify: `backend/tests/test_code_reviewer.py`

**Step 1: 改造 CodeReviewer 类**

```python
# backend/agent_simple/form_filler/code_reviewer.py
"""代码审查 Agent - 规则检查 + LLM 语义审查"""

import ast
import json
import logging
import re
from backend.llm.base import BaseLLM
from backend.agent_simple.types import InteractiveElement
from backend.agent_simple.form_filler.types import ReviewResult, ReviewIssue
from backend.agent_simple.form_filler.prompts import build_code_reviewer_prompt

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
    """代码审查 Agent - 规则检查 + LLM 语义审查"""

    def __init__(self, llm: BaseLLM | None = None):
        """初始化代码审查器

        Args:
            llm: LLM 实例（可选，用于语义审查）
        """
        self.llm = llm

    def review(self, code: str, elements: list[InteractiveElement]) -> ReviewResult:
        """审查代码（规则检查 + LLM 语义审查）

        Args:
            code: 待审查的代码
            elements: 页面可交互元素列表

        Returns:
            ReviewResult: 审查结果
        """
        issues: list[ReviewIssue] = []
        suggestions: list[str] = []

        # 阶段1: 规则检查
        rule_issues, rule_suggestions = self._rule_based_review(code, elements)
        issues.extend(rule_issues)
        suggestions.extend(rule_suggestions)

        # 阶段2: LLM 语义审查（如果配置了 LLM）
        if self.llm:
            llm_issues, llm_suggestions = self._llm_review(code, elements)
            issues.extend(llm_issues)
            suggestions.extend(llm_suggestions)

        # 确定是否通过
        has_critical = any(i.severity == "CRITICAL" for i in issues)
        has_high = any(i.severity == "HIGH" for i in issues)
        approved = not has_critical and not has_high

        return ReviewResult(approved=approved, issues=issues, suggestions=suggestions)

    def _rule_based_review(
        self,
        code: str,
        elements: list[InteractiveElement]
    ) -> tuple[list[ReviewIssue], list[str]]:
        """基于规则的代码审查"""
        issues = []
        suggestions = []

        # 1. 安全性检查
        issues.extend(self._check_security(code))

        # 2. 语法检查
        issues.extend(self._check_syntax(code))

        # 3. 选择器有效性检查
        selector_issues, selector_suggestions = self._check_selectors(code, elements)
        issues.extend(selector_issues)
        suggestions.extend(selector_suggestions)

        # 4. 逻辑完整性检查
        coverage_issues, coverage_suggestions = self._check_coverage(code, elements)
        issues.extend(coverage_issues)
        suggestions.extend(coverage_suggestions)

        return issues, suggestions

    def _llm_review(
        self,
        code: str,
        elements: list[InteractiveElement]
    ) -> tuple[list[ReviewIssue], list[str]]:
        """LLM 语义审查"""
        issues = []
        suggestions = []

        try:
            messages = build_code_reviewer_prompt(code, elements)
            response = self.llm.chat_with_vision(messages=messages, images=[])

            # 解析 LLM 响应
            llm_result = self._parse_llm_response(response.content)

            if llm_result:
                issues.extend(llm_result.get("issues", []))
                suggestions.extend(llm_result.get("suggestions", []))

        except Exception as e:
            logger.warning(f"LLM 审查失败: {e}")
            # LLM 失败不影响规则检查结果

        return issues, suggestions

    def _parse_llm_response(self, response: str) -> dict | None:
        """解析 LLM 响应"""
        try:
            # 尝试提取 JSON
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                data = json.loads(response[json_start:json_end])

                issues = []
                for item in data.get("issues", []):
                    issues.append(ReviewIssue(
                        severity=item.get("severity", "MEDIUM"),
                        line=item.get("line"),
                        message=item.get("message", ""),
                    ))

                return {
                    "issues": issues,
                    "suggestions": data.get("suggestions", []),
                }
        except json.JSONDecodeError as e:
            logger.warning(f"LLM 响应解析失败: {e}")

        return None

    def _check_security(self, code: str) -> list[ReviewIssue]:
        """检查代码安全性"""
        issues = []
        for dangerous in DANGEROUS_IMPORTS:
            pattern = rf"^\s*(import\s+{dangerous}|from\s+{dangerous}\s+import)"
            if re.search(pattern, code, re.MULTILINE):
                issues.append(ReviewIssue(
                    severity="CRITICAL",
                    line=None,
                    message=f"检测到危险导入: {dangerous}",
                ))
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
        elements: list[InteractiveElement]
    ) -> tuple[list[ReviewIssue], list[str]]:
        """检查选择器有效性"""
        issues = []
        suggestions = []

        # 收集有效属性
        valid_placeholders = {el.placeholder for el in elements if el.placeholder}
        valid_texts = {el.text for el in elements if el.text}

        # 检查 placeholder 选择器
        placeholder_pattern = r'get_by_placeholder\(["\']([^"\']+)["\']\)'
        for match in re.finditer(placeholder_pattern, code):
            value = match.group(1)
            if value not in valid_placeholders:
                suggestions.append(f"placeholder '{value}' 未在元素列表中找到")

        return issues, suggestions

    def _check_coverage(
        self,
        code: str,
        elements: list[InteractiveElement]
    ) -> tuple[list[ReviewIssue], list[str]]:
        """检查字段覆盖完整性"""
        issues = []
        suggestions = []

        input_elements = [
            el for el in elements
            if el.tag in ("INPUT", "SELECT", "TEXTAREA")
        ]
        if not input_elements:
            return issues, suggestions

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
                message=f"字段覆盖率较低: {coverage:.0%}",
            ))

        return issues, suggestions
```

**Step 2: 更新测试文件**

```python
# backend/tests/test_code_reviewer.py
"""代码审查测试"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.agent_simple.form_filler.code_reviewer import CodeReviewer
from backend.agent_simple.form_filler.types import ReviewIssue
from backend.agent_simple.types import InteractiveElement


@pytest.fixture
def elements():
    """测试元素列表"""
    return [
        InteractiveElement(
            index=0, tag="INPUT", type="text",
            id="username", name="username", placeholder="请输入用户名"
        ),
        InteractiveElement(
            index=1, tag="INPUT", type="password",
            id="password", name="password", placeholder="请输入密码"
        ),
        InteractiveElement(
            index=2, tag="BUTTON", type="submit",
            text="登录", id="submit-btn"
        ),
    ]


@pytest.fixture
def mock_llm():
    """模拟 LLM"""
    llm = MagicMock()
    llm.chat_with_vision = AsyncMock()
    return llm


class TestCodeReviewer:
    """CodeReviewer 测试"""

    def test_safe_code_passes(self, elements):
        """测试安全代码通过审查"""
        code = """
async def fill_form(page):
    await page.locator('#username').fill('test')
    await page.locator('#password').fill('pass123')
    await page.locator('#submit-btn').click()
"""
        reviewer = CodeReviewer()
        result = reviewer.review(code, elements)

        assert result.approved is True
        assert len(result.issues) == 0

    def test_dangerous_import_fails(self, elements):
        """测试危险导入导致失败"""
        code = """
import os
async def fill_form(page):
    os.system('rm -rf /')
"""
        reviewer = CodeReviewer()
        result = reviewer.review(code, elements)

        assert result.approved is False
        assert any("危险导入" in i.message for i in result.issues)

    def test_syntax_error_fails(self, elements):
        """测试语法错误导致失败"""
        code = """
async def fill_form(page):
    await page.locator('#username').fill('test'
    # 缺少右括号
"""
        reviewer = CodeReviewer()
        result = reviewer.review(code, elements)

        assert result.approved is False
        assert any("语法错误" in i.message for i in result.issues)

    def test_llm_review_called_when_provided(self, elements, mock_llm):
        """测试 LLM 审查被调用"""
        mock_llm.chat_with_vision.return_value = MagicMock(
            content='{"approved": true, "issues": [], "suggestions": ["建议1"]}'
        )

        code = """
async def fill_form(page):
    await page.locator('#username').fill('test')
"""
        reviewer = CodeReviewer(llm=mock_llm)
        result = reviewer.review(code, elements)

        # LLM 应该被调用
        mock_llm.chat_with_vision.assert_called_once()
        assert "建议1" in result.suggestions

    def test_llm_failure_does_not_crash(self, elements, mock_llm):
        """测试 LLM 失败不会导致崩溃"""
        mock_llm.chat_with_vision.side_effect = Exception("API 错误")

        code = """
async def fill_form(page):
    await page.locator('#username').fill('test')
"""
        reviewer = CodeReviewer(llm=mock_llm)
        # 不应该抛出异常
        result = reviewer.review(code, elements)

        assert result is not None
```

**Step 3: 运行测试验证**

Run: `pytest backend/tests/test_code_reviewer.py -v`
Expected: All tests PASS

**Step 4: Commit**

```bash
git add backend/agent_simple/form_filler/code_reviewer.py backend/tests/test_code_reviewer.py
git commit -m "feat: add LLM semantic review to CodeReviewer"
```

---

## Task 4: 更新 FormFiller 使用多模型

**Files:**
- Modify: `backend/agent_simple/form_filler/orchestrator.py`

**Step 1: 更新 FormFiller 构造函数**

```python
# backend/agent_simple/form_filler/orchestrator.py
"""表单填写编排器 - 协调多 Agent 工作流程"""

import logging

from playwright.async_api import Page

from backend.llm.base import BaseLLM
from backend.llm.factory import LLMFactory
from backend.agent_simple.types import PageState
from backend.agent_simple.form_filler.types import FillResult, ReviewResult, GeneratedCode
from backend.agent_simple.form_filler.code_generator import CodeGenerator
from backend.agent_simple.form_filler.code_reviewer import CodeReviewer
from backend.agent_simple.form_filler.code_optimizer import CodeOptimizer
from backend.agent_simple.form_filler.sandbox import execute_code

logger = logging.getLogger(__name__)


class FormFiller:
    """表单填写编排器 - 协调 CodeGenerator、CodeReviewer、CodeOptimizer"""

    MAX_REVIEW_ROUNDS = 3

    def __init__(
        self,
        page: Page,
        llm: BaseLLM | None = None,
        generator_llm: BaseLLM | None = None,
        optimizer_llm: BaseLLM | None = None,
        reviewer_llm: BaseLLM | None = None,
    ):
        """初始化表单填写器

        Args:
            page: Playwright Page 对象
            llm: 通用 LLM（向后兼容，如果提供则用于生成和优化）
            generator_llm: 代码生成专用 LLM
            optimizer_llm: 代码优化专用 LLM
            reviewer_llm: 代码审查专用 LLM
        """
        self.page = page

        # 确定各模块使用的 LLM
        # 优先级：专用 LLM > 通用 LLM > 工厂创建
        if generator_llm:
            gen_llm = generator_llm
        elif llm:
            gen_llm = llm
        else:
            gen_llm = LLMFactory.get_code_generator_llm()

        if optimizer_llm:
            opt_llm = optimizer_llm
        elif llm:
            opt_llm = llm
        else:
            opt_llm = LLMFactory.get_code_optimizer_llm()

        if reviewer_llm:
            rev_llm = reviewer_llm
        else:
            rev_llm = LLMFactory.get_code_reviewer_llm()

        # 初始化子模块
        self.code_generator = CodeGenerator(gen_llm)
        self.code_reviewer = CodeReviewer(rev_llm)
        self.code_optimizer = CodeOptimizer(opt_llm)

        logger.info(
            f"FormFiller 初始化完成: "
            f"generator={gen_llm.model_name}, "
            f"optimizer={opt_llm.model_name}, "
            f"reviewer={rev_llm.model_name}"
        )

    async def fill_form(self, state: PageState, task: str) -> FillResult:
        """填写表单

        流程：
        1. 生成代码
        2. 审查循环（最多 3 轮）
        3. 执行代码
        4. 返回结果
        """
        logger.info(f"开始表单填写流程，任务: {task[:50]}...")

        # 1. 生成代码
        try:
            generated = await self.code_generator.generate(state, task)
        except Exception as e:
            logger.error(f"代码生成失败: {e}")
            return FillResult(success=False, error=f"代码生成失败: {str(e)}")

        code = generated.code

        # 2. 审查循环
        for round_num in range(self.MAX_REVIEW_ROUNDS):
            review_result = self.code_reviewer.review(code, state.elements)

            if review_result.approved:
                logger.info(f"代码审查通过（第 {round_num + 1} 轮）")
                break

            logger.info(f"代码审查未通过（第 {round_num + 1} 轮），尝试优化...")

            try:
                code = await self.code_optimizer.optimize(
                    code, state.elements, review_result.issues
                )
            except Exception as e:
                logger.error(f"代码优化失败: {e}")

        # 3. 执行代码
        logger.info("=" * 60)
        logger.info("📝 准备执行生成的代码:")
        logger.info("-" * 60)
        for line_num, line in enumerate(code.split('\n'), 1):
            logger.info(f"{line_num:3d} | {line}")
        logger.info("-" * 60)
        logger.info("=" * 60)

        try:
            result = await self._execute_code(code)
            logger.info("✅ 代码执行成功")
            if result.get("stdout"):
                logger.info(f"📤 标准输出:\n{result['stdout']}")
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ 代码执行失败: {error_msg}")

            # 尝试一次优化后重新执行
            logger.info("🔄 尝试优化代码后重新执行...")
            try:
                optimized_code = await self.code_optimizer.optimize(
                    code, state.elements, execution_error=error_msg
                )
                logger.info("📝 优化后的代码:")
                logger.info("-" * 60)
                for line_num, line in enumerate(optimized_code.split('\n'), 1):
                    logger.info(f"{line_num:3d} | {line}")
                logger.info("-" * 60)

                result = await self._execute_code(optimized_code)
                code = optimized_code
                logger.info("✅ 优化后执行成功")
                if result.get("stdout"):
                    logger.info(f"📤 标准输出:\n{result['stdout']}")
            except Exception as retry_error:
                return FillResult(
                    success=False,
                    error=f"执行失败: {error_msg}，重试失败: {str(retry_error)}",
                )

        return FillResult(success=True, code=code)

    async def _execute_code(self, code: str) -> dict:
        """执行代码

        Returns:
            执行结果字典，包含 success, stdout, locals 等
        """
        result = await execute_code(code, {"page": self.page})
        if not result["success"]:
            raise Exception(result.get("error", "未知执行错误"))
        return result
```

**Step 2: 运行现有测试验证兼容性**

Run: `pytest backend/tests/test_orchestrator.py -v`
Expected: All tests PASS

**Step 3: Commit**

```bash
git add backend/agent_simple/form_filler/orchestrator.py
git commit -m "feat: update FormFiller to use multi-model configuration"
```

---

## Task 5: 更新 SimpleAgent 使用多模型

**Files:**
- Modify: `backend/agent_simple/agent.py`

**Step 1: 更新 SimpleAgent 反思模块**

在文件顶部添加导入：

```python
# 在现有导入后添加
from backend.llm.factory import LLMFactory
```

修改 `__init__` 方法，添加反思 LLM：

```python
def __init__(
    self,
    task: str,
    llm: BaseLLM,
    page: Page,
    output_dir: str = "outputs",
    max_steps: int = 20,
    max_retries: int = 3,
    timeout: int = 60000,
    reflect_llm: BaseLLM | None = None,
):
    """初始化 Agent

    Args:
        task: 任务描述
        llm: LLM 实例（用于决策）
        page: Playwright Page 对象
        output_dir: 输出目录（截图、日志等）
        max_steps: 最大执行步数
        max_retries: 单步最大重试次数
        timeout: 操作超时时间（毫秒）
        reflect_llm: 反思专用 LLM（可选，默认从工厂获取）
    """
    self.task = task
    self.llm = llm
    self.page = page
    self.max_steps = max_steps
    self.max_retries = max_retries
    self.timeout = timeout

    # 初始化子模块
    self.perception = Perception(page)
    self.decision = Decision(llm)
    self.executor = Executor(page, llm=llm, timeout=timeout)

    # 反思专用 LLM
    self.reflect_llm = reflect_llm or LLMFactory.get_reflect_llm()

    # 输出目录
    self.output_dir = Path(output_dir)
    self.task_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    self.screenshot_manager = ScreenshotManager(output_dir, self.task_id)

    # 执行历史
    self.history: list[Step] = []

    # 记忆模块
    self.memory = Memory(max_steps=5)

    # 循环检测状态
    self._last_loop_type: str | None = None
```

修改 `_reflect` 方法，使用 `self.reflect_llm`：

```python
async def _reflect(
    self,
    action: Action,
    result: ActionResult,
    state: PageState,
) -> Reflection:
    """反思失败原因并生成修复策略

    Args:
        action: 失败的动作
        result: 执行结果
        state: 页面状态

    Returns:
        Reflection: 反思结果
    """
    # 构建反思 prompt
    elements_text = format_elements_for_prompt(state.elements[:10])
    history_context = self._build_history_context()

    prompt = REFLECTION_PROMPT.format(
        task=self.task,
        history=history_context,
        thought=action.thought,
        action=action.action,
        target=action.target or "无",
        value=action.value or "无",
        error=result.error or "未知错误",
        url=state.url,
        title=state.title,
        elements=elements_text,
    )

    # 调用 LLM 进行反思（使用专用反思 LLM）
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    try:
        # 使用 reflect_llm 而不是 self.llm
        response = await self.reflect_llm.chat_with_vision(
            messages=messages,
            images=[f"data:image/png;base64,{state.screenshot_base64}"],
        )

        # 解析反思结果
        return self._parse_reflection(response.content)

    except Exception as e:
        logger.error(f"反思失败: {e}")
        # 默认重试策略
        return Reflection(
            reason=f"反思调用失败: {e}",
            strategy=ReflectionStrategy.RETRY,
        )
```

**Step 2: 运行现有测试验证兼容性**

Run: `pytest backend/tests/test_agent.py -v`
Expected: All tests PASS

**Step 3: Commit**

```bash
git add backend/agent_simple/agent.py
git commit -m "feat: update SimpleAgent to use dedicated reflect LLM"
```

---

## Task 6: 集成测试和文档更新

**Files:**
- Create: `backend/tests/test_multi_llm_integration.py`
- Modify: `backend/llm/__init__.py`

**Step 1: 创建集成测试**

```python
# backend/tests/test_multi_llm_integration.py
"""多模型配置集成测试"""

import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from backend.llm.config import LLMConfig
from backend.llm.factory import LLMFactory


@pytest.fixture(autouse=True)
def reset():
    """每个测试前重置"""
    LLMConfig.reset()
    LLMFactory.clear_cache()
    yield
    LLMConfig.reset()
    LLMFactory.clear_cache()


@pytest.fixture
def real_config(tmp_path, monkeypatch):
    """创建真实配置"""
    monkeypatch.setenv("DASHSCOPE_API_KEY", "sk-test-key-12345")

    config_content = """
llm:
  api_key: ${DASHSCOPE_API_KEY}
  base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
  default_model: glm-5
  agents:
    simple_agent:
      reflect: glm-5
    decision:
      model: qwen3.5-plus
    form_filler:
      code_generator: glm-5
      code_optimizer: glm-5
      code_reviewer: qwen3-coder-next
"""
    config_file = tmp_path / "llm_config.yaml"
    config_file.write_text(config_content, encoding="utf-8")

    config = LLMConfig()
    config.load(config_file)
    return config


class TestMultiLLMIntegration:
    """多模型集成测试"""

    def test_all_modules_have_correct_models(self, real_config):
        """测试所有模块使用正确的模型"""
        # 反思模块
        reflect_llm = LLMFactory.get_reflect_llm()
        assert reflect_llm.model_name == "glm-5"

        # 决策模块
        decision_llm = LLMFactory.get_decision_llm()
        assert decision_llm.model_name == "qwen3.5-plus"

        # 代码生成
        gen_llm = LLMFactory.get_code_generator_llm()
        assert gen_llm.model_name == "glm-5"

        # 代码优化
        opt_llm = LLMFactory.get_code_optimizer_llm()
        assert opt_llm.model_name == "glm-5"

        # 代码审查
        rev_llm = LLMFactory.get_code_reviewer_llm()
        assert rev_llm.model_name == "qwen3-coder-next"

    def test_same_model_instances_are_shared(self, real_config):
        """测试相同模型的实例被共享"""
        # glm-5 用于反思、生成、优化，应该共享实例
        reflect_llm = LLMFactory.get_reflect_llm()
        gen_llm = LLMFactory.get_code_generator_llm()
        opt_llm = LLMFactory.get_code_optimizer_llm()

        assert reflect_llm is gen_llm
        assert gen_llm is opt_llm

        # qwen3.5-plus 和 qwen3-coder-next 应该是不同实例
        decision_llm = LLMFactory.get_decision_llm()
        rev_llm = LLMFactory.get_code_reviewer_llm()

        assert decision_llm is not rev_llm
        assert decision_llm is not reflect_llm
```

**Step 2: 运行所有测试**

Run: `pytest backend/tests/test_multi_llm_integration.py -v`
Expected: All tests PASS

**Step 3: 运行完整测试套件**

Run: `pytest backend/tests/ -v --ignore=backend/tests/run_*.py`
Expected: All tests PASS

**Step 4: Commit**

```bash
git add backend/tests/test_multi_llm_integration.py
git commit -m "test: add multi-model integration tests"
```

---

## 验证清单

- [ ] 配置文件 `config/llm_config.yaml` 存在且格式正确
- [ ] `LLMConfig` 能正确加载配置并替换环境变量
- [ ] `LLMFactory` 能根据模块路径创建正确的 LLM 实例
- [ ] 相同模型的实例被共享（缓存生效）
- [ ] `CodeReviewer` 新增 LLM 语义审查功能
- [ ] `FormFiller` 使用多模型配置
- [ ] `SimpleAgent` 反思模块使用专用 LLM
- [ ] 所有现有测试通过
- [ ] 新增集成测试通过
