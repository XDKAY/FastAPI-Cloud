import os
import shutil
import anyio


from typing import Optional, Any
from uuid import UUID
from pathlib import Path

from app.core.settings.settings import settings
from app.core.exceptions.file_system import (
    FileSystemExistingDirectoryError,
    FileSystemIsNotEmptyDirectoryError,
    FileSystemExistingFileError,
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

        path_ = FileSystem.get_path_to_directory(user_id, path)

        is_exist_path = await anyio.Path(path_).exists()

        if is_exist_path:
            raise FileSystemExistingDirectoryError(name=path_.name)
        
        await anyio.Path(path_).mkdir()
        
    @staticmethod
    async def delete_dir(user_id: UUID, path: str):
        try:
            path_ = FileSystem.get_path_to_directory(user_id, path)

            is_exist_path = await anyio.Path(path_).exists()
            if is_exist_path:
                await anyio.Path(path_).rmdir()

        except OSError as e:
            raise FileSystemIsNotEmptyDirectoryError(name=path_.name) from e

    @staticmethod
    async def create_file(user_id: UUID, path: str, file_object: Any):
        path_ = FileSystem.get_path_to_directory(user_id, path)

        is_exist_path = await anyio.Path(path_).exists()

        if is_exist_path:
            raise FileSystemExistingFileError(path_.name)

        await file_object.seek(0)

        async with await anyio.open_file(str(path_), "wb") as save_file:
            while (chunck := await file_object.read(1024 * 1024)):
                await save_file.write(chunck)

    @staticmethod
    async def delete_file(user_id: UUID, path: str):
        path_ = FileSystem.get_path_to_directory(user_id, path)

        is_exist_path = await anyio.Path(path_).exists()

        if is_exist_path:
            await anyio.to_thread.run_sync(os.remove, path_)


    @staticmethod
    def get_path_to_directory(user_id: UUID, path: str) -> Path:
        return settings.storage_path / str(user_id) / path
