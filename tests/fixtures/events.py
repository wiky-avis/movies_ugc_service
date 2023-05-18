import pytest_asyncio
from aiokafka import AIOKafkaConsumer

from src.settings.kafka import KafkaConsumerSettings


@pytest_asyncio.fixture(scope="session")
async def event_consumer(event_loop, consumer_settings):
    consumer_settings = KafkaConsumerSettings()

    consumer = AIOKafkaConsumer(
        consumer_settings.topic_name,
        loop=event_loop,
        bootstrap_servers=consumer_settings.bootstrap_servers,
        auto_offset_reset="latest",
        enable_auto_commit=False,
    )
    await consumer.start()
    yield consumer
    await consumer.stop()
