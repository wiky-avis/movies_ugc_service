from pydantic import BaseModel


class AdditionalResponseModel(BaseModel):
    detail: list[str]


class NotFound(AdditionalResponseModel):
    pass


class InternalServerError(AdditionalResponseModel):
    pass
