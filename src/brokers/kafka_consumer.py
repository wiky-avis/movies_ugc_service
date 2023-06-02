import asyncio
import logging
from typing import Dict, List, Optional

import orjson
from aiokafka import AIOKafkaConsumer, ConsumerRecord, errors
from kafka import TopicPartition

from src.brokers.base import BaseConsumer
from src.brokers.exceptions import ConsumerError
from src.settings.kafka import KafkaConsumerSettings, kafka_consumer_settings


logger = logging.getLogger(__name__)


class KafkaConsumer(BaseConsumer):
    config: KafkaConsumerSettings = kafka_consumer_settings
    kafka_consumer: AIOKafkaConsumer = None
    topic_name: str = kafka_consumer_settings.default_topic_name

    async def start(self, topic_name: Optional[str] = None):
        if topic_name:
            self.topic_name = topic_name

        loop = asyncio.get_event_loop()
        self.kafka_consumer = AIOKafkaConsumer(
            self.topic_name,
            loop=loop,
            bootstrap_servers=self.config.bootstrap_servers,
            auto_offset_reset="earliest",
        )
        await self.kafka_consumer.start()

    async def stop(self):
        if self.kafka_consumer:
            await self.kafka_consumer.stop()
            self.kafka_consumer = None

    @staticmethod
    def deserialize(record: ConsumerRecord) -> dict:
        return orjson.loads(record.value)

    async def consume(self) -> list[dict]:
        await self.start()
        partition: TopicPartition = list(self.kafka_consumer.assignment())[0]
        await self.kafka_consumer.seek_to_end(partition)

        retrieved_events = []
        while True:
            try:
                response: Dict[
                    TopicPartition, List[ConsumerRecord]
                ] = await self.kafka_consumer.getmany(
                    partition,
                    timeout_ms=self.config.timeout_ms,
                    max_records=self.config.max_records,
                )
                if partition in response:
                    for record in response[partition]:
                        retrieved_events.append(
                            dict(
                                key=record.key.decode("utf-8"),
                                value=self.deserialize(record),
                            )
                        )

            except errors.KafkaError:
                logger.error(
                    "Error when receiving events for topic %s",
                    self.topic_name,
                    exc_info=True,
                )
                raise ConsumerError
            finally:
                await self.stop()
                return retrieved_events
