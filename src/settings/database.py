from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    host: str = Field(default="clickhouse")

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"
