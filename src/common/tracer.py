from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import Span, TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

from src.settings import settings


def request_hook(span: Span, scope) -> None:
    headers = dict(
        (i.decode("UTF-8"), j.decode("UTF-8")) for i, j in scope["headers"]
    )
    request_id = headers.get("x-request-id")
    if span and span.is_recording():
        span.set_attribute("http.request_id", request_id)  # type: ignore


def configure_tracer(app: FastAPI) -> None:
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create(
                attributes={
                    SERVICE_NAME: "ugc_app",
                },
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(  # type: ignore
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.jaeger_host,
                agent_port=settings.jaeger_port,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(  # type: ignore
        BatchSpanProcessor(ConsoleSpanExporter())
    )
    FastAPIInstrumentor().instrument_app(
        app=app,
        excluded_urls="/swagger.json,/swagger,/swaggerui/*",
        server_request_hook=request_hook,  # type: ignore
    )
