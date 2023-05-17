from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from src.repositories.base import BaseRepository
from src.settings.db import db_settings


class UserActivityRepository(BaseRepository):
    def __init__(self, client: AsyncIOMotorClient):
        self._db = client.db_client[db_settings.db_name]

    async def insert_one(self, data: dict, table_name: str):
        collection = self._db[table_name]
        await collection.insert_one(data)

    async def update_one(
        self, filter_: dict, key: str, value: Any, table_name: str
    ):
        collection = self._db[table_name]
        await collection.update_one(filter_, {"$set": {key: value}})

    async def find_one(self, filter_: dict, table_name: str):
        collection = self._db[table_name]
        return await collection.find_one(filter_)

    # async def insert_or_update_view_progress(self, data: dict):
    #     table_name = "view_progress"
    #     filter_query = {
    #         "film_id": data.get("film_id"),
    #         "user_id": data.get("user_id"),
    #     }
    #
    #     if await self.find_one(filter_=filter_query, table_name=table_name):
    #         await self.update_one(
    #             filter_=filter_query,
    #             key="viewed_frame",
    #             value=data.get("viewed_frame"),
    #             table_name=table_name,
    #         )
    #     else:
    #         await self.insert_one(data=data, table_name=table_name)
