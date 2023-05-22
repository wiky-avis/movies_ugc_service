from enum import Enum
from typing import List

from pydantic import BaseModel


class EventType(str, Enum):
    ADDED = "added"
    DELETED = "deleted"


class UserBookmark(BaseModel):
    user_id: str
    film_id: str
    event_type: EventType = EventType.ADDED
    ts: str


class UserBookmarkResponse(BaseModel):
    film_ids: List[str] = list()
