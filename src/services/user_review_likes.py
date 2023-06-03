import logging
from http import HTTPStatus

import dpath
from fastapi import HTTPException
from pymongo.errors import ServerSelectionTimeoutError
from starlette.responses import JSONResponse

from src.api.v1.models.review_likes import ReviewLikeModel
from src.brokers.base import BaseProducer
from src.repositories.base import BaseRepository
from src.services.base import BaseService


logger = logging.getLogger(__name__)


class UserReviewLikesService(BaseService):
    def __init__(self, producer: BaseProducer, repository: BaseRepository):
        self._producer = producer
        self._repository = repository

    async def send(self, key: bytes, value: bytes) -> None:
        await self._producer.send(key=key, value=value)

    async def send_event_review_like(self, data: dict) -> JSONResponse:
        pass

    async def add_like(self, like_data: ReviewLikeModel) -> None:
        film_reviews_table_name = "user_film_reviews"
        review_likes_table_name = "user_film_reviews_likes"
        review = await self._repository.find_one(
                filter_=dict(review_id=like_data.review_id),
                table_name=film_reviews_table_name,
        )
        if not review:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Review not found.",
            )

        try:
            await self._repository.update_one(
                filter_=dict(review_id=like_data.review_id),
                key="dislikes",
                value=1,
                table_name=film_reviews_table_name,
                method="$inc"
            )
            await self._repository.insert_one(
                data=dict(review_id=like_data.review_id, user_id=like_data.user_id, event_type=like_data.event_type),
                table_name=review_likes_table_name,
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

    async def add_dislike(self, like_data: ReviewLikeModel) -> None:
        table_name = "user_film_reviews"
        review = await self._repository.find_one(
            filter_=dict(review_id=like_data.review_id),
            table_name=table_name,
        )
        if not review:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Review not found.",
            )

        try:
            await self._repository.update_one(
                filter_=dict(review_id=like_data.review_id),
                key="likes",
                value=1,
                table_name=table_name,
                method="$inc"
            )
        except ServerSelectionTimeoutError:
            logger.error(
                "MongoDb Error. Failed to add like for review: review_id %s, table_name %s.",
                like_data.review_id,
                table_name,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error add like.",
            )
