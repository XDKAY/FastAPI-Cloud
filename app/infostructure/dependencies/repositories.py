from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repositories.user import SQLUserRepository
from app.infostructure.db.sqlite.database import sqlite_get_session


SQLSessionDep = Annotated[AsyncSession, Depends(sqlite_get_session)]


async def get_user_repository(session: SQLSessionDep) -> SQLUserRepository:
    return SQLUserRepository(session)


UserRepositoryDep = Annotated[SQLUserRepository, Depends(get_user_repository)]