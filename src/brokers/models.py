from pydantic import BaseModel

from src.api.v1.models.bookmarks import BookmarkEventType
from src.api.v1.models.review_likes import LikeEventType


class UserViewProgressEventModel(BaseModel):
    user_id: str
    film_id: str
    viewed_frame: int
    ts: str


class UserBookmarkEventModel(BaseModel):
    user_id: str
    film_id: str
    event_type: BookmarkEventType = BookmarkEventType.ADDED
    ts: str


class FilmReviewEventModel(BaseModel):
    user_id: str
    film_id: str
    review_id: str
    review_title: str
    review_body: str
    ts: str


class UserReviewLikeEventModel(BaseModel):
    user_id: str
    review_id: str
    action: LikeEventType = LikeEventType.LIKE
    ts: str
