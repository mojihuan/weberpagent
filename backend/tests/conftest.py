"""pytest fixtures for Phase 4 scenario tests"""

import asyncio
import os
from pathlib import Path

import pytest

# 添加项目根目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.llm.qwen import QwenChat


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def llm():
    """创建 LLM 实例"""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        pytest.skip("DASHSCOPE_API_KEY 未配置")
    return QwenChat(model="qwen-vl-max")


@pytest.fixture
def test_config():
    """加载测试配置"""
    import yaml
    config_path = Path(__file__).parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def output_dir():
    """创建输出目录"""
    output_path = Path("outputs/tests/phase4")
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path
