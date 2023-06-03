from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ScoreEventType(str, Enum):
    SET = "set"
    DELETE = "delete"


class UserFilmScore(BaseModel):
    user_id: str
    film_id: str
    score: int
    event_type: Optional[ScoreEventType] = None
    ts: Optional[str] = None


class SetFilmScoreInput(BaseModel):
    film_id: str
    score: int = Field(ge=1, le=10)


class FilmAvgScore(BaseModel):
    film_id: str
    avg_score: float
    num_scores: int
