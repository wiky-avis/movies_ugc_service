import logging

from starlette.responses import JSONResponse

from src.brokers.base import BaseProducer
from src.repositories.base import BaseRepository
from src.services.base import BaseService


logger = logging.getLogger(__name__)


class UserFilmScoresService(BaseService):
    def __init__(self, producer: BaseProducer, repository: BaseRepository):
        self._producer = producer
        self._repository = repository

    async def send(self, key: bytes, value: bytes) -> None:
        await self._producer.send(key=key, value=value)

    async def send_event(
        self, score_data: dict, event_type: str
    ) -> JSONResponse:
        return JSONResponse("ok")

    async def set_score(self, score_data: dict) -> None:
        pass

    async def delete_score(self, score_data: dict) -> None:
        pass

    async def get_score(self, score_data: dict) -> JSONResponse:
        return JSONResponse("ok")
