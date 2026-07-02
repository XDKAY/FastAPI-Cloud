from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings.settings import settings
from app.infostructure.db.sqlite.base import Base
from app.infostructure.db.sqlite.models.user import Users


ENGINE = create_async_engine(settings.sqlite.url)
SESSION = async_sessionmaker(ENGINE)


async def sqlite_connect():
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def sqlite_disconnect():
    await ENGINE.dispose()


async def sqlite_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SESSION() as session:
        yield session