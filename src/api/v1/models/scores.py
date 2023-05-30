from enum import Enum

from pydantic import BaseModel, StrictInt


class ScoreEventType(str, Enum):
    SET = "set"
    DELETE = "delete"


class UserFilmScore(BaseModel):
    user_id: str
    film_id: str
    score: int
    event_type: ScoreEventType = ScoreEventType.SET
    ts: str


class SetFilmScoreInput(BaseModel):
    score: StrictInt


class GetTopFilmsScoreInput(BaseModel):
    limit: StrictInt
