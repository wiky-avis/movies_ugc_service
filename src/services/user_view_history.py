# mypy: disable-error-code="attr-defined"
import logging
from datetime import datetime
from http import HTTPStatus
from typing import Optional

import orjson
from fastapi import HTTPException
from fastapi_pagination import paginate
from pymongo.errors import ServerSelectionTimeoutError
from starlette.responses import JSONResponse

from src.api.v1.models.view_progress import FilmView, ViewProgress
from src.brokers.base import BaseProducer
from src.brokers.exceptions import ProducerError
from src.brokers.models import UserViewProgressEventModel
from src.repositories.base import BaseRepository
from src.services.base import BaseService
from src.settings.kafka import kafka_topic_names


logger = logging.getLogger(__name__)


class UserViewHistoryService(BaseService):
    def __init__(self, producer: BaseProducer, repository: BaseRepository):
        self._producer = producer
        self._repository = repository
        self._table_name = "view_progress"

    async def send(
        self,
        key: bytes,
        value: bytes,
        topic: str = kafka_topic_names.view_progress_topic,
    ) -> None:
        await self._producer.send(key=key, value=value, topic=topic)

    async def send_view_progress(
        self, view_progress_data: ViewProgress
    ) -> JSONResponse:
        view_progress = UserViewProgressEventModel(
            user_id=view_progress_data.user_id,
            film_id=view_progress_data.film_id,
            viewed_frame=view_progress_data.viewed_frame,
            ts=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )

        try:
            key = f"{view_progress_data.film_id}:{view_progress_data.user_id}".encode(
                "utf-8"
            )
            await self.send(
                value=orjson.dumps(view_progress.dict()),
                key=key,
            )
        except ProducerError:
            logger.warning(
                "Error sending the event: film_id %s user_id %s.",
                view_progress_data.film_id,
                view_progress_data.user_id,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error sending the event.",
            )

        return JSONResponse(content={"result": "Ok."})

    async def insert_or_update_view_progress(
        self, view_progress_data: ViewProgress
    ) -> None:
        filter_query = dict(
            film_id=view_progress_data.film_id,
            user_id=view_progress_data.user_id,
        )
        try:
            await self._repository.upsert(
                filter_=filter_query,
                document={"viewed_frame": view_progress_data.viewed_frame},
                table_name=self._table_name,
            )
        except ServerSelectionTimeoutError:
            logger.error(
                "MongoDb Error. Failed to create or update a user view progress: filter_query %s, table_name %s.",
                filter_query,
                self._table_name,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error insert or update view progress.",
            )

    async def get_last_view_progress(
        self, filter_query: dict
    ) -> Optional[ViewProgress]:
        user_view_progress = await self._repository.find_one(
            filter_query, self._table_name
        )
        if not user_view_progress:
            logger.warning(
                "View_progress not found: table_name %s filter_query %s.",
                self._table_name,
                filter_query,
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User has no saved progress.",
            )
        return ViewProgress(**user_view_progress)

    async def get_films_ids_watching_now(self):
        result = [
            FilmView(film_id=doc["_id"], count=doc["count"])
            async for doc in self._repository.get_films_watching_now(
                table_name=self._table_name
            )
        ]
        return paginate(sequence=result)
