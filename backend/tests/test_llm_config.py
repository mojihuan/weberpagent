"""LLM 配置加载器测试"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from backend.llm.config import (
    LLMConfig,
    get_llm_api_key,
    get_llm_base_url,
    get_llm_model,
)


@pytest.fixture(autouse=True)
def reset_config():
    """每个测试前重置单例"""
    LLMConfig.reset()
    yield
    LLMConfig.reset()


@pytest.fixture
def mock_env_with_api_key(monkeypatch):
    """Mock 环境变量，设置 API Key"""
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-api-key-12345")


@pytest.fixture
def temp_config_file(tmp_path, mock_env_with_api_key):
    """创建临时配置文件"""
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
    config_file.write_text(config_content)
    return str(config_file)


class TestLLMConfig:
    """LLMConfig 类测试"""

    def test_load_config(self, temp_config_file):
        """测试加载配置文件"""
        config = LLMConfig.get_instance(temp_config_file)

        assert config is not None
        assert config.raw_config is not None
        assert "llm" in config.raw_config

    def test_get_model_simple_agent_reflect(self, temp_config_file):
        """测试获取 simple_agent.reflect 模型"""
        config = LLMConfig.get_instance(temp_config_file)
        model = config.get_model("simple_agent.reflect")

        assert model == "glm-5"

    def test_get_model_decision(self, temp_config_file):
        """测试获取 decision 模型"""
        config = LLMConfig.get_instance(temp_config_file)
        model = config.get_model("decision")

        assert model == "qwen3.5-plus"

    def test_get_model_code_reviewer(self, temp_config_file):
        """测试获取 code_reviewer 模型"""
        config = LLMConfig.get_instance(temp_config_file)
        model = config.get_model("form_filler.code_reviewer")

        assert model == "qwen3-coder-next"

    def test_get_model_code_generator(self, temp_config_file):
        """测试获取 code_generator 模型"""
        config = LLMConfig.get_instance(temp_config_file)
        model = config.get_model("form_filler.code_generator")

        assert model == "glm-5"

    def test_get_model_unknown_returns_default(self, temp_config_file):
        """测试未知模块返回默认模型"""
        config = LLMConfig.get_instance(temp_config_file)
        model = config.get_model("unknown.module")

        assert model == "glm-5"

    def test_get_model_partial_path_returns_default(self, temp_config_file):
        """测试部分路径返回默认模型"""
        config = LLMConfig.get_instance(temp_config_file)
        model = config.get_model("simple_agent.unknown_submodule")

        assert model == "glm-5"

    def test_get_api_key(self, temp_config_file):
        """测试获取 API Key"""
        config = LLMConfig.get_instance(temp_config_file)
        api_key = config.get_api_key()

        assert api_key == "test-api-key-12345"

    def test_get_base_url(self, temp_config_file):
        """测试获取 Base URL"""
        config = LLMConfig.get_instance(temp_config_file)
        base_url = config.get_base_url()

        assert base_url == "https://dashscope.aliyuncs.com/compatible-mode/v1"

    def test_env_var_substitution(self, tmp_path, monkeypatch):
        """测试环境变量替换"""
        monkeypatch.setenv("TEST_API_KEY", "my-custom-key")
        monkeypatch.setenv("DASHSCOPE_API_KEY", "dashscope-key")

        config_content = """
llm:
  api_key: ${TEST_API_KEY}
  base_url: https://example.com/v1
  default_model: test-model
"""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text(config_content)

        LLMConfig.reset()
        config = LLMConfig.get_instance(str(config_file))

        assert config.get_api_key() == "my-custom-key"

    def test_env_var_not_found_raises_error(self, tmp_path):
        """测试环境变量不存在时抛出错误"""
        # 确保环境变量不存在
        if "NONEXISTENT_VAR" in os.environ:
            del os.environ["NONEXISTENT_VAR"]

        config_content = """
llm:
  api_key: ${NONEXISTENT_VAR}
  base_url: https://example.com/v1
  default_model: test-model
"""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text(config_content)

        with pytest.raises(ValueError, match="Environment variable 'NONEXISTENT_VAR' not found"):
            LLMConfig(config_path=str(config_file))

    def test_singleton_pattern(self, temp_config_file):
        """测试单例模式"""
        config1 = LLMConfig.get_instance(temp_config_file)
        config2 = LLMConfig.get_instance()

        assert config1 is config2

    def test_reset_clears_singleton(self, temp_config_file):
        """测试 reset 清除单例"""
        config1 = LLMConfig.get_instance(temp_config_file)
        LLMConfig.reset()
        config2 = LLMConfig.get_instance(temp_config_file)

        assert config1 is not config2

    def test_get_default_model(self, temp_config_file):
        """测试获取默认模型"""
        config = LLMConfig.get_instance(temp_config_file)
        default_model = config.get_default_model()

        assert default_model == "glm-5"


class TestConvenienceFunctions:
    """便捷函数测试"""

    def test_get_llm_model(self, temp_config_file):
        """测试 get_llm_model 便捷函数"""
        LLMConfig.reset()
        # 先初始化单例
        LLMConfig.get_instance(temp_config_file)

        model = get_llm_model("decision")
        assert model == "qwen3.5-plus"

    def test_get_llm_api_key(self, temp_config_file):
        """测试 get_llm_api_key 便捷函数"""
        LLMConfig.reset()
        LLMConfig.get_instance(temp_config_file)

        api_key = get_llm_api_key()
        assert api_key == "test-api-key-12345"

    def test_get_llm_base_url(self, temp_config_file):
        """测试 get_llm_base_url 便捷函数"""
        LLMConfig.reset()
        LLMConfig.get_instance(temp_config_file)

        base_url = get_llm_base_url()
        assert base_url == "https://dashscope.aliyuncs.com/compatible-mode/v1"


class TestConfigFileNotFound:
    """配置文件不存在测试"""

    def test_config_file_not_found(self):
        """测试配置文件不存在时抛出错误"""
        LLMConfig.reset()

        with pytest.raises(FileNotFoundError, match="Config file not found"):
            LLMConfig(config_path="nonexistent/config.yaml")


class TestEmptyApiKey:
    """API Key 为空测试"""

    def test_get_api_key_empty_raises_error(self, tmp_path, monkeypatch):
        """测试 API Key 为空时抛出错误"""
        monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")

        config_content = """
llm:
  api_key: ""
  base_url: https://example.com/v1
  default_model: glm-5
  agents:
    simple_agent:
      reflect: glm-5
"""
        config_file = tmp_path / "empty_key_config.yaml"
        config_file.write_text(config_content)

        LLMConfig.reset()
        config = LLMConfig(str(config_file))

        with pytest.raises(ValueError, match="API key not configured"):
            config.get_api_key()


class TestNestedConfig:
    """嵌套配置测试"""

    def test_deeply_nested_config(self, tmp_path, mock_env_with_api_key):
        """测试深层嵌套配置"""
        config_content = """
llm:
  api_key: ${DASHSCOPE_API_KEY}
  base_url: https://example.com/v1
  default_model: default-model

  agents:
    level1:
      level2:
        level3:
          model: deep-model
"""
        config_file = tmp_path / "nested_config.yaml"
        config_file.write_text(config_content)

        LLMConfig.reset()
        config = LLMConfig.get_instance(str(config_file))

        # 深层嵌套的模型
        model = config.get_model("level1.level2.level3")
        assert model == "deep-model"

        # 不完整路径返回默认模型
        model = config.get_model("level1.level2")
        assert model == "default-model"
