import pytest
import pytest_asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, TopicPartition

from src.settings.kafka import KafkaConsumerSettings, KafkaProduserSettings


@pytest.fixture(scope="session")
def producer_settings():
    settings = KafkaProduserSettings()
    # settings.bootstrap_servers = "localhost:9092"
    
    return settings


@pytest.fixture(scope="session")
def consumer_settings():
    settings = KafkaConsumerSettings()
    # settings.bootstrap_servers = "localhost:9092"
    
    return settings


@pytest_asyncio.fixture(scope="session")
async def event_producer(producer_settings):
    producer = AIOKafkaProducer(
        bootstrap_servers=producer_settings.bootstrap_servers
    )
    await producer.start()
    yield producer
    await producer.stop()


@pytest_asyncio.fixture(scope="session")
async def event_consumer(event_loop, consumer_settings):
    consumer = AIOKafkaConsumer(
        consumer_settings.topic_name,
        loop=event_loop,
        bootstrap_servers=consumer_settings.bootstrap_servers,
        auto_offset_reset="latest",
    )
    await consumer.start()
    yield consumer
    await consumer.stop()