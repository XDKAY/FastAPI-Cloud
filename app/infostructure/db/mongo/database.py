from pymongo import AsyncMongoClient
from beanie import init_beanie
from app.core.settings.settings import settings
from app.infostructure.db.mongo.models.node import Node


CLIENT = AsyncMongoClient(settings.mongo.url)


async def mongo_connect():
    await init_beanie(
        database=CLIENT[settings.mongo.name],
        document_models=[Node],
    )

async def mongo_disconnect():
    await CLIENT.close()
