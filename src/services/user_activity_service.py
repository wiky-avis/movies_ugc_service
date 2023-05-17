import logging
from datetime import datetime
from http import HTTPStatus
from typing import NoReturn

import orjson
from fastapi import HTTPException
from starlette.responses import JSONResponse

from src.api.v1.models.view_progress import ViewProgress
from src.brokers.base import BaseProducer
from src.brokers.exceptions import ProducerError
from src.brokers.models import UserViewProgressEventModel
from src.repositories.base import BaseRepository
from src.services.base import BaseService


logger = logging.getLogger(__name__)


class UserActivityService(BaseService):
    def __init__(self, producer: BaseProducer, repository: BaseRepository):
        self._producer = producer
        self._repository = repository

    async def send(self, key: bytes, value: bytes) -> NoReturn:
        await self._producer.send(key=key, value=value)

    async def send_view_progress(
        self, film_id: str, viewed_frame: int, user_id: str
    ) -> NoReturn:
        view_progress = UserViewProgressEventModel(
            user_id=user_id,
            film_id=film_id,
            viewed_frame=viewed_frame,
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

    async def insert_or_update_view_progress(self, data: dict):
        table_name = "view_progress"
        filter_query = {
            "film_id": data.get("film_id"),
            "user_id": data.get("user_id"),
        }

        if await self._repository.find_one(
            filter_=filter_query, table_name=table_name
        ):
            await self._repository.update_one(
                filter_=filter_query,
                key="viewed_frame",
                value=data.get("viewed_frame"),
                table_name=table_name,
            )
        else:
            await self._repository.insert_one(data=data, table_name=table_name)

    async def get_last_view_progress(self, filter_query: dict):
        table_name = "view_progress"

        user_view_progress = await self._repository.find_one(
            filter_query, table_name
        )
        if not user_view_progress:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User has no saved progress",
            )
        return ViewProgress(**user_view_progress)
