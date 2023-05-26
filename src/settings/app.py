from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class AppSettings(BaseSettings):
    debug: bool = Field(env="DEBUG", default=False)

    project_host: str = Field(env="PROJECT_HOST", default="0.0.0.0")
    project_port: int = Field(env="PROJECT_PORT", default=8000)

    log_format: str = Field(env="LOG_FORMAT", default="INFO")

    enable_sentry: bool = Field(env="ENABLE_SENTRY", default=False)

    enable_tracer: bool = Field(env="ENABLE_TRACER", default=False)
    jaeger_host: str = Field(env="JAEGER_HOST", default="jaeger")
    jaeger_port: int = Field(env="JAEGER_PORT", default=6831)

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


settings = AppSettings()
