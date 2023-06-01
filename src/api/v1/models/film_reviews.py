from pydantic import BaseModel


class AddFilmReviewInput(BaseModel):
    title: str
    body: str


class ReviewList(BaseModel):
    review_id: str
    user_id: str
    review_title: str
    review_body: str
    created_dt: str
