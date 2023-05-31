from pydantic import BaseModel


class ReviewList(BaseModel):
    review_id: str
    user_id: str
    review_title: str
    review_body: str
