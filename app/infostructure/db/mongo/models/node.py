from typing import Optional
from uuid import UUID
from pydantic import Field
from beanie import Document, PydanticObjectId


class Node(Document):
    name: str
    type: str
    parent_id: Optional[PydanticObjectId]
    user_id: UUID
    path: str = ""
    childs: list[PydanticObjectId] = Field(default_factory=list)
    size: int = 0

    class Settings:
        name = "Nodes"