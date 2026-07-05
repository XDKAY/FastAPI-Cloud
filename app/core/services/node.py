from typing import Any, Optional, List
from pathlib import Path
from uuid import UUID
from beanie import PydanticObjectId

from app.core.schemes.node import NodeCreateScheme
from app.core.utils.file_system import FileSystem

from app.core.exceptions.file_system import (
    FileSystemExistingDirectoryError,
    FileSystemIsNotEmptyDirectoryError,
    FileSystemExistingFileError,
)

from app.infostructure.db.mongo.models.node import Node



class NodeService:
    _MODEL = Node

    def __init__(self) -> None:
        self._fs = FileSystem()

    async def get_nodes(self, user_id: UUID, parent_id: Optional[str]) -> List[Node]:

        parent_object_id = PydanticObjectId(parent_id) if parent_id else None

        return await self._MODEL.find(
            self._MODEL.user_id == user_id,
            self._MODEL.parent_id == parent_object_id,
            self._MODEL.name != "",
        ).to_list()

    async def create_node(self, user_id: UUID, node_scheme: NodeCreateScheme, file_object: Optional[Any] = None) -> Node:
        node_model = Node(
            **node_scheme.model_dump(),
            user_id=user_id
        )

        if node_scheme.type == "dir":
            if not node_scheme.parent_id:
                node_model.path = node_scheme.name
                
            else:
                parent = await self._MODEL.find_one(self._MODEL.id == node_scheme.parent_id)
                node_model.path = f"{parent.path}/{node_scheme.name}"

            try:
                await self._fs.create_dir(user_id=user_id, path=node_model.path)
                await node_model.save()

                if node_scheme.parent_id:
                    parent.childs.append(node_model.id)
                    await parent.save()

            except FileSystemExistingDirectoryError:
                raise 

        if node_scheme.type == "file":
            if not node_scheme.parent_id:
                node_model.path = node_scheme.name

            else:
                parent = await self._MODEL.find_one(self._MODEL.id == node_scheme.parent_id)
                node_model.path = f"{parent.path}/{node_scheme.name}"

                parent.childs.append(node_model.id)
                await parent.save()

            try:
                await self._fs.create_file(
                    user_id=user_id, 
                    path=node_model.path, 
                    file_object=file_object
                )
                
                await node_model.save()

                if node_scheme.parent_id:
                    parent.childs.append(node_model.id)
                    await parent.save()

            except FileSystemExistingFileError:
                raise

        return node_model
    

    async def delete_node(self, user_id: UUID, node_id: str) -> None:
        
        node = await self._MODEL.find_one(
            self._MODEL.id == PydanticObjectId(node_id),
            self._MODEL.user_id == user_id
        )

        if node.parent_id:
            parent = await self._MODEL.find_one(
                self._MODEL.id == node.parent_id
            )

            parent.childs.remove(node.id)

            await parent.save()

        if node.type == "dir":
            if node.childs:
                raise FileSystemIsNotEmptyDirectoryError(name=node.name)

            await self._fs.delete_dir(user_id=user_id, path=node.path)
            
        
        if node.type == "file":
            await self._fs.delete_file(user_id=user_id, path=node.path)

        await node.delete()

    async def get_path_node(self, user_id: UUID, filename: str) -> Path:
        node_model = await self._MODEL.find_one(
            self._MODEL.user_id == user_id,
            self._MODEL.name == filename
        )

        return self._fs.get_path_to_directory(user_id=user_id, path=node_model.path)






