from enum import Enum

from pydantic import BaseModel


class LikeEventType(str, Enum):
    LIKE = "like"
    DISLIKE = "dislike"


class ReviewLikeModel(BaseModel):
    review_id: str
    user_id: str
    event_type: LikeEventType


class ReviewLikeInput(BaseModel):
    review_id: str
