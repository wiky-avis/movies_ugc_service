import logging
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from src.api.v1.models.film_scores import FilmAvgScore
from src.repositories.base import BaseRepository
from src.settings.db import db_settings


logger = logging.getLogger(__name__)


class UserActivityRepository(BaseRepository):
    def __init__(self, client: AsyncIOMotorClient):
        self._db = client.db_client[db_settings.db_name]

    async def insert_one(self, data: dict, table_name: str):
        collection = self._db[table_name]
        await collection.insert_one(data)

    async def update_one(
        self, filter_: dict, key: str, value: Any, table_name: str, method: str = "$set"
    ):
        collection = self._db[table_name]
        await collection.update_one(filter_, {method: {key: value}})

    async def upsert(
        self,
        filter_: dict,
        document: dict,
        table_name: str,
    ):
        collection = self._db[table_name]
        await collection.update_one(filter_, {"$set": document}, upsert=True)

    async def find_one(self, filter_: dict, table_name: str) -> dict:
        collection = self._db[table_name]
        return await collection.find_one(filter_)

    def find(self, filter_: dict, columns: dict, table_name: str):
        collection = self._db[table_name]
        return collection.find(filter_, columns)

    async def aggregate_top_films_by_score(
        self, table_name: str, limit: int
    ) -> list[FilmAvgScore]:
        collection = self._db[table_name]

        avg_value_agg_cursor = collection.aggregate(
            [
                {"$match": {"is_deleted": False}},
                {"$group": {"_id": "$film_id", "num_scores": {"$sum": 1}}},
                {
                    "$group": {
                        "_id": None,
                        "avg_num_scores": {"$avg": "$num_scores"},
                    }
                },
            ]
        )

        avg_value_agg = [doc async for doc in avg_value_agg_cursor]
        avg_num_scores = avg_value_agg[0].get("avg_num_scores", 0)

        aggregation_cursor = collection.aggregate(
            [
                {"$match": {"is_deleted": False}},
                {
                    "$group": {
                        "_id": "$film_id",
                        "avg_score": {"$avg": "$score"},
                        "num_scores": {"$sum": 1},
                    }
                },
                {"$match": {"num_scores": {"$gte": avg_num_scores}}},
                {"$sort": {"avg_score": -1}},
                {"$limit": limit},
            ]
        )

        return [
            FilmAvgScore(
                film_id=doc["_id"],
                avg_score=doc["avg_score"],
                num_scores=doc["num_scores"],
            )
            async for doc in aggregation_cursor
        ]

    def get_films_watching_now(self, table_name: str):
        collection = self._db[table_name]
        return collection.aggregate(
            [
                {"$group": {"_id": "$film_id", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
        )
