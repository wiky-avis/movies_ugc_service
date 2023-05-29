# mypy: disable-error-code="attr-defined"
import logging
from datetime import datetime
from http import HTTPStatus
from typing import Optional

import dpath
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


logger = logging.getLogger(__name__)


class UserViewHistoryService(BaseService):
    def __init__(self, producer: BaseProducer, repository: BaseRepository):
        self._producer = producer
        self._repository = repository

    async def send(self, key: bytes, value: bytes) -> None:
        await self._producer.send(key=key, value=value)

    async def send_view_progress(self, data: dict) -> JSONResponse:
        user_id = dpath.get(data, "user_id", default=None)
        film_id = dpath.get(data, "film_id", default=None)
        viewed_frame = dpath.get(data, "viewed_frame", default=None)
        if not user_id or not film_id or not viewed_frame:
            logger.warning(
                "Error send view_progress: user_id %s film_id %s.",
                user_id,
                film_id,
            )
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Error sending the event",
            )

        view_progress = UserViewProgressEventModel(
            user_id=user_id,  # type: ignore[arg-type]
            film_id=film_id,  # type: ignore[arg-type]
            viewed_frame=viewed_frame,  # type: ignore[arg-type]
            ts=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )

        try:
            key = f"{film_id}:{user_id}".encode("utf-8")
            await self.send(
                value=orjson.dumps(view_progress.dict()),
                key=key,
            )
        except ProducerError:
            logger.warning(
                "Error sending the event: film_id %s user_id %s",
                film_id,
                user_id,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error sending the event",
            )

        return JSONResponse(content={"result": "Ok."})

    async def insert_or_update_view_progress(self, data: dict) -> None:
        table_name = "view_progress"
        user_id = dpath.get(data, "user_id", default=None)
        film_id = dpath.get(data, "film_id", default=None)
        viewed_frame = dpath.get(data, "viewed_frame", default=None)
        if not user_id or not film_id or not viewed_frame:
            logger.warning(
                "Error insert or update view_progress: table_name %s user_id %s film_id %s.",
                table_name,
                user_id,
                film_id,
            )
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Error save view_progress",
            )

        filter_query = dict(film_id=film_id, user_id=user_id)
        try:
            await self._repository.upsert(
                filter_=filter_query,
                key="viewed_frame",
                value=viewed_frame,
                table_name=table_name,
            )
        except ServerSelectionTimeoutError:
            logger.error(
                "MongoDb Error. Failed to create or update a user view progress: filter_query %s, table_name %s",
                filter_query,
                table_name,
                exc_info=True,
            )

    async def get_last_view_progress(
        self, filter_query: dict
    ) -> Optional[ViewProgress]:
        table_name = "view_progress"

        user_view_progress = await self._repository.find_one(
            filter_query, table_name
        )
        if not user_view_progress:
            logger.warning(
                "View_progress not found: table_name %s filter_query %s.",
                table_name,
                filter_query,
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User has no saved progress",
            )
        return ViewProgress(**user_view_progress)

    async def get_films_ids_watching_now(self):
        table_name = "view_progress"

        result = [
            FilmView(film_id=doc["_id"], count=doc["count"])
            async for doc in self._repository.get_films_watching_now(
                table_name=table_name
            )
        ]
        return paginate(sequence=result)
