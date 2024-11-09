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
)


async def get_db() -> AsyncSession:
    async with __local_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]
