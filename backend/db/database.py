"""SQLAlchemy 数据库配置"""

from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# 数据库文件路径
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite+aiosqlite:///{DATA_DIR}/database.db"


class Base(DeclarativeBase):
    """SQLAlchemy 基类"""
    pass


# 异步引擎 with explicit pool configuration
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,        # Connection pool size
    max_overflow=0,     # No overflow connections for SQLite
    pool_pre_ping=True, # Validate connections before use
    pool_recycle=3600,  # Recycle connections after 1 hour
    connect_args={"timeout": 30},  # SQLite busy_timeout: wait up to 30s for locks during batch execution
)

# 异步会话工厂
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """获取数据库会话"""
    async with async_session() as session:
        yield session


async def init_db() -> None:
    """初始化数据库（创建表 + 添加新列）"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        # Phase 59: Add sequence_number columns to existing tables if missing
        from sqlalchemy import text

        # steps.sequence_number
        result = await conn.execute(text("PRAGMA table_info(steps)"))
        columns = [row[1] for row in result]
        if "sequence_number" not in columns:
            await conn.execute(text("ALTER TABLE steps ADD COLUMN sequence_number INTEGER"))

        # assertion_results.sequence_number
        result = await conn.execute(text("PRAGMA table_info(assertion_results)"))
        columns = [row[1] for row in result]
        if "sequence_number" not in columns:
            await conn.execute(text("ALTER TABLE assertion_results ADD COLUMN sequence_number INTEGER"))

        # Phase 72: Add batch_id column to runs if missing
        result = await conn.execute(text("PRAGMA table_info(runs)"))
        columns = [row[1] for row in result]
        if "batch_id" not in columns:
            await conn.execute(text("ALTER TABLE runs ADD COLUMN batch_id VARCHAR(8)"))

        # Phase 76: Add login_role column to tasks if missing
        result = await conn.execute(text("PRAGMA table_info(tasks)"))
        columns = [row[1] for row in result]
        if "login_role" not in columns:
            await conn.execute(text("ALTER TABLE tasks ADD COLUMN login_role VARCHAR(20)"))

        # Phase 85: Add healing columns to runs if missing (HEAL-03)
        result = await conn.execute(text("PRAGMA table_info(runs)"))
        columns = [row[1] for row in result]
        if "generated_code_path" not in columns:
            await conn.execute(text(
                "ALTER TABLE runs ADD COLUMN generated_code_path VARCHAR(500)"
            ))
        if "healing_status" not in columns:
            await conn.execute(text(
                "ALTER TABLE runs ADD COLUMN healing_status VARCHAR(20) DEFAULT 'pending'"
            ))
        if "healing_attempts" not in columns:
            await conn.execute(text(
                "ALTER TABLE runs ADD COLUMN healing_attempts INTEGER DEFAULT 0"
            ))
        if "healing_error" not in columns:
            await conn.execute(text(
                "ALTER TABLE runs ADD COLUMN healing_error TEXT"
            ))
        if "healing_error_category" not in columns:
            await conn.execute(text(
                "ALTER TABLE runs ADD COLUMN healing_error_category VARCHAR(50) DEFAULT ''"
            ))
