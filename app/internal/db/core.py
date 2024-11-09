from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.internal.config import settings


def __get_engine(url: str = str(settings.POSTGRES_DATABASE_URI)) -> AsyncEngine:
    return create_async_engine(url)


__local_session: async_sessionmaker = async_sessionmaker(
    bind=__get_engine(),
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autoflush=False,  # Don't auto-flush changes to DB
    autocommit=False,  # Keep everything in transactions
)


async def get_db() -> AsyncSession:
    async with __local_session() as session:
        yield session
        await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_db)]
