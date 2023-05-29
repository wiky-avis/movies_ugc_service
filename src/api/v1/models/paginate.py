# mypy: disable-error-code="misc"
from fastapi_pagination import Page
from pydantic import Field


Page = Page.with_custom_options(
    size=Field(20, ge=1, le=100),
)
