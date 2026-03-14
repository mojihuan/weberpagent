"""Unit tests for LLM configuration

Tests FND-04: LLM deterministic configuration
"""
import pytest


class TestCreateLLM:
    """Tests for create_llm() - placeholders for Plan 01-04"""

    @pytest.mark.skip(reason="Implemented in Plan 01-04 Task 3")
    def test_create_llm_temperature_default(self):
        """create_llm() returns temperature=0.0 by default"""
        pass

    @pytest.mark.skip(reason="Implemented in Plan 01-04 Task 3")
    def test_create_llm_temperature_from_config(self):
        """create_llm() respects provided temperature in config"""
        pass


class TestGetLLMConfig:
    """Tests for get_llm_config() - placeholders for Plan 01-04"""

    @pytest.mark.skip(reason="Implemented in Plan 01-04 Task 3")
    def test_get_llm_config_uses_settings(self):
        """get_llm_config() uses centralized Settings"""
        pass

    @pytest.mark.skip(reason="Implemented in Plan 01-04 Task 3")
    def test_get_llm_config_temperature_zero(self):
        """get_llm_config() returns temperature=0.0"""
        pass
