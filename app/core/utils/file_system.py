import anyio

from typing import Optional
from uuid import UUID
from pathlib import Path

from app.core.settings.settings import settings
from app.core.exceptions.file_system import (
    FileSystemExistingDirectoryError,
    FileSystemIsNotEmptyDirectoryError,
)



class FileSystem:

    _ROOT_CREATED = False

    @staticmethod
    async def create_storage_dir():

        if FileSystem._ROOT_CREATED:
            return

        path_ = settings.storage_path
        is_exist_path = await anyio.Path(path_).exists()

        if not is_exist_path:
            await anyio.Path(path_).mkdir()

            FileSystem._ROOT_CREATED = True


    @staticmethod
    async def create_dir(user_id: UUID, path: str):

        path_ = FileSystem._get_path_to_directory(user_id, path)

        is_exist_path = await anyio.Path(path_).exists()

        if is_exist_path:
            raise FileSystemExistingDirectoryError(name=path_.name)
        
        await anyio.Path(path_).mkdir()
        
    @staticmethod
    async def delete_dir(user_id: UUID, path: str):
        try:
            path_ = FileSystem._get_path_to_directory(user_id, path)

            is_exist_path = await anyio.Path(path_).exists()
            if is_exist_path:
                await anyio.Path(path_).rmdir()

        except OSError as e:
            raise FileSystemIsNotEmptyDirectoryError(name=path_.name) from e

    @staticmethod
    def _get_path_to_directory(user_id: UUID, path: str) -> Path:
        return settings.storage_path / str(user_id) / path
