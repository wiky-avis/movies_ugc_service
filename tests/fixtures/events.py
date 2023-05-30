import pytest_asyncio
from aiokafka import AIOKafkaConsumer

from src.settings.kafka import KafkaConsumerSettings, kafka_consumer_settings


@pytest_asyncio.fixture(scope="session")
async def event_consumer(event_loop, consumer_settings):
    consumer_settings: KafkaConsumerSettings = kafka_consumer_settings

    consumer = AIOKafkaConsumer(
        consumer_settings.default_topic_name,
        loop=event_loop,
        bootstrap_servers=consumer_settings.bootstrap_servers,
        auto_offset_reset="latest",
    )
    await consumer.start()
    yield consumer
    await consumer.stop()
