from pydantic import BaseModel


class AddFilmReviewSchema(BaseModel):
    title: str
    body: str
