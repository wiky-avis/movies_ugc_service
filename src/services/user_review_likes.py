import logging

import dpath
from starlette.responses import JSONResponse

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

    async def add_like(self, data: dict) -> None:
        table_name = "user_film_reviews"
        review_id = dpath.get(data, "review_id", default=None)
        review = await self._repository.find_one(
                filter_=dict(review_id=review_id),
                columns={},
                table_name=table_name,
        )

    async def add_dislike(self, data: dict) -> None:
        table_name = "user_film_reviews"
        review_id = dpath.get(data, "review_id", default=None)
        review = await self._repository.find_one(
            filter_=dict(review_id=review_id),
            columns={},
            table_name=table_name,
        )
