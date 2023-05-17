from motor.motor_asyncio import AsyncIOMotorClient

from src.settings.db import db_settings


class MongoDbConnector:
    db_client: AsyncIOMotorClient = None

    @classmethod
    async def setup(cls):
        cls.db_client = AsyncIOMotorClient(
            db_settings.db_url, serverSelectionTimeoutMS=5000
        )

    @classmethod
    async def close(cls):
        if cls.db_client:
            await cls.db_client.close()
            cls.db_client = None
