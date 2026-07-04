from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.infostructure.db.sqlite.database import (
    sqlite_connect,
    sqlite_disconnect
)
from app.infostructure.db.mongo.database import (
    mongo_connect,
    mongo_disconnect
)
from app.infostructure.api import routers


@asynccontextmanager
async def lifespan(_: FastAPI):
    await sqlite_connect()
    await mongo_connect()
    yield
    await sqlite_disconnect()
    await mongo_disconnect()


app = FastAPI(
    lifespan=lifespan
)

app.include_router(routers)