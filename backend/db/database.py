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
)

# 异步会话工厂
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """获取数据库会话"""
    async with async_session() as session:
        yield session


async def init_db():
    """初始化数据库（创建表）"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
