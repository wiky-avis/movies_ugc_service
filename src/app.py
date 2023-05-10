import sys

import uvicorn as uvicorn
from fastapi import FastAPI

# from src.api.v1.endpoints import view_progress
from src.brokers.kafka_producer import KafkaProducer
from src.containers import Container
from src.settings import logger, settings


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    app = FastAPI(
        on_startup=[
            KafkaProducer.setup,
        ],
        on_shutdown=[
            KafkaProducer.close,
        ],
        title="test",
        openapi_url="/openapi.json",
        docs_url="/swagger",
        openapi_prefix="",
    )
    app.container = container

    # app.include_router(view_progress.router, prefix="/api/v1")

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
