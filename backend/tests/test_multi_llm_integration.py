# backend/tests/test_multi_llm_integration.py
"""多模型配置集成测试"""

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
def test_config(tmp_path, monkeypatch):
    """创建测试配置"""
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

    # 使用构造函数传入配置文件路径
    config = LLMConfig(str(config_file))
    return config


class TestMultiLLMIntegration:
    """多模型集成测试"""

    def test_all_modules_have_correct_models(self, test_config):
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

    def test_same_model_instances_are_shared(self, test_config):
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

    def test_factory_clear_cache(self, test_config):
        """测试清除缓存"""
        # 创建实例
        llm1 = LLMFactory.get_reflect_llm()

        # 清除缓存
        LLMFactory.clear_cache()

        # 再次获取应该是新实例
        llm2 = LLMFactory.get_reflect_llm()
        assert llm1 is not llm2
