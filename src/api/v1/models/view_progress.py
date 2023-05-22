from pydantic import BaseModel, StrictInt


class SaveViewProgressInput(BaseModel):
    viewed_frame: StrictInt


class ViewProgress(BaseModel):
    user_id: str
    film_id: str
    viewed_frame: int
    ts: str
