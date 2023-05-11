import logging
from typing import NoReturn

from aiokafka import AIOKafkaProducer, errors

from src.brokers.base import BaseProducer
from src.brokers.exceptions import ProducerError
from src.settings.kafka import KafkaProduserSettings


logger = logging.getLogger(__name__)


class KafkaProducer(BaseProducer):
    config = KafkaProduserSettings()
    kafka_producer = None

    @classmethod
    async def setup(cls):
        cls.kafka_producer = AIOKafkaProducer(
            bootstrap_servers='broker:9092'
        )
        await cls.kafka_producer.start()

    @classmethod
    async def close(cls):
        if cls.kafka_producer:
            await cls.kafka_producer.stop()
            cls._producer = None

    async def send(self, key: bytes, value: bytes) -> NoReturn:
        try:
            await self.kafka_producer.send_and_wait(
                topic=self.config.topic_name, key=key, value=value
            )
        except errors.KafkaError:
            logger.exception(
                "Error sending the event: topic_name %s",
                self.config.topic_name,
                exc_info=True,
            )
            raise ProducerError
