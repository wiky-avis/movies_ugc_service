from enum import Enum
from typing import List

from pydantic import BaseModel


class BookmarkEventType(str, Enum):
    ADDED = "added"
    DELETED = "deleted"


class UserBookmarkInput(BaseModel):
    film_id: str


class UserBookmarkModel(BaseModel):
    film_id: str
    user_id: str
    event_type: BookmarkEventType = BookmarkEventType.ADDED


class UserBookmarkResponse(BaseModel):
    film_ids: List[str] = list()
