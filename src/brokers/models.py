from pydantic import BaseModel

from src.api.v1.models.bookmarks import EventType


class UserViewProgressEventModel(BaseModel):
    user_id: str
    film_id: str
    viewed_frame: int
    ts: str


class UserBookmarkEventModel(BaseModel):
    user_id: str
    film_id: str
    event_type: EventType = EventType.ADDED
    ts: str


class FilmReviewEventModel(BaseModel):
    user_id: str
    film_id: str
    review_id: str
    review_title: str
    review_body: str
    ts: str
