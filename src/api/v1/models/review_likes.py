from enum import Enum

from pydantic import BaseModel


class EventType(str, Enum):
    LIKE = "like"
    DISLIKE = "dislike"


class ReviewLikeModel(BaseModel):
    review_id: str
    user_id: str
    event_type: EventType
