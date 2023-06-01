# mypy: disable-error-code="attr-defined"
import logging
from datetime import datetime
from http import HTTPStatus

import dpath
import orjson
from fastapi import HTTPException
from fastapi_pagination import paginate
from pymongo import ASCENDING
from pymongo.errors import ServerSelectionTimeoutError
from starlette.responses import JSONResponse

from src.api.v1.models.film_reviews import ReviewList
from src.brokers.base import BaseProducer
from src.brokers.exceptions import ProducerError
from src.brokers.models import FilmReviewEventModel
from src.repositories.base import BaseRepository
from src.services.base import BaseService


logger = logging.getLogger(__name__)


class UserFilmReviewsService(BaseService):
    def __init__(self, producer: BaseProducer, repository: BaseRepository):
        self._producer = producer
        self._repository = repository

    async def send(self, key: bytes, value: bytes) -> None:
        await self._producer.send(key=key, value=value)

    async def send_film_review(self, data: dict) -> JSONResponse:
        user_id = dpath.get(data, "user_id", default=None)
        film_id = dpath.get(data, "film_id", default=None)
        review_id = dpath.get(data, "review_id", default=None)
        review_title = dpath.get(data, "review_title", default=None)
        review_body = dpath.get(data, "review_body", default=None)
        if not user_id or not film_id or not review_title or not review_body:
            logger.warning(
                "Error send new_film_review: user_id %s film_id %s.",
                user_id,
                film_id,
            )
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Error sending the event",
            )

        film_review = FilmReviewEventModel(
            user_id=user_id,  # type: ignore[arg-type]
            film_id=film_id,  # type: ignore[arg-type]
            review_id=review_id,  # type: ignore[arg-type]
            review_title=review_title,  # type: ignore[arg-type]
            review_body=review_body,  # type: ignore[arg-type]
            ts=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )

        try:
            key = f"{film_id}:{user_id}".encode("utf-8")
            await self.send(
                value=orjson.dumps(film_review.dict()),
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

    async def get_film_reviews(self, film_id: str):
        table_name = "user_film_reviews"
        result = [
            ReviewList(
                review_id=doc["review_id"],
                user_id=doc["user_id"],
                review_title=doc["review_title"],
                review_body=doc["review_body"],
            )
            async for doc in self._repository.find(
                filter_=dict(film_id=film_id),
                columns={},
                table_name=table_name,
            ).sort("_id", ASCENDING)
        ]
        return paginate(sequence=result)

    async def create_film_review(self, data: dict) -> None:
        table_name = "user_film_reviews"
        user_id = dpath.get(data, "user_id", default=None)
        film_id = dpath.get(data, "film_id", default=None)
        review_id = dpath.get(data, "review_id", default=None)
        review_title = dpath.get(data, "review_title", default=None)
        review_body = dpath.get(data, "review_body", default=None)
        if not user_id or not film_id or not review_title or not review_body:
            logger.warning(
                "Error insert user's film review: table_name %s user_id %s film_id %s.",
                table_name,
                user_id,
                film_id,
            )
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Error save film review",
            )

        if await self._repository.find_one(
            dict(film_id=film_id, user_id=user_id), table_name
        ):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="User has already written a review for this film",
            )

        query = dict(
            film_id=film_id,
            user_id=user_id,
            review_id=review_id,
            review_title=review_title,
            review_body=review_body,
        )
        try:
            await self._repository.insert_one(
                data=query,
                table_name=table_name,
            )
        except ServerSelectionTimeoutError:
            logger.error(
                "MongoDb Error. Failed to create a user's film review: filter_query %s, table_name %s",
                query,
                table_name,
                exc_info=True,
            )
