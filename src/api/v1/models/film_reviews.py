from pydantic import BaseModel


class Review(BaseModel):
    user_id: str
    film_id: str
    review_id: str
    review_title: str
    review_body: str


class ReviewList(BaseModel):
    review_id: str
    user_id: str
    review_title: str
    review_body: str
