"""Centralized configuration using Pydantic BaseSettings."""
from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


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
