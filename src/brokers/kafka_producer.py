import logging

import backoff
from aiokafka import AIOKafkaProducer, errors

from src.brokers.base import BaseProducer
from src.brokers.exceptions import ProducerError
from src.settings.kafka import KafkaProducerSettings, kafka_producer_settings


logger = logging.getLogger(__name__)


class KafkaProducer(BaseProducer):
    config: KafkaProducerSettings = kafka_producer_settings
    kafka_producer: AIOKafkaProducer = None

    @classmethod
    @backoff.on_exception(
        backoff.expo, errors.KafkaConnectionError, max_time=60
    )
    async def setup(cls):
        cls.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=cls.config.bootstrap_servers
        )
        await cls.kafka_producer.start()

    @classmethod
    async def close(cls):
        if cls.kafka_producer:
            await cls.kafka_producer.stop()
            cls._producer = None

    async def send(
        self,
        key: bytes,
        value: bytes,
        topic: str = kafka_producer_settings.default_topic_name,
    ) -> None:
        try:
            await self.kafka_producer.send_and_wait(
                topic=topic, key=key, value=value
            )
        except errors.KafkaError:
            logger.exception(
                "Error sending the event: topic_name %s",
                topic,
                exc_info=True,
            )
            raise ProducerError
