from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from shared.settings.settings import settings

engine = create_async_engine(url=settings.postgres.dsn, pool_size=10, max_overflow=20)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with session_maker() as session:
        yield session
