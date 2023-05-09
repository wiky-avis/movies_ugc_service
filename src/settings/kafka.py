from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class BaseKafkaSettings(BaseSettings):
    bootstrap_servers: str = "localhost:9091"

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


class KafkaProduserSettings(BaseKafkaSettings):
    topic_name: str = Field(env="PRODUCER_TOPIC_NAME", default="my_topic")


class KafkaConsumerSettings(BaseKafkaSettings):
    topic_name: str = Field(env="CONSUMER_TOPIC_NAME", default="my_topic")
    timeout_ms: int = Field(env="CONSUMER_TIMEOUT_MS", default=1000)
    max_records: Optional[int] = Field(env="CONSUMER_MAX_RECORDS")
