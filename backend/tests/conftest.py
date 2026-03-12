"""pytest fixtures for Phase 4 scenario tests"""

import asyncio
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

# 添加项目根目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.llm import get_llm

load_dotenv()


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def llm():
    """创建 LLM 实例"""
    try:
        return get_llm()
    except Exception as e:
        pytest.skip(f"LLM 配置未就绪: {e}")


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


@pytest.fixture
def erp_config():
    """ERP 测试配置"""
    return {
        "base_url": os.getenv("ERP_BASE_URL", "https://erp.example.com"),
        "username": os.getenv("ERP_USERNAME", "test_user"),
        "password": os.getenv("ERP_PASSWORD", ""),
    }
