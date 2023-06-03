import logging
from datetime import datetime
from http import HTTPStatus

import orjson
from fastapi import HTTPException
from pymongo.errors import ServerSelectionTimeoutError
from starlette.responses import JSONResponse

from src.api.v1.models.review_likes import ReviewLikeModel
from src.brokers.base import BaseProducer
from src.brokers.exceptions import ProducerError
from src.brokers.models import UserReviewLikeEventModel
from src.repositories.base import BaseRepository
from src.services.base import BaseService
from src.settings import kafka_topic_names


logger = logging.getLogger(__name__)


class UserReviewLikesService(BaseService):
    def __init__(self, producer: BaseProducer, repository: BaseRepository):
        self._producer = producer
        self._repository = repository
        self._film_reviews_table_name = "user_film_reviews"
        self._review_likes_table_name = "user_film_reviews_likes"

    async def send(
        self,
        key: bytes,
        value: bytes,
        topic: str = kafka_topic_names.film_reviews_likes_topic,
    ) -> None:
        await self._producer.send(key=key, value=value)

    async def send_event_review_like(
        self, like_data: ReviewLikeModel
    ) -> JSONResponse:
        review_like_data = UserReviewLikeEventModel(
            user_id=like_data.user_id,
            review_id=like_data.review_id,
            action=like_data.event_type,
            ts=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )

        try:
            key = f"{like_data.review_id}:{like_data.user_id}".encode("utf-8")
            await self.send(
                value=orjson.dumps(review_like_data.dict()),
                key=key,
            )
        except ProducerError:
            logger.warning(
                "Error sending the event: review_id %s user_id %s.",
                like_data.review_id,
                like_data.user_id,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error sending the event.",
            )

        return JSONResponse(content={"result": "Ok."})

    async def add_like(self, like_data: ReviewLikeModel) -> None:
        review = await self._repository.find_one(
            filter_=dict(review_id=like_data.review_id),
            table_name=self._film_reviews_table_name,
        )
        if not review:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Review not found.",
            )
        if await self._repository.find_one(
            dict(
                review_id=like_data.review_id,
                user_id=like_data.user_id,
                event_type=like_data.event_type,
            ),
            self._review_likes_table_name,
        ):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="The user has already liked the review.",
            )

        try:
            await self._repository.update_one(
                filter_=dict(review_id=like_data.review_id),
                key="likes",
                value=1,
                table_name=self._film_reviews_table_name,
                method="$inc",
            )
            await self._repository.insert_one(
                data=dict(
                    review_id=like_data.review_id,
                    user_id=like_data.user_id,
                    event_type=like_data.event_type,
                ),
                table_name=self._review_likes_table_name,
            )
        except ServerSelectionTimeoutError:
            logger.error(
                "MongoDb Error. Failed to add like for review: review_id %s.",
                like_data.review_id,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error add like.",
            )

    async def add_dislike(self, like_data: ReviewLikeModel) -> None:
        review = await self._repository.find_one(
            filter_=dict(review_id=like_data.review_id),
            table_name=self._film_reviews_table_name,
        )
        if not review:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Review not found.",
            )
        if await self._repository.find_one(
            dict(
                review_id=like_data.review_id,
                user_id=like_data.user_id,
                event_type=like_data.event_type,
            ),
            self._review_likes_table_name,
        ):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="The user has already disliked the review.",
            )

        try:
            await self._repository.update_one(
                filter_=dict(review_id=like_data.review_id),
                key="dislikes",
                value=1,
                table_name=self._film_reviews_table_name,
                method="$inc",
            )
            await self._repository.insert_one(
                data=dict(
                    review_id=like_data.review_id,
                    user_id=like_data.user_id,
                    event_type=like_data.event_type,
                ),
                table_name=self._review_likes_table_name,
            )
        except ServerSelectionTimeoutError:
            logger.error(
                "MongoDb Error. Failed to add dislike for review: review_id %s.",
                like_data.review_id,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error add dislike.",
            )
