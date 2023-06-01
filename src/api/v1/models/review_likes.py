from enum import Enum


class EventType(str, Enum):
    LIKE = "like"
    DISLIKE = "dislike"
