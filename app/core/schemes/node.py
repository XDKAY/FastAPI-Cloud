from typing import Optional
from pydantic import BaseModel
from beanie import PydanticObjectId


class NodeCreateScheme(BaseModel):
    """ Schema for files and directories """

    name: str
    type: str
    parent_id: Optional[PydanticObjectId] = None
    size: int = 0
