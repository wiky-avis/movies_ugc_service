from typing import Any

from pydantic import BaseModel


class AddFilmReviewResponse(BaseModel):
    success: bool = True
    content: Any = None


class AdditionalResponseModel(BaseModel):
    detail: list[str]


class NotFound(AdditionalResponseModel):
    pass


class InternalServerError(AdditionalResponseModel):
    pass
