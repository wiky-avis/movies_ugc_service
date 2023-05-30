from pydantic import BaseModel


class FilmReview(BaseModel):
    user_id: str
    film_id: str
    review_text: str
    ts: str


class ReviewList(BaseModel):
    user_id: str
    review_text: str
