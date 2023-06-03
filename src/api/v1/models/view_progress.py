from typing import Optional

from pydantic import BaseModel, StrictInt


class SaveViewProgressInput(BaseModel):
    film_id: str
    viewed_frame: StrictInt


class ViewProgress(BaseModel):
    user_id: str
    film_id: str
    viewed_frame: int
    ts: Optional[str] = None


class FilmView(BaseModel):
    film_id: str
    count: int
