from enum import Enum

from pydantic import BaseModel


class EventType(str, Enum):
    ADDED = "added"
    DELETED = "deleted"


class UserBookmark(BaseModel):
    user_id: str
    film_id: str
    event_type: EventType = EventType.ADDED
    ts: str
