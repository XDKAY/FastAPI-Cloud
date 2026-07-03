from typing import Optional
from uuid import UUID
from app.core.repositories.user import AbstractUserRepository
from app.core.schemes.user import (
    UserCreateScheme,
    UserPrivateScheme,
    UserDTO
)

class UserService:
    def __init__(self, repo: AbstractUserRepository) -> None:
        self._repo = repo

    async def get_user_by_id(self, user_id: UUID) -> Optional[UserPrivateScheme]:
        return await self._repo.get_by_id(user_id)

    async def create_user(self, user: UserCreateScheme) -> UserPrivateScheme:
        return await self._repo.create(user)

    async def get_existing_user(self, username: str, email: str) -> Optional[UserPrivateScheme]:
        return await self._repo.get_existing(username, email)

    async def delete_user(self, user_id: UUID) -> None:
        await self._repo.remove(user_id)