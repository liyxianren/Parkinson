"""
Tremor Guard - Database Configuration
震颤卫士 - 数据库配置

SQLAlchemy 异步数据库连接
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # 开发模式下打印 SQL
    pool_pre_ping=True,   # 连接池预检查
    pool_size=10,
    max_overflow=20
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# 声明基类
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    获取数据库会话 (依赖注入)

    Usage:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """初始化数据库 (创建所有表)"""
    # 导入所有模型以注册到 Base
    from app.models import user, device, tremor_data, medication, rehabilitation
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """关闭数据库连接"""
    await engine.dispose()
