import logging
from datetime import datetime
from http import HTTPStatus

import orjson
from fastapi import HTTPException
from pymongo.errors import ServerSelectionTimeoutError
from starlette.responses import JSONResponse

from src.api.v1.models.bookmarks import UserBookmarkModel
from src.brokers.base import BaseProducer
from src.brokers.exceptions import ProducerError
from src.brokers.models import UserBookmarkEventModel
from src.repositories.base import BaseRepository
from src.services.base import BaseService
from src.settings.kafka import kafka_topic_names


logger = logging.getLogger(__name__)


class UserBookmarksService(BaseService):
    def __init__(self, producer: BaseProducer, repository: BaseRepository):
        self._producer = producer
        self._repository = repository
        self._table_name = "user_bookmarks"

    async def send(
        self,
        key: bytes,
        value: bytes,
        topic: str = kafka_topic_names.bookmarks_topic,
    ) -> None:
        await self._producer.send(key=key, value=value, topic=topic)

    async def send_event_bookmark(
        self, bookmark_data: UserBookmarkModel
    ) -> JSONResponse:
        view_progress = UserBookmarkEventModel(
            user_id=bookmark_data.user_id,  # type: ignore[arg-type]
            film_id=bookmark_data.film_id,  # type: ignore[arg-type]
            event_type=bookmark_data.event_type,  # type: ignore[arg-type]
            ts=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )

        try:
            key = f"{bookmark_data.film_id}:{bookmark_data.user_id}".encode(
                "utf-8"
            )
            await self.send(
                value=orjson.dumps(view_progress.dict()),
                key=key,
            )
        except ProducerError:
            logger.warning(
                "Error sending the event for bookmarks: film_id %s user_id %s event_type %s.",
                bookmark_data.film_id,
                bookmark_data.user_id,
                bookmark_data.event_type,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error sending the event.",
            )

        return JSONResponse(content={"result": "Ok."})

    async def create_bookmark(self, bookmark_data: UserBookmarkModel) -> None:
        query = dict(
            film_id=bookmark_data.film_id,
            user_id=bookmark_data.user_id,
            is_deleted=False,
        )
        try:
            await self._repository.insert_one(
                data=query,
                table_name=self._table_name,
            )
        except ServerSelectionTimeoutError:
            logger.error(
                "MongoDb Error. Failed to create a user bookmark: filter_query %s, table_name %s.",
                query,
                self._table_name,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error create bookmark.",
            )

    async def delete_bookmark(self, bookmark_data: UserBookmarkModel) -> None:
        filter_query = dict(
            film_id=bookmark_data.film_id, user_id=bookmark_data.user_id
        )
        if not await self._repository.find_one(filter_query, self._table_name):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Error delete bookmark. Bookmark not found.",
            )

        try:
            await self._repository.update_one(
                filter_=filter_query,
                key="is_deleted",
                value=True,
                table_name=self._table_name,
            )
        except ServerSelectionTimeoutError:
            logger.error(
                "MongoDb Error. Failed to deleted a user bookmark: filter_query %s, table_name %s.",
                filter_query,
                self._table_name,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error delete bookmark.",
            )

    async def get_bookmarks_by_user_id(self, user_id: str) -> list[str]:
        filter_ = dict(user_id=user_id, is_deleted=False)
        result = [
            doc["film_id"]
            async for doc in self._repository.find(
                filter_, {"film_id": 1}, self._table_name
            )
        ]
        return result
