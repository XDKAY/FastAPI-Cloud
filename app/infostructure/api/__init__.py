from fastapi import APIRouter
from .routers.auth import router as auth_router
from .routers.user import router as user_router
from .routers.node import router as node_router


routers = APIRouter()


routers.include_router(auth_router)
routers.include_router(user_router)
routers.include_router(node_router)