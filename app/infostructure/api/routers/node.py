from fastapi import APIRouter, status

from app.core.schemes.node import NodeCreateScheme
from app.infostructure.dependencies.current_user import CurrentUserDep
from app.infostructure.dependencies.services import NodeServiceDep
from app.infostructure.db.mongo.models.node import Node


router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.post("/", response_model=Node, status_code=status.HTTP_201_CREATED)
async def create_dir(
    current_user: CurrentUserDep, 
    node_scheme: NodeCreateScheme, 
    node_service: NodeServiceDep,
    ):

    node_model = await node_service.create_node(user_id=current_user.id, node_scheme=node_scheme)

    return node_model
