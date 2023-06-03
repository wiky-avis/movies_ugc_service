# mypy: disable-error-code="attr-defined"
import logging
from datetime import datetime
from http import HTTPStatus

import orjson
from bson import json_util
from fastapi import HTTPException
from pymongo.errors import ServerSelectionTimeoutError
from starlette.responses import JSONResponse

from src.api.v1.models.film_scores import (
    FilmAvgScore,
    ScoreEventType,
    UserFilmScore,
)
from src.brokers.base import BaseProducer
from src.brokers.exceptions import ProducerError
from src.repositories.base import BaseRepository
from src.services.base import BaseService
from src.settings.kafka import kafka_topic_names


logger = logging.getLogger(__name__)


class UserFilmScoresService(BaseService):
    def __init__(self, producer: BaseProducer, repository: BaseRepository):
        self._producer = producer
        self._repository = repository
        self.db_table_name = "film_scores"

    async def send(
        self,
        key: bytes,
        value: bytes,
        topic: str = kafka_topic_names.film_score_topic,
    ) -> None:
        await self._producer.send(key=key, value=value, topic=topic)

    async def send_event(
        self, score_data: UserFilmScore, event_type: ScoreEventType
    ) -> JSONResponse:
        film_score = dict(
            user_id=score_data.user_id,
            film_id=score_data.film_id,
            score=int(score_data.score),
            event_type=event_type,
            ts=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )

        try:
            key = f"{score_data.film_id}:{score_data.user_id}".encode("utf-8")
            await self.send(
                value=orjson.dumps(film_score),
                key=key,
            )
        except ProducerError:
            logger.warning(
                "Error send new_film_score - ProducerError: user_id %s film_id %s score %s event_type %s.",
                score_data.user_id,
                score_data.film_id,
                score_data.score,
                event_type,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error sending the event",
            )

        return JSONResponse(content={"result": "Ok."})

    async def set_score(self, score_data: UserFilmScore) -> None:
        filter_ = dict(film_id=score_data.film_id, user_id=score_data.user_id)
        document = dict(
            film_id=score_data.film_id,
            user_id=score_data.user_id,
            score=int(score_data.score),
            is_deleted=False,
        )
        try:
            await self._repository.upsert(
                filter_=filter_,
                document=document,
                table_name=self.db_table_name,
            )
        except ServerSelectionTimeoutError:
            logger.error(
                "MongoDb Error. Failed set film score: filter_query %s, document %s, table_name %s",
                filter_,
                document,
                self.db_table_name,
                exc_info=True,
            )

    async def delete_score(self, score_data: UserFilmScore) -> None:
        filter_query = dict(
            film_id=score_data.film_id, user_id=score_data.user_id
        )
        if await self._repository.find_one(filter_query, self.db_table_name):
            try:
                await self._repository.update_one(
                    filter_=filter_query,
                    key="is_deleted",
                    value=True,
                    table_name=self.db_table_name,
                )
            except ServerSelectionTimeoutError:
                logger.error(
                    "MongoDb Error. Failed to deleted a user film score: filter_query %s, table_name %s",
                    filter_query,
                    self.db_table_name,
                    exc_info=True,
                )
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Internal Server error",
                )
        else:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Score for provided film and user wes not found",
            )

    async def get_user_score(self, user_id: str, film_id: str) -> JSONResponse:
        filter_ = dict(user_id=user_id, film_id=film_id, is_deleted=False)

        result = await self._repository.find_one(filter_, self.db_table_name)

        if not result:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Did not find score for provided user and film",
            )

        return JSONResponse(content=json_util.dumps(result))

    async def get_top_scores(self, limit: int = 10) -> list[FilmAvgScore]:
        return await self._repository.aggregate_top_films_by_score(
            self.db_table_name, limit
        )
