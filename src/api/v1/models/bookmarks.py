from enum import Enum
from typing import List

from pydantic import BaseModel


class EventType(str, Enum):
    ADDED = "added"
    DELETED = "deleted"


class UserBookmarkResponse(BaseModel):
    film_ids: List[str] = list()
