import json
import logging
from datetime import datetime
from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, HTTPException

from src.brokers.exceptions import ProducerError
from src.brokers.kafka_producer import KafkaProducer
from src.services.base import BaseService


logger = logging.getLogger(__name__)


class UserActivityService(BaseService):
    def __init__(self, producer: KafkaProducer):
        self._producer = producer

    async def send(self, key, value):
        await self._producer.send(key=key, value=value)

    async def save_view_progress(self, user_id, film_id, value):
        value = {
            "user_id": user_id,
            "film_id": film_id,
            "viewed_frame": value,
            "event_time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        }

        try:
            key = f"{film_id}:{user_id}".encode("utf-8")
            await self.send(
                value=json.dumps(value, ensure_ascii=False).encode("utf-8"),
                key=key,
            )
        except ProducerError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error sending the event",
            )


@lru_cache()
def user_activity_service(
    producer: KafkaProducer = Depends(KafkaProducer),
) -> UserActivityService:
    return UserActivityService(producer)
