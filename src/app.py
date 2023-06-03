import sys

import sentry_sdk
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from sentry_sdk.integrations.fastapi import FastApiIntegration

from src.api import v1
from src.brokers.kafka_producer import KafkaProducer
from src.common.db import MongoDbConnector
from src.common.tracer import configure_tracer
from src.containers import Container
from src.middleware.request_id import RequestIdMiddleware
from src.settings import logger, settings


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    if settings.enable_sentry:
        sentry_sdk.init(integrations=[FastApiIntegration()])

    app = FastAPI(
        on_startup=[KafkaProducer.setup, MongoDbConnector.setup],
        on_shutdown=[KafkaProducer.close, MongoDbConnector.close],
        title="test",
        openapi_url="/openapi.json",
        docs_url="/swagger",
        openapi_prefix="",
    )
    app.container = container  # type: ignore

    if settings.enable_tracer:
        configure_tracer(app)

    app.include_router(v1.router)

    add_pagination(app)

    # app.middleware("http")(RequestIdMiddleware())

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.project_host,
        port=settings.project_port,
        log_config=logger.LOGGING,
        reload=True,
    )
