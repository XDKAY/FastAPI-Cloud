from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.infostructure.db.sqlite.database import (
    sqlite_connect,
    sqlite_disconnect
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await sqlite_connect()
    yield
    await sqlite_disconnect()


app = FastAPI(
    lifespan=lifespan
)