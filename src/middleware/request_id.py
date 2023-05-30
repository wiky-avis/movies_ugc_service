from uuid import uuid4

from fastapi import Request
from fastapi.responses import JSONResponse

from src.settings import settings


class RequestIdMiddleware:
    async def __call__(self, request: Request, call_next):
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
