from typing import Annotated
from fastapi import Depends

from .repositories import UserRepositoryDep
from app.core.services.user import UserService


async def get_user_service(repo: UserRepositoryDep) -> UserService:
    return UserService(repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]