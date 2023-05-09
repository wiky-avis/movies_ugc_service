import logging

from aiokafka import AIOKafkaConsumer, errors

from src.brokers.base import BaseConsumer
from src.brokers.exceptions import ProducerError
from src.brokers.kafka_producer import BaseKafkaSettings


class KafkaConsumerSettings(BaseKafkaSettings):
    topic_name: str = "my_topic"
    timeout_ms: int = 10 * 1000
    max_records: int = 10


logger = logging.getLogger(__name__)


class KafkaConsumer(BaseConsumer):
    config = KafkaConsumerSettings()
    kafka_consumer = None

    async def start(self):
        self.kafka_consumer = AIOKafkaConsumer(
            self.config.topic_name,
            bootstrap_servers=self.config.bootstrap_servers,
        )
        await self.kafka_consumer.start()

    async def stop(self):
        if self.kafka_consumer:
            await self.kafka_consumer.stop()
            self.kafka_consumer = None

    async def consume(self):
        await self.start()

        retrieved_requests = []
        try:
            result = await self.kafka_consumer.getmany(
                timeout_ms=self.config.timeout_ms,
                max_records=self.config.max_records,
            )
            for tp, messages in result.items():
                if messages:
                    for message in messages:
                        retrieved_requests.append(
                            {
                                "key": message.key.decode("utf-8"),
                                "value": message.value.decode("utf-8"),
                            }
                        )

            return retrieved_requests
        except errors.KafkaError:
            logger.error(
                f"Error when receiving events for topic %s",
                self.config.topic_name,
                exc_info=True,
            )
            raise ProducerError
        finally:
            await self.stop()
