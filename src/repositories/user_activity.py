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

    async def upsert(
        self, filter_: dict, key: str, value: Any, table_name: str
    ):
        collection = self._db[table_name]
        await collection.update_one(
            filter_, {"$set": {key: value}}, upsert=True
        )

    async def upsert_document(
        self,
        filter_: dict,
        document: dict,
        table_name: str,
        upsert: bool = True,
    ):
        collection = self._db[table_name]
        await collection.update_one(filter_, {"$set": document}, upsert=upsert)

    async def find_one(self, filter_: dict, table_name: str):
        collection = self._db[table_name]
        return await collection.find_one(filter_)

    def find(self, filter_: dict, columns: dict, table_name: str):
        collection = self._db[table_name]
        return collection.find(filter_, columns)

    def aggregate_top_films_by_score(self, table_name: str, limit: int = 10):
        collection = self._db[table_name]

        avg_value_agg = collection.aggregate(
            [
                {"$match": {"is_deleted": False}},
                {"$group": {"_id": None, "num_scores": {"$sum": 1}}},
                {
                    "$group": {
                        "_id": None,
                        "avg_num_scores": {"$avg": "$num_scores"},
                    }
                },
            ]
        )

        avg_num_scores = avg_value_agg[0].get("avg_num_scores", 0)

        return collection.aggregate(
            [
                {"$match": {"is_deleted": False}},
                {
                    "$group": {
                        "film_id": "$film_id",
                        "avg_score": {"$avg": "$score"},
                        "num_scores": {"$sum": 1},
                    }
                },
                {"$match": {"num_scores": {"$gte": avg_num_scores}}},
                {"$sort": {"avg_score": -1}},
                {"$limit": limit},
            ]
        )

    def get_films_watching_now(self, table_name: str):
        collection = self._db[table_name]
        return collection.aggregate(
            [
                {"$group": {"_id": "$film_id", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
        )
