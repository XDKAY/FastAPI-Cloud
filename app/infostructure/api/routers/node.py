from typing import List, Optional, Annotated

from fastapi import APIRouter, status, Query, UploadFile, File
from fastapi.responses import FileResponse

from app.core.schemes.node import NodeCreateScheme
from app.infostructure.dependencies.current_user import CurrentUserDep
from app.infostructure.dependencies.services import NodeServiceDep
from app.infostructure.db.mongo.models.node import Node


router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.get("/")
async def get_nodes(current_user: CurrentUserDep, node_service: NodeServiceDep, parent_id: Optional[str] = Query(default=None)) -> List[Node]:
    list_nodes = await node_service.get_nodes(user_id=current_user.id, parent_id=parent_id)
    return list_nodes


@router.post("/", response_model=Node, status_code=status.HTTP_201_CREATED)
async def create_dir(
    current_user: CurrentUserDep, 
    node_scheme: NodeCreateScheme, 
    node_service: NodeServiceDep,
    ):

    node_model = await node_service.create_node(user_id=current_user.id, node_scheme=node_scheme)

    return node_model


@router.delete("/{node_id}")
async def delete_node(node_id: str, current_user: CurrentUserDep, node_service: NodeServiceDep):
    await node_service.delete_node(user_id=current_user.id, node_id=node_id)

    return {"message": f"The node with the id {node_id} was successfully deleted"}


@router.post("/upload", response_model=Node)
async def upload_file(
    current_user: CurrentUserDep, 
    node_service: NodeServiceDep, 
    file: UploadFile = File(...),
    parent_id: Optional[str] = Query(default=None)
    ):

    node_scheme = NodeCreateScheme(
        name=file.filename,
        type="file",
        parent_id=parent_id,
        size=file.size
    )

    node_model = await node_service.create_node(
        user_id=current_user.id, 
        node_scheme=node_scheme, 
        file_object=file
    )

    return node_model


@router.get("/download/{filename}", response_class=FileResponse)
async def download_file(filename: str, current_user: CurrentUserDep, node_service: NodeServiceDep):
    path = await node_service.get_path_node(user_id=current_user.id, filename=filename)
    return FileResponse(
        path=path, 
        filename=filename, 
        media_type='application/octet-stream',
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )