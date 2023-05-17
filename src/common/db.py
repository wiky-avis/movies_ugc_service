from motor.motor_asyncio import AsyncIOMotorClient

from src.settings.db import db_settings

client = AsyncIOMotorClient(db_settings.db_url, serverSelectionTimeoutMS=5000)
db = client[db_settings.db_name]


async def get_session() -> AsyncIOMotorClient:
    return db
