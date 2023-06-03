# mypy: disable-error-code="attr-defined"
import logging
from http import HTTPStatus

import orjson
from fastapi import HTTPException
from fastapi_pagination import paginate
from pymongo.errors import ServerSelectionTimeoutError
from starlette.responses import JSONResponse

from src.api.v1.models.film_reviews import ReviewModel
from src.brokers.base import BaseProducer
from src.brokers.exceptions import ProducerError
from src.brokers.models import FilmReviewEventModel
from src.repositories.base import BaseRepository
from src.services.base import BaseService
from src.settings.kafka import kafka_topic_names


logger = logging.getLogger(__name__)


class UserFilmReviewsService(BaseService):
    def __init__(self, producer: BaseProducer, repository: BaseRepository):
        self._producer = producer
        self._repository = repository

    async def send(
        self,
        key: bytes,
        value: bytes,
        topic: str = kafka_topic_names.film_reviews_topic,
    ) -> None:
        await self._producer.send(key=key, value=value, topic=topic)

    async def send_film_review(self, review: ReviewModel) -> JSONResponse:
        film_review = FilmReviewEventModel(
            user_id=review.user_id,
            film_id=review.film_id,  # type: ignore[arg-type]
            review_id=review.review_id,
            review_title=review.review_title,
            review_body=review.review_body,
            ts=review.created_dt,
        )

        try:
            key = f"{review.film_id}:{review.user_id}".encode("utf-8")
            await self.send(
                value=orjson.dumps(film_review.dict()),
                key=key,
            )
        except ProducerError:
            logger.warning(
                "Error sending the event: film_id %s user_id %s.",
                review.film_id,
                review.user_id,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error sending the event.",
            )

        return JSONResponse(content={"result": "Ok."})

    async def get_film_reviews(self, film_id: str):
        table_name = "user_film_reviews"
        result = [
            ReviewModel(
                review_id=doc["review_id"],
                user_id=doc["user_id"],
                review_title=doc["review_title"],
                review_body=doc["review_body"],
                created_dt=doc["created_dt"],
                likes=doc["likes"],
                dislikes=doc["dislikes"],
            )
            async for doc in self._repository.find(
                filter_=dict(film_id=film_id),
                columns={},
                table_name=table_name,
            ).sort("created_dt", -1)
        ]
        return paginate(sequence=result)

    async def create_film_review(self, review: ReviewModel) -> None:
        table_name = "user_film_reviews"

        if await self._repository.find_one(
            dict(film_id=review.film_id, user_id=review.user_id), table_name
        ):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="User has already written a review for this film.",
            )

        query = review.dict(exclude_none=True)
        try:
            await self._repository.insert_one(
                data=query,
                table_name=table_name,
            )
        except ServerSelectionTimeoutError:
            logger.error(
                "MongoDb Error. Failed to create a user's film review: filter_query %s, table_name %s.",
                query,
                table_name,
                exc_info=True,
            )
