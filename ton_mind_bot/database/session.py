from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ton_mind_bot.config import settings
from ton_mind_bot.database.base import Base

engine = create_async_engine(settings.database_url, future=True, echo=False)
session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with session_factory() as session:
        yield session
