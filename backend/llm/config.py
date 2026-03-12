"""LLM 配置加载器

从 YAML 文件加载多模型配置，支持环境变量替换。
"""

import os
import re
from pathlib import Path
from typing import Any, Optional

import yaml


class LLMConfig:
    """LLM 配置单例类

    从 YAML 文件加载配置，支持环境变量替换。
    提供按模块路径获取模型名称的方法。

    Usage:
        config = LLMConfig.get_instance()
        model = config.get_model("simple_agent.reflect")
        api_key = config.get_api_key()
    """

    _instance: Optional["LLMConfig"] = None
    _config_path: str = "config/llm_config.yaml"

    def __init__(self, config_path: Optional[str] = None):
        """初始化配置

        Args:
            config_path: 配置文件路径，默认为 config/llm_config.yaml
        """
        self._config_path = config_path if config_path else self._config_path
        self._config: dict = {}
        self._load_config()

    @classmethod
    def get_instance(cls, config_path: Optional[str] = None) -> "LLMConfig":
        """获取单例实例

        Args:
            config_path: 配置文件路径（仅首次调用时有效）

        Returns:
            LLMConfig 单例实例
        """
        if cls._instance is None:
            cls._instance = cls(config_path)
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """重置单例实例（用于测试）"""
        cls._instance = None

    def _load_config(self) -> None:
        """从 YAML 文件加载配置"""
        # 查找配置文件
        config_path = self._find_config_file()

        with open(config_path, "r", encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)

        # 替换环境变量
        self._config = self._substitute_env_vars(raw_config)

    def _find_config_file(self) -> Path:
        """查找配置文件

        按以下顺序查找：
        1. 绝对路径
        2. 相对于当前工作目录
        3. 相对于项目根目录（向上查找）

        Returns:
            配置文件路径

        Raises:
            FileNotFoundError: 配置文件不存在
        """
        config_path = Path(self._config_path)

        # 如果是绝对路径
        if config_path.is_absolute() and config_path.exists():
            return config_path

        # 相对于当前工作目录
        if config_path.exists():
            return config_path

        # 向上查找项目根目录
        current = Path.cwd()
        for _ in range(10):  # 最多向上查找 10 层
            candidate = current / self._config_path
            if candidate.exists():
                return candidate
            parent = current.parent
            if parent == current:
                break
            current = parent

        raise FileNotFoundError(
            f"Config file not found: {self._config_path}. "
            f"Searched from: {Path.cwd()}"
        )

    def _substitute_env_vars(self, value: Any) -> Any:
        """递归替换配置中的环境变量

        支持 ${VAR_NAME} 格式的环境变量引用。

        Args:
            value: 配置值（可以是字符串、字典、列表）

        Returns:
            替换后的配置值
        """
        if isinstance(value, str):
            # 匹配 ${VAR_NAME} 格式
            pattern = r"\$\{([^}]+)\}"

            def replace(match: re.Match) -> str:
                var_name = match.group(1)
                env_value = os.environ.get(var_name)
                if env_value is None:
                    raise ValueError(
                        f"Environment variable '{var_name}' not found. "
                        f"Please set it before loading config."
                    )
                return env_value

            return re.sub(pattern, replace, value)

        elif isinstance(value, dict):
            return {k: self._substitute_env_vars(v) for k, v in value.items()}

        elif isinstance(value, list):
            return [self._substitute_env_vars(item) for item in value]

        return value

    def get_model(self, module_path: str) -> str:
        """获取模块对应的模型名称

        Args:
            module_path: 模块路径，格式为 "agent_name.submodule"
                        例如: "simple_agent.reflect", "decision", "form_filler.code_generator"

        Returns:
            模型名称，如果未配置则返回默认模型

        Examples:
            >>> config = LLMConfig.get_instance()
            >>> config.get_model("simple_agent.reflect")
            'glm-5'
            >>> config.get_model("decision")
            'qwen3.5-plus'
            >>> config.get_model("unknown.module")
            'glm-5'  # 返回默认模型
        """
        llm_config = self._config.get("llm", {})
        agents_config = llm_config.get("agents", {})

        # 解析模块路径
        parts = module_path.split(".")

        # 遍历配置层级查找模型
        current = agents_config
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                # 未找到配置，返回默认模型
                return llm_config.get("default_model", "glm-5")

        # 如果最终值是字典，检查是否有 model 字段
        if isinstance(current, dict):
            return current.get("model", llm_config.get("default_model", "glm-5"))

        # 如果最终值是字符串，直接返回
        if isinstance(current, str):
            return current

        # 其他情况返回默认模型
        return llm_config.get("default_model", "glm-5")

    def get_api_key(self) -> str:
        """获取 API Key

        Returns:
            API Key 字符串

        Raises:
            ValueError: API Key 未配置或为空
        """
        api_key = self._config.get("llm", {}).get("api_key", "")
        if not api_key:
            raise ValueError(
                "API key not configured. "
                "Please set DASHSCOPE_API_KEY environment variable "
                "or configure api_key in config/llm_config.yaml"
            )
        return api_key

    def get_base_url(self) -> str:
        """获取 API Base URL

        Returns:
            Base URL 字符串
        """
        return self._config.get("llm", {}).get(
            "base_url", "https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

    def get_default_model(self) -> str:
        """获取默认模型名称

        Returns:
            默认模型名称
        """
        return self._config.get("llm", {}).get("default_model", "glm-5")

    @property
    def raw_config(self) -> dict:
        """获取原始配置（用于调试）

        Returns:
            原始配置字典
        """
        return self._config.copy()


# 便捷函数
def get_llm_model(module_path: str) -> str:
    """获取模块对应的 LLM 模型名称

    Args:
        module_path: 模块路径，如 "simple_agent.reflect"

    Returns:
        模型名称
    """
    return LLMConfig.get_instance().get_model(module_path)


def get_llm_api_key() -> str:
    """获取 LLM API Key

    Returns:
        API Key
    """
    return LLMConfig.get_instance().get_api_key()


def get_llm_base_url() -> str:
    """获取 LLM API Base URL

    Returns:
        Base URL
    """
    return LLMConfig.get_instance().get_base_url()
