import logging
from datetime import datetime
from http import HTTPStatus

import orjson
from fastapi import HTTPException
from starlette.responses import JSONResponse

from src.api.v1.models.scores import ScoreEventType, UserFilmScore
from src.brokers.base import BaseProducer
from src.brokers.exceptions import ProducerError
from src.repositories.base import BaseRepository
from src.services.base import BaseService
from src.settings.kafka import kafka_producer_settings


logger = logging.getLogger(__name__)


class UserFilmScoresService(BaseService):
    def __init__(self, producer: BaseProducer, repository: BaseRepository):
        self._producer = producer
        self._repository = repository

    async def send(
        self,
        key: bytes,
        value: bytes,
        topic: str = kafka_producer_settings.film_score_topic,
    ) -> None:
        await self._producer.send(key=key, value=value, topic=topic)

    async def send_event(
        self, score_data: dict, event_type: ScoreEventType
    ) -> JSONResponse:
        user_id = score_data.get("user_id")
        film_id = score_data.get("film_id")
        score = score_data.get("score")
        if not user_id or not film_id or not score:
            logger.warning(
                "Error send new_bookmark: user_id %s film_id %s score %s event_type %s.",
                user_id,
                film_id,
                score,
                event_type,
            )
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Error sending the event",
            )

        film_score = UserFilmScore(
            user_id=user_id,
            film_id=film_id,
            score=int(score),
            event_type=event_type,
            ts=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )

        try:
            key = f"{film_id}:{user_id}".encode("utf-8")
            await self.send(
                value=orjson.dumps(film_score.dict()),
                key=key,
            )
        except ProducerError:
            logger.warning(
                "Error send new_bookmark: user_id %s film_id %s score %s event_type %s.",
                user_id,
                film_id,
                score,
                event_type,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error sending the event",
            )

        return JSONResponse(content={"result": "Ok."})

    async def set_score(self, score_data: dict) -> None:
        pass

    async def delete_score(self, score_data: dict) -> None:
        pass

    async def get_score(self, score_data: dict) -> JSONResponse:
        return JSONResponse("ok")
