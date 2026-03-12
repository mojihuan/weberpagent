"""LLM 工厂类测试"""

from unittest.mock import MagicMock

import pytest

from backend.llm.base import BaseLLM
from backend.llm.config import LLMConfig
from backend.llm.factory import LLMFactory, get_llm


@pytest.fixture(autouse=True)
def reset_singletons():
    """每个测试前重置单例"""
    LLMConfig.reset()
    LLMFactory.clear_cache()
    yield
    LLMConfig.reset()
    LLMFactory.clear_cache()


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


@pytest.fixture
def mock_llm_class():
    """创建 Mock LLM 类"""
    class MockLLM(BaseLLM):
        def __init__(self, model: str, api_key: str):
            self.model = model
            self.api_key = api_key

        @property
        def model_name(self) -> str:
            return self.model

        async def chat_with_vision(self, messages: list[dict], images: list[str]):
            pass

        def parse_action(self, response: str):
            pass

    return MockLLM


class TestLLMFactory:
    """LLMFactory 类测试"""

    def test_create_returns_llm_instance(
        self, temp_config_file, mock_llm_class
    ):
        """测试 create 返回 LLM 实例"""
        LLMConfig.get_instance(temp_config_file)
        LLMFactory.set_llm_class(mock_llm_class)

        llm = LLMFactory.create("decision")

        assert llm is not None
        assert isinstance(llm, BaseLLM)

    def test_create_uses_correct_model(
        self, temp_config_file, mock_llm_class
    ):
        """测试 create 使用正确的模型"""
        LLMConfig.get_instance(temp_config_file)
        LLMFactory.set_llm_class(mock_llm_class)

        # 测试 decision 模块
        llm_decision = LLMFactory.create("decision")
        assert llm_decision.model == "qwen3.5-plus"

        # 测试 simple_agent.reflect 模块
        llm_reflect = LLMFactory.create("simple_agent.reflect")
        assert llm_reflect.model == "glm-5"

        # 测试 code_reviewer 模块
        llm_reviewer = LLMFactory.create("form_filler.code_reviewer")
        assert llm_reviewer.model == "qwen3-coder-next"

    def test_same_model_shares_instance(
        self, temp_config_file, mock_llm_class
    ):
        """测试相同模型共享实例"""
        LLMConfig.get_instance(temp_config_file)
        LLMFactory.set_llm_class(mock_llm_class)

        # 这些模块都使用 glm-5
        llm1 = LLMFactory.create("simple_agent.reflect")
        llm2 = LLMFactory.create("form_filler.code_generator")
        llm3 = LLMFactory.create("form_filler.code_optimizer")

        # 应该是同一个实例（因为模型相同）
        assert llm1 is llm2
        assert llm2 is llm3

    def test_different_model_creates_new_instance(
        self, temp_config_file, mock_llm_class
    ):
        """测试不同模型创建新实例"""
        LLMConfig.get_instance(temp_config_file)
        LLMFactory.set_llm_class(mock_llm_class)

        # decision 使用 qwen3.5-plus
        llm_decision = LLMFactory.create("decision")
        # reflect 使用 glm-5
        llm_reflect = LLMFactory.create("simple_agent.reflect")
        # code_reviewer 使用 qwen3-coder-next
        llm_reviewer = LLMFactory.create("form_filler.code_reviewer")

        # 应该是不同的实例（因为模型不同）
        assert llm_decision is not llm_reflect
        assert llm_decision is not llm_reviewer
        assert llm_reflect is not llm_reviewer

    def test_convenience_methods(
        self, temp_config_file, mock_llm_class
    ):
        """测试便捷方法"""
        LLMConfig.get_instance(temp_config_file)
        LLMFactory.set_llm_class(mock_llm_class)

        # 测试所有便捷方法
        assert LLMFactory.get_reflect_llm().model == "glm-5"
        assert LLMFactory.get_decision_llm().model == "qwen3.5-plus"
        assert LLMFactory.get_code_generator_llm().model == "glm-5"
        assert LLMFactory.get_code_optimizer_llm().model == "glm-5"
        assert LLMFactory.get_code_reviewer_llm().model == "qwen3-coder-next"

    def test_clear_cache(
        self, temp_config_file, mock_llm_class
    ):
        """测试清除缓存"""
        LLMConfig.get_instance(temp_config_file)
        LLMFactory.set_llm_class(mock_llm_class)

        # 创建实例
        llm1 = LLMFactory.create("decision")

        # 清除缓存
        LLMFactory.clear_cache()

        # 再次创建应该是新实例
        llm2 = LLMFactory.create("decision")
        assert llm1 is not llm2

    def test_set_llm_class(
        self, temp_config_file, mock_llm_class
    ):
        """测试设置 LLM 类"""
        LLMConfig.get_instance(temp_config_file)
        LLMFactory.set_llm_class(mock_llm_class)

        llm = LLMFactory.create("decision")
        assert isinstance(llm, mock_llm_class)

    def test_create_with_unknown_module_uses_default(
        self, temp_config_file, mock_llm_class
    ):
        """测试未知模块使用默认模型"""
        LLMConfig.get_instance(temp_config_file)
        LLMFactory.set_llm_class(mock_llm_class)

        llm = LLMFactory.create("unknown.module")
        assert llm.model == "glm-5"  # 默认模型


class TestGetLLMFunction:
    """get_llm 便捷函数测试"""

    def test_get_llm_function(
        self, temp_config_file, mock_llm_class
    ):
        """测试 get_llm 便捷函数"""
        LLMConfig.get_instance(temp_config_file)
        LLMFactory.set_llm_class(mock_llm_class)

        llm = get_llm("decision")
        assert llm is not None
        assert llm.model == "qwen3.5-plus"

    def test_get_llm_shares_instance_with_factory(
        self, temp_config_file, mock_llm_class
    ):
        """测试 get_llm 与工厂共享实例"""
        LLMConfig.get_instance(temp_config_file)
        LLMFactory.set_llm_class(mock_llm_class)

        llm1 = get_llm("decision")
        llm2 = LLMFactory.create("decision")

        # 应该是同一个实例
        assert llm1 is llm2


class TestCacheKey:
    """缓存键测试"""

    def test_cache_key_includes_class_name(
        self, temp_config_file, mock_llm_class
    ):
        """测试缓存键包含类名"""
        LLMConfig.get_instance(temp_config_file)
        LLMFactory.set_llm_class(mock_llm_class)

        # 创建实例
        LLMFactory.create("decision")

        # 检查缓存键
        assert "MockLLM:qwen3.5-plus" in LLMFactory._instances

    def test_different_classes_different_cache(
        self, temp_config_file, mock_llm_class
    ):
        """测试不同类使用不同缓存"""
        LLMConfig.get_instance(temp_config_file)
        LLMFactory.set_llm_class(mock_llm_class)

        # 使用 MockLLM 创建实例
        llm1 = LLMFactory.create("decision")

        # 创建另一个 Mock 类
        class AnotherMockLLM(BaseLLM):
            def __init__(self, model: str, api_key: str):
                self.model = model

            @property
            def model_name(self) -> str:
                return self.model

            async def chat_with_vision(self, messages, images):
                pass

            def parse_action(self, response):
                pass

        LLMFactory.set_llm_class(AnotherMockLLM)
        llm2 = LLMFactory.create("decision")

        # 应该是不同的实例（因为类不同）
        assert llm1 is not llm2
        assert not isinstance(llm2, mock_llm_class)
        assert isinstance(llm2, AnotherMockLLM)
