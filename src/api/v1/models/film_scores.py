from enum import Enum

from pydantic import BaseModel, Field


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
    score: int = Field(..., ge=1, le=10)


class FilmAvgScore(BaseModel):
    film_id: str
    avg_score: int
    num_scores: int
