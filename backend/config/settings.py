"""Centralized configuration using Pydantic BaseSettings."""
from functools import lru_cache
from pathlib import Path

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file from project root (handles relative path issues)
_project_root = Path(__file__).parent.parent.parent
_env_file = _project_root / ".env"
if _env_file.exists():
    load_dotenv(_env_file)


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All settings can be overridden via environment variables or .env file.
    Environment variable names are case-insensitive (e.g., LLM_MODEL or llm_model).
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM Configuration
    dashscope_api_key: str = ""
    openai_api_key: str = ""
    llm_model: str = "qwen3.5-plus"
    llm_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    llm_temperature: float = 0.0

    # ERP Configuration
    erp_base_url: str = ""
    erp_username: str = ""
    erp_password: str = ""

    # 外部 API 模块路径（用于前置条件中复用现有项目的 API 封装）
    # 例如：/path/to/your/erp-test-project
    # 设置后可在前置条件代码中 import api.xxx
    erp_api_module_path: str | None = None

    # External webseleniumerp project path for precondition operations
    # Points to the webseleniumerp project containing base_prerequisites.py
    # Set this to enable importing external precondition operations (FA1, HC1, etc.)
    # Example: /Users/you/projects/webseleniumerp
    weberp_path: str | None = Field(default=None, validation_alias="WEBSERP_PATH")

    # Database Configuration
    database_url: str = "sqlite+aiosqlite:///./data/database.db"

    # Server Configuration
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Return cached Settings singleton.

    Uses lru_cache to ensure Settings is only instantiated once,
    providing a single source of truth throughout the application.
    """
    return Settings()
