from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class BaseKafkaSettings(BaseSettings):
    bootstrap_servers: str = Field(env="KAFKA_SERVER", default="broker:9092")
    default_topic_name: str = Field(
        env="DEFAULT_TOPIC_NAME", default="default-topic"
    )

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


class KafkaProducerSettings(BaseKafkaSettings):
    default_topic_name: str = Field(
        env="DEFAULT_TOPIC_NAME", default="default-topic"
    )


class KafkaConsumerSettings(BaseKafkaSettings):
    timeout_ms: int = Field(env="CONSUMER_TIMEOUT_MS", default=1000)
    max_records: Optional[int] = Field(
        env="CONSUMER_MAX_RECORDS", default=None
    )


class KafkaTopicNames(BaseSettings):
    view_progress_topic: str = Field(
        env="VIEW_PROGRESS_TOPIC_NAME", default="progress-topic"
    )
    bookmarks_topic: str = Field(
        env="BOOKMARKS_TOPIC_NAME", default="bookmarks-topic"
    )
    film_score_topic: str = Field(
        env="FILM_SCORE_TOPIC_NAME", default="film-score-topic"
    )

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


kafka_producer_settings = KafkaProducerSettings()
kafka_consumer_settings = KafkaConsumerSettings()
kafka_topic_names = KafkaTopicNames()
