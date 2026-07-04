from typing import Annotated
from fastapi import Depends

from .repositories import UserRepositoryDep
from app.core.services.user import UserService
from app.core.services.node import NodeService


async def get_user_service(repo: UserRepositoryDep) -> UserService:
    return UserService(repo)


async def get_node_service() -> NodeService:
    return NodeService()


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
NodeServiceDep = Annotated[NodeService, Depends(get_node_service)]