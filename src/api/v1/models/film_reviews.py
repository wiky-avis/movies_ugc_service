from typing import Optional

from pydantic import BaseModel


class AddFilmReviewInput(BaseModel):
    film_id: str
    title: str
    body: str


class ReviewModel(BaseModel):
    film_id: Optional[str] = None
    review_id: str
    user_id: str
    review_title: str
    review_body: str
    created_dt: str
    likes: int = 0
    dislikes: int = 0
