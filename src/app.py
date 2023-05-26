import sys
from uuid import uuid4

import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from src.api import v1
from src.brokers.kafka_producer import KafkaProducer
from src.common.db import MongoDbConnector
from src.common.tracer import configure_tracer
from src.containers import Container
from src.settings import logger, settings


def init_sentry():
    if settings.enable_sentry:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration

        sentry_sdk.init(integrations=[FastApiIntegration()])


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    init_sentry()

    app = FastAPI(
        on_startup=[KafkaProducer.setup, MongoDbConnector.setup],
        on_shutdown=[KafkaProducer.close, MongoDbConnector.close],
        title="test",
        openapi_url="/openapi.json",
        docs_url="/swagger",
        openapi_prefix="",
    )
    app.container = container  # type: ignore
    add_pagination(app)

    if settings.enable_tracer:
        configure_tracer(app)

    app.include_router(v1.router)

    return app


app = create_app()


@app.middleware("http")
async def validate_request_id_header(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id")
    if request_id is None:
        if settings.debug:
            request.headers.__dict__["_list"].append(
                (
                    "x-request-id".encode(),
                    f"{str(uuid4())}".encode(),
                )
            )
        else:
            return JSONResponse(
                content={"message": "Missing X-Request-Id header"},
                status_code=400,
            )

    response = await call_next(request)
    return response


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.project_host,
        port=settings.project_port,
        log_config=logger.LOGGING,
        reload=True,
    )
